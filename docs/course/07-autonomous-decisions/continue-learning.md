# Continue learning

## Next steps

:::{dropdown} The blackboard: sharing data between behavior tree nodes — Next step
:icon: light-bulb

**What it is.** A behavior tree's **blackboard** is shared key-value
storage every node in the tree can read and write — how a `Detect` leaf
passes a marker's position to a later `NavigateToMarker` leaf, without
either node needing a direct reference to the other.

**Why it matters.** [Mission logic's](mission-logic.md#behavior-trees-in-contrast)
Sequence and Fallback control *order*; the blackboard is how data actually
flows between the leaves that order controls — without it, a behavior
tree can only sequence actions, not pass results between them.

**Needs.** [Mission logic's](mission-logic.md) behavior-tree comparison.

**Try it.** {{ unverified }} — in a BehaviorTree.CPP or `py_trees` example,
write one leaf that writes a value to the blackboard and a second that
reads it, and confirm the second sees the first's value.

**Check.** The second leaf's read matches exactly what the first leaf
wrote, including after the tree re-ticks.

**Read more.** [BehaviorTree.CPP:
blackboard](https://www.behaviortree.dev/docs/tutorial-basics/tutorial_02_basic_ports)
:::

:::{dropdown} Action cancellation and preemption — Next step
:icon: light-bulb

**What it is.** Actively **cancelling** a running action
([module 2's](../02-ros2/services-parameters-actions.md#try-it-yourself-actions)
goal → feedback → result pattern) before it finishes — e.g. abandoning a
navigation goal because the mission decided on a better one — rather than
only ever waiting for natural completion or timeout.

**Why it matters.** [The practical exercise](practical-exercise.md) only
ever *waits* for `NAVIGATE` to finish or fail; a more responsive mission
needs to actively abandon a stale goal, the same responsiveness
[module 6's](../06-navigation/nav2-architecture-and-costmaps.md#inputs-and-outputs)
action client introduces but does not use.

**Needs.** [Module 6's action
client](../06-navigation/nav2-architecture-and-costmaps.md#inputs-and-outputs)
example.

**Try it.** Send a navigation goal, wait two seconds, then call
`goal_handle.cancel_goal_async()` before it completes, and confirm — via
the action's result — that it reports cancelled rather than succeeded or
failed.

**Check.** The action's result status is explicitly "cancelled", distinct
from both "succeeded" and "aborted".

**Read more.** [ROS 2: actions —
canceling goals](https://docs.ros.org/en/humble/Tutorials/Intermediate/Writing-an-Action-Server-Client/Py.html)
:::

## Intermediate projects

:::{dropdown} Lifecycle-controlled subsystems — Intermediate
:icon: light-bulb

**What it is.** Using a mission's state machine to actively control
subsystem **lifecycle** transitions
({ref}`module 2's <lifecycle-nodes>` lifecycle-node topic) — e.g.
only activating a perception pipeline once the mission actually reaches a
`SEARCH` state, rather than every subsystem running full-time from
start-up.

**Why it matters.** This saves real compute and power on a resource-limited
onboard computer, and makes a subsystem's "is it supposed to be doing
anything right now" question answerable from mission state alone.

**Needs.** {ref}`Module 2's lifecycle nodes <lifecycle-nodes>` and
[the practical exercise](practical-exercise.md).

**Try it.** Convert your practical exercise's marker detector into a
lifecycle node, and have the `SEARCH` state call `ros2 lifecycle set` to
activate it on entry and deactivate it on exit.

**Check.** `ros2 lifecycle get` on the detector reports `inactive` outside
`SEARCH` and `active` only while the mission is actually in that state.

**Read more.** [ROS 2: managed
nodes](https://docs.ros.org/en/humble/Concepts/Intermediate/About-Ros2-Managed-Nodes.html)
:::

:::{dropdown} Mission monitoring — Intermediate
:icon: light-bulb

**What it is.** A separate node that observes a mission's status
transitions and logs them with timing, without participating in the
mission itself — you will meet exactly this pattern as the optional
**Mission monitoring node** on the
[capstone project's mission monitoring
page](../hackathon/mission-monitor.md).

**Why it matters.** Debugging a mission after the fact needs a record of
what it actually did and when; building that as a separate observer keeps
the mission's own state machine simple and unburdened by logging detail.

**Needs.** [The practical exercise](practical-exercise.md), publishing
`/mission_status`.

**Try it.** Write a small node that subscribes to `/mission_status`, times
how long the mission spends in each reported state, and prints a summary
when the mission finishes.

**Check.** The summary's total duration matches your own stopwatch timing
of one run, within a second or two.

**Read more.** [Capstone project: mission monitoring
node](../hackathon/mission-monitor.md) has a complete, runnable example.
:::

## Advanced topics

(planning-scene-and-collision-objects)=
:::{dropdown} Planning scene and collision objects — Advanced
:icon: light-bulb

{{ alert }} **What it is.** MoveIt 2's **planning scene** is its model of
everything the arm must avoid — the robot itself, and **collision
objects** you add to represent the environment (a table, a shelf, the
object being grasped). Motion planning fails deliberately rather than
producing a colliding trajectory if the scene says a path is blocked.

**Why it matters.** A pick-and-place sequence
([the MoveIt and manipulation
section](planning-and-manipulation.md#moveit-and-manipulation)) that plans
without telling MoveIt about the table in front of the robot will happily
plan a path *through* that table — the planning scene is what prevents
that.

**Needs.** [The MoveIt and manipulation
section](planning-and-manipulation.md#moveit-and-manipulation).

**Try it.** {{ unverified }} — add a box collision object to the planning
scene representing a table surface, then request a motion plan to a pose
that would require passing through it, and confirm planning fails or
routes around it instead of through it.

**Check.** The same goal pose plans successfully once the collision object
is removed, and fails or replans once it is present — a direct before/after
comparison.

**Read more.** [MoveIt 2: planning scene and collision
objects](https://moveit.picknik.ai/main/doc/examples/planning_scene/planning_scene_tutorial.html)
:::

:::{dropdown} A simple pick-and-place pipeline — Advanced
:icon: light-bulb

{{ alert }} **What it is.** Chaining the pieces above into one mission:
detect an object ([module 4](../04-perception/index.md)), plan a
collision-free approach (planning scene, above), grasp, lift, and place —
expressed as states with their own failure exits, exactly [Mission
logic's](mission-logic.md) core pattern applied to manipulation instead of
navigation.

**Why it matters.** This is the concrete synthesis of most of this course:
perception, TF, and now planning and manipulation, all inside one state
machine.

**Needs.** [Planning scene and collision objects](#planning-scene-and-collision-objects)
above, and [module 4's](../04-perception/index.md) marker detection.

**Try it.** {{ unverified }} — extend [the practical exercise's](practical-exercise.md)
state machine with `APPROACH`, `GRASP` and `PLACE` states, each calling
into MoveIt, each with an explicit failure exit (e.g. "inverse kinematics
returned no solution" → a named failure state, not a crash).

**Check.** Running the extended mission with an intentionally unreachable
target pose ends in your named failure state, not a hang or a traceback.

**Read more.** [ALeRT/Spot: manipulation with
MoveIt](../../platforms/alert-spot.md#manipulation-with-moveit)
:::

:::{dropdown} Multi-robot task allocation — Advanced
:icon: light-bulb

**What it is.** Deciding *which* robot does *which* part of a mission when
more than one is available — from a simple fixed split (robot A always
searches, robot B always delivers) to an auction-based approach where
robots bid on subtasks based on their own cost estimate.

**Why it matters.** This is the natural extension of the
{ref}`capstone project's <optional-extensions-capstone>` "communicate
with a second robot" optional extension — coordinating two independent
state machines is a different problem than running one.

**Needs.** [The practical exercise](practical-exercise.md), and access to
(or simulation of) a second robot.

**Try it.** {{ unverified }} — on paper, design a simple allocation rule
for two robots and one mission with two subtasks (e.g. "search area A" and
"search area B"), and state what message each robot would need to publish
for the other to know the task is claimed.

**Check.** Your design avoids both robots claiming the same subtask and
leaving the other subtask unclaimed — trace through the message sequence
by hand to confirm.

**Read more.** {{ unverified }} — multi-robot coordination tooling in ROS 2
is an active area with no single standard package this course pins;
search current literature on "multi-robot task allocation ROS 2" when you
reach this point.
:::
