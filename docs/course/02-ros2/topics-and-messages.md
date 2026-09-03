# Topics and messages

{{ common }} {{ core }}

## What this topic is

A **topic** is a named channel carrying messages of one type. A
**message** is the typed structure sent on it — not a Python string, but
a defined type such as `geometry_msgs/msg/Twist`, which has named fields
(`linear`, `angular`).

## Why a robot needs it

Publishers and subscribers never know about each other directly:
asynchronous, one to many, no reply expected. That is what lets you
swap a real sensor in for a simulated one without touching the node that
consumes its data — they only ever agreed on the topic's name and type.

## Inputs and outputs

A topic has any number of publishers and any number of subscribers, all
agreeing on one message type. `/turtle1/cmd_vel` carries
`geometry_msgs/msg/Twist`: two 3D vectors, `linear` (metres per second)
and `angular` (radians per second) — turtlesim only reads `linear.x` and
`angular.z`, since it lives in a 2D plane.

## Try it yourself: inspecting topics

```bash
ros2 topic list
ros2 topic list -t
```

`-t` adds each topic's message type in brackets — `/turtle1/cmd_vel
[geometry_msgs/msg/Twist]` is the one this page cares about.

```bash
ros2 topic info /turtle1/cmd_vel
ros2 topic info -v /turtle1/cmd_vel
```

The plain version names the type and counts publishers/subscribers; `-v`
additionally prints each side's QoS profile — the setting behind the
"nothing arrives and there is no error" failure class you will meet
properly in [module 3](../03-sensors-tf/practical-exercise.md#common-problems), and
reproduce on purpose in [Continue learning](continue-learning.md).

```bash
ros2 topic echo /turtle1/pose
```

**Expected result**: a stream of `x`, `y`, `theta`, `linear_velocity`,
`angular_velocity` values, updating continuously even if you are not
driving — the simulator publishes pose every cycle regardless. Stop it
with <kbd>Ctrl</kbd>+<kbd>C</kbd>.

```bash
ros2 topic hz /turtle1/pose
```

**Expected result**: an average rate around 62 Hz (turtlesim's fixed
simulation rate), printed continuously. This is the same tool
[module 8](../08-integration/continue-learning.md) uses to check whether
a real sensor is actually publishing at the rate it claims to.

```bash
ros2 interface show geometry_msgs/msg/Twist
```

**Expected result**:

```text
Vector3  linear
        float64 x
        float64 y
        float64 z
Vector3  angular
        float64 x
        float64 y
        float64 z
```

`/turtle1/cmd_vel` is published **continuously** rather than once because
that is what makes "no command yet" and "explicit stop" the same,
unambiguous state — the value simply holds at whatever was last sent,
exactly as you saw when releasing an arrow key sends an explicit
all-zero `Twist`.

## Try it yourself: moving the turtle without the keyboard

`turtle_teleop_key` is nothing special — it is just another node
publishing `Twist` messages. You can do exactly what it does directly
from the command line, with `ros2 topic pub`.

:::{warning}
Every command below **runs continuously** at 1 Hz until you press
<kbd>Ctrl</kbd>+<kbd>C</kbd> — the turtle keeps moving the whole time. Have
your finger ready, and expect to press it after a second or two.
:::

**1. Drive straight:**

```bash
ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```

**Expected result**: the turtle drives forward in a straight line until
you cancel the command, then keeps its last velocity until a new message
arrives — cancelling `ros2 topic pub` and then pressing an arrow key once
is the cleanest way to bring it fully to rest.

**2. Turn in place:**

```bash
ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.0}}"
```

**3. Drive in a circle** (both at once):

```bash
ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.8}}"
```

:::{admonition} Task: predict, then check
:class: task

Before running command 3 above, predict: will a **larger** `angular.z`
(with `linear.x` unchanged) make the circle bigger or smaller? Write your
answer down, then run it with `angular.z: 3.6` (double) and compare.
:::

## Expected result

A tighter (smaller-radius) circle with the doubled `angular.z`. The
turtle turns more per second of forward travel, so it curves harder —
the ratio of `linear.x` to `angular.z` sets the circle's radius, not
either value alone.

## Verification

If your prediction was "bigger", that is worth noticing directly: many
people expect "more turning" to mean "a wider circle", when it is the
opposite. Cancel any still-running `topic pub` with
<kbd>Ctrl</kbd>+<kbd>C</kbd> before continuing.

## How ALeRT applies it

{{ alert }} {{ simulation }} Spot's odometry, point cloud and camera
image are all topics, continuously published exactly like
`/turtle1/pose` — see [this module's Try it on
Spot](practical-exercises.md#try-it-on-spot) for sorting Spot's real
topics into sensor/motion/state categories yourself.

## How Carologistics applies it

{{ carologistics }} {{ documented }} Robotino's laser scans and base
odometry are topics in the same sense; the
[`laser_scan_integrator`](../../platforms/carologistics-robotino.md#key-repositories)
node specifically exists to merge two scan topics into one, using TF to
account for the sensors' relative positions — a topic-to-topic
transformation, not a special ROS 2 mechanism.

## Common problems

- **`ros2 topic pub` seems to hang.** It is not hanging — it is
  publishing continuously at 1 Hz by design. Press
  <kbd>Ctrl</kbd>+<kbd>C</kbd>.
- **Nothing prints from `ros2 topic echo`.** Confirm the topic name with
  `ros2 topic list` first — a typo produces silence, not an error.

## Next subtopic

[Services, parameters and actions](services-parameters-actions.md) — the
three tools ROS 2 offers when a continuous stream is the wrong shape for
the job.
