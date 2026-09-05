# Platform notes

{{ common }} {{ core }}

## What this topic is

The same seven-step mission from [The mission and
self-assessment](mission-and-checklist.md), with the specific advantages
and considerations each platform track brings to it.

## Why a robot needs it

The mission's shape is identical on every platform, but the details that
make it succeed or fail on a given robot are not — a drive system's turning
characteristics, a leg's terrain advantage, and a gripper's iteration time
all change what "reliable" actually takes to achieve.

## How it works

```{figure} ../../_static/images/diagrams/10-hackathon-arena-schematic.svg
:alt: A top-down schematic floor plan. A Start Zone sits bottom left. A dashed example route winds past two labelled obstacles and an unmapped-on-the-day area to a Target Zone top right containing a marker. An optional Drop Zone sits near the start for the transport extension.
:width: 100%

Schematic only, illustrating the shape of the mission rather than any
particular physical layout.
```

This sketch fixes the **shape** of the mission — start, obstacles, a
target area, an optional drop zone for the transport extension — so you can
build and test against something concrete regardless of where you actually
run it. Build your own version of this layout with whatever space and
obstacles you have available; the exact dimensions do not matter, only that
it exercises every step of the mission above.

### Simulation

{{ simulation }}

Run the full mission in [Webots](../../platforms/simulation.md). The mission
and the self-assessment checklist are identical; a crashed simulation can
simply be restarted from a clean state, which is one of simulation's
genuine advantages for practicing this project repeatedly.

## How ALeRT applies it

{{ alert }}

Legged locomotion is the advantage on any non-flat terrain (see the
[platform page](../../platforms/alert-spot.md)). Manipulation attempts should
budget extra iteration time — MoveIt planning failures are a normal part of
a first attempt, not a sign something is broken.

## Next subtopic

[Mission monitoring and recovery](mission-monitor.md) — an optional
development node, and what to do after an unexpected stop.
