# 3. Sensors, TF2 and RViz

:::{admonition} Session 3
:class: note

Monday, 12 October 2026, 17:35 – 19:00
:::

{{ common }}

A LiDAR measures "2.4 metres, that way". That is useless until you know where
the LiDAR is on the robot, and where the robot is in the room. This session is
about the machinery that answers those questions — coordinate frames and
transforms — and about seeing it all in RViz.

## Learning objectives

After this session you can:

- name the standard sensor message types and what each contains;
- explain what a coordinate frame is and read a TF tree;
- publish a static transform and check it;
- visualize sensor data in RViz and fix it when nothing appears;
- diagnose the QoS mismatch that silently hides topics;
- look up the transform between any two frames from a node.

## Prerequisites

[Session 2](02-ros2.md). You can write a subscriber and inspect topics from the
command line.

## Sensors and their messages

ROS 2 defines standard message types so that any LiDAR works with any mapping
package. Learning the messages matters more than learning any particular
driver.

```{list-table}
:header-rows: 1
:widths: 22 30 48

* - Sensor
  - Message type
  - What is inside
* - 2D LiDAR
  - `sensor_msgs/msg/LaserScan`
  - An array of ranges, plus the angle the first one starts at and the angle
    between them
* - 3D LiDAR / depth
  - `sensor_msgs/msg/PointCloud2`
  - A packed array of 3D points
* - Camera
  - `sensor_msgs/msg/Image`
  - Pixels, width, height, encoding
* - Camera intrinsics
  - `sensor_msgs/msg/CameraInfo`
  - The calibration matrices — see [session 4](04-perception.md)
* - IMU
  - `sensor_msgs/msg/Imu`
  - Angular velocity, linear acceleration, orientation
* - Wheel odometry
  - `nav_msgs/msg/Odometry`
  - Estimated pose and velocity, with covariances
```

Inspect any of them:

```bash
ros2 interface show sensor_msgs/msg/LaserScan
```

### Reading a LaserScan

A `LaserScan` is not a list of points. It is a list of *distances*, plus enough
metadata to work out the direction of each:

```yaml
header:
  stamp: {sec: 1666101279, nanosec: 103108176}
  frame_id: laser_frame
angle_min: -3.14
angle_max: 3.14
angle_increment: 0.0087
range_min: 0.45
range_max: 100.0
ranges: [.inf, .inf, 7.115, 6.744, 6.387, ...]
```

Three things to notice:

**`frame_id`** — which coordinate frame these measurements are expressed in.
This is the link to everything below.

**`.inf` entries** — nothing was detected in that direction within range. Real
sensor data is full of them, and code that does not handle them crashes on the
first wall-free direction. `nan` appears too, for invalid readings.

**`range_min`** — measurements closer than this are meaningless. An obstacle
pressed against the sensor may report a plausible-looking number.

Index `i` in `ranges` corresponds to angle `angle_min + i * angle_increment`.

### Sensor limits

Every sensor lies, in its own characteristic way:

- **LiDAR** — struggles with glass, mirrors and matte black surfaces; a 2D
  LiDAR sees only one horizontal slice, so it misses a table top at chest
  height and the floor beneath it.
- **Cameras** — depend on lighting; motion blur destroys detection; rolling
  shutter distorts fast-moving objects.
- **IMU** — accurate over short intervals, drifts over long ones.
- **Encoders** — perfect until a wheel slips, and there is nothing in the data
  to tell you when it did.

Knowing the failure mode of each sensor is what lets you diagnose the system
later: if the map is skewed, suspect the odometry; if the obstacle was invisible,
suspect the LiDAR plane.

## Coordinate frames and TF2

### The problem

The LiDAR reports a point 2.4 m ahead of *itself*. The navigation stack wants
to know where that point is relative to the *robot's base*, and the map wants
to know where it is in the *room*. Each of those is a different coordinate
frame, and something has to convert between them.

That something is **TF2**. Each part of the robot gets its own frame, the
relationships between frames are published continuously, and any node can then
ask: *where is this point, expressed in that frame?*

### The standard frames

Robotics has settled on a conventional set of frames, and the entire navigation
stack assumes it:

```text
map            fixed to the world; does not drift, but jumps when
 │             localization corrects itself
 ▼
odom           smooth and continuous, but drifts over time
 │
 ▼
base_footprint the robot's position on the ground plane
 │
 ▼
base_link      the robot's body
 ├──► laser_frame     where the LiDAR is mounted
 ├──► camera_link     where the camera is mounted
 └──► imu_link        where the IMU is mounted
```

The `map` → `odom` → `base_link` split is subtle and important:

**`odom` → `base_link`** is published by the odometry source. It is smooth —
it never jumps — but it drifts, so after ten minutes it is wrong.

**`map` → `odom`** is published by the localization system (session 5). It is
the correction: the difference between where odometry thinks the robot is and
where it actually is. It jumps whenever localization improves its estimate.

