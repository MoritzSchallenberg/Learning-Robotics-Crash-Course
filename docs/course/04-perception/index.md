# 4. Perception and Object Detection

{{ common }}

A camera gives you a grid of coloured pixels. Turning that into "there is a
marker 2.1 metres ahead, slightly left" is perception. This module's core is
the smallest complete version of that pipeline: an image message, OpenCV, a
fiducial marker, and a published result.

This module has four deeper chapters, listed below. They are **not** part
of the core task — they exist so you can go further afterwards, or prepare
beforehand.

```{toctree}
:maxdepth: 1
:hidden:

camera-calibration
fiducial-markers
object-detection
data-labeling
```

::::{grid} 1 1 2 2
:gutter: 2

:::{grid-item-card} Camera calibration
:link: camera-calibration
:link-type: doc

{{ optional }} Preparation / reference — not required to complete the core
task with a pre-calibrated camera.
:::

:::{grid-item-card} Fiducial markers in depth
:link: fiducial-markers
:link-type: doc

{{ advanced }} AprilTag, colour-based detection, the full ArUco node.
:::

:::{grid-item-card} Object detection with YOLO
:link: object-detection
:link-type: doc

{{ advanced }} Neural-network detection, GPU/CPU inference, custom training.
:::

:::{grid-item-card} Data labeling
:link: data-labeling
:link-type: doc

{{ advanced }} How to label a dataset well enough to train on.
:::

::::

## Overview

You will learn what separates *detecting* something in an image from
*localizing* it in the world, process a camera image inside a ROS 2 node
with OpenCV, and detect a fiducial marker, publishing its ID as a ROS 2
message.

## Learning objectives

By the end of this module you can:

1. explain the difference between *detecting* something and *localizing*
   it;
2. process a camera image inside a ROS 2 node with OpenCV;
3. detect a fiducial marker and publish where it is as a ROS 2 message.

## Prerequisites

- [Module 3](../03-sensors-tf.md) completed.
- A **calibrated** camera stream already running — either the simulator, or
  a webcam calibrated in advance using
  [Camera calibration](camera-calibration.md). Calibrating on the fly is
  not part of the core task; do it beforehand.
- One or more printed ArUco markers, dictionary `DICT_6X6_50` — see the
  guided example below for how to generate and print your own.

## Core concepts

### Detection versus localization

Hold on to this distinction — it is the point of the whole module.

**Detection** answers *what*, in image coordinates: "there is a marker, in a
box from pixel (120, 240) to (200, 310)." On its own it cannot tell a robot
where to drive.

**Localization** answers *where*, in the world: "there is a marker at
(1.8, 0.4, 0.7) in the `map` frame." This is what the robot needs, and it
needs more than the image alone — a calibrated camera, and either depth, a
known object size, or a known surface.

```{figure} ../../_static/images/diagrams/05-perception-pipeline.svg
:alt: A left to right pipeline: Camera produces an Image message, which is rectified using CameraInfo from calibration, then passed to a Detector such as ArUco or YOLO, producing a Detection message, which combined with a TF transform gives a Pose in the map frame.
:width: 100%

Detection gives pixels; only calibration plus a known size or depth turns it
into a usable position.
```

Fiducial markers are popular precisely because they collapse this: a marker
of known physical size gives full 6D pose from a single image, with the size
supplying the missing depth information for free.

### OpenCV in a ROS 2 node

OpenCV works on NumPy arrays; ROS 2 uses `sensor_msgs/msg/Image`.
`cv_bridge` converts between them:

```python
from cv_bridge import CvBridge

self.bridge = CvBridge()

def image_callback(self, msg):
    frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
    # ... process frame with OpenCV ...
    self.publisher.publish(self.bridge.cv2_to_imgmsg(frame, 'bgr8'))
```

:::{tip}
Publish the annotated image on a topic and view it in RViz rather than
`cv2.imshow()`. It works over SSH, it works on the robot, and it can be
recorded in a rosbag.
:::

### Detecting an ArUco marker

```python
import cv2

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)
detector = cv2.aruco.ArucoDetector(dictionary)

corners, ids, _rejected = detector.detectMarkers(frame)
if ids is not None:
    cv2.aruco.drawDetectedMarkers(frame, corners, ids)
```

