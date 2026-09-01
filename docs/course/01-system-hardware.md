# 1. System Architecture and Robot Hardware

:::{admonition} Session 1
:class: note

Monday, 05 October 2026, 17:35 – 19:00
:::

{{ common }}

Before any software makes sense, you need a picture of the machine it runs on.
This evening is about that picture: what an autonomous robot is made of, how
the parts connect, and why the software is structured the way it is.

## Learning objectives

After this session you can:

- describe the sense–think–act chain and place any component into it;
- explain what a motor controller, an encoder and an IMU each contribute;
- read a robot's power and data topology and say what fails if one link breaks;
- name the difference between an onboard computer and a microcontroller, and
  say which job belongs where;
- compare two very different robots — a wheeled Robotino and a legged Spot —
  in terms of the same architecture.

## Prerequisites

None beyond curiosity. The [prerequisites](../prerequisites/index.md) section
matters from session 2 onwards.

## The sense–think–act chain

Every autonomous robot, from a vacuum cleaner to a Mars rover, is the same loop
running over and over:

```text
   ┌──────────┐      ┌────────────────┐      ┌───────────┐
   │  SENSE   │ ───► │     THINK      │ ───► │    ACT    │
   │ sensors  │      │  computation   │      │ actuators │
   └──────────┘      └────────────────┘      └───────────┘
         ▲                                          │
         └──────────  the world changes  ◄──────────┘
```

**Sense** — LiDAR, cameras, IMU, wheel encoders, bumpers. Each produces a
stream of measurements, each with its own rate, its own noise, and its own
position on the robot.

**Think** — the onboard computer turns those measurements into an estimate of
the world and a decision about what to do. This is where ROS 2 lives, and where
almost everything in this course happens.

**Act** — motor controllers, grippers, arms. Commands go out, the world
changes, and the loop starts again.

The loop is what makes a robot a robot rather than a remote-controlled toy.
When something misbehaves, your first diagnostic question is always: *which
stage of the loop broke?*

## Components

### Drive and motor controllers

The computer does not talk to a motor directly. A **motor controller** sits in
between: it takes a target velocity, measures what the motor is actually doing,
and adjusts the current many hundreds of times a second to close the gap.

This matters for a practical reason: the control loop that keeps a wheel at the
right speed runs on the controller, at a rate a general-purpose operating
system cannot guarantee. Your ROS 2 node says "drive forward at 0.3 m/s" and
the controller works out how.

Drive geometry differs between platforms and changes what the robot can do:

```{list-table}
:header-rows: 1
:widths: 25 35 40

* - Geometry
  - Can it move sideways?
  - Example
* - Differential drive
  - No — it must turn first
  - Most two-wheeled research robots
* - Omnidirectional
  - Yes, in any direction, while rotating
  - Festo Robotino {{ carologistics }}
* - Legged
  - Yes, and over steps and rubble
  - Boston Dynamics Spot {{ alert }}
```

### Encoders

An **encoder** measures how far a motor has actually turned. Count the ticks
from both wheels, apply the geometry of the robot, and you get an estimate of
where it has travelled: this is **odometry**, and it is the foundation of
session 5.

Odometry drifts. Wheels slip, tyres compress, the floor is uneven, and every
small error is added to all previous errors and never removed. Over a few
metres it is excellent. Over a few minutes it is fiction. Correcting that drift
against a map is exactly what localization does.

### IMU

An **inertial measurement unit** measures acceleration and angular velocity.
Integrating angular velocity gives orientation, which is far more responsive
than deriving it from wheel encoders — and it keeps working when the wheels
slip. It also drifts, in its own way, which is why odometry and IMU are
normally fused rather than used alone.

### Cameras and LiDAR

A **LiDAR** sweeps a laser and measures the time until the reflection returns,
producing accurate distances to whatever surrounds the robot. A 2D LiDAR gives
a slice at one height; a 3D LiDAR gives a full point cloud. LiDAR is precise
and largely indifferent to lighting, which is why mapping and obstacle
avoidance are built on it.

A **camera** gives colour and texture — everything you need to tell *what*
something is, and nothing you need to tell *how far away* it is. Depth cameras
add distance, over a limited range.

The division of labour is the point: LiDAR tells you where things are, cameras
tell you what they are, and neither replaces the other.

### Onboard computer and microcontrollers

Two very different kinds of computer sit on a robot:

**The onboard computer** — an x86 mini-PC or a powerful ARM board running Linux
and ROS 2. It handles perception, mapping, planning and decision making. It has
plenty of memory and no timing guarantees whatsoever.

**Microcontrollers** — small, cheap, no operating system, but able to hit a
timing deadline every single cycle. They read sensors and drive motors, and
they are what you use when "usually within 10 ms" is not good enough.

The rule of thumb: anything that must happen at an exact moment goes on a
microcontroller; anything that must think goes on the onboard computer.

### Power

Power is not a footnote. It is the most common cause of behaviour that looks
like a software bug.

A robot typically has one battery, a set of DC-DC converters producing the
voltages the various components need, and a distribution network. When the
battery sags, the symptoms are wonderfully misleading: a sensor drops off the
USB bus, the computer reboots mid-run, a motor stalls under load only when the
LiDAR is also spinning.