The result is a tree in which every node can get a smooth estimate (via `odom`)
or a globally correct one (via `map`), as needed.

:::{note}
Each frame has exactly **one** parent. Two nodes publishing the same transform
produce a tree that flickers between them and behaviour that makes no sense.
`ros2 run tf2_tools view_frames` shows you who publishes what.
:::

### Static versus dynamic transforms

A **static** transform never changes: the LiDAR is bolted to the chassis
15 cm above `base_link` and stays there. Published once, on `/tf_static`.

A **dynamic** transform changes constantly: `odom` → `base_link` changes every
time the robot moves. Published continuously on `/tf`.

### Publishing a static transform

```yaml
launch:

- node:
    pkg: "tf2_ros"
    exec: "static_transform_publisher"
    name: "base_link_to_laser"
    args: '0.0 0.0 0.15 3.14159 0.0 0.0 base_link laser_frame'
```

The arguments are:

```text
x y z yaw pitch roll parent_frame child_frame
```

Translation in **metres**, rotation as Euler angles in **radians**. A
quaternion form is also accepted:

```text
x y z qx qy qz qw parent_frame child_frame
```

The transform describes where the **child** sits relative to the **parent**.
The example above says: `laser_frame` is 15 cm above `base_link`, rotated by π
about the X axis — that is, mounted upside down, which many LiDARs are.

:::{warning}
Getting the direction of a transform backwards is the classic TF mistake. The
arguments describe the child *in the parent's* coordinates. If your sensor data
appears mirrored or on the wrong side of the robot, this is almost always why.
:::

### Inspecting the tree

```bash
# Generate a PDF diagram of the whole tree
ros2 run tf2_tools view_frames

# Print one transform live
ros2 run tf2_ros tf2_echo base_link laser_frame

# Watch the raw topics
ros2 topic echo /tf_static
```

`view_frames` writes `frames.pdf` into the current directory and is the fastest
way to see a broken tree: a disconnected frame stands out immediately.

### Looking up a transform in a node

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener


class FrameListener(Node):

    def __init__(self):
        super().__init__('tf2_listener')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.create_timer(0.25, self.on_timer)

    def on_timer(self):
        from_frame = 'base_link'
        to_frame = 'laser_frame'
        try:
            transform = self.tf_buffer.lookup_transform(
                from_frame, to_frame, rclpy.time.Time())
        except TransformException as ex:
            self.get_logger().info(
                f'Could not transform {from_frame} to {to_frame}: {ex}')
            return

        t = transform.transform.translation
        r = transform.transform.rotation
        self.get_logger().info(
            f'position: ({t.x:.3f}, {t.y:.3f}, {t.z:.3f}) '
            f'orientation: ({r.x:.3f}, {r.y:.3f}, {r.z:.3f}, {r.w:.3f})')


def main():
    rclpy.init()
    node = FrameListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

The listener fills a buffer with recent transforms in the background;
`lookup_transform` then queries it. Passing `rclpy.time.Time()` asks for the
latest available transform.

The two frames do not have to be adjacent. TF2 chains through the tree for you
— which is exactly the point.

:::{warning}
Catch `TransformException` specifically rather than using a bare `except:`. A
lookup legitimately fails while the tree is still being populated at startup,
and a bare except will also swallow the `KeyboardInterrupt` you use to stop the
node.
:::

## RViz

RViz is the 3D viewer for everything ROS 2 publishes. Start it:

```bash
rviz2
```

The workflow is always the same:

1. Set **Fixed Frame** under *Global Options*. This is the frame everything is
   drawn relative to. If it is wrong or does not exist, you see nothing.
2. Click **Add** to add a display.
3. Use the **By topic** tab, which lists what is actually available and
   configures the display for you.

Displays you will use constantly:

`TF`
: every coordinate frame as a set of axes — the first thing to add when
  something looks misplaced

`LaserScan`
: 2D laser data as points

`PointCloud2`
: 3D data

`Image`
: a camera stream in a panel

`RobotModel`
: the robot's geometry, from `/robot_description`

`Map`
: an occupancy grid (session 5)

Save your configuration once it is useful — *File → Save Config As* — and load
it from a launch file. Rebuilding an RViz setup from scratch every session is a
waste of an evening.

### When RViz shows nothing

This happens to everyone, and there are only three causes.

**1. The fixed frame does not exist.**
RViz reports `No transform from [laser_frame] to [map]`. Set the fixed frame to
something that does exist — `base_link` is a safe choice while debugging — or
fix the missing transform.

**2. The topic is not being published.**
Check outside RViz first:

```bash
ros2 topic hz /scan
```

No output means the problem is upstream, not in RViz.

**3. QoS mismatch.**

This is the one that wastes hours, because there is no error message. ROS 2
lets publishers and subscribers negotiate *Quality of Service*, and if their
policies are incompatible, no data flows at all — silently.

Sensor drivers typically publish **Best Effort** (drop a scan rather than delay
one), while RViz defaults to **Reliable**. Result: nothing appears.

