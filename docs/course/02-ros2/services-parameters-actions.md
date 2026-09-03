# Services, parameters and actions

{{ common }} {{ core }}

## What this topic is

Three more ways nodes exchange data, each shaped for a job a topic is not:

- **Service** — a request and a synchronous response, like calling a
  function over the network: you ask, you wait, you get exactly one
  answer.
- **Parameter** — a named, typed configuration value a node exposes,
  that you can read and — if the node allows it — change while it runs.
- **Action** — a goal that takes time, reports progress as it goes
  (**feedback**), and can be cancelled before it produces a final
  **result**. The one tool of the three that is not immediate.

## Why a robot needs it

"Stand up" is not a stream you publish forever — it is a request with
one outcome. "How fast should the wheels spin" is not something you
recompile for — it is a live, readable, settable value. "Navigate to
that door" is neither instant nor a fire-and-forget stream — it needs
progress and the ability to change your mind. Three different shapes,
three different tools.

## Try it yourself: services

```bash
ros2 service list
ros2 service list -t
ros2 service type /spawn
ros2 interface show turtlesim/srv/Spawn
```

**Expected result** for the last command:

```text
float32 x
float32 y
float32 theta
string name # Optional.  A unique name will be created and returned if this is empty
---
string name
```

Everything above the `---` is the **request** you send; everything below
is the **response** you get back — the shape every service has, unlike a
topic's one-way message.

**Spawn a second turtle:**

```bash
ros2 service call /spawn turtlesim/srv/Spawn "{x: 2, y: 2, theta: 0.2, name: ''}"
```

**Expected result**: a second turtle appears at `(2, 2)`, and the response
prints the name it was auto-assigned (typically `turtle2`, since the name
field was left empty).

**Clear the background:**

```bash
ros2 service call /clear std_srvs/srv/Empty
```

**Expected result**: any trail lines both turtles have drawn disappear;
the turtles themselves stay where they are. `std_srvs/srv/Empty` is a
request and response with **no fields at all** — some services exist
purely to trigger an action, with nothing to configure.

**Remove a turtle, then respawn it elsewhere:**

```bash
ros2 service call /kill turtlesim/srv/Kill "{name: 'turtle2'}"
ros2 service call /spawn turtlesim/srv/Spawn "{x: 8, y: 8, theta: 0.0, name: 'turtle2'}"
```

**Expected result**: `turtle2` disappears, then reappears at `(8, 8)` —
this time with its name given explicitly rather than auto-assigned.

**Verification — topic vs. service, from what you just did**: `ros2
topic pub` (previous page) ran **continuously**, publishing the same
`Twist` every second until you stopped it, and nothing ever confirmed it
arrived. Every `ros2 service call` above ran **exactly once**, returned
**one specific answer** (a name, or nothing for `/clear`), and then
finished on its own — no `Ctrl`+`C` needed.

## Try it yourself: parameters

```bash
ros2 param list /turtlesim
ros2 param get /turtlesim background_r
```

**Expected result** for `get`: a line like `Integer value is: 69`
(turtlesim's default background is a shade of blue-teal; `background_r`,
`_g` and `_b` are its three RGB components, each 0–255).

```bash
ros2 param set /turtlesim background_r 150
```

**Expected result**: the background colour changes. If it does not
appear to change immediately, call
`ros2 service call /clear std_srvs/srv/Empty` — the parameter is a live
setting either way (confirm it with `ros2 param get` right after `set`),
but the window only *redraws* on certain events, and `/clear` is the
reliable way to force one.

:::{important}
`ros2 param set` only changes the value **for as long as this node keeps
running** — it is not written back to any file, and a fresh
`turtlesim_node` starts again from the defaults. Use `ros2 param dump`,
below, if you actually want to keep a set of values.
:::

```bash
ros2 param dump /turtlesim
```

**Expected result**: the node's entire current parameter set, printed as
YAML — useful for capturing exactly what a working configuration looked
like.

:::{warning}
**Setting a parameter the node never declared does not silently do
nothing — it fails, visibly.** Try it:

```bash
ros2 param set /turtlesim not_a_real_parameter 1
```

Expect the CLI to report the set as failed (a message to the effect of
"Setting parameter failed", because the node's parameter service rejects
an undeclared name) rather than accepting it quietly. If you ever see a
`param set` you *expect* to work produce this failure, the actual bug is
almost always a typo in the parameter's name, not a mysterious silent
no-op.
:::

