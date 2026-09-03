# Continue learning

This page is a development plan, not just a list of closed dropdowns —
work through a topic's "Try it" step, not only its description.

## Next steps

Topics you can start on directly after this module's core path.

(launch-files)=
:::{dropdown} Launch files — starting several nodes at once
:icon: light-bulb

**What it is.** A **launch file** starts nodes together, with parameters
and remappings, instead of one `ros2 run` per terminal.

**Why it matters.** Every module from here on starts more than one node
at once; you will build a real launch file in
[module 8](../08-integration.md), where a whole robot starts from a
single command.

**Needs.** This module's core path.

**Try it.** Write a two-node YAML launch file that starts two
`turtlesim_node` instances, the second under a `second` namespace:

```yaml
launch:
- node:
    pkg: "turtlesim"
    exec: "turtlesim_node"
    name: "sim"
- node:
    pkg: "turtlesim"
    exec: "turtlesim_node"
    name: "second_sim"
    namespace: "second"
```

```bash
ros2 launch my_package my_launch_file.launch.yaml
```

**Check.** `ros2 node list` shows both `/sim` and `/second/second_sim`,
and two turtle windows open.

**Common difficulty.** Forgetting the namespace on the second node opens
two windows but leaves both nodes competing for the same
`/turtle1/cmd_vel` topic name.

