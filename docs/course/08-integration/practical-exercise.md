# Practical exercise

{{ common }} {{ core }}

## Goal

Find one deliberately introduced fault using the eight-step procedure, fix
it, then run a complete mini-mission end to end.

## Starting point

A working `robot_bringup` launch file from your previous modules, and one
fault from
[System bring-up and diagnostics' Try it
yourself](system-bringup-and-diagnostics.md#try-it-yourself) table — pick
one you have not tried yet, or ask someone else to pick one for you
without telling you which.

## Steps

1. Apply one fault from the table to a copy of your launch file, then
   `ros2 launch robot_bringup robot.launch.yaml` — note what looks wrong.
2. Work through
   {ref}`the eight-step procedure <the-eight-step-diagnostic-procedure>`
   above, in order, **without changing anything yet**.
3. Write down the step number where the fault first became visible.
4. Fix only that one thing.
5. Re-launch and confirm the symptom is gone.
6. Record a bag of the fixed system:
   `ros2 bag record -o mini_mission /scan /odom /tf /tf_static /cmd_vel`
7. Run the full mini-mission from
   [module 7](../07-autonomous-decisions.md): navigate, detect, report,
   return — while the bag records.

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

## Try it on Spot

{{ alert }} {{ spotsim }}

Run this module's eight-step diagnostic procedure against the full Webots
Spot stack instead of a small `robot_bringup` launch file — a genuinely
bigger system is exactly where a systematic procedure earns its keep over
guessing:

1. Bring up drivers, SLAM or navigation, and any perception node you have
   working, in the order
   {ref}`System bring-up and diagnostics' startup order <startup-order>`
   describes (drivers and TF first, localization next, navigation last).
2. Confirm node, topic and TF state with the same commands as this
   module's practical task (`ros2 node list`, `ros2 topic hz` on at least
   the LiDAR and odometry topics, `ros2 run tf2_tools view_frames`).
3. Record a rosbag of the whole system running normally for about a
   minute: `ros2 bag record /scan /Spot/odometry /tf /tf_static -o
   spot_baseline`.
4. Pick one fault from [System bring-up and diagnostics' own fault
   table](system-bringup-and-diagnostics.md#try-it-yourself) and apply it
   to a **copy** of Spot's launch configuration.
5. Work the eight-step procedure, in order, without changing anything
   yet, and note the step where the fault first became visible.
6. Fix it, confirm the symptom is gone, and record a second, fixed-state
   rosbag.

**Verification**: identical to this module's own — the fault is found and
named by diagnostic step number, and both rosbags (baseline and
post-fault, or fixed) exist and replay correctly.

:::{note}
{{ spotreadonly }} This exercise is read-only with respect to the
*physical* robot's actuators — inspecting a running system's diagnostics
does not require moving anything. If your "system" for this exercise
includes real Spot hardware rather than only Webots, keep it stationary
(standing or sitting, not navigating) for the duration of this exercise.
:::

## Next subtopic

[Interesting videos](videos.md) — recording and replaying a rosbag,
step by step.

## Sources

- [Diagnostic sequence](../../reference/ros2-cheatsheet.md#diagnostic-sequence)
