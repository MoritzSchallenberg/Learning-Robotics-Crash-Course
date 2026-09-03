# LaserScan and coordinate frames

{{ common }} {{ core }}

## What this topic is

Two things a robot needs to place any sensor reading in space: the
message that carries the reading (`LaserScan` here), and the machinery
(**TF2**) that says where the sensor that produced it actually is.

## Why a robot needs it

A LiDAR measures "2.4 metres, that way." That is useless until you know
*where the sensor is* and *where the robot is* — every later module's
sensor data (camera, point cloud, odometry) is placed in space the same
way this page teaches for a 2D laser scan.

## How it works: reading a LaserScan

A `LaserScan` is not a list of points — it is a list of *distances*, plus
enough metadata to work out the direction of each one.

```{figure} ../../_static/images/diagrams/04-lidar-scan-angles.svg
:alt: A robot at the centre of a fan of laser rays sweeping from angle_min to angle_max, with two example rays hitting a wall labelled with their measured range, and one ray showing an infinite reading meaning no obstacle was found within range_max.
:width: 100%

`ranges[i]` is measured at `angle_min + i × angle_increment`. `.inf` means
nothing was detected within `range_max`.
```

## Inputs and outputs

```yaml
header: {frame_id: laser_frame}
angle_min: -3.14
angle_max: 3.14
angle_increment: 0.0087
range_min: 0.45
range_max: 100.0
ranges: [.inf, .inf, 7.115, 6.744, ...]
```

Two things bite people immediately: `.inf`/`nan` entries are normal and
code that does not handle them crashes on the first open direction; and
`frame_id` says *which sensor frame* these numbers are relative to —
which is where TF2 comes in.

## How it works: coordinate frames

Each part of the robot gets its own **frame**. TF2 tracks the
relationships between them so any node can ask: *where is this point, in
that frame?*

```{figure} ../../_static/images/diagrams/03-tf-tree.svg
:alt: A tree of coordinate frames. Map connects to Odom with a dynamic transform corrected by localization. Odom connects to Base Footprint with a dynamic transform from odometry. Base Footprint connects to Base Link with a static transform, and Base Link connects to Laser Frame, Camera Link and IMU Link, each with a static transform.
:width: 100%

`map`→`odom`→`base_link` is dynamic (published continuously); `base_link`→
sensor frames is static (published once).
```

`map` → `odom` → `base_footprint` → `base_link` is the standard
convention. Every node underneath can get a smooth local estimate (via
`odom`) or a globally correct one (via `map`), as needed.
[Module 5](../05-mapping-localization.md) explains *why* the tree splits
at `odom` — for this module, the important part is the last hop:
`base_link` → sensor frame, which is **static** — it never changes
because the sensor is bolted where it is bolted.

```bash
ros2 run tf2_ros static_transform_publisher x y z yaw pitch roll parent child
```

:::{warning}
Argument order is `x y z yaw pitch roll` — not roll, pitch, yaw. Getting this
backwards is the single most common TF mistake, and it is very visible: your
sensor data appears rotated or on the wrong side of the robot.
:::

## Small example: a minimal TF listener node

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

Catch `TransformException` specifically — a lookup legitimately fails
while the buffer is still filling at startup, and a bare `except:` also
swallows `KeyboardInterrupt`. You will reuse this exact pattern in
[module 4](../04-perception/fiducial-markers.md) to turn a detected
marker into a usable position.

An IMU (`sensor_msgs/msg/Imu`) gives angular velocity and linear
acceleration directly from the sensor frame — useful for orientation, but
like any sensor it has noise and drift of its own. A **dynamic** transform
(`odom`→`base_link`, published on `/tf` rather than `/tf_static`) changes
every cycle as the robot moves; [module 5](../05-mapping-localization.md)
is where you first publish one for real.

## How ALeRT applies it

{{ alert }} {{ simulation }} Spot's TF tree is rooted at `base_footprint`,
with the 3D LiDAR, gripper camera and odometry all as frames off it — see
[the practical exercise's Try it on Spot](practical-exercise.md#try-it-on-spot)
for building it yourself in RViz.

## How Carologistics applies it

{{ carologistics }} {{ documented }} Robotino's `laser_scan_integrator`
node merges two `LaserScan` topics into one, "accounting for their
relative positions via TF and the robot's footprint" — see the
[platform page](../../platforms/carologistics-robotino.md#key-repositories)
— a direct, production use of exactly the static-transform mechanism this
page teaches.

## Common problems

- **`No transform from [X] to [Y]`.** Either the transform genuinely is
  not published, or the fixed frame is wrong.

## Next subtopic

[Practical TF and RViz exercise](practical-exercise.md) — diagnose and
fix a missing transform yourself.

## Sources

- [TF2 tutorials](https://docs.ros.org/en/humble/Tutorials/Intermediate/Tf2/Tf2-Main.html)
- [REP 105: Coordinate frames for mobile platforms](https://www.ros.org/reps/rep-0105.html)
