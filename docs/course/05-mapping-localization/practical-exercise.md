# Practical exercise

{{ common }} {{ core }}

## Goal

Produce a map of a small area, then localize the robot on it and confirm
the estimated position matches reality.

## Starting point

Your own bringup and SLAM/localization configuration — SLAM Toolbox and
AMCL installed and launchable, with the sensor and TF setup from
[module 3](../03-sensors-tf.md) already working. `robot_bringup` and
`my_robot_slam` below are placeholder package names for whatever your own
workspace or platform track actually calls them (see your [platform
page](../../platforms/index.md)); configuring SLAM Toolbox and AMCL from
scratch is its own task, not part of this module's core — see
[SLAM Toolbox's own getting-started
docs](https://github.com/SteveMacenski/slam_toolbox#getting-started) if
you need to set that configuration up first.

## Steps

1. `ros2 launch robot_bringup robot.launch.yaml`
2. `ros2 launch my_robot_slam slam_toolbox.launch.yaml use_sim_time:=false`
3. In RViz (fixed frame `map`), drive slowly (≤0.5 m/s) in a loop around the
   space, watching the map form — see [Mapping and SLAM: how it
   works](mapping-and-slam.md#how-it-works) for why slow and looped matters.
4. Save it: `ros2 run nav2_map_server map_saver_cli -f ~/course_ws/my_map`
5. Stop SLAM Toolbox. Start localization instead:
   `ros2 launch my_robot_slam localization.launch.yaml`
6. Set the initial pose in RViz with **2D Pose Estimate**, roughly where the
   robot actually is.
7. Drive a short distance and watch the particle cloud tighten around the
   true position — see [Localization and 3D mapping: how it
   works](localization-and-3d-mapping.md#how-it-works) for what AMCL is
   doing while this happens.

## Expected result

After step 7, the live laser scan sits directly on the mapped walls, and
stays there as the robot moves.

## Verification

Watch the scan against the walls, not the numeric pose — if the scan slides
through a wall, localization has not converged, no matter what the pose
readout claims. `ros2 topic echo /amcl_pose --once` should report a small
covariance once converged.

## Common problems

- **The map is doubled or smeared** — driven too fast or hit something.
  There is no fix but starting the map over, slowly.
- **No map appears in RViz** — QoS: `/map` is Transient Local; set the
  display's Durability to match, or to *System Default*.
- **AMCL never publishes `map`→`odom`** — no initial pose was set, or the
  lifecycle manager has not activated the AMCL/map_server nodes
  (`ros2 lifecycle get /amcl`).
- **`use_sim_time` mismatch.** Set on some nodes and not others — check
  every node, not just the one you changed last.
- **SLAM Toolbox and AMCL fighting.** Only one may run at a time; stop SLAM
  Toolbox completely before starting AMCL.

## Optional extensions

{{ optional }}

Pick the robot up (or teleport it in simulation) and put it down somewhere
else. Watch localization fail, then recover it with a fresh 2D Pose
Estimate — this is exactly the kidnapped-robot failure mode covered in
[Continue learning](continue-learning.md), and one you diagnose again in
[module 8](../08-integration.md).

{{ simulation }} Identical procedure, much faster — a whole arena maps in a
few minutes and resets instantly if driven too fast. Set
`use_sim_time:=true` on **every** launch file, or nothing will time out
sensibly; see
[Simulation time](../../platforms/simulation.md#simulation-time).

(try-it-on-spot)=
## Try it on Spot

{{ alert }} {{ spotsim }}

```bash
ros2 launch webots_spot slam_launch.py
```

1. Drive Spot through the arena slowly and deliberately — the same
   "slowly, and close loops" discipline as this module's guided example,
   now on legs instead of wheels, using
   `ros2 run teleop_twist_keyboard teleop_twist_keyboard`.
2. Watch the map form in RViz. Identify at least one gap or smeared area,
   and explain why it happened (moved too fast through that area, or
   never actually looked at it).
3. Save the map: `ros2 run nav2_map_server map_saver_cli -f ~/spot_map`.
4. Stop SLAM, load the saved map for localization instead
   (`ros2 launch webots_spot nav_launch.py` uses a saved map — see the
   [platform page's note on where the map file needs to
   live](../../platforms/alert-spot.md#mapping-and-navigation)), set an
   initial pose, and confirm the particle cloud converges as it did in
   this module's practical task.

:::{danger}
{{ spotsupervised }} On the **physical** Spot, mapping and localization
are supervised-only exercises: an unmapped or partially mapped
environment, on legs, in an area not already cleared and approved by a
trained team member, is a real collision and fall risk that the
simulation's "just restart it" safety net does not have. Do not attempt
this on real hardware without direct supervision — see the [platform
page's operating
sequence](../../platforms/alert-spot.md#operating-the-physical-robot).
:::

**Verification**: same as this module's own — the live scan sits on the
mapped walls once localized, and stays there as Spot moves.

## Next subtopic

[Interesting videos](videos.md) — one carefully checked SLAM Toolbox video.
