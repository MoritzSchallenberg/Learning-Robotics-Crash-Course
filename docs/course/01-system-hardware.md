# 1. System Architecture and Robot Hardware

{{ common }}

Before any software makes sense, you need a picture of the machine it runs
on. This module is about that picture: what an autonomous robot is made of,
how the parts connect, and why the software is structured the way it is.

## Overview

You will learn the sense–process–act loop that every autonomous robot runs,
and use it to read any robot's power and data topology — real or described.
The module ends with you producing your own system diagram of a robot,
distinguishing data flow, power flow and the safety chain.

## Learning objectives

By the end of this module you can:

1. describe the sense–process–act loop and place any robot component in it;
2. read a robot's power and data topology and say what fails if one link
   breaks;
3. compare a wheeled robot and a legged robot using the same architecture.

## Prerequisites

None. This is the one module with no software prerequisite —
[module 2](02-ros2.md) is where the [prerequisites](../prerequisites/index.md)
start to matter.

## Core concepts

### The sense–process–act loop

Every autonomous robot, from a vacuum cleaner to a Mars rover, runs the same
loop over and over:

```{figure} ../_static/images/diagrams/01-sensor-processing-actuator-loop.svg
:alt: A closed loop diagram showing Sensors feeding Processing, Processing commanding Actuators, Actuators changing the World, and the World being observed again by Sensors. A Battery powers all three blocks through dashed power lines, and an Emergency Stop can cut power to the Actuators directly.
:width: 100%

The sense–process–act loop: data flows in a circle (solid blue), power
branches out from the battery to every stage (dashed amber), and the E-stop
can cut actuator power independently of software (red).
```

**Sense** — LiDAR, cameras, IMU, wheel encoders, bumpers. Each produces a
stream of measurements, each with its own rate, noise and position on the
robot.

**Process** — the onboard computer turns those measurements into a decision.
This is where ROS 2 lives, and where the rest of this course happens.

**Act** — motor controllers, grippers, arms. Commands go out, the world
changes, and the loop starts again.

When something misbehaves later in this course, your first diagnostic
question is always: *which stage of the loop broke?*

### Drive, power, compute, network, safety — in one paragraph each

**Drive and motor controllers.** The computer never talks to a motor
directly. A motor controller sits in between, closing a fast control loop
that a general-purpose computer cannot guarantee. Drive geometry differs by
platform: **differential drive** must turn before it can move sideways;
**omnidirectional** drive (Robotino) can translate in any direction while
rotating; **legged** locomotion (Spot) can cross terrain wheels cannot.

**Power.** One battery, several DC-DC converters, one distribution network.
A sagging battery produces symptoms that look exactly like software bugs —
a sensor drops off the bus, the computer reboots mid-run.

**Onboard compute.** A general-purpose computer (Linux, ROS 2, no timing
guarantee) handles perception and decisions. A microcontroller (no OS, but a
guaranteed timing deadline) handles anything that must happen at an exact
moment — closing a motor loop, reading an encoder.

**Network.** Onboard, wired (Ethernet, USB, serial). Off-board, wireless —
and Wi-Fi is the weakest, most shared, lowest-bandwidth link in the whole
system. [Module 8](08-integration.md) and the
[networking prerequisite](../prerequisites/networking.md) come back to this.

**Safety.** Layered: a physical **E-stop** that cuts motor power
independently of software; **software limits** on speed and acceleration;
**reflexes** in firmware (stop at a cliff, stop on contact) that act before
any planner gets a say.

:::{tip}
When something inexplicable happens on a real robot, check the battery
voltage before you read another line of code. This costs nothing and saves
hours.
:::

### Two robots, one architecture

{{ platformspecific }}

```{list-table}
:header-rows: 1
:widths: 22 39 39

* - Aspect
  - Robotino {{ carologistics }}
  - Spot {{ alert }}
* - Drive
  - Wheeled, omnidirectional
  - Quadruped, legged
* - Moves over
  - Flat industrial floors
  - Rubble, steps, uneven terrain
* - Main range sensor
  - 2D laser scanners
  - 3D LiDAR
* - Shaped by
  - Precision docking, repeatability
  - Traversing terrain, reaching into gaps
```

Detailed component lists live on the platform pages —
[Carologistics/Robotino](../platforms/carologistics-robotino.md) and
[ALeRT/Spot](../platforms/alert-spot.md) — not here. This module is about the
architecture both robots share.

## Guided example

Before drawing your own diagram, walk through the loop above end to end on
a robot you have access to (real or simulated), naming every part you find
as **sense**, **process** or **act**:

1. Point to a sensor. What does it measure, and how often does it publish?
2. Trace the wire or wireless link from that sensor to the onboard
   computer. Is it the same physical path every other sensor uses, or a
   separate one?
3. Find the onboard computer and, if the platform has one, the
   microcontroller. Which loop below runs on which?
