#!/usr/bin/env python3
"""
Module 2 practical task -- reference solution.

Drives turtlesim's turtle through a square with no keyboard input, using
a timer callback and a DRIVE/TURN/DONE state machine.

Try the starter file yourself before reading this -- it is
`turtle_course/turtle_course/turtle_controller.py`, one directory up.

To run this exact file (rather than working through the starter's TODOs):
copy it over the starter file's location, keeping the same filename, then
`colcon build --packages-select turtle_course` and
`ros2 run turtle_course turtle_controller`.
"""

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

        self.get_logger().info(
            f'Starting: driving a {SIDES}-sided figure.'
        )

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
                self.get_logger().info(
                    f'Side {self.sides_completed}/{SIDES} complete.'
                )
                if self.sides_completed >= SIDES:
                    self.state = State.DONE
                    self.stop_turtle()
                    self.get_logger().info('Figure complete. Stopping.')
                    return
                else:
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
