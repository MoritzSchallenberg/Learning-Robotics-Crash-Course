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

:::{grid-item-card} Versions and compatibility
:link: compatibility
:link-type: doc

Which platform runs which Ubuntu, which ROS 2 distribution, and which
simulator — and where the source material contradicts itself.
:::

:::{grid-item-card} Glossary
:link: glossary
:link-type: doc

Every term used in the course, in plain language, with a link to where it is
explained properly.
:::

:::{grid-item-card} Sources and licenses
:link: sources
:link-type: doc

Where this material came from, how it was used, what was excluded, and the
licenses of the software the course teaches.
:::

::::

## Quick answers

**"Nothing is being published."**
→ [Diagnostic sequence](ros2-cheatsheet.md#diagnostic-sequence)

**"RViz shows nothing and there is no error."**
→ QoS mismatch.
[Module 3](../course/03-sensors-tf.md#common-problems)

**"Which ROS 2 distribution should I install?"**
→ [Compatibility matrix](compatibility.md)

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
sources
```
