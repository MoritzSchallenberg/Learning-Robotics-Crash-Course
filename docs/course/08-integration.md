# 8. System Integration and Testing

{{ common }}

Seven modules of pieces. This one turns them into one system, started with
one command — and teaches the skill that decides how the capstone project
goes: finding out what is broken, fast.

## Overview

You will learn the correct startup order for a full robot system, a
systematic eight-step procedure for finding a fault instead of guessing,
and how to record and replay a rosbag of a real run.

## Learning objectives

By the end of this module you can:

1. bring up a whole robot with one launch command, in the correct order;
2. record and replay a rosbag of a real run;
3. work a systematic procedure to find a fault you introduce yourself.

## Prerequisites

Modules [2](02-ros2.md) through [7](07-autonomous-decisions.md)
completed — this module assembles what you already built, it does not
introduce a new subsystem.

## Core concepts

### Startup order

Each layer needs the one above it already running:

```{figure} ../_static/images/diagrams/09-integration-test-flow.svg
:alt: Left, the bring-up order: Drivers and TF, then Localization, then Navigation, then Mission control, each depending on the layer above. Right, a five-question debugging flow chart: is the node running, is the topic publishing, do names and QoS match, is the TF tree complete, are lifecycle nodes activated, ending at problem located.
:width: 100%

Start in this order; debug by working down this checklist rather than
guessing.
```

Nav2 started before localization spends its startup complaining about
missing transforms. One command should bring up the whole robot:

```bash
ros2 launch robot_bringup robot.launch.yaml
```

### The eight-step diagnostic procedure

When something does not work, resist changing things — work down the stack
in order. The fault is almost always lower than where you noticed it.

```bash
ros2 node list                          # 1. is the node running?
ros2 topic hz /scan                     # 2. is anything published?
ros2 topic info -v /scan                # 3. do names and QoS match?
ros2 run tf2_tools view_frames          # 4. is the TF tree complete?
ros2 lifecycle get /amcl                # 5. are lifecycle nodes activated?
ros2 param get /my_node use_sim_time    # 6. are parameters what you think?
ros2 run rqt_graph rqt_graph            # 7. look at the whole graph
# 8. read the data itself (rqt, rviz)
```

