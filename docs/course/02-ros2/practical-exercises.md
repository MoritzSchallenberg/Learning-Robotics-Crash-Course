# Practical exercises

{{ optional }}

## The turtlesim challenge

> Spawn a second turtle, and make the first turtle move through a
> reproducible geometric path without any keyboard control.

You already have everything this needs from the earlier subtopics:
`/spawn` ([services](services-parameters-actions.md)), a timer-driven
`Twist` publisher (your own [controller](turtle-controller.md)). Pick at
least one extension:

- Subscribe to `/turtle1/pose` in your controller and log the position at
  each corner, instead of only trusting the timing.
- Have the controller stop early if the turtle's `x` or `y` gets within a
  fixed margin of the window edge (turtlesim's window is roughly 11×11
  units, origin at the bottom-left) — a first taste of the obstacle-margin
  thinking [module 6](../06-navigation/nav2-architecture-and-costmaps.md#how-it-works) covers properly.
- Spawn a second turtle and have your controller's node publish to
  `/turtle2/cmd_vel` as well, driving both through different paths at
  once from one process.
- Record the run: `ros2 bag record /turtle1/cmd_vel /turtle1/pose`, then
  play it back and confirm `ros2 topic echo` during playback matches what
  you saw live — the same rosbag pattern
  [module 8](../08-integration.md#core-concepts) uses for a real robot.

**Expected result**: a reproducible path — running the same controller
twice produces the same shape, not a random one.

**Verification**: re-run your controller from a fresh `turtlesim_node`
twice, and confirm both runs draw the same figure.

## Try it on Spot

{{ alert }} {{ spotsim }}

Run this module's inspection commands against
[Webots Spot](../../platforms/alert-spot.md#the-webots-spot-simulation)
instead of turtlesim, and compare what changed and what did not.

```bash
ros2 launch webots_spot spot_launch.py
```

Then, in another terminal:

```bash
ros2 node list
ros2 topic list -t
ros2 service list -t
ros2 action list -t
ros2 topic hz /scan
rqt_graph
```

:::{warning}
Check the topic and node names your own launch actually produces before
assuming any of the ones below — simulation repository branches change
these over time. `ros2 topic list` is always the ground truth, not this
page.
:::

- Assign at least five of the listed nodes to a job, the same way you
  assigned `/turtlesim` and `/teleop_turtle` in
  [Nodes and packages](nodes-and-packages.md).
- Sort the topics you find into **sensor** (e.g. the LiDAR/point-cloud and
  camera topics), **motion** (`/cmd_vel`) and **state** (odometry) — the
  same three-way split
  [Topics and messages](topics-and-messages.md) implicitly used for
  turtlesim's much smaller graph.
- Open `rqt_graph` and compare it to the two-node turtlesim graph you saw
  earlier: what is fundamentally the same (nodes as ovals, topics as
  rectangles, the same publish/subscribe arrows), and what is just
  *more of* it (many more nodes and topics, not a different kind of
  system)?

**Expected result**: a full node/topic inventory of the Spot simulation,
sorted into the same categories turtlesim's much smaller graph used.

**Verification**: you should be able to point at one topic from each of
the three categories above and name the node that publishes it.

## Common problems

- **`ros2 topic pub` seems to hang.** Not a bug — see
  [Topics and messages](topics-and-messages.md#common-problems).
- **Recorded bag replays but `ros2 topic echo` shows nothing.** Confirm
  the topic name matches exactly, and that no other node is still
  publishing zeros on top of the replay.

## Next subtopic

[Interesting videos](videos.md) — one carefully checked recommendation —
and then [Continue learning](continue-learning.md) for what to build
next.

## Sources

- [ROS 2: Recording and playing back data](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data.html)
