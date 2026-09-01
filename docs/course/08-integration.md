# 8. System Integration and Testing

:::{admonition} Session 8
:class: note

Wednesday, 28 October 2026, 17:35 – 19:00
:::

{{ common }}

Eight weeks of pieces. Tonight they become one system — and you learn the skill
that actually decides how the hackathon goes: finding out what is broken, fast.

## Learning objectives

After this session you can:

- structure a robot's startup as composed launch files;
- separate configuration from code;
- use ROS 2 logging effectively and read the output;
- record and replay a rosbag, and debug from it;
- follow a systematic procedure to locate a fault;
- explain what Ansible does for fleet deployment.

## Prerequisites

Sessions [2](02-ros2.md) through [7](07-autonomous-decisions.md). You will be
assembling everything you have built.

## Interfaces between subsystems

By now your robot is roughly this:

```text
   drivers  ──►  /scan, /odom, /image_raw, /tf
                        │
                        ▼
   localization  ──►  /map, map→odom
                        │
                        ▼
   navigation  ──►  /cmd_vel, /plan
                        │
                        ▼
   mission control  ──►  goals, decisions
```

Every arrow is a contract with four parts: a **topic name**, a **message
type**, a **frame**, and a **QoS profile**. Almost every integration failure is
one of those four not matching — and none of them produces a helpful error.

:::{tip}
Write the contracts down. A short table in your team's README listing every
topic your system uses, with its type, publisher, subscribers and frame, will
save more time during the hackathon than any code you write that day.
:::

## Startup order

Order matters, because each layer needs the one below it to already exist:

1. **Drivers and TF** — sensors publishing, transform tree complete
2. **Localization** — needs `/scan` and `/odom`
3. **Navigation** — needs `map` → `odom` → `base_link`
4. **Mission control** — needs the navigation action server

Start Nav2 before localization and it will spend its startup complaining about
missing transforms, and may or may not recover.

### Structuring launch files

The maintainable pattern is one launch file per subsystem and one top-level
file that includes them:

```text
robot_bringup/launch/
├── robot.launch.yaml          # the only one you run by hand
├── drivers.launch.yaml        # lidar, camera, motor controller
├── tf.launch.yaml             # static transforms
├── localization.launch.yaml   # map_server + amcl
└── navigation.launch.py       # nav2
```

```yaml
# robot.launch.yaml
launch:

- include:
    file: "$(find-pkg-share robot_bringup)/launch/drivers.launch.yaml"

- include:
    file: "$(find-pkg-share robot_bringup)/launch/tf.launch.yaml"

- include:
    file: "$(find-pkg-share robot_bringup)/launch/localization.launch.yaml"

- include:
    file: "$(find-pkg-share robot_bringup)/launch/navigation.launch.py"
```

The goal is that one command brings up the whole robot:

```bash
ros2 launch robot_bringup robot.launch.yaml
```

:::{tip}
Being able to start and stop the entire system with one command is worth real
effort. During the hackathon you will do it dozens of times, often under time
pressure, and every manual step is a step someone forgets.
:::

## Configuration

Values that change between robots, runs or venues belong in configuration
files, not in code. Velocity limits, frame names, topic names, map paths,
camera parameters — all of it.

```text
robot_bringup/
├── config/
│   ├── nav2_params.yaml
│   ├── amcl_params.yaml
│   └── camera_params.yaml
└── launch/
```

Use launch arguments for what changes per run:

```bash
ros2 launch robot_bringup robot.launch.yaml use_sim_time:=true
```

:::{warning}
`use_sim_time` deserves its own mention one last time, because it will bite you
in integration more than anywhere else. It must be `true` for **every** node in
simulation and `false` for **every** node on hardware. A single node with the
wrong value produces transform errors that look like a TF bug and are not.
:::

## Logging

### Using it properly

```python
self.get_logger().debug('Details only useful while developing')
self.get_logger().info('Normal progress: reached waypoint 3')
self.get_logger().warning('Something is odd but recoverable')
self.get_logger().error('This operation failed')
self.get_logger().fatal('The node cannot continue')
```

Choose the level honestly. A node that logs everything at `info` is as useless
as one that logs nothing, because nobody reads a wall of text.

Change the level at runtime without editing code:

