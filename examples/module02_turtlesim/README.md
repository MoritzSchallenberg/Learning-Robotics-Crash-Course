# Module 2 example: `turtle_course`

The starter package for [module 2's practical
task](../../docs/course/02-ros2.md#practical-task): a turtlesim controller
that drives the turtle through a square with no keyboard input, using only
a timer callback and a small state machine.

Built for **ROS 2 Humble** on **Ubuntu 22.04**, following this course's
[supported environment](../../docs/reference/compatibility.md). No other
distribution is tested against it.

## Layout

```text
module02_turtlesim/
├── README.md                 -- this file
├── turtle_course/            -- the actual ROS 2 package (ament_python)
│   ├── package.xml
│   ├── setup.py
│   ├── setup.cfg
│   ├── resource/turtle_course
│   └── turtle_course/
│       ├── __init__.py
│       └── turtle_controller.py   -- starter file, with `# TODO` blocks
└── solutions/
    └── turtle_controller_solution.py   -- reference solution, separate
                                            from the package so it is
                                            never accidentally built or
                                            imported by it
```

## Getting it into your workspace

Copy the `turtle_course/` package directory (not this whole
`module02_turtlesim/` folder) into your workspace's `src/`:

```bash
cp -r turtle_course ~/course_ws/src/
cd ~/course_ws
colcon build --packages-select turtle_course
source install/setup.bash
```

If you cloned this repository directly, `turtle_course/` is at
`examples/module02_turtlesim/turtle_course/` from the repository root.

## Running it

In one terminal:

```bash
ros2 run turtlesim turtlesim_node
```

In a second terminal, after building and sourcing as above:

```bash
ros2 run turtle_course turtle_controller
```

**Expected result**: the turtle drives forward, turns roughly 90 degrees,
and repeats four times, ending back close to its start heading, then
stops. The starter file's `# TODO` blocks are unfilled by default, so
running it as downloaded does nothing until you complete them -- see the
module page for the full task description.

## Checking your own work

```bash
colcon test --packages-select turtle_course
colcon test-result --verbose
```

This runs `ament_flake8`, `ament_pep257` and `ament_copyright` (style and
docstring checks, not a functional test of the turtle's actual path --
there is no automated way to check a simulated turtle's on-screen movement
from a unit test). Confirming the square was actually driven is a visual
check in `turtlesim_node`'s window, described on the module page.
