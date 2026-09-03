# Continue learning

## Next steps

(tuning-task-costmap-parameter)=
:::{dropdown} Tuning task: measuring what a costmap parameter actually does — Next step
:icon: light-bulb

**What it is.** A guided before/after measurement, not just reading about
parameters: change one costmap value, re-run the practical task's goal, and
record what actually changed.

**Why it matters.** [Nav2 architecture and costmaps'](nav2-architecture-and-costmaps.md#how-it-works)
tip already claims the inflation radius controls doorway behaviour; this
task makes you verify that claim yourself rather than take it on faith —
the same "measure it, do not guess" standard as this course's
power-budgeting exercise in
[module 1](../01-hardware/continue-learning.md).

**Needs.** [The practical exercise](practical-exercise.md), working end to
end.

**Try it.** Record the time-to-goal and the path's minimum distance to any
obstacle for your practical exercise's run. Increase the inflation radius
by 50%, re-run the identical goal, and record both numbers again.

**Check.** You have two comparable measurements (before/after) and can
state, in one sentence, what the larger inflation radius actually cost or
gained.

**Read more.** [Nav2: costmap
configuration](https://docs.nav2.org/humble/configuration_and_development/configuration_guide/core_servers/costmap_2d/index.html)
:::

## Intermediate projects

(recovery-behaviors-and-bt)=
:::{dropdown} Recovery behaviors and behavior trees in Nav2 — Intermediate
:icon: light-bulb

**What it is.** The **Behavior Server** runs recovery actions (spin, back
up, wait) when the planner or controller gets stuck; the **BT Navigator**
coordinates the whole sequence — planning, following, recovering — using a
behavior tree, the same formalism
[module 7](../07-autonomous-decisions.md#core-concepts) covers for mission
logic.

**Why it matters.** [The practical exercise's](practical-exercise.md#common-problems)
Common problems already names "the robot spins in place and gives up" as
expected recovery behaviour; understanding the tree that drives it is what
lets you change *when* and *how* it recovers, instead of just observing
that it does.

**Needs.** [The practical exercise](practical-exercise.md).

**Try it.** Find your Nav2 configuration's behavior tree XML file (often
`navigate_w_replanning_and_recovery.xml` or similar) and identify, by
reading it, which recovery action runs first when the planner fails.

**Check.** You can name the first recovery action from the XML, and
confirm it matches what you actually observed in
[the practical exercise's Optional
extensions](practical-exercise.md#optional-extensions) (surrounding the
robot with obstacles).

**Read more.** [Nav2: behavior
trees](https://docs.nav2.org/humble/configuration_and_development/configuration_guide/core_servers/bt_plugins/)
:::

:::{dropdown} Waypoint missions, keepout and speed zones — Intermediate
:icon: light-bulb

**What it is.** Three related Nav2 capabilities beyond a single goal:
**waypoint following** (a queue of goals visited in order, via
`nav2_waypoint_follower`), **keepout zones** (regions the planner must never
route through, layered onto the costmap), and **speed zones** (regions
where maximum velocity is reduced, independent of the global speed limit).

**Why it matters.** This is the direct bridge to the
[capstone project's](../hackathon.md#the-mission) multi-step mission —
"reach a target area", "handle more than one target" — expressed as Nav2
primitives instead of one-off custom code.

**Needs.** [The practical exercise](practical-exercise.md).

**Try it.** Configure `nav2_waypoint_follower` with two or three goal poses
in your test area and run it as a single mission instead of individual
**Nav2 Goal** clicks.

**Check.** The robot visits all configured waypoints in order, in one
continuous run, with no manual goal-setting between them.

**Read more.** [Nav2: waypoint
following](https://docs.nav2.org/humble/tutorials/docs/navigation2_with_waypoint_following.html) ·
[Nav2: keepout
zones](https://docs.nav2.org/humble/tutorials/docs/navigation2_with_keepout_filter.html)
:::

## Advanced topics

(docking-and-navigating-through-poses)=
:::{dropdown} Docking and navigating through poses — Advanced
:icon: light-bulb

**What it is.** **Navigate Through Poses** drives through a sequence of
intermediate poses on the way to a final goal (unlike waypoint following,
it does not stop and re-plan at each one); **docking**
(`opennav_docking`) is a specialised final-approach behaviour for precisely
reaching a charging station or a work cell.

**Why it matters.** {{ carologistics }} Robotino's precision-docking task
([module 1](../01-hardware/sense-process-act.md#how-it-works)) is exactly
this problem — a generic navigation goal is not precise enough for docking
to a production machine within millimetres.

**Needs.** [The practical exercise](practical-exercise.md).

**Try it.** {{ unverified }} — compare `NavigateToPose` and
`NavigateThroughPoses` by sending the same intermediate waypoint as either
a full stop-and-replan goal, or as a pass-through pose, and observe the
difference in the robot's path smoothness.

**Check.** You can describe, from what you observed, the concrete
difference in robot behaviour between the two action types.

**Read more.** [Nav2: Navigate Through
Poses](https://docs.nav2.org/humble/behavior_trees/trees/nav_through_poses_recovery.html) ·
[Nav2: docking](https://docs.nav2.org/humble/configuration_and_development/configuration_guide/others/docking_server.html)
:::

(systematic-tuning-and-navigation-metrics)=
:::{dropdown} Systematic tuning and navigation metrics — Advanced
:icon: light-bulb

**What it is.** Measuring navigation performance with actual numbers
instead of "it seemed fine": **success rate** (goals reached ÷ goals
attempted, over many trials), **time to goal**, and **minimum obstacle
distance** during the run — the same three numbers the
[capstone project's](../hackathon.md#self-assessment-checklist)
self-assessment implicitly depends on being good.

**Why it matters.** A single successful demo run proves the system *can*
work; a measured success rate over many runs is what tells you whether it
*reliably* works — the difference matters enormously for the capstone
project.

**Needs.** The tuning-task topic above, run more than once.

**Try it.** Run [the practical exercise's](practical-exercise.md) goal ten
times in a row (resetting between each), logging success/failure,
time-to-goal and minimum obstacle distance for each attempt.

**Check.** You can report an actual success rate (e.g. "8/10") rather than
a single anecdote, plus the mean time-to-goal across successful runs.

**Read more.** [Nav2:
benchmarking](https://docs.nav2.org/humble/tutorials/docs/navigation2_with_gps.html)
— search the Nav2 docs for the specific benchmarking tooling current at
the time you read this; it has changed across releases.
:::

:::{dropdown} Autonomous exploration — Advanced
:icon: light-bulb

**What it is.** Sending one goal is navigation; choosing your own goals is
exploration. The simplest version picks random reachable points and
navigates to each in turn — a starting pattern, not a good one, since it
wastes time revisiting known areas. **Frontier exploration** is the better
approach: find the boundary between known-free and unknown space, drive to
the nearest one, repeat until no frontiers remain.

**Why it matters.** This is directly useful for the
[capstone project](../hackathon.md)'s optional "explore an unknown area"
extension.

**Needs.** [The practical exercise](practical-exercise.md), working end to
end.

**Try it.** {{ unverified }} — set up
[`nav2_wfd`](https://github.com/SeanReg/nav2_wavefront_frontier_exploration)
(or a similar frontier-exploration package) against your own map and let
it choose goals on its own for a small, bounded area.

**Check.** The robot visits every reachable part of the bounded area
without you setting a single goal manually, and stops once no frontiers
remain.

**Read more.** [`nav2_wfd`](https://github.com/SeanReg/nav2_wavefront_frontier_exploration)
:::
