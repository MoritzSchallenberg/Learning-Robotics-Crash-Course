# Learning Robotics Crash Course

A hands-on introduction to autonomous mobile robotics for the teams and
research groups of the **MASKOR Institute at FH Aachen**.

Eight modules build up from the anatomy of a robot to a fully autonomous
mission — sensing, transforms, perception, mapping and localization,
navigation, and high-level decision making — and a closing capstone project
puts everything together on a real or simulated robot.

<a class="lrcc-cta" href="course/index.html">Start the Course →</a>

## Who this is for

New members of the robotics teams who already bring some technical
grounding — you can program a little (Python is enough), you are not afraid
of a terminal, and you want to understand how an autonomous robot actually
works. This is not a general first-semester introduction to programming or
computing.

You do **not** need prior ROS experience. You do **not** need to own a
robot: every module can be completed in simulation.

By the end of the course you will be able to bring up a robot system,
inspect it with the ROS 2 command line, read its sensors, build a map,
navigate autonomously in that map, detect objects with a camera, and tie the
pieces together into a mission that runs without a human in the loop.

## What the course covers

The course is built on **ROS 2**, the middleware that nearly all modern
research robots use. Around it you work through the classic autonomy stack:
sensing, transforms, perception, mapping and localization, navigation, and
high-level decision making — always with a practical task, and always on
hardware or a simulator you can actually run.

## Before you start

:::{admonition} Work through the prerequisites first
:class: important

The course starts at the hardware, not at the installer. Complete the
[prerequisites](prerequisites/index.md) first — a working Linux system with
ROS 2 installed makes every module go smoothly.
:::

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} Prerequisites
:link: prerequisites/index
:link-type: doc

Linux and the terminal, ROS 2 installation, Git, and the networking basics
you need to talk to a robot.
:::

:::{grid-item-card} Platform tracks
:link: platforms/index
:link-type: doc

The same course, on your team's system: pure simulation,
Carologistics/Robotino, or ALeRT/Spot.
:::

::::

## The eight course modules

```{list-table}
:header-rows: 1
:widths: 6 34 60
:class: lrcc-schedule

* - #
  - Module
  - Focus
* - 1
  - [System Architecture and Robot Hardware](course/01-system-hardware.md)
  - How a robot is built: sensors, compute, drives, power, safety
* - 2
  - [ROS 2 Fundamentals](course/02-ros2.md)
  - Workspaces, packages, nodes, topics, parameters, launch files
* - 3
  - [Sensors, TF2 and RViz](course/03-sensors-tf.md)
  - Sensor messages, coordinate frames, transforms, visualization
* - 4
  - [Perception and Object Detection](course/04-perception/index.md)
  - Camera calibration, OpenCV, markers, YOLO, data labeling
* - 5
  - [Mapping and Localization](course/05-mapping-localization.md)
  - Odometry, occupancy grids, SLAM Toolbox, AMCL
* - 6
  - [Autonomous Navigation](course/06-navigation.md)
  - Nav2, costmaps, planners, controllers, recoveries, exploration
* - 7
  - [Autonomous Decisions and Manipulation](course/07-autonomous-decisions.md)
  - State machines, behavior trees, RAFCON, MoveIt
* - 8
  - [System Integration and Testing](course/08-integration.md)
  - Startup order, configuration, logging, rosbags, debugging
```

The modules build on each other in order — module 3 gives you transforms,
which module 5 needs to build a map, which module 6 needs to navigate,
which module 7 needs to run a mission. If you are joining partway through,
[the course overview](course/index.md) lists each module's prerequisites so
you can see what to catch up on first.

## Capstone project

[Autonomous Robot Mission](course/hackathon.md) — a robot has to cross an
operation area on its own, avoid obstacles, find a target and reach it.
Extended tasks add picking the object up, transporting it, or reporting its
position to another system. It draws on every module above and is the
course's final self-check: if you can complete it, the course has done its
job.

## How to read this site

The **course modules** explain the shared fundamentals once. They are
written to be readable no matter which robot your team runs.

The **platform pages** carry only what is specific to one system — Robotino
commands, Spot startup, simulation launch files — and link back to the
shared explanation instead of repeating it.

Commands that only apply to one system carry a badge:

{{ common }} works everywhere &nbsp;
{{ simulation }} simulation only &nbsp;
{{ carologistics }} Carologistics/Robotino &nbsp;
{{ alert }} ALeRT/Spot

Content within a module is also marked by how essential it is to that
module's core learning objective:

{{ core }} the module's central concept and task &nbsp;
{{ optional }} worth doing if you have the time &nbsp;
{{ advanced }} deliberately beyond the module's core scope, for later
reading &nbsp;
{{ platformspecific }} Robotino, Spot or simulation only

The whole course runs on one fixed toolchain — Ubuntu 22.04 LTS and ROS 2
Humble — so no command needs its own distribution badge. See
[Supported environment](reference/compatibility.md) for the exact versions
and how to check them on your own machine.

```{toctree}
:hidden:
:maxdepth: 2
:caption: Getting started

prerequisites/index
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: Course

course/index
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: Platform tracks

platforms/index
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: Reference

reference/index
```
