# 6. Autonomous Navigation

{{ common }}

## Module overview

The robot has a map and knows where it is. This module has it start
driving itself: you give it a goal, Nav2 works out the path, and it reacts
when something gets in the way.

**The problem it solves**: knowing your position ([module 5](05-mapping-localization.md))
does not get you anywhere by itself — something has to turn "go there"
into a safe path and continuous velocity commands that react to whatever
the map did not know about.

**Where it sits in the system**: directly after
[module 5's](05-mapping-localization.md) map and localized pose — Nav2
will not work without a reliable `map`→`odom`→`base_link` chain — and
directly underneath [module 7's](07-autonomous-decisions.md) mission
logic, which calls navigation as one action among several.

**Needs**: [module 5](05-mapping-localization.md) — a saved map and AMCL
localizing on it.

**Leads into**: [module 7](07-autonomous-decisions.md) treats
`NavigateToPose` as one action a state machine or behavior tree can call,
retry, or replace with a different one on failure.

## Learning objectives

By the end of this module you can:

1. name the four main Nav2 servers and what each is responsible for;
2. explain the difference between the global and local costmap;
3. send the robot to a goal and observe it re-plan around a new obstacle;
4. name at least one Nav2 capability beyond a single goal (waypoints,
   keepout zones, or docking).

## How the complete system fits together

```{figure} ../_static/images/diagrams/07-nav2-architecture-simplified.svg
:alt: A navigation goal enters the BT Navigator, which coordinates a Planner Server reading the Global Costmap, a Controller Server reading the Local Costmap, and a Behavior Server for recovery actions. The Controller Server outputs cmd_vel.
:width: 100%

The BT Navigator dispatches to three servers; the Controller Server is the
only one that outputs `/cmd_vel`.
```

Navigation is exposed as a ROS 2 action (`NavigateToPose`,
[module 2](02-ros2/services-parameters-actions.md#try-it-yourself-actions)):
a goal pose in, feedback while driving, a result at the end. Its inputs are
the map ([module 5](05-mapping-localization.md)), the localized pose, and
live sensor data; its output is `/cmd_vel`
([module 2](02-ros2/topics-and-messages.md)).

## How ALeRT uses this topic

{{ alert }} {{ documented }}

Spot navigates with `ros2 launch webots_spot nav_launch.py` — the same
Planner/Controller/Behavior split this module teaches, on a legged
platform whose local costmap has to account for a wider, less predictable
footprint than a wheeled robot's. **Sensors/actuators**: the same 2D
`/scan` and localized pose from [module 5](05-mapping-localization.md),
feeding Nav2's costmaps directly. **Typical team task**: comparing
recovery-behaviour outcomes across repeated attempts at the same goal,
since a legged platform's failure modes are less repeatable than a
wheeled one's — see this module's [Try it on
Spot](06-navigation/practical-exercise.md#try-it-on-spot).
**Verification status**: {{ simulation }} confirmed in Webots.

## How Carologistics uses this topic

{{ carologistics }} {{ documented }}

Robotino runs [`robotino_navigation`](../platforms/carologistics-robotino.md#key-repositories),
Nav2 configuration working with both the simulation and real robots, with
a documented two-SICK-TiM571 sensor setup. **Sensors/actuators**: the
merged laser scan from [module 3's](03-sensors-tf.md)
`laser_scan_integrator`, feeding the same costmap architecture.
**Typical team task**: precision docking to a production machine within
millimetres — see this module's
{ref}`Continue learning: docking and navigating through poses <docking-and-navigating-through-poses>`.
**Verification status**: {{ documented }} via the platform page's
repository description.

## ALeRT and Carologistics compared

```{list-table}
:header-rows: 1
:widths: 22 26 26 26

* - Aspect
  - ALeRT / Spot
  - Carologistics / Robotino
  - Shared principle
* - Navigation goal precision
  - A reachable area is usually enough
  - Millimetre-precision docking to a machine
  - Both use the same `NavigateToPose`/`NavigateThroughPoses` actions
* - Local costmap challenge
  - Legged footprint, less predictable per step
  - {{ unverified }} — not documented; likely a standard footprint model
  - Both keep the local costmap in `odom` so it stays smooth
* - Area constraint
  - {{ unverified }} — not documented
  - `mps_map_bounded` layers a competition-area boundary
  - Both can add costmap layers beyond the raw sensor data
* - Repeat-run comparison
  - Explicitly compared across attempts (this module's Spot task)
  - {{ unverified }} — not documented as a standard team practice
  - A single successful run does not prove reliability
```

## Core learning path

```text
1. Nav2 architecture and costmaps
2. Practical navigation exercise
```

That is this module's roughly 80–100 minute core learning time.
**Interesting videos** and **Continue learning** are worthwhile
afterwards but not required for the core path.

## Subtopics

::::{grid} 1 1 2 2
:gutter: 2

:::{grid-item-card} Nav2 architecture and costmaps
:link: 06-navigation/nav2-architecture-and-costmaps
:link-type: doc

{{ core }} The Planner/Controller/Behavior split, global vs. local
costmaps, and a first goal sent by hand.
:::

:::{grid-item-card} Practical exercise
:link: 06-navigation/practical-exercise
:link-type: doc

{{ core }} Send the robot to a goal, introduce an obstacle, and watch it
re-plan — plus this module's Try it on Spot section.
:::

:::{grid-item-card} Interesting videos
:link: 06-navigation/videos
:link-type: doc

One carefully checked video recommendation.
:::

:::{grid-item-card} Continue learning
:link: 06-navigation/continue-learning
:link-type: doc

Costmap tuning, behavior trees, waypoints and keepout zones, docking,
navigation metrics, autonomous exploration.
:::

::::

## Prerequisites

[Module 5](05-mapping-localization.md) completed — a saved map and AMCL
localizing on it. Nav2 will not work without a reliable
`map`→`odom`→`base_link` chain.

## Connection to the next module

This module sent the robot to *one* goal you chose.
[Module 7](07-autonomous-decisions.md) has it choose its own next step,
including what to do when something fails.

## Further reading

- [Nav2 documentation](https://docs.nav2.org/humble/)
- [Nav2 configuration guide](https://docs.nav2.org/humble/configuration_and_development/configuration_guide/)
- [Nav2 first-time setup](https://docs.nav2.org/humble/configuration_and_development/first_time_robot_setup_guide/)
- [Behavior trees in Nav2](https://docs.nav2.org/humble/configuration_and_development/configuration_guide/core_servers/bt_plugins/)
  — the bridge to [module 7](07-autonomous-decisions.md)

```{toctree}
:maxdepth: 1
:hidden:

06-navigation/nav2-architecture-and-costmaps
06-navigation/practical-exercise
06-navigation/videos
06-navigation/continue-learning
```
