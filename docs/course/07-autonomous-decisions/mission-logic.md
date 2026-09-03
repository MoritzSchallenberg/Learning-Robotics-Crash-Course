# Mission logic

{{ common }} {{ core }}

## What this topic is

A **finite state machine**: the robot is always in exactly one **state**;
**transitions** move it to the next one depending on the outcome. A
**behavior tree**: a tree, re-evaluated many times a second, built from a
few control nodes — **Sequence** (run children in order, fail on first
failure) and **Fallback** (try children in order, succeed on first
success).

## Why a robot needs it

`drive(); detect(); grasp(); deliver()` has no answer to "what if `detect`
finds nothing?" other than crashing. **Every real mission is mostly
failure handling** — the tools on this page exist to make that structure
explicit instead of buried in nested `if` statements.

## How it works

### Finite state machines

```{figure} ../../_static/images/diagrams/08-state-machine-behavior-tree.svg
:alt: Left, a finite state machine with states Idle, Navigate, Detect and Deliver in sequence, each with its own explicit failure transition to a shared Abort state. Right, a behavior tree with a Fallback root whose first child is a Sequence of Navigate, Detect and Deliver, and whose second child is a Recovery action used if the sequence fails.
:width: 100%

A state machine needs one failure transition per state; a behavior tree
needs one shared recovery branch.
```

What makes the left side useful is not the happy path — it is that **every
state has a named exit for failure**. Drawing it forces the question "and
what if this does not work?" for every step.

### Behavior trees, in contrast

Nav2's BT Navigator, which you already used in
[module 6](../06-navigation.md), is exactly this pattern.

```{list-table}
:header-rows: 1
:widths: 30 35 35

* -
  - State machine
  - Behavior tree
* - Failure handling
  - One transition per state
  - One shared fallback branch
* - Scales to
  - Small, well-understood missions
  - Larger missions with shared recovery
* - Easiest to
  - Explain and step through
  - Extend without touching existing states
```

For [the practical exercise](practical-exercise.md), a state machine is
the faster thing to get working.

## Inputs and outputs

A mission's state machine calls into other modules' clients as its
"actions" — a navigation goal ([module 6](../06-navigation.md)), a
detection check ([module 4](../04-perception/index.md)) — and typically
publishes its own status (`/mission_status`) so an external observer can
tell what it is doing, per [the practical
exercise's](practical-exercise.md#verification) verification step.

## Try it yourself

Build and deliberately break a minimal three-state mission before tackling
the full one in [the practical exercise](practical-exercise.md), so the
failure mode is familiar rather than surprising:

```python
import time
from enum import Enum, auto


class State(Enum):
    IDLE = auto()
    WAIT_FOR_INPUT = auto()
    DONE = auto()


def run_mission(get_input, timeout_s=5.0):
    state = State.IDLE
    deadline = None

    while state is not State.DONE:
        if state is State.IDLE:
            state = State.WAIT_FOR_INPUT
            deadline = time.time() + timeout_s

        elif state is State.WAIT_FOR_INPUT:
            if get_input() is not None:
                state = State.DONE
            elif time.time() > deadline:
                print('timed out waiting for input')
                state = State.DONE
            else:
                time.sleep(0.1)

    print('mission finished')
```

Run it with a `get_input` that always returns `None` — it should print
"timed out waiting for input" after five seconds and then finish, not hang
forever. Now comment out the `elif time.time() > deadline:` branch and run
it again: the loop never exits, because `WAIT_FOR_INPUT` has no way out
when its condition is never met. This is the exact failure mode [the
practical exercise](practical-exercise.md) asks you to avoid in a real
mission — a state with no timeout is a state that can hang forever.

## How ALeRT applies it

{{ alert }} {{ documented }} The team uses
[RAFCON](https://github.com/DLR-RM/RAFCON), a graphical state machine
editor, for exactly this pattern in practice — see
{ref}`Planning and manipulation approaches <rafcon-a-graphical-state-machine-tool>`
for the full walkthrough.

## How Carologistics applies it

{{ carologistics }} {{ documented }} The central goal-reasoning agent,
[`expertino-rcll`](../../platforms/carologistics-robotino.md#key-repositories),
plays the same role as this page's state machine — deciding what the
robot does next and reacting when a step fails — at fleet scale rather
than for one robot.

## Common problems

- **A state with no way out.** Waiting for something with no timeout.
  Every waiting state needs a deadline, exactly like this page's broken
  guided-example variant.
- **Only the happy path exists.** The most common first draft. If your
  diagram has no failure transitions, it is not finished.

## Next subtopic

[Planning and manipulation approaches](planning-and-manipulation.md) —
what to reach for when a state machine or behavior tree is not the right
tool.
