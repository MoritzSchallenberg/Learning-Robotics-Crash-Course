# Simulation

{{ simulation }}

Everything on this site can be done without a physical robot. A simulator
gives you a robot that never runs out of battery, never breaks, and can be
reset instantly — which makes it the better place to learn, and often the
better place to develop.

## Why simulate

**Availability.** There are more team members than robots.

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

ALeRT uses [Webots](https://cyberbotics.com/), an open-source robot
simulator with a ROS 2 interface.

### Installation

```bash
sudo apt install ros-$ROS_DISTRO-webots-ros2
```

Install Webots itself from the
[official installation guide](https://cyberbotics.com/doc/guide/installation-procedure).

:::{warning}
Install the Webots version ALeRT's simulation repository asks for, not the
newest release. This site's own examples were written against **Webots
R2023b**, and simulation packages are frequently pinned to a specific
version. The repository README is the authority, not this page. See
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

### The ALeRT simulation

ALeRT maintains a Webots simulation of Spot and its competition arena. Use
this simulation for every hands-on exercise on this site:

- {{ alert }} [ALeRT / Spot](../platforms/spot/index.md)

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

## Working through this site in simulation

Every topic works, with one adjustment: topic names differ between
simulations, so check yours before assuming `/scan` and `/cmd_vel`.

```{list-table}
:header-rows: 1
:widths: 32 68

* - Topic
  - In simulation
* - [Hardware design](../platforms/hardware-design/index.md)
  - KiCad and Fusion are desktop design tools, independent of Webots — no
    simulation-specific variation applies to this topic.
* - [ROS 2 fundamentals](../ros2/index.md)
  - Identical. `turtlesim` needs no simulator at all.
* - [Sensors and TF2](../sensors-frames/index.md)
  - Identical, and easier — simulated TF trees are usually complete and
    correct from the start.
* - [Perception](../perception/index.md)
  - Simulated cameras publish valid `camera_info` already, so calibration is
    not needed. Do the calibration exercise anyway if you can borrow a webcam.
* - [Mapping](../mapping-world-models/index.md)
  - Identical, and much faster: you can map a whole arena in minutes and reset
    if it goes wrong.
* - [Navigation](../navigation-exploration/index.md)
  - Identical. Set velocity limits to the simulated robot's actual limits.
* - [Autonomous decisions](../decision-making/index.md)
  - Identical. The best place to develop mission logic — you can run the same
    failure scenario twenty times.
* - [Integration](../integration-testing/index.md)
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
topic depends on getting them right.
:::

## Reproducible tasks without ALeRT hardware

If you are not on the ALeRT team, these are enough to work through this
whole site:

**ROS 2** (ROS 2 fundamentals): `turtlesim`. No simulator required.

```bash
ros2 run turtlesim turtlesim_node
```

**Sensors and Coordinate Frames, Mapping and World Models, and
Localization, Navigation and Exploration**: any Webots example with a
laser scanner and odometry, or the [Nav2 simulation
tutorials](https://docs.nav2.org/humble/getting_started/), which ship a
complete mapped environment.

**Perception, and Autonomous Decision-Making**: print ArUco markers on
paper and hold them in front of a webcam, or place them in the simulated
world.

## Common mistakes

**Everything times out and TF complains about extrapolation.**
`use_sim_time`. Always.

**The simulation runs but no ROS 2 topics appear.**
The ROS 2 interface node is not running, or the Webots version does not match
the `webots_ros2` version.

**RViz shows nothing.**
QoS — simulated sensors often publish Best Effort. See
[Sensors and Coordinate Frames](../sensors-frames/practical-exercise.md#common-problems).

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
