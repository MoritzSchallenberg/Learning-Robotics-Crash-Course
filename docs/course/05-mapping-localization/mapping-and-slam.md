# Mapping and SLAM

{{ common }} {{ core }}

## What this topic is

**Odometry** is the robot's own estimate of how far it has travelled, from
wheel encoders (often fused with an IMU). An **occupancy grid** is a 2D map:
the world divided into cells, each `0` (free), `100` (occupied), or `-1`
(unknown). **SLAM** (Simultaneous Localization And Mapping) builds an
occupancy grid while simultaneously working out where the robot is within
it.

## Why a robot needs it

Odometry is **smooth** — the estimate never jumps — but it **drifts**:
small errors accumulate and are never corrected on their own. Building a
map from raw odometry alone means the map itself drifts. SLAM solves both
problems at once, by recognising previously seen places and using that
match to correct the drift accumulated since.

## How it works

Odometry alone cannot build a trustworthy map: measure the drift for
yourself before relying on any map built from it.

```bash
ros2 run tf2_ros tf2_echo odom base_link
```

Note the printed translation, then drive the robot (or teleoperate it in
simulation) in a square, back to the exact spot it started from, and read
the transform again. The gap between the two readings is the drift — good
over a few metres, unreliable after a few minutes.

SLAM Toolbox closes that gap with **loop closure**: recognising a
previously seen place and using the match to correct everything mapped
since. This is exactly why the practical exercise on this module's next
subpage asks you to drive slowly and close loops, rather than trusting
odometry over a long, one-way path.

A saved map is two files: `map.pgm` (the image) and `map.yaml` (resolution,
origin, thresholds) — produced by `nav2_map_server`'s `map_saver_cli`, used
on the practical exercise's next step.

## Inputs and outputs

SLAM Toolbox subscribes to `/scan` (a `LaserScan`, see
[module 3](../03-sensors-tf/laserscan-and-frames.md)) and the
`odom`→`base_link` transform, and publishes an occupancy grid on `/map`
plus the `map`→`odom` transform — the correction that keeps `odom`'s
smooth drift from accumulating forever.

```{figure} ../../_static/images/diagrams/06-mapping-localization-dataflow.svg
:alt: Two modes sharing laser scan and odometry as inputs. Mapping mode feeds SLAM Toolbox, producing an occupancy grid map and the map to odom transform. Localization mode feeds a saved map plus scan and odometry into AMCL, producing a corrected pose and the same map to odom transform.
:width: 100%

Mapping mode (this page) and localization mode
([the next subtopic](localization-and-3d-mapping.md)) publish the same
`map`→`odom` transform, but only one of the two nodes may run at a time.
```

## Try it yourself

Start SLAM Toolbox against a live `/scan` and `odom` (your own bringup, or
a simulation), drive slowly in a loop around the space, and watch the map
form in RViz (fixed frame `map`). Save it once the shape looks right:

```bash
ros2 run nav2_map_server map_saver_cli -f ~/course_ws/my_map
```

The full end-to-end walkthrough, with exact launch commands for your own
workspace or platform, is this module's
[practical exercise](practical-exercise.md).

## How ALeRT applies it

{{ alert }} {{ simulation }} Spot maps with `ros2 launch webots_spot
slam_launch.py` — the same SLAM Toolbox this page teaches, just a
platform-specific launch file. See this module's [Try it on
Spot](practical-exercise.md#try-it-on-spot).

## How Carologistics applies it

{{ carologistics }} {{ documented }} Robotino does not typically map live
during competition — [`mps-map-gen`](../../platforms/carologistics-robotino.md#key-repositories)
extends a pre-built map-server map with game-specific information instead.
The underlying occupancy-grid representation is identical; only *when* the
map is built differs.

## Common problems

- **The map is doubled or smeared.** Driven too fast, or collided with
  something. There is no fix but starting the map over, slowly.
- **No map appears in RViz.** QoS: `/map` is Transient Local; set the
  display's Durability to match, or to *System Default*.

## Next subtopic

[Localization and 3D mapping](localization-and-3d-mapping.md) — finding the
robot's pose on a map that already exists.
