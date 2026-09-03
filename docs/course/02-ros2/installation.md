# Installation

{{ common }}

This page gets you from a bare Ubuntu machine to a working ROS 2 Humble
workspace, with nothing left implicit. You should not need to leave this
page to complete the base installation — the official ROS 2 documentation is
linked throughout for reference and troubleshooting, not as a replacement
for the steps here.

Every command below was checked against the official ROS 2 Humble
documentation (`docs.ros.org/en/humble/`, retrieved 2026-09-02), the one
distribution this course uses throughout.

This page is preparation for the rest of this module — a system install and
several downloads, which take a different amount of time on every machine.
Its duration does not count toward this module's own 80–100 minute core
learning time; that time starts once ROS 2 is installed and you move on to
[Nodes and packages](nodes-and-packages.md).

## Learning objectives

After this page you have:

- confirmed your machine meets the course's [supported
  environment](../../reference/compatibility.md);
- ROS 2 Humble installed, sourced automatically in every new terminal;
- a working `colcon` workspace with one example package built;
- rosdep initialised;
- the simulator your platform track needs.

## Step 1 — Check your operating system

The course's fixed baseline is **Ubuntu 22.04 LTS (Jammy)** — see [Supported
environment](../../reference/compatibility.md) for why.

```bash
cat /etc/os-release
```

**Expected result**: `VERSION_ID="22.04"` and `VERSION_CODENAME=jammy`
somewhere in the output.

**Verification**: `lsb_release -a` should print `Ubuntu 22.04.x LTS`.