**Read more.** [Full launch file
walkthrough](../../reference/ros2-cheatsheet.md#launch) for YAML vs
Python launch files and composing them.
:::

:::{dropdown} Parameters, properly — Next step
:icon: light-bulb

**What it is.** Declaring a parameter with a type and a default
(`node.declare_parameter('rate', 10.0)`) instead of relying on an
undeclared name — which, as
[Services, parameters and actions](../02-ros2/services-parameters-actions.md)
already showed, fails loudly rather than doing nothing — and reacting to
a parameter change with a callback instead of only reading it once at
startup.

**Why it matters.** Every node you write for the rest of this course reads
at least one parameter; getting declaration right now avoids exactly the
failed-`param-set` you already triggered on purpose earlier.

**Needs.** [The turtle controller task](turtle-controller.md).

**Try it.** Add a second, declared parameter to `turtle_controller.py`
(e.g. `forward_speed` as a float, replacing the `FORWARD_SPEED` constant),
register an `add_on_set_parameters_callback`, and confirm the callback
fires on `ros2 param set`.

**Check.** `ros2 param get /turtle_controller forward_speed` reflects a
value you set live, and your callback's log line appears when you set it.

**Common difficulty.** Forgetting that `declare_parameter` must run once,
in `__init__`, before anything tries to `get_parameter` it — a
`get_parameter` call on an undeclared name raises immediately, the same
failure mode as the CLI's `param set`.

**Read more.** [ROS 2: using
parameters](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-Python.html)
:::

(custom-message-and-service-types)=
:::{dropdown} Custom message and service types — Next step
:icon: light-bulb

**What it is.** Defining your own `.msg` or `.srv` file in an
`interfaces`-style package when none of the standard `std_msgs` or
`geometry_msgs` types fit your data.

**Why it matters.** Real robot data — a detected object with a label and a
confidence, a mission status with a reason string — rarely fits a bare
`String` or `Float64`; this course's own capstone project uses a custom
`mission_status` message shape for exactly this reason.

**Needs.** A working workspace and one built package.

**Try it.** Define a `.msg` file with two fields (e.g. `string label` and
`float64 confidence`), build it, then publish and echo one message of that
type.

**Check.** `ros2 interface show <your_package>/msg/<YourType>` prints your
field definitions, and `ros2 topic echo` shows both fields correctly.

**Common difficulty.** A custom interface package needs its own
`ament_cmake` build (even inside an otherwise Python workspace) — copying
a `.msg` file into an `ament_python` package's folder and expecting
`colcon build` to generate the interface is the single most common first
mistake.

**Read more.** [ROS 2: creating custom msg and srv
files](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html)
:::

:::{dropdown} Namespaces and remapping — Next step
:icon: light-bulb

**What it is.** Running the *same* node under a different name
(`__node:=second_controller`) or with its topics under a namespace prefix
(`/second/turtle1/cmd_vel` instead of `/turtle1/cmd_vel`), without
changing a line of code.

**Why it matters.** This is how two identical robots — or two instances of
the same simulated robot — run side by side without their topics
colliding; you already saw the pattern in the "Launch files" entry above
(`namespace: "second"`).

**Needs.** [The turtle controller task](turtle-controller.md).

**Try it.** Run a second `turtlesim_node` under a namespace
(`ros2 run turtlesim turtlesim_node --ros-args -r __ns:=/second`), then
run your controller the same way, and confirm it drives the *second*
turtle, not the first.

**Check.** `ros2 topic list` shows both `/turtle1/cmd_vel` and
`/second/turtle1/cmd_vel` as separate topics, and only the second window's
turtle moves.

**Common difficulty.** Remapping the *node* name and remapping the
*topic namespace* are two different flags (`__node:=` vs `__ns:=`) doing
two different jobs; mixing them up renames the wrong thing.

**Read more.** [ROS 2: remapping
arguments](https://docs.ros.org/en/humble/How-To-Guides/Node-arguments.html)
:::

## Intermediate projects

Larger exercises that connect more than one subtopic.

:::{dropdown} QoS basics, with a reproducible mismatch — Intermediate
:icon: light-bulb

**What it is.** Quality of Service settings — **reliability**
(`RELIABLE` vs `BEST_EFFORT`) and **durability** (`VOLATILE` vs
`TRANSIENT_LOCAL`) — that a publisher and subscriber must be
*compatible* on, not necessarily identical, or no data crosses at all with
no error message.

**Why it matters.** A QoS mismatch is one of the few ROS 2 failures with
**zero** error output — the node runs, the topic exists, and nothing
arrives. [Module 3's](../03-sensors-tf/practical-exercise.md#common-problems) "RViz shows
nothing" diagnosis exists largely because of this.

**Needs.** [The turtle controller task](turtle-controller.md) and a
second, hand-written subscriber node.

**Try it — reproduce the failure on purpose.** Write a tiny second node
that subscribes to `/turtle1/cmd_vel` with `RELIABLE` reliability, while
temporarily publishing from a modified copy of your controller with
`BEST_EFFORT`. Confirm nothing arrives, then check `ros2 topic info -v
/turtle1/cmd_vel` to see the mismatch reported there.

**Check.** You can point at the exact `ros2 topic info -v` output line
that shows the incompatible profiles, and fix it by matching one setting.

**Common difficulty.** `ros2 topic pub` and `ros2 topic echo` both default
to a QoS that is compatible with almost anything, which is exactly why the
mismatch only shows up once you set it explicitly in code — the CLI tools
alone will not reproduce this bug for you.

**Read more.** [ROS 2: About Quality of Service
settings](https://docs.ros.org/en/humble/Concepts/Intermediate/About-Quality-of-Service-Settings.html)
:::

(lifecycle-nodes)=
:::{dropdown} Lifecycle nodes — Intermediate
:icon: light-bulb

**What it is.** A node with an explicit state machine
(`unconfigured → inactive → active → finalized`) instead of "doing its job
the moment it starts" — you already ran `ros2 lifecycle get` against one in
[module 6](../06-navigation/nav2-architecture-and-costmaps.md#how-it-works) without building one yourself.

**Why it matters.** A lifecycle node lets a supervisor (or you, by hand)
control exactly when it starts doing real work — critical for a system
where bring-up order matters, which is the entire subject of
[module 8](../08-integration.md#core-concepts).

**Needs.** Comfort with plain `rclpy` nodes.

**Try it.** Convert `turtle_controller.py` into a
`rclpy.lifecycle.LifecycleNode`, moving the publisher's creation into
`on_configure` and only starting the timer in `on_activate`.

**Check.** `ros2 lifecycle get /turtle_controller` reports `unconfigured`
immediately after launch, and the turtle does not move until you call
`ros2 lifecycle set /turtle_controller activate`.

**Common difficulty.** Forgetting that a lifecycle node's callbacks must
each return a `TransitionCallbackReturn` value — a plain `return` (which
returns `None`) is treated as a failed transition, not a successful one.

**Read more.** [ROS 2: managed
(lifecycle) nodes](https://docs.ros.org/en/humble/Concepts/Intermediate/About-Ros2-Managed-Nodes.html)
:::

## Advanced topics

Research-adjacent frameworks, or content not yet fully tested on this
course's own hardware.

:::{dropdown} Node composition — Advanced
:icon: light-bulb

**What it is.** Loading several nodes as plugins into one OS process
(a "component container"), instead of one process per node, so that
messages between them can be passed by pointer instead of copied and
serialized.

**Why it matters.** For a high-rate pipeline — a camera driver feeding a
perception node feeding a detector, all in [module
4](../04-perception/index.md) — process-per-node overhead adds real
latency; composition removes most of it.

**Needs.** Two working nodes, in separate packages.

**Try it.** Convert one node into a composable node class and load both it
and a second node into one `component_container` using
`ros2 component load`.

**Check.** `ros2 component list` shows both components loaded into the
same container process.

**Common difficulty.** A composable node's constructor signature differs
from a plain node's (`rclpy.node.Node.__init__` takes `context` and other
composition-specific arguments you must pass through), so a
straight copy-paste of a plain node usually needs small adjustments.

**Read more.** [ROS 2:
composition](https://docs.ros.org/en/humble/Tutorials/Intermediate/Composition.html)
:::

:::{dropdown} Executors and callback groups — Advanced
:icon: light-bulb

**What it is.** The **executor** is what actually calls your callbacks;
the default single-threaded executor runs them one at a time, which is
usually fine until one callback blocks and starves every other callback in
that node. **Callback groups** (`MutuallyExclusiveCallbackGroup`,
`ReentrantCallbackGroup`) control which callbacks are allowed to run
concurrently against a multi-threaded executor.

**Why it matters.** A node that "randomly stops responding to one topic
while another still works" is very often a single blocking callback
starving a single-threaded executor, not a network or QoS problem.

**Needs.** Comfort with plain `rclpy` nodes and Python threading concepts.

**Try it.** Add a deliberately slow (`time.sleep(2)`) callback to one
subscription in a node with two subscriptions on a single-threaded
executor, and observe the second subscription's callback stall too; then
switch to a `MultiThreadedExecutor` and confirm it no longer does.

**Check.** You can explain, from what you observed, which executor and
which callback-group setting fixed the stall.

**Common difficulty.** Switching to a `MultiThreadedExecutor` alone does
not make callbacks thread-safe against each other — shared state your
callbacks both touch (like `self.state` in this module's own controller)
still needs a lock or a `ReentrantCallbackGroup` used deliberately, not by
accident.

**Read more.** [ROS 2: executors and callback
groups](https://docs.ros.org/en/humble/Concepts/Intermediate/About-Executors.html)
:::

(automated-tests-for-ros-2-packages)=
:::{dropdown} Automated tests for ROS 2 packages — Advanced
:icon: light-bulb

**What it is.** Unit tests for plain Python logic via `pytest`
(no ROS 2 needed), and integration tests via `launch_testing`, which starts
real nodes and checks what they publish — both run automatically by
`colcon test`, exactly as this course's own `turtle_course` package does
for its style checks.

**Why it matters.** A change that breaks a node's behaviour should fail a
test, not get discovered when the [capstone project](../hackathon.md)
breaks in front of you — this is what
[module 8's](../08-integration.md#core-concepts) "reproducible" standard
looks like applied to code instead of launch files.

**Needs.** A working package with at least one node.

**Try it.** Write one `pytest` unit test that checks
`turtle_controller.py`'s state machine transitions correctly after four
simulated `TIMER_PERIOD`-sized time steps — call `control_loop()` directly
in the test rather than actually running ROS 2.

**Check.** `colcon test --packages-select turtle_course` shows your new
test passing (or correctly failing, if you deliberately break the
transition logic first to confirm the test actually catches it).

**Common difficulty.** Testing a real `rclpy` node usually needs
`rclpy.init()` called once for the whole test session, not per test — a
missing or repeated `init()` produces confusing errors that look unrelated
to the actual logic being tested.

**Read more.** [ROS 2:
launch_testing](https://github.com/ros2/launch/tree/humble/launch_testing) ·
[colcon test](https://colcon.readthedocs.io/en/released/user/quick-start.html#test-packages)
:::
