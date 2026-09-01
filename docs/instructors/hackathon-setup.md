# Hackathon setup

Running the closing event described on the
[hackathon page](../course/hackathon.md) — the facilitator side of that
page's rules and rubric.

:::{admonition} This is Draft 0.1 tooling for a Draft 0.1 event
:class: warning

The [hackathon rubric](../course/hackathon.md#scoring-rubric) and
[arena](../course/hackathon.md#schematic-arena) are both explicitly draft —
see `DECISIONS_NEEDED.md` items 8 and 9. This page assumes they will be
finalised before 07 November 2026 and describes the *process* for running
the event regardless of the exact final numbers.
:::

## Roles

**Referee** (at least one per concurrent arena) — starts and stops the
clock, judges collisions and manual interactions per the
[rubric](../course/hackathon.md#scoring-rubric), holds final say on
disputes, and owns the arena E-stop override.

**Scorer** — runs the [scoring node](../course/hackathon.md#the-scoring-node)
or an equivalent checklist, records each team's result.

**Safety spotter** per team — see the hackathon page's own
[recommended team roles](../course/hackathon.md#group-size-and-roles); this
is a team role, not an event-staff role, but a facilitator should confirm
every team has assigned one before their attempt.

## Before the event

- [ ] Arena confirmed and built to the dimensions decided under
      `DECISIONS_NEEDED.md` item 8 — not the schematic sketch, which is
      illustrative only.
- [ ] Every referee and scorer has read the
      [hackathon page](../course/hackathon.md) in full, including the
      rules, abort conditions and hardware-failure procedure.
- [ ] The rubric to be used is confirmed — either the Draft 0.1 as
      published, or a corrected version, but **the same version for every
      team**.
- [ ] A schedule exists: which team runs in which slot, with buffer time
      between attempts for the arena to be reset and checked.
- [ ] Spare batteries, a basic tool kit, and a designated "hardware failure"
      table are ready, separate from the arena itself.
- [ ] A method for collecting each team's required rosbag
      (see the hackathon page's
      [required logs](../course/hackathon.md#required-logs)) is agreed —
      a shared drive or USB collection point, decided and communicated in
      advance, not improvised on the day.

## Safety briefing (give this to every team before their slot)

1. Point out the arena E-stop and each team's own robot E-stop.
2. State the abort conditions from the
   [hackathon page](../course/hackathon.md#abort-conditions) out loud.
3. Confirm the team's safety spotter is holding the E-stop, not doing
   anything else, for the duration of the attempt.
4. State clearly: stopping a run early for safety costs points, but is
   always the right call over letting something get hurt or broken.

## Running an attempt

1. Confirm the arena is clear and the previous team's equipment is fully
   removed.
2. Team declares ready; referee starts the clock and the rosbag recording
   simultaneously (or confirms the team has started their own).
3. Referee observes and logs: collisions, manual interactions, and the
   final `mission_status` value.
4. At the time limit or on `mission_status`, referee stops the clock and
   records the elapsed time.
5. Scorer fills in the rubric based on referee observation plus any
   automated topics (`/detected_target`, `/mission_status`).
6. Team retrieves their equipment; referee confirms the arena is clear for
   the next team.

## Hardware failure, in practice

The [hackathon page's procedure](../course/hackathon.md#procedure-for-a-hardware-failure)
is the rule; this is what it looks like for a referee running it:

1. The moment a team reports a failure, say the clock is stopped **out
   loud** so there is no ambiguity about whether the attempt is still
   scored live.
2. Give the team a fixed, short window (a few minutes) to assess whether it
   is fixable — do not let an assessment become an unbounded repair
   session that blocks the schedule for other teams.
3. If fixable within that window and the schedule allows a restart slot,
   log the delay and let them restart with a time penalty per the rubric.
4. If not, log what failed (for `CONTENT_REVIEW.md`'s benefit in a future
   course version) and move to the next team; offer a later slot only if
   the schedule has room.

## After the event

- [ ] Collect every team's rosbag, with their consent, before laptops
      leave the room.
- [ ] Record final scores and any rubric disputes for
      `DECISIONS_NEEDED.md` item 9's eventual resolution — what actually
      happened is the best input to correcting the draft rubric.
- [ ] Note anything about the arena that did not match the schematic's
      assumptions, for `DECISIONS_NEEDED.md` item 8.
- [ ] Return all E-stops, spares and tools to storage.
- [ ] Thank every team — win, lose, or hardware failure; eight weeks of
      85-minute evenings is real work.