**Typical problem**: a different Ubuntu release, another distribution, or
WSL. Install Ubuntu 22.04 LTS from
[releases.ubuntu.com](https://releases.ubuntu.com/) first — a native
install is strongly preferred, since RViz and Webots both need working 3D
acceleration that virtual machines and WSL rarely provide well.

## Step 2 — Update the system

```bash
sudo apt update
sudo apt upgrade -y
```

**Explanation**: installs the latest security and package-index updates
before adding a new repository on top.

**Expected result**: the command finishes with no errors; on a freshly
installed system there may be nothing to upgrade.

**Verification**: run `sudo apt update` again — it should report no further
changes.

:::{warning}
The official ROS 2 Humble installation notes flag a specific, documented
risk on Ubuntu 22.04: skipping this update step on a very fresh install can,
in rare cases, remove `systemd`- and `udev`-related packages during the ROS 2
install and break the desktop session. Running the update above first avoids
it.
:::

## Step 3 — Set the locale to UTF-8

ROS 2 requires a UTF-8 locale; most fresh Ubuntu installs already have one,
but confirm rather than assume.

```bash
locale
```

**Expected result**: `LANG=en_US.UTF-8` and similar `LC_*` lines all ending
in `UTF-8`. If they do not, set it explicitly:

```bash
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```

**Verification**: run `locale` again — every line should end in `UTF-8`.

**Typical problem**: a non-English locale that is not UTF-8 (e.g.
`de_DE.ISO-8859-1`). Any UTF-8 locale works, it does not have to be
`en_US`; `de_DE.UTF-8` is equally valid if you generate that instead.

## Step 4 — Enable required Ubuntu repositories

The ROS 2 packages depend on Ubuntu's **universe** repository.

```bash
sudo apt install software-properties-common
sudo add-apt-repository universe
```

**Expected result**: apt reports the universe repository as enabled (or
already enabled).

**Verification**:

```bash
apt-cache policy | grep universe
```

should list at least one `universe` component.

## Step 5 — Add the ROS 2 apt repository

```bash
sudo apt update && sudo apt install curl -y
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F'"' '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb
```

**Explanation**: this is the official ROS 2 apt-source package. It installs
the signing key and the `packages.ros.org` repository entry for your exact
Ubuntu release in one step, so there is no key or sources-list line to copy
by hand.

**Expected result**: `dpkg -i` finishes with no errors and reports the
package as installed.

**Verification**:

```bash
apt-cache policy | grep -A1 packages.ros.org
```

shows the ROS 2 repository listed.

**Typical problem**: `curl: (6) Could not resolve host` — no network
connection, or a captive portal that has not been accepted yet.

## Step 6 — Install ROS 2 Humble Desktop

```bash
sudo apt update
sudo apt install ros-humble-desktop
```

**Explanation**: the **desktop** variant includes RViz2 and the
visualization tools every later module relies on — do not substitute
`ros-humble-ros-base`, which omits them.

**Expected result**: apt downloads and installs several hundred packages;
this can take a while on a slow connection.

**Verification**:

```bash
apt list --installed | grep ros-humble-desktop
```

**Typical problem**: `Unable to locate package ros-humble-desktop` means
step 5 did not complete — re-run `apt-cache policy | grep packages.ros.org`
to confirm the repository is actually present before retrying.

## Step 7 — Install development tools

```bash
sudo apt install ros-dev-tools
```

**Explanation**: this bundles `colcon` (the build tool), `rosdep`
(dependency installer) and other command-line tools used throughout the
course, so they do not need to be installed one by one.

**Expected result**: installs with no errors.

**Verification**: `colcon version` and `rosdep --version` both print a
version number.

## Step 8 — Initialise rosdep

```bash
sudo rosdep init
rosdep update
```

**Explanation**: `rosdep` maps a package's declared dependencies to the
correct apt packages for your system. `rosdep init` sets this up once
system-wide; `rosdep update` downloads the current dependency database and
is safe to re-run any time.

**Expected result**: `rosdep update` finishes with `updated cache`.

**Typical problem**: `ERROR: default sources list file already exists` —
`rosdep init` was already run (by you or another user on a shared machine);
this is harmless, continue with `rosdep update`.

## Step 9 — Source ROS 2 in this terminal

```bash
source /opt/ros/humble/setup.bash
```

**Expected result**: no output.

**Verification**:

```bash
echo $ROS_DISTRO
```

should print `humble`.

## Step 10 — Source ROS 2 automatically in every terminal

```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
```

Open a **new** terminal and confirm:

```bash
echo $ROS_DISTRO
```

**Expected result**: `humble`, with no need to source anything by hand.

**Typical problem**: this prints nothing. Either the line was appended to
the wrong file (confirm you are using `bash`, with `echo $SHELL`), or the
terminal was not actually closed and reopened.

:::{warning}
Keep exactly **one** `source /opt/ros/...` line in `.bashrc`. Sourcing two
different ROS 2 distributions in the same shell produces errors that make no
sense until you notice the duplicate line.
:::

## Verify the base installation: talker and listener

:::{admonition} Task: prove ROS 2 itself works, before building anything
:class: task

In one terminal:

```bash
source /opt/ros/humble/setup.bash
ros2 run demo_nodes_cpp talker
```

In a second terminal:

```bash
source /opt/ros/humble/setup.bash
ros2 run demo_nodes_py listener
```
:::

:::{admonition} Expected result
:class: result

The talker terminal prints `Publishing: 'Hello World: N'` roughly once a
second; the listener terminal prints `I heard: [Hello World: N]` with
matching numbers. This confirms both the C++ and the Python client library
work, which is the actual thing this step exists to check.
:::

Stop both with <kbd>Ctrl</kbd>+<kbd>C</kbd>.

## Step 11 — Create your own workspace

A *workspace* is a directory where you build your own packages, kept
separate from the system installation in `/opt/ros`.

```bash
mkdir -p ~/robot_ws/src
cd ~/robot_ws
colcon build
```

**Expected result**: `colcon build` reports `Summary: 0 packages finished`
— correct, since `src` is still empty — and creates three new directories:

`build`
: intermediate build artefacts — CMake and compiler output

`install`
: the result: the packages plus the `setup.*sh` files you source

`log`
: logs of each `colcon build` invocation, useful when a build fails

:::{warning}
Never run `colcon build` with `sudo`. It creates root-owned files in your
workspace that later builds cannot overwrite, and the fix is more annoying
than the problem you were trying to solve.
:::

## Step 12 — Build an example package

```bash
cd ~/robot_ws/src
ros2 pkg create --build-type ament_python my_first_pkg
cd ~/robot_ws
colcon build --packages-select my_first_pkg
```

**Expected result**: `colcon build` reports `Summary: 1 package finished`.

**Verification**:

```bash
source ~/robot_ws/install/setup.bash
ros2 pkg list | grep my_first_pkg
```

should print `my_first_pkg`.

## Step 13 — Source your workspace automatically

```bash
echo "source ~/robot_ws/install/setup.bash" >> ~/.bashrc
```

**Verification**: open a new terminal and run `ros2 pkg list | grep
my_first_pkg` directly, with no manual `source` first.

:::{note}
This line must come **after** the `/opt/ros/humble/setup.bash` line in
`.bashrc` — a workspace overlay only makes sense on top of the base
installation it was built against.
:::

## Step 14 — The simulator

Which simulator you install depends on your platform track.

{{ simulation }} {{ carologistics }} {{ alert }}

Both the Carologistics RCLL simulation and the ALeRT Spot simulation are
built on [Webots](https://cyberbotics.com/).

```bash
sudo apt install ros-humble-webots-ros2
```

**Verification**: `ros2 pkg list | grep webots_ros2`.

Install Webots itself from the [official installation
guide](https://cyberbotics.com/doc/guide/installation-procedure), then
follow your platform page for the actual simulation package:

- [Simulation track](../../platforms/simulation.md)
- [Carologistics / Robotino](../../platforms/carologistics-robotino.md)
- [ALeRT / Spot](../../platforms/alert-spot.md)

## Step 15 — An editor

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
`~/robot_ws/robot.code-workspace`) stores your open files and settings.
Opening that file later restores the session.
:::

## Preflight check

Run this once the steps above are done, before continuing to [Nodes and
packages](nodes-and-packages.md), and again any time something feels
wrong — a read-only script that checks your OS, `ROS_DISTRO`, the `ros2`
CLI, your workspace, RViz, the simulator and basic network settings, then
tells you exactly what to fix.

```bash
bash scripts/course-preflight.sh
```

It prints `PASS`, `WARNING` or `FAIL` for each check, with a concrete next
step for anything short of `PASS`, and exits non-zero if any check `FAIL`s.

:::{note}
The script only reads state. It never installs anything, changes
configuration, deletes a file, reads a credential, or queries a private
network target — safe to run as often as you like, on any machine.
:::

## Common installation problems

**`ros2: command not found`.**
ROS 2 is not sourced in this terminal. Check `echo $ROS_DISTRO`, then check
that the `source` line is really in `~/.bashrc` and that you opened a new
terminal.

**`Unable to locate package ros-humble-desktop`.**
Step 5 (adding the ROS 2 apt repository) did not complete, or `sudo apt
update` was not re-run afterwards. Re-check
`apt-cache policy | grep packages.ros.org`.

**`Package 'turtlesim' not found`.**
You installed `ros-humble-ros-base` instead of the desktop variant. Install
it explicitly: `sudo apt install ros-humble-turtlesim`.

**`colcon build` succeeds but `ros2 run` cannot find your package.**
You did not source `install/setup.bash` after building, or you are in a
terminal that was opened before the build.

**`rosdep: command not found`.**
Step 7 was skipped or failed — re-run `sudo apt install ros-dev-tools`.

**Locale-related warnings from `rosdep` or `colcon`.**
Revisit step 3; a non-UTF-8 locale causes exactly this class of unrelated-
looking warning.

## Next subtopic

With ROS 2 installed, sourced, and one example package built, continue to
[Nodes and packages](nodes-and-packages.md), where this module's own
turtlesim lab starts.

## Further reading

- [ROS 2 Humble installation guide](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html) — retrieved 2026-09-02, the authoritative source this page was checked against
- [colcon documentation](https://colcon.readthedocs.io/en/released/)
- [rosdep documentation](https://docs.ros.org/en/independent/api/rosdep/html/)
- [Supported environment](../../reference/compatibility.md) on this site
