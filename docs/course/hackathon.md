# Hackathon: Autonomous Robot Challenge

:::{admonition} Schedule
:class: note

Saturday–Sunday, 07–08 November 2026
:::

{{ common }}

Everything from the eight sessions, on one robot, running on its own.

:::{admonition} Draft rules
:class: warning

This is the **first draft** of the challenge. The scoring is deliberately
published early so that teams can build against it and so that it can be
criticised and corrected before the event. Point values and the exact arena
layout will be confirmed closer to the date. If something here is ambiguous or
unfair, say so — that is what a draft is for.
:::

## The mission

A robot has to cross an operation area autonomously, avoid obstacles, find
targets and reach them. In the extended levels it also picks up an object,
transports it, or reports its position to another system.

The mission is deliberately layered. A team that only completes Level 1 has
still built a working autonomous robot. Levels 2 and 3 are for teams who get
there with time to spare.

### Level 1 — Autonomous traversal

The robot starts at a marked position and must:

1. traverse the operation area **without manual control**;
2. avoid all obstacles, including ones not present when the map was made;
3. reach the designated target zone;
4. signal completion by publishing to the scoring topic.

Everything you need for this is in sessions 1 to 6.

### Level 2 — Find and report

In addition:

1. detect all fiducial markers placed in the area;
2. publish each marker's ID as it is found;
3. store each marker's pose as a TF frame, and keep it available **after the
   marker is out of sight**;
4. return to the start position and signal completion.

Sessions 4 and 7 cover this. Point 3 is the interesting one: it is not enough
to see a marker, you have to remember where it was.

### Level 3 — Manipulate or relay

Choose one, depending on your platform:

**Transport** {{ alert }} {{ carologistics }}
: Pick up a designated object, carry it to the drop zone, and place it.

**Relay** {{ simulation }} {{ common }}
: Report the object's pose accurately enough for a second system to act on it,
  in the `map` frame with a stated accuracy.

## Scoring

A scoring node runs during your attempt. It listens on the topics below,
records what you report and how long you take, and publishes the result.

### Interface

```{list-table}
:header-rows: 1
:widths: 26 30 44

* - Topic
  - Type
  - Meaning
* - `/detected_ids`
  - `std_msgs/msg/Int32`
  - Publish each marker ID as you detect it
* - `/object_reported`
  - `std_msgs/msg/Int32`
  - Publish the ID of a marker whose associated object you also identified
* - `/finished`
  - `std_msgs/msg/Bool`
  - Publish `true` once, when your run is complete
* - `/results`
  - `std_msgs/msg/Float32MultiArray`
  - Published by the scorer with your result
```

:::{warning}
Publish `true` on `/finished` exactly once, and only when you are actually
done. The clock stops at that message, and reports arriving afterwards are not
counted.
:::

### Points

**Positive**

```{list-table}
:header-rows: 1
:widths: 60 20 20

* - Achievement
  - Points
  - Level
* - Reaching the target zone autonomously
  - 5
  - 1
* - Each marker correctly detected and reported
  - 2
  - 2
* - Each marker whose associated object is also reported
  - 3
  - 2
* - Each marker still available as a TF frame at the end of the run
  - 1
  - 2
* - Returning to the start position
  - 3
  - 2
* - Object successfully transported to the drop zone
  - 8
  - 3
* - Object pose reported within 10 cm of ground truth
  - 5
  - 3
```

**Negative**

```{list-table}
:header-rows: 1
:widths: 60 40

* - Penalty
  - Points
* - Each collision with the arena or an obstacle
  - −3
* - Each manual interaction (gamepad, terminal command, physical assistance)
  - −2
* - Each started minute beyond the time limit
  - −1
```

**Time limit**: 15 minutes per attempt.

**Ties** are decided by elapsed time.

:::{note}
Manual interaction is penalised but permitted. A run that finishes with three
manual interventions scores better than one that gets stuck at minute two.
Recovering is worth points.
:::

### The scoring node

Your solution will be graded by a node with this interface. It is published
here so you can test against it — run it yourself during development.

