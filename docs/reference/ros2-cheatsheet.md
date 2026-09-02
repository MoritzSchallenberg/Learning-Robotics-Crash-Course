# ROS 2 cheat sheet

{{ common }}

The commands you will actually use, in one place. Everything here works on both
[Humble and Jazzy](compatibility.md) unless noted.

:::{tip}
Write `$ROS_DISTRO` instead of `humble` or `jazzy` and your commands work on
both systems.
:::

## Environment

```bash
echo $ROS_DISTRO                          # which distribution is sourced?
source /opt/ros/$ROS_DISTRO/setup.bash    # source the installation
source ~/robot_ws/install/setup.bash      # source your workspace on top
echo $AMENT_PREFIX_PATH                   # package search order
printenv | grep ROS                       # all ROS environment variables
ros2 daemon stop                          # reset the discovery daemon
```

## Building

```bash
colcon build                                     # build everything
colcon build --packages-select <pkg>             # build one package
colcon build --symlink-install                   # Python changes take effect
                                                 #   without rebuilding
colcon build --packages-up-to <pkg>              # a package and its deps
rm -rf build install log && colcon build         # clean rebuild
```

:::{warning}
Never `sudo colcon build`. It creates root-owned files you cannot overwrite
later.
:::

## Packages

```bash
ros2 pkg list                       # all packages
ros2 pkg list | grep nav2           # find one
ros2 pkg prefix <pkg>               # where is it installed?
ros2 pkg executables <pkg>          # what can I run from it?
ros2 pkg xml <pkg>                  # its package.xml

ros2 pkg create --build-type ament_python <name> --dependencies rclpy
ros2 pkg create --build-type ament_cmake <name> --dependencies rclcpp
```

## Nodes

```bash
ros2 run <pkg> <executable>                 # start a node
ros2 node list                              # running nodes
ros2 node info /<node>                      # its topics, services, actions

# Rename a node or remap a topic at launch
ros2 run <pkg> <exe> --ros-args -r __node:=new_name
ros2 run <pkg> <exe> --ros-args -r /cmd_vel:=/robot/cmd_vel
```

## Topics

```bash
ros2 topic list                     # all topics
ros2 topic list -t                  # with message types
ros2 topic echo /<topic>            # print messages as they arrive
ros2 topic echo /<topic> --once     # just one
ros2 topic info /<topic>            # type and connection counts
ros2 topic info -v /<topic>         # ... plus the QoS profiles
ros2 topic hz /<topic>              # actual publishing rate
ros2 topic bw /<topic>              # bandwidth used
ros2 topic find <msg_type>          # which topics carry this type?

# Publish by hand
ros2 topic pub /<topic> <type> '<yaml>'
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
  '{linear: {x: 0.2}, angular: {z: 0.0}}'

# Stop a robot immediately
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist '{}'
```

:::{tip}
`ros2 topic info -v` is the single most useful debugging command in ROS 2. It
shows both the connection counts and the QoS profiles — the two things that
silently prevent data from flowing.
:::

## Interfaces

```bash
ros2 interface show <type>              # what fields does it have?
ros2 interface list                     # every known interface
ros2 interface package <pkg>            # interfaces in one package
ros2 interface proto <type>             # a template you can fill in

ros2 interface show sensor_msgs/msg/LaserScan
ros2 interface show geometry_msgs/msg/Twist
```

## Services

```bash
ros2 service list                       # all services
ros2 service list -t                    # with types
ros2 service type /<service>            # the type of one
ros2 service find <type>                # which services use this type?
ros2 service call /<service> <type> '<yaml>'

ros2 service call /reset std_srvs/srv/Empty "{}"
```

## Actions

```bash
ros2 action list                        # all actions
ros2 action list -t                     # with types
ros2 action info /<action>              # clients and servers
ros2 action send_goal /<action> <type> '<yaml>'
ros2 action send_goal --feedback /<action> <type> '<yaml>'

ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose \
  '{pose: {header: {frame_id: map}, pose: {position: {x: 1.0, y: 0.5}}}}'
```

## Parameters

```bash
ros2 param list                         # every parameter of every node
ros2 param list /<node>                 # one node's parameters
ros2 param get /<node> <param>
ros2 param set /<node> <param> <value>
ros2 param describe /<node> <param>     # type, constraints, description
ros2 param dump /<node>                 # all values, as YAML
ros2 param load /<node> <file.yaml>     # apply a file
```

## Transforms

```bash
ros2 run tf2_tools view_frames                    # writes frames.pdf
ros2 run tf2_ros tf2_echo <source> <target>       # live transform
ros2 topic echo /tf_static

# Publish a static transform by hand
ros2 run tf2_ros static_transform_publisher \
  <x> <y> <z> <yaw> <pitch> <roll> <parent> <child>

ros2 run tf2_ros static_transform_publisher \
  0 0 0.15 0 0 3.14159 base_link laser_frame
```

:::{warning}
The Euler form takes **yaw pitch roll**, in that order — not roll pitch yaw.
This trips up nearly everyone at least once.
:::

