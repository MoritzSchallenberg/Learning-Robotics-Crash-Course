# 3. Sensors, TF2 and RViz

{{ common }}

A LiDAR measures "2.4 metres, that way." That is useless until you know
*where the sensor is* and *where the robot is*. This module covers the
machinery that answers those questions — coordinate frames — and seeing it
all in RViz.

## Overview

You will learn to read a `LaserScan` message, understand the TF tree that
places any sensor reading in space, and visualize both in RViz — including
diagnosing and fixing the most common reason nothing appears at all.

## Learning objectives

By the end of this module you can:

1. read a `LaserScan` message and explain what each field means;
2. read a TF tree and explain the difference between a static and a dynamic
   transform;
3. visualize sensor data in RViz, including fixing the most common reason
   nothing appears.

## Prerequisites

[Module 2](02-ros2.md) completed — you can start a node, read a topic, and
set a parameter.

## Core concepts

### Reading a LaserScan

A `LaserScan` is not a list of points — it is a list of *distances*, plus
enough metadata to work out the direction of each one.

```{figure} ../_static/images/diagrams/04-lidar-scan-angles.svg
:alt: A robot at the centre of a fan of laser rays sweeping from angle_min to angle_max, with two example rays hitting a wall labelled with their measured range, and one ray showing an infinite reading meaning no obstacle was found within range_max.
:width: 100%

`ranges[i]` is measured at `angle_min + i × angle_increment`. `.inf` means
nothing was detected within `range_max`.
```

```yaml
header: {frame_id: laser_frame}
angle_min: -3.14
angle_max: 3.14
angle_increment: 0.0087
range_min: 0.45
range_max: 100.0
ranges: [.inf, .inf, 7.115, 6.744, ...]
```

Two things bite people immediately: `.inf`/`nan` entries are normal and code
that does not handle them crashes on the first open direction; and
`frame_id` says *which sensor frame* these numbers are relative to — which
is where TF2 comes in.

### Coordinate frames, minimally

Each part of the robot gets its own **frame**. TF2 tracks the relationships
between them so any node can ask: *where is this point, in that frame?*

```{figure} ../_static/images/diagrams/03-tf-tree.svg
:alt: A tree of coordinate frames. Map connects to Odom with a dynamic transform corrected by localization. Odom connects to Base Footprint with a dynamic transform from odometry. Base Footprint connects to Base Link with a static transform, and Base Link connects to Laser Frame, Camera Link and IMU Link, each with a static transform.
:width: 100%

`map`→`odom`→`base_link` is dynamic (published continuously); `base_link`→
sensor frames is static (published once).
```

`map` → `odom` → `base_footprint` → `base_link` is the standard convention.
Every node underneath can get a smooth local estimate (via `odom`) or a
globally correct one (via `map`), as needed. Module 5 explains *why* the
tree splits at `odom` — for this module, the important part is the last
hop: `base_link` → sensor frame, which is **static** — it never changes
because the sensor is bolted where it is bolted.

```bash
ros2 run tf2_ros static_transform_publisher x y z yaw pitch roll parent child
```

:::{warning}
Argument order is `x y z yaw pitch roll` — not roll, pitch, yaw. Getting this
backwards is the single most common TF mistake, and it is very visible: your
sensor data appears rotated or on the wrong side of the robot.
:::

## Guided example

RViz showing nothing is the single most common problem in this module, so
work through the diagnosis once, deliberately, before you need it under
pressure:

1. Start any node that publishes `/scan`, then open RViz and add a
   `LaserScan` display on it, with **Fixed Frame** set to a frame you have
   not actually set up yet (e.g. `map`). Confirm: nothing appears.
2. Change **Fixed Frame** to `base_link`. Still nothing? That rules out
   "wrong fixed frame" and points at the transform tree or the data itself.
3. Check the data exists at all: `ros2 topic hz /scan`. No output means the
   problem is upstream of RViz entirely — a driver that is not running.
4. Check the transform tree: `ros2 run tf2_tools view_frames`, then open
   `frames.pdf`. A disconnected frame is visible immediately as a gap.
5. If the tree is complete and data is flowing but the display is still
   empty, check Quality of Service: `ros2 topic info -v /scan`. Set the
   RViz display's Reliability to *Best Effort* or *System Default* — sensor
   drivers rarely publish *Reliable*, and a mismatch produces no error at
   all, just silence.

Every "why is nothing showing?" question in this course reduces to one of
these four checks, in this order.

