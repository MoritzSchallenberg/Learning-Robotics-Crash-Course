# Hackathon: Autonomous Robot Challenge

:::{admonition} Schedule
:class: note

Saturday–Sunday, 07–08 November 2026
:::

{{ common }}

Everything from the eight sessions, on one robot, running on its own.

:::{admonition} Draft 0.1 — not confirmed
:class: warning

Everything on this page — the rubric, the arena, the time limit — is
**Draft 0.1**, published early so teams can build against it and so it can
be corrected before the event. It is deliberately easy to change: every
number lives in one table, and `DECISIONS_NEEDED.md` tracks exactly what
still needs sign-off (items 8 and 9). If something here is unfair or
unclear, say so — that is what a draft is for.
:::

## The common mission

Every team, on every platform, attempts the same seven-step mission:

1. **Start correctly** — bring up the robot from a cold state with the
   team's own launch procedure.
2. **Establish position** — localize, or otherwise determine a known
   starting pose.
3. **Reach a target area** — navigate there autonomously, no manual driving.
4. **Handle obstacles** — detect and avoid at least one obstacle not present
   when the arena was last mapped.
5. **Recognise a target** — detect a marker or object in the target area.
6. **Report success** — signal mission completion on the agreed topic.
7. **Fail safely** — if something goes wrong, reach a safe, stopped state
   rather than continuing blindly.

### Optional extensions (bonus)

- pick up and transport the recognised object;
- plan a new route after being blocked;
- communicate with a second robot;
- handle more than one target;
- explore an area with no prior map.

:::{note}
**Manipulation and multi-robot tasks are bonus only.** A team without a
gripper, or running only one robot, is never penalised for not attempting
them — see the rubric below, where the maximum achievable score without any
bonus is the full 100 points.
:::

## Scoring rubric

A transparent 100-point rubric, split across what can be measured
automatically and what a referee assesses directly.

```{list-table}
:header-rows: 1
:widths: 60 20 20

* - Area
  - Points
  - Assessed by
* - Safe and reproducible system bring-up
  - 10
  - Referee checklist
* - Localization / known starting state
  - 10
  - Referee + `/mission_status`
* - Autonomous navigation
  - 20
  - Referee + navigation log
* - Obstacle reaction
  - 15
  - Referee observation
* - Perception and target recognition
  - 15
  - `/detected_target` topic + referee
* - Mission logic and failure handling
  - 15
  - Referee + `/mission_status`
* - Integration and technical robustness
  - 10
  - Referee checklist
* - Short documentation and final presentation
  - 5
  - Referee
* - **Total**
  - **100**
  -
```

**Bonus points** (added on top of the 100, capped at +15 total): transport
task completed (+8), new route planned after a block (+4), multi-robot
communication demonstrated (+3).

**Penalties**: −3 per collision with the arena or an obstacle; −2 per manual
interaction (gamepad, terminal command, physical assistance) after the run
has started; −1 per full minute beyond the time limit.

**Time limit**: 15 minutes per attempt. **Ties**: decided by elapsed time,
then by fewer manual interactions.

:::{admonition} TODO-REVIEW
:class: todo-review

The point values above are a considered first draft, not a validated one —
they have not been tested against the real arena or the robots available on
the day. See `DECISIONS_NEEDED.md` item 9. Collision detection is assumed to
be judged by a human referee; if an automated method is intended for a
future version, this section needs revising rather than the automation being
invented here.
:::

## Rules and logistics

### Safety rules

- A referee or team member must be within reach of the physical E-stop at
  all times during a run.
- If a robot is about to injure a person or destroy itself or the arena,
  stop it immediately — a stopped run costs points; a broken robot costs
  the weekend.
- No run begins until the referee confirms the arena is clear.

### Permitted preparation

- Mapping the arena in advance, if access is provided ahead of the event.
- Tuning navigation and perception parameters using data from practice
  runs.
- Pre-training a detection model on the announced target object(s), once
  confirmed.
- Team-written launch, configuration and mission-control code, prepared in
  advance.

Not permitted: teleoperating any part of the scored attempt except as a
penalised manual interaction; hard-coding the exact arena layout from
insider knowledge not available to other teams.

### Starting state

The robot begins powered off or in a defined idle state, at a marked start
position, facing a direction the team declares in advance. The clock starts
when the team signals ready and the referee starts the run.

### Abort conditions

A run is aborted (scored as-is, mission incomplete) if: the E-stop is
pressed for safety reasons; the robot leaves the arena boundary; the time
limit is reached; or the team requests it.

### Required logs

