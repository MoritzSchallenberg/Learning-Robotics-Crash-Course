# Capstone: Autonomous Robot Mission

{{ common }}

## Module overview

Everything from the eight modules, on one robot, running on its own. This
is the course's final self-check: if you can complete it, the course has
done its job.

**The problem it solves**: every earlier module exercised one subsystem —
mapping, navigation, perception, mission logic — in isolation. The
capstone is where all of them cooperate, unattended, in one run, with a
defined way to tell afterwards whether it actually worked.

**Needs**: all eight course modules completed, in particular
[module 8](08-integration.md) — this project assumes you can already bring
up a whole system with one command and diagnose a fault systematically.

**This is the closing technical task of the course**: a self-check against
a fixed, platform-independent checklist, not an event with scoring,
ranking or a schedule.

## Learning objectives

By completing this project you demonstrate that you can:

1. integrate every module's subsystem into one reproducible system;
2. run an autonomous mission with no manual driving during the attempt;
3. produce a rosbag and logs that let you (or someone else) verify what the
   system actually did.

## How the complete system fits together

The mission draws on every subsystem from the previous modules —
localization, navigation, perception and mission logic — coordinated by
the same startup order and diagnostic discipline
[module 8](08-integration.md) teaches. Nothing here is new subject matter;
this project's only new content is running all of it together, once, on
its own.

## How ALeRT uses this topic

{{ alert }} Legged locomotion is the advantage on any non-flat terrain.
See [Platform notes](hackathon/platform-notes.md) for detail specific to
the mission.

## How Carologistics uses this topic

{{ carologistics }} Robotino's omnidirectional drive is a genuine
advantage for tight turns, and the transport extension maps naturally
onto its existing gripper. See [Platform notes](hackathon/platform-notes.md)
for detail specific to the mission.

## Subtopics

::::{grid} 1 1 2 2
:gutter: 2

:::{grid-item-card} The mission and self-assessment
:link: hackathon/mission-and-checklist
:link-type: doc

{{ core }} The seven-step mission, optional extensions, the
self-assessment checklist, and safety.
:::

:::{grid-item-card} Platform notes
:link: hackathon/platform-notes
:link-type: doc

{{ core }} Simulation, Carologistics/Robotino and ALeRT/Spot specifics,
and the schematic mission area.
:::

:::{grid-item-card} Mission monitoring and recovery
:link: hackathon/mission-monitor
:link-type: doc

An optional monitoring node, required logs, and handling an unexpected
stop.
:::

:::{grid-item-card} Interesting videos
:link: hackathon/videos
:link-type: doc

One carefully checked video recommendation.
:::

:::{grid-item-card} Continue learning
:link: hackathon/continue-learning
:link-type: doc

Subsystem decomposition, test matrices, measurable acceptance criteria,
fault injection, repeatability, retrospectives.
:::

::::

## Prerequisites

All eight course modules completed, in particular
[module 8](08-integration.md) — this project assumes you can already bring
up a whole system with one command and diagnose a fault systematically.

## Connection to the course

This project draws on every module:
[1](01-system-hardware.md) · [2](02-ros2.md) · [3](03-sensors-tf.md) ·
[4](04-perception/index.md) · [5](05-mapping-localization.md) ·
[6](06-navigation.md) · [7](07-autonomous-decisions.md) ·
[8](08-integration.md).

## Further reading

- [Nav2 costmap filters](https://docs.nav2.org/humble/configuration_and_development/configuration_guide/core_servers/costmap_2d/costmap_filters/keepout_filter/)
- [Nav2 tutorials](https://docs.nav2.org/humble/tutorials/)
- Your [platform track](../platforms/index.md)

```{toctree}
:maxdepth: 1
:hidden:

hackathon/mission-and-checklist
hackathon/platform-notes
hackathon/mission-monitor
hackathon/videos
hackathon/continue-learning
```
