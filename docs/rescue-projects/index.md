# Rescue Applications and Projects

## Overview

Every earlier topic exercised one subsystem — mapping, navigation,
perception, mission logic — in isolation. This category is where they
cooperate, unattended, in one run, on a real or simulated rescue-style
task, with a defined way to tell afterwards whether it actually worked.

**Needs**: [Integration, Diagnostics and Testing](../integration-testing/index.md)
completed — this category assumes you can already bring up a whole system
with one command and diagnose a fault systematically.

**This is a closing technical exercise, not a scored event.** The
checklist it is measured against is a fixed, platform-independent
self-assessment — not a ranking, a schedule, or a jury.

## How ALeRT uses this topic

{{ alert }} Legged locomotion is the advantage on any non-flat terrain.
See [Platform notes](platform-notes.md) for detail specific to
the mission.

## Subtopics

::::{grid} 1 1 2 2
:gutter: 2

:::{grid-item-card} Autonomous Rescue Mission
:link: autonomous-rescue-mission
:link-type: doc

{{ foundation }} The seven-step mission, optional extensions, the
self-assessment checklist, and safety.
:::

:::{grid-item-card} Platform notes
:link: platform-notes
:link-type: doc

{{ foundation }} Simulation and ALeRT/Spot specifics, and the schematic
mission area.
:::

:::{grid-item-card} Mission monitoring and recovery
:link: mission-monitor
:link-type: doc

An optional monitoring node, required logs, and handling an unexpected
stop.
:::

:::{grid-item-card} Interesting videos
:link: videos
:link-type: doc

One carefully checked video recommendation.
:::

:::{grid-item-card} Continue learning
:link: continue-learning
:link-type: doc

Subsystem decomposition, test matrices, measurable acceptance criteria,
fault injection, repeatability, retrospectives.
:::

::::

## Content already present

The [Autonomous Rescue Mission](autonomous-rescue-mission.md) page has the
full seven-step mission, its self-assessment checklist, and safety
requirements; see that page for learning objectives, prerequisites and how
the complete system fits together, rather than repeating them here.

## Related topics

This category draws on every other topic on this site:
[Hardware Design](../platforms/hardware-design/index.md),
[ROS 2](../ros2/index.md),
[Sensors and Coordinate Frames](../sensors-frames/index.md),
[Perception](../perception/index.md),
[Mapping and World Models](../mapping-world-models/index.md),
[Localization, Navigation and Exploration](../navigation-exploration/index.md),
[Autonomous Decision-Making](../decision-making/index.md), and
[Integration, Diagnostics and Testing](../integration-testing/index.md).

## Further reading

- [Nav2 costmap filters](https://docs.nav2.org/humble/configuration_and_development/configuration_guide/core_servers/costmap_2d/costmap_filters/keepout_filter/)
- [Nav2 tutorials](https://docs.nav2.org/humble/tutorials/)
- [ALeRT Platforms and Safety](../platforms/index.md)

```{toctree}
:maxdepth: 1
:hidden:

autonomous-rescue-mission
platform-notes
mission-monitor
videos
continue-learning
```
