# 7. Autonomous Decisions and Manipulation

:::{admonition} Session 7
:class: note

Monday, 26 October 2026, 17:35 – 19:00
:::

{{ common }}

You can now navigate, perceive and localize. What is missing is the thing that
decides *what to do next* — and what to do when a step fails. That layer is the
difference between a robot that follows instructions and a robot that completes
a mission.

## Learning objectives

After this session you can:

- model a mission as a finite state machine, including its failure paths;
- explain how a behavior tree differs and when it is the better fit;
- build a small state machine in RAFCON;
- describe what PlanSys2 and Golog++ add over both;
- move a manipulator with MoveIt and explain the pick-and-place sequence.

## Prerequisites

[Session 6](06-navigation.md). Your robot can navigate to a goal, and you have
sent one from code with an action client.

## The problem

A mission sounds simple written down:

> Drive to the shelf, find the marked object, pick it up, bring it to the drop
> zone.

Now consider what actually happens. Navigation fails because someone left a
box in the corridor. The object is not where it was expected. The gripper
closes on nothing. The battery runs low halfway through.

A script cannot handle this. `drive(); detect(); grasp(); deliver()` has no
answer to "what if `detect` finds nothing?" other than crashing. **Every real
mission is mostly failure handling**, and the tools in this session exist to
make that structure explicit instead of buried in nested `if` statements.

## Finite state machines

A **finite state machine** is the oldest and clearest answer: the robot is
always in exactly one *state*, and *transitions* move it to the next one
depending on the outcome.

```text
        ┌──────────────┐
        │     IDLE     │
        └──────┬───────┘
               │ start
               ▼
        ┌──────────────┐  failure   ┌──────────────┐
        │  NAVIGATE    ├───────────►│    ABORT     │
        └──────┬───────┘            └──────────────┘
               │ arrived                    ▲
               ▼                            │
        ┌──────────────┐  not found         │
        │   DETECT     ├────────────────────┤
        └──────┬───────┘                    │
               │ found                      │
               ▼                            │
        ┌──────────────┐  grasp failed      │
        │    GRASP     ├────────────────────┘
        └──────┬───────┘
               │ holding
               ▼
        ┌──────────────┐
        │   DELIVER    │
        └──────────────┘
```

What makes this useful is not the happy path down the left side — it is that
every state has a named exit for failure. Drawing the diagram forces you to
answer "and what if this does not work?" for every single step.

:::{tip}
Draw the state machine on paper *before* writing code. Ten minutes with a pen
routinely saves an evening, because the awkward question — what happens if the
gripper closes on nothing? — surfaces while it is still cheap to answer.
:::

**Strengths**: obvious, debuggable, easy to explain to someone else.

**Weakness**: it grows badly. Adding a state that any other state might
transition to means adding transitions everywhere, and a 30-state machine
becomes a tangle.

## Behavior trees

A **behavior tree** attacks that scaling problem. Instead of a graph of states
with explicit transitions, you build a *tree* that is walked, top to bottom,
many times a second. Each node returns `SUCCESS`, `FAILURE`, or `RUNNING`.

The structure comes from a small set of control nodes:

`Sequence`
: run children in order; fail as soon as one fails. "Do all of these."

`Fallback` (or Selector)
: try children in order; succeed as soon as one succeeds. "Try these until one
  works."

`Parallel`
: run children simultaneously

`Decorator`
: modify a child — retry it N times, invert its result, add a timeout

```text
              Fallback
             /        \
      Sequence          Recovery
     /    |    \
Navigate Detect Grasp
```

Read that as: *try to do the whole sequence; if any part fails, run recovery.*
The recovery logic appears once, not once per state — that is the scaling
advantage.

Because the tree is re-evaluated continuously, it also reacts naturally: a
high-priority branch such as "if the battery is critical, go home" is checked
on every tick without wiring a transition from every other state.

You have already used one. Nav2's BT Navigator is a behavior tree, and
`navigate_w_replanning_and_recovery.xml` is exactly the pattern above: follow
the path, and on failure clear the costmap, spin, back up, and re-plan.

