# Sense–process–act

{{ common }} {{ core }}

## What this topic is

The loop every autonomous robot runs, forever: **sense** the world,
**process** what that means, **act** on the decision, and sense again.

## Why a robot needs it

Every diagnostic question in this entire course reduces to "which stage
of this loop broke?" — a sensor not publishing, a decision never made, or
a command never reaching the motor. Learning to place a component in this
loop is learning to debug a robot.

## How it works

```{figure} ../../_static/images/diagrams/01-sensor-processing-actuator-loop.svg
:alt: A closed loop diagram showing Sensors feeding Processing, Processing commanding Actuators, Actuators changing the World, and the World being observed again by Sensors. A Battery powers all three blocks through dashed power lines, and an Emergency Stop can cut power to the Actuators directly.
:width: 100%

The sense–process–act loop: data flows in a circle (solid blue), power
branches out from the battery to every stage (dashed amber), and the
E-stop can cut actuator power independently of software (red).
```

**Sense** — LiDAR, cameras, IMU, wheel encoders, bumpers. Each produces a
stream of measurements, each with its own rate, noise and position on the
robot.

**Process** — the onboard computer turns those measurements into a
decision. This is where ROS 2 lives, and where the rest of this course
happens.

**Act** — motor controllers, grippers, arms. Commands go out, the world
changes, and the loop starts again.

:::{tip}
When something inexplicable happens on a real robot, check the battery
voltage before you read another line of code. This costs nothing and
saves hours.
:::

## Sensors, actuators and drives

The computer never talks to a motor directly. A motor controller sits in
between, closing a fast control loop that a general-purpose computer
cannot guarantee. Drive geometry differs by platform: **differential
drive** must turn before it can move sideways; **omnidirectional** drive
(Robotino) can translate in any direction while rotating; **legged**
locomotion (Spot) can cross terrain wheels cannot.

## Computing and microcontrollers

A general-purpose computer (Linux, ROS 2, no timing guarantee) handles
perception and decisions. A microcontroller (no OS, but a guaranteed
timing deadline) handles anything that must happen at an exact moment —
closing a motor loop, reading an encoder.

## Communication interfaces and networking

Onboard, wired (Ethernet, USB, serial). Off-board, wireless — and Wi-Fi
is the weakest, most shared, lowest-bandwidth link in the whole system.
[Module 8](../08-integration.md) and the
[networking prerequisite](../../prerequisites/networking.md) come back
to this; [Continue learning](continue-learning.md) covers CAN, UART and
I²C in more depth.

## Power supply and energy budgeting

One battery, several DC-DC converters, one distribution network. A
sagging battery produces symptoms that look exactly like software bugs —
a sensor drops off the bus, the computer reboots mid-run. See
[Continue learning](continue-learning.md) for actually budgeting one.

## Safety and emergency stops

Layered: a physical **E-stop** that cuts motor power independently of
software; **software limits** on speed and acceleration; **reflexes** in
firmware (stop at a cliff, stop on contact) that act before any planner
gets a say.

## Two robots, one architecture

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
[Carologistics/Robotino](../../platforms/carologistics-robotino.md) and
[ALeRT/Spot](../../platforms/alert-spot.md) — not here. This module is
about the architecture both robots share.

## Try it yourself

Before drawing your own diagram (in
[the practical exercise](practical-exercise.md)), walk through the loop
above end to end on a robot you have access to (real or simulated),
naming every part you find as **sense**, **process** or **act**:

1. Point to a sensor. What does it measure, and how often does it
   publish?
2. Trace the wire or wireless link from that sensor to the onboard
   computer. Is it the same physical path every other sensor uses, or a
   separate one?
3. Find the onboard computer and, if the platform has one, the
   microcontroller. Which loop above runs on which?
4. Point to an actuator. Trace the command path back from the computer to
   it.
5. Find the E-stop. Confirm — without pressing it — which of the paths you
   just traced it would cut.

If you have no robot available, do the same walk-through using the
diagram above and the [platform hardware pages](../../platforms/index.md)
instead of a physical machine — the reasoning is identical either way.

## Expected result

You can point to at least one real (or documented) example of each of
sense, process, act, power and safety on your chosen robot.

## Verification

Ask yourself, for each component you pointed to: if this failed silently
right now, what would the robot appear to be doing wrong? If you cannot
answer, you have not actually placed it in the loop yet.

## Common problems

- **Treating the microcontroller as a detail** — whether a loop runs on
  the microcontroller or the onboard computer decides whether it is
  real-time.
- **Skipping the network** — a laptop running RViz over Wi-Fi is part of
  the data path, not an outside observer.

## Next subtopic

[KiCad: schematics for robotic systems](kicad-schematic.md) — turn this
block diagram into a real electrical schematic; or skip straight to
[the practical exercise](practical-exercise.md) if schematics are not
your immediate goal.

## Sources

- [RoboCup Logistics League](https://ll.robocup.org/) {{ carologistics }}
- [RoboCup Rescue League](https://rescuesim.robocup.org/) {{ alert }}
