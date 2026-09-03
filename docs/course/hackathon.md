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
  [module 1's safety section](01-hardware/sense-process-act.md#safety-and-emergency-stops) for why
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

## Continue learning

These are engineering practices worth applying to the mission itself, not
event rules — no scoring, ranking or organisational planning below, only
ways to make the attempt more deliberate and more reproducible.

:::{dropdown} Decomposing the mission into subsystems and interfaces — Next step
:icon: light-bulb

**What it is.** Before writing code, break "run the mission" into named
subsystems (localization, navigation, perception, mission logic) and write
down each one's **interface** — exactly which topics, services or actions
it consumes and produces — as a short document or a diagram, before you
integrate any of them.

**Why it matters.** [Module 1's](01-hardware/practical-exercise.md)
system diagram did this for hardware; doing the same for software
subsystems here catches interface mismatches (a topic name or message type
two subsystems disagree on) on paper, before they cost an integration
session.

**Needs.** Modules 1–8 completed.

**Try it.** Draw a box for each subsystem in your mission plan, and label
every arrow between them with the actual topic/service/action name and
type — not just "navigation talks to perception".

**Check.** Someone who has not seen your code can tell, from the diagram
alone, exactly which ROS 2 interface connects any two subsystems.

**Read more.** [Module 1: system
diagrams](01-hardware/practical-exercise.md)
:::

:::{dropdown} Integration order and a test matrix — Next step
:icon: light-bulb

**What it is.** Deciding the order subsystems come online in
([module 8's](08-integration.md#core-concepts) startup order, applied to
your mission specifically), and a **test matrix** — which subsystem
combinations you have actually tested together, and which you have only
tested alone.

**Why it matters.** "Each part works alone" and "the whole mission works"
are different claims; a test matrix makes visible exactly which
combinations you have and have not verified, instead of assuming untested
combinations are fine.

**Needs.** Your subsystem decomposition from the topic above.

**Try it.** Build a small table: rows and columns are your subsystems,
each cell marked tested-together or not-yet-tested. Fill it in as you
actually integrate, not in advance.

**Check.** By the time you attempt a full mission run, every cell adjacent
to the diagonal (each subsystem paired with the one it directly talks to)
is marked tested.

**Read more.** [Module 8: startup
order](08-integration.md#core-concepts)
:::

:::{dropdown} Measurable acceptance criteria beyond the checklist — Intermediate
:icon: light-bulb

**What it is.** Turning each self-assessment checklist item above into a
number where possible — not just "the target area is reached" but "reached
within N seconds, within M centimetres of the marked target" — the same
discipline as [module 6's](06-navigation.md#continue-learning) navigation
metrics, applied to the whole mission.

**Why it matters.** A binary pass/fail can hide a mission that barely
passes every time versus one that passes with real margin; a number lets
you tell those apart and track whether changes actually help.

**Needs.** The self-assessment checklist above, attempted at least once.

**Try it.** Pick two checklist items and define a measurable version of
each (a time, a distance, a count), then record the actual value from your
next attempt.

**Check.** You have two concrete numbers, not just two checkmarks, from a
real run.

**Read more.** [Module 6: systematic tuning and navigation
metrics](06-navigation.md#continue-learning)
:::

:::{dropdown} Failure modes and a logging strategy — Intermediate
:icon: light-bulb

**What it is.** Listing, in advance, the ways the mission could plausibly
fail (lost localization, blocked path, no target found, communication
drop) and deciding, for each, what should be logged at the moment it
happens — rather than discovering after a failed run that the one piece of
information you needed was never recorded.

**Why it matters.** [Module 8's](08-integration.md#continue-learning)
logging-levels topic covers *how* to log; this is deciding *what* is worth
logging, specific to your mission's actual failure modes.

**Needs.** [Module 8's logging
levels](08-integration.md#continue-learning) and your subsystem
decomposition above.

**Try it.** For each failure mode you listed, write the exact log line
(with real field names) your code would need to emit for you to diagnose
it later from a log alone, without having watched the run live.

**Check.** Deliberately trigger one listed failure mode and confirm the
log actually contains the line you designed for it.

**Read more.** [Module 8: logging
levels](08-integration.md#continue-learning)
:::

:::{dropdown} A fault-injection test for the whole mission — Intermediate
:icon: light-bulb

**What it is.** Applying [module 8's](08-integration.md#guided-example)
fault-injection table to the **whole mission** rather than one subsystem —
deliberately breaking one thing (a renamed topic, a missing static
transform) and confirming the mission fails safely rather than hanging or
behaving unpredictably.

**Why it matters.** This directly exercises the self-assessment
checklist's "if something fails, the mission ends in a defined, safe
state" item, under a condition you actually chose and can reproduce, not
just when something happens to break on its own.

**Needs.** [Module 8's fault
table](08-integration.md#guided-example) and a working mission attempt.

**Try it.** Pick one fault from module 8's table, apply it to a copy of
your mission's launch configuration, and run the mission end to end.

**Check.** `/mission_status` reports a defined failure value (never
silence, never a hang) within a reasonable time of the fault taking
effect.

**Read more.** [Module 8: the guided
example's fault table](08-integration.md#guided-example)
:::

:::{dropdown} Repeatability across multiple mission runs — Next step
:icon: light-bulb

**What it is.** Running the full mission several times in a row from a
clean, cold state, and recording success/failure for each — rather than
treating one successful run as proof the mission works, the same
distinction [module 6's](06-navigation.md#continue-learning) navigation
metrics topic makes for a single navigation goal.

**Why it matters.** The self-assessment checklist's first item — "the
system starts reproducibly, with one command, from a cold state" — is only
actually verified by doing it more than once.

**Needs.** A working end-to-end mission attempt.

**Try it.** Run the mission five times in a row, resetting to a cold state
between each, and record a simple pass/fail for each attempt.

**Check.** You can report an actual count (e.g. "4/5") instead of a single
anecdote, and — for any failure — which checklist item it failed on.

**Read more.** [Module 6: systematic tuning and navigation
metrics](06-navigation.md#continue-learning)
:::

:::{dropdown} A short technical retrospective — Next step
:icon: light-bulb

**What it is.** After an attempt (successful or not), writing a short,
honest technical note: what worked, what did not, what you would change
about the *design* next time — a few paragraphs, not a report.

**Why it matters.** The test matrix, failure-mode list and fault-injection
results above are only useful if something is done with them; a short
retrospective is where that actually happens, while the details are still
fresh.

**Needs.** At least one full mission attempt.

**Try it.** Write three short sections: what worked as designed, what
failed and why (referencing your logs or rosbag), and one concrete design
change you would make before the next attempt.

**Check.** Your "what failed and why" section cites specific evidence (a
log line, a bag timestamp) rather than a guess.

**Read more.** N/A — this is a habit, not a tool with documentation to
link.
:::

## Interesting videos

{{ optional }}

::::{grid} 1 1 1 1
:gutter: 2

:::{grid-item-card} Raph Rover Demo — ROS 2 Mobile Robot for Research & Autonomous Navigation
:link: https://www.youtube.com/watch?v=U3E-mRUrGgM

**Generation Robots · English · ~2 min**

Covers: a short demonstration of a real wheeled robot running an
autonomous navigation mission end to end under ROS 2 — bring-up, sensing,
and moving through an environment on its own.

*Why watch it*: a short, concrete "this is what the finished thing looks
like" reference for the capstone's own mission — start correctly,
localize, reach a target, avoid an obstacle — on real hardware rather
than only in this course's own text description.

*Compatibility*: conceptual — a product demonstration, not a
command-by-command tutorial.
:::

::::

:::{note}
This is deliberately one carefully checked video rather than a longer,
unverified list. If this link is ever dead or the content has moved, that
is a documentation bug worth reporting — see the [repository
README](https://github.com/MoritzSchallenberg/Learning-Robotics-Crash-Course).
:::

## Connection to the course

This project draws on every module:
[1](01-system-hardware.md) · [2](02-ros2.md) · [3](03-sensors-tf.md) ·
[4](04-perception/index.md) · [5](05-mapping-localization.md) ·
[6](06-navigation.md) · [7](07-autonomous-decisions.md) ·
[8](08-integration.md).

## Further reading

- [Nav2 costmap filters](https://docs.nav2.org/humble/configuration_and_development/configuration_guide/core_servers/costmap_2d/costmap_filters/keepout_filter/)
- [Nav2 tutorials](https://docs.nav2.org/humble/tutorials/)
- Your [platform track](../platforms/index.md)
