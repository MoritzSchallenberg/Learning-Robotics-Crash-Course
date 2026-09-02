# Carologistics / Robotino

{{ carologistics }}

[Carologistics](https://www.carologistics.org/) is the joint RoboCup Logistics
League team of FH Aachen and RWTH Aachen. The robots are Festo Robotinos,
adapted for an industrial logistics scenario: they drive to production
machines, dock precisely, and move workpieces through a manufacturing chain.

This page covers what is specific to that system. The fundamentals are in the
[course modules](../course/index.md).

:::{admonition} Internal information is not published here
:class: warning

Network configuration, host names, IP addresses and device credentials are
internal team information and are deliberately absent from this public site.
Ask your team lead for the network setup, and never commit those details to a
public repository.
:::

## System versions

This track follows the course's [supported
environment](../reference/compatibility.md): Ubuntu 22.04 LTS and ROS 2
Humble. Every command on this page and in the course modules assumes that
baseline.

```{list-table}
:header-rows: 1
:widths: 35 65

* - Component
  - Version
* - Developer workstation OS
  - Ubuntu 22.04 LTS (course baseline)
* - ROS 2 distribution
  - Humble Hawksbill
* - Simulator
  - Webots {{ unverified }} — check the repository README
* - Robot base
  - Festo Robotino 4
* - Deployment
  - Ansible
```

:::{note}
The team's own production repositories evolve independently of this course
and may target a different Ubuntu release or ROS 2 distribution at any given
time. Check the README of each repository you actually clone before
assuming it matches the course baseline above — this page teaches the
course's fixed environment, not necessarily the exact configuration of every
production system.
:::

## The RoboCup Logistics League

Understanding the competition explains most of the design decisions.

Two teams of robots share a factory floor populated with **Modular Production
Stations (MPS)** — machines from Festo that process workpieces. The robots must
work out where the machines are, then transport workpieces between them in the
right order to complete production orders. A **referee box (refbox)** issues
orders and scores the game over the network.

The first three minutes are the **exploration phase**: machine positions are
unknown and must be discovered and reported for points. After that, the ground
truth is published to all teams.

Two consequences run through the whole system:

**Precision matters more than speed.** Docking to a conveyor belt is a
millimetre-scale operation, which is why the robot is omnidirectional and why
so much effort goes into laser-based machine detection.

**The clock is running.** Exploration is scored on speed, which is why
markerless detection is an active research topic for the team.

## Hardware

### The robot

```{list-table}
:header-rows: 1
:widths: 30 70

* - Component
  - Notes
* - Festo Robotino 4
  - Omnidirectional base — it can translate in any direction while rotating
* - SICK TiM571
  - 2D laser scanners, used for navigation and machine detection
* - Logitech C905 webcam
  - Mounted at MPS tag height, for marker detection
* - Global-shutter Pi camera
  - Mounted at workpiece height, for object tracking and manipulation
* - Raspberry Pi 5
  - Forwards the Pi camera image; processing currently happens on the Robotino
* - Custom gripper
  - Stepper motors with encoders, driven by an Arduino, on a custom PCB
```

**Omnidirectional drive** is the defining feature. Unlike a differential-drive
robot, the Robotino can move sideways without turning first, which makes
docking to a machine far easier — it can align its orientation and its position
independently.

:::{note}
This matters for [Nav2 configuration](../course/06-navigation.md): a controller
that assumes differential drive will not use the lateral degree of freedom.
Check which controller plugin your team's configuration uses.
:::

### Off-field equipment

The team also runs a router, an access point, a refbox machine and an agent
laptop. The specifics are internal.

## Software stack

```text
   Robotino driver          base motion and odometry
   Laser driver             SICK TiM571 scanners
   laser_scan_integrator    merges two scans into one
   Laser lines              extracts line segments -> machine detection
   Tag vision               ArUco markers identify machines and sides
   Object tracking          YOLOv8-nano + triangulation for workpieces
   Nav2                     navigation
   Gripper controller       Arduino-based ROS controller
   CLIPS-Executive / agent  high-level goal reasoning
   Refbox interface         protobuf communication with the referee box
   Ansible                  deployment across the fleet
```

### Key repositories

