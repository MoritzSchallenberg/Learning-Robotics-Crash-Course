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

### From block diagram to real design

{{ optional }}

The diagram you will draw in this module's practical task is a starting
point, not the finished design. Two companion pages take one step further,
each with its own hands-on practical task:

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} KiCad: schematics for robotic systems
:link: 01-hardware/kicad-schematic
:link-type: doc

Turn a block diagram into a real electrical schematic — symbols, wiring,
net labels, and an Electrical Rules Check.
:::

:::{grid-item-card} Autodesk Fusion: mechanical robot parts
:link: 01-hardware/fusion-mechanical-design
:link-type: doc

Design a parametric mechanical part — a sensor mount — where a dimension
you change updates the whole part.
:::

::::

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

## Continue learning

Each topic below is a real next step, not just a keyword. Two of them —
KiCad and Fusion — are full pages with their own practical task, linked
above; the rest are dropdowns here.

:::{dropdown} Choosing sensors and actuators — Next step
:icon: light-bulb

**What it is.** Picking a specific sensor or actuator for a task, based on
its actual specifications — range, field of view, update rate, current
draw — rather than "the one the last team used".

**Why it matters.** The sense–process–act loop above tells you a stage
needs a sensor; it does not tell you *which* one. A LiDAR with too narrow a
field of view, or a motor that cannot supply enough torque at the robot's
target speed, produces a system that "should" work and does not.

**Needs.** This module's core concepts.

**Try it.** Pick one sensor and one actuator from a platform page
([Carologistics/Robotino](../platforms/carologistics-robotino.md) or
[ALeRT/Spot](../platforms/alert-spot.md)) and write down, from its
datasheet, the one specification that most limits what the robot can do
with it.

**Check.** You can name the limiting number (not just the part name) and
explain, in one sentence, what breaks if that number is exceeded.

**Read more.** [ROS 2 hardware
integration](https://docs.ros.org/en/humble/) — start from a driver
package's README for the sensor family you picked.
:::

:::{dropdown} Power and battery budgeting — Next step
:icon: light-bulb

**What it is.** Adding up every component's current draw at its supply
voltage to get a total power budget, then dividing battery capacity by that
total to estimate runtime.

**Why it matters.** "The battery died mid-run" is one of the most common,
most avoidable robot failures, and it is arithmetic, not guesswork — a
computer, a LiDAR, and two motors under load draw a very predictable
current.

**Needs.** This module's "Drive, power, compute, network, safety" section.

**Try it.** For a platform page's listed components, estimate each
component's typical current draw (from its datasheet or a reasonable
published figure), sum them at each voltage rail, and divide a plausible
battery capacity (Wh) by the total power (W) to get an estimated runtime in
hours.

**Check.** Your estimate is within a sensible order of magnitude of what
the platform page or team documentation states, and you can show the
arithmetic that got you there.

**Read more.** {{ unverified }} — battery chemistry and exact runtime
depend on the specific pack; treat any number here as an estimate to verify
against the real hardware, not a guarantee.
:::

:::{dropdown} Communication interfaces: CAN, Ethernet, USB, UART, I²C — Intermediate
:icon: light-bulb

**What it is.** The wired links that connect a robot's parts, each suited
to a different job:

```{list-table}
:header-rows: 1
:widths: 14 30 28 28

* - Interface
  - Typical use
  - Distance / speed
  - Multi-device?
* - CAN
  - Motor controllers, distributed real-time control
  - Long runs, robust to noise, moderate speed
  - Yes, natively (multi-drop bus)
* - Ethernet
  - Onboard computer ↔ sensors (cameras, some LiDAR)
  - Fast, network-based
  - Yes, via switches
* - USB
  - Onboard computer ↔ a nearby sensor or microcontroller
  - Short runs, high speed
  - One host, several devices (hub)
* - UART
  - Microcontroller ↔ computer, simple point-to-point
  - Short runs, low-to-moderate speed
  - No (point-to-point)
* - I²C
  - Microcontroller ↔ nearby small sensors/ICs on one board
  - Very short runs, low speed
  - Yes, natively (addressed bus)
```

