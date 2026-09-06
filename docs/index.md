# ALeRT Advanced Robotics Tutorial

A technical reference and tutorial site for **ALeRT** (Aachen Legged
Rescue Team), the RoboCup Rescue League team at the **MASKOR Institute,
FH Aachen**. It explains the robotics, ROS 2 and ALeRT-specific systems
this team's software is built on, for anyone who wants to understand or
extend it.

<a class="lrcc-cta" href="ros2/index.html">Browse the topics →</a>

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
go smoothly. See [Getting Started](getting-started/index.md).
:::

## Topics

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} Getting Started
:link: getting-started/index
:link-type: doc

Linux and the terminal, Git, networking, and ROS 2 installation.
:::

:::{grid-item-card} ROS 2
:link: ros2/index
:link-type: doc

Nodes, topics, services, parameters, actions, launch files, `colcon` —
the middleware everything else runs on.
:::

:::{grid-item-card} ALeRT Platforms and Safety
:link: platforms/index
:link-type: doc

Spot, its manipulator, hardware design (KiCad, Fusion), system
architecture, and safe start/stop procedures.
:::

:::{grid-item-card} Simulation
:link: simulation/index
:link-type: doc

Webots, the ALeRT Spot simulation, simulation time, and the difference
between simulation and hardware.
:::

:::{grid-item-card} Sensors and Coordinate Frames
:link: sensors-frames/index
:link-type: doc

Cameras, LiDAR, IMU, TF2, static and dynamic transforms.
:::

:::{grid-item-card} Perception
:link: perception/index
:link-type: doc

Camera calibration, OpenCV, ArUco/AprilTag, YOLO, data labeling.
:::

:::{grid-item-card} Mapping and World Models
:link: mapping-world-models/index
:link-type: doc

Occupancy grids, SLAM Toolbox, 3D mapping, saving and loading maps.
:::

:::{grid-item-card} Localization, Navigation and Exploration
:link: navigation-exploration/index
:link-type: doc

AMCL, Nav2, costmaps, planners, controllers, recovery behavior.
:::

:::{grid-item-card} Robot Manipulation
:link: manipulation/index
:link-type: doc

Arm fundamentals, MoveIt 2, planning scenes, grippers, perception-to-grasp.
:::

:::{grid-item-card} Autonomous Decision-Making
:link: decision-making/index
:link-type: doc

State machines, behavior trees, RAFCON, PlanSys2, Golog++.
:::

:::{grid-item-card} Integration, Diagnostics and Testing
:link: integration-testing/index
:link-type: doc

Startup order, configuration, logging, rosbags, systematic debugging.
:::

:::{grid-item-card} Rescue Applications and Projects
:link: rescue-projects/index
:link-type: doc

Worked examples that combine several topics into one autonomous mission.
:::

:::{grid-item-card} Reference
:link: reference/index
:link-type: doc

Cheat sheet, supported environment, glossary.
:::

::::

Topics build on each other where a real dependency exists — transforms
are needed before mapping, mapping before navigation, navigation before a
full mission — each topic's own Prerequisites section states exactly what
it assumes, so you can start wherever your own knowledge runs out.

## How to read this site

**Topic pages** explain shared fundamentals once, in general terms.

**Platform pages** carry only what is specific to ALeRT's own systems —
Spot startup, manipulator control, simulation launch files — and link back
to the shared explanation instead of repeating it.

Every topic is marked with a difficulty level:

{{ foundation }} foundational &nbsp;
{{ intermediate }} intermediate &nbsp;
{{ advanced }} advanced &nbsp;
{{ research }} research / experimental

and, where a claim is about ALeRT's own systems specifically, a
verification status:

{{ documented }} confirmed via a repository or written documentation
&nbsp;
{{ simulation }} runs in Webots &nbsp;
{{ hardwareverified }} actually checked on running hardware &nbsp;
{{ unverified }} plausible, not checked &nbsp;
{{ historical }} no longer current, kept for context

rather than a badge implying a claim applies to every team or every
robot.

This site runs on one fixed toolchain — Ubuntu 22.04 LTS and ROS 2
Humble — unless a specific ALeRT repository is documented to need
something else. See [Supported environment](reference/compatibility.md)
for the exact versions and how to check them on your own machine.

```{toctree}
:hidden:
:maxdepth: 2
:caption: Getting Started

getting-started/index
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: ROS 2

ros2/index
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: ALeRT Platforms and Safety

platforms/index
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: Simulation

simulation/index
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: Sensors and Coordinate Frames

sensors-frames/index
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: Perception

perception/index
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: Mapping and World Models

mapping-world-models/index
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: Localization, Navigation and Exploration

navigation-exploration/index
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: Robot Manipulation

manipulation/index
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: Autonomous Decision-Making

decision-making/index
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: Integration, Diagnostics and Testing

integration-testing/index
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: Rescue Applications and Projects

rescue-projects/index
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: Reference

reference/index
```