:::{tip}
When something inexplicable happens on a real robot, check the battery voltage
before you read another line of code. This advice costs nothing and saves
hours.
:::

### Network

Onboard, components are wired over Ethernet, USB and serial buses. Off-board,
the robot talks to your laptop over Wi-Fi.

That last link is the weakest part of most robot systems: it is shared, it
drops, and it has a fraction of the bandwidth of the wired links. This is why
session 3 cares about how much data a sensor publishes, and why
[the networking page](../prerequisites/networking.md) explains republishers.

### Safety

Any robot that can move can hurt someone or destroy itself. Safety is built in
layers:

**Emergency stop** — a physical button that cuts motor power, independently of
any software. It works when the computer has crashed, which is exactly when you
need it.

**Software limits** — velocity and acceleration caps, so a bug produces a slow
mistake rather than a fast one.

**Reflexes** — reactive behaviours in firmware: stop at a cliff, stop on
bumper contact. Fast, dumb, and independent of the planning stack.

:::{danger}
E-stops are not a convenient way to stop a robot. Pressing one on a legged
robot drops it where it stands, and on a manipulator lets the arm fall
mid-motion. Use the normal shutdown path unless someone or something is
actually about to be hurt.
:::

:::{warning}
Some tutorials disable reflexes or safety overrides so that a robot will
reverse or drive faster during an exercise. Understand what you are switching
off before you switch it off, only do it in a clear space, and switch it back
on afterwards.
:::

## Two robots, one architecture

The institute runs two very different platforms. They map onto the same
architecture, which is the point of learning the architecture.

```{list-table}
:header-rows: 1
:widths: 22 39 39

* - Aspect
  - Robotino {{ carologistics }}
  - Spot {{ alert }}
* - Type
  - Wheeled, omnidirectional
  - Quadruped, legged
* - Made by
  - Festo Didactic
  - Boston Dynamics
* - Moves over
  - Flat industrial floors
  - Rubble, steps, uneven terrain
* - Main range sensor
  - 2D laser scanners
  - 3D LiDAR
* - Cameras
  - Webcam plus a global-shutter camera for manipulation
  - Multiple onboard cameras, plus a gripper camera on the arm
* - Manipulation
  - Custom gripper for factory workpieces
  - Arm with a gripper
* - Competition
  - RoboCup Logistics League
  - RoboCup Rescue League
* - The task shapes it
  - Precision docking at machines, repeatability
  - Traversing terrain, reaching into awkward places
```

Notice how much follows from the last row. The Logistics League happens on a
flat factory floor where a robot must dock to a machine within millimetres, so
Robotino is omnidirectional and its perception is built around precise
short-range measurement. The Rescue League happens in collapsed buildings where
wheels do not work at all, so Spot has legs and 3D perception.

Neither robot is better. They are answers to different questions — and both run
ROS 2, publish transforms, build maps, and navigate with the same stack you
will learn in the coming weeks.

## Task

:::{admonition} Task: map a real robot
:class: task

Work in pairs, at a robot if one is available, otherwise from your platform's
documentation.

**Part 1 — Identify the components.**

Walk the robot and list what you find. For every component, note:

- what it is;
- which stage of the sense–think–act loop it belongs to;
- what it connects to, physically;
- what stops working if it fails.

Aim for at least ten components.

**Part 2 — Draw the system diagram.**

Draw the robot as a block diagram with **two kinds of arrow**:

- **data** — which component sends information to which, and over what
  (USB, Ethernet, serial, Wi-Fi);
- **power** — what feeds what, from the battery through the converters.

Mark clearly:

- where the emergency stop cuts in;
- which links are wired and which are wireless;
- which parts run on a microcontroller and which on the onboard computer.

**Part 3 — Break it.**

Pick three components. For each, answer in one sentence: if this fails
silently, what would the robot *appear* to be doing wrong?
:::

:::{admonition} Expected result
:class: result

One diagram per pair, on paper or in any drawing tool, in which someone who has
never seen the robot can trace a LiDAR measurement from the sensor to the
onboard computer, and a velocity command from the computer back out to a wheel.

Part 3 is the one to discuss as a group: most of the interesting answers are
symptoms that look like software bugs.
:::

## Common mistakes

**Drawing data flow and power as the same arrows.**
They follow different paths, and confusing them makes the diagram useless for
debugging. Use two arrow styles.

**Forgetting the network.**
Your laptop is part of the system. If RViz runs on it, that Wi-Fi link is in
the data path.

**Treating the microcontroller as a detail.**
Whether a loop runs on the microcontroller or the onboard computer determines
whether it is real-time. That distinction explains a lot of later behaviour.

## Further reading

- [ROS 2 concepts](https://docs.ros.org/en/jazzy/Concepts.html) — the software
  side of what you drew today
- [RoboCup Logistics League](https://ll.robocup.org/) {{ carologistics }}
- [RoboCup Rescue League](https://rescuesim.robocup.org/) {{ alert }}
- Your platform track: [Carologistics/Robotino](../platforms/carologistics-robotino.md) ·
  [ALeRT/Spot](../platforms/alert-spot.md) ·
  [Simulation](../platforms/simulation.md)
