# 4. Perception and Object Detection

{{ common }}

## Module overview

A camera gives you a grid of coloured pixels. **Perception** is turning
that into "there is a marker 2.1 metres ahead, slightly left" — an image
message, OpenCV, a fiducial marker (or a trained detector), and a
published result.

**The problem it solves**: none of a robot's later decisions — navigate
here, grasp that, report this — can happen until *something* in the raw
sensor stream has been turned into a named, located thing. Perception is
that turning point.

**Where it sits in the system**: right after [module 3's](../03-sensors-tf.md)
sensor and TF work, and right before
[module 5's](../05-mapping-localization.md) mapping and
[module 7's](../07-autonomous-decisions.md) mission logic, both of which
consume a detected object's pose rather than raw pixels.

**Needs**: [module 2](../02-ros2.md) (nodes, topics, your own controller)
and [module 3](../03-sensors-tf.md) (TF frames, since a detection is
useless without a frame to place it in).

**Leads into**: [module 5](../05-mapping-localization.md) uses a detected
marker's pose the same way it uses any other localization input;
[module 7](../07-autonomous-decisions.md) uses this module's own
practical task's detector directly inside its mission state machine.

## Learning objectives

By the end of this module you can:

1. explain the difference between *detecting* something and *localizing*
   it;
2. process a camera image inside a ROS 2 node with OpenCV;
3. detect a fiducial marker and publish where it is as a ROS 2 message;
4. name at least one deeper technique (calibration, a trained detector,
   or data labeling) well enough to know when you would reach for it.

## How the complete system fits together

```{figure} ../../_static/images/diagrams/05-perception-pipeline.svg
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
[module 2's](../02-ros2.md) topics and nodes,
[module 3's](../03-sensors-tf.md) TF frames — perception does not
introduce a new communication mechanism, only a new kind of processing
inside a node you already know how to write.

## How ALeRT uses this topic

{{ alert }} {{ documented }}

Spot's gripper camera feeds ArUco detection, red-line HSV detection, and
(with the Hazmat exercise) trained-model detection via YOLO/OpenVINO —
see the [platform page](../../platforms/alert-spot.md#image-processing)
for the exact tutorials. **Typical team task**: pointing the gripper
camera at a target before a manipulation attempt, since Spot's arm needs
a located object, not just a detected one. **Known peculiarity**:
{{ unverified }} the onboard compute may not have a usable GPU, which is
why the team uses OpenVINO for CPU inference rather than assuming a GPU
is available. **Verification status**: {{ simulation }} confirmed in
Webots; the physical-hardware inference performance is not independently
re-verified by this course.

## How Carologistics uses this topic

{{ carologistics }} {{ documented }}

Robotino's vision stack includes a "Tag vision" node for ArUco-based
machine identification and an "Object tracking" node using YOLOv8-nano
with triangulation for workpieces — see the [platform
page](../../platforms/carologistics-robotino.md#software-stack).
**Typical team task**: identifying a production machine's exact position
and side from its ArUco tag before docking — precision perception feeding
a precision docking manoeuvre. **Known peculiarity**:
{{ unverified }} the team also researches **markerless** machine
detection (`ros2-markerless-mps`), since the exploration phase of a
competition run is scored on speed and reading a marker up close costs
time. **Verification status**: {{ documented }} via the team wiki and
repository metadata cited on the platform page; exact model weights and
calibration parameters are `Not documented` publicly.

## ALeRT and Carologistics compared

```{list-table}
:header-rows: 1
:widths: 22 26 26 26

* - Aspect
  - ALeRT / Spot
  - Carologistics / Robotino
  - Shared principle
* - Environment
  - Cluttered, changeable rescue arena
  - Structured, mostly static factory floor
  - Both still calibrate once, detect continuously
* - Primary marker use
  - ArUco on the gripper camera, for manipulation targets
  - ArUco tags on machines, for docking precision
  - Detection → pose → TF, the same three steps
* - Beyond markers
  - Red-line HSV detection; Hazmat sign detection via YOLO
  - Markerless machine detection (research), workpiece tracking via YOLO
  - Both push past markers once markers alone are not enough
* - Speed vs. precision
  - {{ unverified }} not a scored constraint in the same way
  - Exploration-phase detection is scored on speed
  - {{ unverified }} — no reliable cross-team comparison available
```

## Core learning path

```text
1. Perception pipeline
2. Practical perception exercise
```

That is this module's roughly 80–100 minute core learning time. The four
deeper chapters below (camera calibration, fiducial markers in depth,
object detection with YOLO, data labeling), **Interesting videos** and
**Continue learning** are worthwhile afterwards but not required for the
core path — pick them up in whichever order matches what you actually
need next.

## Subtopics

::::{grid} 1 1 2 2
:gutter: 2

:::{grid-item-card} Perception pipeline
:link: perception-pipeline
:link-type: doc

{{ core }} Detection vs. localization, OpenCV in a ROS 2 node, and
generating your own ArUco marker.
:::

:::{grid-item-card} Practical perception exercise
:link: practical-exercise
:link-type: doc

{{ core }} This module's practical task: detect a marker, publish its ID,
and this module's Try it on Spot section.
:::

:::{grid-item-card} Camera calibration
:link: camera-calibration
:link-type: doc

{{ optional }} Preparation / reference — not required to complete the
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

- [Module 3](../03-sensors-tf.md) completed.
- A **calibrated** camera stream already running — either the simulator, or
  a webcam calibrated in advance using
  [Camera calibration](camera-calibration.md). Calibrating on the fly is
  not part of the core task; do it beforehand.
- One or more printed ArUco markers, dictionary `DICT_6X6_50` — see
  [Perception pipeline](perception-pipeline.md) for how to generate and
  print your own.

## Connection to the next module

This module produced a marker position that existed only while the
marker was visible. [Module 5](../05-mapping-localization.md) builds a
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