Full version: [ROS 2 cheat sheet](../reference/ros2-cheatsheet.md#diagnostic-sequence).

### rosbags, briefly

Record everything a run needs to be replayable, including both TF topics:

```bash
ros2 bag record -o mini_mission /scan /odom /tf /tf_static /cmd_vel
ros2 bag play mini_mission --clock
```

:::{warning}
Always include `/tf` **and** `/tf_static`. Without both, nothing in the
replay can be placed in space — the single most common thing people forget.
:::

## Guided example

Practice the diagnostic procedure on a fault you introduce yourself, using
your own working `robot_bringup` launch file from previous modules. Make a
copy of it first, then apply exactly **one** of these changes:

```{list-table}
:header-rows: 1
:widths: 45 30 25

* - Change
  - Diagnostic step that finds it
  - Difficulty
* - Rename a published topic in one launch argument
  - Step 3 (names/QoS)
  - Easy
* - Set `use_sim_time` wrong on exactly one node
  - Step 6 (parameters)
  - Medium
* - Remove one node from the lifecycle manager's `node_names`
  - Step 5 (lifecycle)
  - Medium
* - Swap two arguments in a static transform publisher
  - Step 4 (TF tree)
  - Medium
* - Point a map's `yaml_filename` at a file that does not exist
  - Step 1–2 (node/topic)
  - Easy
```

Launch your modified file, then work through the eight-step procedure
**without changing anything yet**, and note which step first reveals the
symptom. Compare it against the table — did the fault surface at the step
you expected? If not, that mismatch is worth understanding before you move
on to the practical task, where you will not know the answer in advance.

## Practical task

### Goal
Find one deliberately introduced fault using the eight-step procedure, fix
it, then run a complete mini-mission end to end.

### Starting point
A working `robot_bringup` launch file from your previous modules, and one
fault from the guided example's table above — pick one you have not tried
yet, or ask someone else to pick one for you without telling you which.

### Steps
1. Apply one fault from the table to a copy of your launch file, then
   `ros2 launch robot_bringup robot.launch.yaml` — note what looks wrong.
2. Work through the eight-step procedure above, in order, **without
   changing anything yet**.
3. Write down the step number where the fault first became visible.
4. Fix only that one thing.
5. Re-launch and confirm the symptom is gone.
6. Record a bag of the fixed system:
   `ros2 bag record -o mini_mission /scan /odom /tf /tf_static /cmd_vel`
7. Run the full mini-mission from [module 7](07-autonomous-decisions.md):
   navigate, detect, report, return — while the bag records.

## Expected result

The fault is found and named by diagnostic step number, not by lucky
guessing, and the recorded mini-mission bag plays back and shows the whole
run in RViz.

## Verification

```bash
ros2 bag info mini_mission
```

Lists all five topics with sensible message counts, and
`ros2 bag play mini_mission --clock` reproduces the run in RViz.

## Common problems

- **Fixed the symptom, not the cause** — e.g., restarting a node instead of
  fixing the renamed topic. Confirm with a fresh launch, not a patched
  running system.
- **Bag replays but nothing appears in RViz** — `/tf_static` was not
  recorded, or `use_sim_time` is not set on the consumers, or `--clock` was
  omitted from playback.
- **`use_sim_time` fixed on one node, forgotten on another** — check every
  node, not just the one you just edited.
- **Debugging by changing things.** Change one thing at a time and observe;
  changing three and having it work teaches you nothing about which one
  mattered.
- **No logs at the decision points.** Add `info`-level logging where your
  mission decides something, before you need it for real.

## Optional extensions

{{ optional }}

Ask someone else to apply one of the table's faults to a copy of your
launch file without telling you which, then time yourself finding it — a
closer approximation of a real, unannounced fault than choosing your own.

{{ simulation }} Identical task, and often the better choice for this
exercise — instant resets mean you can try more faults from the table in
the same sitting.

## Advanced topics

{{ advanced }}

:::{dropdown} Structuring launch files and configuration
:icon: light-bulb

One launch file per subsystem, one top-level file that includes them:

```yaml
# robot.launch.yaml
launch:
- include: {file: "$(find-pkg-share robot_bringup)/launch/drivers.launch.yaml"}
- include: {file: "$(find-pkg-share robot_bringup)/launch/tf.launch.yaml"}
- include: {file: "$(find-pkg-share robot_bringup)/launch/localization.launch.yaml"}
- include: {file: "$(find-pkg-share robot_bringup)/launch/navigation.launch.py"}
```

Values that change between robots or runs belong in config files, not code —
velocity limits, frame names, map paths — and launch arguments for what
changes per run: `ros2 launch robot_bringup robot.launch.yaml
use_sim_time:=true`.
:::

(ansible-as-a-deployment-example)=
:::{dropdown} Ansible as a deployment example
:icon: light-bulb

{{ carologistics }} Once several robots run the same software, updating by
hand does not scale. [Ansible](https://docs.ansible.com/) describes the
desired state of a machine in a *playbook* and makes it so — safe to re-run,
works over plain SSH.

```bash
ansible-playbook -i robots.inv -t fast-deploy robot.yml -l robot-1 -K
```

The Carologistics team uses it for both robot deployment and workstation
setup — see the
[Carologistics platform page](../platforms/carologistics-robotino.md#setup)
for their actual inventory and playbook structure. This is one example of a
deployment tool, not something every team needs to adopt.
:::

## Continue learning

:::{dropdown} Logging levels and where they belong — Next step
:icon: light-bulb

**What it is.** `get_logger().debug/info/warn/error/fatal(...)` — five
severity levels, filterable at runtime with
`ros2 run <pkg> <node> --ros-args --log-level debug` without touching
code. This module's Common problems section already tells you to add
`info`-level logging at decision points; this topic is choosing the right
level for each message.

**Why it matters.** Everything logged at `info` on a busy node buries the
one line that actually mattered during a real debugging session; reserving
`info` for state transitions and decisions, and `debug` for routine detail,
keeps a log usable under pressure.

**Needs.** This module's practical task.

**Try it.** Audit your `robot_bringup` nodes' log calls and reclassify any
line that fires every cycle (should be `debug`) versus one that fires only
on a state change or an error (should stay `info` or higher).

**Check.** Running with the default log level shows only meaningful
transitions, not a scrolling wall of routine detail; running with
`--log-level debug` shows everything.

**Read more.** [ROS 2: logging](https://docs.ros.org/en/humble/Concepts/Intermediate/About-Logging.html)
:::

:::{dropdown} ROS 2 diagnostics — Intermediate
:icon: light-bulb

**What it is.** The `diagnostic_updater`/`diagnostic_aggregator` packages
publish structured `OK`/`WARN`/`ERROR` status per subsystem on
`/diagnostics`, aggregated into a tree you can inspect with
`ros2 run rqt_runtime_monitor rqt_runtime_monitor` — a standard way to
answer "which part of the system is unhappy" without grepping logs.

**Why it matters.** This module's eight-step diagnostic procedure is
something *you* run by hand; `diagnostic_updater` is the same idea running
continuously and automatically, the natural next step once a system has
enough subsystems that manual checking does not scale.

**Needs.** This module's practical task, a working multi-node system.

**Try it.** Add a `diagnostic_updater.Updater` to one node that reports
`WARN` if a sensor topic's rate drops below a threshold, and confirm it
shows up correctly in the runtime monitor.

**Check.** Stopping the sensor's driver flips that diagnostic's status to
`WARN` or `ERROR` within a few seconds, visible in the monitor.

**Read more.** [ROS 2:
diagnostics](https://docs.ros.org/en/humble/p/diagnostic_updater/)
:::

:::{dropdown} Measuring topic frequency and latency — Next step
:icon: light-bulb

**What it is.** `ros2 topic hz` (this module's own eight-step procedure,
step 2) measures publish rate; `ros2 topic delay` measures the gap between
a message's timestamp and when it was received — two different, both
useful, numbers.

**Why it matters.** A topic publishing at the expected rate can still have
growing delay (a node falling behind under load); rate alone would miss
that.

**Needs.** This module's eight-step procedure.

**Try it.** Run `ros2 topic hz /scan` and `ros2 topic delay /scan`
side by side while the system is under normal load, then again while
running something CPU-heavy alongside it (a second build, for instance),
and compare both numbers.

**Check.** You can state whether rate, delay, or both changed under load,
with actual numbers from both runs.

**Read more.** [ROS 2 cheat sheet: diagnostic
sequence](../reference/ros2-cheatsheet.md#diagnostic-sequence)
:::

:::{dropdown} CPU and memory observation — Intermediate
:icon: light-bulb

**What it is.** Standard Linux tools (`top`, `htop`, `ros2 run
rqt_top rqt_top` for a ROS 2-aware view) applied to a running robot
system — which node's process is using the most CPU or memory right now.

**Why it matters.** "The robot is lagging" can be a CPU-bound node stealing
time from everything else, or a slow memory leak that only shows up after
an hour — neither is visible from `ros2 topic hz` alone.

**Needs.** A running multi-node system (this module's practical task).

**Try it.** Run your full `robot_bringup` system and note each node's CPU
and memory usage with `rqt_top` at startup, then again after ten minutes of
running.

**Check.** You can name which process used the most CPU, and whether any
process's memory usage grew unexpectedly over the ten minutes.

**Read more.** [rqt_top](https://docs.ros.org/en/humble/p/rqt_top/)
:::

:::{dropdown} Continuous Integration for a ROS 2 package — Advanced
:icon: light-bulb

**What it is.** Running [module 2's automated
tests](02-ros2.md#continue-learning) automatically on every push, in a
clean environment, via GitHub Actions or similar — the same principle this
course's own website uses for its own build
([README](https://github.com/MoritzSchallenberg/Learning-Robotics-Crash-Course)),
applied to a ROS 2 package instead of a Sphinx site.

**Why it matters.** A test that only runs when someone remembers to run it
locally gets skipped under time pressure — exactly when a regression is
most likely to slip through unnoticed.

**Needs.** [Module 2's automated
tests](02-ros2.md#continue-learning) working locally first.

**Try it.** {{ unverified }} — write a minimal GitHub Actions workflow that
checks out your package, installs ROS 2 Humble (or runs inside an
`osrf/ros:humble-desktop` container image), and runs `colcon test`.

**Check.** The workflow shows green on a passing commit and red on a
commit that deliberately breaks your test from module 2.

**Read more.** [ros-tooling/action-ros-ci](https://github.com/ros-tooling/action-ros-ci)
— a maintained GitHub Action for exactly this.
:::

:::{dropdown} Containers for reproducible deployment — Advanced
:icon: light-bulb

**What it is.** Packaging a ROS 2 environment and your workspace into a
Docker image, so "works on my machine" becomes "works in this exact,
shareable image" — a different answer to the same reproducible-deployment
problem [Ansible](#ansible-as-a-deployment-example) solves by configuring a
real machine instead.

**Why it matters.** A container pins the entire software environment (OS
packages, ROS 2 version, dependencies), not just your own code — useful
for a workstation build that has to match a robot's environment exactly.

**Needs.** This module's practical task, and basic Docker familiarity.

**Try it.** {{ unverified }} — write a `Dockerfile` starting from
`osrf/ros:humble-desktop` that copies in and builds one of your packages,
then run a node from inside the resulting container.

**Check.** `docker run` starts your node successfully with no manual setup
step inside the container beyond what the `Dockerfile` already did.

**Read more.** [Docker images for
ROS](https://hub.docker.com/_/ros) · [Ansible as a deployment
example](#ansible-as-a-deployment-example) above, for the alternative
approach
:::

:::{dropdown} SROS2: securing a ROS 2 system — Advanced
:icon: light-bulb

**What it is.** SROS2 adds authentication, encryption and access control to
ROS 2's DDS communication — by default, anything on the same
[`ROS_DOMAIN_ID`](../prerequisites/networking.md) can publish, subscribe
and call services on anything else, with no authentication at all.

**Why it matters.** A robot that only ever runs on an isolated lab network
may reasonably accept that default; one reachable from a shared or
less-trusted network should not — the same reasoning as
[the networking prerequisite's](../prerequisites/networking.md) domain-ID
isolation advice, taken further.

**Needs.** A working multi-node system and comfort with the ROS 2 CLI.

**Try it.** {{ unverified }} — generate an SROS2 keystore for one node
using `ros2 security` tooling, and run that node with security enabled
while a second, non-enrolled node attempts to communicate with it.

**Check.** You can state, from what you observed, whether the
non-enrolled node's communication was actually blocked.

**Read more.** [ROS 2:
SROS2](https://docs.ros.org/en/humble/Tutorials/Advanced/Security/Introducing-ros2-security.html)
:::

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