Check what the publisher actually offers:

```bash
ros2 topic info -v /scan
```

Then set the display's QoS in RViz to match. In practice:

```{list-table}
:header-rows: 1
:widths: 30 35 35

* - Data
  - Reliability
  - Durability
* - Sensor streams (`/scan`, images)
  - Best Effort
  - Volatile
* - Maps (`/map`)
  - Reliable
  - Transient Local
```

**Transient Local** matters for maps: the map is published once, and a
subscriber that starts later still needs to receive it. A volatile subscriber
would simply never see it.

:::{tip}
Setting a display's Reliability to *System Default* makes RViz adopt the
publisher's setting and resolves most of these cases without thinking about it.
:::

## Task

:::{admonition} Task: build and inspect a transform tree
:class: task

**Part 1 — Visualize the laser.**

1. Start your robot or simulation.
2. Start RViz, set the fixed frame to `base_link`, and add a `LaserScan`
   display on your scan topic.
3. If nothing appears, work through the three causes above. Note which one it
   was.
4. Wave your hand or place an obstacle in front of the sensor and confirm the
   points move.

**Part 2 — Explore the TF tree.**

1. Run `ros2 run tf2_tools view_frames` and open the resulting `frames.pdf`.
2. Draw the tree on paper. Which frames exist? Which node publishes each?
3. Use `ros2 run tf2_ros tf2_echo base_link <sensor_frame>` and compare the
   numbers to where the sensor physically sits on the robot.

**Part 3 — Add a static transform.**

Create a launch file `robot_tf.launch.yaml` in a `robot_bringup` package that
publishes this tree using `static_transform_publisher`:

```{list-table}
:header-rows: 1
:widths: 30 30 40

* - Parent → child
  - Translation (x, y, z) m
  - Rotation (roll, pitch, yaw) rad
* - `base_footprint` → `base_link`
  - (0.0, 0.0, 0.01)
  - (0, 0, 0)
* - `base_link` → `imu_link`
  - (0.0, 0.0, 0.068)
  - (0, 0, 0)
* - `base_link` → `laser_frame`
  - (0.0, 0.0, 0.15)
  - (3.14159, 0, 0)
* - `base_link` → `camera_link`
  - (0.07, 0.0, 0.11)
  - (0, 0, 0)
```

Give every node a distinct `name`. Then visualize the result in RViz with a
`TF` display and fixed frame `base_footprint`.

**Part 4 — Write a TF listener.**

Adapt the listener node above to print the transform between `base_link` and
your laser frame. Then physically move the robot (or drive it in simulation)
and print `odom` → `base_link` instead. Watch the numbers change.
:::

:::{admonition} Expected result
:class: result

In part 1, laser points appear and respond to obstacles.

In part 3, RViz shows four sets of coordinate axes in the right places, and
`laser_frame` is visibly flipped relative to the others.

In part 4, the `base_link` → `laser_frame` numbers stay constant no matter how
the robot moves — it is a static transform. The `odom` → `base_link` numbers
change as the robot drives, and drift slowly even when it does not.
:::

:::{dropdown} Hint: static transform launch file
:icon: light-bulb

```yaml
launch:

- node:
    pkg: "tf2_ros"
    exec: "static_transform_publisher"
    name: "footprint_to_base"
    args: '0.0 0.0 0.01 0.0 0.0 0.0 base_footprint base_link'

- node:
    pkg: "tf2_ros"
    exec: "static_transform_publisher"
    name: "base_to_laser"
    args: '0.0 0.0 0.15 0.0 0.0 3.14159 base_link laser_frame'
```

Note the argument order: `x y z yaw pitch roll`. The table above lists roll,
pitch, yaw — the reverse. Getting this wrong is the most common error in this
task, and it is very visible in RViz.
:::

## Common mistakes

**`No transform from [X] to [Y]`.**
Either the transform is genuinely not published, or the fixed frame is wrong.
`view_frames` tells you which.

**The scan appears rotated 180° or mirrored.**
The rotation in your static transform is wrong, or you swapped parent and
child.

**The scan drifts away from the walls as the robot turns.**
The translation is roughly right but the sensor is not where you said it is.
Measure it.

**Nothing appears and there is no error.**
QoS. Run `ros2 topic info -v`.

**`lookup_transform` always fails at startup.**
Normal — the buffer needs a moment to fill. Catch the exception and try again
next cycle rather than crashing.

**Two nodes publishing the same transform.**
The tree flickers. Only one publisher per parent–child pair.

## Further reading

- [TF2 tutorials](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Tf2-Main.html)
  — the official series, worth doing in full
- [REP 105: Coordinate frames for mobile platforms](https://www.ros.org/reps/rep-0105.html)
  — where `map`, `odom` and `base_link` are actually defined
- [About Quality of Service settings](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Quality-of-Service-Settings.html)
- [RViz user guide](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/RViz/RViz-User-Guide/RViz-User-Guide.html)
