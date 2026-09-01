# Learning Robotics Crash Course

A shared introduction to autonomous mobile robotics for the teams and research
groups of the **MASKOR Institute at FH Aachen**.

The course brings together material that used to live in three separate places
— the ROS Summer School, the ALeRT/Spot practical course and the Carologistics
team wiki — into one path that every team can follow. Eight evening sessions
build up from the anatomy of a robot to a fully autonomous mission, and a
closing hackathon puts everything together on a real or simulated robot.

<a class="lrcc-cta" href="course/index.html">Start the Course →</a>

## Who this is for

New members of the robotics teams who already bring some technical
grounding — you can program a little (Python is enough), you are not afraid of
a terminal, and you want to understand how an autonomous robot actually works.

You do **not** need prior ROS experience. You do **not** need to own a robot:
every session can be followed in simulation.

By the end of the course you will be able to bring up a robot system, inspect
it with the ROS 2 command line, read its sensors, build a map, navigate
autonomously in that map, detect objects with a camera, and tie the pieces
together into a mission that runs without a human in the loop.

## What the course covers

The course is built on **ROS 2**, the middleware that nearly all modern
research robots use. Around it we work through the classic autonomy stack:
sensing, transforms, perception, mapping and localization, navigation, and
high-level decision making — always with a practical task, and always on
hardware or a simulator you can actually run.

## Before the first session

:::{admonition} Please arrive prepared
:class: important

The first evening starts at the hardware, not at the installer. Work through
the [prerequisites](prerequisites/index.md) beforehand — a working Linux
system with ROS 2 installed saves the whole group a lot of time.
:::

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} Prerequisites
:link: prerequisites/index
:link-type: doc

Linux and the terminal, ROS 2 installation, Git, and the networking basics you
need to talk to a robot.
:::

:::{grid-item-card} Platform tracks
:link: platforms/index
:link-type: doc

The same course, on your team's system: pure simulation,
Carologistics/Robotino, or ALeRT/Spot.
:::

::::

## The eight course evenings

All sessions run from **17:35 to 19:00**.

```{list-table}
:header-rows: 1
:widths: 6 22 44 28
:class: lrcc-schedule

* - #
  - Date
  - Session
  - Focus
* - 1
  - Mon, 05 Oct 2026
  - [System Architecture and Robot Hardware](course/01-system-hardware.md)
  - How a robot is built: sensors, compute, drives, power, safety
* - 2
  - Wed, 07 Oct 2026
  - [ROS 2 Fundamentals](course/02-ros2.md)
  - Workspaces, packages, nodes, topics, parameters, launch files
* - 3
  - Mon, 12 Oct 2026
  - [Sensors, TF2 and RViz](course/03-sensors-tf.md)
  - Sensor messages, coordinate frames, transforms, visualization
* - 4
  - Wed, 14 Oct 2026
  - [Perception and Object Detection](course/04-perception.md)
  - Camera calibration, OpenCV, markers, YOLO, data labeling
* - 5
  - Mon, 19 Oct 2026
  - [Mapping and Localization](course/05-mapping-localization.md)
  - Odometry, occupancy grids, SLAM Toolbox, AMCL
* - 6
  - Wed, 21 Oct 2026
  - [Autonomous Navigation](course/06-navigation.md)
  - Nav2, costmaps, planners, controllers, recoveries, exploration
* - 7
  - Mon, 26 Oct 2026
  - [Autonomous Decisions and Manipulation](course/07-autonomous-decisions.md)
  - State machines, behavior trees, RAFCON, MoveIt
* - 8
  - Wed, 28 Oct 2026
  - [System Integration and Testing](course/08-integration.md)
  - Startup order, configuration, logging, rosbags, debugging
```

## Closing hackathon

**Sat–Sun, 07–08 Nov 2026** — the
[Autonomous Robot Challenge](course/hackathon.md). A robot has to cross an
operation area on its own, avoid obstacles, find a target and reach it. Extended
levels add picking the object up, transporting it, or reporting its position to
another system.

## How to read this site

The **course modules** explain the shared fundamentals once. They are written
to be readable no matter which robot your team runs.

The **platform pages** carry only what is specific to one system — Robotino
commands, Spot startup, simulation launch files — and link back to the shared
explanation instead of repeating it.

Commands that only apply to one system or one ROS 2 distribution carry a badge:

{{ common }} works everywhere &nbsp;
{{ simulation }} simulation only &nbsp;
{{ carologistics }} Carologistics/Robotino &nbsp;
{{ alert }} ALeRT/Spot &nbsp;
{{ jazzy }} ROS 2 Jazzy &nbsp;
{{ humble }} ROS 2 Humble

:::{warning}
The three source courses were written for **different** operating systems and
ROS 2 distributions. Never mix a Humble guide with a Jazzy setup without
checking. The [compatibility matrix](reference/compatibility.md) lists which
combination each instruction was written for.
:::

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
