# Glossary

{{ common }}

Terms used throughout this course, in plain language.

## A

**Action**
: A ROS 2 communication pattern for long-running tasks: a goal is sent,
  feedback arrives while it runs, a result comes at the end, and it can be
  cancelled. Navigation is an action. See
  [module 2](../course/02-ros2/services-parameters-actions.md#try-it-yourself-actions).

**AMCL**
: Adaptive Monte Carlo Localization. Estimates the robot's pose on a known map
  using a particle filter. See
  [module 5](../course/05-mapping-localization.md).

**Ament**
: The build system underlying ROS 2 packages. `ament_python` for Python
  packages, `ament_cmake` for C++.

**Ansible**
: An automation tool that configures machines from declarative playbooks over
  SSH. Used by Carologistics for fleet deployment. See
  [module 8](../course/08-integration.md).

**AprilTag**
: A family of fiducial markers, robust at distance and in poor lighting. See
  [module 4](../course/04-perception/fiducial-markers.md).

**ArUco**
: A family of fiducial markers, built into OpenCV. See
  [module 4](../course/04-perception/fiducial-markers.md).

## B

**`base_link`**
: The coordinate frame attached to the robot's body. Sensor frames hang off it.

**`base_footprint`**
: The robot's position projected onto the ground plane.

**Behavior tree**
: A tree of nodes, ticked repeatedly, that decides what a robot does. Nav2 uses
  one internally. See
  [module 7](../course/07-autonomous-decisions.md#behavior-trees-in-contrast).

**Bringup**
: The set of launch files that start a robot's software. See
  [module 8](../course/08-integration.md).

## C

**Callback**
: A function that ROS 2 calls when something happens — a message arrives, a
  timer fires. Callbacks only run while the node is spinning.

**`cmd_vel`**
: The conventional topic name for velocity commands, carrying
  `geometry_msgs/msg/Twist`.

**colcon**
: The build tool for ROS 2 workspaces. `colcon build`.

**Costmap**
: A grid where each cell holds the cost of driving there, from 0 to 254. Nav2
  keeps a global one and a local one. See
  [module 6](../course/06-navigation.md#costmaps-global-vs-local).

**CUDA**
: NVIDIA's platform for general-purpose GPU computation. Used to accelerate
  neural network training and inference.

## D

**DDS**
: Data Distribution Service — the middleware ROS 2 uses to move messages
  between nodes. Fast DDS and Cyclone DDS are two implementations.

**Detection**
: Finding *what* is in an image, in image coordinates. Distinct from
  localization. See
  [module 4](../course/04-perception/perception-pipeline.md#why-a-robot-needs-it).

**Domain ID**
: An integer that partitions a network into independent ROS 2 systems. Nodes
  only see each other if they share one. See
  [Networking](../prerequisites/networking.md).

**Drift**
: The gradual accumulation of error in odometry, which is never corrected by
  odometry itself.

## E

**Encoder**
: A sensor measuring how far a motor has turned. The basis of odometry.

**E-stop**
: Emergency stop. A physical button that cuts motor power independently of
  software.

## F

**Fiducial marker**
: A printed pattern designed to be detected reliably and identified uniquely,
  giving a full 6D pose from one image. ArUco and AprilTag are two families.

**Frame**
: A coordinate system. Everything in ROS 2 that has a position is expressed in
  some frame. See [module 3](../course/03-sensors-tf.md).

**Frontier exploration**
: Autonomously exploring by repeatedly driving to the boundary between known
  and unknown space.

## G

**GLIM**
: A LiDAR–inertial SLAM system for accurate 3D mapping. Used by ALeRT.

**Golog++**
: An action language for high-level robot control, combining programmed
  structure with planning.

**GVM**
: Global Variable Manager. RAFCON's mechanism for sharing values between
  states.

## I

**IK**
: Inverse kinematics. Given a desired gripper pose, compute the joint angles
  that achieve it.

**IMU**
: Inertial measurement unit. Measures acceleration and angular velocity.

**Inflation**
: Expanding obstacles in a costmap by the robot's radius plus a margin, so the
  planner can treat the robot as a point. See
  [module 6](../course/06-navigation.md#costmaps-global-vs-local).

## L

**Launch file**
: A file that starts several nodes together, with parameters and remappings.
  YAML, XML or Python. See
  {ref}`module 2 <launch-files>`.

**LaserScan**
: The message type for 2D laser data: an array of ranges plus the geometry
  needed to interpret them.

**Lifecycle node**
: A node with explicit states — unconfigured, inactive, active. Nav2 nodes are
  lifecycle nodes and do nothing until activated.

**LiDAR**
: Light Detection and Ranging. Measures distance by timing reflected laser
  light.

**Localization**
: Determining where the robot is on a known map. Also: determining where a
  detected object is in the world.

## M

**`map` frame**
: The fixed world frame. Does not drift, but jumps when localization corrects
  itself.

**MoveIt**
: The motion planning framework for manipulators in ROS.

**MPS**
: Modular Production Station. The Festo machines used in the RoboCup Logistics
  League. {{ carologistics }}

## N

**Namespace**
: A prefix applied to a node's names, so several instances can run without
  colliding: `/robot1/scan` and `/robot2/scan`.

**Nav2**
: The ROS 2 navigation stack. See [module 6](../course/06-navigation.md).

**Node**
: One program doing one job in a ROS 2 system.

## O

**Occupancy grid**
: A 2D map where each cell is free (0), occupied (100) or unknown (−1).

**Octomap**
: A 3D occupancy map stored as an octree — the 3D analogue of an occupancy
  grid. {{ alert }}

**`odom` frame**
: The odometry frame. Smooth and continuous, but drifts over time.

**Odometry**
: The robot's own estimate of how far it has travelled, from encoders and
  often an IMU.

**OpenCV**
: The standard computer vision library.

**OpenVINO**
: An Intel runtime for efficient neural network inference on CPUs.

## P

**Package**
: The unit of organisation in ROS 2: nodes, launch files and configuration,
  built and installed together.

**Parameter**
: A node's configuration value, readable and changeable at runtime.

**Particle filter**
: An estimation method using many weighted hypotheses. AMCL uses one.

**PlanSys2**
: A PDDL-based planning system for ROS 2.

**Publisher**
: The side of a topic that sends messages.

## Q

**QoS**
: Quality of Service. Policies governing how messages are delivered.
  Incompatible policies mean **no data flows, with no error message** — one of
  the most common problems in ROS 2. See
  [module 3](../course/03-sensors-tf.md#common-problems).

## R

**RAFCON**
: A graphical state machine editor and execution engine from DLR. See
  [module 7](../course/07-autonomous-decisions.md).

**rclpy**
: The Python client library for ROS 2. (`rclcpp` is the C++ one.)

**RCLL**
: RoboCup Logistics League. {{ carologistics }}

**Recovery behavior**
: What Nav2 does when planning or control fails: clear the costmap, spin, back
  up, wait.

**Refbox**
: Referee box. Issues orders and scores a RoboCup game. {{ carologistics }}

**Remapping**
: Renaming a topic, service or node at launch time without changing code.

**rosbag**
: A recording of ROS 2 topics that can be replayed. See
  [module 8](../course/08-integration.md#rosbags-briefly).

**RRL**
: RoboCup Rescue League. {{ alert }}

**RViz**
: The 3D visualization tool for ROS. See
  [module 3](../course/03-sensors-tf.md).

## S

**Service**
: A ROS 2 communication pattern: a request, then a response. For quick
  operations with an answer.

**SLAM**
: Simultaneous Localization And Mapping. Building a map while working out where
  you are in it.

**SLAM Toolbox**
: The standard 2D SLAM package for ROS 2. See
  [module 5](../course/05-mapping-localization.md).

**Sourcing**
: Running a setup script in the current shell so ROS 2 can find packages.
  `source install/setup.bash`.

**Spin**
: Handing control to ROS 2 so it can run callbacks. `rclpy.spin(node)` runs
  until shutdown; `spin_once()` handles one round of work.

**State machine**
: A model where the system is in exactly one state, with defined transitions
  between them. See
  [module 7](../course/07-autonomous-decisions.md#finite-state-machines).

**Subscriber**
: The side of a topic that receives messages.

## T

**TF2**
: The transform library. Tracks the relationships between coordinate frames and
  converts between them. See [module 3](../course/03-sensors-tf.md).

**Topic**
: A named channel carrying messages of one type, from any number of publishers
  to any number of subscribers.

**Transform**
: The translation and rotation relating one frame to another.

**Twist**
: `geometry_msgs/msg/Twist` — linear and angular velocity. What `/cmd_vel`
  carries.

## U

**`use_sim_time`**
: A parameter telling a node to use the simulator's clock rather than the
  system clock. Must be consistent across **every** node. The single most
  common cause of inexplicable behaviour in simulation.

## W

**Webots**
: The open-source robot simulator used by both institute teams.

**Workspace**
: A directory where you build ROS 2 packages, containing `src`, `build`,
  `install` and `log`.

## Y

**YOLO**
: "You Only Look Once" — a family of fast neural network object detectors. See
  [module 4](../course/04-perception/object-detection.md).
