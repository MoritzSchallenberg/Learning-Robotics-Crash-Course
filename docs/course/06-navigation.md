# 6. Autonomous Navigation

{{ common }}

The robot has a map and knows where it is. This module has it start driving
itself: you give it a goal, Nav2 works out the path, and it reacts when
something gets in the way.

## Overview

You will learn the Nav2 architecture — the servers that plan, control and
recover — and the difference between the global and local costmap, then
send the robot to a goal and watch it re-plan around an obstacle you
introduce yourself.

## Learning objectives

By the end of this module you can:

1. name the four main Nav2 servers and what each is responsible for;
2. explain the difference between the global and local costmap;
3. send the robot to a goal and observe it re-plan around a new obstacle.

## Prerequisites

[Module 5](05-mapping-localization.md) completed — a saved map and AMCL
localizing on it. Nav2 will not work without a reliable
`map`→`odom`→`base_link` chain.

## Core concepts

### Nav2, minimally

[Nav2](https://docs.nav2.org/) is a set of servers coordinated by a
behavior tree, not one program:

```{figure} ../_static/images/diagrams/07-nav2-architecture-simplified.svg
:alt: A navigation goal enters the BT Navigator, which coordinates a Planner Server reading the Global Costmap, a Controller Server reading the Local Costmap, and a Behavior Server for recovery actions. The Controller Server outputs cmd_vel.
:width: 100%

The BT Navigator dispatches to three servers; the Controller Server is the
only one that outputs `/cmd_vel`.
```

**Planner Server** — given the whole map and a goal, computes a global path.
Thinks slowly, does not know about a chair someone just moved.

**Controller Server** — given that path and live sensor data, computes
actual velocity commands at ~20 Hz. This is what keeps the robot off the
chair.

**Behavior Server** — recovery actions when planning or control fails: spin
to clear the costmap, back up, wait.

### Costmaps: global vs. local

```{list-table}
:header-rows: 1
:widths: 24 38 38

* -
  - Global costmap
  - Local costmap
* - Covers
  - The whole map
  - A small window around the robot
* - Frame
  - `map`
  - `odom`
* - Built from
  - Static map + sensors
  - Live sensor data only
* - Used by
  - The planner
  - The controller
* - Answers
  - "Which route should I take?"
  - "What is in front of me right now?"
```

The local costmap uses `odom` on purpose: `odom` is smooth, so obstacles do
not jump when localization corrects itself.

:::{tip}
If the robot refuses to fit through a doorway it physically fits through,
the **inflation radius** (how far obstacles are padded) is too large. If it
clips corners, too small. One parameter, most doorway problems.
:::

## Guided example

Bring up Nav2 and send one goal before attempting the full re-plan task, so
you can see each server's role separately:

1. Bring up drivers, TF and localization (modules 3–5's launch files), then
   `ros2 launch nav2_bringup navigation_launch.py params_file:=<config path>`.
2. `ros2 lifecycle get /planner_server` and `ros2 lifecycle get
   /controller_server` — both should report `active`. If either does not,
   stop here; nothing past this point will work until it does.
3. Open the Nav2 RViz config: *File → Open Config* →
   `/opt/ros/$ROS_DISTRO/share/nav2_bringup/rviz/nav2_default_view.rviz`,
   click **2D Pose Estimate**, and confirm both costmaps appear as distinct
   layers.
4. Click **Nav2 Goal** nearby, inside open space. Watch the planned path
   line appear (the Planner Server), then the robot move along it (the
   Controller Server).
5. Run `ros2 action list` while the goal is active — `/navigate_to_pose`
   confirms the action interface you are driving.

With that working, the practical task below adds the one thing this
walkthrough does not cover: reacting to something the map did not know
about.

## Practical task

### Goal
Send the robot to a goal in RViz, then place an unmapped obstacle in its
path and watch it re-plan.

### Starting point
A workspace with `my_robot_navigation` already configured with velocity and
inflation parameters matched to your robot — configuring Nav2 from scratch
is not part of this module.

### Steps
1. Bring up drivers, TF, localization and Nav2, exactly as in the guided
   example above.
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

- **Nav2 starts but nothing happens on a goal** — lifecycle nodes not
  activated: `ros2 lifecycle get /planner_server` should say `active`.
- **The robot spins in place and gives up** — the goal is unreachable, or
  fully blocked; recovery behaviours are doing exactly what they should.
- **The path goes through a wall** — the global costmap is not receiving
  the static map (`map_subscribe_transient_local` must be `True`).
- **"Goal rejected" or transform timeouts.** `use_sim_time` inconsistent, or
  the transform chain from module 5 is broken — fix localization first.
- **Nav2 commands are ignored.** Nav2 publishes `/cmd_vel` by default; your
  driver may listen on a different, possibly namespaced, topic.

## Optional extensions

{{ optional }}

Fully surround the robot with obstacles after it starts driving and watch
which recovery behaviours trigger, in what order, from the Nav2 terminal
output — this is a preview of the failure handling
[module 7](07-autonomous-decisions.md) formalises.

{{ simulation }} Identical task. Placing a "new" obstacle is easier in
Webots — drag any object into the scene mid-run. Set velocity and inflation
parameters to the *simulated* robot's actual size and speed, not a guess.

## Advanced topics

{{ advanced }}

:::{dropdown} An action client for NavigateToPose
:icon: light-bulb

Navigation is exposed as an **action**
([module 2](02-ros2.md#advanced-topics)) — it takes time, reports progress,
and can be cancelled:

```python
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient

self.client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
self.client.wait_for_server()

goal = NavigateToPose.Goal()
goal.pose.header.frame_id = 'map'
goal.pose.pose.position.x = 1.5
goal.pose.pose.position.y = 0.5
goal.pose.pose.orientation.w = 1.0

send_future = self.client.send_goal_async(goal)
```

:::{note}
The goal's `frame_id` decides what the coordinates mean: `map` sends an
absolute position; `base_link` sends a position **relative to the robot
right now**. Mixing these up sends the robot somewhere baffling.
:::
:::

:::{dropdown} Autonomous exploration
:icon: light-bulb

Sending one goal is navigation; choosing your own goals is exploration. The
simplest version picks random reachable points and navigates to each in
turn — a starting pattern, not a good one, since it wastes time revisiting
known areas.

**Frontier exploration** is the better approach: find the boundary between
known-free and unknown space, drive to the nearest one, repeat until no
frontiers remain. See
[`nav2_wfd`](https://github.com/SeanReg/nav2_wavefront_frontier_exploration).
This is directly useful for the
[capstone project](hackathon.md)'s optional "explore an unknown area"
extension.
:::

## Try it on Spot

{{ alert }} {{ spotsim }}

```bash
ros2 launch webots_spot nav_launch.py
```

Run this module's practical task against Spot's own navigation launch
file instead of a generic one:

1. Set the initial pose, send a goal, and watch the global (planned) and
   local (reactive) paths separately in RViz — the same two-costmap
   distinction from this module's core concepts, now on a legged
   platform where the local costmap has to account for a wider, less
   predictable footprint than a wheeled robot's.
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
or a fluke; see [this module's own tuning-task
entry](#continue-learning) in Continue learning for the same principle
applied more systematically.

## Continue learning

:::{dropdown} Tuning task: measuring what a costmap parameter actually does — Next step
:icon: light-bulb

**What it is.** A guided before/after measurement, not just reading about
parameters: change one costmap value, re-run the practical task's goal, and
record what actually changed.

**Why it matters.** This module's tip already claims the inflation radius
controls doorway behaviour; this task makes you verify that claim yourself
rather than take it on faith — the same "measure it, do not guess"
standard as this course's power-budgeting exercise in
[module 1](01-system-hardware.md#continue-learning).

**Needs.** This module's practical task, working end to end.

**Try it.** Record the time-to-goal and the path's minimum distance to any
obstacle for your practical task's run. Increase the inflation radius by
50%, re-run the identical goal, and record both numbers again.

**Check.** You have two comparable measurements (before/after) and can
state, in one sentence, what the larger inflation radius actually cost or
gained.

**Read more.** [Nav2: costmap
configuration](https://docs.nav2.org/humble/configuration_and_development/configuration_guide/core_servers/costmap_2d/index.html)
:::

:::{dropdown} Recovery behaviors and behavior trees in Nav2 — Intermediate
:icon: light-bulb

**What it is.** The **Behavior Server** runs recovery actions (spin, back
up, wait) when the planner or controller gets stuck; the **BT Navigator**
coordinates the whole sequence — planning, following, recovering — using a
behavior tree, the same formalism
[module 7](07-autonomous-decisions.md#core-concepts) covers for mission
logic.

**Why it matters.** This module's Common problems already names "the robot
spins in place and gives up" as expected recovery behaviour; understanding
the tree that drives it is what lets you change *when* and *how* it
recovers, instead of just observing that it does.

**Needs.** This module's practical task.

**Try it.** Find your Nav2 configuration's behavior tree XML file (often
`navigate_w_replanning_and_recovery.xml` or similar) and identify, by
reading it, which recovery action runs first when the planner fails.

**Check.** You can name the first recovery action from the XML, and
confirm it matches what you actually observed in the practical task's
Optional extensions (surrounding the robot with obstacles).

**Read more.** [Nav2: behavior
trees](https://docs.nav2.org/humble/configuration_and_development/configuration_guide/core_servers/bt_plugins/)
:::

:::{dropdown} Waypoint missions, keepout and speed zones — Intermediate
:icon: light-bulb

**What it is.** Three related Nav2 capabilities beyond a single goal:
**waypoint following** (a queue of goals visited in order, via
`nav2_waypoint_follower`), **keepout zones** (regions the planner must never
route through, layered onto the costmap), and **speed zones** (regions
where maximum velocity is reduced, independent of the global speed limit).

**Why it matters.** This is the direct bridge to the
[capstone project's](hackathon.md#the-mission) multi-step mission — "reach
a target area", "handle more than one target" — expressed as Nav2
primitives instead of one-off custom code.

**Needs.** This module's practical task.

**Try it.** Configure `nav2_waypoint_follower` with two or three goal poses
in your test area and run it as a single mission instead of individual
**Nav2 Goal** clicks.

**Check.** The robot visits all configured waypoints in order, in one
continuous run, with no manual goal-setting between them.

**Read more.** [Nav2: waypoint
following](https://docs.nav2.org/humble/tutorials/docs/navigation2_with_waypoint_following.html) ·
[Nav2: keepout
zones](https://docs.nav2.org/humble/tutorials/docs/navigation2_with_keepout_filter.html)
:::

:::{dropdown} Docking and navigating through poses — Advanced
:icon: light-bulb

**What it is.** **Navigate Through Poses** drives through a sequence of
intermediate poses on the way to a final goal (unlike waypoint following,
it does not stop and re-plan at each one); **docking**
(`opennav_docking`) is a specialised final-approach behaviour for precisely
reaching a charging station or a work cell.

**Why it matters.** {{ carologistics }} Robotino's precision-docking task
([module 1](01-system-hardware.md#core-concepts)) is exactly this
problem — a generic navigation goal is not precise enough for docking to a
production machine within millimetres.

**Needs.** This module's practical task.

**Try it.** {{ unverified }} — compare `NavigateToPose` and
`NavigateThroughPoses` by sending the same intermediate waypoint as either
a full stop-and-replan goal, or as a pass-through pose, and observe the
difference in the robot's path smoothness.

**Check.** You can describe, from what you observed, the concrete
difference in robot behaviour between the two action types.

**Read more.** [Nav2: Navigate Through
Poses](https://docs.nav2.org/humble/behavior_trees/trees/nav_through_poses_recovery.html) ·
[Nav2: docking](https://docs.nav2.org/humble/configuration_and_development/configuration_guide/others/docking_server.html)
:::

:::{dropdown} Systematic tuning and navigation metrics — Advanced
:icon: light-bulb

**What it is.** Measuring navigation performance with actual numbers
instead of "it seemed fine": **success rate** (goals reached ÷ goals
attempted, over many trials), **time to goal**, and **minimum obstacle
distance** during the run — the same three numbers the
[capstone project's](hackathon.md#self-assessment-checklist) self-assessment
implicitly depends on being good.

**Why it matters.** A single successful demo run proves the system *can*
work; a measured success rate over many runs is what tells you whether it
*reliably* works — the difference matters enormously for the capstone
project.

**Needs.** The tuning-task topic above, run more than once.

**Try it.** Run this module's practical task's goal ten times in a row
(resetting between each), logging success/failure, time-to-goal and
minimum obstacle distance for each attempt.

**Check.** You can report an actual success rate (e.g. "8/10") rather than
a single anecdote, plus the mean time-to-goal across successful runs.

**Read more.** [Nav2:
benchmarking](https://docs.nav2.org/humble/tutorials/docs/navigation2_with_gps.html)
— search the Nav2 docs for the specific benchmarking tooling current at
the time you read this; it has changed across releases.
:::

## Interesting videos

{{ optional }}

::::{grid} 1 1 1 1
:gutter: 2

:::{grid-item-card} Practical Demonstration of New User-Requested Nav2 Features
:link: https://www.youtube.com/watch?v=BmyCi2lcdJY

**Steve Macenski · ROSDevDay 2021 · English · ~50 min**

Covers: live demonstrations of Nav2 features by Nav2's lead maintainer,
including planning, costmaps and recovery behaviour in practice.

*Why watch it*: straight from the source that maintains the tool this
module teaches — a deeper, maintainer's-eye view of the same
Planner/Controller/Behavior Server architecture from this module's core
concepts.

*Compatibility*: conceptual — Nav2 has gained features since 2021; treat
this as orientation on the architecture and reasoning, and check the
[current Nav2 documentation](https://docs.nav2.org/humble/) for anything
version-specific before relying on it.
:::

::::

:::{note}
This is deliberately one carefully checked video rather than a longer,
unverified list. If this link is ever dead or the content has moved, that
is a documentation bug worth reporting — see the [repository
README](https://github.com/MoritzSchallenberg/Learning-Robotics-Crash-Course).
:::

## Connection to the next module

This module sent the robot to *one* goal you chose.
[Module 7](07-autonomous-decisions.md) has it choose its own next step,
including what to do when something fails.

## Further reading

- [Nav2 documentation](https://docs.nav2.org/humble/)
- [Nav2 configuration guide](https://docs.nav2.org/humble/configuration_and_development/configuration_guide/)
- [Nav2 first-time setup](https://docs.nav2.org/humble/configuration_and_development/first_time_robot_setup_guide/)
- [Behavior trees in Nav2](https://docs.nav2.org/humble/configuration_and_development/configuration_guide/core_servers/bt_plugins/)
  — the bridge to [module 7](07-autonomous-decisions.md)
