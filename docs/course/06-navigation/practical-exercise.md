# Practical exercise

{{ common }} {{ core }}

## Goal

Send the robot to a goal in RViz, then place an unmapped obstacle in its
path and watch it re-plan.

## Starting point

A workspace with `my_robot_navigation` already configured with velocity and
inflation parameters matched to your robot — configuring Nav2 from scratch
is not part of this module.

## Steps

1. Bring up drivers, TF, localization and Nav2, exactly as in
   [Nav2 architecture and costmaps: Try it
   yourself](nav2-architecture-and-costmaps.md#try-it-yourself).
2. Click **2D Pose Estimate**, confirm the costmaps appear.
3. Click **Nav2 Goal** and set a point several metres away.
4. While the robot is driving, place an obstacle across its planned path
   that was not there when the map was built.
5. Watch the planned path change in RViz, and time how long the re-plan
   takes.

## Expected result

The robot drives to the goal and stops within tolerance. When you introduce
the obstacle, the path visibly reroutes around it within a second or two.

## Verification

```bash
ros2 action list
```

Shows `/navigate_to_pose` while the goal is active. The path line in RViz
changes shape at the moment the obstacle appears — that visible change is
the verification, not just "the robot arrived."

## Common problems

- **The robot spins in place and gives up.** The goal is unreachable, or
  fully blocked; recovery behaviours are doing exactly what they should.
- **"Goal rejected" or transform timeouts.** `use_sim_time` inconsistent, or
  the transform chain from [module 5](../05-mapping-localization.md) is
  broken — fix localization first.
- **Nav2 commands are ignored.** Nav2 publishes `/cmd_vel` by default; your
  driver may listen on a different, possibly namespaced, topic.

## Optional extensions

{{ optional }}

Fully surround the robot with obstacles after it starts driving and watch
which recovery behaviours trigger, in what order, from the Nav2 terminal
output — this is a preview of the failure handling
[module 7](../07-autonomous-decisions.md) formalises.

{{ simulation }} Identical task. Placing a "new" obstacle is easier in
Webots — drag any object into the scene mid-run. Set velocity and inflation
parameters to the *simulated* robot's actual size and speed, not a guess.

## Try it on Spot

{{ alert }} {{ spotsim }}

```bash
ros2 launch webots_spot nav_launch.py
```

Run this module's practical task against Spot's own navigation launch
file instead of a generic one:

1. Set the initial pose, send a goal, and watch the global (planned) and
   local (reactive) paths separately in RViz — the same two-costmap
   distinction from [Nav2 architecture and
   costmaps](nav2-architecture-and-costmaps.md#how-it-works), now on a
   legged platform where the local costmap has to account for a wider,
   less predictable footprint than a wheeled robot's.
2. Introduce a new obstacle not on the map and watch the recovery
   behaviour trigger.
3. Run the goal a second time and compare: did the same recovery
   behaviour trigger, or a different one?

Record, across both attempts:

```{list-table}
:header-rows: 1
:widths: 40 30 30

* - Measurement
  - Attempt 1
  - Attempt 2
* - Goal reached?
  -
  -
* - Time to goal
  -
  -
* - Recovery behaviours triggered
  -
  -
* - Minimum obstacle distance (if measurable)
  -
  -
```

**Verification**: you have two filled rows, not one — a single successful
run does not tell you whether the recovery behaviour you saw was typical
or a fluke; see
{ref}`Continue learning: systematic tuning and navigation metrics <systematic-tuning-and-navigation-metrics>`
for the same principle applied more systematically.

## Next subtopic

[Interesting videos](videos.md) — a maintainer's-eye demonstration of Nav2
features.

## Sources

- [Nav2 first-time setup](https://docs.nav2.org/humble/configuration_and_development/first_time_robot_setup_guide/)
