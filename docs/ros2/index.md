# ROS 2

## Overview

Hardware Design covered the electrical and mechanical design a robot is built
from. **ROS 2** is the software that runs on top of that hardware: it
organises a robot's software into **nodes** exchanging data over
**topics**, and the rest of this topic is a full, hands-on lab where you
install it, drive, inspect, script and eventually replace part of a small
running ROS 2 system yourself.

**The problem it solves**: a real robot is not one program — it is many
independent programs (a sensor driver, a planner, a motor controller)
that need to exchange data and commands without every one of them knowing
about every other one, and without a change to one requiring a rebuild of
the rest. ROS 2 is the middleware that makes that decoupling practical.

**Where it sits in the system**: everywhere. Every topic after this one
— sensors, perception, mapping, navigation, decisions, integration — is
built out of ROS 2 nodes, topics, services, parameters and actions. This
topic is the one time this site teaches those five tools directly,
without a sensor or a mission in the way.

**Needs**: [Hardware Design](../platforms/hardware-design/index.md) completed, and the general
[prerequisites](../getting-started/index.md) (Linux, Git, networking). ROS 2
itself is not yet installed at this point — this topic's own
[Installation and environment setup](installation.md) is the
first subtopic below.

**Leads into**: every later topic assumes fluency with `ros2 node`,
`ros2 topic`, `ros2 service`, `ros2 param` and `ros2 action`, and this
topic's own `turtle_controller` package is the pattern
[Perception's](../perception/index.md) and
[Autonomous Decision-Making's](../decision-making/index.md) practical tasks build on
directly.

## Learning objectives

By the end of this topic you can:

1. explain what a node, a topic, a message, a service, a parameter and an
   action are, and pick the right one for a given job;
2. inspect a running ROS 2 system entirely from the command line — no
   source code required;
3. publish, call and configure a running system by hand, without writing
   any code;
4. write a small `rclpy` node that publishes on a timer and reacts to its
   own internal state;
5. read a `rqt_graph` visualisation and relate it back to what
   `ros2 node info` already told you;
6. recognise the same five ROS 2 primitives inside a much larger system
   than turtlesim, such as a real robot's.

## How the complete system fits together

```{figure} ../_static/images/diagrams/ros2-node-topic-communication.svg
:alt: Two publisher nodes send data to a topic named /scan, which two subscriber nodes read from. A separate pair of nodes shows a two-way service call for contrast.
:width: 100%

Topics decouple publishers from subscribers; services are a direct
request/response between two nodes instead.
```

A ROS 2 system is a graph of **nodes** exchanging typed data over three
channel shapes:

```{list-table}
:header-rows: 1
:widths: 16 21 21 21 21

* -
  - Topic
  - Service
  - Parameter
  - Action
* - Pattern
  - Stream, no reply
  - Request → response
  - Get/set a value
  - Goal → feedback → result
* - Duration
  - Continuous
  - Immediate
  - Immediate
  - Seconds to minutes
* - Who initiates
  - Publisher, whenever
  - Client, on demand
  - Client, on demand
  - Client, on demand
* - Turtlesim example
  - `/turtle1/cmd_vel`
  - `/spawn`
  - `background_r`
  - `rotate_absolute`
```

The decoupling is the whole point: swap the simulator for a real robot,
and every node downstream keeps working, because they only ever agreed on
a topic's **name** and **type** — not on which program is on the other
end. That is true whether the "other end" is `turtle_teleop_key`, a
Webots Spot driver, or a real Spot's motor controller.

## How ALeRT uses this topic

{{ alert }} {{ documented }}

Spot's ROS 2 system is the same five primitives as turtlesim, just with
many more nodes: sensor drivers (LiDAR, gripper camera, odometry),
posture control exposed as **services** (`/Spot/stand_up`,
`/Spot/sit_down`, `/Spot/lie_down`, of type `webots_spot_msgs/srv/SpotMotion`
— see the [platform page](../platforms/spot/index.md#services-and-actions)),
one **action** you will use directly in this topic's own Try it on Spot
section (`/turtle1/rotate_absolute` has no Spot equivalent documented at
this fundamentals level; Spot's own action usage is covered once
navigation is introduced in [Navigation and Exploration](../navigation-exploration/index.md)), and topics for
everything continuous — odometry, the point cloud, the camera image,
`/cmd_vel`.

**Typical team task**: bringing up the Webots Spot simulation and
confirming, with exactly the CLI commands this topic teaches, that the
expected nodes are running before attempting anything more advanced —
the same triage habit this topic's own diagnostic tasks build.

**Known peculiarity**: {{ unverified }} exact node and topic names change
between branches of the simulation repository; this topic (and the
[platform page](../platforms/spot/index.md)) both explicitly tell you to
confirm with `ros2 topic list` rather than trust a fixed list.

**Verification status**: {{ simulation }} confirmed in Webots; real-Spot
node/topic names are documented on the platform page but this site does
not claim to have re-verified every one against current hardware.

## Working through this topic

Work through the subtopics below in this order — each one uses a command
or an idea from the one before it:

```text
1. Installation and environment setup
2. Nodes and packages
3. Topics and messages
4. Services, parameters and actions
5. Write your own turtle controller
6. Practical exercises (the turtlesim challenge, Try it on Spot)
```

Installation is its own, separate first step — a system install and
several downloads take a different amount of time on every machine.
**Interesting videos** and **Continue learning** are worthwhile
afterwards, but are not required to move on to the next topic.

## Subtopics

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} Installation and environment setup
:link: installation
:link-type: doc

Get from a bare Ubuntu machine to a working ROS 2 Humble workspace, with
nothing left implicit.
:::

:::{grid-item-card} Nodes and packages
:link: nodes-and-packages
:link-type: doc

Install turtlesim, start it and drive it by keyboard, then inspect the
two nodes that just did that with `ros2 node info`.
:::

:::{grid-item-card} Topics and messages
:link: topics-and-messages
:link-type: doc

Inspect `/turtle1/cmd_vel`'s type and QoS, then drive the turtle
yourself with `ros2 topic pub` — no keyboard at all.
:::

:::{grid-item-card} Services, parameters and actions
:link: services-parameters-actions
:link-type: doc

Spawn, clear and kill turtles with services; read and change a live
parameter; send a cancellable action goal.
:::

:::{grid-item-card} Write your own turtle controller
:link: turtle-controller
:link-type: doc

This topic's practical task: replace `turtle_teleop_key` with your own
`rclpy` node that drives a square, no keyboard involved.
:::

:::{grid-item-card} Practical exercises
:link: practical-exercises
:link-type: doc

The turtlesim challenge, and this topic's Try it on Spot section.
:::

:::{grid-item-card} Interesting videos
:link: videos
:link-type: doc

One carefully checked video recommendation.
:::

:::{grid-item-card} Continue learning
:link: continue-learning
:link-type: doc

Parameters done properly, custom interfaces, QoS mismatches, namespaces,
lifecycle nodes, composition, executors, automated tests — and launch
files, the one topic this topic only touches in passing.
:::

::::

## Preflight check

`scripts/tutorial-preflight.sh` is a read-only script that checks your OS,
`ROS_DISTRO`, the `ros2` CLI, your workspace and RViz — nothing more — and
tells you exactly what to fix if anything is missing:

```bash
bash scripts/tutorial-preflight.sh
```

Run it once [Installation and environment
setup](installation.md) is done, before continuing to Nodes and
packages, and again any time a command in this site behaves
unexpectedly and you suspect your environment rather than your code.

## Connection to the next topic

This topic gave you a running ROS 2 system: nodes talking over topics,
services, parameters and actions. [Sensors and Coordinate Frames](../sensors-frames/index.md) has those
topics carry **sensor data**, and you learn where in space that data
actually is.

```{toctree}
:hidden:
:maxdepth: 1

installation
nodes-and-packages
topics-and-messages
services-parameters-actions
turtle-controller
practical-exercises
videos
continue-learning
```