```python
#!/usr/bin/env python3

import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, Float32MultiArray, Int32


class ScoringNode(Node):
    """Records reported IDs and elapsed time for one challenge attempt."""

    def __init__(self):
        super().__init__('scoring_node', namespace='scoring')

        self.marker_ids = set()
        self.object_ids = set()
        self.start_time = time.time()
        self.finished = False

        self.create_subscription(Int32, 'detected_ids', self.on_marker, 10)
        self.create_subscription(Int32, 'object_reported', self.on_object, 10)
        self.create_subscription(Bool, 'finished', self.on_finished, 10)

        self.results_publisher = self.create_publisher(
            Float32MultiArray, 'results', 10)

        self.get_logger().info('Scoring started. Clock is running.')

    def on_marker(self, msg):
        if self.finished:
            return
        if msg.data not in self.marker_ids:
            self.marker_ids.add(msg.data)
            self.get_logger().info(f'Marker reported: {msg.data}')

    def on_object(self, msg):
        if self.finished:
            return
        if msg.data not in self.object_ids:
            self.object_ids.add(msg.data)
            self.get_logger().info(f'Object reported for marker: {msg.data}')

    def on_finished(self, msg):
        if not msg.data or self.finished:
            return
        self.finished = True
        self.publish_results(time.time() - self.start_time)

    def publish_results(self, duration):
        # Format: [marker ids..., -1.0, object ids..., -2.0, duration]
        message = Float32MultiArray()
        message.data = (
            [float(i) for i in sorted(self.marker_ids)]
            + [-1.0]
            + [float(i) for i in sorted(self.object_ids)]
            + [-2.0, duration]
        )
        self.results_publisher.publish(message)
        self.get_logger().info(
            f'Finished. Markers={sorted(self.marker_ids)} '
            f'Objects={sorted(self.object_ids)} Time={duration:.2f}s')


def main():
    rclpy.init()
    node = ScoringNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

:::{admonition} TODO-REVIEW
:class: todo-review

Point values, the time limit and the arena layout are a **draft proposal**,
not confirmed rules. They need review by the course organisers against the
actual arena and the robots available on the day. Collision detection and
ground-truth object poses are assumed to be judged by a human referee; if an
automated method is intended, this section needs revising.
:::

## Preparation

### What to build beforehand

Nothing here should be new on the day. By the end of session 8 you should
have:

- a **bringup** launch file that starts the whole robot with one command;
- a **map** of an environment resembling the arena;
- **localization** that reliably converges;
- **navigation** tuned to your robot's actual velocity and size;
- **detection** of the marker family that will be used;
- a **mission controller** — state machine or behavior tree — that handles
  failure;
- **rosbag recording** as a one-line command.

### What to test beforehand

The failures that end hackathon runs are almost never algorithmic:

- **Battery life.** How long does a full charge actually last under load? Is
  there a spare, and is it charged?
- **Cold start.** Can you go from powered-off to navigating in under five
  minutes, with no manual steps?
- **Recovery.** If a node crashes mid-run, can you restart just that part?
- **The unknown obstacle.** Your map will not match the arena. Test with
  obstacles that are not in the map.
- **Lighting.** Marker detection that works in your lab may fail under
  different lights. Test in varied conditions.
- **Everyone can run it.** If only one person can start the robot, you have a
  single point of failure who might be getting coffee.

### Strategy

**Get Level 1 working end to end first.** A robot that reliably crosses the
arena scores more than a half-finished manipulation pipeline.

**Make it robust before making it clever.** A slow, reliable run beats a fast
run that fails on attempt one.

**Record everything.** Bag every practice run. When something goes wrong you
will have the data.

**Commit often.** Being able to `git checkout` back to the version that worked
an hour ago is worth more on the day than any single feature.

## On the day

### Format

Each team gets multiple attempts. The best attempt counts.

Between attempts you may change code, re-map, and re-tune. Use the time — the
first attempt is reconnaissance.

### Rules

- The robot must run **autonomously**. Manual interactions are permitted and
  penalised.
- The arena may differ from what you mapped. Expect it to.
- Safety first: if a robot is about to hurt someone or damage itself, stop it.
  A stopped run costs points; a broken robot costs the weekend.

### Judging

A referee records collisions and manual interactions. The scoring node records
detections and time. Both go into the final score.

Disputes are settled by the organisers. This is a course, not a world
championship — if a rule turns out to be unfair, it gets fixed rather than
enforced.

## Ideas to go further

If you finish early, the source courses suggest plenty:

- **Full coverage** — traverse every reachable part of the arena, not just a
  path through it.
- **Frontier exploration** — explore an arena you have no map of at all.
- **Keep-out zones and speed zones** — use Nav2 costmap filters to mark areas
  the robot must avoid or must slow down in.
- **Multi-robot** — two robots sharing what they find.
- **Custom detection** — train a model on the actual objects in the arena
  ([session 4](04-perception.md)).
- **Docking** — end the run by driving precisely onto a charging station using
  a marker.

## Further reading

- All eight sessions: [1](01-system-hardware.md) · [2](02-ros2.md) ·
  [3](03-sensors-tf.md) · [4](04-perception.md) ·
  [5](05-mapping-localization.md) · [6](06-navigation.md) ·
  [7](07-autonomous-decisions.md) · [8](08-integration.md)
- [Nav2 keep-out filter](https://docs.nav2.org/jazzy/configuration_and_development/configuration_guide/core_servers/costmap_2d/costmap_filters/keepout_filter/)
- [Nav2 tutorials](https://docs.nav2.org/jazzy/tutorials/)
- Your [platform track](../platforms/index.md)
