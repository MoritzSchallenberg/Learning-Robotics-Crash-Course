# Nav2 architecture and costmaps

{{ common }} {{ core }}

## What this topic is

[Nav2](https://docs.nav2.org/) is a set of servers coordinated by a
behavior tree, not one program: a **Planner Server**, a **Controller
Server**, and a **Behavior Server**, dispatched by the **BT Navigator**. A
**costmap** is a grid where each cell holds the cost of driving there, from
0 to 254 — Nav2 keeps a **global** one and a **local** one.

## Why a robot needs it

A robot with a map and a position ([module 5](../05-mapping-localization.md))
still cannot get anywhere on its own: something has to turn "go to this
point" into an actual path, and actual velocity commands that react to
whatever the map did not know about. Splitting that into cooperating
servers — rather than one monolithic planner — is what lets the slow,
whole-map planning and the fast, reactive obstacle-avoidance run at their
own, very different, rates.

## How it works

```{figure} ../../_static/images/diagrams/07-nav2-architecture-simplified.svg
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
to clear the costmap, back up, wait — the mechanism behind
{ref}`Continue learning: recovery behaviors and behavior trees <recovery-behaviors-and-bt>`.

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
clips corners, too small. One parameter, most doorway problems — see
{ref}`Continue learning's tuning task <tuning-task-costmap-parameter>`
for measuring this yourself.
:::

## Inputs and outputs

Navigation is exposed as a ROS 2 action
([module 2](../02-ros2/services-parameters-actions.md#try-it-yourself-actions)):
`NavigateToPose` takes a goal pose, reports feedback while driving, and
returns a result — the same goal/feedback/result/cancel shape as
turtlesim's `RotateAbsolute`, at a much larger scale.

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

## Try it yourself

Bring up Nav2 and send one goal before attempting the full re-plan task in
[the practical exercise](practical-exercise.md), so you can see each
server's role separately:

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

## How ALeRT applies it

{{ alert }} {{ simulation }} Spot navigates with `ros2 launch webots_spot
nav_launch.py` — the same two-costmap distinction above, on a legged
platform whose local costmap accounts for a wider, less predictable
footprint than a wheeled robot's. See [this module's Try it on
Spot](practical-exercise.md#try-it-on-spot).

## How Carologistics applies it

{{ carologistics }} {{ documented }} Robotino runs
[`robotino_navigation`](../../platforms/carologistics-robotino.md#key-repositories),
Nav2 configuration working with both the simulation and real robots. The
same Planner/Controller/Behavior split applies; the team's
`mps_map_bounded` layer (see [module 5](../05-mapping-localization.md#how-carologistics-uses-this-topic))
adds a competition-area boundary to the global costmap specifically.

## Common problems

- **Nav2 starts but nothing happens on a goal.** Lifecycle nodes not
  activated: `ros2 lifecycle get /planner_server` should say `active`.
- **The path goes through a wall.** The global costmap is not receiving
  the static map (`map_subscribe_transient_local` must be `True`).

## Next subtopic

[Practical exercise](practical-exercise.md) — send the robot to a goal and
watch it re-plan around an obstacle you introduce yourself.

## Sources

- [Nav2 documentation](https://docs.nav2.org/humble/)
- [Nav2 configuration guide](https://docs.nav2.org/humble/configuration_and_development/configuration_guide/)
