# Instructor guides

Material for whoever is facilitating a session or the hackathon — what to
prepare, how much time it takes, and what to expect from participants.

:::{note}
This section is public, like the rest of the site. It contains **no**
internal operational data — no credentials, no internal addresses, no
private repository links, no team scheduling. Where a real answer depends on
information specific to your team or venue, this section says so and points
at where that decision actually gets made, rather than inventing one — see
[`DECISIONS_NEEDED.md`](https://github.com/MoritzSchallenberg/Learning-Robotics-Crash-Course/blob/main/DECISIONS_NEEDED.md)
in the repository for the organisational decisions still open.
:::

## What is here

```{toctree}
:maxdepth: 1

preparation-checklist
session-plans
hackathon-setup
```

**[Preparation checklist](preparation-checklist.md)** — what every session
needs in general: devices, software, prep time, materials, the shape of a
good demonstration, and what to do when hardware fails mid-session.

**[Session plans](session-plans.md)** — per-session facilitator notes: what
package or workspace to pre-build, what to print, what fault to plant, and
the specific problems participants tend to hit on that particular evening.

**[Hackathon setup](hackathon-setup.md)** — running the closing event:
referee role, safety briefing, arena setup, scoring, and the
hardware-failure procedure in practice.

## Why this exists

Every session in the [course](../course/index.md) is built around a strict
**85-minute** run sheet with one Core practical task. That only works if the
task is *ready to start* the moment participants sit down — a workspace that
still needs building, a marker that still needs printing, or a fault that
still needs planting all eat directly into the 85 minutes that have no
slack for it. This section exists so that preparation happens **before** the
session, every time.

## The one rule that matters most

**Never make a participant install or build something large during the
session.** Every session page's "Starting point" describes a pre-built
workspace or package — build it *before* participants arrive, exactly as
each [session plan](session-plans.md) describes. A `colcon build` that takes
four minutes is four minutes gone from an 85-minute evening, times however
many participants hit it at once.
