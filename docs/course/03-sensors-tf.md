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

## Continue learning

:::{dropdown} URDF, Xacro and robot_state_publisher — Next step
:icon: light-bulb

**What it is.** A **URDF** (Unified Robot Description Format) file
describes a robot's links and joints in XML; **Xacro** adds macros and
parameters on top so you do not repeat yourself for, say, four identical
wheels. `robot_state_publisher` reads a URDF and **publishes exactly the
static transforms** this module has you write by hand with
`static_transform_publisher` — for a robot with more than two or three
frames, URDF is how real teams actually manage this, not individual
`static_transform_publisher` calls per frame.

**Why it matters.** This module's practical task published one static
transform manually; a real robot might have a dozen. URDF is what makes
that scale.

**Needs.** This module's practical task completed.

**Try it — a mini-project.** Write a minimal URDF for a simple sensor
mount: a `base_link`, one child link for a LiDAR frame, and one for a
camera frame, each connected by a fixed joint with a plausible mounting
offset. Launch it with `robot_state_publisher` and confirm both frames
appear correctly in RViz's TF display.

**Check.** `ros2 run tf2_tools view_frames` shows both sensor frames
correctly parented to `base_link`, with no manual
`static_transform_publisher` call needed.

**Read more.** [URDF: getting
started](https://docs.ros.org/en/humble/Tutorials/Intermediate/URDF/URDF-Main.html) ·
[Xacro](https://docs.ros.org/en/humble/Tutorials/Intermediate/URDF/Using-Xacro-to-Clean-Up-a-URDF-File.html)
:::

:::{dropdown} Timestamps: why every message needs one — Next step
:icon: light-bulb

**What it is.** Every message with a `header` carries a `stamp` — *when*
the data was actually measured, which can be meaningfully earlier than
when a subscriber receives it. TF2 lookups use this: `lookup_transform`
can ask "where was the robot at the time this scan was captured?" instead
of "where is it right now?".

**Why it matters.** Using "now" instead of a message's own stamp is a
common, subtle source of misplaced sensor data — the robot has moved
between capture and processing, especially at higher speeds.

**Needs.** This module's TF listener pattern (Advanced topics above).

**Try it.** In the TF listener snippet above, replace
`rclpy.time.Time()` (meaning "latest available") with the actual
`msg.header.stamp` from a received `LaserScan`, and compare the resulting
transform to the "latest" version while the robot (real or simulated) is
moving.

**Check.** You can explain, in one sentence, a situation where the two
lookups would return different results.

**Read more.** [TF2: time
travel](https://docs.ros.org/en/humble/Tutorials/Intermediate/Tf2/Time-Travel-With-Tf2-Cpp.html)
:::

:::{dropdown} Synchronizing multiple sensors with message_filters — Intermediate
:icon: light-bulb

**What it is.** `message_filters.TimeSynchronizer` (or
`ApproximateTimeSynchronizer`) calls your callback only once matching
messages from **several** topics have arrived, close together in time —
instead of you manually buffering and pairing them up.

**Why it matters.** [Module 4's](04-perception/camera-calibration.md)
camera-and-depth fusion, and any real sensor-fusion task, needs two
streams that were captured at close to the same instant; without a
synchronizer you are pairing whatever happened to arrive most recently on
each topic, which silently drifts out of sync under load.

**Needs.** Two topics publishing at a similar rate — a simulated camera and
LiDAR both work.

**Try it.** Subscribe to two topics with an
`ApproximateTimeSynchronizer` (slop of e.g. 0.05s) and log both messages'
timestamps every time the combined callback fires.

**Check.** The logged timestamp difference between the two messages stays
within your configured slop on every callback.

**Read more.** [message_filters
documentation](https://github.com/ros2/message_filters)
:::

:::{dropdown} Recording and replaying with rosbag2 — Next step
:icon: light-bulb

**What it is.** `ros2 bag record` captures every message on chosen topics
to disk with their original timestamps; `ros2 bag play` replays them as if
they were live — you will use this properly in
[module 8](08-integration.md#core-concepts), but the underlying tool
matters here too: a bag is the easiest way to debug a TF problem offline.

**Why it matters.** Recording once and replaying repeatedly turns a
"the sensor is not in front of me right now" debugging session into
something you can pause, rewind and inspect at leisure.

**Needs.** A working `/scan` publisher, real or simulated.

**Try it.** Record `/scan`, `/tf` and `/tf_static` for 15 seconds while
moving the sensor (or the simulated robot), then play the bag back with
`--clock` and confirm RViz shows the same scan movement.

**Check.** The replayed scan visually matches what you saw live, at the
same points in the recording.

**Read more.** [Module 8: rosbags,
briefly](08-integration.md#core-concepts) ·
[ros2 bag](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data.html)
:::

:::{dropdown} IMU and odometry fusion with robot_localization — Intermediate
:icon: light-bulb

**What it is.** `robot_localization`'s `ekf_node` fuses multiple sources of
motion estimate — wheel odometry and an IMU, typically — into one smoother,
more accurate `odom`→`base_link` transform than either source alone.
[Module 5](05-mapping-localization.md#core-concepts) covers *why* odometry
drifts; this is the standard tool for reducing that drift.

**Why it matters.** Wheel odometry alone drifts badly on wheel slip; an IMU
alone drifts in orientation over time. Fused, each corrects the other's
weak point.

**Needs.** A source of wheel odometry and IMU data (real or simulated).

**Try it.** {{ unverified }} — install `robot_localization`, configure a
minimal `ekf_node` with wheel odometry and IMU as inputs, and compare its
output `odom`→`base_link` transform against raw wheel odometry alone while
driving a known path.

**Check.** You can state, with a concrete before/after transform reading,
whether fusion visibly reduced drift on your test path.

**Read more.** [robot_localization
documentation](https://docs.ros.org/en/ros2_packages/humble/api/robot_localization/)
:::

:::{dropdown} Calibrating between sensors — Advanced
:icon: light-bulb

**What it is.** **Extrinsic calibration**: finding the *actual* transform
between two sensors (e.g. camera and LiDAR) precisely enough that data from
both agrees — as opposed to this module's static transform, which is only
as accurate as your tape-measure estimate.

**Why it matters.** A few centimetres or a couple of degrees of error in a
hand-measured static transform is invisible with one sensor, but shows up
immediately as misaligned data once you fuse two — exactly the kind of
error module 4's camera-LiDAR fusion work depends on being small.

**Needs.** Two sensors viewing an overlapping area, and
[module 4's camera calibration](04-perception/camera-calibration.md)
completed first.

**Try it.** {{ unverified }} — research one open-source
LiDAR-camera extrinsic calibration tool and describe, in your own words,
what target (checkerboard, ArUco board) and procedure it requires.

**Check.** You can name the calibration target type and roughly how many
captured views it typically needs.

**Read more.** {{ unverified }} — search for "LiDAR camera extrinsic
calibration ROS 2"; tooling in this space changes often enough that this
course does not pin one specific package.
:::

:::{dropdown} PointCloud2 — Advanced
:icon: light-bulb

**What it is.** `sensor_msgs/msg/PointCloud2` represents a 3D point cloud —
the natural output of a depth camera or a 3D LiDAR, and a step up in
complexity from the 2D `LaserScan` this module covers: each point carries
`x, y, z` (and often more fields, like color or intensity), packed in a
binary layout described by the message's own field metadata rather than a
flat array.

**Why it matters.** [ALeRT/Spot's](../platforms/alert-spot.md) 3D LiDAR
publishes `PointCloud2`, not `LaserScan`; several of
[module 5's](05-mapping-localization.md#advanced-topics) advanced 3D
mapping topics (Octomap, GLIM) consume it directly.

**Needs.** A `PointCloud2` source — a simulated depth camera or 3D LiDAR.

**Try it.** Use `sensor_msgs_py.point_cloud2.read_points` to iterate over
one received `PointCloud2` message and print the `x, y, z` of its first ten
points.

**Check.** The printed values are plausible 3D coordinates (small numbers
in metres, not garbage), confirming you decoded the binary layout
correctly.

**Read more.** [PointCloud2
message](https://docs.ros.org/en/humble/p/sensor_msgs/) ·
[sensor_msgs_py.point_cloud2](https://github.com/ros2/common_interfaces/blob/humble/sensor_msgs_py/sensor_msgs_py/point_cloud2.py)
:::

## Connection to the next module

This module placed *distance* data in space. [Module 4](04-perception/index.md)
places *camera* data in space — detecting a marker and publishing where it
actually is, using this same TF machinery.

## Further reading

- [TF2 tutorials](https://docs.ros.org/en/humble/Tutorials/Intermediate/Tf2/Tf2-Main.html)
- [REP 105: Coordinate frames for mobile platforms](https://www.ros.org/reps/rep-0105.html)
- [About Quality of Service settings](https://docs.ros.org/en/humble/Concepts/Intermediate/About-Quality-of-Service-Settings.html)
