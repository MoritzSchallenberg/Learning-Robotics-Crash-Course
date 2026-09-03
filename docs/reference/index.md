# Reference

Material to look things up in, rather than to read through.

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} ROS 2 cheat sheet
:link: ros2-cheatsheet
:link-type: doc

Every command you will actually use, grouped by what you are trying to do —
plus a diagnostic sequence for when nothing works.
:::

:::{grid-item-card} Supported environment
:link: compatibility
:link-type: doc

The course's fixed toolchain — Ubuntu 22.04, ROS 2 Humble — and the
per-track simulator and package versions.
:::

:::{grid-item-card} Glossary
:link: glossary
:link-type: doc

Every term used in the course, in plain language, with a link to where it is
explained properly.
:::

::::

## Quick answers

**"Nothing is being published."**
→ [Diagnostic sequence](ros2-cheatsheet.md#diagnostic-sequence)

**"RViz shows nothing and there is no error."**
→ QoS mismatch.
[Module 3](../course/03-sensors-tf/practical-exercise.md#common-problems)

**"What exact software versions does this course use?"**
→ [Supported environment](compatibility.md)

**"What does that acronym mean?"**
→ [Glossary](glossary.md)

**"Everything times out in simulation."**
→ `use_sim_time`.
[Simulation](../platforms/simulation.md#simulation-time)

```{toctree}
:hidden:
:maxdepth: 1

ros2-cheatsheet
compatibility
glossary
```
