# Practical TF and RViz exercise

{{ common }} {{ core }}

## Guided example: diagnosing "RViz shows nothing"

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

## Goal

Get a laser scan visible in RViz, correctly placed relative to the robot,
by publishing one missing static transform.

## Starting point

A workspace with a `robot_bringup` package containing a launch file that
starts a simulated (or real) LiDAR publishing `/scan`, but is
**deliberately missing** the `base_link` → `laser_frame` transform — you
can build this scenario yourself by taking any working sensor launch file
and removing its `static_transform_publisher` node.

## Steps

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
launch file to recreate this exercise.

## Try it on Spot

{{ alert }} {{ spotsim }}

Build the RViz setup from the [platform
page](../../platforms/alert-spot.md#rviz-setup) yourself, using this
page's own diagnosis procedure rather than the platform page's
already-finished list:

1. Set **Fixed Frame** to `base_footprint` and add a `TF` display —
   confirm the tree is connected with `ros2 run tf2_tools view_frames`,
   exactly as in the guided example above.
2. Add `RobotModel` (topic `/robot_description`) — this is a robot's own
   structure, rendered from a real URDF instead of drawn as a diagram.
3. Add `PointCloud2` on the 3D LiDAR topic, `Odometry`, and `LaserScan` on
   `/scan` — and apply this page's own QoS lesson **before** being told
   the answer: if `/scan` shows nothing, check reliability first, not the
   transform tree.
4. Add `Image` on the gripper camera topic.
5. Measure each sensor's actual publish rate with `ros2 topic hz`, and
   record a short rosbag of all of them together:
   `ros2 bag record /scan /Spot/odometry -o spot_sensors`.

:::{admonition} Task: diagnose it yourself
:class: task

Before reading the platform page's finished RViz setup, remove **one**
display you just added (or leave one on the wrong QoS setting) and run
the guided example's four-step "nothing shows up" procedure against it.
Did it find the fault at the step you expected?
:::

**Verification**: every display shows real data, and you can state, from
memory, which QoS setting `/scan` needs and why (Spot's LiDAR-derived scan
publishes Best Effort, same as most real sensor drivers).

## Next subtopic

[Interesting videos](videos.md), then
[Continue learning](continue-learning.md).
