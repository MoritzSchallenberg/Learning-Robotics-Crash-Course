# Continue learning

Each topic below is a real next step, not just a keyword. KiCad and
Fusion are full pages with their own practical task, linked from the
[module overview](../01-system-hardware.md); the rest are dropdowns here.

## Next steps

:::{dropdown} Choosing sensors and actuators — Next step
:icon: light-bulb

**What it is.** Picking a specific sensor or actuator for a task, based on
its actual specifications — range, field of view, update rate, current
draw — rather than "the one the last team used".

**Why it matters.** [Sense–process–act](sense-process-act.md) tells you a
stage needs a sensor; it does not tell you *which* one. A LiDAR with too
narrow a field of view, or a motor that cannot supply enough torque at
the robot's target speed, produces a system that "should" work and does
not.

**Needs.** [Sense–process–act](sense-process-act.md).

**Try it.** Pick one sensor and one actuator from a platform page
([Carologistics/Robotino](../../platforms/carologistics-robotino.md) or
[ALeRT/Spot](../../platforms/alert-spot.md)) and write down, from its
datasheet, the one specification that most limits what the robot can do
with it.

**Check.** You can name the limiting number (not just the part name) and
explain, in one sentence, what breaks if that number is exceeded.

**Read more.** [ROS 2 hardware
integration](https://docs.ros.org/en/humble/) — start from a driver
package's README for the sensor family you picked.
:::

:::{dropdown} Power and battery budgeting — Next step
:icon: light-bulb

**What it is.** Adding up every component's current draw at its supply
voltage to get a total power budget, then dividing battery capacity by that
total to estimate runtime.

**Why it matters.** "The battery died mid-run" is one of the most common,
most avoidable robot failures, and it is arithmetic, not guesswork — a
computer, a LiDAR, and two motors under load draw a very predictable
current.

**Needs.** [Sense–process–act's power
section](sense-process-act.md#power-supply-and-energy-budgeting).

**Try it.** For a platform page's listed components, estimate each
component's typical current draw (from its datasheet or a reasonable
published figure), sum them at each voltage rail, and divide a plausible
battery capacity (Wh) by the total power (W) to get an estimated runtime in
hours.

**Check.** Your estimate is within a sensible order of magnitude of what
the platform page or team documentation states, and you can show the
arithmetic that got you there.

**Read more.** {{ unverified }} — battery chemistry and exact runtime
depend on the specific pack; treat any number here as an estimate to verify
against the real hardware, not a guarantee.
:::

## Intermediate projects

:::{dropdown} Communication interfaces: CAN, Ethernet, USB, UART, I²C — Intermediate
:icon: light-bulb

**What it is.** The wired links that connect a robot's parts, each suited
to a different job:

```{list-table}
:header-rows: 1
:widths: 14 30 28 28

* - Interface
  - Typical use
  - Distance / speed
  - Multi-device?
* - CAN
  - Motor controllers, distributed real-time control
  - Long runs, robust to noise, moderate speed
  - Yes, natively (multi-drop bus)
* - Ethernet
  - Onboard computer ↔ sensors (cameras, some LiDAR)
  - Fast, network-based
  - Yes, via switches
* - USB
  - Onboard computer ↔ a nearby sensor or microcontroller
  - Short runs, high speed
  - One host, several devices (hub)
* - UART
  - Microcontroller ↔ computer, simple point-to-point
  - Short runs, low-to-moderate speed
  - No (point-to-point)
* - I²C
  - Microcontroller ↔ nearby small sensors/ICs on one board
  - Very short runs, low speed
  - Yes, natively (addressed bus)
```

**Why it matters.** Picking the wrong interface for a job — I²C across a
robot chassis, for instance — produces exactly the kind of noise-sensitive,
intermittent fault that looks like a software bug.

**Needs.** [Sense–process–act's computing
section](sense-process-act.md#computing-and-microcontrollers).

**Try it.** For each interface above, name one component from a platform
page that plausibly uses it, based on the interface's characteristics.

**Check.** Your four choices are each defensible from the table above, not
guessed.

**Read more.** [ROS 2 hardware driver
packages](https://docs.ros.org/en/humble/) typically state which interface
they expect in their own README.
:::

:::{dropdown} Fuses, wire sizing and a hardware BOM — Intermediate
:icon: light-bulb

**What it is.** Sizing a fuse and its wire to the actual current a circuit
carries (a fuse rated too high protects nothing; a wire too thin for its
current overheats), and keeping a **bill of materials (BOM)** — every part,
its value, and its source — as the design's single source of truth.

**Why it matters.** This is the mechanical/electrical equivalent of
[module 8's](../08-integration.md#core-concepts) "one command, one source
of truth" for software configuration — a design that lives only in one
person's head, or an out-of-date drawing, fails the same way undocumented
config does.

**Needs.** The power-budgeting topic above, and (optionally) the
[KiCad tutorial](kicad-schematic.md).

**Try it.** For one supply rail from your power-budgeting exercise, look up
a wire-gauge-vs-current table and state the minimum wire gauge for that
current, then pick a fuse rated between the normal operating current and
the wire's maximum.

**Check.** Your fuse rating is higher than normal operating current but
lower than what the wire can safely carry — if either is not true, the
choice is wrong.

**Read more.** [KiCad tutorial: fuses and a safe-stop
path](kicad-schematic.md#core-concepts-in-the-editor) covers how
to represent this in a schematic.
:::

:::{dropdown} Diagnostics: adding measurement points — Intermediate
:icon: light-bulb

**What it is.** Deliberately designing in places to measure a signal or
voltage — a test point, an accessible connector, a status LED — rather than
discovering after the fact that nothing is probeable without desoldering
something.

**Why it matters.** [Module 8's](../08-integration.md#core-concepts)
eight-step diagnostic procedure assumes you *can* check each layer;
hardware with no measurement points makes step 1 ("is it powered?")
surprisingly hard to answer.

**Needs.** [Sense–process–act's power
section](sense-process-act.md#power-supply-and-energy-budgeting).

**Try it.** Pick one power rail from your practical exercise's diagram and
name one concrete, physical way you could check its voltage without
disassembling anything.

**Check.** Your answer names an actual accessible point (a connector pin, a
test pad), not just "measure it somehow".

**Read more.** [Module 8: the eight-step diagnostic
procedure](../08-integration.md#core-concepts)
:::

## Advanced topics

:::{dropdown} Hardware-in-the-loop testing — Advanced
:icon: light-bulb

**What it is.** Running real control software against real electronics
(a motor controller, a sensor board) while the rest of the system —
physics, other sensors — stays simulated. A middle ground between pure
simulation and a full physical robot.

**Why it matters.** It catches integration bugs between real hardware and
your software that pure simulation cannot see, without needing the whole
robot assembled.

**Needs.** A working simulation setup ([module 8's simulation
notes](../08-integration.md#optional-extensions)) and access to at least one
piece of real hardware (a motor controller or sensor board).

**Try it.** {{ unverified }} — describe, on paper, how you would connect
one real component (e.g. a motor controller) to your simulated robot's
command topic, and what you would need to fake on the simulation side for
that to work.

**Check.** Your plan identifies exactly which signal crosses from
simulated to real hardware, and in which direction.

**Read more.** [ROS 2 and hardware
interfaces](https://docs.ros.org/en/humble/) — search for `ros2_control`,
the standard ROS 2 hardware-abstraction framework.
:::
