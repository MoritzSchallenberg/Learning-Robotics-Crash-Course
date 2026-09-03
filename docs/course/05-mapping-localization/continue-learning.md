# Continue learning

## Next steps

:::{dropdown} Loop closure — Next step
:icon: light-bulb

**What it is.** SLAM's correction mechanism: recognising that the robot has
returned to a **previously seen place**, and using that match to correct
the accumulated drift in everything mapped since — this is the actual
mechanism behind "why mapping needs SLAM, not just odometry" from [Mapping
and SLAM: how it works](../05-mapping-localization/mapping-and-slam.md#how-it-works).

**Why it matters.** A map built without ever closing a loop keeps
accumulating drift the whole time; a large mapped area can end up visibly
misaligned with itself (a corridor that should form a rectangle "doesn't
quite close") without one.

**Needs.** [The practical exercise](practical-exercise.md).

**Try it.** Map an area that includes a loop (drive around a full
rectangle of furniture or a room's perimeter back to your start point) and
compare the map's visual alignment to the same area mapped as a single
out-and-back path with no loop.

**Check.** You can point to a visible seam or misalignment in the
no-loop-closure map that the loop-closed map does not have.

**Read more.** [SLAM Toolbox: loop
closure](https://github.com/SteveMacenski/slam_toolbox#zzz-loop-closure)
:::

:::{dropdown} Evaluating map quality — Next step
:icon: light-bulb

**What it is.** Looking at a finished occupancy grid critically: are walls
single, crisp lines (good) or doubled/smeared (bad, from driving too fast —
[the practical exercise's](practical-exercise.md#common-problems) Common
problems section)? Is there unexplained "noise" occupying open floor?

**Why it matters.** Navigation in [module 6](../06-navigation.md) trusts this
map completely; a smeared or noisy map produces a robot that refuses to
plan through a doorway that is actually clear.

**Needs.** [The practical exercise](practical-exercise.md).

**Try it.** Open your saved `map.pgm` in an image viewer and identify any
doubled walls or spurious occupied cells, then re-map the same area more
slowly and compare.

**Check.** The slower re-map has visibly cleaner (thinner, more
consistent) walls than the first attempt.

**Read more.** [The practical exercise's Common
problems](practical-exercise.md#common-problems) already names the usual
causes.
:::

:::{dropdown} Saving, versioning and updating maps — Next step
:icon: light-bulb

**What it is.** A saved map (`map.pgm` + `map.yaml`) is just two files —
treat them like any other project artefact: committed to git alongside the
package that uses them, and re-saved (a new pair of files, not an
overwrite) whenever the mapped area actually changes.

**Why it matters.** A team running localization against a six-month-old map
of a room that has since been rearranged gets exactly the "scan slides
through what should be a wall" symptom
[the practical exercise's Verification](practical-exercise.md#verification)
warns about — an out-of-date map is a silent failure mode, not a crash.

**Needs.** [Git prerequisite](../../prerequisites/git.md) and
[the practical exercise](practical-exercise.md).

**Try it.** Commit your saved map files to a git repository, then re-map
the same area with one object moved, save under a new filename, and commit
that as a second version.

**Check.** `git log` shows both map versions, and you can explain from the
commit messages alone which is current.

**Read more.** [Module 8: reproducible
systems](../08-integration/system-bringup-and-diagnostics.md) — the same "one source of
truth, in version control" principle.
:::

## Intermediate projects

:::{dropdown} SLAM Toolbox and AMCL parameters worth tuning — Intermediate
:icon: light-bulb

**What it is.** Both SLAM Toolbox and AMCL ship with many tunable
parameters; a handful matter far more than the rest for typical
first-time problems — SLAM Toolbox's `minimum_travel_distance` and
`minimum_travel_heading` (how far the robot must move before adding a new
scan), and AMCL's `min_particles`/`max_particles` and `update_min_d`
(how many pose hypotheses it tracks, and how far it must move before
re-evaluating them).

**Why it matters.** The default parameters are reasonable starting points,
not guaranteed-correct values for your specific robot and environment;
tuning them is usually faster than debugging a symptom that a parameter
change would have prevented.

**Needs.** [The practical exercise](practical-exercise.md), working end to
end.

**Try it.** Halve AMCL's `max_particles` from its configured value, re-run
localization, and observe whether convergence becomes noticeably less
stable (watch the particle cloud spread in RViz).

**Check.** You can describe, concretely, what changed in the particle
cloud's behaviour between the two settings.

**Read more.** [Nav2: configuring
AMCL](https://docs.nav2.org/humble/configuration_and_development/configuration_guide/others/configuring_amcl/) ·
[SLAM Toolbox parameters](https://github.com/SteveMacenski/slam_toolbox#configuration)
:::

:::{dropdown} The kidnapped-robot problem and detecting localization loss — Intermediate
:icon: light-bulb

**What it is.** The **kidnapped-robot problem**: a robot's estimated
position is wrong (a bad initial pose, or genuinely picked up and moved
without odometry seeing it) and it must recover without external help —
you already reproduced a version of this in
[the practical exercise's Optional
extensions](practical-exercise.md#optional-extensions), and it is
introduced conceptually in [Localization and 3D mapping: how it
works](../05-mapping-localization/localization-and-3d-mapping.md#how-it-works).
Detecting the loss automatically (rather than a human noticing the scan
drifting through a wall) means watching AMCL's reported **covariance**: a
healthy, converged localization has low covariance; a lost one has high,
growing covariance.

**Why it matters.** A mission that keeps navigating confidently on a wrong
pose estimate is worse than one that stops and asks for help — this is
exactly the kind of silent failure the
[capstone project's](../hackathon.md#self-assessment-checklist) safety
thinking cares about.

**Needs.** [The practical exercise's Optional
extensions](practical-exercise.md#optional-extensions) (deliberately
losing localization) completed once already.

**Try it.** Subscribe to `/amcl_pose` and log its covariance values before
and after deliberately "kidnapping" the robot (moving it without driving
it there) as in the practical exercise's Optional extensions; write a
simple threshold check that would flag "likely lost".

**Check.** Your threshold correctly flags the post-kidnap covariance as
high, and does not falsely flag the normal, converged covariance from
before.

**Read more.** [AMCL: overview and pose
covariance](https://docs.nav2.org/humble/configuration_and_development/configuration_guide/others/configuring_amcl/)
:::

## Advanced topics

:::{dropdown} Multi-session mapping — Advanced
:icon: light-bulb

**What it is.** Extending or merging a previously saved map in a **new**
mapping session, rather than always starting from an empty map — SLAM
Toolbox supports loading an existing map as the starting point for further
mapping.

**Why it matters.** Re-mapping an entire building from scratch every time
one room changes does not scale; multi-session mapping lets you update just
the part that changed.

**Needs.** A previously saved map from [the practical
exercise](practical-exercise.md).

**Try it.** {{ unverified }} — start SLAM Toolbox in its "continue mapping"
mode against your saved map, extend it into an adjacent area you have not
mapped yet, and save the result.

**Check.** The newly saved map contains both the original mapped area and
the newly extended area, correctly aligned with each other.

**Read more.** [SLAM Toolbox: continuing a
map](https://github.com/SteveMacenski/slam_toolbox#continuing-a-map)
:::
