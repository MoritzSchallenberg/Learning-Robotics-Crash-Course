# Autodesk Fusion: mechanical robot parts

{{ optional }}

The [KiCad tutorial](kicad-schematic.md) designed the electrical side of a
robot subsystem. This page designs the **mechanical** side — a single
bracket, in [Autodesk Fusion](https://www.autodesk.com/products/fusion-360/)
— parametric CAD, so that a change like "the mounting holes need to move"
is a number you edit, not a part you rebuild from scratch.

:::{important}
**Fusion has no native Linux client.** Its officially supported desktop
platforms are Windows and macOS (checked against Autodesk's own system
requirements page, 2026-09-02); there is also a browser-based version with
more limited functionality, and running the Windows desktop app inside a
Windows virtual machine or on a dual-boot machine is the common workaround
on an otherwise Ubuntu setup. This course runs on Ubuntu
([Supported environment](../../reference/compatibility.md)), so plan for one
of those options rather than expecting `apt install` to work here — check
Autodesk's current system requirements before you install anything, since
supported platforms do change between releases.
:::

## Learning objectives

By the end of this page you can:

1. build a fully-constrained, parametric 2D sketch;
2. turn a sketch into a 3D part with extrude, cut and fillet;
3. change a part's dimensions after the fact by editing a parameter, not
   the geometry;
4. export a part for both manufacturing reference and 3D printing.

## Prerequisites

None specific to Fusion. Comfort with the general idea of components from
[module 1](../01-system-hardware.md) helps but is not required.

## Core concepts

### Sketches, constraints and "fully defined"

Every 3D part starts as a 2D **sketch** on a plane. A line you just draw is
*under-constrained* — Fusion shows it in a different color (typically blue,
until fully defined, then black) because it does not yet know exactly where
that line has to be. **Constraints** (horizontal, vertical, equal, tangent,
concentric) and **dimensions** (an exact length or angle) pin it down. A
sketch is **fully defined** when nothing in it can move without violating a
constraint or dimension — Fusion tells you explicitly when you reach this
state.

:::{tip}
An under-constrained sketch is not just untidy — it means a later edit can
silently distort the part in a way you did not intend. Fully define every
sketch before extruding it.
:::

### Parameters

**Modify → Change Parameters** (or the parameters dialog) lets you name a
dimension instead of leaving it as an anonymous number — `plate_thickness`
instead of `d3`. Reference a parameter's name in another dimension's
expression field (e.g. `plate_thickness / 2`) and the two stay linked
automatically. This is the mechanical equivalent of using `$ROS_DISTRO`
instead of hard-coding a distribution name
([installation guide](../../prerequisites/installation.md)) — one named
value, referenced everywhere it matters, instead of copies that can drift
out of sync.

### From sketch to solid

**Extrude** pulls a closed sketch profile into a 3D solid along a distance.
**Cut** is the same operation in the subtractive direction — remove
material rather than add it (used for a mounting hole, for instance).
**Hole** is a dedicated tool for exactly that case, and — unlike a plain
cut — it can also add a counterbore, countersink or thread callout in one
step. **Fillet** and **chamfer** round or bevel an edge after the solid
exists; both take an edge selection and a radius or distance.

### Components and assemblies, briefly

A single part is a **body**; a **component** is what Fusion actually
positions, constrains and reuses. This page stays inside one component, but
know that a real robot design is many components joined together — the
mechanical equivalent of module 1's "the robot is many parts, not one" —
covered further in Continue learning below.

## Guided example: a fully-defined rectangle

Before the practical task, practice reaching "fully defined" on the
simplest possible sketch:

1. **File → New Design**, then start a sketch on the XY plane.
2. Draw a rough rectangle with the line tool — it is under-constrained
   (colored) at this point.
3. Add a horizontal and a vertical dimension for two adjacent sides.
4. Notice: the sketch is now fully defined (Fusion's status area confirms
   this, and the geometry usually turns black) with just those two
   dimensions, because the rectangle constraint tool already fixed the
   angles.
5. Change one dimension's value and confirm the whole rectangle updates —
   this is the parametric behaviour the practical task below depends on.

## Practical task

### Goal

Design a simple parametric sensor mount: a flat plate with two mounting
holes and a cutout for a generic sensor, where the hole spacing can be
changed after the fact without rebuilding the part.

:::{note}
Use clearly invented example dimensions, or pick your own — this exercise
does not reproduce a real Robotino or Spot mounting bracket.
:::

### Starting point

A new, empty Fusion design.

### Steps

1. Sketch a rectangular plate on the XY plane; fully define it with
   dimensions (length, width) tied to named parameters
   (`plate_length`, `plate_width`).
2. Extrude it to a `plate_thickness` parameter you also name explicitly.
3. Sketch two circles for mounting holes, dimensioned from a shared
   `hole_spacing` parameter rather than fixed coordinates.
4. Use the **Hole** tool (or cut) to cut both mounting holes through the
   plate.
5. Sketch and cut a rectangular or circular cutout sized for a generic
   sensor, as its own named parameters.
6. Add a fillet to the plate's outer corners.
7. Open **Modify → Change Parameters** and change `hole_spacing` — confirm
   both holes move together, symmetrically, with no other edit.
8. Export a STEP file (**File → Export**, format STEP) and a file for
   printing (STL or 3MF).
9. Create a basic drawing (**File → New Drawing → From Design**) with one
   view of the finished plate.

## Expected result

A single solid body: a plate with two holes and a sensor cutout, where
changing `hole_spacing` moves both holes together without touching any
other geometry, plus a STEP file, a print-ready file, and one drawing view.

## Verification

```{list-table}
:header-rows: 1
:widths: 50 50

* - Check
  - Pass condition
* - Sketch state
  - The main sketch shows as fully defined, not under-constrained
* - Parametric behaviour
  - Changing `hole_spacing` in the parameters dialog moves both holes with
    no manual re-edit
* - Named parameters
  - At least three parameters have real names, not the default `d1`, `d2`
* - No stray geometry
  - The design has exactly one body — no leftover, unused sketch profiles
    turned into extra solids
* - Exports exist
  - A `.step` file and a `.stl` or `.3mf` file were both actually produced
* - Drawing
  - At least one 2D view was generated from the 3D model
```

## Common problems

- **A dimension applied to the wrong entity** locks a sketch in an
  unintended shape — delete the dimension and re-add it to the correct
  line or point rather than fighting the solver.
- **"Fully defined" claimed but the part still distorts on edit.** Usually
  one redundant, contradictory constraint was added and silently
  overridden an earlier one — check the sketch's constraint list.
- **Two mounting holes defined by absolute coordinates instead of from
  each other.** This defeats the point of parametric spacing; dimension
  hole 2 relative to hole 1 (or both from a shared centerline), not both
  from the sketch origin independently.
- **Fillets applied before the part is otherwise finished.** A fillet can
  make later edits fail in confusing ways; add cosmetic fillets and
  chamfers last.

## Optional extensions

{{ optional }}

Add a third, independent mounting variant (a different hole pattern) as a
**second configuration** of named parameters you can switch between, rather
than a second file — this previews the parametric-variants topic in
Continue learning below.

## Continue learning

:::{dropdown} Assemblies and joints — Next step
:icon: light-bulb

**What it is.** Combining multiple components into an **assembly**, and
connecting them with **joints** (revolute, slider, rigid) that define how
they can move relative to each other — the mechanical equivalent of a TF2
transform chain ([module 3](../03-sensors-tf.md#core-concepts)).

**Why it matters.** A robot is never one part; understanding how Fusion
models multi-part motion is what lets you design something that actually
has to move, like a gripper or a leg joint.

**Needs.** This page's practical task completed.

**Try it.** Create a second, simple component (a small block) and join it
to your practical-task plate with a revolute joint, then drag it through
its range of motion.

**Check.** The joint's angle limits actually stop the motion where you set
them, not just at an arbitrary point.

**Read more.** [Fusion: Joints in an
assembly](https://help.autodesk.com/view/fusion360/ENU/)
:::

:::{dropdown} Motion and interference checking — Intermediate
:icon: light-bulb

**What it is.** Fusion's motion study tools can drive an assembly's joints
through a range and flag **interference** — two bodies occupying the same
space — automatically, rather than you eyeballing it.

**Why it matters.** This is the mechanical-design equivalent of the
collision checking [module 7](../07-autonomous-decisions.md#advanced-topics)
covers for a manipulator's planning scene — catching a physical collision
before it happens on the real robot.

**Needs.** An assembly with at least one joint (the previous topic).

**Try it.** Run **Inspect → Interference Check** on your two-part joined
assembly across its full range of motion.

**Check.** You can state, from the tool's report, whether any interference
exists at any point in the joint's travel.

**Read more.** [Fusion: Interference and motion
tools](https://help.autodesk.com/view/fusion360/ENU/)
:::

:::{dropdown} Sheet metal — Intermediate
:icon: light-bulb

**What it is.** A dedicated workflow for parts made from a single bent
sheet (brackets, chassis panels) — Fusion tracks the flat pattern
automatically as you design the folded shape.

**Why it matters.** Many real robot chassis parts are sheet metal, not
solid-machined blocks; the design rules (minimum bend radius, relief cuts)
are specific to this workflow and do not appear in ordinary solid modeling.

**Needs.** Comfort with the core sketch/extrude workflow from this page.

**Try it.** Convert your practical-task plate into a sheet-metal part with
one 90° bend along one edge, then inspect the automatically generated flat
pattern.

**Check.** The flat pattern's overall length correctly accounts for the
bend allowance, not simply the two flat segments added together.

**Read more.** [Fusion: Sheet Metal
workspace](https://help.autodesk.com/view/fusion360/ENU/)
:::

:::{dropdown} Design for additive manufacturing — Intermediate
:icon: light-bulb

**What it is.** Design choices specific to 3D printing: minimum wall
thickness, overhang angles that need support material, and orientation on
the print bed — different constraints than machining or sheet metal.

**Why it matters.** A part that is trivially printable in one orientation
can need extensive support material — or fail outright — in another; this
is why a print-ready export alone (this page's practical task) is not the
same as a print-*optimised* design.

**Needs.** A completed solid part (this page's practical task).

**Try it.** Check your practical-task plate's thinnest wall against your
printer's (or a generic FDM printer's) minimum wall-thickness guideline,
and identify whether any feature would need support material in its
current orientation.

**Check.** You can state the plate's minimum wall thickness and whether it
clears a typical 0.8 mm FDM guideline.

**Read more.** [Fusion: 3D print
preparation](https://help.autodesk.com/view/fusion360/ENU/)
:::

:::{dropdown} Tolerances, fits and load simulation — Advanced
:icon: light-bulb

**What it is.** Specifying a dimensional **tolerance** (how much a real
manufactured part is allowed to deviate) and choosing a **fit** (how two
mating parts' tolerances relate — clearance, transition, interference); at
a more advanced level, Fusion's simulation workspace can estimate stress
and deflection under a load.

**Why it matters.** A design that is dimensionally "correct" on screen can
still fail to assemble, or fail under load, if tolerances and material
behaviour were never considered — the mechanical equivalent of the
{{ unverified }} discipline this course applies to unverified technical
claims: do not assume a part will hold without checking.

**Needs.** A completed, exported part.

**Try it.** Add a tolerance callout to one dimension on your practical-task
drawing, and, if you have access to Fusion's simulation workspace, run a
basic static stress study on the plate under a plausible small load.

**Check.** You can point to the specific tolerance value you chose and
justify it, or state a maximum deflection value from the simulation.

**Read more.** [Fusion: Simulation
workspace](https://help.autodesk.com/view/fusion360/ENU/)
:::

:::{dropdown} Embedding electronic components and linking to KiCad — Advanced
:icon: light-bulb

**What it is.** Importing a STEP model of an electronic component (many
manufacturers publish one) into a mechanical assembly to check clearance
and mounting — and, in the other direction, exporting your KiCad board
outline into Fusion to confirm it actually fits the enclosure you are
designing.

**Why it matters.** This is where the [KiCad tutorial](kicad-schematic.md)
and this page meet: an electrical design and a mechanical enclosure that
were never checked against each other is a common, entirely avoidable
source of "the board does not fit the case" late in a build.

**Needs.** A STEP export from the KiCad practical task (or any STEP model
of an electronic part), and this page's practical task.

**Try it.** Import any STEP file into your Fusion design as a reference
component and check, visually, whether it clears your plate's cutout.

**Check.** You can state, from the assembly, whether the imported part
physically fits without modifying your plate.

**Read more.** [KiCad: exporting a board
outline](https://docs.kicad.org/9.0/en/pcbnew/pcbnew.html) ·
[Fusion: importing STEP
files](https://help.autodesk.com/view/fusion360/ENU/)
:::

## Connection to the next module

This page and the [KiCad tutorial](kicad-schematic.md) are the two concrete
sides of [module 1's](../01-system-hardware.md) block diagram: electrical
and mechanical detail behind the same boxes and arrows. From here, the
course returns to software — [module 2](../02-ros2.md) turns those boxes
into running ROS 2 nodes.

## Further reading

- [Autodesk Fusion system
  requirements](https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/System-requirements-for-Autodesk-Fusion-360.html) — retrieved 2026-09-02
- [Autodesk Fusion help](https://help.autodesk.com/view/fusion360/ENU/)
- [Fusion learning resources](https://www.autodesk.com/certification/learn-fusion)
