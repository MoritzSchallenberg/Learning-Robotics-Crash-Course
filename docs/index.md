# ALeRT Advanced Robotics Tutorial

A technical reference and tutorial site for **ALeRT** (Aachen Legged
Rescue Team), the RoboCup Rescue League team at the **MASKOR Institute,
FH Aachen**. It explains the robotics, ROS 2 and ALeRT-specific systems
this team's software is built on, for anyone who wants to understand or
extend it.

<a class="lrcc-cta" href="course/index.html">Browse the topics →</a>

:::{admonition} This site is being restructured
:class: important

This page still links to the site's earlier module-based structure while
the move to a topic-based navigation (Getting Started, ROS 2, ALeRT
Platforms and Safety, Simulation, Sensors and Coordinate Frames,
Perception, Mapping and World Models, Localization/Navigation/Exploration,
Robot Manipulation, Autonomous Decision-Making, Integration/Diagnostics/
Testing, Rescue Applications and Projects, Reference) is completed. Links
below remain valid; their location in the navigation will change.
:::

## Who this is for

Anyone working on or learning from ALeRT's software — team members getting
started, and anyone consulting a specific topic (ROS 2 concepts, a sensor,
Nav2, MoveIt 2, a specific ALeRT repository) as a reference. Some prior
programming ability (Python is enough) is assumed; no prior ROS 2
experience is required.

Every topic states what it needs, what is documented versus verified only
in simulation versus verified on physical hardware, and links to the
ALeRT repositories it is grounded in.

## What this site covers

Built around **ROS 2**, the middleware ALeRT's software uses throughout.
Topics cover the full autonomy stack — sensing, transforms, perception,
mapping, localization, navigation, decision-making and manipulation — each
explained in general terms first, then tied to how ALeRT's own systems
(Spot, its manipulator, and the surrounding sensor and compute stack)
actually use it.

## Before you start

:::{admonition} Work through Getting Started first
:class: important

A working Linux system with ROS 2 Humble installed makes every later topic
go smoothly. See [Prerequisites](prerequisites/index.md).
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

The same material, on your system: pure simulation, or ALeRT/Spot.
:::

::::

## Current topics

```{list-table}
:header-rows: 1
:widths: 34 66

* - Topic
  - Covers
* - [Hardware Design with KiCad and Fusion](course/01-system-hardware.md)
  - Electrical schematics in KiCad, parametric mechanical parts in Fusion
* - [ROS 2 Fundamentals](course/02-ros2.md)
  - Workspaces, packages, nodes, topics, parameters, launch files
* - [Sensors, TF2 and RViz](course/03-sensors-tf.md)
  - Sensor messages, coordinate frames, transforms, visualization
* - [Perception and Object Detection](course/04-perception/index.md)
  - Camera calibration, OpenCV, markers, YOLO, data labeling
* - [Mapping and Localization](course/05-mapping-localization.md)
  - Odometry, occupancy grids, SLAM Toolbox, AMCL
* - [Autonomous Navigation](course/06-navigation.md)
  - Nav2, costmaps, planners, controllers, recoveries, exploration
* - [Autonomous Decisions and Manipulation](course/07-autonomous-decisions.md)
  - State machines, behavior trees, RAFCON, MoveIt
* - [System Integration and Testing](course/08-integration.md)
  - Startup order, configuration, logging, rosbags, debugging
```

Topics build on each other where a real dependency exists — transforms
are needed before mapping, mapping before navigation, navigation before a
full mission — each topic's own Prerequisites section states exactly what
it assumes.

## Rescue applications

[Rescue mission projects](course/hackathon.md) — worked examples that
combine several topics into one autonomous task (crossing an area,
finding a target, an optional pick-and-place extension). These are
technical worked examples, not a scored or scheduled event.

## How to read this site

**Topic pages** explain shared fundamentals once, in general terms.

**Platform pages** carry only what is specific to ALeRT's own systems —
Spot startup, manipulator control, simulation launch files — and link back
to the shared explanation instead of repeating it.

Every topic is marked with a difficulty level:

{{ core }} foundational &nbsp;
{{ optional }} intermediate &nbsp;
{{ advanced }} advanced, for later reading

and, where a claim is about ALeRT's own systems specifically, a
verification status — Documented, Simulation verified, Hardware verified,
Hardware verification required, Experimental, or Historical — rather than
a badge implying it applies to every team.

This site runs on one fixed toolchain — Ubuntu 22.04 LTS and ROS 2
Humble — unless a specific ALeRT repository is documented to need
something else. See [Supported environment](reference/compatibility.md)
for the exact versions and how to check them on your own machine.

```{toctree}
:hidden:
:maxdepth: 2
:caption: Getting started

prerequisites/index
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: Topics

course/index
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: Platforms

platforms/index
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: Reference

reference/index
```
