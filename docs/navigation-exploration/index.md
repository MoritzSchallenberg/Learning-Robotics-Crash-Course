# Autonomous Navigation

## Overview

The robot has a map and knows where it is. This topic has it start
driving itself: you give it a goal, Nav2 works out the path, and it reacts
when something gets in the way.

**The problem it solves**: knowing your position ([Mapping and World Models](../mapping-world-models/index.md))
does not get you anywhere by itself — something has to turn "go there"
into a safe path and continuous velocity commands that react to whatever
the map did not know about.

**Where it sits in the system**: directly after
[Mapping and World Models's](../mapping-world-models/index.md) map and localized pose — Nav2
will not work without a reliable `map`→`odom`→`base_link` chain — and
directly underneath [Autonomous Decision-Making's](../decision-making/index.md) mission
logic, which calls navigation as one action among several.

**Needs**: [Mapping and World Models](../mapping-world-models/index.md) — a saved map and AMCL
localizing on it.

**Leads into**: [Autonomous Decision-Making](../decision-making/index.md) treats
`NavigateToPose` as one action a state machine or behavior tree can call,
retry, or replace with a different one on failure.

## Learning objectives

By the end of this topic you can:

1. name the four main Nav2 servers and what each is responsible for;
2. explain the difference between the global and local costmap;
3. send the robot to a goal and observe it re-plan around a new obstacle;
4. name at least one Nav2 capability beyond a single goal (waypoints,
   keepout zones, or docking).

## How the complete system fits together

```{figure} ../_static/images/diagrams/nav2-architecture-simplified.svg
:alt: A navigation goal enters the BT Navigator, which coordinates a Planner Server reading the Global Costmap, a Controller Server reading the Local Costmap, and a Behavior Server for recovery actions. The Controller Server outputs cmd_vel.
:width: 100%

The BT Navigator dispatches to three servers; the Controller Server is the
only one that outputs `/cmd_vel`.
```

Navigation is exposed as a ROS 2 action (`NavigateToPose`,
[ROS 2](../ros2/services-parameters-actions.md#try-it-yourself-actions)):
a goal pose in, feedback while driving, a result at the end. Its inputs are
the map ([Mapping and World Models](../mapping-world-models/index.md)), the localized pose, and
live sensor data; its output is `/cmd_vel`
([ROS 2](../ros2/topics-and-messages.md)).

## How ALeRT uses this topic

{{ alert }} {{ documented }}

Spot navigates with `ros2 launch webots_spot nav_launch.py` — the same
Planner/Controller/Behavior split this topic teaches, on a legged
platform whose local costmap has to account for a wider, less predictable
footprint than a wheeled robot's. **Sensors/actuators**: the same 2D
`/scan` and localized pose from [Mapping and World Models](../mapping-world-models/index.md),
feeding Nav2's costmaps directly. **Typical team task**: comparing
recovery-behaviour outcomes across repeated attempts at the same goal,
since a legged platform's failure modes are less repeatable than a
wheeled one's — see this topic's [Try it on
Spot](practical-exercise.md#try-it-on-spot).
**Verification status**: {{ simulation }} confirmed in Webots.

## Working through this topic

```text
1. Nav2 architecture and costmaps
2. Practical navigation exercise
```

**Interesting videos** and **Continue learning** are worthwhile
afterwards, but are not required to move on to the next topic.

## Subtopics

::::{grid} 1 1 2 2
:gutter: 2

:::{grid-item-card} Nav2 architecture and costmaps
:link: nav2-architecture-and-costmaps
:link-type: doc

{{ foundation }} The Planner/Controller/Behavior split, global vs. local
costmaps, and a first goal sent by hand.
:::

:::{grid-item-card} Practical exercise
:link: practical-exercise
:link-type: doc

{{ foundation }} Send the robot to a goal, introduce an obstacle, and watch it
re-plan — plus this topic's Try it on Spot section.
:::

:::{grid-item-card} Interesting videos
:link: videos
:link-type: doc

One carefully checked video recommendation.
:::

:::{grid-item-card} Continue learning
:link: continue-learning
:link-type: doc

Costmap tuning, behavior trees, waypoints and keepout zones, docking,
navigation metrics, autonomous exploration.
:::

::::

## Prerequisites

[Mapping and World Models](../mapping-world-models/index.md) completed — a saved map and AMCL
localizing on it. Nav2 will not work without a reliable
`map`→`odom`→`base_link` chain.

## Connection to the next topic

This topic sent the robot to *one* goal you chose.
[Autonomous Decision-Making](../decision-making/index.md) has it choose its own next step,
including what to do when something fails.

## Further reading

- [Nav2 documentation](https://docs.nav2.org/humble/)
- [Nav2 configuration guide](https://docs.nav2.org/humble/configuration_and_development/configuration_guide/)
- [Nav2 first-time setup](https://docs.nav2.org/humble/configuration_and_development/first_time_robot_setup_guide/)
- [Behavior trees in Nav2](https://docs.nav2.org/humble/configuration_and_development/configuration_guide/core_servers/bt_plugins/)
  — the bridge to [Autonomous Decision-Making](../decision-making/index.md)

```{toctree}
:maxdepth: 1
:hidden:

nav2-architecture-and-costmaps
practical-exercise
videos
continue-learning
```
