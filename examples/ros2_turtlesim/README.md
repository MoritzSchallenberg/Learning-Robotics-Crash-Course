# ROS 2 example: `turtle_tutorial`

The starter package for [the ROS 2 topic's practical
task](../../docs/ros2/index.md#practical-exercises): a turtlesim controller
that drives the turtle through a square with no keyboard input, using only
a timer callback and a small state machine.

Built for **ROS 2 Humble** on **Ubuntu 22.04**, following this site's
[supported environment](../../docs/reference/compatibility.md). No other
distribution is tested against it.

## Layout

```text
ros2_turtlesim/
├── README.md                   -- this file
├── turtle_tutorial/            -- the actual ROS 2 package (ament_python)
│   ├── package.xml
│   ├── setup.py
│   ├── setup.cfg
│   ├── resource/turtle_tutorial
│   └── turtle_tutorial/
│       ├── __init__.py
│       └── turtle_controller.py   -- starter file, with `# TODO` blocks
└── solutions/
    └── turtle_controller_solution.py   -- reference solution, separate
                                            from the package so it is
                                            never accidentally built or
                                            imported by it
```

## Getting it into your workspace

Copy the `turtle_tutorial/` package directory (not this whole
`ros2_turtlesim/` folder) into your workspace's `src/`:

```bash
cp -r turtle_tutorial ~/ros2_ws/src/
cd ~/ros2_ws
colcon build --packages-select turtle_tutorial
source install/setup.bash
```

If you cloned this repository directly, `turtle_tutorial/` is at
`examples/ros2_turtlesim/turtle_tutorial/` from the repository root.

## Running it

In one terminal:

```bash
ros2 run turtlesim turtlesim_node
```

In a second terminal, after building and sourcing as above:

```bash
ros2 run turtle_tutorial turtle_controller
```

**Expected result**: the turtle drives forward, turns roughly 90 degrees,
and repeats four times, ending back close to its start heading, then
stops. The starter file's `# TODO` blocks are unfilled by default, so
running it as downloaded does nothing until you complete them -- see the
ROS 2 topic page for the full task description.

## Checking your own work

```bash
colcon test --packages-select turtle_tutorial
colcon test-result --verbose
```

This runs `ament_flake8`, `ament_pep257` and `ament_copyright` (style and
docstring checks, not a functional test of the turtle's actual path --
there is no automated way to check a simulated turtle's on-screen movement
from a unit test). Confirming the square was actually driven is a visual
check in `turtlesim_node`'s window, described on the ROS 2 topic page.
