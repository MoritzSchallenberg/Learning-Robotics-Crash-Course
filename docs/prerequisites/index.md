# Prerequisites

Everything in this section should be done **before the first course evening**.
None of it is difficult, but a fresh Linux install plus ROS 2 can easily eat an
evening, and that is time we would rather spend on robots.

## What you need

```{list-table}
:header-rows: 1
:widths: 30 70

* - Requirement
  - Notes
* - A 64-bit computer with Linux
  - Native install strongly preferred. A virtual machine works for the first
    sessions but struggles with 3D visualization and simulation.
* - Ubuntu LTS
  - Which release depends on your team — see
    [the compatibility matrix](../reference/compatibility.md).
* - ROS 2
  - Jazzy Jalisco or Humble Hawksbill, matching your team.
* - Basic Python
  - Variables, functions, classes, imports. Every exercise in this course is
    solvable in Python.
* - A GitHub account
  - With an SSH key, so you can clone and push team repositories.
```

:::{admonition} Which Ubuntu and which ROS 2?
:class: important

Do not guess. The Carologistics and ALeRT stacks are pinned to *different*
distributions, and a mismatch produces errors that look like broken code but
are really a version problem. Check
[Versions and compatibility](../reference/compatibility.md) first, and ask your
team which combination is current.
:::

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

If something does not work, that is normal and worth saying out loud. Bring the
exact error message — not a paraphrase — to the session or your team channel.
Most installation problems are one of three things: the wrong ROS 2
distribution, a workspace that was never sourced, or a network setting.
