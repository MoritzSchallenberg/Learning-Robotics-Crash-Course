# 5. Mapping and Localization

:::{admonition} Session 5
:class: note

Monday, 19 October 2026, 17:35 – 19:00 (85 minutes)
:::

{{ common }}

The robot has sensors, knows where they are mounted, and can detect a
marker. It still has no idea where *it* is. Tonight gives it a map, and then
a position in that map.

## Tonight

**Learning objectives** — by 19:00 you can:

1. explain the difference between mapping and localization, and why they
   need different tools;
2. build or load an occupancy grid map with SLAM Toolbox;
3. check the robot's estimated position against the map in RViz.

**Visible result of the evening**: a map exists (built tonight or loaded
from a save), and the robot's laser scan visibly lines up with the walls of
that map in RViz.

**Preparation**: [session 3](03-sensors-tf.md) completed — a working TF tree
and a visible laser scan are required; you cannot map without both.

## Run sheet (85 minutes)

```{list-table}
:header-rows: 1
:widths: 16 20 64
:class: lrcc-runsheet

* - Time
  - Block
  - Content
* - 17:35–17:45
  - Opening
  - Recap TF; today `odom` and `map` both get filled in for real
* - 17:45–18:05
  - Theory {{ core }}
  - Odometry, occupancy grids, mapping vs. localization, SLAM Toolbox
* - 18:05–18:15
  - Demonstration {{ core }}
  - Live: watch a map form while driving, then localize on a saved one
* - 18:15–18:50
  - Practical task {{ core }}
  - Build (or load) a map; check the estimated position
* - 18:50–19:00
  - Wrap-up
  - Compare estimated vs. actual position; preview session 6
```

## Theory

{{ core }}

### Odometry, briefly

**Odometry** is the robot's own estimate of how far it has travelled, from
wheel encoders (often fused with an IMU). It is **smooth** — the estimate
never jumps — and it **drifts**: small errors accumulate and are never
corrected on their own.

```bash
ros2 run tf2_ros tf2_echo odom base_link
```

Drive a square back to the exact start point and read it again — the gap is
the drift. Good over a few metres, unreliable after a few minutes.

### Occupancy grids

A 2D map is an **occupancy grid**: the world divided into cells, each `0`
(free), `100` (occupied), or `-1` (unknown). Saved as two files: `map.pgm`
(the image) and `map.yaml` (resolution, origin, thresholds).

### Mapping and localization are different problems

**Mapping** (this evening, first half): you do not yet know where you are,
and you build the map while driving — **SLAM** (Simultaneous Localization
And Mapping) solves both at once by recognising previously seen places to
correct drift.

**Localization** (this evening, second half): a map already exists; you only
need to find the robot's position *in* it — **AMCL**, a particle filter that
scores hypotheses against the laser scan.

```{figure} ../_static/images/diagrams/06-mapping-localization-dataflow.svg
:alt: Two modes sharing laser scan and odometry as inputs. Mapping mode feeds SLAM Toolbox, producing an occupancy grid map and the map to odom transform. Localization mode feeds a saved map plus scan and odometry into AMCL, producing a corrected pose and the same map to odom transform.
:width: 100%

Both modes publish the same `map`→`odom` transform — the correction that
keeps `odom`'s smooth drift from accumulating forever.
```

This is why the `map`/`odom`/`base_link` split from session 3 exists:
`odom`→`base_link` stays smooth and local; `map`→`odom` is the correction,
published by whichever of SLAM Toolbox or AMCL is currently running — never
both at once.

:::{danger}
Only **one** node may publish `map`→`odom` at a time. Running SLAM Toolbox
and AMCL together produces a pose that jumps unpredictably between their two
answers.
:::

## Practical task

### Goal
Produce a map of a small area, then localize the robot on it and confirm the
estimated position matches reality.

### Starting point
A pre-built `robot_bringup` + `my_robot_slam` workspace with SLAM Toolbox
and AMCL already configured — only the launch commands below are new
tonight.

### Steps
1. `ros2 launch robot_bringup robot.launch.yaml`
2. `ros2 launch my_robot_slam slam_toolbox.launch.yaml use_sim_time:=false`
3. In RViz (fixed frame `map`), drive slowly (≤0.5 m/s) in a loop around the
   space, watching the map form.
