# Capstone: Autonomous Robot Mission

{{ common }}

Everything from the eight modules, on one robot, running on its own. This
is the course's final self-check: if you can complete it, the course has
done its job.

## Overview

You will combine mapping, localization, navigation, perception and mission
logic into one autonomous run: bring up a robot, have it find its own
position, reach a target area on its own, handle an obstacle it did not
know about, recognise a target, and end in a safe, defined state — whether
the mission succeeded or not.

## Learning objectives

By completing this project you demonstrate that you can:

1. integrate every module's subsystem into one reproducible system;
2. run an autonomous mission with no manual driving during the attempt;
3. produce a rosbag and logs that let you (or someone else) verify what the
   system actually did.

## Prerequisites

All eight course modules completed, in particular
[module 8](08-integration.md) — this project assumes you can already bring
up a whole system with one command and diagnose a fault systematically.

## The mission

The same seven-step mission applies regardless of platform:

1. **Start correctly** — bring up the robot from a cold state with your own
   launch procedure.
2. **Establish position** — localize, or otherwise determine a known
   starting pose.
3. **Reach a target area** — navigate there autonomously, no manual driving.
4. **Handle obstacles** — detect and avoid at least one obstacle not present
   when the area was last mapped.
5. **Recognise a target** — detect a marker or object in the target area.
6. **Report success** — signal mission completion on an agreed topic.
7. **Fail safely** — if something goes wrong, reach a safe, stopped state
   rather than continuing blindly.

### Optional extensions

- pick up and transport the recognised object;
- plan a new route after being blocked;
- communicate with a second robot;
- handle more than one target;
- explore an area with no prior map.

:::{note}
**Manipulation and multi-robot tasks are optional extensions, not
requirements.** A robot without a gripper, or a single-robot setup, can
complete every item in the self-assessment checklist below without
attempting them.
:::

## Self-assessment checklist

Rather than a points-based score, check the mission against these
statements. Each should be true and demonstrable — ideally from your rosbag
and logs, not just from memory:

- [ ] The system starts reproducibly, with one command, from a cold state.
- [ ] The robot establishes its position (localizes, or otherwise
      confirms a known starting pose) before moving toward the target.
- [ ] The target area is reached without any manual driving during the
      run.
- [ ] At least one obstacle not present in the original map is detected
      and avoided.
- [ ] The target object or marker is correctly recognised.
- [ ] Errors and key decisions are logged — you can reconstruct what the
      system did and why from the log alone.
- [ ] If something fails, the mission ends in a defined, safe state rather
      than hanging or continuing blindly.

A run that satisfies every item above is a complete demonstration of this
course's learning objectives, independent of platform, of whether any
optional extension was attempted, and of how the run compares to anyone
else's.

## Safety

- Keep the physical E-stop within reach for the entire run — yours, or
  whoever is operating alongside you.
- If the robot is about to injure someone or destroy itself or its
  surroundings, stop it immediately. A stopped run is always the right
  call over letting something get hurt or broken; see
  [module 1's safety section](01-system-hardware.md#core-concepts) for why
  the E-stop is independent of software in the first place.
- Confirm the area is clear of people and fragile objects before starting
  a run, and check the robot's actual footprint against the space
  available — a wider turning radius than expected is a common way a
  "clear" area turns out not to be.

## Required logs

Record a rosbag of your attempt, containing at minimum `/tf`, `/tf_static`,
`/scan` (or your platform's equivalent range sensor), `/cmd_vel` and
`/mission_status`, following the practice from
[module 8](08-integration.md#rosbags-briefly). This is what lets you check
the self-assessment checklist against evidence rather than memory, and lets
you replay a failed attempt to see exactly where it went wrong.

## Platform notes

### Simulation

{{ simulation }}

Run the full mission in [Webots](../platforms/simulation.md). The mission
and the self-assessment checklist are identical; a crashed simulation can
simply be restarted from a clean state, which is one of simulation's
genuine advantages for practicing this project repeatedly.

### Carologistics / Robotino

{{ carologistics }}

Robotino's omnidirectional drive is a genuine advantage for tight turns —
plan for it in your navigation parameters (see the
[platform page](../platforms/carologistics-robotino.md)). The transport
extension maps naturally onto Robotino's gripper carrying a workpiece to a
marked location.

### ALeRT / Spot

{{ alert }}

Legged locomotion is the advantage on any non-flat terrain (see the
[platform page](../platforms/alert-spot.md)). Manipulation attempts should
budget extra iteration time — MoveIt planning failures are a normal part of
a first attempt, not a sign something is broken.

## Schematic mission area

```{figure} ../_static/images/diagrams/10-hackathon-arena-schematic.svg
:alt: A top-down schematic floor plan. A Start Zone sits bottom left. A dashed example route winds past two labelled obstacles and an unmapped-on-the-day area to a Target Zone top right containing a marker. An optional Drop Zone sits near the start for the transport extension.
:width: 100%

Schematic only, illustrating the shape of the mission rather than any
particular physical layout.
```

This sketch fixes the **shape** of the mission — start, obstacles, a
target area, an optional drop zone for the transport extension — so you can
build and test against something concrete regardless of where you actually
run it. Build your own version of this layout with whatever space and
obstacles you have available; the exact dimensions do not matter, only that
it exercises every step of the mission above.

## Mission monitoring node

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
[module 7](07-autonomous-decisions.md) already asks of every state.
:::

## Handling an unexpected stop

If the robot stops unexpectedly mid-run — a dropped connection, a stalled
motor, an E-stop press — do not simply restart the same launch command and
hope. Work through it like any other fault:

1. Check the last few log lines and the last `mission_status` value before
   the stop; often the mission logic already told you what it was doing.
2. Run the [eight-step diagnostic procedure](08-integration.md#the-eight-step-diagnostic-procedure)
   before touching anything.
3. If a physical E-stop was pressed, the platform typically needs an
   explicit re-enable step before it will move again — check your
   [platform page](../platforms/index.md) for the exact procedure.
4. Once you understand what happened, restart from a clean, known state
   rather than from wherever the system was left.

## Preparing for the project

Build the mission end to end first — reliable beats clever. Rehearse the
cold-start-to-ready sequence until it is routine. Record every practice
attempt; when something goes wrong, the bag is what lets you find out why
without having to reproduce it live.

## Connection to the course

This project draws on every module:
[1](01-system-hardware.md) · [2](02-ros2.md) · [3](03-sensors-tf.md) ·
[4](04-perception/index.md) · [5](05-mapping-localization.md) ·
[6](06-navigation.md) · [7](07-autonomous-decisions.md) ·
[8](08-integration.md).

## Further reading

- [Nav2 costmap filters](https://docs.nav2.org/jazzy/configuration_and_development/configuration_guide/core_servers/costmap_2d/costmap_filters/keepout_filter/)
- [Nav2 tutorials](https://docs.nav2.org/jazzy/tutorials/)
- Your [platform track](../platforms/index.md)
