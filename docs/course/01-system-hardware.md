# 1. System Architecture and Robot Hardware

{{ common }}

## Module overview

Before any software makes sense, you need a picture of the machine it
runs on. This module is about that picture: what an autonomous robot is
made of, how the parts connect, and why the software is structured the
way it is.

**The problem it solves**: without a shared picture of sense/process/act,
every later module's terminology ("this node processes that sensor's
data and commands this actuator") has nothing to attach to.

**Where it sits in the system**: everywhere, structurally — this module
does not teach one subsystem, it teaches the *shape* every subsystem in
every later module fits into.

**Needs**: nothing. This is the one module with no software prerequisite
— [module 2](02-ros2.md) is where the
[prerequisites](../prerequisites/index.md) start to matter.

**Leads into**: every later module. [Module 2](02-ros2.md) turns this
module's boxes into running nodes; the KiCad and Fusion pages here turn
the same boxes into a real electrical and mechanical design.

## Learning objectives

By the end of this module you can:

1. describe the sense–process–act loop and place any robot component in
   it;
2. read a robot's power and data topology and say what fails if one link
   breaks;
3. compare a wheeled robot and a legged robot using the same
   architecture;
4. draw and defend your own system diagram of a robot you have access to,
   or one you only have a description of.

## How the complete system fits together

```{figure} ../_static/images/diagrams/01-sensor-processing-actuator-loop.svg
:alt: A closed loop diagram showing Sensors feeding Processing, Processing commanding Actuators, Actuators changing the World, and the World being observed again by Sensors. A Battery powers all three blocks through dashed power lines, and an Emergency Stop can cut power to the Actuators directly.
:width: 100%

The sense–process–act loop: data flows in a circle (solid blue), power
branches out from the battery to every stage (dashed amber), and the
E-stop can cut actuator power independently of software (red).
```

Every autonomous robot, from a vacuum cleaner to a Mars rover, runs the
same loop over and over: **sense** (LiDAR, cameras, IMU, encoders) feeds
**process** (the onboard computer — where ROS 2 lives, and where the rest
of this course happens), which commands **act** (motor controllers,
grippers, arms), which changes the world, which is sensed again. Power
branches to every stage from one battery; a physical E-stop can cut
actuator power independently of any of it. See
[Sense–process–act](01-hardware/sense-process-act.md) for the full
explanation, including drive types, compute, networking and safety.

## How ALeRT uses this topic

{{ alert }} {{ documented }}

Spot is a quadruped: legs instead of wheels, because the RoboCup Rescue
League's terrain (rubble, stairs, uneven ground) has no other answer. Its
main range sensor is a 3D LiDAR rather than a 2D scanner, because the
environment has vertical structure a flat scan cannot represent. See the
[platform page](../platforms/alert-spot.md) for the full hardware list.
**Typical team task**: confirming which of Spot's own onboard sensors and
which of the workstation-side tools (RViz, `rqt`) a given exercise
actually needs, since Spot itself is not the only compute involved.
**Verification status**: {{ documented }} via the platform page and the
team's own repository.

## How Carologistics uses this topic

{{ carologistics }} {{ documented }}

Robotino is a wheeled, **omnidirectional** platform: it can translate in
any direction while rotating, because the RoboCup Logistics League's
factory floor rewards millimetre-precise docking over rough-terrain
capability. Its main range sensors are two 2D SICK TiM571 laser
scanners, merged into one by the `laser_scan_integrator` node — see the
[platform page](../platforms/carologistics-robotino.md#hardware) for the
full component list. **Typical team task**: checking the omnidirectional
drive's actual degrees of freedom are being used by whichever Nav2
controller is configured, since a controller written for differential
drive silently ignores the lateral degree of freedom. **Verification
status**: {{ documented }} via the platform page's hardware table.

## ALeRT and Carologistics compared

```{list-table}
:header-rows: 1
:widths: 22 26 26 26

* - Aspect
  - ALeRT / Spot
  - Carologistics / Robotino
  - Shared principle
* - Drive
  - Quadruped, legged
  - Wheeled, omnidirectional
  - Both are answers to their own competition's terrain
* - Main range sensor
  - 3D LiDAR
  - Two merged 2D laser scanners
  - Both need a documented sensor mount and TF frame
* - What the drive is shaped by
  - Traversing terrain, reaching into gaps
  - Precision docking, repeatability
  - Neither is "better"; both answer different questions
* - Manipulation
  - An arm, for the Dexterity competition category
  - A custom stepper-driven gripper
  - Both separate locomotion from manipulation hardware
```

See [Sense–process–act's own comparison
table](01-hardware/sense-process-act.md#two-robots-one-architecture) for
the sensor/drive/environment breakdown this table summarises.

## Core learning path

```text
1. Sense–process–act
2. Practical hardware exercise
```

That is this module's roughly 80–100 minute core learning time. KiCad,
Fusion, **Interesting videos** and **Continue learning** are worthwhile
afterwards but not required for the core path.

## Subtopics

::::{grid} 1 1 2 2
:gutter: 2

:::{grid-item-card} Sense–process–act
:link: 01-hardware/sense-process-act
:link-type: doc

{{ core }} The loop, drive/power/compute/network/safety, and the
Robotino-vs-Spot comparison.
:::

:::{grid-item-card} Practical hardware exercise
:link: 01-hardware/practical-exercise
:link-type: doc

{{ core }} This module's practical task: draw your own system diagram,
plus this module's Try it on Spot section.
:::

:::{grid-item-card} KiCad: schematics for robotic systems
:link: 01-hardware/kicad-schematic
:link-type: doc

{{ optional }} Turn a block diagram into a real electrical schematic —
symbols, wiring, net labels, and an Electrical Rules Check.
:::

:::{grid-item-card} Autodesk Fusion: mechanical robot parts
:link: 01-hardware/fusion-mechanical-design
:link-type: doc

{{ optional }} Design a parametric mechanical part — a sensor mount —
where a dimension you change updates the whole part.
:::

:::{grid-item-card} Interesting videos
:link: 01-hardware/videos
:link-type: doc

One carefully checked video recommendation.
:::

:::{grid-item-card} Continue learning
:link: 01-hardware/continue-learning
:link-type: doc

Choosing sensors and actuators, power budgeting, communication
interfaces, fuses and wire sizing, diagnostics, hardware-in-the-loop.
:::

::::

## Prerequisites

None. This is the one module with no software prerequisite.

## Connection to the next module

This module produced a diagram of boxes and arrows.
[Module 2](02-ros2.md) turns them into running software: the boxes become
**nodes**, the arrows become **topics**, and you start, inspect and modify a
real ROS 2 system.

## Further reading

- [ROS 2 concepts](https://docs.ros.org/en/humble/Concepts.html) — the
  software side of what you just drew
- [RoboCup Logistics League](https://ll.robocup.org/) {{ carologistics }}
- [RoboCup Rescue League](https://rescuesim.robocup.org/) {{ alert }}
- Platform detail: [Carologistics/Robotino](../platforms/carologistics-robotino.md) ·
  [ALeRT/Spot](../platforms/alert-spot.md) ·
  [Simulation](../platforms/simulation.md)

```{toctree}
:maxdepth: 1
:hidden:

01-hardware/sense-process-act
01-hardware/practical-exercise
01-hardware/kicad-schematic
01-hardware/fusion-mechanical-design
01-hardware/videos
01-hardware/continue-learning
```
