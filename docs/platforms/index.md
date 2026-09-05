# Platform tracks

The [topic pages](../course/index.md) explain the shared fundamentals once.
These pages carry only what is specific to one system: the launch commands, the
topic names, the hardware quirks.

If a general concept is explained elsewhere on this site, these pages link to
it rather than repeating it. That is deliberate — one explanation, kept
correct in one place.

## Pick your track

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} Simulation
:link: simulation
:link-type: doc

No robot required. Webots, the ALeRT Spot simulation, reproducible tasks. The
right choice if you are learning, or if the hardware is booked.
:::

:::{grid-item-card} ALeRT / Spot
:link: alert-spot
:link-type: doc

Boston Dynamics Spot in the RoboCup Rescue League. Legged locomotion, 3D
mapping, manipulation.
:::

::::

## The tracks at a glance

```{list-table}
:header-rows: 1
:widths: 30 35 35

* -
  - Simulation
  - ALeRT / Spot
* - Hardware needed
  - None
  - Spot
* - Robot type
  - Varies
  - Quadruped
* - Ubuntu / ROS 2
  - 22.04 / Humble
  - 22.04 / Humble
* - Simulator
  - Webots
  - Webots
* - Main range sensor
  - Varies
  - 3D LiDAR
* - Manipulation
  - Optional
  - Arm with gripper
* - Competition
  - —
  - RoboCup Rescue League
```

Both tracks run the same [supported environment](../reference/compatibility.md)
— Ubuntu 22.04 LTS and ROS 2 Humble, unless a specific ALeRT repository is
documented to need something else — so commands are portable between them
wherever the underlying hardware is. Only the hardware-specific details
(sensors, manipulation) actually differ.

## Can I follow this without hardware?

Yes, in simulation — that is what the [simulation track](simulation.md) is
for. Most topics on this site can be worked through without touching a
physical robot.

If you plan to work with the physical Spot, follow the ALeRT/Spot track from
the start: you get used to its topic names, its tooling and its conventions,
which makes the transition to real hardware much shorter.

```{toctree}
:hidden:
:maxdepth: 1

simulation
alert-spot
```
