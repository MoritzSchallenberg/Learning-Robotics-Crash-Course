# 7. Autonomous Decisions and Manipulation

{{ common }}

You can navigate, perceive and localize. What is missing is the thing that
decides *what to do next* — and what to do when a step fails. This module's
core is that decision layer, not any one tool for building it.

## Overview

You will learn to model a mission as a sequence of states with explicit
failure exits, see what a behavior tree adds over a plain state machine,
and implement a mission that recovers or reports cleanly instead of hanging
when a step fails.

## Learning objectives

By the end of this module you can:

1. model a small mission as a sequence of states with explicit failure
   exits;
2. explain what a behavior tree adds over a plain state machine;
3. implement and run a mission with at least one failure or retry branch.

## Prerequisites

[Module 6](06-navigation.md) completed — you can send a navigation goal
from code and read its result.

## Core concepts

### Why a script is not enough

`drive(); detect(); grasp(); deliver()` has no answer to "what if `detect`
finds nothing?" other than crashing. **Every real mission is mostly failure
handling** — the tools below exist to make that structure explicit instead
of buried in nested `if` statements.

### Finite state machines

The robot is always in exactly one **state**; **transitions** move it to the
next one depending on the outcome.

```{figure} ../_static/images/diagrams/08-state-machine-behavior-tree.svg
:alt: Left, a finite state machine with states Idle, Navigate, Detect and Deliver in sequence, each with its own explicit failure transition to a shared Abort state. Right, a behavior tree with a Fallback root whose first child is a Sequence of Navigate, Detect and Deliver, and whose second child is a Recovery action used if the sequence fails.
:width: 100%

A state machine needs one failure transition per state; a behavior tree
needs one shared recovery branch.
```

What makes the left side useful is not the happy path — it is that **every
state has a named exit for failure**. Drawing it forces the question "and
what if this does not work?" for every step.

### Behavior trees, in contrast

A tree, re-evaluated many times a second, built from a few control nodes:
**Sequence** (run children in order, fail on first failure — "do all of
these"), **Fallback** (try children in order, succeed on first success —
"try these until one works"). Nav2's BT Navigator, which you already used
in module 6, is exactly this pattern.

```{list-table}
:header-rows: 1
:widths: 30 35 35

* -
  - State machine
  - Behavior tree
* - Failure handling
  - One transition per state
  - One shared fallback branch
* - Scales to
  - Small, well-understood missions
  - Larger missions with shared recovery
* - Easiest to
  - Explain and step through
  - Extend without touching existing states
```

For the practical task below, a state machine is the faster thing to get
working.

## Guided example

Build and deliberately break a minimal three-state mission before tackling
the full one, so the failure mode is familiar rather than surprising:

```python
import time
from enum import Enum, auto


class State(Enum):
    IDLE = auto()
    WAIT_FOR_INPUT = auto()
    DONE = auto()


def run_mission(get_input, timeout_s=5.0):
    state = State.IDLE
    deadline = None

    while state is not State.DONE:
        if state is State.IDLE:
            state = State.WAIT_FOR_INPUT
            deadline = time.time() + timeout_s

        elif state is State.WAIT_FOR_INPUT:
            if get_input() is not None:
                state = State.DONE
            elif time.time() > deadline:
                print('timed out waiting for input')
                state = State.DONE
            else:
                time.sleep(0.1)

    print('mission finished')
```

Run it with a `get_input` that always returns `None` — it should print
"timed out waiting for input" after five seconds and then finish, not hang
forever. Now comment out the `elif time.time() > deadline:` branch and run
it again: the loop never exits, because `WAIT_FOR_INPUT` has no way out
when its condition is never met. This is the exact failure mode the
practical task below asks you to avoid in a real mission — a state with no
timeout is a state that can hang forever.

## Practical task

### Goal
Implement a mission — *navigate to a point, look for a marker, report* —
that visibly recovers instead of hanging when the marker is not found.

