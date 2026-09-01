# Decisions needed

Organisational and rights-holder decisions that this development pass could
not reliably make, and should not make on its own. Each is recorded here
with its current status, why it matters, and the trade-offs — not a
decision imposed on the institute's behalf.

**None of these block the technical completion of the site.** Every page
that depends on an unresolved item here says so explicitly (a visible
"Draft," an `{{ unverified }}` badge, or a note pointing back to this file)
and degrades gracefully rather than guessing.

---

## 1. Final content license

**Current status**: undecided. No `LICENSE` file is present. `LICENSES.md`
and `docs/reference/sources.md` both flag this openly rather than assuming
an answer.

**Why a decision is needed**: the repository is public, and without an
explicit license, default copyright applies — nobody outside the institute
may legally reuse, adapt or redistribute the course text, which works
against the stated goal of a shared, growable course. The source material
also originates from three different teams (Summer School, Carologistics,
ALeRT); whoever holds rights to each needs to agree before any license is
attached to the combined result.

**Recommended option**: not a specific license — that choice belongs to the
rights holders, not to this development pass. What is recommended is the
*process*: institute leadership decides in consultation with the
Carologistics and ALeRT team leads (who hold rights to the source material
this course draws on), and records the outcome in a `LICENSE` file plus an
update to `LICENSES.md`.

**Possible alternatives, described neutrally**:

```{list-table}
:header-rows: 1
:widths: 26 74

* - Option
  - What it means
* - Keep "all rights reserved"
  - Simplest; the current default. Prevents reuse outside the institute even
    by other universities or teams who might benefit from it.
* - CC BY 4.0
  - Permissive; anyone may reuse and adapt with attribution. Common for
    public teaching material, but allows commercial reuse and adaptation the
    institute may not want.
* - CC BY-SA 4.0
  - Like CC BY, but adaptations must be shared under the same license. Keeps
    derivatives open; some organisations avoid "share-alike" terms for
    unrelated reasons (compatibility with other material they hold).
* - CC BY-NC 4.0
  - Like CC BY, but forbids commercial use. Common for educational content;
    "commercial" can be ambiguous in edge cases (e.g. a company running
    internal training from it).
* - An institute-specific license text
  - Full control over terms, but needs legal drafting and is unfamiliar to
    reusers compared to a standard Creative Commons license.
```

**Impact of not deciding**: the site remains legally "all rights reserved"
by default — usable by the institute itself, but not confidently reusable
or adaptable by anyone else, including future course maintainers outside
the original team.

---

## 2. Officially supported ROS distribution per team

**Current status**: `docs/reference/compatibility.md` documents a real,
unresolved contradiction — the Carologistics introductory setup guide
specifies Ubuntu 24.04 with ROS 2 Jazzy, while the `robotino_navigation`
repository documents and states it was tested on ROS 2 Humble. ALeRT/Spot is
consistently Humble on Ubuntu 22.04 throughout its source material, with no
contradiction found there.

**Why a decision is needed**: participants following the Carologistics
track cannot know which distribution their actual lab robots run without
being told, and following the wrong one produces failures that look like
broken code. This can only be resolved by someone checking what is
currently deployed on the physical robots — not by reading documentation
further, since the documentation is exactly what disagrees with itself.

**Recommended option**: the Carologistics team lead confirms, in one
sentence, which distribution is authoritative for the team's current robots
and workstations, and `docs/reference/compatibility.md` is updated to state
it as fact rather than an open contradiction.

**Possible alternatives**: (a) standardise the whole team on Jazzy/24.04
going forward, matching the newer LTS and the setup guide; (b) standardise
on Humble/22.04, matching what `robotino_navigation` is actually tested
against today; (c) confirm both are genuinely in concurrent use on
different machines, and document which machine runs which.

**Impact of not deciding**: this site continues to present the
contradiction honestly rather than picking a side, which is safe but leaves
new Carologistics members to discover the correct answer by trial and
error or by asking in person — exactly the friction this course exists to
remove.

---

## 3. Sign-off on the platform pages from ALeRT and Carologistics

