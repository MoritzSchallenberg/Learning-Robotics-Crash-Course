#!/usr/bin/env python3
"""
Module 2 practical task -- starter file.

Drive turtlesim's turtle through a square, with no keyboard input, using
only a timer callback and a small state machine (DRIVE / TURN / DONE) --
the same state-machine shape module 7 formalises later in the course.

Fill in every ``# TODO`` block below. Nothing here is a trick: every piece
you need (the publisher, the message type, the timer pattern) was already
used in this module's guided example against the exact same topic,
`/turtle1/cmd_vel`.

Run it with:

    ros2 run turtle_course turtle_controller

...against a running `turtlesim_node` in another terminal. The solution is
in `examples/module02_turtlesim/solutions/turtle_controller_solution.py`
in this repository -- try it yourself first.
"""

from enum import auto, Enum

from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node


class State(Enum):
    DRIVE = auto()
    TURN = auto()
    DONE = auto()


# Tuned so that TURN_SECONDS of angular.z = TURN_SPEED turns exactly 90
# degrees (pi/2 radians): TURN_SPEED * TURN_SECONDS == pi / 2.
FORWARD_SPEED = 1.5    # m/s, while driving one side
DRIVE_SECONDS = 2.0    # seconds per side
TURN_SPEED = 0.785398  # rad/s (pi/4), while turning a corner
TURN_SECONDS = 2.0     # seconds per corner
SIDES = 4              # a square has four sides
TIMER_PERIOD = 0.1     # seconds between timer callbacks


class TurtleController(Node):
    """Drive turtlesim's turtle through a square, then stop."""

    def __init__(self):
        super().__init__('turtle_controller')

        # TODO 1: create a publisher on '/turtle1/cmd_vel' for Twist
        # messages, queue size 10. Store it as self.cmd_vel_pub.
        self.cmd_vel_pub = None  # replace this line

        # State machine bookkeeping.
        self.state = State.DRIVE
        self.sides_completed = 0
        self.elapsed_in_state = 0.0

        # TODO 2: create a timer that calls self.control_loop every
        # TIMER_PERIOD seconds. Store it as self.timer (not strictly
        # required to store, but useful if you want to cancel it later).
        self.timer = None  # replace this line

        self.get_logger().info(
            f'Starting: driving a {SIDES}-sided figure.'
        )

    def control_loop(self):
        """Run one control step; called every TIMER_PERIOD seconds."""
        if self.state is State.DONE:
            return

        self.elapsed_in_state += TIMER_PERIOD
        # Becomes used once TODOs 3, 5 and 7 are filled in below.
        msg = Twist()  # noqa: F841

        if self.state is State.DRIVE:
            # TODO 3: set msg.linear.x to FORWARD_SPEED so the turtle
            # drives forward while in the DRIVE state.
            pass

            if self.elapsed_in_state >= DRIVE_SECONDS:
                # TODO 4: switch self.state to State.TURN and reset
                # self.elapsed_in_state to 0.0.
                pass

        elif self.state is State.TURN:
            # TODO 5: set msg.angular.z to TURN_SPEED so the turtle turns
            # while in the TURN state.
            pass

            if self.elapsed_in_state >= TURN_SECONDS:
                self.sides_completed += 1
                self.get_logger().info(
                    f'Side {self.sides_completed}/{SIDES} complete.'
                )
                if self.sides_completed >= SIDES:
                    # TODO 6: switch self.state to State.DONE. Do not
                    # publish any further movement after this -- the
                    # early return at the top of this method handles
                    # that once self.state is State.DONE, but you still
                    # need to stop the turtle's current motion once here.
                    pass
                    self.stop_turtle()
                    self.get_logger().info('Figure complete. Stopping.')
                    return
                else:
                    self.state = State.DRIVE
                    self.elapsed_in_state = 0.0

        # TODO 7: publish msg on self.cmd_vel_pub.
        pass

    def stop_turtle(self):
        """
        Publish a zero Twist so the turtle actually stops.

        An empty ``cmd_vel`` message defaults every field to 0.0, which
        is exactly what we want here.
        """
        # TODO 8: publish an all-zero Twist() on self.cmd_vel_pub.
        pass


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
