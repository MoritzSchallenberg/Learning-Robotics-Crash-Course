# Nodes and packages

{{ common }} {{ core }}

## What this topic is

A **node** is one program doing one job — a LiDAR driver is a node, a
path planner is a node. A **package** is the unit you build: nodes,
launch files and configuration, installed together with `colcon`. Nodes
start and stop independently of each other.

## Why a robot needs it

A robot is not one program. Splitting it into many small, independent
nodes means a sensor driver can crash and restart without taking the
planner down with it, and means you can swap one node (a different
camera driver, say) without touching anything else — the whole point of
[module 2's system-level explanation](../02-ros2.md#how-the-complete-system-fits-together).

## How it works

Each node registers itself with the ROS 2 graph when it starts, and the
CLI can list and inspect any running node without you reading its source
code.

## Try it yourself: preparing and starting turtlesim

Install turtlesim and rqt's plugin set — the second, `ros-humble-rqt*`,
pulls in `rqt_graph` and the rest of rqt's plugins used later in this
module:

```bash
sudo apt update
sudo apt install ros-humble-turtlesim ros-humble-rqt*
source /opt/ros/humble/setup.bash
```

**Verification**:

```bash
ros2 pkg executables turtlesim
```

**Expected result**: a list including at least `turtlesim
draw_square`, `turtlesim turtle_teleop_key` and `turtlesim
turtlesim_node`. If the command reports "package not found", the install
did not complete or this terminal was not sourced after it.

Open two terminals, both sourced (`echo $ROS_DISTRO` should print
`humble` in each).

Terminal 1:

```bash
ros2 run turtlesim turtlesim_node
```

Terminal 2:

```bash
ros2 run turtlesim turtle_teleop_key
```

**Expected result**: a window opens with a turtle in the middle
(terminal 1), and terminal 2 prints instructions for the arrow keys.
Click into terminal 2's window (it needs keyboard focus, not the turtle
window) and drive with the arrow keys — the turtle moves, and releasing
the key stops it.

This is **two separate nodes**, not one program with a GUI:

- `turtlesim_node` is the simulator itself — it owns the turtle's actual
  position and redraws the window every cycle. It has no idea what a
  keyboard is.
- `turtle_teleop_key` only reads your keypresses and turns them into
  `Twist` messages on a topic. It has no idea what a turtle looks like.

Neither program imports the other, and neither would need to change if
you swapped a real robot in for the simulated turtle. Each terminal
needed `source /opt/ros/humble/setup.bash` (directly or via `.bashrc`)
because that is what puts the `ros2` command and the turtlesim libraries
on that terminal's path; a terminal that skips it cannot find either.

**Why the turtle stops when you release the key**: `turtle_teleop_key`
only publishes a movement command *while a key is held*, and immediately
publishes a **zero** `Twist` the instant you let go. The turtle is not
"decelerating" — it is receiving an explicit stop command every time. You
will reproduce this exact behaviour yourself in
[the turtle controller task](turtle-controller.md).

Leave both terminals running for the rest of this lab.

## Inspecting nodes

In a third terminal:

```bash
ros2 node list
```

**Expected result**:

```text
/turtlesim
/teleop_turtle
```

Now look inside each one:

```bash
ros2 node info /turtlesim
ros2 node info /teleop_turtle
```

`ros2 node info` lists everything a node publishes, subscribes to, and
offers as a service or action — the node's entire footprint on the ROS
graph, without reading a line of its source code. Expect `/turtlesim` to
show, among others, a subscriber on `/turtle1/cmd_vel`, publishers
including `/turtle1/pose`, several **Service Servers** (`/spawn`, `/kill`,
`/clear` among them), and one **Action Server**
(`/turtle1/rotate_absolute`). Expect `/teleop_turtle` to show mainly a
publisher on `/turtle1/cmd_vel` and, since it is what actually drives the
rotate action when you press the rotation keys, an **Action Client** for
that same action name.

:::{admonition} Task: draw the communication diagram
:class: task

From the two `ros2 node info` outputs alone — no source code — draw two
boxes, `/turtlesim` and `/teleop_turtle`, and one labelled arrow between
them for every publisher/subscriber or client/server pair you found.
:::

## Expected result

Two nodes running, correctly named in `ros2 node list`, and a diagram you
drew yourself from their `ros2 node info` output alone.

## Verification

Your diagram should have at least one arrow from `/teleop_turtle` to
`/turtlesim` (the `cmd_vel` topic) and, if you found the rotate action
pair, a second arrow the other way for feedback and result. If you only
drew one arrow total, look again at `/turtlesim`'s publishers —
`/teleop_turtle` does not subscribe to any of them, which is worth
noticing: teleop only ever sends, it never listens.

## How ALeRT applies it

{{ alert }} {{ simulation }} Webots Spot is the same idea at a larger
scale: `ros2 node list` after `ros2 launch webots_spot spot_launch.py`
returns many more nodes than turtlesim's two — drivers, a state
publisher, perception nodes — but each one is still one program doing
one job. See [this module's overview](../02-ros2.md#how-alert-uses-this-topic)
and [Try it on Spot](practical-exercises.md#try-it-on-spot) for the
exercise applying `ros2 node list`/`ros2 node info` there directly.

## How Carologistics applies it

{{ carologistics }} {{ documented }} Robotino's node graph (see the
[platform page](../../platforms/carologistics-robotino.md#software-stack))
includes a base-motion driver, a laser driver, vision nodes and Nav2 —
the same "many small nodes, not one program" architecture, run
continuously on real hardware rather than started fresh for a lab
exercise.

## Common problems

- **`Package 'turtlesim' not found`** — the install above did not
  complete, or this terminal was opened before it finished.
- **Nothing happens when I press arrow keys.** `turtle_teleop_key`'s
  *terminal window*, not the turtle window, needs keyboard focus.

## Next subtopic

[Topics and messages](topics-and-messages.md) — inspect what
`/turtle1/cmd_vel` actually carries, and drive the turtle yourself
without the keyboard at all.

## Sources

- [ROS 2: Understanding nodes](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes.html)
- [ROS 2: Using turtlesim, ros2, and rqt](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Introducing-Turtlesim/Introducing-Turtlesim.html)
