# Planning and manipulation approaches

{{ common }} {{ advanced }}

## What this topic is

Three tools beyond the state machine/behavior tree pattern from [Mission
logic](mission-logic.md): a graphical state machine editor (RAFCON), two
**planning** systems that decide *what* to do rather than being told *how*
(PlanSys2, Golog++), and motion planning for a physical arm (MoveIt 2).

## Why a robot needs it

[Mission logic's](mission-logic.md) state machines and behavior trees say
*how* — every transition, explicitly. A planner says *what*, and works out
the how itself; that trade-off matters once a mission has too many
situations to enumerate by hand, or once "the mission" includes moving a
physical arm rather than just navigating.

## How it works

(rafcon-a-graphical-state-machine-tool)=
### RAFCON — a graphical state machine tool

{{ alert }} [RAFCON](https://github.com/DLR-RM/RAFCON) is a graphical state
machine editor and execution engine from DLR, used by the ALeRT team. You
drag states and draw transitions; each state's body is Python:

```python
def execute(self, inputs, outputs, gvm):
    node = gvm.get_variable("new_ros2_node", True)
    publisher = node.create_publisher(String, '/chatter', 10)
    publisher.publish(String(data='I am in State 1'))
    return "success"
```

The pattern that matters: initialise **one** ROS 2 node at the start of the
machine, put it in the shared Global Variable Manager, and have every state
fetch it from there — never call `rclpy.shutdown()` inside a state, or every
state after it fails.

Full walkthrough and the ROS 2 subscription pattern:
[ALeRT/Spot platform page](../../platforms/alert-spot.md#high-level-control).

### PlanSys2 and Golog++ — planning instead of programming the mission

**[PlanSys2](https://plansys2.github.io/)** is a ROS 2 planning system based
on PDDL. You describe the world as predicates ("robot is at the shelf",
"gripper is empty") and actions with preconditions and effects; given a
goal, the planner produces — and re-plans — a sequence of actions.

**[Golog++](https://github.com/MASKOR/gologpp)** is an action language,
developed with institute involvement, sitting between the two: you write a
partially specified procedure and leave the rest to the planner.

**How they compare to a state machine or behavior tree:**

```{list-table}
:header-rows: 1
:widths: 28 24 24 24

* -
  - State machine
  - Behavior tree
  - Planner (PlanSys2 / Golog++)
* - You specify
  - Every transition
  - Tree structure + leaves
  - Goal + available actions
* - Adapts to
  - Nothing unplanned
  - Known failure patterns
  - Situations you did not anticipate
* - Cost
  - Grows with states
  - Grows with tree size
  - A formal domain model, up front
* - Debugging
  - Step through states
  - Step through ticks
  - Read the plan the solver chose
```

Planning is the right tool when the world is too varied to enumerate in
advance. It is not part of this course's hands-on track: neither institute
team currently runs PlanSys2 or Golog++ for competition missions — both use
state machines or behavior trees, because predictable behaviour under time
pressure matters more than adapting to the unexpected. Treat this as
orientation for further reading, not a tool this course walks through
building.

### MoveIt and manipulation

{{ alert }} Where [Mission logic's](mission-logic.md) general decision
principles connect to a physical arm:
[MoveIt 2](https://moveit.picknik.ai/) solves inverse kinematics and
collision-free motion planning. A pick-and-place sequence is exactly the
state-machine pattern from [Mission logic](mission-logic.md), with `GRASP`
and `RELEASE` as states with their own failure exits (a `None`
inverse-kinematics result is "unreachable," not a crash). Full example on
the [ALeRT/Spot platform
page](../../platforms/alert-spot.md#manipulation-with-moveit).
{{ carologistics }} Robotino's simpler custom gripper is covered on the
[Carologistics platform page](../../platforms/carologistics-robotino.md#gripper).

## How ALeRT applies it

{{ alert }} {{ documented }} All three approaches above are ALeRT-specific:
RAFCON for high-level mission control, and MoveIt 2 for the arm — see the
[platform page's high-level control
section](../../platforms/alert-spot.md#high-level-control) and
[manipulation-with-MoveIt
section](../../platforms/alert-spot.md#manipulation-with-moveit).

## How Carologistics applies it

{{ carologistics }} {{ documented }} Carologistics uses neither PlanSys2
nor Golog++ nor RAFCON for competition missions — the team's central
[`expertino-rcll`](../../platforms/carologistics-robotino.md#key-repositories)
agent and Robotino's [custom
gripper](../../platforms/carologistics-robotino.md#gripper) use the
state-machine/behavior-tree pattern from [Mission
logic](mission-logic.md) instead, for the same predictability-under-time-pressure
reason explained above.

## Next subtopic

[Practical exercise](practical-exercise.md) — implement a mission that
recovers instead of hanging when a step fails.

## Sources

- [RAFCON documentation](https://rafcon.readthedocs.io/en/stable/concepts.html)
- [PlanSys2](https://plansys2.github.io/) and its
  [behavior tree actions tutorial](https://plansys2.github.io/tutorials/docs/bt_actions.html)
- [MoveIt 2](https://moveit.picknik.ai/)