Public repositories under the
[Carologistics organisation](https://github.com/carologistics):

`robotino_navigation`
: Nav2 configuration for Robotino, working with both the Webots simulation and
  real robots. Documents a two-SICK-TiM571 setup with 3D-printed mounts.

`rcll_simulation_webots`
: Webots simulation of the RCLL game field with Robotino robots — robot and
  machine descriptions, sensor interfaces, an omnidirectional controller, SLAM
  Toolbox integration and Nav2.

`mps-map-gen`
: Extends a map from a map server with game-specific information — machines on
  the field, and boundaries for the competition area. Publishes two maps:
  `mps_map` for localization, and `mps_map_bounded` which adds a bounding box
  so navigation keeps the robot inside the legal playing area. It can also
  publish static transforms for points of interest, such as directly in front
  of a machine's conveyor.

`laser_scan_integrator`
: Merges two laser scans into one, accounting for their relative positions via
  TF and the robot's footprint.

`ros2-markerless-mps`
: Research towards detecting machines without markers.

`expertino-rcll`
: The central goal-reasoning agent.

`ansible`
: Deployment playbooks for robots and workstations.

:::{note}
Several of these repositories have little or no README. The descriptions above
come from the team wiki and repository metadata. When in doubt, read the code
or ask — do not assume behaviour from a package name.
:::

## Setup

### Workstation setup with Ansible

The team automates workstation setup. On Fedora:

```bash
sudo dnf install ansible ansible-collection-community-general
```

Generate an SSH key and add it to your GitHub account
([see the Git page](../prerequisites/git.md)), then register GitHub's
fingerprint:

```bash
ssh-keyscan github.com >> ~/.ssh/known_hosts
```

Then pull and apply the team configuration:

```bash
ansible-pull -i localhost, -U git@github.com:carologistics/ansible.git \
  --skip-tags simulation,gazebo -K simulation-setup.yml
```

This sets up the ROS 2 workspaces, the refbox, and the shell environment.

:::{note}
You need access to the team's repositories for this to work. Ask your team
lead. `-K` prompts for the privilege-escalation password.
:::

### DDS configuration

The Carologistics lab restricts ROS 2 discovery so that machines do not
interfere with each other. See
[Networking](../prerequisites/networking.md#restricting-discovery-to-one-interface)
for the Cyclone DDS configuration.

## Working with the robots

### Starting a robot

Switch it on, wait for it to boot, then connect over SSH
([see Networking](../prerequisites/networking.md)).

The team uses `screen` sessions with pre-filled startup commands, entered with
a shell macro:

```bash
sf
```

This opens tabs with the startup commands ready to run. If the session is
already running but shows no commands, `Ctrl` + `a` followed by `Ctrl` + `e`
replaces the default tabs with fresh ones.

:::{tip}
`screen` is why the team uses it rather than plain SSH: the session survives a
dropped Wi-Fi connection, and several people can attach to the same session
without fighting over the terminal.
:::

### Localizing a robot

Connect via VNC for a graphical session, then start RViz — either from the
`Robotino<i>Rviz2` entry in the quick menu, or directly:

```bash
ros2 launch robotino_navigation robotino_rviz.launch.py namespace:=robotinobase<i>
```

Replace `<i>` with the robot number.

Then, exactly as in [module 5](../course/05-mapping-localization.md):

1. Click **2D Pose Estimate** and set the robot's actual position and heading.
2. Check that the laser data aligns with the walls on the map.
3. Send a short **Nav2 Goal** and confirm it drives sensibly before trusting it
   with anything longer.

:::{note}
Robots are namespaced per robot number, so topics are
`/robotinobase<i>/...`. Everything in the course modules applies, but the topic
names are prefixed.
:::

### Deploying software

```bash
ansible-playbook -i robotinos.inv -t fast-deploy robotino.yml -l <host> -K
```

`fast-deploy` pulls the latest code, stashes local changes and rebuilds. See
[module 8](../course/08-integration.md) for what the
options mean.

### Starting a test game

Start the robots and the refbox, then start the central agent. In
`~/fawkes-robotino/bin`:

```bash
./off_field_central_agent_start.bash 1 3
```

The numbers are the robot numbers to control. If everything works, the robots
appear in the refbox frontend.

## Perception

### Tag vision

Machines carry **ArUco markers** — the `ARUCO_ORIGINAL` dictionary — identifying
both the machine and which side you are looking at. The tag camera sits at
marker height.

The general technique is in
[module 4](../course/04-perception/fiducial-markers.md). What is specific here
is the combination: the tag identifies the machine, and the **laser lines**
give its precise position and orientation. Cross-checking the two is what makes
detection reliable enough to dock against.

### Laser lines

The laser scanners see the flat front faces of the machines as straight line
segments. Extracting those lines gives an accurate position and orientation for
a machine — far more precise than a camera at that distance.

The field is a grid, and machines sit on cells at 45° increments, which
constrains the search considerably.

### Object tracking

The Pi camera plus YOLOv8-nano detects workpieces; the position is then
triangulated using the laser lines, giving a 6D pose (with pitch and roll
assumed zero). This is exactly the detection-to-localization step described in
[module 4](../course/04-perception/index.md#detection-versus-localization) — the
laser line supplies the depth that the bounding box cannot.

### Markerless MPS detection

{{ advanced }} {{ unverified }} — a Carologistics research topic, not a
finished, ready-to-run system, and not part of any module's core task.

**Purpose, in one sentence**: during the three-minute exploration phase
([module 1](../course/01-system-hardware.md) explains why that phase
exists), machines currently must carry a visible marker to be located
quickly; markerless detection aims to find them from appearance alone,
because the league scores exploration speed and a marker-free approach
generalises to machines the team's cameras have never specifically been
tuned for.

The approach under investigation, as of when this page was written: a
camera generates per-cell probabilities for machine presence and rotation,
aggregated across robots and combined with the laser-line evidence
described above. Rotation is the hard part — candidate approaches include
learning each side of a machine separately, detecting front and back
together with the traffic-light position, or training a network that
predicts orientation directly, which needs orientation labels in the
training data (see [data labeling](../course/04-perception/data-labeling.md)
for the general labeling workflow this would build on).

This description reflects the public team wiki at the time of writing and
describes work in progress. No internal topic names, repository paths or
operational data are reproduced here — check the current state with the
team, via the public
[`ros2-markerless-mps`](https://github.com/carologistics/ros2-markerless-mps)
repository, before relying on any of it.

### Data labeling

Training data for object detection is labeled with a browser-based annotation
tool. The general workflow and the rules for good labels are in
[module 4](../course/04-perception/object-detection.md#training-a-custom-model).

Carologistics-specific classes:

**Conveyor**
: The front rectangle of the belt on a machine, bounded by the upper and lower
  rounded sections, or by the blue narrowing cone and the lower section. Label
  only the black area, without adjacent grey parts.

**Slide**
: Primarily on ring machines. The target area is bounded by the two black
  sides, the lower rectangle and the upper edge.

**Workpiece**
: Only the lower part, identifiable by its barcode and colour — red, silver,
  metallic or transparent.

:::{note}
The team's annotation workspace requires an invitation. Ask your team lead.

The reference images in the team wiki are not reproduced here: they are served
from time-limited private URLs and their licensing for public republication is
not established. See `CONTENT_REVIEW.md` in the repository.
:::

## Gripper

The gripper is a custom mechanism, built from the following pieces, in
general-principle terms — the same
[sense–process–act pattern](../course/01-system-hardware.md#core-concepts) as the
rest of the robot, at a smaller scale:

**Actuators**: NEMA 17 stepper motors (with an encoder) for the finer
axes, and a NEMA 24 stepper motor with an integrated brake for the axis that
must hold position under load without power. Igus motor controllers drive
the steppers.

**Sensors**: the motor encoders report shaft position, which is what lets
the controller know where the gripper actually is rather than only where it
was commanded to be — the same open-loop-vs-closed-loop distinction as the
drive motors in [module 1](../course/01-system-hardware.md).

**Control**: a custom PCB carries an Arduino Giga, which exposes a ROS
interface to the rest of the robot's software — the gripper is a node like
any other from the perspective of
[module 2](../course/02-ros2.md), just one whose "actuator" output is a
motor controller board instead of `/cmd_vel`.

**Safety**: as with the rest of the robot, the platform E-stop
([module 1](../course/01-system-hardware.md)) cuts gripper power along
with drive power. A brake-equipped axis is a deliberate safety property in
its own right — it will not drop whatever it is holding purely because power
was cut.

:::{note}
{{ unverified }} This is the mechanism's general design as documented in the
team wiki, not a tested command-level interface. No connection, power or
motion command is given here because none could be confirmed against
running hardware — inventing one would be worse than not having it. Ask the
hardware team for the current control interface and topic names before
writing code against this gripper.
:::

## Hardware and CAD

The team designs its own mounts and PCBs:

- **CAD**: Fusion 360, with an Autodesk education licence
- **Circuit design**: [KiCad](https://www.kicad.org/)
- **3D printing**: [PrusaSlicer](https://www.prusa3d.com/p/prusaslicer/)

Access to the team's CAD cloud is arranged internally.

## Working through the course

Everything in the [course modules](../course/index.md) applies. The
substitutions:

```{list-table}
:header-rows: 1
:widths: 30 70

* - Where the course says
  - On Robotino
* - `/scan`
  - Namespaced per robot; two scanners merged by `laser_scan_integrator`
* - `/cmd_vel`
  - Namespaced per robot — and remember it accepts lateral velocity too
* - Differential drive assumptions
  - Omnidirectional: `linear.y` is meaningful
* - Generic map
  - `mps-map-gen` extends the map with machines and field bounds
* - Generic markers
  - ArUco `ARUCO_ORIGINAL` on machines, cross-checked with laser lines
```

## Further reading

- [Carologistics on GitHub](https://github.com/carologistics)
- [Carologistics team website](https://www.carologistics.org/)
- [RoboCup Logistics League](https://ll.robocup.org/)
- [Festo Robotino](https://www.festo-didactic.com/)
- [Nav2 documentation](https://docs.nav2.org/)
