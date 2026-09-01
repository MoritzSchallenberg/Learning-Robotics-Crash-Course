# 6. Autonomous Navigation

:::{admonition} Session 6
:class: note

Wednesday, 21 October 2026, 17:35 – 19:00 (85 minutes)
:::

{{ common }}

The robot has a map and knows where it is. Tonight it starts driving itself:
you give it a goal, Nav2 works out the path, and it reacts when something
gets in the way.

## Tonight

**Learning objectives** — by 19:00 you can:

1. name the four main Nav2 servers and what each is responsible for;
2. explain the difference between the global and local costmap;
3. send the robot to a goal and observe it re-plan around a new obstacle.

**Visible result of the evening**: the robot drives autonomously to a point
you click in RViz, and visibly re-routes when you place an obstacle it did
not know about.

**Preparation**: [session 5](05-mapping-localization.md) completed — a saved
map and AMCL localizing on it. Nav2 will not work without a reliable
`map`→`odom`→`base_link` chain.

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
  - Recap localization; today the robot acts on where it is, not just
    knows it
* - 17:45–18:05
  - Theory {{ core }}
  - Nav2 architecture, costmaps, planner vs. controller
* - 18:05–18:15
  - Demonstration {{ core }}
  - Live: send a goal, then block the path mid-drive
* - 18:15–18:50
  - Practical task {{ core }}
  - Navigate to a goal; force a re-plan
* - 18:50–19:00
  - Wrap-up
  - Confirm re-planning worked for everyone; preview session 7
```

## Theory

{{ core }}

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

## Practical task

### Goal
Send the robot to a goal in RViz, then place an unmapped obstacle in its
path and watch it re-plan.

### Starting point
A pre-built workspace with `my_robot_navigation` already configured with
velocity and inflation parameters matched to your robot — configuring Nav2
from scratch is not part of tonight.

### Steps
1. Bring up drivers, TF and localization (sessions 3–5's launch files).
2. `ros2 launch nav2_bringup navigation_launch.py params_file:=<config path>`
3. Open the Nav2 RViz config: *File → Open Config* →
   `/opt/ros/$ROS_DISTRO/share/nav2_bringup/rviz/nav2_default_view.rviz`
4. Click **2D Pose Estimate**, confirm the costmaps appear.
5. Click **Nav2 Goal** and set a point several metres away.
6. While the robot is driving, place an obstacle across its planned path
   that was not there when the map was built.
7. Watch the planned path change in RViz, and time how long the re-plan
   takes.

### Expected result
The robot drives to the goal and stops within tolerance in step 5. In step
7, the path visibly reroutes around the new obstacle within a second or two.

### Verification
```bash
ros2 action list
```
Shows `/navigate_to_pose` while the goal is active. The path line in RViz
changes shape at the moment the obstacle appears — that visible change is
the verification, not just "the robot arrived."

### Common problems
- **Nav2 starts but nothing happens on a goal** — lifecycle nodes not
  activated: `ros2 lifecycle get /planner_server` should say `active`.
- **The robot spins in place and gives up** — the goal is unreachable, or
  fully blocked; recovery behaviours are doing exactly what they should.
- **The path goes through a wall** — the global costmap is not receiving
  the static map (`map_subscribe_transient_local` must be `True`).

### Extension

{{ optional }}

Fully surround the robot with obstacles after it starts driving and watch
which recovery behaviours trigger, in what order, from the Nav2 terminal
output — this is a preview of the failure handling
[session 7](07-autonomous-decisions.md) formalises.

## Simulation fallback

{{ simulation }}

Identical task. Placing a "new" obstacle is easier in Webots — drag any
object into the scene mid-run. Set velocity and inflation parameters to the
*simulated* robot's actual size and speed, not a guess.

## Advanced: sending goals from code and exploring

{{ advanced }}

:::{dropdown} An action client for NavigateToPose
:icon: light-bulb

Navigation is exposed as an **action**
([session 2](02-ros2.md#advanced-launch-files-services-and-actions)) — it
takes time, reports progress, and can be cancelled:

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
[hackathon](hackathon.md)'s optional "explore an unknown area" extension.
:::

## Common mistakes

**"Goal rejected" or transform timeouts.** `use_sim_time` inconsistent, or
the transform chain from session 5 is broken — fix localization first.

**Nav2 commands are ignored.** Nav2 publishes `/cmd_vel` by default; your
driver may listen on a different, possibly namespaced, topic.

## Transition to session 7

Tonight the robot went to *one* goal you chose. Next week it chooses its own
next step, including what to do when something fails —
[Autonomous Decisions and Manipulation](07-autonomous-decisions.md).

## Further reading

- [Nav2 documentation](https://docs.nav2.org/jazzy/)
- [Nav2 configuration guide](https://docs.nav2.org/jazzy/configuration_and_development/configuration_guide/)
- [Nav2 first-time setup](https://docs.nav2.org/jazzy/configuration_and_development/first_time_robot_setup_guide/)
- [Behavior trees in Nav2](https://docs.nav2.org/jazzy/configuration_and_development/configuration_guide/core_servers/bt_plugins/)
  — the bridge to [session 7](07-autonomous-decisions.md)
