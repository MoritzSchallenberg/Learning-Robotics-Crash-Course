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
A workspace with a `perception_demo` package containing a node template
`aruco_node.py` with the subscriber and publisher already wired, and
`# TODO` comments marking exactly where detection code goes — and a
running, calibrated camera topic.

### Steps
1. `ros2 launch perception_demo camera.launch.yaml`
2. Confirm the image: add an `Image` display in RViz on `/camera/image_raw`.
3. Open `aruco_node.py`; fill in the two `# TODO` blocks: create the
   detector, call `detectMarkers`.
4. Build: `colcon build --packages-select perception_demo`.
5. Run: `ros2 run perception_demo aruco_node`.
6. Hold a printed marker in front of the camera.
7. Confirm in a second terminal: `ros2 topic echo /detected_marker_id`.

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
