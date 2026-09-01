# Linux and the terminal

{{ common }}

Everything in robotics research happens in a terminal. Not because graphical
tools are bad, but because a robot you are connected to over the network often
gives you nothing else — and because a command you can type is a command you
can put in a script.

## Learning objectives

After this page you can:

- open and split a terminal, and stop a running program;
- navigate a Linux filesystem with absolute and relative paths;
- create files and directories from the command line;
- explain what `~/.bashrc` does and why ROS 2 depends on it;
- add a `source` line and an alias to your shell configuration.

## Prerequisites

A working Linux system. Nothing else.

## The terminal

A *terminal* (more precisely a terminal emulator) is a program that gives you a
text interface to the operating system: you type a command, the system runs it,
and prints the result. The program that reads and interprets what you type is
the *shell*; on Ubuntu that is **Bash** (Bourne Again SHell).

The shortcuts worth memorising on day one:

```{list-table}
:header-rows: 1
:widths: 40 60

* - Shortcut
  - Effect
* - `Ctrl` + `Alt` + `T`
  - Open a new terminal window
* - `Ctrl` + `Shift` + `T`
  - Open a new tab in the current terminal
* - `Ctrl` + `Shift` + `C`
  - Copy from the terminal
* - `Ctrl` + `Shift` + `V`
  - Paste into the terminal
* - `Ctrl` + `C`
  - Stop the program that is currently running
* - `Tab`
  - Auto-complete a command or path
```

`Ctrl` + `C` is the one you will use constantly: almost every ROS 2 node runs
until you stop it.

### Terminator

A robot system means many programs running at once, each in its own terminal.
[Terminator](https://gnome-terminator.org/) splits one window into several
panes so you can watch them all together.

```{list-table}
:header-rows: 1
:widths: 40 60

* - Shortcut
  - Effect
* - `Ctrl` + `Shift` + `E`
  - Split the current pane vertically
* - `Ctrl` + `Shift` + `O`
  - Split the current pane horizontally
```

Install it with:

```bash
sudo apt install terminator
```

## Moving around the filesystem

Linux arranges every file in a single tree that starts at the *root directory*,
written `/`. There are no drive letters; a USB stick or a second disk is
mounted somewhere inside that same tree.

### Where am I, and who am I?

```bash
whoami   # your username
pwd      # print working directory: where you are right now
```

Whenever this course writes `<username>`, substitute what `whoami` prints.

### Listing directory contents

```bash
ls                # contents of the current directory
ls -l /etc        # long format, contents of /etc
ls -a ~           # include hidden files (names starting with a dot)
```

The general shape is `ls <options> <location>`; both parts are optional.

### Absolute and relative paths

An **absolute** path describes a location starting from the root and always
begins with `/`:

```bash
ls /home/<username>/Desktop
```

A **relative** path starts from wherever you currently are and has no leading
slash. If you are already in your home directory, this is the same thing:

```bash
ls Desktop
```

Three shortcuts appear everywhere:

`~`
: your home directory (`/home/<username>`)

`.`
: the current directory

`..`
: the parent directory

### Changing directory

```bash
cd ~/Downloads    # go to Downloads inside your home directory
cd ..             # go up one level
cd                # go home
```

:::{tip}
Press `Tab` while typing a path and the shell completes it for you. If several
names match, nothing happens on the first press — press `Tab` twice to see all
candidates. Using `Tab` is not laziness; it is how you avoid typos in long
paths.
:::

### Creating files and directories

```bash
mkdir test                   # create a directory
mkdir -p test/subdirectory   # create it including any missing parents
touch test/example_file      # create an empty file
```

If the file already exists, `touch` leaves the content alone and just updates
its timestamps.

## The shell configuration: `.bashrc`

Every time you open a terminal, Bash reads and executes `~/.bashrc` before
handing you the prompt. It is an ordinary shell script, and it is where you put
anything that should apply to every new terminal. The leading dot makes it
hidden, which is why you need `ls -a` to see it.

This file matters enormously for ROS 2.

### Sourcing

The `source` command runs a script **in your current shell**, so the variables
it sets stick around afterwards. ROS 2 uses this to make its packages findable:

```bash
source /opt/ros/$ROS_DISTRO/setup.bash    # the ROS 2 installation itself
source ~/robot_ws/install/setup.bash      # your own workspace on top of it
```

Typing that in every new terminal gets old fast, so append it to `.bashrc`:

```bash
echo "source ~/robot_ws/install/setup.bash" >> ~/.bashrc
```

Or open `~/.bashrc` in an editor and add the line at the end by hand — often
the safer choice, because a mistyped `>` instead of `>>` overwrites the file
instead of appending to it.

:::{note}
Layering matters. Sourcing `/opt/ros/<distro>/setup.bash` makes the
system-wide ROS 2 packages available; sourcing your workspace afterwards puts
your own packages *on top*. If you create a package with the same name as a
system package, your local version wins. That is occasionally what you want and
usually a source of confusion — avoid name clashes.
:::

:::{warning}
Sourcing affects only terminals opened *afterwards*. Terminals you already have
open keep the old environment. After building a workspace, open a new terminal
or re-source it — this is the single most common "but it worked a minute ago"
in ROS 2.
:::

### Aliases

An alias is a short name for a longer command. Robotics workflows repeat the
same few commands hundreds of times, so they pay off quickly:

```bash
alias colcon_ws="colcon build && source install/setup.bash"
```

Put that line in `~/.bashrc` and from then on typing `colcon_ws` in your
workspace root builds and sources it in one go.

## Task

:::{admonition} Task: set up your shell
:class: task

1. Open a terminal and find out your username and current directory.
2. Create the directory `~/robotics_course/notes` in a single command.
3. Create an empty file inside it called `session1.md`.
4. List the contents of your home directory **including** hidden files and find
   `.bashrc`.
5. Open `~/.bashrc` in an editor and add one alias of your own choosing at the
   end of the file.
6. Open a new terminal and check that your alias works.
:::

:::{admonition} Expected result
:class: result

`ls -a ~` shows `.bashrc` among the hidden files, `ls ~/robotics_course/notes`
lists `session1.md`, and your alias runs in a newly opened terminal but not in
the one you edited `.bashrc` in.
:::

## Common mistakes

**"command not found" after editing `.bashrc`.**
You are still in the old terminal. Open a new one, or run `source ~/.bashrc`.

**A single `>` instead of `>>`.**
`>` overwrites the file; `>>` appends to it. If you truncated your `.bashrc`,
Ubuntu ships a fresh copy at `/etc/skel/.bashrc` you can copy back.

**`mkdir: cannot create directory` for a nested path.**
Add `-p` so the parent directories are created too.

**Editing a file you do not own.**
Files under `/opt` or `/etc` need `sudo`. Files in your home directory never
should — if you find yourself typing `sudo` for something in `~`, something
earlier went wrong (often a `sudo colcon build`, which is never correct).

## Further reading

- [The Linux Command Line](https://linuxcommand.org/tlcl.php) — free book, far
  more than you need but excellent
- [ROS 2: Configuring your environment](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Configuring-ROS2-Environment.html)
  — the official take on sourcing
