# Platform tracks

The [course modules](../course/index.md) explain the shared fundamentals once.
These pages carry only what is specific to one system: the launch commands, the
topic names, the hardware quirks.

If a general concept is explained in the course, these pages link to it rather
than repeating it. That is deliberate — one explanation, kept correct in one
place.

## Pick your track

::::{grid} 1 1 3 3
:gutter: 3

:::{grid-item-card} Simulation
:link: simulation
:link-type: doc

No robot required. Webots, example robots, reproducible tasks. The right choice
if you are learning, or if the hardware is booked.
:::

:::{grid-item-card} Carologistics / Robotino
:link: carologistics-robotino
:link-type: doc

Festo Robotino in the RoboCup Logistics League. Omnidirectional drive, laser
lines, vision, gripper.
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
:widths: 22 26 26 26

* -
  - Simulation
  - Carologistics / Robotino
  - ALeRT / Spot
* - Hardware needed
  - None
  - Robotino
  - Spot
* - Robot type
  - Varies
  - Wheeled, omnidirectional
  - Quadruped
* - Ubuntu / ROS 2
  - 22.04 / Humble
  - 22.04 / Humble
  - 22.04 / Humble
* - Simulator
  - Webots
  - Webots
  - Webots
* - Main range sensor
  - Varies
  - 2D laser scanners
  - 3D LiDAR
* - Manipulation
  - Optional
  - Custom gripper
  - Arm with gripper
* - Competition
  - —
  - RoboCup Logistics League
  - RoboCup Rescue League
```

All three tracks run the same [supported environment](../reference/compatibility.md)
— Ubuntu 22.04 LTS and ROS 2 Humble — so commands are portable between
tracks wherever the underlying hardware is. Only the hardware-specific
details (drive type, sensors, manipulation) actually differ.

## Can I follow a track I do not have hardware for?

Yes, in simulation — that is what the [simulation track](simulation.md) is for.
Every course module can be completed without touching a physical robot.

If you plan to join one of the teams, follow that team's track from the start:
you get used to its topic names, its tooling and its conventions, which makes
the transition to real hardware much shorter.

```{toctree}
:hidden:
:maxdepth: 1

simulation
carologistics-robotino
alert-spot
```
