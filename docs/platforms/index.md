# ALeRT Platforms and Safety

## What belongs to this topic

The physical and simulated systems ALeRT actually builds and runs, and
the safety rules that apply to them: the Spot platform itself, the
electrical and mechanical design tools (KiCad, Fusion) used to build
hardware for it, and the safe start/stop and E-stop procedures that apply
whenever real hardware is involved.

## What it does in the overall system

Every other topic on this site (ROS 2, sensors, perception, mapping,
navigation, manipulation, decision-making) is *general* — it applies to
any ROS 2 robot. This category is where that general knowledge meets
ALeRT's actual, specific systems: exact topic names, exact launch files,
exact hardware, and the safety rules for the one platform this site
documents.

## Where ALeRT uses this

{{ alert }} Every subpage in this category is ALeRT-specific by
definition — there is no other team's platform documented on this site.

## Platforms

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} ALeRT / Spot
:link: spot/index
:link-type: doc

{{ documented }} Boston Dynamics Spot, RoboCup Rescue League. Legged
locomotion, 3D LiDAR, a manipulator arm. The team's primary platform.
:::

:::{grid-item-card} Hardware Design with KiCad and Fusion
:link: hardware-design/index
:link-type: doc

{{ foundation }} Electrical schematics in KiCad, parametric mechanical
parts in Fusion — the tools used to design physical hardware, independent
of any one robot.
:::

::::

For the simulation-only path (no physical hardware needed to work
through this site), see [Simulation](../simulation/index.md), a separate
top-level topic.

## Available tutorials

- [ALeRT / Spot](spot/index.md) — the platform reference: hardware,
  launch commands, RViz setup, services and actions, mapping and
  navigation, 3D mapping, manipulation with MoveIt, object detection,
  high-level control, and operating the physical robot.
- [Hardware Design with KiCad and Fusion](hardware-design/index.md) — a
  KiCad electrical-schematic tutorial and an Autodesk Fusion
  parametric-CAD tutorial, each with a practical task.

## Content already present

Both subpages above are complete, existing tutorials — this category was
assembled from already-migrated content, not written fresh.

## Planned content

- A **system architecture** overview tying the Spot platform's compute,
  sensors and actuators together in one diagram (currently, this
  information lives distributed across the Spot platform page's
  individual sections).
- Further verified platforms, if and when ALeRT documents one (see
  [`webots_ros2_go2`](https://github.com/RRL-ALeRT/webots_ros2_go2),
  whose Unitree Go2 support is explicitly marked "(Todo)" in its own
  README — not a verified platform yet).

## Required knowledge

[ROS 2](../ros2/index.md) fundamentals (nodes, topics, services, actions)
before the Spot-specific launch files and topic names on the platform
page make sense.

## Related ALeRT repositories

See each subpage's own repository list — [ALeRT /
Spot](spot/index.md#further-reading) and the audit in
[Robot Manipulation](../manipulation/index.md#related-alert-repositories)
for the manipulator specifically.

## Verification status

{{ simulation }} The Webots Spot simulation is confirmed working and is
the primary way this site's exercises are actually run.
{{ hardwareverified }} is claimed only where the platform page explicitly
says so; supervised-only real-hardware exercises are marked
accordingly — see [Safety levels](#safety-levels) below.

(safety-levels)=
## Safety levels

Every hands-on exercise involving the physical Spot carries exactly one
of three safety-level badges, defined once here and used throughout this
site:

```{list-table}
:header-rows: 1
:widths: 30 70

* - Badge
  - Meaning
* - {{ spotsim }}
  - Simulation only — no physical robot involved.
* - {{ spotreadonly }}
  - May be performed on the physical robot, but only by observing or
    reading state — no commands that move it.
* - {{ spotsupervised }}
  - May be performed on the physical robot, but only with a trained team
    member present, able to reach the E-stop.
```

See [ALeRT / Spot: operating the physical
robot](spot/index.md#operating-the-physical-robot) for the concrete
start/stop sequence and E-stop locations these levels assume.

## Common limitations

- **This site documents one platform.** Claims here do not generalise to
  any other robot; general ROS 2 concepts are covered separately under
  their own topics, precisely so they do not need repeating per platform.
- **Real-hardware verification is the exception, not the default.** Most
  claims here are {{ simulation }} or {{ documented }}, not
  {{ hardwareverified }} — check the specific claim's badge before
  assuming it was checked on the physical robot.

## Continue learning

See each subpage's own Continue learning section.

## Interesting videos

See each subpage's own video page where one exists.

```{toctree}
:hidden:
:maxdepth: 1

spot/index
hardware-design/index
```
