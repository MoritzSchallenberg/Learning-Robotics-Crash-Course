# 5. Mapping and Localization

:::{admonition} Session 5
:class: note

Monday, 19 October 2026, 17:35 – 19:00
:::

{{ common }}

The robot has sensors and knows where they are mounted. It still has no idea
where *it* is. This session gives it a map, and then a position in that map —
the two things navigation cannot work without.

## Learning objectives

After this session you can:

- explain what odometry provides and how it fails;
- read an occupancy grid and its metadata;
- build a map with SLAM Toolbox and save it;
- localize on a saved map with AMCL;
- diagnose the difference between an odometry problem and a localization
  problem;
- say what Octomap and GLIM add for 3D environments.

## Prerequisites

[Session 3](03-sensors-tf.md): a working TF tree and a visible laser scan. You
cannot map without both.

## Odometry

**Odometry** is the robot's own estimate of how far it has travelled, computed
from wheel encoders — often fused with an IMU. It provides the `odom` →
`base_link` transform.

Its two defining properties:

**It is smooth.** The estimate never jumps. Between two moments, the change is
always small and continuous, which is exactly what a local controller needs.

**It drifts.** Every small error accumulates and is never corrected. Wheels
slip, tyres deform, the floor is uneven. After a few metres it is very good;
after a few minutes of driving it can be metres and tens of degrees wrong.

```bash
ros2 topic echo /odom --once
ros2 run tf2_ros tf2_echo odom base_link
```

:::{tip}
Try this: note the odometry, drive the robot in a square back to its exact
starting point, and read the odometry again. The gap is the drift. On a real
robot it is sobering.
:::

Odometry alone is enough to drive around a corner and hopeless for finding your
way back across a building. Fixing that is what the rest of this session is
about.

## Occupancy grids

A 2D map in ROS 2 is an **occupancy grid**: the world divided into square
cells, each holding one number.

```{list-table}
:header-rows: 1
:widths: 25 75

* - Value
  - Meaning
* - `0`
  - Free — the robot may drive here
* - `100`
  - Occupied — there is an obstacle
* - `-1`
  - Unknown — never observed
```

The **resolution** is the size of one cell, typically 0.05 m. Finer means more
detail and much more memory and computation; the area grows with the square of
the resolution.

The message is `nav_msgs/msg/OccupancyGrid`, and a saved map is two files:

`map.pgm`
: a greyscale image — white free, black occupied, grey unknown

`map.yaml`
: the metadata — resolution, the world coordinates of the image origin, and the
  thresholds that decide what counts as occupied

:::{note}
The `image:` entry in the `.yaml` should be just the filename, not a path, and
both files must sit in the same directory. This trips people up when they
reorganise their map folder.
:::

## SLAM: building the map

**SLAM** — Simultaneous Localization And Mapping — is the chicken-and-egg
problem of robotics: to build a map you need to know where you are, and to know
where you are you need a map. SLAM solves both at once, by recognising when the
robot returns to a place it has seen before and correcting the accumulated
drift.

