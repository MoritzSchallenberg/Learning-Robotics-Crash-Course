# Continue learning

## Next steps

:::{dropdown} URDF, Xacro and robot_state_publisher — Next step
:icon: light-bulb

**What it is.** A **URDF** (Unified Robot Description Format) file
describes a robot's links and joints in XML; **Xacro** adds macros and
parameters on top so you do not repeat yourself for, say, four identical
wheels. `robot_state_publisher` reads a URDF and **publishes exactly the
static transforms** [the practical exercise](practical-exercise.md) has
you write by hand with `static_transform_publisher` — for a robot with
more than two or three frames, URDF is how real teams actually manage
this, not individual `static_transform_publisher` calls per frame.

**Why it matters.** The practical exercise published one static
transform manually; a real robot might have a dozen. URDF is what makes
that scale.

**Needs.** [The practical exercise](practical-exercise.md) completed.

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

**Needs.** [The TF listener
pattern](../03-sensors-tf/laserscan-and-frames.md#small-example-a-minimal-tf-listener-node).

**Try it.** In the TF listener snippet, replace
`rclpy.time.Time()` (meaning "latest available") with the actual
`msg.header.stamp` from a received `LaserScan`, and compare the resulting
transform to the "latest" version while the robot (real or simulated) is
moving.

**Check.** You can explain, in one sentence, a situation where the two
lookups would return different results.

**Read more.** [TF2: time
travel](https://docs.ros.org/en/humble/Tutorials/Intermediate/Tf2/Time-Travel-With-Tf2-Cpp.html)
:::

:::{dropdown} Recording and replaying with rosbag2 — Next step
:icon: light-bulb

**What it is.** `ros2 bag record` captures every message on chosen topics
to disk with their original timestamps; `ros2 bag play` replays them as if
they were live — you will use this properly in
[module 8](../08-integration.md#core-concepts), but the underlying tool
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
briefly](../08-integration.md#core-concepts) ·
[ros2 bag](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data.html)
:::

## Intermediate projects

:::{dropdown} Synchronizing multiple sensors with message_filters — Intermediate
:icon: light-bulb

**What it is.** `message_filters.TimeSynchronizer` (or
`ApproximateTimeSynchronizer`) calls your callback only once matching
messages from **several** topics have arrived, close together in time —
instead of you manually buffering and pairing them up.

**Why it matters.** [Module 4's](../04-perception/camera-calibration.md)
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

:::{dropdown} IMU and odometry fusion with robot_localization — Intermediate
:icon: light-bulb

**What it is.** `robot_localization`'s `ekf_node` fuses multiple sources of
motion estimate — wheel odometry and an IMU, typically — into one smoother,
more accurate `odom`→`base_link` transform than either source alone.
[Module 5](../05-mapping-localization.md#core-concepts) covers *why* odometry
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

## Advanced topics

:::{dropdown} Calibrating between sensors — Advanced
:icon: light-bulb

**What it is.** **Extrinsic calibration**: finding the *actual* transform
between two sensors (e.g. camera and LiDAR) precisely enough that data from
both agrees — as opposed to the practical exercise's static transform,
which is only as accurate as your tape-measure estimate.

**Why it matters.** A few centimetres or a couple of degrees of error in a
hand-measured static transform is invisible with one sensor, but shows up
immediately as misaligned data once you fuse two — exactly the kind of
error module 4's camera-LiDAR fusion work depends on being small.

**Needs.** Two sensors viewing an overlapping area, and
[module 4's camera calibration](../04-perception/camera-calibration.md)
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

(pointcloud2-advanced)=
:::{dropdown} PointCloud2 — Advanced
:icon: light-bulb

**What it is.** `sensor_msgs/msg/PointCloud2` represents a 3D point cloud —
the natural output of a depth camera or a 3D LiDAR, and a step up in
complexity from the 2D `LaserScan` this module covers: each point carries
`x, y, z` (and often more fields, like color or intensity), packed in a
binary layout described by the message's own field metadata rather than a
flat array.

**Why it matters.** [ALeRT/Spot's](../../platforms/alert-spot.md) 3D LiDAR
publishes `PointCloud2`, not `LaserScan`; several of
[module 5's](../05-mapping-localization.md#advanced-topics) advanced 3D
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
