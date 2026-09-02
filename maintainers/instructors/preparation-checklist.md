# Preparation checklist

What every session needs, in general. [Session plans](session-plans.md) adds
what is specific to each of the eight evenings.

## Needed devices

```{list-table}
:header-rows: 1
:widths: 30 70

* - Device
  - Notes
* - Facilitator laptop
  - Running the demonstration; should have the same pre-built workspace
    participants get, tested the day before.
* - Per-participant-group laptop
  - One per group — group size is not yet fixed, see
    [`DECISIONS_NEEDED.md`](https://github.com/MoritzSchallenberg/Learning-Robotics-Crash-Course/blob/main/DECISIONS_NEEDED.md)
    item 6 — with [prerequisites](../prerequisites/index.md) already
    installed and `scripts/course-preflight.sh` passing with no `FAIL`.
* - Robot(s) or simulation-capable machines
  - See [`DECISIONS_NEEDED.md`](https://github.com/MoritzSchallenberg/Learning-Robotics-Crash-Course/blob/main/DECISIONS_NEEDED.md)
    item 5 — real availability is an open organisational question this site
    cannot answer for you.
* - A projector or shared screen
  - For the 10-minute demonstration block; test it works with a terminal at
    a readable font size *before* the session, not during the opening.
```

## Needed software

Every session assumes a **pre-built** workspace, listed per session in
[session plans](session-plans.md). Build and test all of them the day
before, following that session's exact commands — do not assume a build
that worked last course still works; dependencies drift.

## Preparation time

Budget roughly **60–90 minutes** of facilitator time per session:
15 minutes reading that session's page and [session plan](session-plans.md)
in full, 20–30 minutes building and testing the pre-built workspace end to
end (following the session's own Steps as if you were a participant),
10 minutes preparing physical materials (printed markers, checkerboards),
and 15 minutes rehearsing the 10-minute demonstration block so it fits the
time.

Session 8's planted fault and the hackathon's arena setup need more —
see their specific notes.

## Materials per evening

```{list-table}
:header-rows: 1
:widths: 12 88

* - Session
  - Physical materials
* - 1
  - None — the practical task is drawing, on paper or a shared drawing tool.
* - 2
  - None.
* - 3
  - None, beyond the robot/simulation itself.
* - 4
  - Printed ArUco markers (dictionary `DICT_6X6_50`), one per group, plus
    spares. A checkerboard calibration target **only** if any group is
    calibrating a webcam ahead of time — see
    [camera calibration](../course/04-perception/camera-calibration.md),
    which is preparation, not part of the session itself.
* - 5
  - None, beyond the robot/simulation itself.
* - 6
  - An object to use as an "unmapped obstacle" per group.
* - 7
  - None.
* - 8
  - One deliberately modified launch/config file per group — see
    [session plans](session-plans.md#session-8) for what makes a good one.
```

## The shape of a good demonstration (10 minutes)

Every run sheet allocates exactly 10 minutes to a live demonstration between
the theory block and the practical task. What works:

1. **Narrate before you act.** Say what you are about to type and what you
   expect to happen, *then* run it — participants learn the reasoning, not
   just the command.
2. **Show the task's actual failure mode once, on purpose**, where the
   session has one (RViz showing nothing in session 3, a blocked path in
   session 6, a planted fault in session 8). Seeing the instructor recover
   from a controlled failure is worth more than a flawless run.
3. **Stop at 10 minutes.** The practical task is where learning actually
   happens; a demonstration that runs long steals from it.

## Expected participant problems

Every session page has a **Common problems** section written from real
failure modes in the source material and this site's own testing — read it
as part of your preparation, not just as a participant reference. The three
that recur across almost every session:

- **A terminal that was not sourced** after a build (`source
  install/setup.bash` in *this* terminal).
- **`use_sim_time` inconsistent** across nodes, in every session from 5
  onward.
- **QoS mismatches** producing silent failure (nothing appears, no error) —
  first seen in session 3, relevant again in sessions 5 and 6.

Knowing these before a participant hits them means you recognise the
symptom in seconds instead of debugging alongside them from scratch.

## Fallback plan if hardware fails

Every session page has a **Simulation fallback** section for exactly this.
If a robot is unavailable or breaks mid-session:

1. Announce it immediately — do not let a group discover it by confusion.
2. Point the affected group(s) to that session's Simulation fallback
   section; the task and learning objective stay identical.
3. If simulation is *also* unavailable on a given machine, pair that group
   with another rather than losing them for the evening.

## Time control

The 85-minute run sheet has no slack built in. Two habits that keep it on
track: **start the practical task block on time even if theory ran long** —
cut the last few minutes of theory rather than the task, since the task is
where the learning objective is actually met; and **announce the halfway
point** of the 35-minute practical task block once, out loud, so groups can
judge their own pace against Verification rather than only against Steps.

## Acceptance points

Before ending a session, confirm — by asking groups directly, not by
assuming — that each group reached the session's stated **Expected result**
and could run its **Verification** command successfully. A session where
half the room silently did not finish the Core task is a session that needs
a different pace next time, and you will not know unless you ask.

## Cleanup and data backup checklist

- [ ] Every physical robot is returned to its charging state.
- [ ] Any rosbags recorded during the session (sessions 8 onward) are copied
      off participant laptops if they contain useful teaching examples —
      **only with participant consent**, following the same rule as the
      hackathon's required logs.
- [ ] Printed materials (markers, checkerboards) are collected for next
      time.
- [ ] Any planted fault ([session 8](session-plans.md#session-8)) is
      reverted in the shared repository before the next group uses it.
- [ ] Note anything that did not go to plan, for the next facilitator —
      this is what future editions of `CONTENT_REVIEW.md` and
      `DECISIONS_NEEDED.md` draw on.
