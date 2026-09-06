# Integration, Diagnostics and Testing

## Overview

Every earlier topic built one piece. This one turns them into one system,
started with one command — and teaches the skill that decides how the
[Autonomous Rescue Mission](../rescue-projects/autonomous-rescue-mission.md)
goes: finding out what is broken, fast.

**The problem it solves**: nothing built in the [ROS
2](../ros2/index.md) through [Autonomous
Decision-Making](../decision-making/index.md) topics becomes a working
robot by itself; something has to start every subsystem in the right
order, and when something breaks, a systematic procedure finds it far
faster than guessing.

**Where it sits in the system**: directly after every other topic on this
site — [ROS 2](../ros2/index.md) through [Autonomous
Decision-Making](../decision-making/index.md) completed — this topic
assembles what you already built, it does not introduce a new subsystem.

**Needs**: [ROS 2](../ros2/index.md) through [Autonomous
Decision-Making](../decision-making/index.md) completed.

**Leads into**: the [Autonomous Rescue
Mission](../rescue-projects/autonomous-rescue-mission.md) is where you run
everything as a complete autonomous mission, on one robot, on its own.

## Learning objectives

By the end of this topic you can:

1. bring up a whole robot with one launch command, in the correct order;
2. record and replay a rosbag of a real run;
3. work a systematic procedure to find a fault you introduce yourself;
4. name at least one deployment or observability tool beyond the core
   procedure (Ansible, `diagnostic_updater`, or CI).

## How the complete system fits together

```{figure} ../_static/images/diagrams/integration-test-flow.svg
:alt: Left, the bring-up order: Drivers and TF, then Localization, then Navigation, then Mission control, each depending on the layer above. Right, a five-question debugging flow chart: is the node running, is the topic publishing, do names and QoS match, is the TF tree complete, are lifecycle nodes activated, ending at problem located.
:width: 100%

Start in this order; debug by working down this checklist rather than
guessing.
```

Everything in this diagram is something you already built: drivers and TF
([Sensors and Coordinate Frames](../sensors-frames/index.md)), localization
([Mapping and World Models](../mapping-world-models/index.md)), navigation
([Navigation and Exploration](../navigation-exploration/index.md)), and mission control
([Autonomous Decision-Making](../decision-making/index.md)). This topic's only new content
is the order to start them in, and the procedure to debug them together.

## How ALeRT uses this topic

{{ alert }} {{ simulation }}

Spot's full Webots stack is bring-up and debugged with the same order and
eight-step procedure this topic teaches, just at a larger scale — see
this topic's [Try it on
Spot](practical-exercise.md#try-it-on-spot). **Typical
team task**: recording a baseline rosbag of a normally-running system
before deliberately introducing a fault, so there is always a known-good
reference to diff against. **Verification status**: {{ simulation }}
confirmed in Webots.

## Working through this topic

```text
1. System bring-up and diagnostics
2. Practical integration exercise
```

**Interesting videos** and **Continue learning** are worthwhile
afterwards, but are not required to move on to the next topic.

## Subtopics

::::{grid} 1 1 2 2
:gutter: 2

:::{grid-item-card} System bring-up and diagnostics
:link: system-bringup-and-diagnostics
:link-type: doc

{{ foundation }} Startup order, the eight-step diagnostic procedure, and
rosbags.
:::

:::{grid-item-card} Practical exercise
:link: practical-exercise
:link-type: doc

{{ foundation }} Find a fault, fix it, run a mini-mission — plus this topic's
Try it on Spot section.
:::

:::{grid-item-card} Interesting videos
:link: videos
:link-type: doc

One carefully checked video recommendation.
:::

:::{grid-item-card} Continue learning
:link: continue-learning
:link-type: doc

Logging levels, diagnostics, topic frequency/latency, CPU/memory, CI,
containers, Ansible, SROS2.
:::

::::

## Prerequisites

[ROS 2](../ros2/index.md) through [Autonomous
Decision-Making](../decision-making/index.md) completed — this topic
assembles what you already built, it does not introduce a new subsystem.

## Readiness checklist

Before attempting the [Autonomous Rescue
Mission](../rescue-projects/autonomous-rescue-mission.md):

- [ ] One command brings up the whole system, from cold, with no manual
      steps.
- [ ] Every configuration value lives in a config file, in version control.
- [ ] Rosbag recording is one command you know by heart.
- [ ] You can restore a known-good state from git in under a minute.
- [ ] You have personally started the robot at least once, end to end.

## Connection to the next topic

This topic assembled every piece from the previous ones into one system.
The [Autonomous Rescue
Mission](../rescue-projects/autonomous-rescue-mission.md) is where you run
it as a complete autonomous mission, on one robot, on its own.

## Further reading

- [ROS 2 launch documentation](https://docs.ros.org/en/humble/Tutorials/Intermediate/Launch/Launch-Main.html)
- [ros2 bag](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data.html)
- [Ansible documentation](https://docs.ansible.com/)
- [Diagnostic sequence](../reference/ros2-cheatsheet.md#diagnostic-sequence)

```{toctree}
:maxdepth: 1
:hidden:

system-bringup-and-diagnostics
practical-exercise
videos
continue-learning
```