**Why it matters.** Picking the wrong interface for a job — I²C across a
robot chassis, for instance — produces exactly the kind of noise-sensitive,
intermittent fault that looks like a software bug.

**Needs.** This module's "Onboard compute" paragraph.

**Try it.** For each interface above, name one component from a platform
page that plausibly uses it, based on the interface's characteristics.

**Check.** Your four choices are each defensible from the table above, not
guessed.

**Read more.** [ROS 2 hardware driver
packages](https://docs.ros.org/en/humble/) typically state which interface
they expect in their own README.
:::

:::{dropdown} Fuses, wire sizing and a hardware BOM — Intermediate
:icon: light-bulb

**What it is.** Sizing a fuse and its wire to the actual current a circuit
carries (a fuse rated too high protects nothing; a wire too thin for its
current overheats), and keeping a **bill of materials (BOM)** — every part,
its value, and its source — as the design's single source of truth.

**Why it matters.** This is the mechanical/electrical equivalent of
[module 8's](08-integration.md#core-concepts) "one command, one source of
truth" for software configuration — a design that lives only in one
person's head, or an out-of-date drawing, fails the same way undocumented
config does.

**Needs.** The power-budgeting topic above, and (optionally) the
[KiCad tutorial](01-hardware/kicad-schematic.md).

**Try it.** For one supply rail from your power-budgeting exercise, look up
a wire-gauge-vs-current table and state the minimum wire gauge for that
current, then pick a fuse rated between the normal operating current and
the wire's maximum.

**Check.** Your fuse rating is higher than normal operating current but
lower than what the wire can safely carry — if either is not true, the
choice is wrong.

**Read more.** [KiCad tutorial: fuses and a safe-stop
path](01-hardware/kicad-schematic.md#core-concepts-in-the-editor) covers how
to represent this in a schematic.
:::

:::{dropdown} Diagnostics: adding measurement points — Intermediate
:icon: light-bulb

**What it is.** Deliberately designing in places to measure a signal or
voltage — a test point, an accessible connector, a status LED — rather than
discovering after the fact that nothing is probeable without desoldering
something.

**Why it matters.** [Module 8's](08-integration.md#core-concepts)
eight-step diagnostic procedure assumes you *can* check each layer;
hardware with no measurement points makes step 1 ("is it powered?")
surprisingly hard to answer.

**Needs.** This module's "Power" paragraph.

**Try it.** Pick one power rail from your practical task's diagram and
name one concrete, physical way you could check its voltage without
disassembling anything.

**Check.** Your answer names an actual accessible point (a connector pin, a
test pad), not just "measure it somehow".

**Read more.** [Module 8: the eight-step diagnostic
procedure](08-integration.md#core-concepts)
:::

:::{dropdown} Hardware-in-the-loop testing — Advanced
:icon: light-bulb

**What it is.** Running real control software against real electronics
(a motor controller, a sensor board) while the rest of the system —
physics, other sensors — stays simulated. A middle ground between pure
simulation and a full physical robot.

**Why it matters.** It catches integration bugs between real hardware and
your software that pure simulation cannot see, without needing the whole
robot assembled.

**Needs.** A working simulation setup ([module 8's simulation
notes](08-integration.md#optional-extensions)) and access to at least one
piece of real hardware (a motor controller or sensor board).

**Try it.** {{ unverified }} — describe, on paper, how you would connect
one real component (e.g. a motor controller) to your simulated robot's
command topic, and what you would need to fake on the simulation side for
that to work.

**Check.** Your plan identifies exactly which signal crosses from
simulated to real hardware, and in which direction.

**Read more.** [ROS 2 and hardware
interfaces](https://docs.ros.org/en/humble/) — search for `ros2_control`,
the standard ROS 2 hardware-abstraction framework.
:::

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
:hidden:
:maxdepth: 1

01-hardware/kicad-schematic
01-hardware/fusion-mechanical-design
```