## Try it yourself: actions

```bash
ros2 action list
ros2 action list -t
ros2 action info /turtle1/rotate_absolute
ros2 interface show turtlesim/action/RotateAbsolute
```

**Expected result** for the last command:

```text
# The desired heading in radians
float32 theta
---
# The angular displacement in radians to the starting position
float32 delta
---
# The remaining rotation in radians
float32 remaining
```

Three sections, in order: **goal** (what you ask for — a heading, in
radians), **result** (what you get once it finishes), **feedback** (what
you get *while it runs* — here, how much rotation is left).

**Send a goal, and watch feedback stream in:**

```bash
ros2 action send_goal /turtle1/rotate_absolute turtlesim/action/RotateAbsolute "{theta: 1.57}" --feedback
```

**Expected result**: the turtle rotates to face straight up
(1.57 rad ≈ 90°), the terminal prints a `remaining` feedback value that
counts down toward zero as it turns, and finally prints the result
(`delta`, the total angular displacement) once it stops. Unlike
`topic pub`, you did not need to cancel anything — the action finished on
its own once the goal was reached.

**Cancel a goal in progress**: run the command again with a large turn
(`{theta: -3.0}`, more than half a full rotation) and press
<kbd>Ctrl</kbd>+<kbd>C</kbd> partway through. `Ctrl`+`C` here kills the
CLI client, not necessarily the action itself — see
[Continue learning](continue-learning.md) for cancelling an action
*properly*, from code, with `cancel_goal_async()`.

## Try it yourself: seeing the whole graph

```bash
rqt_graph
```

**Expected result**: a window with nodes as ovals and topics as
rectangles, arrows showing data flow — `/teleop_turtle` →
`/turtle1/cmd_vel` → `/turtlesim`, and similar for every other connection
you already found by hand with `ros2 node info`. By default, debug-only
topics like `/parameter_events` and `/rosout` are hidden behind a
checkbox in the top-left ("Hide: Debug") — untick it if you want to see
everything, including the noise a real system also carries.

:::{admonition} Task: compare CLI and graph
:class: task

Spawn a third turtle (`ros2 service call /spawn ...` again, any
position), then refresh `rqt_graph` (the refresh button, top-left). What
changed in the graph? Does the new turtle have its own `cmd_vel` topic,
or does it share one with the others?
:::

## Expected result

A graph you can read at a glance, matching everything you already found
by hand — and a third turtle that has topics but no controller.

## Verification

A new turtle spawned this way has **no** teleop node publishing to it —
only `/turtlesim` itself gains a new set of `/turtle3/...` topics (pose,
color_sensor) with nothing publishing `/turtle3/cmd_vel`. This is worth
noticing before [the turtle controller task](turtle-controller.md):
spawning a turtle and *controlling* it are two separate things.

## How ALeRT applies it

{{ alert }} Spot's postures are exposed as **services**
(`/Spot/stand_up`, `/Spot/sit_down`, `/Spot/lie_down`, type
`webots_spot_msgs/srv/SpotMotion`) rather than topics or actions — a
natural fit, since standing up either succeeds or does not, with no
meaningful "progress" to report partway through. See the [platform
page](../../platforms/alert-spot.md#services-and-actions) for the exact
calls, and [module 7's Try it on
Spot](../07-autonomous-decisions.md#try-it-on-spot) for building a
mission state machine around them.

## How Carologistics applies it

{{ carologistics }} {{ unverified }} The exact ROS 2 service and action
interfaces used by Robotino's gripper controller and its CLIPS-Executive
agent are not documented in public repository READMEs at the time of
writing. Treat any specific interface name for those two components as
`Not documented` rather than assumed — see [this module's team
comparison](../02-ros2.md#alert-and-carologistics-compared).

## Common problems

- **`ros2 param set` reports the set failed.** Either a typo in the
  parameter name (the common case — check `ros2 param list` for the
  exact spelling), or you are trying to set a parameter the node never
  declared, which is supposed to fail loudly, not silently.

## Next subtopic

[Write your own turtle controller](turtle-controller.md) — this
module's practical task, replacing `turtle_teleop_key` with your own
`rclpy` node.

## Sources

- [ROS 2: Understanding services](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html)
- [ROS 2: Understanding parameters](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters.html)
- [ROS 2: Understanding actions](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html)
