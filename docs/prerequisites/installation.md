# Installation

This page gets you from a bare machine to a working ROS 2 workspace.

:::{danger}
**Check which distribution your team uses before you install anything.** The
three MASKOR courses this material comes from were written for different
combinations of Ubuntu and ROS 2, and they are not interchangeable. See
[Versions and compatibility](../reference/compatibility.md).
:::

## Learning objectives

After this page you have:

- Ubuntu installed in the release your team uses;
- ROS 2 installed and sourced;
- a `colcon` workspace that builds;
- the simulator your platform track needs.

## Step 1 — Ubuntu

```{list-table}
:header-rows: 1
:widths: 30 25 45

* - Your track
  - Ubuntu release
  - ROS 2 distribution
* - {{ carologistics }}
  - 24.04 LTS (Noble)
  - Jazzy Jalisco {{ jazzy }}
* - {{ alert }}
  - 22.04 LTS (Jammy)
  - Humble Hawksbill {{ humble }}
* - {{ simulation }}
  - Either, matching whichever track you follow
  - Either
```

Download the image from [releases.ubuntu.com](https://releases.ubuntu.com/),
write it to a USB stick, and boot from it. Ubuntu's own
[installation tutorial](https://ubuntu.com/tutorials/install-ubuntu-desktop)
covers the details.

:::{note}
A native installation is strongly preferred. RViz, Gazebo and Webots all need
working 3D acceleration, which virtual machines rarely provide well. WSL is
possible but adds a whole class of graphics and networking problems on top of
the ones you are here to learn about.
:::

## Step 2 — ROS 2

Follow the official installation guide for your distribution — it is kept
current, and reproducing the apt commands here would only let them go stale:

- {{ jazzy }} [ROS 2 Jazzy installation](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html)
- {{ humble }} [ROS 2 Humble installation](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html)

Install the **desktop** variant (`ros-<distro>-desktop`); it includes RViz and
the visualization tools that later sessions rely on.

Then add the build tooling:

```bash
sudo apt install python3-colcon-common-extensions
sudo apt install ros-$ROS_DISTRO-teleop-twist-keyboard
```

### Source ROS 2 automatically

```bash
echo "source /opt/ros/$ROS_DISTRO/setup.bash" >> ~/.bashrc
```

Open a new terminal and confirm:

```bash
echo $ROS_DISTRO
```

This should print `jazzy` or `humble`. If it prints nothing, ROS 2 is not
sourced and nothing else on this page will work.

:::{tip}
`$ROS_DISTRO` is set for you once ROS 2 is sourced. This course uses
`$ROS_DISTRO` in `apt install` commands rather than a hard-coded name, so the
same command works on both distributions.
:::

## Step 3 — Create a workspace

A *workspace* is a directory where you build your own packages. Create one and
build it once so the layout is initialised:

```bash
mkdir -p ~/robot_ws/src
cd ~/robot_ws
colcon build
```

You now have three new directories next to `src`:

`build`
: intermediate build artefacts — CMake and compiler output

`install`
: the result: the packages plus the `setup.*sh` files you source

`log`
: logs of each `colcon build` invocation, useful when a build fails

Add the workspace to your shell configuration:

```bash
echo "source ~/robot_ws/install/setup.bash" >> ~/.bashrc
```

:::{warning}
Never run `colcon build` with `sudo`. It creates root-owned files in your
workspace that later builds cannot overwrite, and the fix is more annoying than
the problem you were trying to solve.
:::

## Step 4 — The simulator

Which simulator you install depends on your track.

### Webots

{{ simulation }} {{ carologistics }} {{ alert }}

Both the Carologistics RCLL simulation and the ALeRT Spot simulation are built
on [Webots](https://cyberbotics.com/).

```bash
# ROS 2 interface for Webots
sudo apt install ros-$ROS_DISTRO-webots-ros2
```

Install Webots itself from the
[official installation guide](https://cyberbotics.com/doc/guide/installation-procedure).

:::{admonition} Webots versions differ between teams
:class: warning

Both source courses pin **Webots R2023b**, but they pair it with different ROS
2 distributions, and the simulation repositories move independently of this
site. Install the version your team's simulation repository asks for in its
README rather than the newest release. See
[compatibility](../reference/compatibility.md).
:::

Then follow your platform page for the actual simulation package:

- [Simulation track](../platforms/simulation.md)
- [Carologistics / Robotino](../platforms/carologistics-robotino.md)
- [ALeRT / Spot](../platforms/alert-spot.md)

## Step 5 — An editor

Any editor works. Most of the teams use
[Visual Studio Code](https://code.visualstudio.com/), which matters later
because its Remote-SSH extension lets you edit code directly on a robot.

Start it from inside a package directory:

```bash
cd ~/robot_ws/src
code .
```

:::{tip}
`File > Save Workspace As…` inside your ROS workspace (for example
`~/robot_ws/robot.code-workspace`) stores your open files and settings. Opening
that file later restores the session, which is worth the ten seconds it takes.
:::

## Verify your installation

:::{admonition} Task: prove the installation works
:class: task

Run each of these and check the result:

```bash
# 1. ROS 2 is sourced
echo $ROS_DISTRO

# 2. A node starts
ros2 run turtlesim turtlesim_node

# 3. In a second terminal: the node is visible
ros2 node list

# 4. In the second terminal: you can drive the turtle
ros2 run turtlesim turtle_teleop_key
```
:::

:::{admonition} Expected result
:class: result

Step 1 prints your distribution name. Step 2 opens a window with a turtle in
it. Step 3 lists `/turtlesim`. Step 4 lets you move the turtle with the arrow
keys, as long as the cursor stays in that terminal.

If all four work, your installation is sound and you are ready for session 1.
:::

## Common mistakes

**`ros2: command not found`.**
ROS 2 is not sourced in this terminal. Check `echo $ROS_DISTRO`, then check
that the `source` line is really in `~/.bashrc` and that you opened a new
terminal.

**`Package 'turtlesim' not found`.**
You installed `ros-<distro>-ros-base` instead of the desktop variant. Install
it explicitly: `sudo apt install ros-$ROS_DISTRO-turtlesim`.

**`colcon build` succeeds but `ros2 run` cannot find your package.**
You did not source `install/setup.bash` after building, or you are in a
terminal that was opened before the build.

**Mixed distributions.**
Sourcing two different ROS 2 distributions in the same shell produces errors
that make no sense. Keep exactly one `source /opt/ros/...` line in `.bashrc`.

## Further reading

- [ROS 2 documentation](https://docs.ros.org/) — start here for anything ROS 2
- [colcon documentation](https://colcon.readthedocs.io/)
- [Versions and compatibility](../reference/compatibility.md) on this site