```{list-table}
:header-rows: 1
:widths: 25 37 38

* -
  - State machine
  - Behavior tree
* - Structure
  - Graph of states and transitions
  - Tree, ticked repeatedly
* - Failure handling
  - An explicit transition per state
  - One shared fallback branch
* - Reactivity
  - Only at transitions
  - Every tick
* - Scales to
  - Small, well-understood missions
  - Large missions with shared recovery
* - Easiest to
  - Explain and step through
  - Extend without touching what exists
```

Neither is better in general. For the hackathon mission, a state machine is
usually the faster thing to get working; a behavior tree is what you reach for
when the recovery logic starts repeating.

## RAFCON

[RAFCON](https://github.com/DLR-RM/RAFCON) is a graphical state machine editor
and execution engine developed at DLR. You build the machine by dragging states
and drawing transitions, and write the body of each state in Python.

```bash
rafcon
```

### The concepts

**Hierarchy states** are containers; they hold other states but no code of
their own. This is how a large machine stays readable — a state at the top
level can expand into a whole sub-machine.

**Execution states** contain the Python that actually does something. Each has
an `execute` function returning the name of an outcome:

```python
from std_msgs.msg import String


def execute(self, inputs, outputs, gvm):
    node = gvm.get_variable("new_ros2_node", True)
    publisher = node.create_publisher(String, '/chatter', 10)

    message = String()
    message.data = 'I am in State 1'
    publisher.publish(message)

    return "success"
```

**Outcomes** are the named exits from a state. `success` exists by default; add
your own (`not_found`, `timeout`, `grasp_failed`) through the *Logical Linkage*
widget. Outcomes are what the arrows in your paper diagram become.

**Input and output ports** pass typed values between states — one state
computes a pose, the next drives to it.

**Scoped variables** are shared within a container state, useful for a counter
across a loop.

**The Global Variable Manager (GVM)** shares values across the whole machine:

```python
gvm.set_variable("target_pose", pose)
pose = gvm.get_variable("target_pose")
```

### Interfacing with ROS 2

The pattern is: initialise **one** ROS 2 node at the start of the machine, put
it in the GVM, and have every state fetch it from there.

```python
node = gvm.get_variable("new_ros2_node", True)
```

Subscribing inside a state works like anywhere else, with one critical
difference:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Listener(Node):

    def __init__(self):
        super().__init__('listener')
        self.subscription = self.create_subscription(
            String, '/chatter', self.callback, 10)
        self.done = False
        self.count = 0
        self.maximum = 1

    def callback(self, msg):
        print(f'I heard: {msg.data}')
        self.count += 1
        if self.count >= self.maximum:
            self.done = True


def execute(self, inputs, outputs, gvm):
    listener = Listener()
    listener.maximum = inputs["count"]
    while not listener.done:
        rclpy.spin_once(listener)
    return "success"
```

:::{danger}
Use `rclpy.spin_once()` in a loop with a termination condition — never
`rclpy.spin()`, and **never** `rclpy.shutdown()`. `spin()` blocks forever and
the state never exits; `shutdown()` kills the node the whole state machine
shares, and everything after it fails.

Every state that waits for something must have a way to stop waiting. A state
with no exit condition is a hung mission.
:::

## PlanSys2 and Golog++

State machines and behavior trees say *how*. Planning says *what*, and works
out the how itself.

**[PlanSys2](https://plansys2.github.io/)** is a ROS 2 planning system based on
PDDL. You describe the world in terms of predicates ("the robot is at the
shelf", "the gripper is empty") and actions with preconditions and effects.
Given a goal, the planner produces a sequence of actions that reaches it —
and re-plans if the world turns out differently.

**[Golog++](https://github.com/MASKOR/gologpp)** is an action language,
developed with involvement from the institute, that sits between the two: you
write a partially specified procedure and leave the rest to the planner,
combining programmer control with automated search.

The trade-off is straightforward. Planning adapts to situations you did not
anticipate — that is the whole appeal. It also needs a formal domain model,
which is real work, and it is harder to debug when it produces a plan you did
not expect.

For this course, know that these exist and what they are for. Both institute
teams use behavior trees or state machines for competition missions, because
predictability under time pressure matters more than flexibility.

:::{admonition} TODO-REVIEW
:class: todo-review

The source material references PlanSys2 and Golog++ by link only, without a
worked example or a tested installation procedure. Expert review is required
before this becomes a hands-on section.
:::

## Manipulation with MoveIt

{{ alert }} — the arm is on Spot; Robotino's gripper is a simpler custom
mechanism, covered on the
[Carologistics page](../platforms/carologistics-robotino.md).

[MoveIt 2](https://moveit.picknik.ai/) is the motion planning framework for
manipulators. It handles what makes arms hard: an arm has many joints, most
target poses have multiple valid joint configurations, and the arm must not
collide with the world or with itself.

The pieces:

**Inverse kinematics (IK)** — given where you want the gripper, compute the
joint angles that put it there. Often there are several answers, and sometimes
none.

**Motion planning** — given a start and goal configuration, find a collision-
free trajectory between them.

**Execution** — send that trajectory to the controllers.

### Trying it interactively

```bash
# Platform-specific -- check your platform page for the exact launch file
ros2 launch <your_moveit_config> moveit_launch.py
```

In RViz you can drag the interactive marker at the gripper to a target pose,
click **Plan**, inspect the trajectory, and click **Execute**.

Doing this by hand first is worth the time: you develop an intuition for what
the arm can and cannot reach, which makes the failures in code much less
mysterious.

:::{note}
If planning fails, the target is usually outside the arm's reachable workspace
or the pose would collide — with the environment or with the arm itself. Move
the target closer or change its approach angle. "No IK solution found" almost
always means "not physically reachable like that".
:::

### Pick and place

The canonical sequence, with a node per capability:

```python
import rclpy


def main():
    rclpy.init()

    gripper = GripperActionClient()
    navigator = NavigateToPoseActionClient()
    moveit = MoveGroupActionClient()

    # 1. Drive to the pick location
    navigator.send_goal(position=[0.433, 3.189, 0.520],
                        orientation=[0.0, 0.0, 0.707, 0.707])
    while not navigator.goal_done:
        rclpy.spin_once(navigator)

    # 2. Find the object -- its pose is published as a TF frame
    pose_node = GetPose("P")
    while pose_node.pose is None:
        rclpy.spin_once(pose_node)
    pose = pose_node.pose
    pose_node.destroy_node()

    # 3. Approach from slightly above rather than straight at it
    pose.position.z += 0.05

    # 4. Solve IK for that pose
    ik_solver = InverseKinematicsClient()
    target_angles = ik_solver.send_request(pose)
    ik_solver.destroy_node()
    if target_angles is None:
        return                      # unreachable -- handle this, do not crash

    # 5. Move, grasp, retract
    moveit.send_goal(target_angles)
    while not moveit.goal_done:
        rclpy.spin_once(moveit)

    gripper.send_goal("close")
    while not gripper.goal_done:
        rclpy.spin_once(gripper)

    # ... retract, navigate to the drop point, open the gripper ...

    rclpy.shutdown()
```

Three things this illustrates:

**Every step can fail.** `target_angles is None` is not an edge case, it is
Tuesday. The `if` that returns early is the beginning of the failure handling
that a state machine would make explicit.

**Approach poses matter.** Moving to 5 cm above the object and then descending
is far more reliable than driving straight at it, because it gives the planner
a collision-free approach direction.

**Each capability is its own node.** Navigation, IK, arm motion and gripper are
separate clients. That separation is exactly what lets you drop them into
RAFCON states or behavior tree nodes without rewriting them.

## Task

:::{admonition} Task: model and run a mission
:class: task

**Part 1 — Design it on paper.**

Design a state machine for this mission:

> Drive to a marked location, look for an ArUco marker, and if you find it,
> report its ID and return to the start. If you do not find it after 30
> seconds, return to the start and report failure.

Draw every state and every transition. For each state answer:

- what does it do?
- what are its possible outcomes?
- what data does it need from the previous state?
- what happens if it fails or takes too long?

**Part 2 — Implement it.**

Choose **one**:

- *RAFCON route*: build the machine in RAFCON. Start with the `/chatter`
  example from above to get comfortable with states, outcomes, transitions and
  ports, then build your mission.
- *Python route*: implement the same machine as a Python class with an explicit
  state variable and a transition table. Reuse the Nav2 action client from
  [session 6](06-navigation.md) and the marker detection from
  [session 4](04-perception.md).

Whichever you choose, the timeout and failure paths must actually work — that
is the point of the exercise.

**Part 3 — Break it deliberately.**

1. Run it with the marker present. It should succeed.
2. Run it with **no** marker. Does it time out and return home, or hang?
3. Block the robot's path. Does navigation failure propagate to your state
   machine, or does it wait forever?
4. Fix whatever you found.

**Part 4 (optional) — Manipulation.** {{ alert }}

In simulation, plan and execute an arm motion in RViz by hand. Then write a
node that moves the arm to a pose obtained from a TF frame.
:::

:::{admonition} Expected result
:class: result

A state machine that reaches its goal when everything works, **and** returns
home cleanly when the marker is missing or navigation fails — without hanging
and without a traceback.

Part 3 is the real deliverable. Almost every first attempt hangs on at least
one of those three cases; finding out which is the exercise.
:::

:::{dropdown} Hint: a minimal state machine in Python
:icon: light-bulb

```python
import time
from enum import Enum, auto


class State(Enum):
    IDLE = auto()
    NAVIGATE = auto()
    SEARCH = auto()
    RETURN = auto()
    DONE = auto()
    FAILED = auto()


class Mission:

    def __init__(self, node):
        self.node = node
        self.state = State.IDLE
        self.marker_id = None

    def step(self):
        if self.state is State.IDLE:
            self.state = State.NAVIGATE

        elif self.state is State.NAVIGATE:
            self.state = (State.SEARCH if self.navigate_to_target()
                          else State.FAILED)

        elif self.state is State.SEARCH:
            deadline = time.time() + 30.0
            while time.time() < deadline:
                if self.marker_id is not None:
                    self.state = State.RETURN
                    return
                self.spin_once()
            self.node.get_logger().warning('No marker found within 30 s')
            self.state = State.RETURN

        elif self.state is State.RETURN:
            self.state = (State.DONE if self.navigate_home() else State.FAILED)
```

Note that `SEARCH` transitions to `RETURN` whether or not it found the marker —
the mission always comes home. Whether it *succeeded* is a separate question
from whether it *finished*, and conflating the two is how robots get stranded.
:::

## Common mistakes

**A state with no way out.**
Waiting for something that never arrives, with no timeout. Every waiting state
needs a deadline.

**Failure is not propagated.**
The action client reports failure and the state machine transitions to the next
state anyway. Always check the result status.

**`rclpy.shutdown()` inside a state.**
Kills the shared node and everything after it. Never call it except at the very
end of the program.

**The state machine works and the robot does not.**
Your states never checked whether their actions succeeded — they just ran and
returned `success`.

**Only the happy path exists.**
The classic. If your diagram has no failure transitions, it is not finished.

**MoveIt cannot find a plan.**
The pose is unreachable or in collision. Try an approach pose above the target
first.

## Further reading

- [RAFCON documentation](https://rafcon.readthedocs.io/en/stable/concepts.html)
  and the [RAFCON repository](https://github.com/DLR-RM/RAFCON)
- [BehaviorTree.CPP](https://www.behaviortree.dev/) — the library Nav2 uses
- [Nav2 behavior trees](https://docs.nav2.org/behavior_trees/index.html)
- [PlanSys2](https://plansys2.github.io/) and its
  [behavior tree actions tutorial](https://plansys2.github.io/tutorials/docs/bt_actions.html)
- [MoveIt 2](https://moveit.picknik.ai/)
- [ROS 2 actions](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions.html)
