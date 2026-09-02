# 5. Mapping and Localization

{{ common }}

The robot has sensors, knows where they are mounted, and can detect a
marker. It still has no idea where *it* is. This module gives it a map, and
then a position in that map.

## Overview

You will learn why mapping and localization are different problems needing
different tools, build (or load) an occupancy grid map with SLAM Toolbox,
and check the robot's estimated position against that map in RViz.

## Learning objectives

By the end of this module you can:

1. explain the difference between mapping and localization, and why they
   need different tools;
2. build or load an occupancy grid map with SLAM Toolbox;
3. check the robot's estimated position against the map in RViz.

## Prerequisites

[Module 3](03-sensors-tf.md) completed — a working TF tree and a visible
laser scan are required; you cannot map without both.

## Core concepts

### Odometry, briefly

**Odometry** is the robot's own estimate of how far it has travelled, from
wheel encoders (often fused with an IMU). It is **smooth** — the estimate
never jumps — and it **drifts**: small errors accumulate and are never
corrected on their own.

### Occupancy grids

A 2D map is an **occupancy grid**: the world divided into cells, each `0`
(free), `100` (occupied), or `-1` (unknown). Saved as two files: `map.pgm`
(the image) and `map.yaml` (resolution, origin, thresholds).

### Mapping and localization are different problems

**Mapping**: you do not yet know where you are, and you build the map while
driving — **SLAM** (Simultaneous Localization And Mapping) solves both at
once by recognising previously seen places to correct drift.

**Localization**: a map already exists; you only need to find the robot's
position *in* it — **AMCL**, a particle filter that scores hypotheses
against the laser scan.

```{figure} ../_static/images/diagrams/06-mapping-localization-dataflow.svg
:alt: Two modes sharing laser scan and odometry as inputs. Mapping mode feeds SLAM Toolbox, producing an occupancy grid map and the map to odom transform. Localization mode feeds a saved map plus scan and odometry into AMCL, producing a corrected pose and the same map to odom transform.
:width: 100%

Both modes publish the same `map`→`odom` transform — the correction that
keeps `odom`'s smooth drift from accumulating forever.
```

This is why the `map`/`odom`/`base_link` split from module 3 exists:
`odom`→`base_link` stays smooth and local; `map`→`odom` is the correction,
published by whichever of SLAM Toolbox or AMCL is currently running — never
both at once.

:::{danger}
Only **one** node may publish `map`→`odom` at a time. Running SLAM Toolbox
and AMCL together produces a pose that jumps unpredictably between their two
answers.
:::

## Guided example

Measure odometry drift for yourself before you rely on any map built from
it:

```bash
ros2 run tf2_ros tf2_echo odom base_link
```

Note the printed translation, then drive the robot (or teleoperate it in
simulation) in a square, back to the exact spot it started from, and read
the transform again. The gap between the two readings is the drift — good
over a few metres, unreliable after a few minutes. This is exactly why
mapping needs SLAM's loop-closing correction rather than trusting odometry
alone, and why the practical task below asks you to drive slowly and close
loops.

## Practical task

### Goal
Produce a map of a small area, then localize the robot on it and confirm
the estimated position matches reality.

### Starting point
A `robot_bringup` + `my_robot_slam` workspace with SLAM Toolbox and AMCL
already configured, built following the
[installation guide](../prerequisites/installation.md).

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
- **Map doubled or smeared.** Drove too fast, or collided with something.
- **`use_sim_time` mismatch.** Set on some nodes and not others — check
  every node, not just the one you changed last.
- **SLAM Toolbox and AMCL fighting.** Only one may run at a time; stop SLAM
  Toolbox completely before starting AMCL.

## Optional extensions

{{ optional }}

Pick the robot up (or teleport it in simulation) and put it down somewhere
else. Watch localization fail, then recover it with a fresh 2D Pose
Estimate — this is exactly the failure mode you diagnose in
[module 8](08-integration.md).

