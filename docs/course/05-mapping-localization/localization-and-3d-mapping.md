# Localization and 3D mapping

{{ common }} {{ core }}

## What this topic is

**Localization**: a map already exists; the task is only to find the
robot's position *in* it. **AMCL** (Adaptive Monte Carlo Localization) is
the standard ROS 2 tool: a particle filter that scores many pose
hypotheses against the live laser scan and keeps the ones that agree with
it.

## Why a robot needs it

Mapping happens once; localizing happens every time the robot starts a new
session on a map that already exists. A robot that cannot localize cannot
trust anything about "where am I", which makes every later navigation goal
meaningless.

## How it works

AMCL scatters a cloud of pose hypotheses (particles) around a starting
estimate, scores each against the incoming laser scan, and repeatedly
resamples toward the hypotheses that agree best with what the sensor
actually sees. As the robot moves, the cloud tightens around the true pose.

Like SLAM Toolbox on [this module's previous
subtopic](mapping-and-slam.md), AMCL publishes the `map`→`odom` correction
— never both at once (see [this module's
overview](../05-mapping-localization.md#how-the-complete-system-fits-together)).

If the estimate is ever badly wrong — a bad initial pose, or the robot
genuinely moved without odometry seeing it — this is the classic
**kidnapped-robot problem**. AMCL alone does not detect this automatically;
[Continue learning](continue-learning.md) covers watching the reported
covariance to flag it programmatically.

## Inputs and outputs

AMCL subscribes to a saved map, `/scan`, and odometry, and publishes
`/amcl_pose` (with a covariance) plus the `map`→`odom` transform. Set the
initial pose once, at start-up, with RViz's **2D Pose Estimate** tool.

## Try it yourself

```bash
ros2 topic echo /amcl_pose --once
```

**Expected result**: a pose with a small covariance once localization has
converged — watch the scan against the mapped walls in RViz as the real
check, not the numeric pose alone: if the scan slides through a wall,
localization has not converged no matter what the pose readout claims. The
full walkthrough, including starting localization and setting the initial
pose, is this module's [practical exercise](practical-exercise.md).

## How ALeRT applies it

{{ alert }} {{ simulation }} Spot localizes with `ros2 launch webots_spot
nav_launch.py` against a previously saved map — see the [platform page's
note on where the map file needs to
live](../../platforms/alert-spot.md#mapping-and-navigation).

## How Carologistics applies it

{{ carologistics }} {{ documented }} Robotino sets **2D Pose Estimate**
and checks scan-to-wall alignment exactly as described above, per robot,
under a namespace — see the [platform page's localizing-a-robot
steps](../../platforms/carologistics-robotino.md#localizing-a-robot).

## Common problems

- **AMCL never publishes `map`→`odom`.** No initial pose was set, or the
  lifecycle manager has not activated the AMCL/map_server nodes
  (`ros2 lifecycle get /amcl`).
- **`use_sim_time` mismatch.** Set on some nodes and not others — check
  every node, not just the one you changed last.
- **SLAM Toolbox and AMCL fighting.** Only one may run at a time; stop SLAM
  Toolbox completely before starting AMCL.

## Mapping rough 3D terrain

{{ advanced }}

:::{dropdown} Octomap and GLIM
:icon: light-bulb

{{ alert }} An occupancy grid is a flat slice — fine for a robot on a
factory floor, useless for one climbing over rubble. ALeRT uses two 3D
approaches for that case; **neither is part of the general course**, and
both are genuinely more advanced than the 2D SLAM and localization covered
above.

**Octomap** — a 3D occupancy map stored as an *octree*: the 3D
generalisation of the occupancy grid, subdividing space only where detail
is needed, so it stays memory-efficient as the volume grows. Where a 2D
grid answers "is this cell free?", an octree answers the same question in
three dimensions without needing a full dense 3D array. ALeRT uses it for
3D path planning around obstacles a 2D map cannot represent — a table top
and the floor beneath it, for instance, look identical to a single-height
2D LiDAR slice but are entirely different in an octree.

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

## Next subtopic

[Practical exercise](practical-exercise.md) — map an area, then localize
on it end to end.