:::{warning}
The dictionary must match the markers you printed. `DICT_6X6_50` will not
detect a `DICT_4X4_50` marker, and there is no error — you simply get no
detections. Check which dictionary your markers came from.
:::

## Guided example

Generate and print your own ArUco marker using the same OpenCV library the
detector above uses, so you know exactly which dictionary and ID you are
working with:

```python
import cv2

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)
marker_image = cv2.aruco.generateImageMarker(dictionary, 0, 400)  # marker ID 0, 400px
cv2.imwrite('marker_0.png', marker_image)
```

Print `marker_0.png` at a convenient size (10 cm square is a reasonable
default for a desk-scale test), and repeat with a different ID for a second
marker.

Then confirm detection works before wiring it into a full node — run the
same three lines interactively in a Python shell against a single captured
frame, or against the live topic:

```bash
ros2 run usb_cam usb_cam_node_exe   # or your platform's camera driver
ros2 topic echo /image_raw --once   # confirm the topic is actually publishing
```

If `detectMarkers` finds nothing on a frame you can see the marker in
clearly, the dictionary is the first thing to check — printed markers are
easy to generate in the wrong dictionary by mistake.

## Practical task

### Goal
Detect an ArUco marker in a live camera stream, draw a box around it, and
publish the detected marker ID on a ROS 2 topic.

### Starting point
A new package (call it `perception_demo`) with an empty node file
`aruco_node.py`, and a running, calibrated camera topic — either your
platform's real driver, or [Webots'](../../platforms/simulation.md)
simulated camera. This module's Guided example above already gave you
every piece of code the node needs (`cv_bridge` conversion, the ArUco
detector, `generateImageMarker`); this task is wiring them together into
one subscriber-callback node, not a fill-in-the-blank template.

### Steps
1. Create the package: `ros2 pkg create --build-type ament_python
   perception_demo`, add `rclpy`, `sensor_msgs`, `std_msgs` and
   `cv_bridge` as `exec_depend` entries in `package.xml`.
2. In `aruco_node.py`, subscribe to your camera's image topic (confirm
   the exact name with `ros2 topic list` first — do not assume
   `/camera/image_raw`), convert each frame with `cv_bridge`, and run the
   `detectMarkers` call from the Guided example inside the callback.