## Practical task

### Goal
Get a laser scan visible in RViz, correctly placed relative to the robot,
by publishing one missing static transform.

### Starting point
A workspace with a `robot_bringup` package containing a launch file that
starts a simulated (or real) LiDAR publishing `/scan`, but is
**deliberately missing** the `base_link` → `laser_frame` transform — you
can build this scenario yourself by taking any working sensor launch file
and removing its `static_transform_publisher` node.

### Steps
1. `ros2 launch robot_bringup sensors.launch.yaml`
2. Start RViz: `rviz2`. Set **Fixed Frame** to `base_link`.
3. Add a `LaserScan` display on `/scan`. Confirm nothing appears.
4. Run `ros2 run tf2_tools view_frames` and open `frames.pdf` — find the gap.
5. Publish the missing transform. Measure your sensor's actual mounting
   position and orientation on the robot; if you have no robot to measure
   and need a documented example to work from, a LiDAR mounted 15 cm above
   `base_link` and rotated 180° about its vertical axis publishes with:
   `ros2 run tf2_ros static_transform_publisher 0 0 0.15 0 0 3.14159
   base_link laser_frame`
6. Add the same line to `sensors.launch.yaml` as a `static_transform_publisher`
   node so it starts automatically next time.
7. Restart the launch file and confirm the scan now appears.

## Expected result

Laser points appear in RViz, aligned with any obstacle you place in front of
the real or simulated sensor.

## Verification

```bash
ros2 run tf2_ros tf2_echo base_link laser_frame
```

Prints the transform continuously and matches what you published. Moving an
obstacle in front of the sensor moves the corresponding points in RViz.

## Common problems

- **Still nothing after adding the transform** — check the **fixed frame**
  in RViz is `base_link`, not something that does not exist.
- **Scan appears mirrored or rotated 180°** — swapped roll/pitch/yaw order,
  or parent/child reversed.
- **Nothing appears and there is no error at all** — QoS mismatch. Set the
  display's Reliability to *Best Effort* or *System Default*; sensor
  drivers rarely publish *Reliable*.
- **`No transform from [X] to [Y]`.** Either the transform genuinely is not
  published, or the fixed frame is wrong. `view_frames` shows which.
- **The scan drifts from the walls as the robot turns.** The static
  transform's rotation is off, or you mixed static with a dynamic use case.

## Optional extensions

{{ optional }}

Add a second static transform for a camera or IMU frame of your choosing,
and add both to the `TF` display in RViz to see the whole tree at once.

No LiDAR available? Any Webots example with a LiDAR works identically — the
transform, the `view_frames` diagnosis, and the fix are the same regardless
of whether the scan is real or simulated. Simulated TF trees are often
complete already; if so, deliberately remove one static transform from the
launch file to recreate this module's exercise.

## Advanced topics

{{ advanced }}

:::{dropdown} A minimal TF listener node
:icon: light-bulb

```python
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

# in __init__:
self.tf_buffer = Buffer()
self.tf_listener = TransformListener(self.tf_buffer, self)

# in a timer callback:
try:
    t = self.tf_buffer.lookup_transform('base_link', 'laser_frame', rclpy.time.Time())
except TransformException as ex:
    self.get_logger().info(f'lookup failed: {ex}')
    return
```

Catch `TransformException` specifically — a lookup legitimately fails while
the buffer is still filling at startup, and a bare `except:` also swallows
`KeyboardInterrupt`. You will reuse this exact pattern in
[module 4](04-perception/fiducial-markers.md) to turn a detected marker
into a usable position.
:::

:::{dropdown} IMU and dynamic transforms, briefly
:icon: light-bulb

An IMU (`sensor_msgs/msg/Imu`) gives angular velocity and linear
acceleration directly from the sensor frame — useful for orientation, but
like any sensor it has noise and drift of its own. A **dynamic** transform
(`odom`→`base_link`, published on `/tf` rather than `/tf_static`) changes
every cycle as the robot moves; module 5 is where you first publish one for
real.
:::

## Connection to the next module

This module placed *distance* data in space. [Module 4](04-perception/index.md)
places *camera* data in space — detecting a marker and publishing where it
actually is, using this same TF machinery.

## Further reading

- [TF2 tutorials](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Tf2-Main.html)
- [REP 105: Coordinate frames for mobile platforms](https://www.ros.org/reps/rep-0105.html)
- [About Quality of Service settings](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Quality-of-Service-Settings.html)
