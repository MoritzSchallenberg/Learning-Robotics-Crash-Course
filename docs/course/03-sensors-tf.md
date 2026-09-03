# 3. Sensors, TF2 and RViz

{{ common }}

## Module overview

A LiDAR measures "2.4 metres, that way." That is useless until you know
*where the sensor is* and *where the robot is*. This module covers the
machinery that answers those questions — coordinate frames — and seeing
it all in RViz.

**The problem it solves**: every sensor reading is meaningless without a
frame to place it in; TF2 is ROS 2's shared answer to "where is this,
relative to that", used identically whether "this" is a laser point, a
detected marker, or a navigation goal.

**Where it sits in the system**: right after
[module 2's](02-ros2.md) nodes and topics, and directly underneath every
later module — [module 4's](04-perception/index.md) detections,
[module 5's](05-mapping-localization.md) map, and
[module 6's](06-navigation.md) navigation goals are all TF frames under
the hood.

**Needs**: [module 2](02-ros2.md) — you can start a node, read a topic,
and set a parameter.

**Leads into**: [module 4](04-perception/index.md) reuses this module's
TF listener pattern directly to turn a detected marker into a usable
position; [module 5](05-mapping-localization.md) explains why the tree
splits at `odom` and adds the moving half of it.

## Learning objectives

By the end of this module you can:

1. read a `LaserScan` message and explain what each field means;
2. read a TF tree and explain the difference between a static and a
   dynamic transform;
3. diagnose and fix the most common reason nothing appears in RViz;
4. write a minimal TF listener node.

## How the complete system fits together

```{figure} ../_static/images/diagrams/03-tf-tree.svg
:alt: A tree of coordinate frames. Map connects to Odom with a dynamic transform corrected by localization. Odom connects to Base Footprint with a dynamic transform from odometry. Base Footprint connects to Base Link with a static transform, and Base Link connects to Laser Frame, Camera Link and IMU Link, each with a static transform.
:width: 100%

`map`→`odom`→`base_link` is dynamic (published continuously); `base_link`→
sensor frames is static (published once).
```

Every sensor publishes a message carrying a `frame_id`; TF2 tracks the
transform from that frame back to `base_link`, `odom`, or `map`, so any
node — including one written by a completely different team, in a later
module — can ask "where is this point, in the frame I actually need?"
without knowing anything about how the sensor is physically mounted.

## How ALeRT uses this topic

{{ alert }} {{ documented }}

Spot's TF tree runs from `base_footprint` up through the 3D LiDAR,
gripper camera and odometry frames — see the [platform
page](../platforms/alert-spot.md#rviz-setup) for the exact RViz displays
used. **Typical team task**: confirming `/scan` (Spot's LiDAR flattened
to 2D) is set to Best Effort reliability in every new RViz config, since
this is the single most common "nothing shows up" cause the team
encounters. **Known peculiarity**: {{ documented }} the Best Effort
setting on `/scan` is "not optional" per the platform page — the
publisher uses it, and a Reliable display shows nothing, with no error.
**Verification status**: {{ simulation }} confirmed in Webots.

## How Carologistics uses this topic

{{ carologistics }} {{ documented }}

Robotino's `laser_scan_integrator` node "merges two laser scans into one,
accounting for their relative positions via TF and the robot's
footprint" — see the [platform
page](../platforms/carologistics-robotino.md#key-repositories) — a
direct production use of the exact static-transform mechanism this
module teaches, at a scale (two physically offset scanners, continuously
merged) beyond this module's own single-sensor practical task.
**Typical team task**: verifying a new or moved sensor's static transform
is correct before trusting any detection derived from it, since a wrong
mount transform silently misplaces every downstream reading.
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
* - Main range sensor
  - One 3D LiDAR
  - Two merged 2D laser scanners
  - Both need an accurate static transform to trust
* - TF tree root
  - `base_footprint`
  - {{ unverified }} — not explicitly named on the platform page
  - Both follow REP 105's map/odom/base convention
* - QoS gotcha
  - `/scan` must be Best Effort in RViz
  - {{ unverified }} — not documented, but the same ROS 2 default applies
  - Sensor drivers rarely publish Reliable
* - Multi-sensor fusion
  - {{ unverified }} — not documented at the TF level
  - Two scanners merged into one via TF-aware integration
  - Both need `message_filters` or manual TF-aware merging for more
```

## Core learning path

```text
1. LaserScan and coordinate frames
2. Practical TF and RViz exercise
```

That is this module's roughly 80–100 minute core learning time.
**Interesting videos** and **Continue learning** are worthwhile
afterwards but not required for the core path.

## Subtopics

::::{grid} 1 1 2 2
:gutter: 2

:::{grid-item-card} LaserScan and coordinate frames
:link: 03-sensors-tf/laserscan-and-frames
:link-type: doc

{{ core }} Reading a LaserScan, the TF tree, static transforms, and a
minimal TF listener node.
:::

:::{grid-item-card} Practical TF and RViz exercise
:link: 03-sensors-tf/practical-exercise
:link-type: doc

{{ core }} Diagnose and fix a missing transform, plus this module's Try
it on Spot section.
:::

:::{grid-item-card} Interesting videos
:link: 03-sensors-tf/videos
:link-type: doc

One carefully checked video recommendation.
:::

:::{grid-item-card} Continue learning
:link: 03-sensors-tf/continue-learning
:link-type: doc

URDF/Xacro, timestamps, sensor synchronisation, rosbag2, sensor fusion,
extrinsic calibration, PointCloud2.
:::

::::

## Prerequisites

[Module 2](02-ros2.md) completed — you can start a node, read a topic, and
set a parameter.

## Connection to the next module

This module placed *distance* data in space. [Module 4](04-perception/index.md)
places *camera* data in space — detecting a marker and publishing where it
actually is, using this same TF machinery.

## Further reading

- [TF2 tutorials](https://docs.ros.org/en/humble/Tutorials/Intermediate/Tf2/Tf2-Main.html)
- [REP 105: Coordinate frames for mobile platforms](https://www.ros.org/reps/rep-0105.html)
- [About Quality of Service settings](https://docs.ros.org/en/humble/Concepts/Intermediate/About-Quality-of-Service-Settings.html)

```{toctree}
:maxdepth: 1
:hidden:

03-sensors-tf/laserscan-and-frames
03-sensors-tf/practical-exercise
03-sensors-tf/videos
03-sensors-tf/continue-learning
```
