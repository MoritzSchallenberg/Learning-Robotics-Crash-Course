# 6. Autonomous Navigation

:::{admonition} Session 6
:class: note

Wednesday, 21 October 2026, 17:35 – 19:00
:::

{{ common }}

The robot has a map and knows where it is. Tonight it starts driving itself:
you give it a goal, and Nav2 works out the path, follows it, and deals with
whatever gets in the way.

## Learning objectives

After this session you can:

- describe the Nav2 architecture and name what each server does;
- explain the difference between the global and local costmap;
- configure and launch Nav2 on your robot;
- send goals from RViz and from code;
- observe re-planning when an obstacle appears;
- send goals programmatically with an action client.

## Prerequisites

[Session 5](05-mapping-localization.md): a saved map, and AMCL localizing on
it. Nav2 will not work without a reliable `map` → `odom` → `base_link` chain.

## The Nav2 architecture

[Nav2](https://docs.nav2.org/) is not one program. It is a set of servers, each
owning one part of the problem, coordinated by a behavior tree.

```text
                    ┌──────────────────────┐
   goal ──────────► │    BT Navigator      │  decides what to do, and when
                    └──────────┬───────────┘
                               │
        ┌──────────────┬───────┴───────┬──────────────┐
        ▼              ▼               ▼              ▼
   ┌─────────┐   ┌───────────┐   ┌──────────┐   ┌──────────┐
   │ Planner │   │Controller │   │ Behavior │   │ Smoother │
   │ global  │   │  local    │   │ recovery │   │  path    │
   └────┬────┘   └─────┬─────┘   └────┬─────┘   └──────────┘
        │              │              │
        ▼              ▼              │
   ┌─────────┐   ┌───────────┐        │
   │ global  │   │   local   │ ◄──────┘
   │ costmap │   │  costmap  │
   └─────────┘   └───────────┘
        ▲              ▲
        │              │
      map          live sensors
```

**Planner server** — given the whole map and a goal, computes a path from here
to there. It thinks globally and slowly, and it does not know about the chair
someone just moved.

**Controller server** — given that path and live sensor data, computes the
actual velocity commands. It thinks locally and fast, at 20 Hz or so, and it is
what keeps the robot off the chair.

**Behavior server** — the recovery behaviours. When planning or control fails,
these try to unstick the robot: spin in place to clear the costmap, back up,
wait for a moving obstacle to pass.

**Smoother server** — refines a path, removing the jitter that grid-based
planners produce.

**BT Navigator** — a behavior tree that sequences all of the above: plan,
follow, and on failure try recovery, then re-plan. Changing navigation
behaviour often means changing this tree rather than writing code.

## Costmaps

The costmap is how Nav2 represents the world for planning. It is a grid where
each cell holds a **cost** from 0 to 254 — not simply free or occupied, but
*how bad it would be to drive here*.

There are two, deliberately:

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
* - Updates at
  - ~1 Hz
  - ~5 Hz
* - Built from
  - The static map, plus sensors
  - Live sensor data only
* - Used by
  - The planner
  - The controller
* - Answers
  - "Which route should I take?"
  - "What is in front of me right now?"
```

The local costmap uses the `odom` frame on purpose: `odom` is smooth, so
obstacles do not jump around when localization corrects itself.

### Costmap layers

Each costmap is assembled from plugin **layers**:

`static_layer`
: the saved map from `map_server`

`obstacle_layer`
: obstacles from live sensor data, marked and cleared as the robot observes
  them

`voxel_layer`
: like the obstacle layer but 3D-aware, so it can distinguish a table top from
  the floor

`inflation_layer`
: expands obstacles by the robot's radius plus a margin, so the planner can
  treat the robot as a point

The **inflation layer** is the one worth understanding. Without it the planner
would happily route the robot's centre 2 cm from a wall — geometrically valid,
physically a collision. Two parameters control it:

`inflation_radius`
: how far the cost spreads from an obstacle. Roughly the robot's radius plus
  clearance.

`cost_scaling_factor`
: how quickly cost falls off with distance. Higher means the robot hugs walls
  more closely.

:::{tip}
If your robot refuses to fit through a doorway it physically fits through, the
inflation radius is too large. If it clips corners, it is too small. This one
parameter explains most doorway problems.
:::

## Setting up Nav2

### Install

```bash
sudo apt install ros-$ROS_DISTRO-navigation2 ros-$ROS_DISTRO-nav2-bringup
```

### The parameter file

Create a package `my_robot_navigation` with `config/` and `launch/`
directories. The parameter file is long; these are the parts you will actually
change.

```yaml
controller_server:
  ros__parameters:
    use_sim_time: False
    controller_frequency: 20.0
    progress_checker_plugins: ["progress_checker"]
    goal_checker_plugins: ["goal_checker"]
    controller_plugins: ["FollowPath"]

    progress_checker:
      plugin: "nav2_controller::SimpleProgressChecker"
      required_movement_radius: 0.5
      movement_time_allowance: 10.0

    goal_checker:
      plugin: "nav2_controller::SimpleGoalChecker"
      xy_goal_tolerance: 0.25
      yaw_goal_tolerance: 0.25
      stateful: True

    FollowPath:
      plugin: "dwb_core::DWBLocalPlanner"
      # --- velocity limits: set these to YOUR robot ---
      min_vel_x: 0.0
      max_vel_x: 0.26
      max_vel_theta: 1.0
      acc_lim_x: 2.5
      acc_lim_theta: 3.2
      # --- trajectory sampling ---
      vx_samples: 20
      vtheta_samples: 20
      sim_time: 1.7
      xy_goal_tolerance: 0.25
      critics: ["RotateToGoal", "Oscillation", "BaseObstacle", "GoalAlign",
                "PathAlign", "PathDist", "GoalDist"]

planner_server:
  ros__parameters:
    use_sim_time: False
    expected_planner_frequency: 20.0
    planner_plugins: ["GridBased"]
    GridBased:
      plugin: "nav2_navfn_planner/NavfnPlanner"
      tolerance: 0.5
      use_astar: false
      allow_unknown: true

local_costmap:
  local_costmap:
    ros__parameters:
      use_sim_time: False
      update_frequency: 5.0
      publish_frequency: 2.0
      global_frame: odom
      robot_base_frame: base_footprint
      rolling_window: true
      width: 3
      height: 3
      resolution: 0.05
      robot_radius: 0.22
      plugins: ["voxel_layer", "inflation_layer"]
      inflation_layer:
        plugin: "nav2_costmap_2d::InflationLayer"
        cost_scaling_factor: 1.0
        inflation_radius: 0.22
      voxel_layer:
        plugin: "nav2_costmap_2d::VoxelLayer"
        enabled: True
        publish_voxel_map: True
        z_resolution: 0.05
        z_voxels: 16
        max_obstacle_height: 2.0
        observation_sources: scan
        scan:
          topic: /scan
          max_obstacle_height: 2.0
          clearing: True
          marking: True
          data_type: "LaserScan"

global_costmap:
  global_costmap:
    ros__parameters:
      use_sim_time: False
      update_frequency: 1.0
      publish_frequency: 1.0
      global_frame: map
      robot_base_frame: base_footprint
      robot_radius: 0.22
      resolution: 0.05
      track_unknown_space: true
      plugins: ["static_layer", "obstacle_layer", "inflation_layer"]
      static_layer:
        plugin: "nav2_costmap_2d::StaticLayer"
        map_subscribe_transient_local: True
      obstacle_layer:
        plugin: "nav2_costmap_2d::ObstacleLayer"
        enabled: True
        observation_sources: scan
        scan:
          topic: /scan
          max_obstacle_height: 2.0
          clearing: True
          marking: True
          data_type: "LaserScan"
      inflation_layer:
        plugin: "nav2_costmap_2d::InflationLayer"
        cost_scaling_factor: 1.0
        inflation_radius: 0.22
```

:::{danger}
The velocity limits, `robot_radius` and `inflation_radius` above are **not**
values for your robot. `max_vel_x: 0.26` and a radius of 0.22 m describe a
small differential-drive platform. Measure your robot and set them, or it will
either crawl, or plan paths it cannot physically follow.

An omnidirectional robot {{ carologistics }} also needs a controller that can
use lateral motion, and a legged robot {{ alert }} has different constraints
again. Check your platform page.
:::

:::{warning}
`use_sim_time` appears in every block above. It must be `true` everywhere in
simulation and `false` everywhere on hardware. A single block left at the wrong
value produces transform-timeout errors that look like a TF problem.
:::

### Launching

```bash
ros2 launch nav2_bringup navigation_launch.py \
  use_sim_time:=False \
  params_file:=/path/to/your/nav2_params.yaml
```

The full startup sequence, in order:

1. **Robot bringup** — drivers, sensors, TF.
2. **Localization** — `map_server` and `amcl` from
   [session 5](05-mapping-localization.md).
3. **Nav2** — the navigation servers.
4. **RViz** — `File → Open Config →`
   `/opt/ros/$ROS_DISTRO/share/nav2_bringup/rviz/nav2_default_view.rviz`

Order matters: Nav2 needs the map and the transform chain to already exist.

## Navigating

1. Click **2D Pose Estimate** and set the robot's actual position.
2. Wait for the costmaps to appear in RViz.
3. Click **Nav2 Goal** and click-drag a goal pose on the map.
4. Watch: the planner draws a path, the controller follows it, and the local
   costmap lights up around obstacles.

### Sending goals from code

Navigation is exposed as an **action**, which is the right choice: it takes
time, it reports progress, and it can be cancelled.

```python
#!/usr/bin/env python3

import rclpy
from action_msgs.msg import GoalStatus
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient
from rclpy.node import Node


class GoalSender(Node):

    def __init__(self):
        super().__init__('goal_sender')
        self.client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

    def send_goal(self, x, y, yaw_z=0.0, yaw_w=1.0):
        self.client.wait_for_server()

        goal = NavigateToPose.Goal()
        goal.pose = PoseStamped()
        goal.pose.header.frame_id = 'map'
        goal.pose.header.stamp = self.get_clock().now().to_msg()
        goal.pose.pose.position.x = x
        goal.pose.pose.position.y = y
        goal.pose.pose.orientation.z = yaw_z
        goal.pose.pose.orientation.w = yaw_w

        self.get_logger().info(f'Sending goal: x={x:.2f} y={y:.2f}')

        send_future = self.client.send_goal_async(
            goal, feedback_callback=self.on_feedback)
        rclpy.spin_until_future_complete(self, send_future)
        goal_handle = send_future.result()

        if not goal_handle.accepted:
            self.get_logger().error('Goal rejected')
            return False

        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)

        status = result_future.result().status
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('Goal reached')
            return True

        self.get_logger().warning(f'Navigation ended with status {status}')
        return False

    def on_feedback(self, feedback):
        remaining = feedback.feedback.distance_remaining
        self.get_logger().info(f'{remaining:.2f} m remaining')


