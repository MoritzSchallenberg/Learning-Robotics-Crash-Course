# Mapping and Localization

## Overview

The robot has sensors, knows where they are mounted, and can detect a
marker. It still has no idea where *it* is. This topic gives it a map,
and then a position in that map.

**The problem it solves**: navigating anywhere on purpose needs two
different things — a representation of the space (a map) and an estimate
of where the robot is within it (localization) — built and maintained by
two different tools, not one.

**Where it sits in the system**: directly after
[Sensors and Coordinate Frames's](../sensors-frames/index.md) TF tree and laser scan — mapping and
localization both consume `/scan` and the `odom`→`base_link` transform
this topic's `map`→`odom` correction sits on top of.

**Needs**: [Sensors and Coordinate Frames](../sensors-frames/index.md) — a working TF tree and a visible
laser scan; you cannot map without both.

**Leads into**: [Navigation and Exploration](../navigation-exploration/index.md) plans paths using the map and
pose this topic produces; without a converged localization, navigation has
nothing reliable to plan from.

## Learning objectives

By the end of this topic you can:

1. explain the difference between mapping and localization, and why they
   need different tools;
2. build or load an occupancy grid map with SLAM Toolbox;
3. check the robot's estimated position against the map in RViz;
4. explain why only one node may publish `map`→`odom` at a time.

## How the complete system fits together

```{figure} ../_static/images/diagrams/mapping-localization-dataflow.svg
:alt: Two modes sharing laser scan and odometry as inputs. Mapping mode feeds SLAM Toolbox, producing an occupancy grid map and the map to odom transform. Localization mode feeds a saved map plus scan and odometry into AMCL, producing a corrected pose and the same map to odom transform.
:width: 100%

Both modes publish the same `map`→`odom` transform — the correction that
keeps `odom`'s smooth drift from accumulating forever.
```

This is why the `map`/`odom`/`base_link` split from [Sensors and Coordinate Frames](../sensors-frames/index.md)
exists: `odom`→`base_link` stays smooth and local; `map`→`odom` is the
correction, published by whichever of SLAM Toolbox or AMCL is currently
running — never both at once.

:::{danger}
Only **one** node may publish `map`→`odom` at a time. Running SLAM Toolbox
and AMCL together produces a pose that jumps unpredictably between their two
answers.
:::

## How ALeRT uses this topic

{{ alert }} {{ documented }}

Spot maps and localizes with the same `webots_spot` launch files this
topic's practical task uses (`slam_launch.py`, then `nav_launch.py` with a
saved map) — see the [platform page's mapping and
navigation section](../platforms/spot/index.md#mapping-and-navigation).
**Sensors/actuators**: the 3D LiDAR flattened to a 2D `/scan`, feeding
SLAM Toolbox and AMCL exactly as in this topic's practical task.
**Known peculiarity**: {{ documented }} a rescue arena is rarely flat, so a
2D occupancy grid alone is not enough — ALeRT additionally uses two 3D
approaches (Octomap, GLIM), covered in this topic's [3D mapping
subtopic](localization-and-3d-mapping.md#mapping-rough-3d-terrain).
**Typical team task**: mapping a new arena slowly enough to avoid the
doubled-wall smearing this topic's Common problems section warns about,
then confirming localization converges before trusting navigation on top of
it. **Verification status**: {{ simulation }} confirmed in Webots; the
physical robot is a supervised-only exercise (see this topic's [Try it on
Spot](practical-exercise.md#try-it-on-spot)).

## Working through this topic

```text
1. Mapping and SLAM (odometry, occupancy grids, SLAM Toolbox)
2. Localization and 3D mapping (AMCL, kidnapped-robot basics, Octomap/GLIM)
3. Practical mapping and localization exercise
```

**Interesting videos** and **Continue learning** are worthwhile afterwards,
but are not required to move on to the next topic.

## Subtopics

::::{grid} 1 1 2 2
:gutter: 2

:::{grid-item-card} Mapping and SLAM
:link: mapping-and-slam
:link-type: doc

{{ foundation }} Odometry drift, occupancy grids, and building a map with SLAM
Toolbox.
:::

:::{grid-item-card} Localization and 3D mapping
:link: localization-and-3d-mapping
:link-type: doc

{{ foundation }} Finding the robot's pose with AMCL, recovering from a lost pose,
and ALeRT's 3D mapping extensions.
:::

:::{grid-item-card} Practical exercise
:link: practical-exercise
:link-type: doc

{{ foundation }} Map an area, then localize on it — plus this topic's Try it on
Spot section.
:::

:::{grid-item-card} Interesting videos
:link: videos
:link-type: doc

One carefully checked video recommendation.
:::

:::{grid-item-card} Continue learning
:link: continue-learning
:link-type: doc

Loop closure, map versioning, parameter tuning, the kidnapped-robot
problem, multi-session mapping.
:::

::::

## Prerequisites

[Sensors and Coordinate Frames](../sensors-frames/index.md) completed — a working TF tree and a visible
laser scan are required; you cannot map without both.

## Connection to the next topic

This topic found the robot's own position. [Navigation and Exploration](../navigation-exploration/index.md)
uses that position to decide how to get somewhere else on its own.

## Further reading

- [SLAM Toolbox](https://github.com/SteveMacenski/slam_toolbox) and its
  configuration guide
- [Nav2 AMCL configuration](https://docs.nav2.org/humble/configuration_and_development/configuration_guide/others/configuring_amcl/)
- [REP 105: Coordinate frames](https://www.ros.org/reps/rep-0105.html)

```{toctree}
:maxdepth: 1
:hidden:

mapping-and-slam
localization-and-3d-mapping
practical-exercise
videos
continue-learning
```
