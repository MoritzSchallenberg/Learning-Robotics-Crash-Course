# 7. Autonomous Decisions and Manipulation

:::{admonition} Session 7
:class: note

Monday, 26 October 2026, 17:35 – 19:00 (85 minutes)
:::

{{ common }}

You can navigate, perceive and localize. What is missing is the thing that
decides *what to do next* — and what to do when a step fails. Tonight's core
is that decision layer, not any one tool for building it.

## Tonight

**Learning objectives** — by 19:00 you can:

1. model a small mission as a sequence of states with explicit failure
   exits;
2. explain what a behavior tree adds over a plain state machine;
3. implement and run a mission with at least one failure or retry branch.

**Visible result of the evening**: a mission runs to completion when
everything works, **and** recovers or reports cleanly when a step you
control deliberately fails — not hangs, not crashes.

**Preparation**: [session 6](06-navigation.md) completed — you can send a
navigation goal from code and read its result.

## Run sheet (85 minutes)

```{list-table}
:header-rows: 1
:widths: 16 20 64
:class: lrcc-runsheet

* - Time
  - Block
  - Content
* - 17:35–17:45
  - Opening
  - Recap: a script has no answer to "what if this fails?" — today's session
    is entirely about that gap
* - 17:45–18:05
  - Theory {{ core }}
  - States, transitions, failure exits; state machine vs. behavior tree
* - 18:05–18:15
  - Demonstration {{ core }}
  - Live: run a 3-state mission, then break it on purpose
* - 18:15–18:50
  - Practical task {{ core }}
  - Model and implement a mission with a failure branch
* - 18:50–19:00
  - Wrap-up
  - Deliberately fail each other's missions; preview session 8
```

## Theory

{{ core }}

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
"try these until one works"). Nav2's BT Navigator, which you already used in
session 6, is exactly this pattern.

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

For tonight's task, a state machine is the faster thing to get working.

## Practical task

### Goal
Implement a mission — *navigate to a point, look for a marker, report* —
that visibly recovers instead of hanging when the marker is not found.

### Starting point
A pre-built `mission_demo` package with the navigation action client from
[session 6](06-navigation.md#advanced-sending-goals-from-code-and-exploring)
and the marker detector from
[session 4](04-perception/index.md) already available as importable helper
classes — you write the state machine, not the underlying clients.

### Steps
1. On paper, draw states: `IDLE → NAVIGATE → SEARCH → RETURN → DONE`, plus a
   `FAILED` exit from `NAVIGATE`.
2. Decide `SEARCH`'s timeout (30 s is reasonable) and what happens on
   timeout — it must still transition, not hang.
3. Implement the state machine in Python using the provided helper classes
   (a `State` enum plus a `step()` method is enough — see the hint below).
4. Run it with the marker **present**. Confirm it completes.
5. Run it with **no marker** in the search area. Confirm it does not hang.
6. Block the navigation goal (place an obstacle across the only path).
   Confirm `NAVIGATE`'s failure exit actually fires.
7. Fix whatever you found in steps 5–6.

### Expected result
The mission finishes in all three cases — success, marker not found,
navigation blocked — with no run lasting longer than the timeout you chose,
and no traceback.

### Verification
```bash
ros2 topic echo /mission_status
```
Reports `succeeded`, `marker_not_found` or `navigation_failed` — three
distinct outcomes, never silence.

### Common problems
- **A state with no way out** — waiting for something with no timeout. Every
  waiting state needs a deadline.
- **Failure not propagated** — the action client reports failure and the
  code moves to the next state anyway; always check the result status.
- **Only the happy path exists** — the most common first draft. If your
  diagram has no failure transitions, it is not finished.

### Extension

{{ optional }}

Add a fourth state that retries `SEARCH` once, from a slightly different
position, before giving up — the smallest possible recovery behaviour.

## Simulation fallback

{{ simulation }}

Identical task; failing "on purpose" is easier in simulation — remove the
marker from the scene, or block the path with a dragged object, exactly as
in [session 6](06-navigation.md#simulation-fallback).

## Advanced: RAFCON, and where planning fits

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
orientation for further reading, not a tool you are expected to install
tonight.
:::

:::{dropdown} MoveIt and manipulation
:icon: light-bulb

{{ alert }} Where session 7's general decision principles connect to a
physical arm: [MoveIt 2](https://moveit.picknik.ai/) solves inverse
kinematics and collision-free motion planning. A pick-and-place sequence is
exactly the state-machine pattern above, with `GRASP` and `RELEASE` as
states with their own failure exits (a `None` inverse-kinematics result is
"unreachable," not a crash). Full example on the
[ALeRT/Spot platform page](../platforms/alert-spot.md#manipulation-with-moveit).
{{ carologistics }} Robotino's simpler custom gripper is covered on the
[Carologistics platform page](../platforms/carologistics-robotino.md#gripper).
:::

## Common mistakes

**`rclpy.shutdown()` inside a state.** Kills the shared node and everything
after it. Only call it once, at the very end of the program.

**The state machine "works" and the robot does not.** States ran and
returned `success` without checking whether their action actually succeeded.

## Transition to session 8

Tonight's mission ran alone, once, by hand. Next week you assemble every
piece from the last seven sessions into one system, start it with one
command, and learn to find a fault fast —
[System Integration and Testing](08-integration.md).

## Further reading

- [BehaviorTree.CPP](https://www.behaviortree.dev/) — the library Nav2 uses
- [Nav2 behavior trees](https://docs.nav2.org/jazzy/configuration_and_development/configuration_guide/core_servers/bt_plugins/)
- [RAFCON documentation](https://rafcon.readthedocs.io/en/stable/concepts.html)
- [PlanSys2](https://plansys2.github.io/) and its
  [behavior tree actions tutorial](https://plansys2.github.io/tutorials/docs/bt_actions.html)
- [MoveIt 2](https://moveit.picknik.ai/)