4. Save it: `ros2 run nav2_map_server map_saver_cli -f ~/course_ws/my_map`
5. Stop SLAM Toolbox. Start localization instead:
   `ros2 launch my_robot_slam localization.launch.yaml`
6. Set the initial pose in RViz with **2D Pose Estimate**, roughly where the
   robot actually is.
7. Drive a short distance and watch the particle cloud tighten around the
   true position.

### Expected result
After step 7, the live laser scan sits directly on the mapped walls, and
stays there as the robot moves.

### Verification
Watch the scan against the walls, not the numeric pose — if the scan slides
through a wall, localization has not converged, no matter what the pose
readout claims. `ros2 topic echo /amcl_pose --once` should report a small
covariance once converged.

### Common problems
- **The map is doubled or smeared** — driven too fast or hit something.
  There is no fix but starting the map over, slowly.
- **No map appears in RViz** — QoS: `/map` is Transient Local; set the
  display's Durability to match, or to *System Default*.
- **AMCL never publishes `map`→`odom`** — no initial pose was set, or the
  lifecycle manager has not activated the AMCL/map_server nodes
  (`ros2 lifecycle get /amcl`).

### Extension

{{ optional }}

Pick the robot up (or teleport it in simulation) and put it down somewhere
else. Watch localization fail, then recover it with a fresh 2D Pose
Estimate — this is exactly the failure mode you diagnose in
[session 8](08-integration.md).

## Simulation fallback

{{ simulation }}

Identical procedure, much faster — a whole arena maps in a few minutes and
resets instantly if driven too fast. Set `use_sim_time:=true` on **every**
launch file tonight, or nothing will time out sensibly; see
[Simulation time](../platforms/simulation.md#simulation-time).

## Advanced: 3D mapping

{{ advanced }}

:::{dropdown} Octomap and GLIM — ALeRT's 3D mapping extensions
:icon: light-bulb

{{ alert }} An occupancy grid is a flat slice — fine for a robot on a
factory floor, useless for one climbing over rubble. ALeRT uses two 3D
approaches for that case; **neither is part of the general course**, and
both are genuinely more advanced than tonight's 2D SLAM.

**Octomap** — a 3D occupancy map stored as an *octree*: the 3D
generalisation of the occupancy grid, subdividing space only where detail is
needed, so it stays memory-efficient as the volume grows. Where a 2D grid
answers "is this cell free?", an octree answers the same question in three
dimensions without needing a full dense 3D array. ALeRT uses it for 3D path
planning around obstacles a 2D map cannot represent — a table top and the
floor beneath it, for instance, look identical to a single-height 2D LiDAR
slice but are entirely different in an octree.

```bash
sudo apt install ros-humble-octomap*
```

The team maintains a fork at
[RRL-ALeRT/octomap_mapping](https://github.com/RRL-ALeRT/octomap_mapping);
use the launch file from that repository.

**GLIM** — a LiDAR–inertial SLAM system that tightly fuses a 3D LiDAR with
IMU data to build accurate 3D point-cloud maps, rather than the 2D
scan-matching SLAM Toolbox performs. It is the right tool where 2D scan
matching fails entirely: uneven ground, stairs, rubble — situations where
"the floor" is not a single plane. Installation:
[koide3.github.io/glim](https://koide3.github.io/glim/installation.html).

{{ unverified }} Beyond the install commands above, this course has not
independently verified a working configuration for either tool — the
source material references them by repository link, without a tested
parameter set. If you use them, expect to read the linked repository's own
documentation rather than following a recipe here, and treat any specific
command you find elsewhere as needing a check against the current
repository state.
:::

## Common mistakes

**Map doubled or smeared.** Drove too fast, or collided with something.

**`use_sim_time` mismatch.** Set on some nodes and not others — check every
node, not just the one you changed last.

**SLAM Toolbox and AMCL fighting.** Only one may run at a time; stop SLAM
Toolbox completely before starting AMCL.

## Transition to session 6

Tonight the robot knows where it is. Next week it decides how to get
somewhere else on its own —
[Autonomous Navigation](06-navigation.md).

## Further reading

- [SLAM Toolbox](https://github.com/SteveMacenski/slam_toolbox) and its
  configuration guide
- [Nav2 AMCL configuration](https://docs.nav2.org/jazzy/configuration_and_development/configuration_guide/others/configuring_amcl/)
- [REP 105: Coordinate frames](https://www.ros.org/reps/rep-0105.html)