```bash
ros2 run <pkg> <node> --ros-args --log-level debug
ros2 run <pkg> <node> --ros-args --log-level my_node:=debug
```

:::{tip}
For anything inside a callback running at 20 Hz, use throttled logging so it
does not flood the terminal:

```python
self.get_logger().info('Still waiting for the goal', throttle_duration_sec=2.0)
```
:::

### Reading it

Launch output interleaves every node, which is chaotic but also exactly what
you want when diagnosing startup order. Logs are also written to
`~/.ros/log/`, one directory per launch, which is where to look when the
terminal has scrolled away.

## ROS bags

A **rosbag** records topics to disk and replays them later. It is the single
most valuable debugging tool in ROS 2, because it turns "it failed once
yesterday and we cannot reproduce it" into something you can replay as often as
you like.

### Recording

```bash
ros2 bag record -a                              # everything (large!)
ros2 bag record /scan /odom /tf /tf_static      # specific topics
ros2 bag record -o mission_run_3 /scan /odom /tf /tf_static /cmd_vel
```

```bash
ros2 bag info mission_run_3
```

:::{warning}
`-a` records camera and point cloud topics too, and will fill a disk in
minutes. Name the topics you need. Always include `/tf` **and** `/tf_static` —
without both, nothing can be placed in space on replay, and this is the single
most common thing people forget.
:::

### Replaying

```bash
ros2 bag play mission_run_3
ros2 bag play mission_run_3 --rate 0.5     # half speed, to watch closely
ros2 bag play mission_run_3 --loop
```

Replayed data has the timestamps it was recorded with, so nodes consuming it
need:

```bash
ros2 param set /my_node use_sim_time true
```

and the bag needs `--clock` to publish the clock:

```bash
ros2 bag play mission_run_3 --clock
```

:::{tip}
Record a bag of every serious test run during the hackathon. When something
goes wrong you will have the evidence, and you can develop the fix against the
recorded data instead of monopolising the robot.
:::

## A debugging procedure

When something does not work, resist the urge to change things. Work down the
stack in order — the fault is almost always lower than where you noticed it.

### 1. Is the node running?

```bash
ros2 node list
```

Not there? Check the launch output for the exception that killed it.

### 2. Is the topic being published?

```bash
ros2 topic list
ros2 topic hz /scan
ros2 topic echo /scan --once
```

`hz` reports nothing → nothing is publishing. `hz` reports a rate but `echo`
shows nothing → almost certainly QoS.

### 3. Do the names match?

```bash
ros2 topic info -v /scan
```

Publishers and subscribers both listed? A count of zero on either side means
somebody has the name wrong, or a namespace is in play.

### 4. Do the QoS profiles match?