def main():
    rclpy.init()
    node = GoalSender()
    try:
        node.send_goal(1.5, 0.5)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

:::{note}
The goal's `frame_id` decides what the coordinates mean. `map` sends the robot
to an absolute position; `base_link` sends it to a position **relative to
itself** — "two metres forward from wherever you are". Both are useful; mixing
them up produces a robot that drives somewhere baffling.
:::

:::{tip}
To find coordinates on your map: in RViz use **Publish Point** and run
`ros2 topic echo /clicked_point` in a terminal. Click anywhere on the map and
read off the coordinates.
:::

## Autonomous exploration

Sending one goal is navigation. Choosing your own goals is exploration.

The simplest version picks random reachable points within the map bounds and
navigates to each in turn. It is crude, but it demonstrates the pattern that
session 7 builds on: a node that decides what to do, using navigation as a
service.

```python
import random

# Map bounds -- read these off YOUR map with Publish Point
MAP_MIN_X, MAP_MAX_X = -1.0, 3.0
MAP_MIN_Y, MAP_MAX_Y = 0.0, 4.0


def random_goal():
    return (
        round(random.uniform(MAP_MIN_X, MAP_MAX_X), 2),
        round(random.uniform(MAP_MIN_Y, MAP_MAX_Y), 2),
    )
```

