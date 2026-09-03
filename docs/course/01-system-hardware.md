# 1. Hardware Design with KiCad and Fusion

{{ common }}

## Module overview

A robot is a physical machine before it is any software. This module
covers how that machine's design is actually captured and communicated:
an **electrical schematic**, drawn in KiCad, and a **mechanical CAD
model**, built in Autodesk Fusion.

**The problem it solves**: "what powers what" and "how is this part
actually shaped and mounted" are questions a block diagram or a verbal
description cannot answer precisely enough to build or debug real
hardware from. A schematic and a CAD model are the two documents a team
actually works from.

**Where it sits in the system**: this module is self-contained — the two
tutorials teach general electrical and mechanical design skills that
apply to any robot project, not a specific ROS 2 subsystem covered later
in the course.

**Needs**: nothing. This is the one module with no software prerequisite.

**Leads into**: KiCad and Fusion produce the electrical and mechanical
design a real robot is built from; [module 2](02-ros2.md) is where the
course turns to the software that runs on top of that hardware.

## Learning objectives

By the end of this module you can:

1. explain why an electrical schematic and a mechanical CAD model are
   each needed, and what question each one answers;
2. read and draw a KiCad electrical schematic — symbols, wiring, net
   labels — and run an Electrical Rules Check;
3. build a fully-constrained, parametric mechanical part in Fusion, where
   changing a named parameter updates the part without rebuilding it;
4. export both a schematic and a CAD model in a form someone else can
   actually use.

## How the complete system fits together

An electrical schematic and a mechanical CAD model describe the same
physical robot from two different, complementary angles. The schematic
answers "what is wired to what, and at what voltage" — power rails,
signal nets, connectors, the emergency-stop path. The CAD model answers
"what shape is this part, and how is it mounted" — a sensor bracket's
dimensions, its mounting holes, its clearance against everything around
it. Neither replaces the other: a correct schematic can still describe a
part that does not physically fit, and a correct mechanical design can
still wire a sensor to the wrong voltage.

KiCad and Fusion are the two tools this module uses to produce each of
those documents. [The KiCad tutorial](01-hardware/kicad-schematic.md)
covers the electrical side; [the Fusion
tutorial](01-hardware/fusion-mechanical-design.md) covers the mechanical
side.

## How ALeRT uses this topic

{{ alert }} {{ documented }}

Spot's electrical and mechanical design decisions are documented on the
[platform page](../platforms/alert-spot.md) at the level of stated
component choices — a full internal schematic or CAD model for the
production Spot platform is not published as part of this course.
**Verification status**: {{ documented }} via the platform page.

## How Carologistics uses this topic

{{ carologistics }} {{ documented }}

Robotino's hardware is documented on the [platform
page](../platforms/carologistics-robotino.md) at the same level — stated
components and a hardware table, not a published internal schematic or
CAD model. **Verification status**: {{ documented }} via the platform
page's hardware table.

## ALeRT and Carologistics compared

```{list-table}
:header-rows: 1
:widths: 22 26 26 26

* - Aspect
  - ALeRT / Spot
  - Carologistics / Robotino
  - Shared principle
* - Published internal schematic/CAD
  - {{ unverified }} — not published as part of this course
  - {{ unverified }} — not published as part of this course
  - Both teams work from real electrical and mechanical design documents;
    this module teaches the tools, not the teams' own files
* - Design tools
  - {{ unverified }} — not documented on the platform page
  - {{ unverified }} — not documented on the platform page
  - This module's KiCad/Fusion exercises use invented example values, not
    either team's real design
```

## Core learning path

```text
1. KiCad: schematics for robotic systems
2. Autodesk Fusion: mechanical robot parts
```

That is this module's roughly 80–100 minute core learning time.
**Interesting videos** and **Continue learning** are worthwhile
afterwards but not required for the core path.

## Subtopics

::::{grid} 1 1 2 2
:gutter: 2

:::{grid-item-card} KiCad: schematics for robotic systems
:link: 01-hardware/kicad-schematic
:link-type: doc

{{ core }} Turn a block diagram into a real electrical schematic —
symbols, wiring, net labels, and an Electrical Rules Check.
:::

:::{grid-item-card} Autodesk Fusion: mechanical robot parts
:link: 01-hardware/fusion-mechanical-design
:link-type: doc

{{ core }} Design a parametric mechanical part — a sensor mount — where a
dimension you change updates the whole part.
:::

:::{grid-item-card} Interesting videos
:link: 01-hardware/videos
:link-type: doc

One carefully checked video recommendation.
:::

:::{grid-item-card} Continue learning
:link: 01-hardware/continue-learning
:link-type: doc

Hierarchical schematics, custom symbols, PCB layout, sheet metal, DFAM,
STEP exchange between KiCad and Fusion, and more.
:::

::::

## Prerequisites

None. This is the one module with no software prerequisite.

## Connection to the next module

This module produced an electrical schematic and a mechanical CAD model —
what the robot's hardware actually is.
[Module 2](02-ros2.md) turns to the software that runs on top of that
hardware: nodes, topics, and a first running ROS 2 system.

## Further reading

- [KiCad documentation](https://docs.kicad.org/)
- [Autodesk Fusion help](https://help.autodesk.com/view/fusion360/ENU/)
- Platform detail: [Carologistics/Robotino](../platforms/carologistics-robotino.md) ·
  [ALeRT/Spot](../platforms/alert-spot.md) ·
  [Simulation](../platforms/simulation.md)

```{toctree}
:maxdepth: 1
:hidden:

01-hardware/kicad-schematic
01-hardware/fusion-mechanical-design
01-hardware/videos
01-hardware/continue-learning
```