3. Add a publisher for `/detected_marker_id`
   (`std_msgs/msg/Int32`, or a custom type from
   [module 2's Continue learning](../02-ros2.md#continue-learning) if
   you want to publish more than an ID) and publish whenever a marker is
   found.
4. Register the node as a console script in `setup.py`, then build:
   `colcon build --packages-select perception_demo`.
5. Run it: `ros2 run perception_demo aruco_node`.
6. Confirm the image is actually arriving first — add an `Image` display
   in RViz on your camera's real topic name, or `ros2 topic hz` it.
7. Hold a printed marker (from the Guided example) in front of the
   camera.
8. Confirm in a second terminal: `ros2 topic echo /detected_marker_id`.

## Expected result

The marker is outlined in the published annotated image, and its ID is
printed every time `ros2 topic echo /detected_marker_id` receives a message.

## Verification

```bash
ros2 topic hz /detected_marker_id
```

Publishes at a steady rate whenever a marker is visible, and stops
publishing new IDs when it is removed from view (the node should not
report a marker that is not there).

## Common problems

- **No detections, no errors** — wrong dictionary, or the image topic name
  in the node does not match the camera's actual topic
  (`ros2 topic list` to check).
- **Detections flicker on and off** at the edge of the frame — expected;
  this is exactly why module 5's mapping task needs the position to be
  *remembered*, not just detected once.
- **`cv_bridge` import error** — the workspace was not sourced, or
  `cv_bridge` was not installed for your ROS 2 distribution.
- **Detection works on a still image but not live.** Motion blur — reduce
  exposure time, slow down, or improve lighting.
- **Poses look plausible but are numerically wrong.** Usually a
  calibration or marker-size problem — see
  [camera calibration](camera-calibration.md) and the size warning in
  [fiducial markers](fiducial-markers.md).

## Optional extensions

{{ optional }}

Publish the detected marker's position as a TF frame (see
[fiducial markers in depth](fiducial-markers.md#a-tf-listener-for-a-detected-marker))
so that `ros2 run tf2_ros tf2_echo base_link <marker_frame>` gives you a
distance and direction, not just an ID.

No camera available at all? Use a static test image saved as a file and
read it with `cv2.imread()` instead of subscribing to a topic —
everything downstream of `detectMarkers` is unchanged. A photo of your
printed marker from the guided example works as this test image.

**Test under changed lighting.** Dim the room, or point a lamp directly
at the marker to create glare, and re-run your practical task's node
without changing any code. Record at what point detection starts missing
frames it caught easily before — a concrete first data point for
[this module's occlusion-handling
topic](#handling-occlusion) in Continue learning, since inconsistent
lighting produces the same kind of intermittent "sometimes not detected"
symptom as physical occlusion does.

## Try it on Spot

{{ alert }} {{ spotsim }}

The [platform page](../../platforms/alert-spot.md#image-processing)
already names the two ALeRT tutorial exercises this module's techniques
map onto; do them yourself here, against Webots Spot:

1. Subscribe to the gripper camera
   (`/SpotArm/gripper_camera/image_color`) and confirm it with an `Image`
   display in RViz before writing any code — the same "check the data
   exists first" habit from this module's own Common problems section.
2. Run this module's ArUco detector against that subscription instead of
   a generic webcam topic. The simulation uses the same `DICT_6X6_50`
   dictionary as this module's guided example, so no code changes to the
   detector itself should be needed — only the topic name.
3. Publish the detected marker ID, exactly as in this module's practical
   task.
4. **Optional**: also publish the marker's pose as a TF frame (this
   module's [Optional
   extensions](index.md#optional-extensions)), using the gripper camera's
   real calibration rather than an assumed one.
5. **Optional**: detect the red line on the floor with an HSV threshold
   ([platform page's line-following
   exercise](../../platforms/alert-spot.md#line-following)) and publish
   the thresholded mask as a debug `Image` topic — a visible way to check
   your HSV range is actually right, rather than guessing from numbers
   alone.

:::{warning}
Turning a detection into a **movement command** (driving toward a
detected marker or line) is a simulation-only exercise. Do not send
`cmd_vel` commands derived from live image processing on a physical
Spot outside a supervised exercise — see
[module 7](../07-autonomous-decisions.md#try-it-on-spot).
:::

**Verification**: `ros2 topic echo /detected_marker_id` reports a value
only while a marker is actually visible in the gripper camera's real
field of view, not the field of view you assumed it had.

## Continue learning

This module's deeper chapters already follow one connected path — calibrate
the camera ([camera calibration](camera-calibration.md)), detect something
in the image ([fiducial markers](fiducial-markers.md) or
[object detection](object-detection.md)), then turn that detection into a
pose and a TF frame (this page's Optional extensions, and
[module 3](../03-sensors-tf.md#core-concepts)). The topics below extend that
same path rather than starting a new one.

:::{dropdown} Image transport and compressed streams — Next step
:icon: light-bulb

**What it is.** `image_transport` republishes an `Image` topic in
alternative encodings — most usefully `compressed`, a JPEG/PNG-encoded
version of the same stream — subscribed to with the same API, just a
different topic suffix (`/image_raw/compressed`).

**Why it matters.** A raw `Image` topic over Wi-Fi to a robot
([networking prerequisite](../../prerequisites/networking.md)) can saturate
the link almost by itself; compressed transport is often the difference
between a usable remote view and a stalled one.

**Needs.** This module's practical task.

**Try it.** Subscribe to `/camera/image_raw/compressed` instead of the raw
topic, decode it with `cv_bridge.compressed_imgmsg_to_cv2`, and compare
`ros2 topic bw` on both topics.

**Check.** The compressed topic's bandwidth (`ros2 topic bw`) is visibly
lower than the raw topic's, for the same visual content.

**Read more.** [image_transport](https://github.com/ros-perception/image_common)
:::

:::{dropdown} Marker boards and multi-marker setups — Next step
:icon: light-bulb

**What it is.** A **board** of several ArUco/AprilTag markers in one known
fixed layout — OpenCV's `cv2.aruco.Board` — gives a more accurate,
more occlusion-tolerant pose than one single marker, because it can
estimate a pose from partial visibility of the set.

**Why it matters.** A single marker's pose becomes unreliable at a
shallow viewing angle or partial occlusion; a board keeps working as long
as *some* of its markers are visible.

**Needs.** This module's practical task and printed markers.

**Try it.** Print three markers in a known, measured arrangement, define
a `cv2.aruco.Board` with their positions, and estimate the board's pose
with only two of the three markers visible to the camera.

**Check.** The board pose estimate remains stable (does not jump wildly)
as you cover one of the three markers.

**Read more.** [OpenCV: ArUco board
detection](https://docs.opencv.org/4.x/db/da9/tutorial_aruco_board_detection.html)
:::

(handling-occlusion)=
:::{dropdown} Handling occlusion — Intermediate
:icon: light-bulb

**What it is.** What a detector should do when its target is partially or
fully blocked from view — briefly missing a detection is normal and
expected, not a bug to "fix" by lowering your detection threshold until
false positives appear instead.

**Why it matters.** This module's own Common problems section already notes
detections "flicker on and off at the edge of the frame" — occlusion
handling is the general version of that: deciding how many missed frames
before you treat a target as genuinely lost, versus temporarily hidden.

**Needs.** This module's practical task.

**Try it.** Add a small state variable to `aruco_node.py` that only reports
"marker lost" after N consecutive frames with no detection (rather than
immediately on the first missed frame), and test it by briefly waving a
hand in front of the camera.

**Check.** A brief, sub-second occlusion no longer triggers a "lost"
report, while genuinely removing the marker still does after N frames.

**Read more.** [Module 7: state
machines](../07-autonomous-decisions.md#core-concepts) — the same
debounce pattern applies to any noisy binary signal, not just detections.
:::

:::{dropdown} Depth cameras and point clouds — Intermediate
:icon: light-bulb

**What it is.** A depth camera (e.g. an Intel RealSense) publishes both a
color `Image` and a `PointCloud2` (or a raw depth `Image`) — depth solves
directly the "how far away is this pixel" problem that a fiducial marker's
known size solves indirectly.

**Why it matters.** Not every object worth detecting is a marker with a
known size; depth gives you 3D position for *any* detected pixel region,
marker or not.

**Needs.** [PointCloud2](../03-sensors-tf.md#advanced-topics)
(module 3's advanced topics) and a depth camera, real or simulated.

**Try it.** {{ unverified }} — subscribe to a depth camera's `Image` topic
alongside its color image, and read the depth value at the pixel
coordinates of one of your ArUco detections from this module's practical
task.

**Check.** The depth-derived distance to the marker is within a plausible
range of a distance you measure by hand.

**Read more.** [RealSense ROS
wrapper](https://github.com/IntelRealSense/realsense-ros)
:::

:::{dropdown} Tracking a detection across frames — Intermediate
:icon: light-bulb

**What it is.** Assigning a stable ID to the *same* object across
consecutive frames — object **tracking** — rather than treating every
frame's detection as unrelated to the last, which is what this module's
practical task does today.

**Why it matters.** Without tracking, a target that flickers between
"detected" and "not detected" for one frame looks like two different
objects, one disappearing and one appearing; a mission that needs to
"follow this object" needs it to stay the same object.

**Needs.** This module's practical task, or
[object detection](object-detection.md).

**Try it.** {{ unverified }} — implement the simplest possible tracker: if
a new detection's center is within some pixel distance of the previous
frame's detection, treat it as the same tracked object and keep its ID;
otherwise assign a new one.

**Check.** A marker moved slowly across the frame keeps the same tracked
ID throughout; a marker that disappears and a different one that appears
elsewhere get different IDs.

**Read more.** [ByteTrack](https://github.com/ifzhang/ByteTrack) and
similar are the standard approach for a real deployment — worth reading
once your own simple version works.
:::

:::{dropdown} Evaluating a detector: precision, recall, confusion matrix — Intermediate
:icon: light-bulb

**What it is.** **Precision** — of everything the detector flagged, how
much was actually correct; **recall** — of everything that was actually
there, how much did it find; a **confusion matrix** lays both out per
class, showing exactly which classes get mistaken for which.

**Why it matters.** "The model works" is not a number. A detector that
never misses a target but also flags a hundred wrong things
(low precision, high recall) fails differently — and needs a different
fix — than one that only ever reports confident, correct detections but
misses half the real targets (high precision, low recall).

**Needs.** [Object detection](object-detection.md) and
[data labeling](data-labeling.md) completed — you need both a trained
model and a labelled validation set to evaluate against.

**Try it.** Run your trained YOLO model's built-in validation
(`yolo val model=<your_model> data=<your_data.yaml>`) and read its
reported precision, recall and confusion matrix for your classes.

**Check.** You can state which of your classes the model confuses most
often, directly from the confusion matrix.

**Read more.** [Ultralytics: model
validation](https://docs.ultralytics.com/modes/val/)
:::

:::{dropdown} Deployment: CPU, GPU and edge devices — Advanced
:icon: light-bulb

**What it is.** The same trained model runs at very different speeds
depending on where it runs: a laptop CPU, a discrete GPU
([GPU acceleration](object-detection.md#gpu-acceleration)), or a small
edge accelerator (e.g. an NVIDIA Jetson) built into the robot itself —
each has a different latency/power/cost trade-off.

**Why it matters.** A model that hits 30 FPS on a development laptop's GPU
can drop to 2 FPS on the robot's actual onboard computer; deployment
target is a design decision, not an afterthought.

**Needs.** [Object detection's GPU
acceleration section](object-detection.md#gpu-acceleration).

**Try it.** Measure your trained model's inference time per frame on CPU
only, then again with GPU acceleration enabled (if available), and compute
the resulting frames-per-second for each.

**Check.** You have two concrete FPS numbers, CPU vs. GPU, from your own
measurement, not an assumed ratio.

**Read more.** [Ultralytics: model
export and deployment](https://docs.ultralytics.com/modes/export/)
:::

:::{dropdown} Sensor-crossing plausibility checks — Advanced
:icon: light-bulb

**What it is.** Cross-checking one sensor's result against a second,
independent sensor before acting on it — e.g. does a camera-detected
object's approximate distance roughly agree with what the LiDAR reports in
that direction — rather than trusting a single detection outright.

**Why it matters.** Every sensor can be wrong in its own specific way (a
camera can misclassify; a LiDAR cannot see glass); a mission-critical
decision — such as this course's own
[capstone project](../hackathon.md) reporting mission success — is more
trustworthy if two independent sensors agree, not just one.

**Needs.** Two independent sensors covering overlapping data — camera plus
LiDAR is the common case.

**Try it.** {{ unverified }} — for one ArUco detection from this module's
practical task, look up the LiDAR range in roughly the same direction (from
`/scan`) and compare it to the camera-derived distance to the marker.

**Check.** You can state both distances and whether they agree within a
sensible margin, or explain why they legitimately would not (e.g. the
LiDAR's beam missing the marker entirely).

**Read more.** [Module 6: costmaps built from multiple
sensors](../06-navigation.md#core-concepts) is the same principle applied
at the navigation layer.
:::

## Interesting videos

{{ optional }}

::::{grid} 1 1 1 1
:gutter: 2

:::{grid-item-card} Generate ArUco Markers for Detection and Pose Estimation with OpenCV in Python
:link: https://www.youtube.com/watch?v=sg1bVJBjbng

**Nicolai Nielsen · English · ~8 min**

Covers: generating ArUco markers with OpenCV and detecting them with pose
estimation — the same `cv2.aruco` API this module's guided example and
practical task use directly.

*Why watch it*: a second walkthrough of the exact `generateImageMarker`
and `detectMarkers` calls this module has you run, including the pose
estimation step this module's Optional extensions point toward.

*Compatibility*: conceptual and applicable to the OpenCV version this
course uses — verify the exact `cv2.aruco` function names against
[OpenCV's own ArUco
documentation](https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html)
if a name in the video looks unfamiliar, since the ArUco API has changed
across OpenCV versions.
:::

::::

:::{note}
This is deliberately one carefully checked video rather than a longer,
unverified list. If this link is ever dead or the content has moved, that
is a documentation bug worth reporting — see the [repository
README](https://github.com/MoritzSchallenberg/Learning-Robotics-Crash-Course).
:::

## Connection to the next module

This module produced a marker position that existed only while the marker
was visible. [Module 5](../05-mapping-localization.md) builds a **map** that
remembers the world once and localizes the robot inside it.

## Further reading

- [OpenCV documentation](https://docs.opencv.org/) and the
  [ArUco tutorial](https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html)
- [vision_msgs](https://github.com/ros-perception/vision_msgs)
- The deeper chapters above: [camera calibration](camera-calibration.md) ·
  [fiducial markers](fiducial-markers.md) ·
  [object detection](object-detection.md) · [data labeling](data-labeling.md)
