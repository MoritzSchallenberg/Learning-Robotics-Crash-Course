# KiCad: schematics for robotic systems

{{ optional }}

[Module 1](../01-system-hardware.md) taught the sense–process–act loop as a
*block diagram* — boxes and arrows, no electrical detail. This page teaches
the next level down: a real **electrical schematic**, drawn in
[KiCad](https://www.kicad.org/), the free and open-source EDA tool most
robotics teams actually use.

The goal is **not** to design a complete circuit board. It is to be able to
read and draw a schematic clear enough that someone else on the team — or
you, six months later — can trust it: what powers what, what talks to what,
and where the emergency stop actually cuts power.

## Learning objectives

By the end of this page you can:

1. explain the difference between a system diagram (module 1) and an
   electrical schematic;
2. place, wire and label symbols in KiCad, distinguishing data and power
   nets;
3. run and interpret an Electrical Rules Check (ERC);
4. export a schematic other people can actually read.

## Prerequisites

[Module 1's core concepts](sense-process-act.md#how-it-works) —
specifically the sense–process–act loop and the idea of separate data and
power paths. No prior electronics or CAD experience is assumed.

## System diagram vs. electrical schematic

Module 1's diagram answered *"what talks to what, at the block level"*. A
schematic answers a more specific question: *"what is actually wired to
what pin, and at what voltage"*. A block diagram might show one box labelled
"motor controller"; the schematic shows its power input pin, its signal
pins, and the exact wire or connector between it and everything else. You
need the block diagram to think about the system; you need the schematic to
actually build or debug it.

## Installing KiCad

KiCad packages Ubuntu 22.04 directly:

```bash
sudo apt install kicad
```

**Verification**: `kicad --version` prints a version string (KiCad 7 or
newer is fine for everything on this page).

## Guided example: a new project

1. Open KiCad, then **File → New Project…**, choose a folder and a name
   (e.g. `robot_lowvoltage_example`).
2. KiCad creates a `.kicad_pro` project file alongside a `.kicad_sch`
   schematic file and a `.kicad_pcb` board file — you only need the
   schematic for this page.
3. Double-click the schematic file in the project window to open the
   **Schematic Editor**.

**Expected result**: an empty schematic sheet with a KiCad title block in
the bottom-right corner.

## Core concepts, in the editor

### Placing symbols

Press <kbd>A</kbd> (or the **Add Symbol** toolbar button) to open the symbol
chooser, type part of a name to filter (e.g. `R` for a resistor, `LED` for
an LED), select a match, then click on the sheet to place it. Generic
passives (resistors, capacitors, diodes) live in the `Device` library;
connectors, regulators and specific parts have their own libraries.

### Values and reference designators

Every symbol has a **reference designator** (`R1`, `U1`, `J1`, assigned
automatically as you place symbols, or set manually) and a **value** (the
part number or rating: `10k`, `100nF`, `L298N`). Select a symbol and press
<kbd>E</kbd> to edit both. A schematic where every resistor is just "R?"
with no value is not yet finished.

### Wires, junctions, and unused pins

Press <kbd>W</kbd> to draw a wire between two pins; KiCad auto-completes a
right-angle route as you click. Two wires that cross **without** a junction
dot are not electrically connected — only a explicit junction (a filled
circle, added automatically where a wire ends on another wire, or manually
with the junction tool) makes a connection. This is one of the most common
schematic-reading mistakes: a crossing is not automatically a connection.

Mark any pin you deliberately leave unconnected with a **no-connect flag**
(<kbd>Q</kbd>) rather than leaving it floating — ERC treats an unflagged
open pin as a probable mistake, which is exactly the check you want.

### GND, power symbols and net labels

Press <kbd>P</kbd> for the power symbol library: `GND`, `VCC`, `+5V`,
`+12V`, and so on. Two power symbols with the same name are connected to
each other everywhere they appear on the sheet, even with no visible wire
between them — this is deliberate, and is how large schematics stay
readable instead of becoming a single tangled wire.

**Net labels** (<kbd>L</kbd>) work the same way for signal nets: place a
label reading `CMD_VEL_PWM` on two different wires, anywhere on the sheet
or across sheets, and KiCad treats them as one electrical net. Use them
generously on anything that crosses the sheet, instead of routing one long
wire across the whole page.

### Separating data and power paths visually

Nothing in KiCad forces this, but it is the single habit worth carrying
over from [module 1](sense-process-act.md#how-it-works): keep power
nets (battery, regulators, motor supply) visually grouped on one part of
the sheet, and signal/data nets (UART, I²C, GPIO) on another. A reader
should be able to tell power from data at a glance, the same way the
practical task in module 1 asked for two visually distinct arrow styles.

### Connectors and interfaces

Use the `Connector` library for headers and terminal blocks (`Conn_01x02`,
`Conn_01x04`, and so on) rather than drawing bare wire ends — a connector
symbol documents how the real cable actually terminates, which a floating
wire does not.

### Fuses and a safe-stop path

Represent a fuse with the `Device:Fuse` symbol in series with the supply
rail it protects, sized to the actual current draw of what is downstream —
see [sensor and actuator
selection](continue-learning.md) for how to get that
number. Represent the emergency-stop path as what it actually is on a real
robot: a switch (`Device:SW_SPDT` or similar) placed **in the motor power
path itself**, not as a signal into a microcontroller — matching
[module 1's point](sense-process-act.md#how-it-works) that the E-stop
cuts power independently of software.

### Annotation

**Tools → Annotate Schematic…** assigns final reference designators
(`R1`, `R2`, …) consistently once your layout is settled — run it before
generating a bill of materials, not while you are still adding symbols.

## Electrical Rules Check (ERC)

Run **Inspect → Electrical Rules Checker…**, then **Run ERC**. It reports
things like an input power pin with no driving output, or a pin left
completely unconnected. Two things matter here:

1. **Read every message before dismissing it.** "Input Power pin not driven
   by any Output Power pins" on your `GND` net usually means you need a
   `PWR_FLAG` symbol somewhere on that net, telling ERC the net is
   deliberately supplied from outside the sheet — not a real fault.
2. **Do not ignore ERC by habit.** A schematic with a wall of unread ERC
   warnings is not meaningfully safer than one with no ERC at all. Fix or
   consciously suppress each one, and know which you did.

## Practical task

### Goal

Draw a schematic for a generic mobile robot's low-voltage system, run ERC
clean (or with only explicitly understood, suppressed warnings), and export
it.

:::{note}
This is a **teaching exercise with example values**, not a real Robotino or
Spot circuit — this course does not publish those teams' actual internal
schematics. Invent plausible values for anything not given, and mark them
clearly as example values in your own documentation.
:::

### Starting point

A blank KiCad project.

### Steps

1. Place and wire, at minimum: a battery, a fuse in series with it, an
   E-stop switch in the motor power path, a DC-DC converter symbol, an
   onboard-computer block (a generic IC or a labelled rectangle is fine),
   a microcontroller block, a motor controller, two motor connectors, one
   sensor connector, and a communication connector (UART or USB) between
   the microcontroller and the onboard computer.
2. Give every part a reference designator and a value.
3. Add `GND` and supply-voltage power symbols throughout, rather than
   wiring one long ground return line.
4. Add net labels on the data lines (motor commands, sensor signal).
5. Flag every intentionally unused pin with a no-connect flag.
6. Run ERC. Resolve every warning, or note explicitly why it is safe to
   leave.
7. Export the sheet: **File → Plot…**, format PDF or SVG.

## Expected result

A one-sheet schematic where power and data paths are visually distinguishable, every part is named and valued, the E-stop sits in the motor power path rather than as a signal, and ERC has been run with a documented outcome.

## Verification

Hand the exported PDF/SVG to someone who has not seen it: can they point to
where the E-stop cuts power, and which connector is a sensor versus a
motor, without you explaining it? If not, add labels and revise — the same
"someone else must be able to read it" standard as module 1's diagram.

```{list-table}
:header-rows: 1
:widths: 50 50

* - Check
  - Pass condition
* - Supply voltages
  - Every power symbol is named with an actual voltage, not left as a
    generic `VCC`
* - Open connections
  - ERC reports zero unflagged floating pins
* - Data vs. power
  - A reader can tell them apart without you explaining it
* - ERC run
  - The check was actually run, and its output (clean, or explained) is
    recorded somewhere
* - No sensitive data
  - No internal credentials, host names or real team hardware details
    appear anywhere on the sheet
```

## Common problems

- **Wires that look connected but are not.** A crossing without a junction
  dot is two separate nets. Zoom in if unsure.
- **Two different net labels meant to be the same net** (`CMDVEL` vs.
  `CMD_VEL`) — KiCad treats them as unrelated; a typo silently breaks the
  connection with no error.
- **Ignoring "input power pin not driven" instead of adding a
  `PWR_FLAG`.** This is almost always the fix, not a sign of a real fault.
- **One giant wire across the whole sheet** instead of a net label — it
  works electrically, but nobody can read it later.

## Optional extensions

{{ optional }}

Generate a bill of materials (**Tools → Generate Bill of Materials…**) from
your annotated schematic, and check that every line item has a sensible
value — an automatically generated BOM with three unlabelled "R?" entries
means the schematic was not fully annotated.

## Continue learning

Each of these is a real next step, not just a keyword — pick one when this
page's practical task feels comfortable.

:::{dropdown} Hierarchical schematics — Next step
:icon: light-bulb

**What it is.** Splitting one large schematic into multiple sub-sheets
(power, motor drive, sensors) connected through hierarchical labels, the
same way a large ROS 2 system is split into launch files per subsystem
([module 8](../08-integration.md#advanced-topics)).

**Why it matters.** A one-sheet schematic for a real robot with a dozen
sensors becomes unreadable fast; hierarchy is what keeps a big design
navigable.

**Needs.** This page's practical task completed.

**Try it.** Take your practical-task schematic and split it into two
sheets — "Power" and "Control" — connected by hierarchical pins.

**Check.** ERC still passes across both sheets, and each sheet is readable
on its own without the other open.

**Read more.** [KiCad: hierarchical
design](https://docs.kicad.org/9.0/en/eeschema/eeschema.html#hierarchical-design)
:::

:::{dropdown} Custom symbol libraries — Next step
:icon: light-bulb

**What it is.** Creating your own KiCad symbol for a part not in the
standard libraries — a specific motor controller board, for instance.

**Why it matters.** Real robot BOMs always include at least one part with
no ready-made symbol; knowing how to make a correct one (right pin count,
right pin names) avoids a wrong schematic that "looks fine".

**Needs.** Comfort placing and wiring standard symbols.

**Try it.** Create a new symbol library, then draw a symbol for a 4-pin
connector board (2 power, 2 data) with correctly named and numbered pins.

**Check.** The symbol placed on a fresh sheet has exactly 4 pins, in the
right positions, each electrically connectable.

**Read more.** [KiCad: Symbol
Editor](https://docs.kicad.org/9.0/en/eeschema/eeschema.html#symbol-editor)
:::

:::{dropdown} Footprint assignment and PCB layout — Intermediate
:icon: light-bulb

**What it is.** Assigning a physical **footprint** (the copper pad pattern)
to each symbol, then moving from the schematic into KiCad's PCB Editor to
actually place and route parts on a board.

**Why it matters.** The schematic says what connects to what; the PCB
layout is what turns that into something you can manufacture.

**Needs.** A completed, ERC-clean schematic.

**Try it.** Run **Tools → Assign Footprints…** on your practical-task
schematic, then open the PCB Editor and place the resulting footprints
anywhere on the board outline — no routing required yet.

**Check.** Every footprint listed shows up as a placeable part in the PCB
Editor with no "unassigned" warnings.

**Read more.** [KiCad: Getting started, PCB
layout](https://docs.kicad.org/9.0/en/getting_started_in_kicad/getting_started_in_kicad.html)
:::

:::{dropdown} Design Rules Check, trace width and current — Intermediate
:icon: light-bulb

**What it is.** The PCB Editor's Design Rules Check (DRC) validates
clearance and connectivity on a routed board; **trace width** must be sized
for the current it carries, the same current-budget thinking as a fuse.

**Why it matters.** A board that passes ERC (electrical connectivity) can
still be physically wrong — a trace too thin for a motor's peak current
will overheat.

**Needs.** A routed (even partially) PCB from the footprint-assignment
step above.

**Try it.** Look up a trace-width-vs-current calculator (e.g. the IPC-2221
standard) and check whether a 0.25 mm trace is adequate for a 2 A motor
supply line.

**Check.** You can state, with the calculator's numbers, whether that trace
width is adequate or undersized.

**Read more.** [KiCad: Design Rules
Check](https://docs.kicad.org/9.0/en/pcbnew/pcbnew.html#design-rules-check)
:::

:::{dropdown} Grounding, EMV basics and manufacturing data — Advanced
:icon: light-bulb

**What it is.** Ground-plane design and basic electromagnetic-compatibility
(EMV/EMC) practice for a routed board, and generating the actual
manufacturing files (Gerbers, drill files) a PCB fabricator needs.

**Why it matters.** A robot with badly routed grounds and hand-wavy EMC
practice on real hardware is a common source of exactly the kind of
"looks like a software bug but is not" symptom [module
1](sense-process-act.md#how-it-works) warns about — a noisy ground
plane can corrupt sensor readings in ways no amount of ROS 2 debugging will
find.

**Needs.** A DRC-clean routed board.

**Try it.** Add a ground-fill copper zone to your practical-task board and
re-run DRC.

**Check.** DRC reports no new clearance violations after the fill.

**Read more.** [KiCad: Plot (Gerber/manufacturing
output)](https://docs.kicad.org/9.0/en/pcbnew/pcbnew.html#generate-gerber-files)
:::

:::{dropdown} BOM and version control for KiCad projects — Advanced
:icon: light-bulb

**What it is.** Managing a schematic's bill of materials and version
history properly — KiCad's project files are plain text, which makes them
git-friendly, unlike most proprietary CAD formats.

**Why it matters.** A schematic that only exists as a single person's local
file is exactly the single point of failure
[module 8](../08-integration.md#core-concepts) warns against for software;
the same discipline (version control, reproducible state) applies to
hardware design files.

**Needs.** [The Git prerequisite](../../prerequisites/git.md) and a
completed schematic.

**Try it.** Initialise a git repository in your KiCad project folder,
commit the `.kicad_pro`, `.kicad_sch` and `.kicad_pcb` files, make one
change, and commit again.

**Check.** `git diff` between the two commits shows a readable, meaningful
change rather than an opaque binary diff.

**Read more.** [KiCad and version
control](https://docs.kicad.org/9.0/en/getting_started_in_kicad/getting_started_in_kicad.html)
:::

## Interesting videos

{{ optional }}

::::{grid} 1 1 1 1
:gutter: 2

:::{grid-item-card} KiCad for Beginners — Step by Step Tutorial to get started (2025)
:link: https://www.youtube.com/watch?v=d9_-lQq8ShE

**DIY Hideout · English · ~24 min**

Covers: a from-scratch walkthrough of creating a KiCad project, placing
symbols, wiring, and the schematic-editor basics this page's guided
example also covers.

*Why watch it*: a second, video walkthrough of the same beginner ground
— useful if a particular step (placing a symbol, drawing a wire,
annotating) went by too fast in text form above.

*Compatibility*: conceptual — KiCad's schematic editor UI is broadly
stable across recent major versions, but menu locations can shift between
releases; if a menu path does not match what you see, check the
[current KiCad documentation](https://docs.kicad.org/) for your installed
version.
:::

::::

:::{note}
This is deliberately one carefully checked video rather than a longer,
unverified list. If this link is ever dead or the content has moved, that
is a documentation bug worth reporting — see the [repository
README](https://github.com/MoritzSchallenberg/Learning-Robotics-Crash-Course).
:::

## Connection to the next module

This schematic is the electrical ground truth behind the block diagram from
[module 1](../01-system-hardware.md). The mechanical side of the same robot
— how the parts you just wired are actually mounted — is the subject of
[the Fusion tutorial](fusion-mechanical-design.md).

## Further reading

- [KiCad documentation](https://docs.kicad.org/) — retrieved 2026-09-02
- [KiCad: Getting started in
  KiCad](https://docs.kicad.org/9.0/en/getting_started_in_kicad/getting_started_in_kicad.html)
- [KiCad: Schematic Editor
  reference](https://docs.kicad.org/9.0/en/eeschema/eeschema.html)
