# 8. System Integration and Testing

{{ common }}

## Module overview

Seven modules of pieces. This one turns them into one system, started with
one command — and teaches the skill that decides how the capstone project
goes: finding out what is broken, fast.

**The problem it solves**: nothing built in modules 2–7 becomes a working
robot by itself; something has to start every subsystem in the right
order, and when something breaks, a systematic procedure finds it far
faster than guessing.

**Where it sits in the system**: directly after every other course module
— modules [2](02-ros2.md) through [7](07-autonomous-decisions.md)
completed — this module assembles what you already built, it does not
introduce a new subsystem.

**Needs**: modules [2](02-ros2.md) through
[7](07-autonomous-decisions.md) completed.

**Leads into**: the [capstone project](hackathon.md) is where you run
everything as a complete autonomous mission, on one robot, on its own.

## Learning objectives

By the end of this module you can:

1. bring up a whole robot with one launch command, in the correct order;
2. record and replay a rosbag of a real run;
3. work a systematic procedure to find a fault you introduce yourself;
4. name at least one deployment or observability tool beyond the core
   procedure (Ansible, `diagnostic_updater`, or CI).

## How the complete system fits together

```{figure} ../_static/images/diagrams/09-integration-test-flow.svg
:alt: Left, the bring-up order: Drivers and TF, then Localization, then Navigation, then Mission control, each depending on the layer above. Right, a five-question debugging flow chart: is the node running, is the topic publishing, do names and QoS match, is the TF tree complete, are lifecycle nodes activated, ending at problem located.
:width: 100%

Start in this order; debug by working down this checklist rather than
guessing.
```

Everything in this diagram is a module you already built: drivers and TF
([modules 1](01-system-hardware.md) and [3](03-sensors-tf.md)),
localization ([module 5](05-mapping-localization.md)), navigation
([module 6](06-navigation.md)), and mission control
([module 7](07-autonomous-decisions.md)). This module's only new content
is the order to start them in, and the procedure to debug them together.

## How ALeRT uses this topic

{{ alert }} {{ simulation }}

Spot's full Webots stack is bring-up and debugged with the same order and
eight-step procedure this module teaches, just at a larger scale — see
this module's [Try it on
Spot](08-integration/practical-exercise.md#try-it-on-spot). **Typical
team task**: recording a baseline rosbag of a normally-running system
before deliberately introducing a fault, so there is always a known-good
reference to diff against. **Verification status**: {{ simulation }}
confirmed in Webots.

## How Carologistics uses this topic

{{ carologistics }} {{ documented }}

The team uses [Ansible](https://docs.ansible.com/) for fleet-wide
deployment and workstation setup — a different reproducibility answer than
this module's launch-file structure, solving the same "one source of
truth" problem at the machine-configuration level instead of the
ROS-graph level. See
{ref}`Continue learning: Ansible as a deployment example <ansible-as-a-deployment-example>`.
**Typical team task**: {{ unverified }} — not documented in detail beyond
the Ansible workflow itself. **Verification status**: {{ documented }} via
the platform page's own setup instructions.

## ALeRT and Carologistics compared

```{list-table}
:header-rows: 1
:widths: 22 26 26 26

* - Aspect
  - ALeRT / Spot
  - Carologistics / Robotino
  - Shared principle
* - System complexity
  - Many sensor and motion nodes on one robot
  - Multiple Robotinos plus a central goal-reasoning agent
  - Both need a fixed startup order, not ad hoc launching
* - Deployment
  - {{ unverified }} — not documented as a formal process
  - Ansible playbooks, safe to re-run
  - Both solve "does every machine run the same software"
* - Fault-finding
  - The eight-step procedure, applied to the Webots stack
  - {{ unverified }} — not documented as a standard team practice
  - A systematic procedure beats guessing on any system this size
* - Central coordination
  - {{ unverified }} — one robot, not documented
  - `expertino-rcll` coordinates the whole fleet
  - Neither replaces per-robot startup order with something ad hoc
```

## Core learning path

```text
1. System bring-up and diagnostics
2. Practical integration exercise
```

That is this module's roughly 80–100 minute core learning time.
**Interesting videos** and **Continue learning** are worthwhile
afterwards but not required for the core path.

## Subtopics

::::{grid} 1 1 2 2
:gutter: 2

:::{grid-item-card} System bring-up and diagnostics
:link: 08-integration/system-bringup-and-diagnostics
:link-type: doc

{{ core }} Startup order, the eight-step diagnostic procedure, and
rosbags.
:::

:::{grid-item-card} Practical exercise
:link: 08-integration/practical-exercise
:link-type: doc

{{ core }} Find a fault, fix it, run a mini-mission — plus this module's
Try it on Spot section.
:::

:::{grid-item-card} Interesting videos
:link: 08-integration/videos
:link-type: doc

One carefully checked video recommendation.
:::

:::{grid-item-card} Continue learning
:link: 08-integration/continue-learning
:link-type: doc

Logging levels, diagnostics, topic frequency/latency, CPU/memory, CI,
containers, Ansible, SROS2.
:::

::::

## Prerequisites

Modules [2](02-ros2.md) through [7](07-autonomous-decisions.md)
completed — this module assembles what you already built, it does not
introduce a new subsystem.

## Readiness checklist

Before attempting the [capstone project](hackathon.md):

- [ ] One command brings up the whole system, from cold, with no manual
      steps.
- [ ] Every configuration value lives in a config file, in version control.
- [ ] Rosbag recording is one command you know by heart.
- [ ] You can restore a known-good state from git in under a minute.
- [ ] You have personally started the robot at least once, end to end.

## Connection to the next module

This module assembled every piece from the previous ones into one system.
The [capstone project](hackathon.md) is where you run it as a complete
autonomous mission, on one robot, on its own.

## Further reading

- [ROS 2 launch documentation](https://docs.ros.org/en/humble/Tutorials/Intermediate/Launch/Launch-Main.html)
- [ros2 bag](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data.html)
- [Ansible documentation](https://docs.ansible.com/)
- [Diagnostic sequence](../reference/ros2-cheatsheet.md#diagnostic-sequence)

```{toctree}
:maxdepth: 1
:hidden:

08-integration/system-bringup-and-diagnostics
08-integration/practical-exercise
08-integration/videos
08-integration/continue-learning
```