The tool this course uses is
[SLAM Toolbox](https://github.com/SteveMacenski/slam_toolbox), which is the
standard 2D SLAM package in ROS 2. It can map, refine an existing map, continue
mapping into a saved one, and run as a pure localizer.

### Install

```bash
sudo apt install ros-$ROS_DISTRO-slam-toolbox
```

### Configure

Create a package `my_robot_slam` and a launch file `slam_toolbox.launch.yaml`:

```yaml
launch:

- node:
    pkg: "slam_toolbox"
    exec: "async_slam_toolbox_node"
    name: "slam_toolbox"
    param:
    # frames and topics
    -
      name: "odom_frame"
      value: "odom"
    -
      name: "map_frame"
      value: "map"
    -
      name: "base_frame"
      value: "base_link"
    -
      name: "scan_topic"
      value: "/scan"
    # algorithm
    -
      name: "mode"
      value: "mapping"          # or "localization"
    -
      name: "enable_interactive_mode"
      value: True
```

Check the frame and topic names against your own system — `base_footprint`
instead of `base_link` and a namespaced scan topic are both common.

### Build a map

```bash
# 1. Bring up the robot
ros2 launch robot_bringup robot.launch.yaml

# 2. Start teleoperation in another terminal
ros2 run teleop_twist_keyboard teleop_twist_keyboard

# 3. Start SLAM
ros2 launch my_robot_slam slam_toolbox.launch.yaml use_sim_time:=false

# 4. Visualize
rviz2
```

In RViz, add a `Map` display on `/map`, and set the fixed frame to `map`.

:::{warning}
`use_sim_time` must be `true` when running against a simulator and `false` on a
real robot — and it must be consistent across **every** node in the system.
A mismatch produces transform timing errors and a map that never updates, with
error messages that point everywhere except the real cause.
:::

### Driving a good map

Mapping is a skill, and a failed map usually cannot be salvaged — you start
over. The conventions that make it work:

**Drive slowly.** Around 0.5 m/s, and slower around corners. Speed is the most
common cause of a broken map.

**Do not hit anything.** A collision moves the robot in a way odometry cannot
see, and the map tears.

**Avoid reversing.** Driving backwards degrades odometry on many platforms and
the map stops fitting together.

**Close loops.** Drive in circuits and return to places you have already
mapped. This is how SLAM corrects drift — a map built by driving one long
corridor and stopping has nothing to correct against.

**Watch as you go.** Keep RViz open. If the map starts to smear or double, stop
and go back over the area you just covered rather than pressing on.

:::{tip}
Set the RViz fixed frame to `base_link` while driving and the camera follows
the robot, which makes it much easier to see the map forming.
:::

### Save the map

```bash
mkdir -p ~/robot_ws/src/my_robot_slam/maps
cd ~/robot_ws/src/my_robot_slam/maps
ros2 run nav2_map_server map_saver_cli -f my_map
```

This writes `my_map.pgm` and `my_map.yaml` into the current directory.

Alternatively, use the **SlamToolboxPlugin** panel in RViz
(*Panels → Add New Panel*): **Save Map** writes the image pair, while
**Serialize Map** saves the internal pose graph, which is what you need if you
want to continue mapping later.

:::{note}
Both methods save relative to the working directory of the process, not to
where you think. If a save times out, simply run it again.
:::

### Tuning

If the map quality is poor, these parameters are the ones worth adjusting
first:

```yaml
- name: "link_scan_maximum_distance"
  value: 3.0
- name: "correlation_search_space_dimension"
  value: 1.0
- name: "correlation_search_space_resolution"
  value: 0.02
- name: "correlation_search_space_smear_deviation"
  value: 0.2
- name: "distance_variance_penalty"
  value: 0.5
- name: "angle_variance_penalty"
  value: 1.0
- name: "loop_match_maximum_variance_coarse"
  value: 6.0
```

Change one at a time and re-map, otherwise you learn nothing. The
[SLAM Toolbox configuration guide](https://github.com/SteveMacenski/slam_toolbox#configuration)
documents all of them.

## Localization on a saved map

Once you have a map, you no longer need SLAM. You need to know where the robot
is *in that map* — the `map` → `odom` transform.

The standard answer is **AMCL** (Adaptive Monte Carlo Localization). It
maintains a cloud of *particles*, each a hypothesis about where the robot might
be. Each particle is moved according to odometry, then scored by how well the
laser scan would match the map from that position. Particles that match well
survive and multiply; particles that do not die off. The cloud converges on the
truth.

This design explains its behaviour:

- it needs an **initial estimate**, because it cannot search the whole map;
- it converges as the robot **drives**, because motion is what separates good
  hypotheses from bad ones;
- it corrects odometry drift without ever making motion discontinuous, because
  the correction lands in `map` → `odom`, not in `odom` → `base_link`.

### Install

```bash
sudo apt install ros-$ROS_DISTRO-nav2-amcl ros-$ROS_DISTRO-nav2-map-server \
                 ros-$ROS_DISTRO-nav2-lifecycle-manager
```

### Launch

```yaml
launch:

- node:
    pkg: "nav2_map_server"
    exec: "map_server"
    name: "map_server"
    param:
    -
      name: "yaml_filename"
      value: ""              # absolute path to your map .yaml
    -
      name: "use_sim_time"
      value: False

- node:
    pkg: "nav2_amcl"
    exec: "amcl"
    name: "amcl"
    param:
    -
      name: "base_frame_id"
      value: "base_link"
    -
      name: "odom_frame_id"
      value: "odom"
    -
      name: "global_frame_id"
      value: "map"
    -
      name: "scan_topic"
      value: "/scan"
    -
      name: "laser_max_range"
      value: 10.0
    -
      name: "tf_broadcast"
      value: True
    -
      name: "use_sim_time"
      value: False

- node:
    pkg: "nav2_lifecycle_manager"
    exec: "lifecycle_manager"
    name: "lifecycle_manager"
    param:
    -
      name: "node_names"
      value: ["map_server", "amcl"]
    -
      name: "autostart"
      value: True
```

:::{note}
Nav2 nodes are **lifecycle nodes**: they start in an unconfigured state and do
nothing until something activates them. That something is the
`lifecycle_manager`. If your map never appears and AMCL never publishes, check
that the manager is running and lists every node in `node_names` — this is the
single most common Nav2 startup problem.
:::

### The key AMCL parameters

```{list-table}
:header-rows: 1
:widths: 30 70

* - Parameter
  - Meaning
* - `odom_frame_id`
  - The frame odometry publishes into
* - `base_frame_id`
  - The robot's base frame
* - `global_frame_id`
  - The fixed world frame, normally `map`
* - `tf_broadcast`
  - Whether AMCL publishes `map` → `odom`. Almost always `true`
* - `laser_max_range`
  - Readings beyond this are ignored
* - `set_initial_pose`
  - Start from a configured pose rather than waiting for RViz
```

### Localizing

1. Bring up the robot, then start the localization launch file.
2. In RViz, add a `Map` display (Durability: **Transient Local**) and set the
   fixed frame to `map`.
3. Add displays for `/scan`, `/amcl_pose` and `/particle_cloud`.
4. Click **2D Pose Estimate**, then click and drag on the map where the robot
   actually is, in the direction it faces.
5. Drive around and watch the particle cloud contract.

:::{tip}
Judge localization by looking at the **laser scan against the map walls**. If
the scan lines up with the walls as the robot drives, localization is working.
If the scan slides through the walls, it is not — no matter what the pose
estimate claims.
:::

## Odometry error versus localization error

This is the diagnostic skill worth taking away from this session.

```{list-table}
:header-rows: 1
:widths: 30 35 35

* - Symptom
  - Likely cause
  - What to do
* - Scan matches walls, pose drifts slowly, jumps back periodically
  - Normal — odometry drifting, AMCL correcting
  - Nothing
* - Scan slides through walls, never recovers
  - Localization lost
  - Re-set the initial pose; check the scan topic and frames
* - Scan is rotated relative to the map
  - Bad initial orientation, or a wrong sensor transform
  - Re-set the pose; verify with `tf2_echo`
* - Particle cloud stays wide after driving
  - Not enough distinctive features, or the scan does not match the map
  - Drive somewhere with more structure; check the map is current
* - Pose jumps violently and constantly
  - `map` → `odom` published by two nodes
  - Make sure SLAM Toolbox is not still running alongside AMCL
* - Map does not update at all
  - `use_sim_time` mismatch, or lifecycle nodes not activated
  - Check both across all nodes
```

## 3D mapping

An occupancy grid is a flat slice, which is fine for a robot on a factory floor
and useless for one climbing over rubble. Two 3D approaches the institute uses:

**Octomap** {{ alert }}
: A 3D occupancy map stored as an octree — the 3D generalisation of the
  occupancy grid, subdividing space only where detail is needed, so it stays
  memory-efficient. Used by ALeRT for 3D path planning around obstacles that a
  2D map cannot represent.

**GLIM** {{ alert }}
: A LiDAR–inertial SLAM system that builds accurate 3D point cloud maps by
  tightly fusing 3D LiDAR with IMU data. Appropriate where a 2D scan matcher
  fails entirely — uneven ground, stairs, collapsed structures.

Both are covered on the [ALeRT/Spot page](../platforms/alert-spot.md).

:::{admonition} TODO-REVIEW
:class: todo-review

The source material references Octomap and GLIM by repository link only, with
no configuration or parameters. A domain-specific review is required before
turning these into step-by-step instructions for the course. Treat this section
as an overview, not a guide.
:::

## Sensor fusion in one paragraph

Every sensor is wrong in a different way. Odometry is smooth but drifts. A
LiDAR match against a map is globally correct but jumps. An IMU is excellent
over milliseconds and useless over minutes. **Sensor fusion** combines them so
that each covers the others' weaknesses — typically with a Kalman filter or a
particle filter.

You have already seen this: AMCL fuses odometry with laser-against-map matching
and the `map`/`odom`/`base_link` frame split *is* the architecture of that
fusion. The `robot_localization` package generalises it to arbitrary sensor
sets.

## Task

:::{admonition} Task: map it, then find yourself in it
:class: task

**Part 1 — Measure odometry drift.**

1. Note `ros2 run tf2_ros tf2_echo odom base_link`.
2. Drive the robot in a closed loop back to exactly the same physical spot.
3. Read the transform again. How far off is it, in metres and degrees?
4. Repeat with faster driving and sharper turns. Does the error grow?

**Part 2 — Build a map.**

1. Start SLAM Toolbox and map a room or a section of the arena.
2. Follow the driving conventions above.
3. Save the map into your package's `maps/` directory.
4. Open the `.pgm` in an image viewer and the `.yaml` in an editor. What is the
   resolution? What does `origin` mean?

**Part 3 — Localize.**

1. Stop SLAM Toolbox completely.
2. Start `map_server` and `amcl` with your saved map.
3. Set the initial pose in RViz and drive around until the particle cloud
   converges.
4. Now deliberately break it: pick the robot up and put it down somewhere else
   (or teleport it in simulation). What happens to the scan-versus-map
   alignment? How do you recover?

**Part 4 — Diagnose.**

Using the table above, write one sentence for each: how would you tell an
odometry problem from a localization problem, from the outside?
:::

:::{admonition} Expected result
:class: result

Part 1: a measurable drift, larger when you drive aggressively. On a real robot
expect centimetres over a small loop; on a bad surface, much more.

Part 2: a map in which walls are single clean lines, not doubled or smeared.

Part 3: after setting the initial pose and driving a few metres, the particle
cloud is a tight blob and the laser scan sits on the mapped walls. After the
robot is moved, the scan no longer matches, and re-setting the pose estimate
recovers it.
:::

## Common mistakes

**The map is doubled or smeared.**
Driven too fast, or a collision. Start over and drive slowly.

**No map appears in RViz.**
QoS. The map is published **Transient Local** and RViz defaults to Volatile.
See [session 3](03-sensors-tf.md#when-rviz-shows-nothing).

**The map appears once and never updates.**
`use_sim_time` mismatch. Check it on every node.

**AMCL never publishes `map` → `odom`.**
Either no initial pose was set, or the lifecycle manager is not activating the
nodes.

**Localization is wildly unstable.**
SLAM Toolbox is still running and also publishing `map` → `odom`. Only one node
may own that transform.

**The saved map will not load.**
The `image:` field in the `.yaml` contains a path instead of a bare filename,
or the two files were separated.

## Further reading

- [SLAM Toolbox](https://github.com/SteveMacenski/slam_toolbox) and its
  configuration guide
- [Nav2 AMCL configuration](https://docs.nav2.org/configuration/packages/configuring-amcl.html)
- [Nav2 map server](https://docs.nav2.org/configuration/packages/configuring-map-server.html)
- [REP 105: Coordinate frames](https://www.ros.org/reps/rep-0105.html) — the
  authority on the `map`/`odom` split
- [robot_localization](https://docs.ros.org/en/melodic/api/robot_localization/html/index.html)
  — general-purpose sensor fusion
