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

- [ROS 2 launch documentation](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Launch-Main.html)
- [ros2 bag](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data.html)
- [Ansible documentation](https://docs.ansible.com/)
- [Diagnostic sequence](../reference/ros2-cheatsheet.md#diagnostic-sequence)
