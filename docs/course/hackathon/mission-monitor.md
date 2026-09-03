# Mission monitoring and recovery

{{ common }} {{ core }}

## What this topic is

An optional development node that logs mission status transitions and
target detections with timestamps, plus a systematic way to handle an
unexpected stop mid-run instead of simply restarting and hoping.

## Why a robot needs it

The {ref}`self-assessment checklist <self-assessment-checklist>` asks you
to reconstruct what the system did and why from a log alone — that only
works if something is actually watching and recording the mission's
status the whole time, independent of the mission logic itself.

## Required logs

Record a rosbag of your attempt, containing at minimum `/tf`, `/tf_static`,
`/scan` (or your platform's equivalent range sensor), `/cmd_vel` and
`/mission_status`, following the practice from
[module 8](../08-integration/system-bringup-and-diagnostics.md). This is
what lets you check the
{ref}`self-assessment checklist <self-assessment-checklist>` against
evidence rather than memory, and lets you replay a failed attempt to see
exactly where it went wrong.

## How it works

An optional node for development: it listens for your mission's status
transitions and target detections and logs them with a timestamp, which is
useful for confirming your own mission logic behaves as intended before you
depend on it, and for lining up a log against a rosbag when replaying a
run.

```python
#!/usr/bin/env python3

import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MissionMonitorNode(Node):
    """Logs mission status transitions and timing for one attempt."""

    def __init__(self):
        super().__init__('mission_monitor', namespace='monitor')
        self.start_time = time.time()
        self.finished = False

        self.create_subscription(String, 'detected_target', self.on_target, 10)
        self.create_subscription(String, 'mission_status', self.on_status, 10)

        self.get_logger().info('Mission monitor started.')

    def on_target(self, msg):
        self.get_logger().info(f'Target reported: {msg.data}')

    def on_status(self, msg):
        if self.finished:
            return
        self.get_logger().info(f'Mission status: {msg.data}')
        if msg.data in ('succeeded', 'failed_safe', 'aborted'):
            self.finished = True
            duration = time.time() - self.start_time
            self.get_logger().info(
                f'Attempt finished: {msg.data} in {duration:.1f}s')


def main():
    rclpy.init()
    node = MissionMonitorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

:::{tip}
Publish `mission_status` with the values `succeeded`, `failed_safe` or
`aborted` — never leave it unset. Both this node and you, reading the log
afterwards, need exactly one clear signal for how an attempt ended, which
is the same discipline the state machine in
[module 7](../07-autonomous-decisions.md) already asks of every state.
:::

## Handling an unexpected stop

If the robot stops unexpectedly mid-run — a dropped connection, a stalled
motor, an E-stop press — do not simply restart the same launch command and
hope. Work through it like any other fault:

1. Check the last few log lines and the last `mission_status` value before
   the stop; often the mission logic already told you what it was doing.
2. Run the [eight-step diagnostic
   procedure](../08-integration/system-bringup-and-diagnostics.md) before
   touching anything.
3. If a physical E-stop was pressed, the platform typically needs an
   explicit re-enable step before it will move again — check your
   [platform page](../../platforms/index.md) for the exact procedure.
4. Once you understand what happened, restart from a clean, known state
   rather than from wherever the system was left.

## Preparing for the project

Build the mission end to end first — reliable beats clever. Rehearse the
cold-start-to-ready sequence until it is routine. Record every practice
attempt; when something goes wrong, the bag is what lets you find out why
without having to reproduce it live.

## Next subtopic

[Interesting videos](videos.md) — a short demonstration of a real robot
running an autonomous mission end to end.
