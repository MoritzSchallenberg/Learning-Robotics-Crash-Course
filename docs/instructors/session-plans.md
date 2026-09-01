# Session plans

Facilitator notes per session — what to pre-build, what to print, what to
plant, and what tends to go wrong on that particular evening. Read alongside
that session's own page; this does not repeat its run sheet or theory.

## Session 1 — System Architecture and Robot Hardware

**[Session page](../course/01-system-hardware.md)**

**Pre-build**: nothing. This is the one evening with no software
dependency.

**Bring**: a real robot if available, or printed photos/diagrams of one; a
whiteboard or paper and markers for the drawing task, enough for one sheet
per pair.

**Watch for**: participants drawing data and power as the same line style —
this is the single most common mistake on this page and worth catching
early, in the first five minutes of the practical task, not at the end.

**If no robot is available**: the task works from a description alone; hand
out the one-page hardware description referenced in the task's "Starting
point" instead.

## Session 2 — ROS 2 Fundamentals

**[Session page](../course/02-ros2.md)**

**Pre-build**: a workspace at `~/course_ws` containing a package
`pubsub_demo` with a working publisher node `talker.py`, publishing on
`/course_chat` with a declared `message` parameter and a declared publish
rate. Test the full task yourself, including step 7's rebuild, before the
session — a parameter that was not `declare_parameter`'d is the most common
way this pre-build accidentally fails the task.

**Watch for**: participants running `ros2 run` in a terminal where the
workspace was never sourced — the very first command in the task. Confirm
every laptop's terminal prompt or a quick `echo $AMENT_PREFIX_PATH` shows
the workspace before starting the clock.

## Session 3 — Sensors, TF2 and RViz

**[Session page](../course/03-sensors-tf.md)**

**Pre-build**: a `robot_bringup` package with a `sensors.launch.yaml` that
starts a LiDAR (real or simulated) publishing `/scan`, **with the
`base_link` → `laser_frame` static transform deliberately absent**. Know
the correct transform values yourself so you can confirm a group's answer
quickly rather than re-deriving it live.

**Watch for**: groups setting the RViz Fixed Frame to something that does
not exist and concluding the sensor is broken — check this first if a group
calls you over for "nothing appears."

## Session 4 — Perception and Object Detection

**[Session page](../course/04-perception/index.md)**

**Pre-build**: a `perception_demo` package with `aruco_node.py` containing
the subscriber/publisher scaffolding and two `# TODO` gaps (detector
creation, `detectMarkers` call), plus a running calibrated camera topic —
real, or the simulator's, which needs no calibration.

**Print**: one ArUco marker (dictionary `DICT_6X6_50`) per group, plus
spares — laminating them means a session's wear and tear does not require
reprinting for the next intake.

**Watch for**: a group whose printed marker uses a different dictionary
than the node expects — no error, just silent non-detection. Keep one
"known good" marker on hand to rule this out quickly.

## Session 5 — Mapping and Localization

**[Session page](../course/05-mapping-localization.md)**

**Pre-build**: `robot_bringup` plus a `my_robot_slam` package with SLAM
Toolbox and AMCL already configured for your robot/simulation, and a
reasonably interesting space to map — a single straight corridor gives
poor loop-closure practice; a small loop-shaped area works better.

**Watch for**: a group driving too fast and destroying their map with 20
minutes left — this is unrecoverable within the session, so intervene the
moment you see the map start to smear rather than let them discover it
themselves.

## Session 6 — Autonomous Navigation

**[Session page](../course/06-navigation.md)**

**Pre-build**: `my_robot_navigation` with velocity and inflation parameters
matched to the actual robot/simulation in use — measure the real robot's
top speed and footprint rather than reusing a value from documentation.

**Bring**: one object per group to use as the "unmapped obstacle."

**Watch for**: the practical task's step 6 requires placing an obstacle
*while the robot is driving* — remind groups of this explicitly, since the
natural instinct is to place it before starting, which skips the actual
learning objective (observing a live re-plan).

## Session 7 — Autonomous Decisions and Manipulation

**[Session page](../course/07-autonomous-decisions.md)**

**Pre-build**: a `mission_demo` package exposing the session 6 navigation
client and session 4 marker detector as importable helper classes, so
participants write the state machine itself rather than its dependencies.

**Watch for**: groups whose mission "works" in testing only because they
never tried the no-marker or blocked-path cases from Steps 5–6 — actively
prompt groups to try both rather than waiting for them to reach it.

## Session 8

**[Session page](../course/08-integration.md)**

**Pre-build**: a working `robot_bringup` launch file, **plus one
deliberately modified copy per group** with exactly one fault — do not
reuse the same fault for every group, or the room will simply share the
answer.

Faults that work well, matched to the eight-step diagnostic procedure so
every step gets exercised across the room:

```{list-table}
:header-rows: 1
:widths: 40 30 30

* - Fault
  - Diagnostic step it teaches
  - Difficulty
* - Rename a published topic in one launch arg
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
* - Point a map's `yaml_filename` at a nonexistent file
  - Step 1–2 (node/topic)
  - Easy
```

**Watch for**: a group that "fixes" the symptom without finding the actual
fault (restarting a node instead of renaming the topic back) — ask them to
explain *why* their fix worked before confirming it as correct.

**After the session**: revert every planted fault in the shared repository
before the next group or the next course intake uses it — see the
[preparation checklist's cleanup section](preparation-checklist.md#cleanup-and-data-backup-checklist).

## The hackathon

Not a regular session — see [Hackathon setup](hackathon-setup.md) for the
full closing-event plan.
