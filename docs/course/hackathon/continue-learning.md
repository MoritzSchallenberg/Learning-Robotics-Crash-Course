# Continue learning

These are engineering practices worth applying to the mission itself, not
event rules — no scoring, ranking or organisational planning below, only
ways to make the attempt more deliberate and more reproducible.

## Next steps

:::{dropdown} Decomposing the mission into subsystems and interfaces — Next step
:icon: light-bulb

**What it is.** Before writing code, break "run the mission" into named
subsystems (localization, navigation, perception, mission logic) and write
down each one's **interface** — exactly which topics, services or actions
it consumes and produces — as a short document or a diagram, before you
integrate any of them.

**Why it matters.** [Module 1's](../01-hardware/practical-exercise.md)
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
diagrams](../01-hardware/practical-exercise.md)
:::

:::{dropdown} Integration order and a test matrix — Next step
:icon: light-bulb

**What it is.** Deciding the order subsystems come online in
([module 8's](../08-integration/system-bringup-and-diagnostics.md) startup
order, applied to your mission specifically), and a **test matrix** —
which subsystem combinations you have actually tested together, and which
you have only tested alone.

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
order](../08-integration/system-bringup-and-diagnostics.md)
:::

:::{dropdown} Repeatability across multiple mission runs — Next step
:icon: light-bulb

**What it is.** Running the full mission several times in a row from a
clean, cold state, and recording success/failure for each — rather than
treating one successful run as proof the mission works, the same
distinction [module 6's](../06-navigation/continue-learning.md) navigation
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
metrics](../06-navigation/continue-learning.md)
:::

:::{dropdown} A short technical retrospective — Next step
:icon: light-bulb

**What it is.** After an attempt (successful or not), writing a short,
honest technical note: what worked, what did not, what you would change
about the *design* next time — a few paragraphs, not a report.

**Why it matters.** The test matrix, failure-mode list and fault-injection
results below are only useful if something is done with them; a short
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

## Intermediate projects

:::{dropdown} Measurable acceptance criteria beyond the checklist — Intermediate
:icon: light-bulb

**What it is.** Turning each self-assessment checklist item above into a
number where possible — not just "the target area is reached" but "reached
within N seconds, within M centimetres of the marked target" — the same
discipline as [module 6's](../06-navigation/continue-learning.md) navigation
metrics, applied to the whole mission.

**Why it matters.** A binary pass/fail can hide a mission that barely
passes every time versus one that passes with real margin; a number lets
you tell those apart and track whether changes actually help.

**Needs.** The {ref}`self-assessment checklist <self-assessment-checklist>`,
attempted at least once.

**Try it.** Pick two checklist items and define a measurable version of
each (a time, a distance, a count), then record the actual value from your
next attempt.

**Check.** You have two concrete numbers, not just two checkmarks, from a
real run.

**Read more.** [Module 6: systematic tuning and navigation
metrics](../06-navigation/continue-learning.md)
:::

:::{dropdown} Failure modes and a logging strategy — Intermediate
:icon: light-bulb

**What it is.** Listing, in advance, the ways the mission could plausibly
fail (lost localization, blocked path, no target found, communication
drop) and deciding, for each, what should be logged at the moment it
happens — rather than discovering after a failed run that the one piece of
information you needed was never recorded.

**Why it matters.** [Module 8's](../08-integration/continue-learning.md)
logging-levels topic covers *how* to log; this is deciding *what* is worth
logging, specific to your mission's actual failure modes.

**Needs.** [Module 8's logging
levels](../08-integration/continue-learning.md) and your subsystem
decomposition above.

**Try it.** For each failure mode you listed, write the exact log line
(with real field names) your code would need to emit for you to diagnose
it later from a log alone, without having watched the run live.

**Check.** Deliberately trigger one listed failure mode and confirm the
log actually contains the line you designed for it.

**Read more.** [Module 8: logging
levels](../08-integration/continue-learning.md)
:::

:::{dropdown} A fault-injection test for the whole mission — Intermediate
:icon: light-bulb

**What it is.** Applying
[module 8's](../08-integration/system-bringup-and-diagnostics.md)
fault-injection table to the **whole mission** rather than one subsystem —
deliberately breaking one thing (a renamed topic, a missing static
transform) and confirming the mission fails safely rather than hanging or
behaving unpredictably.

**Why it matters.** This directly exercises the self-assessment
checklist's "if something fails, the mission ends in a defined, safe
state" item, under a condition you actually chose and can reproduce, not
just when something happens to break on its own.

**Needs.** [Module 8's fault
table](../08-integration/system-bringup-and-diagnostics.md) and a working
mission attempt.

**Try it.** Pick one fault from module 8's table, apply it to a copy of
your mission's launch configuration, and run the mission end to end.

**Check.** `/mission_status` reports a defined failure value (never
silence, never a hang) within a reasonable time of the fault taking
effect.

**Read more.** [Module 8: the guided
example's fault table](../08-integration/system-bringup-and-diagnostics.md)
:::
