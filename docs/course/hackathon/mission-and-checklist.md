# The mission and self-assessment

{{ common }} {{ core }}

## What this topic is

A fixed seven-step mission, identical regardless of platform, and a
checklist of demonstrable, evidence-backed statements to verify your
attempt against — rather than a points-based score.

## Why a robot needs it

Every earlier module exercised one subsystem in isolation. A real mission
needs all of them cooperating, unattended, with no manual driving during
the attempt, and a defined way to tell afterwards whether it actually
worked.

## How it works

(the-mission)=
### The mission

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

(optional-extensions-capstone)=
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

(self-assessment-checklist)=
### Self-assessment checklist

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

## Inputs and outputs

The mission draws on every subsystem built in modules 2–7: localization
([module 5](../05-mapping-localization.md)), navigation
([module 6](../06-navigation.md)), perception
([module 4](../04-perception/index.md)) and mission logic
([module 7](../07-autonomous-decisions.md)). Its own output is a rosbag and
a log — see [Mission monitoring and
recovery](mission-monitor.md#required-logs).

## Try it yourself

Build the mission end to end first — reliable beats clever. Rehearse the
cold-start-to-ready sequence until it is routine. Record every practice
attempt; when something goes wrong, the bag is what lets you find out why
without having to reproduce it live.

## Safety

- Keep the physical E-stop within reach for the entire run — yours, or
  whoever is operating alongside you.
- If the robot is about to injure someone or destroy itself or its
  surroundings, stop it immediately. A stopped run is always the right
  call over letting something get hurt or broken; see
  [module 1's safety
  section](../01-hardware/sense-process-act.md#safety-and-emergency-stops)
  for why the E-stop is independent of software in the first place.
- Confirm the area is clear of people and fragile objects before starting
  a run, and check the robot's actual footprint against the space
  available — a wider turning radius than expected is a common way a
  "clear" area turns out not to be.

## Next subtopic

[Platform notes](platform-notes.md) — how the mission looks on
simulation, Carologistics/Robotino, and ALeRT/Spot specifically.

## Sources

- [Nav2 tutorials](https://docs.nav2.org/humble/tutorials/)
