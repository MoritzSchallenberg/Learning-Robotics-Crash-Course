# Autonomous Decision-Making

## Overview

You can navigate, perceive and localize. What is missing is the thing that
decides *what to do next* — and what to do when a step fails. This
topic's core is that decision layer, not any one tool for building it.

**The problem it solves**: chaining calls together
(`drive(); detect(); grasp(); deliver()`) has no answer to "what if
`detect` finds nothing?" other than crashing — a mission needs an explicit
answer for every step that can fail.

**Where it sits in the system**: directly after
[Navigation and Exploration's](../navigation-exploration/index.md) navigation action — this topic treats
`NavigateToPose` as one action among several that a state machine or
behavior tree can call, retry, or replace on failure — and directly
underneath [Integration, Diagnostics and Testing's](../integration-testing/index.md) system-wide integration.

**Needs**: [Navigation and Exploration](../navigation-exploration/index.md) — you can send a navigation goal
from code and read its result.

**Leads into**: [Integration, Diagnostics and Testing](../integration-testing/index.md) assembles every piece from
the previous topics, including this one's mission logic, into one system
started with one command.

## Learning objectives

By the end of this topic you can:

1. model a small mission as a sequence of states with explicit failure
   exits;
2. explain what a behavior tree adds over a plain state machine;
3. implement and run a mission with at least one failure or retry branch;
4. name at least one tool beyond a plain state machine (RAFCON, or a
   planner such as PlanSys2/Golog++) and what problem it is for.

## How the complete system fits together

```{figure} ../_static/images/diagrams/state-machine-behavior-tree.svg
:alt: Left, a finite state machine with states Idle, Navigate, Detect and Deliver in sequence, each with its own explicit failure transition to a shared Abort state. Right, a behavior tree with a Fallback root whose first child is a Sequence of Navigate, Detect and Deliver, and whose second child is a Recovery action used if the sequence fails.
:width: 100%

A state machine needs one failure transition per state; a behavior tree
needs one shared recovery branch.
```

A mission's decision layer calls into the ROS 2 components built in
earlier topics — a navigation goal ([Navigation and Exploration](../navigation-exploration/index.md)), a
detection check ([Perception](../perception/index.md)) — as its "actions",
and typically publishes its own status topic so an external observer can
tell what it is doing.

## How ALeRT uses this topic

{{ alert }} {{ documented }}

Spot's high-level control uses [RAFCON](https://github.com/DLR-RM/RAFCON),
a graphical state machine editor, for exactly this topic's core pattern
— see
{ref}`Planning approaches <rafcon-a-graphical-state-machine-tool>`.
**Sensors/actuators**: postures exposed as **services** (stand, sit, lie
down — quick, either-succeeds-or-not calls, not actions), plus MoveIt 2
for the arm. **Typical team task**: writing one RAFCON state per mission
step, each with its own named failure exit, exactly this topic's own
practical task's discipline. **Verification status**: {{ simulation }}
confirmed in Webots; the physical robot is a supervised-only exercise
(see this topic's [Try it on
Spot](practical-exercise.md#try-it-on-spot)).

## Working through this topic

```text
1. Mission logic (state machines vs. behavior trees)
2. Practical mission exercise
```

**Planning approaches**, **Interesting videos** and **Continue learning**
are worthwhile afterwards, but are not required to move on to the next
topic.

## Subtopics

::::{grid} 1 1 2 2
:gutter: 2

:::{grid-item-card} Mission logic
:link: mission-logic
:link-type: doc

{{ foundation }} State machines, behavior trees, and a guided example that
deliberately hangs.
:::

:::{grid-item-card} Practical exercise
:link: practical-exercise
:link-type: doc

{{ foundation }} Build a mission that recovers instead of hanging — plus this
topic's Try it on Spot section.
:::

:::{grid-item-card} Planning approaches
:link: planning-approaches
:link-type: doc

{{ advanced }} RAFCON, and planning systems (PlanSys2, Golog++) as an
alternative to a hand-written state machine.
:::

:::{grid-item-card} Interesting videos
:link: videos
:link-type: doc

One carefully checked video recommendation.
:::

:::{grid-item-card} Continue learning
:link: continue-learning
:link-type: doc

Blackboards, action cancellation, lifecycle-controlled subsystems,
mission monitoring, planning scenes, pick-and-place, multi-robot
allocation.
:::

::::

## Prerequisites

[Navigation and Exploration](../navigation-exploration/index.md) completed — you can send a navigation goal
from code and read its result.

## Connection to the next topic

This topic's mission ran once, on its own. [Integration, Diagnostics and Testing](../integration-testing/index.md)
assembles every piece from the previous topics into one system, starts it
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

mission-logic
planning-approaches
practical-exercise
videos
continue-learning
```
