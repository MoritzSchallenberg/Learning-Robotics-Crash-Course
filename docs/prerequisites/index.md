# Prerequisites

Work through this section before starting [module 1](../course/01-system-hardware.md).
None of it needs a ROS 2 installation yet — that step is part of
[module 2](../course/02-ros2/installation.md), where it is immediately
followed by the exercises that use it.

## What you need

```{list-table}
:header-rows: 1
:widths: 30 70

* - Requirement
  - Notes
* - A 64-bit computer with Linux
  - Native install strongly preferred. A virtual machine works for the early
    modules but struggles with 3D visualization and simulation.
* - Ubuntu 22.04 LTS
  - The course's fixed baseline — see
    [Supported environment](../reference/compatibility.md). Installed as
    part of [module 2](../course/02-ros2/installation.md), not here.
* - ROS 2 Humble Hawksbill
  - The only distribution this course uses; installed as part of
    [module 2](../course/02-ros2/installation.md), not here.
* - Basic Python
  - Variables, functions, classes, imports. Every exercise in this course is
    solvable in Python.
* - A GitHub account
  - With an SSH key, so you can clone and push team repositories.
```

## Work through these in order

```{toctree}
:maxdepth: 1

linux-terminal
git
networking
```

1. **[Linux and the terminal](linux-terminal.md)** — moving around a Linux
   filesystem, running commands, and what `.bashrc` does. Skip only if you are
   already comfortable in a shell.
2. **[Git](git.md)** — cloning, branching and committing, plus the conventions
   the MASKOR teams expect.
3. **[Networking and SSH](networking.md)** — reaching a robot over the network
   and understanding why ROS 2 sometimes cannot see it.

ROS 2 itself is installed later, as the first step of
[module 2](../course/02-ros2/installation.md) — see that page rather than
installing it here.

## Getting help

If something does not work, that is normal. Bring the exact error message —
not a paraphrase — when you ask your team for help. Once you reach
module 2's installation, most problems there are one of three things: a
distribution other than Humble installed by mistake, a workspace that was
never sourced, or a network setting.
