# Practical exercise

{{ common }} {{ core }}

## Goal

Implement a mission — *navigate to a point, look for a marker, report* —
that visibly recovers instead of hanging when the marker is not found.

## Starting point

A new package (call it `mission_demo`, or reuse an existing one from
earlier modules) into which you copy two pieces of code you already have
working: the navigation action client from
[module 6](../06-navigation/nav2-architecture-and-costmaps.md#inputs-and-outputs),
and the marker-detection pattern from [module 4](../04-perception/index.md).
Wrap each as a small helper class or function your state machine can call
— you are writing the state machine itself in this task, not the
underlying clients, so reuse rather than rewrite them.

## Steps

1. On paper, draw states: `IDLE → NAVIGATE → SEARCH → RETURN → DONE`, plus a
   `FAILED` exit from `NAVIGATE`.
2. Decide `SEARCH`'s timeout (30 s is reasonable) and what happens on
   timeout — it must still transition, not hang, exactly as in [Mission
   logic's guided example](mission-logic.md#try-it-yourself).
3. Implement the state machine in Python using the provided helper classes
   (a `State` enum plus a `step()` method, the same shape as the guided
   example, is enough).
4. Run it with the marker **present**. Confirm it completes.
5. Run it with **no marker** in the search area. Confirm it does not hang.
6. Block the navigation goal (place an obstacle across the only path).
   Confirm `NAVIGATE`'s failure exit actually fires.
7. Fix whatever you found in steps 5–6.

## Expected result

The mission finishes in all three cases — success, marker not found,
navigation blocked — with no run lasting longer than the timeout you chose,
and no traceback.

## Verification

```bash
ros2 topic echo /mission_status
```

Reports `succeeded`, `marker_not_found` or `navigation_failed` — three
distinct outcomes, never silence.

## Common problems

- **A state with no way out.** Waiting for something with no timeout. Every
  waiting state needs a deadline, exactly like [Mission logic's guided
  example's](mission-logic.md#try-it-yourself) broken version.
- **Failure not propagated.** The action client reports failure and the
  code moves to the next state anyway; always check the result status.
- **Only the happy path exists.** The most common first draft. If your
  diagram has no failure transitions, it is not finished.
- **`rclpy.shutdown()` inside a state.** Kills the shared node and
  everything after it. Only call it once, at the very end of the program.
- **The state machine "works" and the robot does not.** States ran and
  returned `success` without checking whether their action actually
  succeeded.

## Optional extensions

{{ optional }}

Add a fourth state that retries `SEARCH` once, from a slightly different
position, before giving up — the smallest possible recovery behaviour.

{{ simulation }} Failing "on purpose" is easier in simulation — remove the
marker from the scene, or block the path with a dragged object, exactly as
in [module 6](../06-navigation/practical-exercise.md#optional-extensions).

**Sketch the same mission as a behavior tree.** On paper, redraw your
practical task's `IDLE → NAVIGATE → SEARCH → RETURN → DONE` state machine
using [Mission logic's](mission-logic.md#how-it-works) own Sequence and
Fallback nodes instead of states and transitions — one Sequence for the
happy path, one Fallback wrapping the whole thing with a recovery branch
for `SEARCH`'s timeout. Compare the two drawings side by side: which one
made the failure-handling structure clearer to draw, and which would be
easier to extend with a sixth step next month?

## Try it on Spot

{{ alert }} {{ spotsim }}

Spot exposes its postures as **services** rather than topics or
actions — a natural fit, since standing up either succeeds or does not,
with no meaningful "progress" to report partway through:

```bash
ros2 service call /Spot/stand_up webots_spot_msgs/srv/SpotMotion
ros2 service call /Spot/sit_down webots_spot_msgs/srv/SpotMotion
ros2 service call /Spot/lie_down webots_spot_msgs/srv/SpotMotion
```

**Task**: build a state machine, exactly [Mission logic's](mission-logic.md)
core pattern, for a small mission:

```text
stand → navigate → detect → return → sit
```

- `stand`: call `/Spot/stand_up`, wait for the response.
- `navigate`: reuse
  [module 6's](../06-navigation/nav2-architecture-and-costmaps.md#inputs-and-outputs)
  action client to send a `NavigateToPose` goal.
- `detect`: reuse [module 4's](../04-perception/index.md) marker detection,
  with a timeout — no marker found in N seconds is a **named** failure
  exit, not a hang.
- `return`: navigate back to the start pose.
- `sit`: call `/Spot/sit_down`.

Log every state transition (state, timestamp, why) — the same discipline
this exercise and the [capstone
project's](../hackathon/continue-learning.md) failure-mode planning both
depend on. Add at least one explicit timeout and one explicit failure
transition, not only the happy path.

:::{admonition} Optional: manipulation
:class: task

{{ advanced }} Add a sixth state that plans a MoveIt trajectory for
Spot's arm ([platform page](../../platforms/alert-spot.md#manipulation-with-moveit))
once `detect` succeeds — with its own timeout, since "planning failed" is
a normal MoveIt outcome, not a crash (see
{ref}`Continue learning's Planning scene dropdown <planning-scene-and-collision-objects>`).
:::

:::{danger}
{{ spotsupervised }} An automatic movement sequence on the **physical**
Spot — stand, walk, sit, with no human confirming each step — is a
supervised-only exercise, never something to run unattended as a first
attempt. Simulate the entire sequence in Webots until every state and
every failure exit has actually been exercised, before ever considering
it on real hardware, and then only with a trained team member present who
can reach the E-stop. See the [platform page's operating
sequence](../../platforms/alert-spot.md#operating-the-physical-robot).
:::

## Next subtopic

[Interesting videos](videos.md) — a longer, hands-on look at behavior
trees.

## Sources

- [ROS 2: managed
  nodes](https://docs.ros.org/en/humble/Concepts/Intermediate/About-Ros2-Managed-Nodes.html)
