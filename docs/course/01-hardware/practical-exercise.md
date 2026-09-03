# Practical hardware exercise

{{ common }} {{ core }}

## Goal

Produce one system diagram — on paper or in any drawing tool — that
traces a sensor reading from the sensor to the onboard computer, and a
command from the computer back out to an actuator, with power and safety
shown separately.

## Starting point

A real robot if you have access to one; otherwise
[the sense–process–act diagram](sense-process-act.md) plus the relevant
[platform hardware page](../../platforms/index.md) as your component
description.

## Steps

1. List every component you can find (aim for at least eight).
2. Sort each into **sense**, **process**, or **act**.
3. Draw them as boxes.
4. Draw **data** arrows (solid, blue) between boxes that exchange
   information.
5. Draw **power** arrows (dashed, amber) from the battery to every box that
   needs it.
6. Mark the **E-stop** and what it cuts (red).
7. Pick three components; for each, write one sentence: *if this fails
   silently, what would the robot appear to be doing wrong?*

## Expected result

A diagram with three visually distinct arrow types that someone who has
never seen the robot could follow, plus three short failure sentences
from step 7.

## Verification

Look at your diagram fresh, or hand it to someone else without explaining
it first: can they name, just from the diagram, which arrow is data and
which is power, and what the E-stop cuts? If not, add a legend and
revise — that is the actual skill this task teaches. For each of the
three failure sentences from step 7, check that the sentence describes an
*observable symptom* ("the robot stops responding to commands"), not just
a repeat of the component name.

## Common problems

- **Data and power drawn as the same arrow style** — the two most common
  debugging questions ("is data flowing?" vs "is it powered?") become
  impossible to separate. Use two visibly different line styles.
- **Forgetting the network** — a laptop running RViz over Wi-Fi is part of
  the data path, not an outside observer.

## Optional extensions

{{ optional }}

Pick one failure sentence from your practical task's step 7 and write the
exact terminal command or observation that would confirm it — you will not
be able to run it until [module 2](../02-ros2.md), but reasoning about it
correctly here is a good sign for [module 8](../08-integration.md).

No robot available at all? Build the diagram from the
[Webots](../../platforms/simulation.md) robot model description instead of a
physical robot — the loop and the component categories are identical; only
"battery" becomes "simulated power", which is worth noting as a limitation
of simulation in its own right.

## Try it on Spot

{{ alert }} {{ spotreadonly }}

Apply this exercise to a real quadruped instead of a diagram — either the
physical Spot, or the [platform page's](../../platforms/alert-spot.md)
description of it if you have no access.

- Point to Spot's sensors and name each: the gripper camera
  (`/SpotArm/gripper_camera/image_color`), the 3D LiDAR (published as
  `/Spot/Velodyne_Puck/point_cloud`), and the leg/joint encoders that feed
  odometry (`/Spot/odometry`).
- Point to the onboard compute and the network link it uses to reach your
  workstation — the same "wireless is the weakest link" point
  [Sense–process–act](sense-process-act.md) made generally.
- Point to the joint actuators (the leg motors) as this module's
  "actuator" stage, and Spot's arm as a second, separate actuator group.
- Find the physical E-stop. **Do not press it** unless something is
  genuinely about to be hurt — see the [platform
  page's](../../platforms/alert-spot.md#operating-the-physical-robot) full
  danger notice. Confirm you can locate it before doing anything else on
  real hardware.
- Compare Robotino and Spot on the same four points (sense/process/act/
  safety) using [the comparison
  table](sense-process-act.md#two-robots-one-architecture) — what
  changed, and what stayed the same?

:::{important}
**Read-only on physical Spot**: sensor and safety-chain identification
only. Do not open any covers or panels, and do not operate any actuator —
this is an inspection exercise, not an operating one. See
[module 7](../07-autonomous-decisions.md#try-it-on-spot) and the
[platform page](../../platforms/alert-spot.md) for what actually moving
Spot requires.
:::

## Next subtopic

[Interesting videos](videos.md), then
[Continue learning](continue-learning.md).