### Starting point
A new package (call it `mission_demo`, or reuse an existing one from
earlier modules) into which you copy two pieces of code you already have
working: the navigation action client from
[module 6](06-navigation.md#advanced-topics), and the marker-detection
pattern from [module 4](04-perception/index.md). Wrap each as a small
helper class or function your state machine can call — you are writing
the state machine itself in this task, not the underlying clients, so
reuse rather than rewrite them.

### Steps
1. On paper, draw states: `IDLE → NAVIGATE → SEARCH → RETURN → DONE`, plus a
   `FAILED` exit from `NAVIGATE`.
2. Decide `SEARCH`'s timeout (30 s is reasonable) and what happens on
   timeout — it must still transition, not hang, exactly as in the guided
   example above.
3. Implement the state machine in Python using the provided helper classes
   (a `State` enum plus a `step()` method, the same shape as the guided
   example, is enough).
4. Run it with the marker **present**. Confirm it completes.
5. Run it with **no marker** in the search area. Confirm it does not hang.
6. Block the navigation goal (place an obstacle across the only path).
   Confirm `NAVIGATE`'s failure exit actually fires.
7. Fix whatever you found in steps 5–6.

## Expected result

The mission finishes in all three cases — success, marker not found,
navigation blocked — with no run lasting longer than the timeout you chose,
and no traceback.

## Verification

```bash
ros2 topic echo /mission_status
```

Reports `succeeded`, `marker_not_found` or `navigation_failed` — three
distinct outcomes, never silence.

## Common problems

- **A state with no way out** — waiting for something with no timeout. Every
  waiting state needs a deadline, exactly like the guided example's broken
  version.
- **Failure not propagated** — the action client reports failure and the
  code moves to the next state anyway; always check the result status.
- **Only the happy path exists** — the most common first draft. If your
  diagram has no failure transitions, it is not finished.
- **`rclpy.shutdown()` inside a state.** Kills the shared node and
  everything after it. Only call it once, at the very end of the program.
- **The state machine "works" and the robot does not.** States ran and
  returned `success` without checking whether their action actually
  succeeded.

## Optional extensions

{{ optional }}

Add a fourth state that retries `SEARCH` once, from a slightly different
position, before giving up — the smallest possible recovery behaviour.

{{ simulation }} Failing "on purpose" is easier in simulation — remove the
marker from the scene, or block the path with a dragged object, exactly as
in [module 6](06-navigation.md#optional-extensions).

**Sketch the same mission as a behavior tree.** On paper, redraw your
practical task's `IDLE → NAVIGATE → SEARCH → RETURN → DONE` state machine
using this module's own Sequence and Fallback nodes instead of states and
transitions — one Sequence for the happy path, one Fallback wrapping the
whole thing with a recovery branch for `SEARCH`'s timeout. Compare the two
drawings side by side: which one made the failure-handling structure
clearer to draw, and which would be easier to extend with a sixth step
next month?

## Advanced topics

{{ advanced }}

:::{dropdown} RAFCON — a graphical state machine tool
:icon: light-bulb

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
[ALeRT/Spot platform page](../platforms/alert-spot.md#high-level-control).
:::

:::{dropdown} PlanSys2 and Golog++ — planning instead of programming the mission
:icon: light-bulb

State machines and behavior trees say *how*. **Planning** says *what*, and
works out the how itself.

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
:::

(moveit-and-manipulation)=
:::{dropdown} MoveIt and manipulation
:icon: light-bulb

{{ alert }} Where this module's general decision principles connect to a
physical arm: [MoveIt 2](https://moveit.picknik.ai/) solves inverse
kinematics and collision-free motion planning. A pick-and-place sequence is
exactly the state-machine pattern above, with `GRASP` and `RELEASE` as
states with their own failure exits (a `None` inverse-kinematics result is
"unreachable," not a crash). Full example on the
[ALeRT/Spot platform page](../platforms/alert-spot.md#manipulation-with-moveit).
{{ carologistics }} Robotino's simpler custom gripper is covered on the
[Carologistics platform page](../platforms/carologistics-robotino.md#gripper).
:::

## Try it on Spot

{{ alert }} {{ spotsim }}

Spot exposes its postures as **services** rather than topics or
actions — a natural fit, since standing up either succeeds or does not,
with no meaningful "progress" to report partway through:

```bash
ros2 service call /Spot/stand_up webots_spot_msgs/srv/SpotMotion
ros2 service call /Spot/sit_down webots_spot_msgs/srv/SpotMotion
ros2 service call /Spot/lie_down webots_spot_msgs/srv/SpotMotion
```

**Task**: build a state machine, exactly this module's core pattern,
for a small mission:

```text
stand → navigate → detect → return → sit
```

- `stand`: call `/Spot/stand_up`, wait for the response.
- `navigate`: reuse [module 6's](06-navigation.md#advanced-topics) action
  client to send a `NavigateToPose` goal.
- `detect`: reuse [module 4's](04-perception/index.md) marker detection,
  with a timeout — no marker found in N seconds is a **named** failure
  exit, not a hang.
- `return`: navigate back to the start pose.
- `sit`: call `/Spot/sit_down`.

Log every state transition (state, timestamp, why) — the same discipline
this module's own practical task and the [capstone
project's](hackathon.md#continue-learning) failure-mode planning both
depend on. Add at least one explicit timeout and one explicit failure
transition, not only the happy path.

:::{admonition} Optional: manipulation
:class: task

{{ advanced }} Add a sixth state that plans a MoveIt trajectory for
Spot's arm ([platform page](../platforms/alert-spot.md#manipulation-with-moveit))
once `detect` succeeds — with its own timeout, since "planning failed" is
a normal MoveIt outcome, not a crash (see [this module's Planning scene
dropdown](#planning-scene-and-collision-objects)).
:::

:::{danger}
{{ spotsupervised }} An automatic movement sequence on the **physical**
Spot — stand, walk, sit, with no human confirming each step — is a
supervised-only exercise, never something to run unattended as a first
attempt. Simulate the entire sequence in Webots until every state and
every failure exit has actually been exercised, before ever considering
it on real hardware, and then only with a trained team member present who
can reach the E-stop. See the [platform page's operating
sequence](../platforms/alert-spot.md#operating-the-physical-robot).
:::

## Continue learning

:::{dropdown} The blackboard: sharing data between behavior tree nodes — Next step
:icon: light-bulb

**What it is.** A behavior tree's **blackboard** is shared key-value
storage every node in the tree can read and write — how a `Detect` leaf
passes a marker's position to a later `NavigateToMarker` leaf, without
either node needing a direct reference to the other.

**Why it matters.** The behavior-tree dropdown above shows Sequence and
Fallback controlling *order*; the blackboard is how data actually flows
between the leaves that order controls — without it, a behavior tree can
only sequence actions, not pass results between them.

**Needs.** This module's core concepts on behavior trees.

**Try it.** {{ unverified }} — in a BehaviorTree.CPP or `py_trees` example,
write one leaf that writes a value to the blackboard and a second that
reads it, and confirm the second sees the first's value.

**Check.** The second leaf's read matches exactly what the first leaf
wrote, including after the tree re-ticks.

**Read more.** [BehaviorTree.CPP:
blackboard](https://www.behaviortree.dev/docs/tutorial-basics/tutorial_02_basic_ports)
:::

:::{dropdown} Action cancellation and preemption — Next step
:icon: light-bulb

**What it is.** Actively **cancelling** a running action
([module 2's](02-ros2.md#core-concepts) goal → feedback → result pattern)
before it finishes — e.g. abandoning a navigation goal because the mission
decided on a better one — rather than only ever waiting for natural
completion or timeout.

**Why it matters.** This module's practical task only ever *waits* for
`NAVIGATE` to finish or fail; a more responsive mission needs to actively
abandon a stale goal, the same responsiveness
[module 6's](06-navigation.md#advanced-topics) action client dropdown
introduces but does not use.

**Needs.** [Module 6's action client](06-navigation.md#advanced-topics)
example.

**Try it.** Send a navigation goal, wait two seconds, then call
`goal_handle.cancel_goal_async()` before it completes, and confirm — via
the action's result — that it reports cancelled rather than succeeded or
failed.

**Check.** The action's result status is explicitly "cancelled", distinct
from both "succeeded" and "aborted".

**Read more.** [ROS 2: actions —
canceling goals](https://docs.ros.org/en/humble/Tutorials/Intermediate/Writing-an-Action-Server-Client/Py.html)
:::

:::{dropdown} Lifecycle-controlled subsystems — Intermediate
:icon: light-bulb

**What it is.** Using a mission's state machine to actively control
subsystem **lifecycle** transitions
([module 2's](02-ros2.md#continue-learning) lifecycle-node topic) — e.g.
only activating a perception pipeline once the mission actually reaches a
`SEARCH` state, rather than every subsystem running full-time from
start-up.

**Why it matters.** This saves real compute and power on a resource-limited
onboard computer, and makes a subsystem's "is it supposed to be doing
anything right now" question answerable from mission state alone.

**Needs.** [Module 2's lifecycle
nodes](02-ros2.md#continue-learning) and this module's practical task.

**Try it.** Convert your practical task's marker detector into a lifecycle
node, and have the `SEARCH` state call `ros2 lifecycle set` to activate it
on entry and deactivate it on exit.

**Check.** `ros2 lifecycle get` on the detector reports `inactive` outside
`SEARCH` and `active` only while the mission is actually in that state.

**Read more.** [ROS 2: managed
nodes](https://docs.ros.org/en/humble/Concepts/Intermediate/About-Ros2-Managed-Nodes.html)
:::

:::{dropdown} Mission monitoring — Intermediate
:icon: light-bulb

**What it is.** A separate node that observes a mission's status
transitions and logs them with timing, without participating in the
mission itself — you will meet exactly this pattern as the optional
**Mission monitoring node** on the
[capstone project page](hackathon.md#mission-monitoring-node).

**Why it matters.** Debugging a mission after the fact needs a record of
what it actually did and when; building that as a separate observer keeps
the mission's own state machine simple and unburdened by logging detail.

**Needs.** This module's practical task, publishing `/mission_status`.

**Try it.** Write a small node that subscribes to `/mission_status`, times
how long the mission spends in each reported state, and prints a summary
when the mission finishes.

**Check.** The summary's total duration matches your own stopwatch timing
of one run, within a second or two.

**Read more.** [Capstone project: mission monitoring
node](hackathon.md#mission-monitoring-node) has a complete, runnable
example.
:::

(planning-scene-and-collision-objects)=
:::{dropdown} Planning scene and collision objects — Advanced
:icon: light-bulb

{{ alert }} **What it is.** MoveIt 2's **planning scene** is its model of
everything the arm must avoid — the robot itself, and **collision
objects** you add to represent the environment (a table, a shelf, the
object being grasped). Motion planning fails deliberately rather than
producing a colliding trajectory if the scene says a path is blocked.

**Why it matters.** A pick-and-place sequence
([the MoveIt dropdown above](#moveit-and-manipulation)) that plans without
telling MoveIt about the table in front of the robot will happily plan a
path *through* that table — the planning scene is what prevents that.

**Needs.** [The MoveIt and manipulation
dropdown](#moveit-and-manipulation) above.

**Try it.** {{ unverified }} — add a box collision object to the planning
scene representing a table surface, then request a motion plan to a pose
that would require passing through it, and confirm planning fails or
routes around it instead of through it.

**Check.** The same goal pose plans successfully once the collision object
is removed, and fails or replans once it is present — a direct before/after
comparison.

**Read more.** [MoveIt 2: planning scene and collision
objects](https://moveit.picknik.ai/main/doc/examples/planning_scene/planning_scene_tutorial.html)
:::

:::{dropdown} A simple pick-and-place pipeline — Advanced
:icon: light-bulb

{{ alert }} **What it is.** Chaining the pieces above into one mission:
detect an object ([module 4](04-perception/index.md)), plan a collision-free
approach (planning scene, above), grasp, lift, and place — expressed as
states with their own failure exits, exactly this module's core pattern
applied to manipulation instead of navigation.

**Why it matters.** This is the concrete synthesis of most of this course:
perception, TF, and now planning and manipulation, all inside one state
machine.

**Needs.** [Planning scene and collision
objects](#planning-scene-and-collision-objects) above, and
[module 4's](04-perception/index.md) marker detection.

**Try it.** {{ unverified }} — extend this module's practical task's state
machine with `APPROACH`, `GRASP` and `PLACE` states, each calling into
MoveIt, each with an explicit failure exit (e.g. "inverse kinematics
returned no solution" → a named failure state, not a crash).

**Check.** Running the extended mission with an intentionally unreachable
target pose ends in your named failure state, not a hang or a traceback.

**Read more.** [ALeRT/Spot: manipulation with
MoveIt](../platforms/alert-spot.md#manipulation-with-moveit)
:::

:::{dropdown} Multi-robot task allocation — Advanced
:icon: light-bulb

**What it is.** Deciding *which* robot does *which* part of a mission when
more than one is available — from a simple fixed split (robot A always
searches, robot B always delivers) to an auction-based approach where
robots bid on subtasks based on their own cost estimate.

**Why it matters.** This is the natural extension of the
[capstone project's](hackathon.md#optional-extensions) "communicate with a
second robot" optional extension — coordinating two independent state
machines is a different problem than running one.

**Needs.** This module's practical task, and access to (or simulation of)
a second robot.

**Try it.** {{ unverified }} — on paper, design a simple allocation rule
for two robots and one mission with two subtasks (e.g. "search area A" and
"search area B"), and state what message each robot would need to publish
for the other to know the task is claimed.

**Check.** Your design avoids both robots claiming the same subtask and
leaving the other subtask unclaimed — trace through the message sequence
by hand to confirm.

**Read more.** {{ unverified }} — multi-robot coordination tooling in ROS 2
is an active area with no single standard package this course pins;
search current literature on "multi-robot task allocation ROS 2" when you
reach this point.
:::

## Interesting videos

{{ optional }}

::::{grid} 1 1 1 1
:gutter: 2

:::{grid-item-card} Behavior Trees for ROS2
:link: https://www.youtube.com/watch?v=KO4S0Lsba6I

**The Construct Robotics Institute · ROS2 Developers Open Class #162 · English · ~68 min**

Covers: behavior trees as a decision-making tool for ROS 2 — Sequence,
Fallback, and how they compare to the state machine this module teaches
as its core pattern.

*Why watch it*: a much longer, hands-on look at exactly the "Behavior
trees, in contrast" comparison this module's core concepts introduce
briefly — useful once the state-machine practical task feels comfortable
and you want to see the alternative built out properly.

*Compatibility*: conceptual and applicable to ROS 2 Humble — behavior
trees themselves are not distribution-specific, though check any specific
package name shown against [Nav2's own behavior tree
documentation](https://docs.nav2.org/humble/configuration_and_development/configuration_guide/core_servers/bt_plugins/).
:::

::::

:::{note}
This is deliberately one carefully checked video rather than a longer,
unverified list. If this link is ever dead or the content has moved, that
is a documentation bug worth reporting — see the [repository
README](https://github.com/MoritzSchallenberg/Learning-Robotics-Crash-Course).
:::

## Connection to the next module

This module's mission ran once, on its own. [Module 8](08-integration.md)
assembles every piece from the previous modules into one system, starts it
with one command, and covers how to find a fault fast.

## Further reading

- [BehaviorTree.CPP](https://www.behaviortree.dev/) — the library Nav2 uses
- [Nav2 behavior trees](https://docs.nav2.org/humble/configuration_and_development/configuration_guide/core_servers/bt_plugins/)
- [RAFCON documentation](https://rafcon.readthedocs.io/en/stable/concepts.html)
- [PlanSys2](https://plansys2.github.io/) and its
  [behavior tree actions tutorial](https://plansys2.github.io/tutorials/docs/bt_actions.html)
- [MoveIt 2](https://moveit.picknik.ai/)