A smarter approach is **frontier exploration**: find the boundaries between
known-free and unknown space, and drive to the nearest one. Repeat until no
frontiers remain, at which point the map is complete. The
[`nav2_wfd`](https://github.com/SeanReg/nav2_wavefront_frontier_exploration)
and `explore_lite` packages implement this.

:::{note}
Random goals in a mapped environment are for practice. For the hackathon you
want frontier exploration or a planned set of waypoints — random search wastes
time, and time is scored.
:::

## Task

:::{admonition} Task: navigate, obstruct, observe
:class: task

**Part 1 — Get Nav2 running.**

1. Bring up the robot, localization, and Nav2 in the correct order.
2. Open the Nav2 RViz configuration.
3. Set the initial pose and confirm both costmaps appear.
4. Send a goal with **Nav2 Goal** and watch the robot drive to it.

**Part 2 — Understand the costmaps.**

1. Toggle the global and local costmap displays on and off. Which shows the
   static map, and which the live obstacles?
2. Place an obstacle in front of the robot that is *not* in the saved map.
   Where does it appear?
3. Change `inflation_radius` to a much larger value, rebuild, and send the same
   goal again. What changed about the path?

**Part 3 — Force a re-plan.**

1. Send a goal several metres away.
2. While the robot is driving, place an obstacle across its planned path.
3. Watch the planned path in RViz. What happens, and how long does it take?
4. Now block it completely — surround the robot. What recovery behaviours
   trigger? Watch the Nav2 terminal output.

**Part 4 — Send goals from code.**

1. Adapt the action client above to send the robot to a pose you pick.
2. Extend it to alternate between **two** poses indefinitely.
3. Add feedback printing, and add a way to cancel the goal.
:::

:::{admonition} Expected result
:class: result

Part 1: the robot drives to the goal and stops within the goal tolerance.

Part 2: the obstacle appears in the local costmap immediately, and in the
global costmap on its slower update cycle. A larger inflation radius makes the
path bow further from walls, and beyond a point makes narrow doorways
unplannable.

Part 3: the path re-routes around the new obstacle within a second or two.
Fully blocked, the robot spins in place to clear its costmap, backs up, and
eventually reports that the goal is unreachable.

Part 4: the robot shuttles between two poses on its own, printing the remaining
distance.
:::

:::{dropdown} Hint: what to look at when the robot does not move
:icon: light-bulb

Work through this in order:

```bash
# 1. Is the action server there at all?
ros2 action list

# 2. Are the nodes activated? (Nav2 nodes are lifecycle nodes)
ros2 lifecycle get /planner_server
ros2 lifecycle get /controller_server

# 3. Is a velocity command being produced?
ros2 topic echo /cmd_vel

# 4. Is the transform chain complete?
ros2 run tf2_tools view_frames
```

If step 3 shows commands but the robot stands still, the problem is between
Nav2 and the motors, not in Nav2. Check the topic name your driver actually
subscribes to.
:::

## Common mistakes

**Nav2 starts but nothing happens.**
Lifecycle nodes not activated. Check the lifecycle manager and that its
`node_names` lists every server.

**"Goal rejected" or transform timeouts.**
`use_sim_time` is inconsistent, or the `map` → `odom` → `base_link` chain is
broken. Fix localization first.

**The robot spins on the spot and gives up.**
Recovery behaviours running because planning failed. Usually the goal is
unreachable, inside an obstacle, or the inflation radius has closed the route.

**The path goes through a wall.**
The global costmap is not getting the static map. Check
`map_subscribe_transient_local: True`.

**The robot oscillates near the goal.**
Goal tolerances are too tight for the robot's precision. Increase
`xy_goal_tolerance`.

**It drives far too slowly or overshoots.**
The velocity and acceleration limits do not match the robot. Measure them.

**Nav2 commands are ignored.**
Nav2 publishes on `/cmd_vel` by default; your driver may listen on something
else. Remap it.

## Further reading

- [Nav2 documentation](https://docs.nav2.org/) — thorough, and the first place
  to look
- [Nav2 documentation home](https://docs.nav2.org/jazzy/)
- [Nav2 configuration guide](https://docs.nav2.org/jazzy/configuration_and_development/configuration_guide/)
- [Nav2 first-time setup](https://docs.nav2.org/jazzy/configuration_and_development/first_time_robot_setup_guide/)
- [Behavior trees in Nav2](https://docs.nav2.org/jazzy/configuration_and_development/configuration_guide/core_servers/bt_plugins/) —
  the bridge to [session 7](07-autonomous-decisions.md)
