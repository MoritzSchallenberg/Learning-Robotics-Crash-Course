# Prerequisites

Work through this section before starting [module 1](../course/01-system-hardware.md).
None of it is difficult, but a fresh Linux install plus ROS 2 can easily eat
several hours, and that is time better spent later on robots than debugging
an installation mid-module.

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
    [Supported environment](../reference/compatibility.md).
* - ROS 2 Humble Hawksbill
  - The only distribution this course uses; see the installation guide below.
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
installation
git
networking
```

1. **[Linux and the terminal](linux-terminal.md)** — moving around a Linux
   filesystem, running commands, and what `.bashrc` does. Skip only if you are
   already comfortable in a shell.
2. **[Installation](installation.md)** — Ubuntu, ROS 2, a workspace, and the
   simulator your team uses.
3. **[Git](git.md)** — cloning, branching and committing, plus the conventions
   the MASKOR teams expect.
4. **[Networking and SSH](networking.md)** — reaching a robot over the network
   and understanding why ROS 2 sometimes cannot see it.

## Getting help

If something does not work, that is normal. Bring the exact error message —
not a paraphrase — when you ask your team for help. Most installation
problems are one of three things: a distribution other than Humble
installed by mistake, a workspace that was never sourced, or a network
setting.
