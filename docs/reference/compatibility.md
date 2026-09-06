# Supported environment

{{ foundation }}

This site is fixed to one toolchain. Every command, package name and
example on this site is written for the environment below — there is no
distribution choice to make, and no per-command version badge, because this
is simply what the whole site assumes.

```text
Ubuntu 22.04 LTS
ROS 2 Humble
Python 3
colcon
RViz2
ALeRT simulation environment (Webots)
```

Install it with [ROS 2's installation
guide](../ros2/installation.md), then confirm it with the
commands in [Checking your own system](#checking-your-own-system) below.

:::{important}
Every package name, API and available feature on this site is specific to
the one distribution above. If you ever consult another ROS 2
distribution's documentation for reference, treat its package prefixes and
APIs as informative only, not copy-pasteable onto this site's material.
:::

## Simulation-only vs. ALeRT / Spot versions

Everything below runs on the one baseline above; this table only records
what differs between working through this site with no team hardware
(Simulation) and working through it on ALeRT's own platform.

```{list-table}
:header-rows: 1
:widths: 20 20 60

* - Path
  - Simulator
  - Key packages
* - **Simulation** {{ simulation }}
  - Webots
  - `webots_ros2`, `nav2_bringup`, `slam_toolbox`
* - **ALeRT / Spot** {{ alert }}
  - Webots R2023b
  - `webots_ros2_spot`, `nav2_bringup`, `slam_toolbox`, `octomap`,
    `moveit2`, `rafcon`
```

:::{note}
ALeRT's own production repositories evolve independently of this site and
may run a different Ubuntu release, ROS 2 distribution, or Webots version
at any given time. Check the README of a repository before building it,
and treat the table above as this site's documented baseline, not a
guarantee about a specific production deployment.
:::

## Hardware-specific names in the general examples

Where a topic uses a generic topic or frame name — `/scan`,
`/cmd_vel`, `base_link` — check what your own system actually publishes with
`ros2 topic list` or `ros2 run tf2_tools view_frames`; a real robot's exact
names depend on its drivers and URDF, and this site deliberately teaches
the general pattern rather than one specific robot's naming.

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

Expect `humble` from the first command and `22.04` (Jammy) from the second.
Anything else means either the setup script did not complete, or `.bashrc`
is not sourcing `/opt/ros/humble/setup.bash` — see the [installation
guide's troubleshooting section](../ros2/installation.md#common-installation-problems).

## Status legend

Difficulty, based on genuine technical difficulty rather than how central a
topic is:

```{list-table}
:header-rows: 1
:widths: 25 75

* - Marker
  - Meaning
* - {{ foundation }}
  - Needs no prior topic on this site beyond what its own Prerequisites
    section states.
* - {{ intermediate }}
  - Builds directly on one or more Foundation topics.
* - {{ advanced }}
  - A real capability, actively used by ALeRT, that takes more background
    or care to apply correctly.
* - {{ research }}
  - Documented for completeness; not part of ALeRT's competition-ready
    path today.
```

Verification, describing what has actually been checked rather than what
is merely plausible:

```{list-table}
:header-rows: 1
:widths: 25 75

* - Marker
  - Meaning
* - {{ documented }}
  - Confirmed via a repository or written documentation.
* - {{ simulation }}
  - Runs in Webots.
* - {{ hardwareverified }}
  - Actually checked on running hardware.
* - {{ unverified }}
  - Taken from source material and **not verified** on current hardware.
    Confirm before relying on it.
* - {{ hwverificationrequired }}
  - Plausible from documentation, but needs a real hardware check before
    being trusted for a competition run.
* - {{ experimental }}
  - Known to be incomplete or unstable; expect rough edges.
* - {{ historical }}
  - No longer current; kept for context only.
```

{{ alert }} marks content specific to the ALeRT team rather than a general
ROS 2 concept.

## A note on how this site handles uncertainty

Where a technical detail could not be verified — because it depends on
hardware this site cannot test, or on an internal repository — this site
does one of two things rather than inventing an answer:

1. Marks the statement with the {{ unverified }} badge.
2. Points at the authoritative upstream source — a repository README or the
   official ROS 2 documentation — instead of reproducing details that may be
   stale.

Commands, topic names and package names on this site are either verified
against primary documentation for ROS 2 Humble, or explicitly marked
unverified. None have been guessed, and none are carried over unchecked from
a newer distribution's documentation.

## Further reading

- [ROS 2 Humble documentation](https://docs.ros.org/en/humble/)
- [ROS 2 distributions](https://docs.ros.org/en/rolling/Releases.html) — the
  release schedule and support windows, for context on why this site
  chose Humble