**Current status**: `docs/platforms/alert-spot.md` and
`docs/platforms/carologistics-robotino.md` were written from the source
material exports and public repositories, restructured and rewritten for
this course. **Neither has been reviewed by the team it describes.**

**Why a decision is needed**: these pages make specific technical claims —
topic names, launch commands, hardware descriptions — that this
development pass could check against documentation but not against running
hardware. A team member who knows the current system should confirm nothing
has drifted since the source material was captured.

**Recommended option**: each team lead (or a delegated member) does one
read-through of their platform page against their current system before the
next public announcement of the site, and opens corrections as pull
requests or issues.

**Possible alternatives**: a lighter-weight review (spot-checking only the
commands marked `{{ unverified }}`) if a full read-through is not feasible
before the next course intake.

**Impact of not deciding**: the pages remain best-effort and clearly marked
as such wherever verification was not possible, but participants may hit
small inaccuracies (a renamed topic, a moved repository) that a five-minute
team review would have caught.

---

## 4. Sign-off on the newly created diagrams

**Current status**: ten original SVG diagrams were created for this
version (`docs/_static/images/diagrams/`), replacing the images excluded
from the source archive. They are original work — not copies or
derivatives of any source-archive image — but they simplify real systems
(Nav2's architecture, the TF tree, the hackathon arena) and a domain expert
has not checked them for technical accuracy.

**Why a decision is needed**: a diagram that is confidently wrong is worse
than no diagram, because it is more persuasive than prose. Someone who
knows Nav2, TF2 and the actual hackathon arena plan should confirm each
diagram matches reality closely enough for teaching purposes.

**Recommended option**: a facilitator or team lead reviews the ten diagrams
alongside the session pages that use them (listed in `CONTENT_REVIEW.md`)
in a single pass — they are simple enough that this is a short review, not
a redesign.

**Possible alternatives**: review only the two diagrams with the least
certain source material (the Nav2 architecture diagram and the hackathon
arena schematic, since the arena itself is also unconfirmed — see item 8).

**Impact of not deciding**: the diagrams stand as a good-faith,
technically-checked-against-documentation effort, but without a domain
expert's sign-off, a subtle simplification that misleads is possible and
would not have been caught by this development pass alone.

---

## 5. Real availability of robots and computers for the course

**Current status**: unknown to this development pass. The course assumes
"a pre-built workspace" and "a robot or simulation" are available at each
session, per the session pages' Preparation sections, but how many physical
Robotinos and Spots — and how many capable laptops or lab machines — will
actually be available on each of the eight evenings is an organisational
fact this site cannot determine.

**Why a decision is needed**: the run sheets assume tasks are completable
in the allotted time slice, which assumes enough hardware that participants
are not queueing for a single robot. Group sizes and task design should
match actual equipment availability.

**Recommended option**: whoever schedules the room and equipment confirms,
before the course starts, how many robots/simulation-capable machines will
be present per session, so facilitators can plan group sizes accordingly
(see item 6).

**Possible alternatives**: run every session simulation-first if hardware
is scarce, reserving physical robot time for a subset of sessions or for
office hours outside the 85-minute slot.

**Impact of not deciding**: facilitators discover equipment constraints
live, on the first session, which is exactly the kind of surprise the
85-minute format has no slack to absorb.

---

## 6. Participant numbers and group size

**Current status**: the hackathon page recommends teams of 2–4 based on a
reasonable guess, not a headcount. The eight course sessions do not specify
group size at all.

**Why a decision is needed**: task design (how many workspaces need to be
pre-built, how many robots are needed simultaneously, how the 85 minutes
divide) depends directly on how many participants and how many groups there
will be.

**Recommended option**: course organisers confirm expected enrolment before
the first session, and facilitators size groups so that every group has
hands-on time with hardware or simulation within the 85-minute task block.

**Possible alternatives**: cap enrolment to match confirmed hardware
availability (see item 5) rather than adjusting group size arbitrarily
upward.

**Impact of not deciding**: group sizes are set ad hoc on the first
evening, which likely works but was not planned.

---

## 7. Rooms and building access

**Current status**: not addressed anywhere on this site, deliberately —
this is exactly the kind of internal operational detail
`SECURITY_REVIEW.md` and `CONTENT_REVIEW.md` identify as inappropriate to
publish. Room booking, building access procedures and similar logistics
belong in the institute's internal channels, not in a public repository.

**Why a decision is needed**: participants still need to know where to go
and how to get in — this course cannot function without that being
communicated, just not through this site.

**Recommended option**: course organisers communicate room and access
information through the institute's normal internal channels (Slack,
email, internal wiki), separate from this public repository.