4. Point to an actuator. Trace the command path back from the computer to
   it.
5. Find the E-stop. Confirm — without pressing it — which of the paths you
   just traced it would cut.

If you have no robot available, do the same walk-through using the diagram
above and the [platform hardware pages](../platforms/index.md) instead of a
physical machine — the reasoning is identical either way.

## Practical task

### Goal
Produce one system diagram — on paper or in any drawing tool — that traces a
sensor reading from the sensor to the onboard computer, and a command from
the computer back out to an actuator, with power and safety shown
separately.

### Starting point
A real robot if you have access to one; otherwise the diagram above plus
the relevant [platform hardware page](../platforms/index.md) as your
component description.

### Steps
1. List every component you can find (aim for at least eight).
2. Sort each into **sense**, **process**, or **act**.
3. Draw them as boxes.
4. Draw **data** arrows (solid, blue) between boxes that exchange
   information.
5. Draw **power** arrows (dashed, amber) from the battery to every box that
   needs it.
6. Mark the **E-stop** and what it cuts (red).
7. Pick three components; for each, write one sentence: *if this fails
   silently, what would the robot appear to be doing wrong?*

## Expected result

A diagram with three visually distinct arrow types that someone who has
never seen the robot could follow, plus three short failure sentences from
step 7.

## Verification

Look at your diagram fresh, or hand it to someone else without explaining
it first: can they name, just from the diagram, which arrow is data and
which is power, and what the E-stop cuts? If not, add a legend and revise —
that is the actual skill this task teaches. For each of the three failure
sentences from step 7, check that the sentence describes an *observable
symptom* ("the robot stops responding to commands"), not just a repeat of
the component name.

## Common problems

- **Data and power drawn as the same arrow style** — the two most common
  debugging questions ("is data flowing?" vs "is it powered?") become
  impossible to separate. Use two visibly different line styles.
- **Forgetting the network** — a laptop running RViz over Wi-Fi is part of
  the data path, not an outside observer.
- **Treating the microcontroller as a detail** — whether a loop runs on the
  microcontroller or the onboard computer decides whether it is real-time.
- **Drawing data flow and power as the same arrows.** They follow different
  paths; conflating them makes the diagram useless for debugging.
- **Skipping the network.** Anything connected over Wi-Fi is part of the
  system, not outside it.

## Optional extensions

{{ optional }}

Pick one failure sentence from your practical task's step 7 and write the
exact terminal command or observation that would confirm it — you will not
be able to run it until [module 2](02-ros2.md), but reasoning about it
correctly here is a good sign for [module 8](08-integration.md).

No robot available at all? Build the diagram from the
[Webots](../platforms/simulation.md) robot model description instead of a
physical robot — the loop and the component categories are identical; only
"battery" becomes "simulated power", which is worth noting as a limitation
of simulation in its own right.

## Advanced topics

{{ advanced }}

:::{dropdown} Encoders, IMU and drive kinematics in detail
:icon: light-bulb

**Encoders** measure motor rotation; combined with drive geometry they give
**odometry** — accurate over a few metres, unreliable after a few minutes,
because small errors accumulate and are never corrected. Module 5 explains
why that matters.

**IMU** measures acceleration and angular velocity directly, which is more
responsive than deriving orientation from wheels, and keeps working when
wheels slip. It drifts too, in a different way — which is why the two are
usually fused rather than trusted alone.

**Drive kinematics** is the mapping between wheel speeds and robot velocity.
For differential drive it's two numbers (left, right wheel speed); for
omnidirectional drive it's three degrees of freedom (x, y, rotation) from
however many wheels the platform has (Robotino uses three or four
omni-wheels).
:::

:::{dropdown} Why RoboCup shapes the hardware
:icon: light-bulb

The RoboCup Logistics League happens on a flat factory floor where a robot
must dock to a machine within millimetres — so Robotino is omnidirectional
and built around precise short-range sensing. The RoboCup Rescue League
happens in a collapsed-building scenario where wheels do not work at all —
so Spot has legs and 3D perception. Neither is "better"; both are answers to
different competition questions.
:::

## Connection to the next module

This module produced a diagram of boxes and arrows.
[Module 2](02-ros2.md) turns them into running software: the boxes become
**nodes**, the arrows become **topics**, and you start, inspect and modify a
real ROS 2 system.

## Further reading

- [ROS 2 concepts](https://docs.ros.org/en/jazzy/Concepts.html) — the
  software side of what you just drew
- [RoboCup Logistics League](https://ll.robocup.org/) {{ carologistics }}
- [RoboCup Rescue League](https://rescuesim.robocup.org/) {{ alert }}
- Platform detail: [Carologistics/Robotino](../platforms/carologistics-robotino.md) ·
  [ALeRT/Spot](../platforms/alert-spot.md) ·
  [Simulation](../platforms/simulation.md)
