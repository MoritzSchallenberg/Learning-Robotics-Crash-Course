# Planning approaches

{{ advanced }}

## What this topic is

Two tools beyond the state machine/behavior tree pattern from [Mission
logic](mission-logic.md): a graphical state machine editor (RAFCON), and
two **planning** systems that decide *what* to do rather than being told
*how* (PlanSys2, Golog++).

## Why a robot needs it

[Mission logic's](mission-logic.md) state machines and behavior trees say
*how* — every transition, explicitly. A planner says *what*, and works out
the how itself; that trade-off matters once a mission has too many
situations to enumerate by hand.

## How it works

(rafcon-a-graphical-state-machine-tool)=
### RAFCON — a graphical state machine tool

{{ alert }} [RAFCON](https://github.com/DLR-RM/RAFCON) is a graphical state
machine editor and execution engine from DLR, used by the ALeRT team. You
drag states and draw transitions; each state's body is Python:

```python
def execute(self, inputs, outputs, gvm):
    node = gvm.get_variable("new_ros2_node", True)
    publisher = node.create_publisher(String, '/chatter', 10)
    publisher.publish(String(data='I am in State 1'))
    return "success"
```

The pattern that matters: initialise **one** ROS 2 node at the start of the
machine, put it in the shared Global Variable Manager, and have every state
fetch it from there — never call `rclpy.shutdown()` inside a state, or every
state after it fails.

Full walkthrough and the ROS 2 subscription pattern:
[ALeRT/Spot platform page](../platforms/spot/index.md#high-level-control).

### PlanSys2 and Golog++ — planning instead of programming the mission

{{ research }} Neither is part of ALeRT's competition-ready path today —
tag this subsection Research, distinct from RAFCON above (Advanced, but
actively used).

**[PlanSys2](https://plansys2.github.io/)** is a ROS 2 planning system based
on PDDL. You describe the world as predicates ("robot is at the shelf",
"gripper is empty") and actions with preconditions and effects; given a
goal, the planner produces — and re-plans — a sequence of actions.

**[Golog++](https://github.com/MASKOR/gologpp)** is an action language,
developed with institute involvement, sitting between the two: you write a
partially specified procedure and leave the rest to the planner. ALeRT's
own [`gologpp-ros`](https://github.com/RRL-ALeRT/gologpp-ros) fork
documents a real Blocksworld example combining Webots, Spot and the
manipulator — see
[`gpp_action_examples`](https://github.com/RRL-ALeRT/gpp_action_examples)
for further action examples.

**How they compare to a state machine or behavior tree:**

```{list-table}
:header-rows: 1
:widths: 28 24 24 24

* -
  - State machine
  - Behavior tree
  - Planner (PlanSys2 / Golog++)
* - You specify
  - Every transition
  - Tree structure + leaves
  - Goal + available actions
* - Adapts to
  - Nothing unplanned
  - Known failure patterns
  - Situations you did not anticipate
* - Cost
  - Grows with states
  - Grows with tree size
  - A formal domain model, up front
* - Debugging
  - Step through states
  - Step through ticks
  - Read the plan the solver chose
```

Planning is the right tool when the world is too varied to enumerate in
advance. {{ documented }} ALeRT does not currently run PlanSys2 or Golog++
for competition missions — RAFCON is the team's primary high-level
control tool. Treat this section as orientation for further reading, not
a tool this site's tutorials build with.

## Verification status

{{ documented }} RAFCON: confirmed via the team's own repositories and the
[platform page's high-level control
section](../platforms/spot/index.md#high-level-control).
{{ documented }} Golog++/`gologpp-ros`: repository exists and documents a
real example; not independently re-verified on hardware or in simulation
by this site.

## Common limitations

- **RAFCON's Global Variable Manager is a single shared namespace.** A key
  collision between two states silently overwrites data rather than
  raising an error — name keys carefully.
- **Neither PlanSys2 nor Golog++ is part of ALeRT's competition-ready
  path today.** Both are genuine, documented capabilities worth learning,
  but a mission built for a live rescue task currently uses RAFCON, not
  a PDDL planner.

## Continue learning

See [Continue learning](continue-learning.md) for hierarchical state
machines, PDDL, PlanSys2 execution details, and Golog++ in more depth.

## Interesting videos

See [Interesting videos](videos.md).