Each team records and submits a rosbag of their best attempt, containing at
minimum `/tf`, `/tf_static`, `/scan` (or equivalent range sensor), `/cmd_vel`
and `/mission_status`, following the practice from
[session 8](08-integration.md#rosbags-briefly). This is both evidence for
scoring disputes and material for a future course's teaching examples
(with team consent).

### Group size and roles

Teams of 2–4. Recommended roles for the run itself: **driver** (owns the
laptop and launch sequence, the only one who touches a keyboard once the
run has started), **spotter** (owns the E-stop, watches the robot, calls
safety stops), **narrator** (talks the referee through what is happening,
useful for the documentation/presentation score).

### Acceptance checklist (bring this, completed, to your slot)

- [ ] One command brings the robot from cold start to ready.
- [ ] The team has rehearsed the full mission at least twice.
- [ ] The E-stop is tested and someone is assigned to hold it.
- [ ] A rosbag recording command is ready to run before the attempt starts.
- [ ] Batteries are charged, and a spare (if any) is ready.
- [ ] The mission-control code handles at least one failure path without
      hanging (see [session 7](07-autonomous-decisions.md)).

## Platform variants

### Simulation

{{ simulation }}

Run the full mission in [Webots](../platforms/simulation.md). Identical
scoring; the "hardware failure" procedure below does not apply — a crashed
simulation is restarted, and the clock resets with it, at the referee's
discretion.

### Carologistics / Robotino

{{ carologistics }}

Robotino's omnidirectional drive is a genuine advantage for tight arena
turns — plan for it in your navigation parameters
(see the [platform page](../platforms/carologistics-robotino.md)). The
transport bonus maps naturally onto Robotino's gripper carrying a workpiece
to a marked drop zone.

### ALeRT / Spot

{{ alert }}

Legged locomotion is the advantage where the arena includes any
non-flat terrain (see the [platform page](../platforms/alert-spot.md)).
Manipulation bonus attempts should budget extra time — MoveIt planning
failures are a normal part of a first attempt, not a sign something is
broken.

## Procedure for a hardware failure

1. **Stop the clock.** Signal the referee immediately — do not attempt a
   repair with the clock running.
2. **Assess**: is this fixable within the event's spare time (battery swap,
   loose connector), or does it end the attempt?
3. **Fixable**: the team gets one restart, at the referee's discretion,
   generally with a time penalty reflecting the delay.
4. **Not fixable**: the attempt ends; the team may run again in a later
   slot if one is available, or the run is scored as-is up to the failure.
5. **Always**: the referee logs what failed, for the acceptance checklist of
   future course versions.

## Schematic arena

```{figure} ../_static/images/diagrams/10-hackathon-arena-schematic.svg
:alt: A top-down schematic floor plan. A Start Zone sits bottom left. A dashed example route winds past two labelled obstacles and an unmapped-on-the-day area to a Target Zone top right containing a marker. An optional Drop Zone sits near the start for the transport bonus task.
:width: 100%

Schematic only — not the confirmed layout. See `DECISIONS_NEEDED.md` item 8.
```

This sketch fixes the **shape** of the mission (start → obstacles →
target, with an optional drop zone) so teams can build and test against
something concrete. The actual dimensions, obstacle placement and target
count depend on the room booked for the event — an open organisational
question, not a technical one; see `DECISIONS_NEEDED.md`.

## The scoring node

Illustrative interface for the automatable part of the score
(perception, mission logic). Test against it during development.

```python
#!/usr/bin/env python3

import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class ScoringNode(Node):
    """Records mission status transitions and timing for one attempt."""

    def __init__(self):
        super().__init__('scoring_node', namespace='scoring')
        self.start_time = time.time()
        self.finished = False

        self.create_subscription(String, 'detected_target', self.on_target, 10)
        self.create_subscription(String, 'mission_status', self.on_status, 10)

        self.get_logger().info('Scoring started. Clock is running.')

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
    node = ScoringNode()
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
`aborted` — never leave it unset. A referee (and this node) needs exactly
one clear signal for how your attempt ended.
:::

## Preparing for it

Build [Level 1 of the common mission](#the-common-mission) end to end first
— reliable beats clever. Rehearse the cold-start-to-ready sequence until
every team member has done it once. Record every practice run; when
something goes wrong you will have the bag.

## Transition from the course

Everything here draws on all eight sessions:
[1](01-system-hardware.md) · [2](02-ros2.md) · [3](03-sensors-tf.md) ·
[4](04-perception/index.md) · [5](05-mapping-localization.md) ·
[6](06-navigation.md) · [7](07-autonomous-decisions.md) ·
[8](08-integration.md).

## Further reading

- [Nav2 costmap filters](https://docs.nav2.org/jazzy/configuration_and_development/configuration_guide/core_servers/costmap_2d/costmap_filters/keepout_filter/)
- [Nav2 tutorials](https://docs.nav2.org/jazzy/tutorials/)
- Your [platform track](../platforms/index.md)
- Open organisational decisions: `DECISIONS_NEEDED.md` in the repository
