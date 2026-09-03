# Write your own turtle controller

{{ common }} {{ core }}

## What this topic is

This module's practical task: an `rclpy` node that replaces
`turtle_teleop_key` entirely — driving turtlesim's turtle through a
square using only a timer callback and a small state machine, no
keyboard involved.

## Why a robot needs it

Every node you have run so far in this module (`turtlesim_node`,
`turtle_teleop_key`) was written by someone else. This is where you find
out that neither was doing anything magical — creating a publisher and a
timer is a handful of lines, and the rest is exactly the state-machine
thinking [module 7](../07-autonomous-decisions.md) formalises properly
later.

## Goal

Replace `turtle_teleop_key` with your own `rclpy` node: a controller that
drives the turtle through a square, using only a timer callback and a
small state machine — no keyboard involved.

## Starting point

The `turtle_course` package in this repository, at
`examples/module02_turtlesim/turtle_course/` — a real, `colcon`-buildable
ROS 2 Humble package with a starter file full of `# TODO` markers. Copy it
into your own workspace:

```bash
cp -r examples/module02_turtlesim/turtle_course ~/course_ws/src/
cd ~/course_ws
colcon build --packages-select turtle_course
source install/setup.bash
```

Open `~/course_ws/src/turtle_course/turtle_course/turtle_controller.py` in
your editor. It is one file, roughly 100 lines, with **8 numbered
`# TODO` blocks**. Every piece you need — creating a publisher, creating a
timer, building and publishing a `Twist` — is something you already ran
by hand in [Topics and messages](topics-and-messages.md), against the
exact same topic.

## Steps

1. **TODO 1–2**: create the publisher (`/turtle1/cmd_vel`,
   `geometry_msgs/msg/Twist`, queue size 10) and a timer that calls
   `self.control_loop` every `TIMER_PERIOD` seconds. Both are one line
   each — `self.create_publisher(...)` and `self.create_timer(...)`.
2. **TODO 3–4**: in the `DRIVE` state, set `msg.linear.x` to
   `FORWARD_SPEED`; once `DRIVE_SECONDS` has elapsed, switch to `TURN` and
   reset the elapsed-time counter.
3. **TODO 5**: in the `TURN` state, set `msg.angular.z` to `TURN_SPEED`.
4. **TODO 6**: once four sides are complete, switch to `DONE`.
5. **TODO 7–8**: publish `msg` at the end of every control step, and give
   `stop_turtle()` a real, all-zero `Twist()` to publish.
6. Build and run:

   ```bash
   colcon build --packages-select turtle_course
   source install/setup.bash
   ros2 run turtle_course turtle_controller
   ```

   against a `turtlesim_node` you have already reset with `/clear` and,
   if it is not centred, a fresh `turtlesim_node` restart.

Stuck for more than a few minutes on any one `TODO`? The reference
solution is in `examples/module02_turtlesim/solutions/`, and also
reproduced below.

:::{dropdown} Solution
:icon: unlock

```python
from enum import auto, Enum

from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node


class State(Enum):
    DRIVE = auto()
    TURN = auto()
    DONE = auto()


FORWARD_SPEED = 1.5
DRIVE_SECONDS = 2.0
TURN_SPEED = 0.785398  # pi/4 rad/s -> 90 degrees in TURN_SECONDS
TURN_SECONDS = 2.0
SIDES = 4
TIMER_PERIOD = 0.1


class TurtleController(Node):
    """Drive turtlesim's turtle through a square, then stop."""

    def __init__(self):
        super().__init__('turtle_controller')
        self.cmd_vel_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.state = State.DRIVE
        self.sides_completed = 0
        self.elapsed_in_state = 0.0
        self.timer = self.create_timer(TIMER_PERIOD, self.control_loop)
        self.get_logger().info(f'Starting: driving a {SIDES}-sided figure.')

    def control_loop(self):
        if self.state is State.DONE:
            return
        self.elapsed_in_state += TIMER_PERIOD
        msg = Twist()

        if self.state is State.DRIVE:
            msg.linear.x = FORWARD_SPEED
            if self.elapsed_in_state >= DRIVE_SECONDS:
                self.state = State.TURN
                self.elapsed_in_state = 0.0

        elif self.state is State.TURN:
            msg.angular.z = TURN_SPEED
            if self.elapsed_in_state >= TURN_SECONDS:
                self.sides_completed += 1
                self.get_logger().info(f'Side {self.sides_completed}/{SIDES} complete.')
                if self.sides_completed >= SIDES:
                    self.state = State.DONE
                    self.stop_turtle()
                    self.get_logger().info('Figure complete. Stopping.')
                    return
                self.state = State.DRIVE
                self.elapsed_in_state = 0.0

        self.cmd_vel_pub.publish(msg)

    def stop_turtle(self):
        self.cmd_vel_pub.publish(Twist())


def main():
    rclpy.init()
    node = TurtleController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```
:::

## Expected result

The turtle drives four sides of roughly equal length, turning
approximately 90° at each corner, ending close to its original heading,
then stops on its own — no keyboard, no `topic pub`, no service call.

## Verification

```bash
ros2 topic echo /turtle1/pose --once
```

Note the `theta` value once the node logs "Figure complete." — it should
be close to the value `theta` had when the node started (within a few
tenths of a radian; the timer-based timing is not perfectly exact, and
that imprecision is itself worth noticing, not a bug to chase). Separately,
`ros2 node info /turtle_controller` should show exactly one publisher
(`/turtle1/cmd_vel`) and nothing else — a minimal, single-purpose node,
same as `turtle_teleop_key` was.

## Check your understanding

Before moving on, you should be able to answer all of these — out loud, to
someone else, or just to yourself — without looking anything up:

- Which nodes are running right now, and what does each one actually do?
- Which topic steers the turtle, and what message type is on it?
- How do you publish a message onto a topic by hand, with no code at all?
- What is actually different about a service call compared to a topic
  publish — not just "different command", but different in what sense?
- Why does an action need feedback and cancellation when a service does
  not?
- Where does your own `turtle_controller` node fit into the graph you saw
  in `rqt_graph` — what does it publish, and what, if anything, does it
  subscribe to?

## How ALeRT and Carologistics apply this

{{ alert }} {{ carologistics }} Both teams' driver and controller nodes
are the same shape as `turtle_controller`: a publisher, a timer or
sensor-driven callback, and internal state — just with real sensor
feedback closing the loop instead of a fixed timer, which is exactly the
gap [module 3](../03-sensors-tf.md) and
[module 6](../06-navigation.md) close.

## Common problems

- **My own node builds but `ros2 run turtle_course turtle_controller`
  says "package not found".** The workspace was not sourced in *this*
  terminal after the build — `source ~/course_ws/install/setup.bash`.
- **The turtle does not move at all when I run my node.** Check `ros2
  topic echo /turtle1/cmd_vel` in a second terminal while your node runs
  — if nothing appears there, TODO 7 (the actual `.publish(msg)` call) is
  still a `pass`.
- **The turtle moves but never turns**, or turns forever without driving
  — a state-transition TODO (4 or 6) still says `pass` instead of
  actually reassigning `self.state`.

## Next subtopic

[Practical exercises](practical-exercises.md) — the turtlesim challenge,
and this module's Try it on Spot section.

## Sources

- [Writing a simple publisher and subscriber (Python)](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html)
- `examples/module02_turtlesim/` in this repository
