# The course

Eight evenings, each **17:35 – 19:00**, followed by a weekend hackathon.

Every session follows the same shape: a short block of theory, then a
hands-on task you run yourself. The theory exists to make the task make sense —
if you only have time for one, do the task.

## How the sessions build on each other

The course is a single arc. Session 3 gives you transforms, which session 5
needs to build a map, which session 6 needs to navigate, which session 7 needs
to run a mission. Skipping an evening is survivable; skipping the task is not.

```{list-table}
:header-rows: 1
:widths: 5 20 40 35

* - #
  - Date
  - Session
  - You will be able to
* - 1
  - Mon, 05 Oct 2026
  - [System Architecture and Robot Hardware](01-system-hardware.md)
  - Name every component of a robot and trace data and power through it
* - 2
  - Wed, 07 Oct 2026
  - [ROS 2 Fundamentals](02-ros2.md)
  - Build a package, write a node, inspect a running system
* - 3
  - Mon, 12 Oct 2026
  - [Sensors, TF2 and RViz](03-sensors-tf.md)
  - Read sensor data and place it correctly in space
* - 4
  - Wed, 14 Oct 2026
  - [Perception and Object Detection](04-perception.md)
  - Find a marker or an object in a camera image and publish where it is
* - 5
  - Mon, 19 Oct 2026
  - [Mapping and Localization](05-mapping-localization.md)
  - Build a map and know where the robot is inside it
* - 6
  - Wed, 21 Oct 2026
  - [Autonomous Navigation](06-navigation.md)
  - Send the robot to a goal and watch it re-plan around an obstacle
* - 7
  - Mon, 26 Oct 2026
  - [Autonomous Decisions and Manipulation](07-autonomous-decisions.md)
  - Model a mission as a state machine or behavior tree
* - 8
  - Wed, 28 Oct 2026
  - [System Integration and Testing](08-integration.md)
  - Bring up a whole system, find a fault, and record evidence
```

## The hackathon

**Sat–Sun, 07–08 Nov 2026** — [Autonomous Robot Challenge](hackathon.md).
Everything from the eight sessions, on one robot, running on its own.

## Before you start

Work through the [prerequisites](../prerequisites/index.md), and find your
[platform track](../platforms/index.md) so you know which commands apply to
your robot.

```{toctree}
:maxdepth: 1
:caption: Sessions

01-system-hardware
02-ros2
03-sensors-tf
04-perception
05-mapping-localization
06-navigation
07-autonomous-decisions
08-integration
hackathon
```