**Possible alternatives**: none within scope of this site — this is purely
an internal communication task.

**Impact of not deciding**: participants do not know where to go. This has
no technical mitigation; it is a plain organisational task.

---

## 8. Final hackathon arena

**Current status**: `docs/course/hackathon.md` includes a **schematic**
arena diagram (start zone, obstacles, target zone, optional drop zone) that
fixes the *shape* of the mission so teams can build against something
concrete. It is explicitly not a scaled or confirmed layout — the actual
room, dimensions and obstacle placement depend on where the hackathon is
held, which was not knowable to this development pass.

**Why a decision is needed**: teams need real dimensions and a real venue
to test navigation and perception parameters against before the event, not
just the day of.

**Recommended option**: the hackathon organisers confirm the venue and
publish real arena dimensions and a scaled layout as early as possible
before 07 November 2026 — ideally with enough lead time for teams to
practice in a space of similar size.

**Possible alternatives**: if a fixed venue cannot be confirmed early, publish
a range of plausible dimensions so teams can test their navigation
parameters against the largest and smallest plausible cases.

**Impact of not deciding**: teams tune navigation and perception parameters
against the schematic sketch's implied scale rather than the real arena,
and may need to adjust on the day — a real risk, given how sensitive Nav2
tuning is to actual dimensions (see [session 6](docs/course/06-navigation.md)).

---

## 9. Final hackathon scoring rubric

**Current status**: `docs/course/hackathon.md` publishes a **Draft 0.1**
100-point rubric across eight categories, explicitly marked as a draft with
a `TODO-REVIEW` admonition, specifically so it can be criticised and
corrected before the event rather than presented as settled.

**Why a decision is needed**: the point values have not been tested against
the real arena, real robots, or a trial run, and collision detection is
assumed (but not confirmed) to be judged by a human referee rather than any
automated method.

**Recommended option**: course organisers run at least one trial attempt
(even informally, with one team's practice robot) against the draft rubric
before the event, adjust point values based on what that reveals, and
remove the Draft marking only once the rubric has been exercised for real.

**Possible alternatives**: keep the rubric as a living draft even into the
event itself, explicitly announced as "subject to referee discretion on
the day" if a trial run is not feasible beforehand.

**Impact of not deciding**: the rubric is used as-is, untested — plausible,
but with a real chance some category (most likely the point split between
navigation and perception) turns out to not reflect actual task difficulty
once teams attempt it.

---

## 10. Facilitators responsible for each session

**Current status**: not specified anywhere. `docs/instructors/` (added in
this version) documents *what* each session needs and *how* to prepare it,
but not *who* is running it.

**Why a decision is needed**: the instructor materials
(`docs/instructors/preparation-checklist.md`,
`docs/instructors/session-plans.md`) assume a facilitator is preparing
each specific evening in advance — pre-building workspaces, planting
faults, testing the demonstration. Someone needs to own that per session.

**Recommended option**: course organisers assign one named facilitator (plus
one backup) per session before the course starts, each confirming they have
read that session's page in `docs/instructors/session-plans.md` and
completed the corresponding preparation checklist.

**Possible alternatives**: a smaller core team rotates through all eight
sessions rather than assigning a different person per evening, trading
variety for consistency of delivery.

**Impact of not deciding**: a session's preparation (pre-built workspaces,
a planted fault for session 8, printed markers for session 4) may not
happen, which the 85-minute run sheets have no slack to recover from
mid-session.