{{ simulation }} Identical procedure, much faster — a whole arena maps in a
few minutes and resets instantly if driven too fast. Set
`use_sim_time:=true` on **every** launch file, or nothing will time out
sensibly; see
[Simulation time](../platforms/simulation.md#simulation-time).

## Advanced topics

{{ advanced }}

:::{dropdown} Octomap and GLIM — ALeRT's 3D mapping extensions
:icon: light-bulb

{{ alert }} An occupancy grid is a flat slice — fine for a robot on a
factory floor, useless for one climbing over rubble. ALeRT uses two 3D
approaches for that case; **neither is part of the general course**, and
both are genuinely more advanced than the 2D SLAM covered above.

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

## Continue learning

:::{dropdown} Loop closure — Next step
:icon: light-bulb

**What it is.** SLAM's correction mechanism: recognising that the robot has
returned to a **previously seen place**, and using that match to correct
the accumulated drift in everything mapped since — this is the actual
mechanism behind "why mapping needs SLAM, not just odometry" from this
module's guided example.

**Why it matters.** A map built without ever closing a loop keeps
accumulating drift the whole time; a large mapped area can end up visibly
misaligned with itself (a corridor that should form a rectangle "doesn't
quite close") without one.

**Needs.** This module's practical task.

**Try it.** Map an area that includes a loop (drive around a full
rectangle of furniture or a room's perimeter back to your start point) and
compare the map's visual alignment to the same area mapped as a single
out-and-back path with no loop.

**Check.** You can point to a visible seam or misalignment in the
no-loop-closure map that the loop-closed map does not have.

**Read more.** [SLAM Toolbox: loop
closure](https://github.com/SteveMacenski/slam_toolbox#zzz-loop-closure)
:::

:::{dropdown} Evaluating map quality — Next step
:icon: light-bulb

**What it is.** Looking at a finished occupancy grid critically: are walls
single, crisp lines (good) or doubled/smeared (bad, from driving too fast —
this module's own Common problems section)? Is there unexplained "noise"
occupying open floor?

**Why it matters.** Navigation in [module 6](06-navigation.md) trusts this
map completely; a smeared or noisy map produces a robot that refuses to
plan through a doorway that is actually clear.

**Needs.** This module's practical task.

**Try it.** Open your saved `map.pgm` in an image viewer and identify any
doubled walls or spurious occupied cells, then re-map the same area more
slowly and compare.

**Check.** The slower re-map has visibly cleaner (thinner, more
consistent) walls than the first attempt.

**Read more.** [Module 5's Common
problems](#common-problems) above already names the usual causes.
:::

:::{dropdown} Saving, versioning and updating maps — Next step
:icon: light-bulb

**What it is.** A saved map (`map.pgm` + `map.yaml`) is just two files —
treat them like any other project artefact: committed to git alongside the
package that uses them, and re-saved (a new pair of files, not an
overwrite) whenever the mapped area actually changes.

**Why it matters.** A team running localization against a six-month-old map
of a room that has since been rearranged gets exactly the "scan slides
through what should be a wall" symptom this module's Verification section
warns about — an out-of-date map is a silent failure mode, not a crash.

**Needs.** [Git prerequisite](../prerequisites/git.md) and this module's
practical task.

**Try it.** Commit your saved map files to a git repository, then re-map
the same area with one object moved, save under a new filename, and commit
that as a second version.

**Check.** `git log` shows both map versions, and you can explain from the
commit messages alone which is current.

**Read more.** [Module 8: reproducible
systems](08-integration.md#core-concepts) — the same "one source of truth,
in version control" principle.
:::

:::{dropdown} SLAM Toolbox and AMCL parameters worth tuning — Intermediate
:icon: light-bulb

**What it is.** Both SLAM Toolbox and AMCL ship with many tunable
parameters; a handful matter far more than the rest for typical
first-time problems — SLAM Toolbox's `minimum_travel_distance` and
`minimum_travel_heading` (how far the robot must move before adding a new
scan), and AMCL's `min_particles`/`max_particles` and `update_min_d`
(how many pose hypotheses it tracks, and how far it must move before
re-evaluating them).

**Why it matters.** The default parameters are reasonable starting points,
not guaranteed-correct values for your specific robot and environment;
tuning them is usually faster than debugging a symptom that a parameter
change would have prevented.

**Needs.** This module's practical task, working end to end.

**Try it.** Halve AMCL's `max_particles` from its configured value, re-run
localization, and observe whether convergence becomes noticeably less
stable (watch the particle cloud spread in RViz).

**Check.** You can describe, concretely, what changed in the particle
cloud's behaviour between the two settings.

**Read more.** [Nav2: configuring
AMCL](https://docs.nav2.org/humble/configuration_and_development/configuration_guide/others/configuring_amcl/) ·
[SLAM Toolbox parameters](https://github.com/SteveMacenski/slam_toolbox#configuration)
:::

:::{dropdown} The kidnapped-robot problem and detecting localization loss — Intermediate
:icon: light-bulb

**What it is.** The **kidnapped-robot problem**: a robot's estimated
position is wrong (a bad initial pose, or genuinely picked up and moved
without odometry seeing it) and it must recover without external help —
you already reproduced a version of this in this module's Optional
extensions. Detecting the loss automatically (rather than a human noticing
the scan drifting through a wall) means watching AMCL's reported
**covariance**: a healthy, converged localization has low covariance; a
lost one has high, growing covariance.

**Why it matters.** A mission that keeps navigating confidently on a wrong
pose estimate is worse than one that stops and asks for help — this is
exactly the kind of silent failure the
[capstone project's](hackathon.md#self-assessment-checklist) safety
thinking cares about.

**Needs.** This module's Optional extensions exercise (deliberately losing
localization) completed once already.

**Try it.** Subscribe to `/amcl_pose` and log its covariance values before
and after deliberately "kidnapping" the robot (moving it without driving
it there) as in this module's Optional extensions; write a simple
threshold check that would flag "likely lost".

**Check.** Your threshold correctly flags the post-kidnap covariance as
high, and does not falsely flag the normal, converged covariance from
before.

**Read more.** [AMCL: overview and pose
covariance](https://docs.nav2.org/humble/configuration_and_development/configuration_guide/others/configuring_amcl/)
:::

:::{dropdown} Multi-session mapping — Advanced
:icon: light-bulb

**What it is.** Extending or merging a previously saved map in a **new**
mapping session, rather than always starting from an empty map — SLAM
Toolbox supports loading an existing map as the starting point for further
mapping.

**Why it matters.** Re-mapping an entire building from scratch every time
one room changes does not scale; multi-session mapping lets you update just
the part that changed.

**Needs.** A previously saved map from this module's practical task.

**Try it.** {{ unverified }} — start SLAM Toolbox in its "continue mapping"
mode against your saved map, extend it into an adjacent area you have not
mapped yet, and save the result.

**Check.** The newly saved map contains both the original mapped area and
the newly extended area, correctly aligned with each other.

**Read more.** [SLAM Toolbox: continuing a
map](https://github.com/SteveMacenski/slam_toolbox#continuing-a-map)
:::

## Connection to the next module

This module found the robot's own position. [Module 6](06-navigation.md)
uses that position to decide how to get somewhere else on its own.

## Further reading

- [SLAM Toolbox](https://github.com/SteveMacenski/slam_toolbox) and its
  configuration guide
- [Nav2 AMCL configuration](https://docs.nav2.org/humble/configuration_and_development/configuration_guide/others/configuring_amcl/)
- [REP 105: Coordinate frames](https://www.ros.org/reps/rep-0105.html)