The same command shows the profiles. Reliability and Durability must be
compatible. See [session 3](03-sensors-tf.md#when-rviz-shows-nothing).

### 5. Is the transform tree complete?

```bash
ros2 run tf2_tools view_frames
ros2 run tf2_ros tf2_echo map base_link
```

### 6. Are lifecycle nodes activated?

```bash
ros2 lifecycle get /amcl
ros2 lifecycle get /controller_server
```

### 7. Are the parameters what you think?

```bash
ros2 param list /my_node
ros2 param get /my_node use_sim_time
```

This one catches an astonishing number of "impossible" problems.

### 8. Look at the data

```bash
rqt
ros2 run rqt_graph rqt_graph
```

`rqt_graph` draws the whole node and topic graph. A node sitting alone with no
connections is immediately visible, and is often the answer.

:::{tip}
Keep a terminal open with `ros2 topic hz` on your most important topic — the
laser scan, usually. When it stops, you know instantly, and you know where.
:::

## Deployment with Ansible

Once several robots run the same software, updating them by hand does not
scale. [Ansible](https://docs.ansible.com/) automates it: you describe the
desired state of a machine in a *playbook*, and Ansible makes it so.

The properties that matter:

**Idempotent** — running a playbook twice has the same effect as running it
once, so it is safe to re-run.

**Agentless** — it works over SSH; nothing needs installing on the robots
beyond an SSH server.

A deployment command looks like this:

```bash
ansible-playbook -i robots.inv -t fast-deploy robot.yml -l robot-1 -K
```

`-i robots.inv`
: the inventory — which hosts exist and how they are grouped

`robot.yml`
: the playbook — which roles to apply

`-l robot-1`
: limit to one host

`-t fast-deploy`
: only run tasks with this tag — typically "pull the latest code and rebuild"

`-K`
: prompt for the privilege-escalation password

:::{note}
Ansible needs passwordless SSH access to the hosts it manages. The inventory
files, host names and credentials for the team networks are internal and are
not published here — ask your team.
:::

{{ carologistics }} The Carologistics team uses Ansible for both robot
deployment and developer workstation setup. See the
[Carologistics page](../platforms/carologistics-robotino.md).

## Task

:::{admonition} Task: integrate, break, repair
:class: task

**Part 1 — One command.**

Restructure your launch files so that a single `ros2 launch` brings up your
entire system in the correct order: drivers, TF, localization, navigation,
mission control. Move every hard-coded value into a config file.

**Part 2 — Record a mission.**

1. Start recording: `ros2 bag record -o mini_mission /scan /odom /tf
   /tf_static /cmd_vel`
2. Run a small mission: navigate to a goal, detect something, come back.
3. Stop the recording and check it with `ros2 bag info`.
4. Replay it with `--clock` and visualize in RViz.

**Part 3 — Find the planted fault.**

Your instructor will hand you a launch or config file with **one** deliberate
fault. It may be a renamed topic, a wrong frame, a QoS mismatch, an incorrect
`use_sim_time`, or a node missing from the lifecycle manager.

Find it using the eight-step procedure above. **Write down which step revealed
it** — that is the part worth discussing afterwards.

**Part 4 — Plant one yourself.**

Swap systems with another pair. Introduce exactly one realistic fault into
theirs and let them find it. Then compare: how long did each take, and which
diagnostic step found it?
:::

:::{admonition} Expected result
:class: result

Part 1: `ros2 launch robot_bringup robot.launch.yaml` brings the system to a
state where you can immediately send a navigation goal.

Part 2: `ros2 bag info` shows all five topics with sensible message counts, and
the replay reproduces the run in RViz.

Parts 3 and 4: the fault found, and — more importantly — a diagnostic step that
found it rather than a lucky guess.
:::

:::{dropdown} Hint: faults worth planting
:icon: light-bulb

Good planted faults are realistic, single-cause, and invisible in the source
until you look:

- rename `/scan` to `/scan_raw` in one config file only;
- set `use_sim_time: true` on exactly one node;
- change `base_link` to `base_footprint` in the AMCL parameters;
- remove one node from the lifecycle manager's `node_names`;
- set `inflation_radius` to 1.5 m so no path can ever be planned;
- change a static transform's rotation by π;
- point a map's `yaml_filename` at a file that does not exist.

Each produces a different symptom and is found at a different step. That is the
lesson: the symptom tells you where to look.
:::

## Common mistakes

**Everything works separately but not together.**
Topic names, frames or QoS do not match at one interface. Work through the
procedure rather than guessing.

**The system works today and not tomorrow.**
Something is not in version control, or a value is hard-coded that should be
configuration.

**A bag replays but nothing appears in RViz.**
`/tf_static` was not recorded, or `use_sim_time` is not set on the consumers,
or `--clock` was omitted.

**Debugging by changing things.**
Change one thing at a time and observe. Changing three things and finding it
works teaches you nothing, and you will not know which to keep.

**No logs when it matters.**
Add `info` logging at the decision points of your mission *before* the
hackathon, not during it.

## Before the hackathon

A checklist worth actually running through:

- [ ] One command brings up the whole system.
- [ ] The system starts from cold with no manual steps.
- [ ] Every configuration value lives in a config file, in git.
- [ ] Rosbag recording is one command you know by heart.
- [ ] Your mission logs enough to reconstruct what it did.
- [ ] You can restore a known-good state from git in under a minute.
- [ ] Batteries are charged and you know how long they last.
- [ ] Every team member can start the robot.

## Further reading

- [ROS 2 launch documentation](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Launch-Main.html)
- [ros2 bag](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data.html)
- [ROS 2 logging](https://docs.ros.org/en/jazzy/Tutorials/Demos/Logging-and-logger-configuration.html)
- [Ansible documentation](https://docs.ansible.com/)
- [The hackathon](hackathon.md) — what all of this is for
