# 5. Mapping and Localization

{{ common }}

## Module overview

The robot has sensors, knows where they are mounted, and can detect a
marker. It still has no idea where *it* is. This module gives it a map,
and then a position in that map.

**The problem it solves**: navigating anywhere on purpose needs two
different things — a representation of the space (a map) and an estimate
of where the robot is within it (localization) — built and maintained by
two different tools, not one.

**Where it sits in the system**: directly after
[module 3's](03-sensors-tf.md) TF tree and laser scan — mapping and
localization both consume `/scan` and the `odom`→`base_link` transform
this module's `map`→`odom` correction sits on top of.

**Needs**: [module 3](03-sensors-tf.md) — a working TF tree and a visible
laser scan; you cannot map without both.

**Leads into**: [module 6](06-navigation.md) plans paths using the map and
pose this module produces; without a converged localization, navigation has
nothing reliable to plan from.

## Learning objectives

By the end of this module you can:

1. explain the difference between mapping and localization, and why they
   need different tools;
2. build or load an occupancy grid map with SLAM Toolbox;
3. check the robot's estimated position against the map in RViz;
4. explain why only one node may publish `map`→`odom` at a time.

## How the complete system fits together

```{figure} ../_static/images/diagrams/06-mapping-localization-dataflow.svg
:alt: Two modes sharing laser scan and odometry as inputs. Mapping mode feeds SLAM Toolbox, producing an occupancy grid map and the map to odom transform. Localization mode feeds a saved map plus scan and odometry into AMCL, producing a corrected pose and the same map to odom transform.
:width: 100%

Both modes publish the same `map`→`odom` transform — the correction that
keeps `odom`'s smooth drift from accumulating forever.
```

This is why the `map`/`odom`/`base_link` split from [module 3](03-sensors-tf.md)
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
module's practical task uses (`slam_launch.py`, then `nav_launch.py` with a
saved map) — see the [platform page's mapping and
navigation section](../platforms/alert-spot.md#mapping-and-navigation).
**Sensors/actuators**: the 3D LiDAR flattened to a 2D `/scan`, feeding
SLAM Toolbox and AMCL exactly as in this module's practical task.
**Known peculiarity**: {{ documented }} a rescue arena is rarely flat, so a
2D occupancy grid alone is not enough — ALeRT additionally uses two 3D
approaches (Octomap, GLIM), covered in this module's [3D mapping
subtopic](05-mapping-localization/localization-and-3d-mapping.md#mapping-rough-3d-terrain).
**Typical team task**: mapping a new arena slowly enough to avoid the
doubled-wall smearing this module's Common problems section warns about,
then confirming localization converges before trusting navigation on top of
it. **Verification status**: {{ simulation }} confirmed in Webots; the
physical robot is a supervised-only exercise (see this module's [Try it on
Spot](05-mapping-localization/practical-exercise.md#try-it-on-spot)).

## How Carologistics uses this topic

{{ carologistics }} {{ documented }}

Robotino localizes against a **pre-built** map rather than mapping live
during competition: [`mps-map-gen`](../platforms/carologistics-robotino.md#key-repositories)
extends a map-server map with game-specific information (machine positions,
a legal-area boundary), publishing `mps_map` for localization and
`mps_map_bounded` for navigation. **Sensors/actuators**: two merged 2D
laser scanners (`laser_scan_integrator`, see [module 3](03-sensors-tf.md)),
feeding AMCL. **Typical team task**: setting **2D Pose Estimate** and
confirming the laser aligns with the map's walls before trusting a
navigation goal — see the [platform page's localization
steps](../platforms/carologistics-robotino.md#localizing-a-robot), which
are the same procedure as this module's practical task, run per-robot under
a namespace. **Verification status**: {{ documented }} via the platform
page's own operating instructions.

## ALeRT and Carologistics compared

```{list-table}
:header-rows: 1
:widths: 22 26 26 26

* - Aspect
  - ALeRT / Spot
  - Carologistics / Robotino
  - Shared principle
* - Map source
  - Live SLAM per mission (`slam_launch.py`)
  - Pre-built once, extended with game info (`mps-map-gen`)
  - Both still localize live with AMCL against whatever map is loaded
* - Map dimensionality
  - 2D for navigation, plus 3D (Octomap/GLIM) for terrain
  - {{ unverified }} — 2D only, not documented otherwise
  - A flat-floor environment rarely needs 3D; a rescue arena usually does
* - Localization tool
  - AMCL, per this module's practical task
  - AMCL, per the platform page's localizing-a-robot steps
  - Same particle-filter approach, same "check the scan against the walls"
    verification
* - Multi-robot map handling
  - {{ unverified }} — single robot, not documented
  - Namespaced per robot (`/robotinobase<i>/...`), shared field map
  - Both follow REP 105's map/odom/base convention underneath
```

## Core learning path

```text
1. Mapping and SLAM (odometry, occupancy grids, SLAM Toolbox)
2. Localization and 3D mapping (AMCL, kidnapped-robot basics, Octomap/GLIM)
3. Practical mapping and localization exercise
```

That is this module's roughly 80–100 minute core learning time.
**Interesting videos** and **Continue learning** are worthwhile afterwards
but not required for the core path.

## Subtopics

::::{grid} 1 1 2 2
:gutter: 2

:::{grid-item-card} Mapping and SLAM
:link: 05-mapping-localization/mapping-and-slam
:link-type: doc

{{ core }} Odometry drift, occupancy grids, and building a map with SLAM
Toolbox.
:::

:::{grid-item-card} Localization and 3D mapping
:link: 05-mapping-localization/localization-and-3d-mapping
:link-type: doc

{{ core }} Finding the robot's pose with AMCL, recovering from a lost pose,
and ALeRT's 3D mapping extensions.
:::

:::{grid-item-card} Practical exercise
:link: 05-mapping-localization/practical-exercise
:link-type: doc

{{ core }} Map an area, then localize on it — plus this module's Try it on
Spot section.
:::

:::{grid-item-card} Interesting videos
:link: 05-mapping-localization/videos
:link-type: doc

One carefully checked video recommendation.
:::

:::{grid-item-card} Continue learning
:link: 05-mapping-localization/continue-learning
:link-type: doc

Loop closure, map versioning, parameter tuning, the kidnapped-robot
problem, multi-session mapping.
:::

::::

## Prerequisites

[Module 3](03-sensors-tf.md) completed — a working TF tree and a visible
laser scan are required; you cannot map without both.

## Connection to the next module

This module found the robot's own position. [Module 6](06-navigation.md)
uses that position to decide how to get somewhere else on its own.

## Further reading

- [SLAM Toolbox](https://github.com/SteveMacenski/slam_toolbox) and its
  configuration guide
- [Nav2 AMCL configuration](https://docs.nav2.org/humble/configuration_and_development/configuration_guide/others/configuring_amcl/)
- [REP 105: Coordinate frames](https://www.ros.org/reps/rep-0105.html)

```{toctree}
:maxdepth: 1
:hidden:

05-mapping-localization/mapping-and-slam
05-mapping-localization/localization-and-3d-mapping
05-mapping-localization/practical-exercise
05-mapping-localization/videos
05-mapping-localization/continue-learning
```
