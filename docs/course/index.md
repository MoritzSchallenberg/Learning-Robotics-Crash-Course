# The course

Eight modules, each built around one central concept and one practical
task, followed by a capstone project that ties them together.

Every module marks its content by how essential it is:
{{ core }} (the module's central concept and task),
{{ optional }} (worth doing with extra time), {{ advanced }} (deliberately
beyond the module's core scope, for later reading) or
{{ platformspecific }} (Robotino, Spot or simulation only). If you only have
time for one thing on any page, do the **Core** practical task — it is what
the next module assumes you can do.

## The learning path

```{list-table}
:header-rows: 1
:widths: 6 26 34 34

* - #
  - Module
  - Focus
  - Result
* - 1
  - [System Architecture and Robot Hardware](01-system-hardware.md)
  - System and hardware
  - Understand components and data flows
* - 2
  - [ROS 2 Fundamentals](02-ros2.md)
  - ROS 2
  - Use nodes, topics and packages
* - 3
  - [Sensors, TF2 and RViz](03-sensors-tf.md)
  - Sensors and TF2
  - Place sensor data correctly in space
* - 4
  - [Perception and Object Detection](04-perception/index.md)
  - Perception
  - Detect a marker or object
* - 5
  - [Mapping and Localization](05-mapping-localization.md)
  - Mapping and localization
  - Build a map and locate the robot
* - 6
  - [Autonomous Navigation](06-navigation.md)
  - Navigation
  - Reach autonomous goals
* - 7
  - [Autonomous Decisions and Manipulation](07-autonomous-decisions.md)
  - Decisions
  - Model a mission
* - 8
  - [System Integration and Testing](08-integration.md)
  - Integration
  - Start and debug the whole system
* - Capstone
  - [Autonomous Robot Mission](hackathon.md)
  - Autonomous mission
  - Combine every module
```

## How the modules build on each other

The course is a single arc, not eight independent topics. Module 3 gives you
transforms, which module 5 needs to build a map, which module 6 needs to
navigate, which module 7 needs to run a mission. Each module's **Core**
practical task is what the following module's **Prerequisites** section
assumes you can already do — skipping a module's reading is survivable,
skipping its Core task is not.

## Joining partway through

If you already have some of these skills, you can start wherever your
knowledge runs out — each module's own **Prerequisites** section states
exactly what it assumes, so you can check quickly whether to work through
the earlier modules first or jump straight in. A reasonable self-check:

- Comfortable with a Linux terminal and `git`? Skip straight to
  [module 1](01-system-hardware.md).
- Already know ROS 2 nodes, topics and launch files? Start at
  [module 3](03-sensors-tf.md).
- Already have TF2 and RViz down? Start at
  [module 4](04-perception/index.md).

Each module is still worth skimming even if you know the general topic —
the platform-specific notes and the exact tools this course standardises on
(SLAM Toolbox, Nav2, ArUco/AprilTag, MoveIt) may differ from what you have
used before.

## Before you start

Work through the [prerequisites](../prerequisites/index.md), and find your
[platform track](../platforms/index.md) so you know which commands apply to
your robot.

```{toctree}
:maxdepth: 1
:caption: Modules

01-system-hardware
02-ros2
03-sensors-tf
04-perception/index
05-mapping-localization
06-navigation
07-autonomous-decisions
08-integration
hackathon
```
