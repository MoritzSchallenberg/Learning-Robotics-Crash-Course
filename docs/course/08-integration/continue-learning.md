# Continue learning

## Next steps

:::{dropdown} Logging levels and where they belong — Next step
:icon: light-bulb

**What it is.** `get_logger().debug/info/warn/error/fatal(...)` — five
severity levels, filterable at runtime with
`ros2 run <pkg> <node> --ros-args --log-level debug` without touching
code. [The practical exercise's](practical-exercise.md#common-problems)
Common problems section already tells you to add `info`-level logging at
decision points; this topic is choosing the right level for each message.

**Why it matters.** Everything logged at `info` on a busy node buries the
one line that actually mattered during a real debugging session; reserving
`info` for state transitions and decisions, and `debug` for routine detail,
keeps a log usable under pressure.

**Needs.** [The practical exercise](practical-exercise.md).

**Try it.** Audit your `robot_bringup` nodes' log calls and reclassify any
line that fires every cycle (should be `debug`) versus one that fires only
on a state change or an error (should stay `info` or higher).

**Check.** Running with the default log level shows only meaningful
transitions, not a scrolling wall of routine detail; running with
`--log-level debug` shows everything.

**Read more.** [ROS 2: logging](https://docs.ros.org/en/humble/Concepts/Intermediate/About-Logging.html)
:::

:::{dropdown} Measuring topic frequency and latency — Next step
:icon: light-bulb

**What it is.** `ros2 topic hz`
({ref}`this module's own eight-step procedure <the-eight-step-diagnostic-procedure>`,
step 2) measures publish rate; `ros2 topic delay` measures the gap between
a message's timestamp and when it was received — two different, both
useful, numbers.

**Why it matters.** A topic publishing at the expected rate can still have
growing delay (a node falling behind under load); rate alone would miss
that.

**Needs.**
{ref}`This module's eight-step procedure <the-eight-step-diagnostic-procedure>`.

**Try it.** Run `ros2 topic hz /scan` and `ros2 topic delay /scan`
side by side while the system is under normal load, then again while
running something CPU-heavy alongside it (a second build, for instance),
and compare both numbers.

**Check.** You can state whether rate, delay, or both changed under load,
with actual numbers from both runs.

**Read more.** [ROS 2 cheat sheet: diagnostic
sequence](../../reference/ros2-cheatsheet.md#diagnostic-sequence)
:::

## Intermediate projects

:::{dropdown} ROS 2 diagnostics — Intermediate
:icon: light-bulb

**What it is.** The `diagnostic_updater`/`diagnostic_aggregator` packages
publish structured `OK`/`WARN`/`ERROR` status per subsystem on
`/diagnostics`, aggregated into a tree you can inspect with
`ros2 run rqt_runtime_monitor rqt_runtime_monitor` — a standard way to
answer "which part of the system is unhappy" without grepping logs.

**Why it matters.**
{ref}`This module's eight-step diagnostic procedure <the-eight-step-diagnostic-procedure>`
is something *you* run by hand; `diagnostic_updater` is the same idea
running continuously and automatically, the natural next step once a
system has enough subsystems that manual checking does not scale.

**Needs.** [The practical exercise](practical-exercise.md), a working
multi-node system.

**Try it.** Add a `diagnostic_updater.Updater` to one node that reports
`WARN` if a sensor topic's rate drops below a threshold, and confirm it
shows up correctly in the runtime monitor.

**Check.** Stopping the sensor's driver flips that diagnostic's status to
`WARN` or `ERROR` within a few seconds, visible in the monitor.

**Read more.** [ROS 2:
diagnostics](https://docs.ros.org/en/humble/p/diagnostic_updater/)
:::

:::{dropdown} CPU and memory observation — Intermediate
:icon: light-bulb

**What it is.** Standard Linux tools (`top`, `htop`, `ros2 run
rqt_top rqt_top` for a ROS 2-aware view) applied to a running robot
system — which node's process is using the most CPU or memory right now.

**Why it matters.** "The robot is lagging" can be a CPU-bound node stealing
time from everything else, or a slow memory leak that only shows up after
an hour — neither is visible from `ros2 topic hz` alone.

**Needs.** A running multi-node system ([the practical
exercise](practical-exercise.md)).

**Try it.** Run your full `robot_bringup` system and note each node's CPU
and memory usage with `rqt_top` at startup, then again after ten minutes of
running.

**Check.** You can name which process used the most CPU, and whether any
process's memory usage grew unexpectedly over the ten minutes.

**Read more.** [rqt_top](https://docs.ros.org/en/humble/p/rqt_top/)
:::

## Advanced topics

(ansible-as-a-deployment-example)=
:::{dropdown} Ansible as a deployment example — Advanced
:icon: light-bulb

{{ carologistics }} Once several robots run the same software, updating by
hand does not scale. [Ansible](https://docs.ansible.com/) describes the
desired state of a machine in a *playbook* and makes it so — safe to re-run,
works over plain SSH.

```bash
ansible-playbook -i robots.inv -t fast-deploy robot.yml -l robot-1 -K
```

The Carologistics team uses it for both robot deployment and workstation
setup — see the
[Carologistics platform page](../../platforms/carologistics-robotino.md#setup)
for their actual inventory and playbook structure. This is one example of a
deployment tool, not something every team needs to adopt.
:::

:::{dropdown} Continuous Integration for a ROS 2 package — Advanced
:icon: light-bulb

**What it is.** Running {ref}`module 2's automated tests
<automated-tests-for-ros-2-packages>` automatically on every push, in a
clean environment, via GitHub Actions or similar — the same principle this
course's own website uses for its own build
([README](https://github.com/MoritzSchallenberg/Learning-Robotics-Crash-Course)),
applied to a ROS 2 package instead of a Sphinx site.

**Why it matters.** A test that only runs when someone remembers to run it
locally gets skipped under time pressure — exactly when a regression is
most likely to slip through unnoticed.

**Needs.** {ref}`Module 2's automated tests
<automated-tests-for-ros-2-packages>` working locally first.

**Try it.** {{ unverified }} — write a minimal GitHub Actions workflow that
checks out your package, installs ROS 2 Humble (or runs inside an
`osrf/ros:humble-desktop` container image), and runs `colcon test`.

**Check.** The workflow shows green on a passing commit and red on a
commit that deliberately breaks your test from module 2.

**Read more.** [ros-tooling/action-ros-ci](https://github.com/ros-tooling/action-ros-ci)
— a maintained GitHub Action for exactly this.
:::

:::{dropdown} Containers for reproducible deployment — Advanced
:icon: light-bulb

**What it is.** Packaging a ROS 2 environment and your workspace into a
Docker image, so "works on my machine" becomes "works in this exact,
shareable image" — a different answer to the same reproducible-deployment
problem [Ansible](#ansible-as-a-deployment-example) solves by configuring a
real machine instead.

**Why it matters.** A container pins the entire software environment (OS
packages, ROS 2 version, dependencies), not just your own code — useful
for a workstation build that has to match a robot's environment exactly.

**Needs.** [The practical exercise](practical-exercise.md), and basic
Docker familiarity.

**Try it.** {{ unverified }} — write a `Dockerfile` starting from
`osrf/ros:humble-desktop` that copies in and builds one of your packages,
then run a node from inside the resulting container.

**Check.** `docker run` starts your node successfully with no manual setup
step inside the container beyond what the `Dockerfile` already did.

**Read more.** [Docker images for
ROS](https://hub.docker.com/_/ros) · [Ansible as a deployment
example](#ansible-as-a-deployment-example) above, for the alternative
approach
:::

:::{dropdown} SROS2: securing a ROS 2 system — Advanced
:icon: light-bulb

**What it is.** SROS2 adds authentication, encryption and access control to
ROS 2's DDS communication — by default, anything on the same
[`ROS_DOMAIN_ID`](../../prerequisites/networking.md) can publish, subscribe
and call services on anything else, with no authentication at all.

**Why it matters.** A robot that only ever runs on an isolated lab network
may reasonably accept that default; one reachable from a shared or
less-trusted network should not — the same reasoning as
[the networking prerequisite's](../../prerequisites/networking.md) domain-ID
isolation advice, taken further.

**Needs.** A working multi-node system and comfort with the ROS 2 CLI.

**Try it.** {{ unverified }} — generate an SROS2 keystore for one node
using `ros2 security` tooling, and run that node with security enabled
while a second, non-enrolled node attempts to communicate with it.

**Check.** You can state, from what you observed, whether the
non-enrolled node's communication was actually blocked.

**Read more.** [ROS 2:
SROS2](https://docs.ros.org/en/humble/Tutorials/Advanced/Security/Introducing-ros2-security.html)
:::
