# System bring-up and diagnostics

{{ common }} {{ core }}

## What this topic is

**Startup order**: the sequence a full robot system's layers must come
online in, so each layer finds what it depends on already running. The
**eight-step diagnostic procedure**: a systematic, ordered way to find a
fault instead of guessing. **rosbags**: recording everything a run needs
to be replayable later.

## Why a robot needs it

Seven modules of pieces do not become one working robot by themselves —
something has to start them all, in an order that actually works, and
when something breaks, guessing at random wastes far more time than
working down a fixed checklist. This is the skill that decides how the
[capstone project](../hackathon.md) goes: finding out what is broken,
fast.

## How it works

(startup-order)=
### Startup order

Each layer needs the one above it already running:

```{figure} ../../_static/images/diagrams/09-integration-test-flow.svg
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

That one command is itself structured — one launch file per subsystem,
one top-level file that includes them:

```yaml
# robot.launch.yaml
launch:
- include: {file: "$(find-pkg-share robot_bringup)/launch/drivers.launch.yaml"}
- include: {file: "$(find-pkg-share robot_bringup)/launch/tf.launch.yaml"}
- include: {file: "$(find-pkg-share robot_bringup)/launch/localization.launch.yaml"}
- include: {file: "$(find-pkg-share robot_bringup)/launch/navigation.launch.py"}
```

Values that change between robots or runs belong in config files, not
code — velocity limits, frame names, map paths — and launch arguments for
what changes per run: `ros2 launch robot_bringup robot.launch.yaml
use_sim_time:=true`. One source of truth, in version control, is the same
principle [module 1's](../01-system-hardware.md) and
[module 5's](../05-mapping-localization.md) own version-control advice
already applies to hardware designs and maps.

(the-eight-step-diagnostic-procedure)=
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

Full version: [ROS 2 cheat sheet](../../reference/ros2-cheatsheet.md#diagnostic-sequence).

(rosbags-briefly)=
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

## Try it yourself

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
on to [the practical exercise](practical-exercise.md), where you will not
know the answer in advance.

## How ALeRT applies it

{{ alert }} {{ simulation }} See this module's [Try it on
Spot](practical-exercise.md#try-it-on-spot) for running the same
diagnostic procedure against the full Webots Spot stack.

## How Carologistics applies it

{{ carologistics }} {{ documented }} Once several robots run the same
software, updating by hand does not scale — the team uses
[Ansible](https://docs.ansible.com/) for both deployment and workstation
setup, a different answer to the same "one source of truth" reproducibility
principle. Full detail in
{ref}`Continue learning: Ansible as a deployment example <ansible-as-a-deployment-example>`.

## Common problems

- **`use_sim_time` fixed on one node, forgotten on another.** Check every
  node, not just the one you just edited.
- **Debugging by changing things.** Change one thing at a time and
  observe; changing three and having it work teaches you nothing about
  which one mattered.

## Next subtopic

[Practical exercise](practical-exercise.md) — find one deliberately
introduced fault, fix it, then run a complete mini-mission end to end.

## Sources

- [ROS 2 launch documentation](https://docs.ros.org/en/humble/Tutorials/Intermediate/Launch/Launch-Main.html)
- [ros2 bag](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data.html)
