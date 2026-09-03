# 7. Autonomous Decisions and Manipulation

{{ common }}

## Module overview

You can navigate, perceive and localize. What is missing is the thing that
decides *what to do next* — and what to do when a step fails. This
module's core is that decision layer, not any one tool for building it.

**The problem it solves**: chaining calls together
(`drive(); detect(); grasp(); deliver()`) has no answer to "what if
`detect` finds nothing?" other than crashing — a mission needs an explicit
answer for every step that can fail.

**Where it sits in the system**: directly after
[module 6's](06-navigation.md) navigation action — this module treats
`NavigateToPose` as one action among several that a state machine or
behavior tree can call, retry, or replace on failure — and directly
underneath [module 8's](08-integration.md) system-wide integration.

**Needs**: [module 6](06-navigation.md) — you can send a navigation goal
from code and read its result.

**Leads into**: [module 8](08-integration.md) assembles every piece from
the previous modules, including this one's mission logic, into one system
started with one command.

## Learning objectives

By the end of this module you can:

1. model a small mission as a sequence of states with explicit failure
   exits;
2. explain what a behavior tree adds over a plain state machine;
3. implement and run a mission with at least one failure or retry branch;
4. name at least one tool beyond a state machine (RAFCON, a planner, or
   MoveIt) and what problem it is for.

## How the complete system fits together

```{figure} ../_static/images/diagrams/08-state-machine-behavior-tree.svg
:alt: Left, a finite state machine with states Idle, Navigate, Detect and Deliver in sequence, each with its own explicit failure transition to a shared Abort state. Right, a behavior tree with a Fallback root whose first child is a Sequence of Navigate, Detect and Deliver, and whose second child is a Recovery action used if the sequence fails.
:width: 100%

A state machine needs one failure transition per state; a behavior tree
needs one shared recovery branch.
```

A mission's decision layer calls into the ROS 2 components built in
earlier modules — a navigation goal ([module 6](06-navigation.md)), a
detection check ([module 4](04-perception/index.md)) — as its "actions",
and typically publishes its own status topic so an external observer can
tell what it is doing.

## How ALeRT uses this topic

{{ alert }} {{ documented }}

Spot's high-level control uses [RAFCON](https://github.com/DLR-RM/RAFCON),
a graphical state machine editor, for exactly this module's core pattern
— see
{ref}`Planning and manipulation approaches <rafcon-a-graphical-state-machine-tool>`.
**Sensors/actuators**: postures exposed as **services** (stand, sit, lie
down — quick, either-succeeds-or-not calls, not actions), plus MoveIt 2
for the arm. **Typical team task**: writing one RAFCON state per mission
step, each with its own named failure exit, exactly this module's own
practical task's discipline. **Verification status**: {{ simulation }}
confirmed in Webots; the physical robot is a supervised-only exercise
(see this module's [Try it on
Spot](07-autonomous-decisions/practical-exercise.md#try-it-on-spot)).

## How Carologistics uses this topic

{{ carologistics }} {{ documented }}

The central goal-reasoning agent,
[`expertino-rcll`](../platforms/carologistics-robotino.md#key-repositories),
plays the same role as this module's state machine — deciding what the
robot does next and reacting when a step fails — at fleet scale.
**Typical team task**: {{ unverified }} — not documented in detail on the
platform page beyond the repository's existence. **Verification status**:
{{ documented }} via the platform page's repository description.

## ALeRT and Carologistics compared

```{list-table}
:header-rows: 1
:widths: 22 26 26 26

* - Aspect
  - ALeRT / Spot
  - Carologistics / Robotino
  - Shared principle
* - Decision tool
  - RAFCON (graphical state machine)
  - `expertino-rcll` (central agent)
  - Both use explicit, named failure exits, not planning
* - Scope
  - One robot's mission
  - Fleet-wide goal reasoning across several Robotinos
  - Neither team runs PlanSys2 or Golog++ for competition
* - Manipulation
  - MoveIt 2 for the arm
  - A simpler custom gripper
  - Both treat "grasp failed" as a named state, not a crash
* - Physical safety
  - Supervised-only for real hardware sequences
  - {{ unverified }} — not documented as a formal policy
  - An automated multi-step sequence needs a human confirming steps
```

## Core learning path

```text
1. Mission logic (state machines vs. behavior trees)
2. Practical mission exercise
```

That is this module's roughly 80–100 minute core learning time.
**Planning and manipulation approaches**, **Interesting videos** and
**Continue learning** are worthwhile afterwards but not required for the
core path.

## Subtopics

::::{grid} 1 1 2 2
:gutter: 2

:::{grid-item-card} Mission logic
:link: 07-autonomous-decisions/mission-logic
:link-type: doc

{{ core }} State machines, behavior trees, and a guided example that
deliberately hangs.
:::

:::{grid-item-card} Practical exercise
:link: 07-autonomous-decisions/practical-exercise
:link-type: doc

{{ core }} Build a mission that recovers instead of hanging — plus this
module's Try it on Spot section.
:::

:::{grid-item-card} Planning and manipulation approaches
:link: 07-autonomous-decisions/planning-and-manipulation
:link-type: doc

{{ advanced }} RAFCON, PlanSys2/Golog++, and MoveIt 2 manipulation.
:::

:::{grid-item-card} Interesting videos
:link: 07-autonomous-decisions/videos
:link-type: doc

One carefully checked video recommendation.
:::

:::{grid-item-card} Continue learning
:link: 07-autonomous-decisions/continue-learning
:link-type: doc

Blackboards, action cancellation, lifecycle-controlled subsystems,
mission monitoring, planning scenes, pick-and-place, multi-robot
allocation.
:::

::::

## Prerequisites

[Module 6](06-navigation.md) completed — you can send a navigation goal
from code and read its result.

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

```{toctree}
:maxdepth: 1
:hidden:

07-autonomous-decisions/mission-logic
07-autonomous-decisions/planning-and-manipulation
07-autonomous-decisions/practical-exercise
07-autonomous-decisions/videos
07-autonomous-decisions/continue-learning
```
