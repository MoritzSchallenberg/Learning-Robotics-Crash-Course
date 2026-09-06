# Sensors, TF2 and RViz

## Overview

A LiDAR measures "2.4 metres, that way." That is useless until you know
*where the sensor is* and *where the robot is*. This topic covers the
machinery that answers those questions — coordinate frames — and seeing
it all in RViz.

**The problem it solves**: every sensor reading is meaningless without a
frame to place it in; TF2 is ROS 2's shared answer to "where is this,
relative to that", used identically whether "this" is a laser point, a
detected marker, or a navigation goal.

**Where it sits in the system**: right after
[ROS 2's](../ros2/index.md) nodes and topics, and directly underneath every
later topic — [Perception's](../perception/index.md) detections,
[Mapping and World Models's](../mapping-world-models/index.md) map, and
[Navigation and Exploration's](../navigation-exploration/index.md) navigation goals are all TF frames under
the hood.

**Needs**: [ROS 2](../ros2/index.md) — you can start a node, read a topic,
and set a parameter.

**Leads into**: [Perception](../perception/index.md) reuses this topic's
TF listener pattern directly to turn a detected marker into a usable
position; [Mapping and World Models](../mapping-world-models/index.md) explains why the tree
splits at `odom` and adds the moving half of it.

## Learning objectives

By the end of this topic you can:

1. read a `LaserScan` message and explain what each field means;
2. read a TF tree and explain the difference between a static and a
   dynamic transform;
3. diagnose and fix the most common reason nothing appears in RViz;
4. write a minimal TF listener node.

## How the complete system fits together

```{figure} ../_static/images/diagrams/tf-tree.svg
:alt: A tree of coordinate frames. Map connects to Odom with a dynamic transform corrected by localization. Odom connects to Base Footprint with a dynamic transform from odometry. Base Footprint connects to Base Link with a static transform, and Base Link connects to Laser Frame, Camera Link and IMU Link, each with a static transform.
:width: 100%

`map`→`odom`→`base_link` is dynamic (published continuously); `base_link`→
sensor frames is static (published once).
```

Every sensor publishes a message carrying a `frame_id`; TF2 tracks the
transform from that frame back to `base_link`, `odom`, or `map`, so any
node — including one written by a completely different team, in a later
topic — can ask "where is this point, in the frame I actually need?"
without knowing anything about how the sensor is physically mounted.

## How ALeRT uses this topic

{{ alert }} {{ documented }}

Spot's TF tree runs from `base_footprint` up through the 3D LiDAR,
gripper camera and odometry frames — see the [platform
page](../platforms/spot/index.md#rviz-setup) for the exact RViz displays
used. **Typical team task**: confirming `/scan` (Spot's LiDAR flattened
to 2D) is set to Best Effort reliability in every new RViz config, since
this is the single most common "nothing shows up" cause the team
encounters. **Known peculiarity**: {{ documented }} the Best Effort
setting on `/scan` is "not optional" per the platform page — the
publisher uses it, and a Reliable display shows nothing, with no error.
**Verification status**: {{ simulation }} confirmed in Webots.

## Working through this topic

```text
1. LaserScan and coordinate frames
2. Practical TF and RViz exercise
```

**Interesting videos** and **Continue learning** are worthwhile
afterwards, but are not required to move on to the next topic.

## Subtopics

::::{grid} 1 1 2 2
:gutter: 2

:::{grid-item-card} LaserScan and coordinate frames
:link: laserscan-and-frames
:link-type: doc

{{ foundation }} Reading a LaserScan, the TF tree, static transforms, and a
minimal TF listener node.
:::

:::{grid-item-card} Practical TF and RViz exercise
:link: practical-exercise
:link-type: doc

{{ foundation }} Diagnose and fix a missing transform, plus this topic's Try
it on Spot section.
:::

:::{grid-item-card} Interesting videos
:link: videos
:link-type: doc

One carefully checked video recommendation.
:::

:::{grid-item-card} Continue learning
:link: continue-learning
:link-type: doc

URDF/Xacro, timestamps, sensor synchronisation, rosbag2, sensor fusion,
extrinsic calibration, PointCloud2.
:::

::::

## Prerequisites

[ROS 2](../ros2/index.md) completed — you can start a node, read a topic, and
set a parameter.

## Connection to the next topic

This topic placed *distance* data in space. [Perception](../perception/index.md)
places *camera* data in space — detecting a marker and publishing where it
actually is, using this same TF machinery.

## Further reading

- [TF2 tutorials](https://docs.ros.org/en/humble/Tutorials/Intermediate/Tf2/Tf2-Main.html)
- [REP 105: Coordinate frames for mobile platforms](https://www.ros.org/reps/rep-0105.html)
- [About Quality of Service settings](https://docs.ros.org/en/humble/Concepts/Intermediate/About-Quality-of-Service-Settings.html)

```{toctree}
:maxdepth: 1
:hidden:

laserscan-and-frames
practical-exercise
videos
continue-learning
```
