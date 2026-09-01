# Versions and compatibility

The three source courses that this site was built from targeted **different**
operating systems, ROS 2 distributions and simulator versions. Following an
instruction written for one system on another produces failures that look like
broken code and are not.

This page records what each instruction was written for.

:::{important}
**If you are setting up a machine with no existing team infrastructure to
match** — a spare laptop, a fresh simulation-only install — this course
recommends **Ubuntu 24.04 with ROS 2 Jazzy**: it is the newer LTS with the
longer support window, and it is what the shared course content (the general
[course modules](../course/index.md), largely drawn from the ROS Summer
School) and the [simulation track](../platforms/simulation.md) are tested
against going forward.

This is a **recommendation for new installs, not a rewrite of existing
guides.** The ALeRT/Spot material stays exactly what it has always been —
**Ubuntu 22.04 with ROS 2 Humble** — because that is what the team's actual
robot runs, and silently "upgrading" a hardware-specific guide to a
distribution nobody has tested it on would be worse than leaving it alone.
If you are joining ALeRT, install Humble on 22.04, full stop; the
recommendation above is not for you.
:::

:::{danger}
**Never assume an instruction transfers between tracks.** ROS 2 distributions
are not compatible with each other: package names differ
(`ros-humble-*` vs `ros-jazzy-*`), APIs change between releases, and a package
that exists in one may not exist in the other.

Where this site could not verify a command on a given distribution, it says so
rather than guessing.
:::

## The matrix

```{list-table}
:header-rows: 1
:widths: 16 15 14 14 20 21

* - Platform
  - OS
  - ROS 2
  - Simulator
  - Key packages
  - Status
* - **Simulation** {{ simulation }}
  - Ubuntu 22.04 or 24.04
  - Humble or Jazzy
  - Webots
  - `webots_ros2`, `nav2`, `slam_toolbox`
  - Verified against upstream docs; must match the track you follow
* - **Carologistics / Robotino** {{ carologistics }}
  - Ubuntu 24.04, or Fedora
  - Jazzy {{ jazzy }}
  - Webots
  - `robotino_navigation`, `rcll_simulation_webots`, `mps-map-gen`,
    `laser_scan_integrator`, `nav2`
  - **Inconsistent in the sources** — see the note below
* - **ALeRT / Spot** {{ alert }}
  - Ubuntu 22.04
  - Humble {{ humble }}
  - Webots R2023b
  - `webots_ros2_spot`, `nav2`, `slam_toolbox`, `octomap`, `moveit2`,
    `rafcon`
  - As documented by the source course
* - **ROS Summer School** (origin of much of the general material)
  - Ubuntu (release not stated)
  - Humble {{ humble }}
  - —
  - `nav2`, `slam_toolbox`, `apriltag_ros`, `usb_cam`, `realsense-ros`
  - Written for physical hardware; generalised on this site
```

## Known inconsistencies

These are real contradictions in the source material, not errors introduced
here. They are recorded so that nobody spends an evening on them.

### Carologistics: Jazzy or Humble?

The Carologistics introductory setup guide specifies **Ubuntu 24.04 with ROS 2
Jazzy**. The `robotino_navigation` repository documents **ROS 2 Humble** and
states that it has been tested on that release.

**What to do**: check the README of each repository before building it. Ask the
team which combination is currently deployed on the robots. This page cannot
resolve the contradiction because resolving it requires testing on the actual
hardware.

{{ unverified }}

### Webots versions

Both team courses reference **Webots R2023b**. Simulation repositories are
often pinned to a specific Webots release, and they move independently of this
site.

**What to do**: install the version the simulation repository's README asks
for, not the newest release and not the version named here.

{{ unverified }}

### Carologistics runs Fedora as well as Ubuntu

The team's robots and some workstations run Fedora, with setup automated
through Ansible. The `dnf` commands in the Carologistics material are Fedora
commands and have no meaning on Ubuntu.

**What to do**: `apt` for Ubuntu, `dnf` for Fedora. The ROS 2 installation
procedure differs substantially between them.

### The Summer School material assumed specific hardware

Much of the general ROS 2, TF, SLAM and Nav2 content on this site originates
from the ROS Summer School, which was taught on a specific robot — an iRobot
Create 3 base with a mini-PC, an RPLidar and a RealSense camera.

On this site that material has been **generalised**: hardware-specific topic
names, driver packages and IP addresses have been replaced with the general
concept, and the platform-specific parts moved to the
[platform pages](../platforms/index.md).

**What to do**: where the course says `/scan` or `/cmd_vel`, check what your
own system actually uses with `ros2 topic list`.

## Distribution differences that matter

```{list-table}
:header-rows: 1
:widths: 25 37 38

* - Topic
  - Humble {{ humble }}
  - Jazzy {{ jazzy }}
* - Ubuntu
  - 22.04 (Jammy)
  - 24.04 (Noble)
* - Support until
  - May 2027
  - May 2029
* - Package prefix
  - `ros-humble-*`
  - `ros-jazzy-*`
* - Default DDS
  - Fast DDS
  - Fast DDS
* - Python
  - 3.10
  - 3.12
```

:::{tip}
Write `ros-$ROS_DISTRO-<package>` rather than a hard-coded distribution name in
your commands and documentation. The same line then works on both, and it is
what this site does throughout.
:::

## Checking your own system

```bash
# Which ROS 2 distribution is sourced?
echo $ROS_DISTRO

# Which Ubuntu release?
lsb_release -a

# Is a specific package installed?
ros2 pkg list | grep nav2

# Which version of a package?
ros2 pkg xml <package_name> | grep version

# Which RMW implementation is in use?
echo $RMW_IMPLEMENTATION
```

## Status legend

```{list-table}
:header-rows: 1
:widths: 25 75

* - Marker
  - Meaning
* - {{ common }}
  - Applies to every platform and both distributions
* - {{ simulation }}
  - Simulation only
* - {{ carologistics }}
  - Specific to Carologistics / Robotino
* - {{ alert }}
  - Specific to ALeRT / Spot
* - {{ jazzy }}
  - Written for ROS 2 Jazzy
* - {{ humble }}
  - Written for ROS 2 Humble
* - {{ unverified }}
  - Taken from source material and **not verified** on current hardware.
    Confirm before relying on it.
```

## A note on how this site handles uncertainty

Where the source material was ambiguous, incomplete, or contradicted itself,
this site does one of three things rather than inventing an answer:

1. States the contradiction explicitly, as above.
2. Marks the section with a visible **TODO-REVIEW** admonition.
3. Points at the authoritative upstream source — a repository README or the
   official ROS 2 documentation — instead of reproducing details that may be
   stale.

Commands, topic names and package names on this site are either taken directly
from the source material, or verified against primary documentation. None have
been guessed.

## Further reading

- [ROS 2 distributions](https://docs.ros.org/en/rolling/Releases.html) — the
  release schedule and support windows
- [ROS 2 Humble documentation](https://docs.ros.org/en/humble/)
- [ROS 2 Jazzy documentation](https://docs.ros.org/en/jazzy/)
- [Ubuntu release cycle](https://ubuntu.com/about/release-cycle)