## Launch

```bash
ros2 launch <pkg> <file.launch.yaml>
ros2 launch <pkg> <file.launch.py> use_sim_time:=true
ros2 launch <pkg> <file> --show-args        # what arguments does it take?
ros2 launch -d <pkg> <file>                 # debug output
```

## Lifecycle nodes

Nav2 nodes are lifecycle nodes; they do nothing until activated.

```bash
ros2 lifecycle nodes                    # which nodes have a lifecycle?
ros2 lifecycle get /<node>              # current state
ros2 lifecycle set /<node> configure
ros2 lifecycle set /<node> activate
```

## Recording and replay

```bash
ros2 bag record -a                                  # everything (large!)
ros2 bag record /scan /odom /tf /tf_static
ros2 bag record -o <name> /scan /odom /tf /tf_static

ros2 bag info <name>
ros2 bag play <name>
ros2 bag play <name> --rate 0.5
ros2 bag play <name> --loop
ros2 bag play <name> --clock              # publish /clock, for use_sim_time
```

:::{warning}
Always record `/tf` **and** `/tf_static`. Without both, nothing in the replay
can be placed in space.
:::

## Introspection tools

```bash
rviz2                                   # 3D visualization
rqt                                     # plugin-based GUI
ros2 run rqt_graph rqt_graph            # the node and topic graph
ros2 run rqt_console rqt_console        # log viewer
ros2 run rqt_plot rqt_plot              # plot numeric topics live
ros2 run rqt_publisher rqt_publisher    # publish to a topic from a GUI
ros2 run rqt_reconfigure rqt_reconfigure # change parameters live
```

## Teleoperation

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard

# With a remapped topic
ros2 run teleop_twist_keyboard teleop_twist_keyboard \
  --ros-args -r /cmd_vel:=/robot/cmd_vel

ros2 run joy joy_node                   # gamepad driver, publishes /joy
```

## Navigation

```bash
sudo apt install ros-$ROS_DISTRO-navigation2 ros-$ROS_DISTRO-nav2-bringup

ros2 launch nav2_bringup navigation_launch.py
ros2 launch slam_toolbox online_async_launch.py
ros2 run nav2_map_server map_saver_cli -f <name>

# Send a goal
ros2 topic pub --once /goal_pose geometry_msgs/msg/PoseStamped \
  '{header: {frame_id: map}, pose: {position: {x: 1.0, y: 0.5}}}'
```

## Common environment variables

```bash
export ROS_DOMAIN_ID=<0-101>          # partition the network
export ROS_LOCALHOST_ONLY=1           # this machine only -- overrides the above
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export CYCLONEDDS_URI=file:///path/to/cyclone_dds.xml
```

## Diagnostic sequence

When something does not work, in this order:

```bash
ros2 node list                          # 1. is the node running?
ros2 topic hz /<topic>                  # 2. is anything published?
ros2 topic info -v /<topic>             # 3. do names and QoS match?
ros2 run tf2_tools view_frames          # 4. is the TF tree complete?
ros2 lifecycle get /<node>              # 5. is it activated?
ros2 param get /<node> use_sim_time     # 6. is sim time consistent?
ros2 run rqt_graph rqt_graph            # 7. look at the whole graph
```

Full explanation in
[module 8](../course/08-integration.md#the-eight-step-diagnostic-procedure).

## Message types you will meet

```{list-table}
:header-rows: 1
:widths: 42 58

* - Type
  - Used for
* - `std_msgs/msg/String`, `Int32`, `Bool`
  - Simple values, examples, scoring topics
* - `geometry_msgs/msg/Twist`
  - Velocity commands (`/cmd_vel`)
* - `geometry_msgs/msg/PoseStamped`
  - A pose with a frame and timestamp
* - `geometry_msgs/msg/TransformStamped`
  - A transform between two frames
* - `sensor_msgs/msg/LaserScan`
  - 2D laser data
* - `sensor_msgs/msg/PointCloud2`
  - 3D point clouds
* - `sensor_msgs/msg/Image`
  - Camera images
* - `sensor_msgs/msg/CameraInfo`
  - Camera calibration
* - `sensor_msgs/msg/Imu`
  - IMU data
* - `sensor_msgs/msg/Joy`
  - Gamepad input
* - `nav_msgs/msg/Odometry`
  - Odometry
* - `nav_msgs/msg/OccupancyGrid`
  - Maps
* - `nav_msgs/msg/Path`
  - A planned path
* - `nav2_msgs/action/NavigateToPose`
  - The navigation action
* - `vision_msgs/msg/Detection2DArray`
  - Object detections
```

## Further reading

- [ROS 2 CLI documentation](https://docs.ros.org/en/jazzy/Concepts/Basic/About-Command-Line-Tools.html)
- [ROS 2 tutorials](https://docs.ros.org/en/jazzy/Tutorials.html)
- [Nav2 documentation](https://docs.nav2.org/)
- [Glossary](glossary.md) on this site
