# Perception and Object Detection

## Overview

A camera gives you a grid of coloured pixels. **Perception** is turning
that into "there is a marker 2.1 metres ahead, slightly left" — an image
message, OpenCV, a fiducial marker (or a trained detector), and a
published result.

**The problem it solves**: none of a robot's later decisions — navigate
here, grasp that, report this — can happen until *something* in the raw
sensor stream has been turned into a named, located thing. Perception is
that turning point.

**Where it sits in the system**: right after [Sensors and Coordinate Frames's](../sensors-frames/index.md)
sensor and TF work, and right before
[Mapping and World Models's](../mapping-world-models/index.md) mapping and
[Autonomous Decision-Making's](../decision-making/index.md) mission logic, both of which
consume a detected object's pose rather than raw pixels.

**Needs**: [ROS 2](../ros2/index.md) (nodes, topics, your own controller)
and [Sensors and Coordinate Frames](../sensors-frames/index.md) (TF frames, since a detection is
useless without a frame to place it in).

**Leads into**: [Mapping and World Models](../mapping-world-models/index.md) uses a detected
marker's pose the same way it uses any other localization input;
[Autonomous Decision-Making](../decision-making/index.md) uses this topic's own
practical task's detector directly inside its mission state machine.

## Learning objectives

By the end of this topic you can:

1. explain the difference between *detecting* something and *localizing*
   it;
2. process a camera image inside a ROS 2 node with OpenCV;
3. detect a fiducial marker and publish where it is as a ROS 2 message;
4. name at least one deeper technique (calibration, a trained detector,
   or data labeling) well enough to know when you would reach for it.

## How the complete system fits together

```{figure} ../_static/images/diagrams/perception-pipeline.svg
:alt: A left to right pipeline: Camera produces an Image message, which is rectified using CameraInfo from calibration, then passed to a Detector such as ArUco or YOLO, producing a Detection message, which combined with a TF transform gives a Pose in the map frame.
:width: 100%

Detection gives pixels; only calibration plus a known size or depth turns
it into a usable position.
```

A `sensor_msgs/msg/Image` topic flows through a rectification step
(using `CameraInfo` from calibration), into a detector — ArUco, AprilTag,
colour thresholding or a trained YOLO model — producing a detection,
which combined with a TF transform gives a usable pose in the `map`
frame. Every ROS 2 component involved is one you already know:
[ROS 2's](../ros2/index.md) topics and nodes,
[Sensors and Coordinate Frames's](../sensors-frames/index.md) TF frames — perception does not
introduce a new communication mechanism, only a new kind of processing
inside a node you already know how to write.

## How ALeRT uses this topic

{{ alert }} {{ documented }}

Spot's gripper camera feeds ArUco detection, red-line HSV detection, and
(with the Hazmat exercise) trained-model detection via YOLO/OpenVINO —
see the [platform page](../platforms/spot/index.md#image-processing)
for the exact tutorials. **Typical team task**: pointing the gripper
camera at a target before a manipulation attempt, since Spot's arm needs
a located object, not just a detected one. **Known peculiarity**:
{{ unverified }} the onboard compute may not have a usable GPU, which is
why the team uses OpenVINO for CPU inference rather than assuming a GPU
is available. **Verification status**: {{ simulation }} confirmed in
Webots; the physical-hardware inference performance is not independently
re-verified by this site.

## Working through this topic

```text
1. Perception pipeline
2. Practical perception exercise
```

The four deeper chapters below (camera calibration, fiducial markers in
depth, object detection with YOLO, data labeling), **Interesting videos**
and **Continue learning** are worthwhile afterwards, but are not required
to move on to the next topic — pick them up in whichever order matches
what you actually need next.

## Subtopics

::::{grid} 1 1 2 2
:gutter: 2

:::{grid-item-card} Perception pipeline
:link: perception-pipeline
:link-type: doc

{{ foundation }} Detection vs. localization, OpenCV in a ROS 2 node, and
generating your own ArUco marker.
:::

:::{grid-item-card} Practical perception exercise
:link: practical-exercise
:link-type: doc

{{ foundation }} This topic's practical task: detect a marker, publish its ID,
and this topic's Try it on Spot section.
:::

:::{grid-item-card} Camera calibration
:link: camera-calibration
:link-type: doc

{{ intermediate }} Preparation / reference — not required to complete the
core task with a pre-calibrated camera.
:::

:::{grid-item-card} Fiducial markers in depth
:link: fiducial-markers
:link-type: doc

{{ advanced }} AprilTag, colour-based detection, the full ArUco node.
:::

:::{grid-item-card} Object detection with YOLO
:link: object-detection
:link-type: doc

{{ advanced }} Neural-network detection, GPU/CPU inference, custom
training.
:::

:::{grid-item-card} Data labeling
:link: data-labeling
:link-type: doc

{{ advanced }} How to label a dataset well enough to train on.
:::

:::{grid-item-card} Interesting videos
:link: videos
:link-type: doc

One carefully checked video recommendation.
:::

:::{grid-item-card} Continue learning
:link: continue-learning
:link-type: doc

Image transport, marker boards, occlusion, depth, tracking, evaluation,
deployment and cross-sensor checks.
:::

::::

## Prerequisites

- [Sensors and Coordinate Frames](../sensors-frames/index.md) completed.
- A **calibrated** camera stream already running — either the simulator, or
  a webcam calibrated in advance using
  [Camera calibration](camera-calibration.md). Calibrating on the fly is
  not part of the core task; do it beforehand.
- One or more printed ArUco markers, dictionary `DICT_6X6_50` — see
  [Perception pipeline](perception-pipeline.md) for how to generate and
  print your own.

## Connection to the next topic

This topic produced a marker position that existed only while the
marker was visible. [Mapping and World Models](../mapping-world-models/index.md) builds a
**map** that remembers the world once and localizes the robot inside it.

## Further reading

- [OpenCV documentation](https://docs.opencv.org/) and the
  [ArUco tutorial](https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html)
- [vision_msgs](https://github.com/ros-perception/vision_msgs)

```{toctree}
:maxdepth: 1
:hidden:

perception-pipeline
practical-exercise
camera-calibration
fiducial-markers
object-detection
data-labeling
videos
continue-learning
```
