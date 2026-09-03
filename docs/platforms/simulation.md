# Simulation

{{ simulation }}

Everything in this course can be done without a physical robot. A simulator
gives you a robot that never runs out of battery, never breaks, and can be
reset instantly — which makes it the better place to learn, and often the
better place to develop.

## Why simulate

**Availability.** There are more course participants than robots.

**Repeatability.** The same scenario, exactly, as often as you like. On real
hardware, no two runs are identical.

**Safety.** A navigation bug that drives into a wall costs nothing.

**Speed.** Reset to a known state in a second, instead of carrying the robot
back to its start position.

The limitation is worth stating plainly: **a simulator lies**. Sensor noise is
cleaner than reality, contact physics is approximate, timing is more generous,
and networks do not drop. Code that works in simulation and fails on hardware
is normal, and the gap is usually noise, timing or friction. Develop in
simulation; validate on hardware.

## Webots

Both institute teams use [Webots](https://cyberbotics.com/), an open-source
robot simulator with a ROS 2 interface.

### Installation

```bash
sudo apt install ros-$ROS_DISTRO-webots-ros2
```

Install Webots itself from the
[official installation guide](https://cyberbotics.com/doc/guide/installation-procedure).

:::{warning}
Install the Webots version your team's simulation repository asks for, not the
newest release. Both source courses were written against **Webots R2023b**, and
simulation packages are frequently pinned to a specific version. The repository
README is the authority, not this page. See
[compatibility](../reference/compatibility.md).
:::

### Getting started with a stock example

`webots_ros2` ships demonstration packages that need no team repository, which
makes them a good place to confirm your installation works:

```bash
ros2 launch webots_ros2_universal_robot multirobot_launch.py
```

Other examples are listed in the
[webots_ros2 documentation](https://docs.ros.org/en/humble/p/webots_ros2/).

### Team simulations

Both teams maintain a Webots simulation of their robot and competition arena.
These are the ones to use if you are following a team track:

- {{ carologistics }} [Carologistics / Robotino](carologistics-robotino.md)
- {{ alert }} [ALeRT / Spot](alert-spot.md)

## Simulation time

This is the one concept that causes more trouble than anything else about
simulation.

A simulator publishes its own clock on `/clock`, which may run faster or slower
than wall-clock time. Nodes must be told to use it:

```bash
ros2 param set /my_node use_sim_time true
```

or, in a launch file:

```yaml
param:
-
  name: "use_sim_time"
  value: True
```

:::{danger}
`use_sim_time` must be `true` on **every** node in simulation, and `false` on
**every** node on hardware. One node with the wrong value produces transform
extrapolation errors, a map that never updates, and navigation that times out
— none of which point at the actual cause.

When something in simulation behaves inexplicably, check this first:

```bash
ros2 param get /my_node use_sim_time
```
:::

## Working through the course in simulation

Every module works, with one adjustment: topic names differ between
simulations, so check yours before assuming `/scan` and `/cmd_vel`.

```{list-table}
:header-rows: 1
:widths: 8 32 60

* - #
  - Module
  - In simulation
* - 1
  - [System hardware](../course/01-system-hardware.md)
  - Inspect the simulated robot's model instead of physical hardware. The
    sensors, frames and drive geometry are all visible in the scene tree.
* - 2
  - [ROS 2 fundamentals](../course/02-ros2.md)
  - Identical. `turtlesim` needs no simulator at all.
* - 3
  - [Sensors and TF2](../course/03-sensors-tf.md)
  - Identical, and easier — simulated TF trees are usually complete and
    correct from the start.
* - 4
  - [Perception](../course/04-perception/index.md)
  - Simulated cameras publish valid `camera_info` already, so calibration is
    not needed. Do the calibration exercise anyway if you can borrow a webcam.
* - 5
  - [Mapping](../course/05-mapping-localization.md)
  - Identical, and much faster: you can map a whole arena in minutes and reset
    if it goes wrong.
* - 6
  - [Navigation](../course/06-navigation.md)
  - Identical. Set velocity limits to the simulated robot's actual limits.
* - 7
  - [Autonomous decisions](../course/07-autonomous-decisions.md)
  - Identical. The best place to develop mission logic — you can run the same
    failure scenario twenty times.
* - 8
  - [Integration](../course/08-integration.md)
  - Identical, except that you cannot simulate a flat battery or a loose
    connector. Those you learn on hardware.
```

## Finding the topic names

Never assume. The first thing to do with any simulation:

```bash
ros2 topic list
ros2 topic list -t          # with message types
ros2 node list
ros2 service list -t
ros2 action list
```

Then find the ones that matter:

```bash
# What accepts velocity commands?
ros2 topic list -t | grep Twist

# What publishes laser data?
ros2 topic list -t | grep LaserScan

# What publishes images?
ros2 topic list -t | grep Image
```

:::{tip}
Write the names down the first time. Simulated robots frequently namespace
their topics — `/Spot/odometry` rather than `/odom` — and every later
module depends on getting them right.
:::

## Reproducible tasks without team hardware

If you are not on either team, these are enough to complete the whole course:

**Module 2** (ROS 2 fundamentals): `turtlesim`. No simulator required.

```bash
ros2 run turtlesim turtlesim_node
```

**Modules 3, 5 and 6** (sensors/TF, mapping/localization, navigation): any
Webots example with a laser scanner and odometry, or the
[Nav2 simulation tutorials](https://docs.nav2.org/humble/getting_started/),
which ship a complete mapped environment.

**Modules 4 and 7** (perception, and the mission in autonomous decisions):
print ArUco markers on paper and hold them in front of a webcam, or place
them in the simulated world.

## Common mistakes

**Everything times out and TF complains about extrapolation.**
`use_sim_time`. Always.

**The simulation runs but no ROS 2 topics appear.**
The ROS 2 interface node is not running, or the Webots version does not match
the `webots_ros2` version.

**RViz shows nothing.**
QoS — simulated sensors often publish Best Effort. See
[module 3](../course/03-sensors-tf/practical-exercise.md#common-problems).

**The simulation runs very slowly.**
No 3D acceleration. This is the usual outcome inside a virtual machine, and the
reason a native Linux install is recommended.

**Code works in simulation and fails on the robot.**
Expected. Look at noise, timing, and topic names first.

## Further reading

- [Webots documentation](https://cyberbotics.com/doc/guide/index)
- [webots_ros2](https://docs.ros.org/en/humble/p/webots_ros2/)
- [Nav2 getting started](https://docs.nav2.org/humble/getting_started/)
- [Using simulation time in ROS 2](https://design.ros2.org/articles/clock_and_time.html)
