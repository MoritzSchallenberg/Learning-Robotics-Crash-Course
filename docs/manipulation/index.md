# Robot Manipulation

## What belongs to this topic

Everything about moving a physical arm on purpose: the arm's own
kinematics, planning a collision-free motion, the gripper and the
controller chain that actually moves the joints, and using perception to
find something worth grasping. This page is currently a **summary and
orientation page**, not a full tutorial series — the practical,
step-by-step tutorials this topic needs (arm fundamentals, a full MoveIt 2
path, planning scenes, grippers and controllers, perception-to-grasp,
pick-and-place) are planned future work, listed under [Planned
content](#planned-content) below rather than written yet.

## What it does in the overall system

A mission decides *that* something should be picked up
([Autonomous Decision-Making](../decision-making/index.md) — the `GRASP`/
`RELEASE` states in a state machine, or a Golog++/RAFCON action); this
topic is *how* that actually happens — turning a target pose into a
collision-free arm trajectory and a gripper command.

## Where ALeRT uses this

{{ alert }} {{ documented }} ALeRT's manipulator is a **Kinova Gen3
7-DOF arm** fitted with a **Robotiq 2F-85 two-finger adaptive gripper**
and an **Intel RealSense** vision module — confirmed from
[`ros2_kortex`](https://github.com/RRL-ALeRT/ros2_kortex)'s own README,
not assumed from the repository name. In the Webots simulation, MoveIt 2
control is already documented and working today — see the [platform
page's Manipulation with MoveIt
section](../platforms/spot/index.md#manipulation-with-moveit):

```bash
ros2 launch webots_spot moveit_launch.py
```

This brings up RViz with the arm controllable via an interactive marker —
drag it to a target pose, **Plan**, inspect the trajectory, then
**Execute**. The simulation also publishes TF frames for objects in the
scene, so a grasp target's pose can come from a
[TF listener](../sensors-frames/index.md) rather than from image-based
pose estimation, which is what makes a first manipulation exercise
tractable before adding perception.

## Available tutorials

None yet on this site specifically for manipulation. Related, already
existing tutorials this topic will build on once written:

- [Sensors and Coordinate Frames](../sensors-frames/index.md) — TF2, the
  listener pattern a grasp pose needs.
- [Perception](../perception/index.md) — detecting an object in the first
  place (ArUco, YOLO).
- [Autonomous Decision-Making](../decision-making/index.md) — the state
  machine or behavior tree pattern a pick-and-place sequence fits into
  (`GRASP`/`RELEASE` as states with their own failure exits).
- [Platform page: Manipulation with
  MoveIt](../platforms/spot/index.md#manipulation-with-moveit) — the one
  concrete, working procedure that exists today (simulation only).

## Content already present

- The platform page's `moveit_launch.py` procedure above (Simulation
  verified).
- The general principle that a pick-and-place sequence is a state machine
  with `GRASP`/`RELEASE` states, each with its own failure exit (a `None`
  inverse-kinematics result is "unreachable," not a crash) — see
  [Autonomous Decision-Making](../decision-making/index.md).

## Planned content

Listed here as topics this category will grow into, not as pages that
exist yet. See `maintainers/` for the corresponding work packages.

- **Robot arm fundamentals** — links, joints, degrees of freedom, revolute
  vs. prismatic joints, joint space vs. Cartesian space, end effector,
  Tool Centre Point, forward/inverse kinematics, joint limits, workspace,
  singularities, self-collision, with an RViz exercise comparing reachable
  and unreachable target poses.
- **A full MoveIt 2 path** — URDF, SRDF, planning groups, end effectors,
  `move_group`, kinematics plugins, planning pipelines, controller
  integration, manual planning in RViz, joint goals, pose goals, plan
  vs. execute, Cartesian paths, velocity/acceleration scaling, and
  `MoveGroupInterface` — preferring, for ROS 2 Humble, the officially
  documented and tested C++ interface, not a Python interface promised
  without confirming it is actually available and tested in this
  project's Humble setup.
- **Planning scene and collision checking** — a step-by-step tutorial:
  plan without an obstacle, add a table as a collision object, re-plan,
  add and attach a workpiece, move with the attached object, detach and
  remove the collision object — covering the planning scene, world vs.
  attached collision objects, the allowed collision matrix, self-collision,
  and why a collision object's pose and frame must stay current.
- **Gripper and controller chain** — the full path from a MoveIt
  trajectory through `FollowJointTrajectory`, a
  `joint_trajectory_controller`, and the `ros2_control` hardware
  interface to the physical joints; `joint_states`, the controller
  manager, gripper open/close/homing, end-stop and blocked-gripper
  detection, feedback, timeout and cancellation — using only interfaces
  actually verified for ALeRT's real manipulator, not invented topic or
  service names.
- **Perception-to-grasp** — camera image → object detection → object pose
  in the camera frame → TF transform → grasp offset → pre-grasp pose →
  MoveIt goal; starting from the simulation's existing object TF (see
  above) before adding image-based pose estimation.
- **Pick-and-place project** — a full simulation project chaining
  detection/TF, planning-scene update, pre-grasp, grasp, attach, lift,
  place, detach and return-to-safe-pose, each phase with its own success
  criterion, timeout, failure exit and recovery; MoveIt Task Constructor
  as an advanced variant.
- **ALeRT's own staged manipulation path** — Stage A (simulation and
  observation: inspect planning groups and joint states, plan only),
  Stage B (simulated execution: joint/pose goals, collision objects,
  gripper control, attach/detach), Stage C (autonomous grasp: object
  pose → TF → pre-grasp → grasp → lift → place), Stage D (physical
  hardware, supervised only: reduced speed, a clear workspace, an
  accessible E-stop, one motion at a time, simulated and trajectory-
  checked first, never an unsupervised automatic pick-and-place).

## Related ALeRT repositories

From [ALeRT on GitHub](https://github.com/RRL-ALeRT), checked directly
(not assumed from repository names alone):

```{list-table}
:header-rows: 1
:widths: 26 50 24

* - Repository
  - What it is
  - Status
* - [`ros2_kortex`](https://github.com/RRL-ALeRT/ros2_kortex)
  - The Kinova Gen3 driver; confirms the real arm/gripper/camera combination
  - Repository documented
* - [`kinova_stuffs`](https://github.com/RRL-ALeRT/kinova_stuffs)
  - Kortex API wheel + launch wrapper; the team's own README says they are
    migrating to `ros2_kortex`, but this "works perfectly fine with ROS2
    Humble" today
  - Repository documented
* - [`kinova-ros2`](https://github.com/RRL-ALeRT/kinova-ros2)
  - Older Jaco2/Mico packages, real Humble build/launch/MoveIt commands,
    no activity since 2023
  - Repository documented, likely superseded
* - [`spot_gen3_moveit`](https://github.com/RRL-ALeRT/spot_gen3_moveit)
  - MoveIt 2 configuration for Spot + Gen3, by its name — no README to
    confirm details
  - Repository exists
* - [`alert_auto_dexterity`](https://github.com/RRL-ALeRT/alert_auto_dexterity)
  - Likely an autonomous-dexterity mission package, by its name — no
    README to confirm details
  - Repository exists
```

## Verification status

{{ simulation }} MoveIt 2 control of the arm in Webots is confirmed
working (the platform page's own procedure). {{ hardwareverified }} is
not claimed for anything on this page — every real-hardware manipulation
claim needs {{ documented }} at minimum (a repository actually confirms
it) or is marked "Hardware verification required".

## Common limitations

- **Two repositories name the real Gen3/gripper hardware, but most of
  the manipulation-specific repositories above (`spot_gen3_moveit`,
  `alert_auto_dexterity`) have no README** — their exact scope is not
  independently confirmed by this site.
- **This page does not yet contain a runnable tutorial.** Until the
  planned content above is written, the platform page's `moveit_launch.py`
  procedure is the only hands-on manipulation exercise this site
  documents.

## Continue learning

Once the planned tutorials above exist, this section will list Next
steps / Intermediate projects / Advanced topics for manipulation
specifically. For now, see
[Autonomous Decision-Making: Continue learning](../decision-making/continue-learning.md)
for the mission-logic side of a pick-and-place sequence.

## Interesting videos

Not yet populated. No manipulation-specific video has been independently
verified for this site yet — quality over quantity, consistent with
every other topic's video page: no video is added until its title,
channel and duration are confirmed via YouTube's own oEmbed endpoint.
