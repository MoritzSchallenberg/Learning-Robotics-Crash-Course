# 4. Perception and Object Detection

:::{admonition} Session 4
:class: note

Wednesday, 14 October 2026, 17:35 – 19:00 (85 minutes)
:::

{{ common }}

A camera gives you a grid of coloured pixels. Turning that into "there is a
marker 2.1 metres ahead, slightly left" is perception. Tonight's core is the
smallest complete version of that pipeline: an image message, OpenCV, a
fiducial marker, and a published result.

This session has four deeper chapters. They are **not** part of tonight's 85
minutes — they exist so you can go further afterwards, or prepare beforehand.

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

{{ optional }} Preparation / reference — not required to complete tonight's
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

## Tonight

**Learning objectives** — by 19:00 you can:

1. explain the difference between *detecting* something and *localizing*
   it;
2. process a camera image inside a ROS 2 node with OpenCV;
3. detect a fiducial marker and publish where it is as a ROS 2 message.

**Visible result of the evening**: your node draws a box around a marker in
a live image and prints the marker's ID to the terminal, published as a ROS
2 topic another node could subscribe to.

**Preparation** — before arriving:

- [Session 3](../03-sensors-tf.md) completed.
- A **calibrated** camera stream already running — either the simulator, or
  a webcam calibrated in advance using
  [Camera calibration](camera-calibration.md). Calibrating during the
  session eats the entire 85 minutes and is not part of tonight.
- Printed ArUco markers, dictionary `DICT_6X6_50` (your facilitator
  provides these).

## Run sheet (85 minutes)

```{list-table}
:header-rows: 1
:widths: 16 20 64
:class: lrcc-runsheet

* - Time
  - Block
  - Content
* - 17:35–17:45
  - Opening
  - Recap TF; today a camera image becomes a position, using the same TF
    machinery
* - 17:45–18:05
  - Theory {{ core }}
  - Image messages, `cv_bridge`, detection vs. localization
* - 18:05–18:15
  - Demonstration {{ core }}
  - Live: detect a marker, watch its TF frame appear
* - 18:15–18:50
  - Practical task {{ core }}
  - Detect a marker and publish the result
* - 18:50–19:00
  - Wrap-up
  - Confirm detections together; preview session 5
```

## Theory

{{ core }}

### Detection versus localization

Hold on to this distinction — it is the point of the whole session.

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

## Practical task

### Goal
Detect an ArUco marker in a live camera stream, draw a box around it, and
publish the detected marker ID on a ROS 2 topic.

### Starting point
A pre-built workspace with a `perception_demo` package containing a node
template `aruco_node.py` with the subscriber and publisher already wired,
and `# TODO` comments marking exactly where detection code goes — and a
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

### Expected result
The marker is outlined in the published annotated image, and its ID is
printed every time `ros2 topic echo /detected_marker_id` receives a message.

### Verification
```bash
ros2 topic hz /detected_marker_id
```
Publishes at a steady rate whenever a marker is visible, and stops publishing
new IDs when it is removed from view (the node should not report a marker
that is not there).

### Common problems
- **No detections, no errors** — wrong dictionary, or the image topic name
  in the node does not match the camera's actual topic
  (`ros2 topic list` to check).
- **Detections flicker on and off** at the edge of the frame — expected;
  this is exactly why session 5's mapping task needs the position to be
  *remembered*, not just detected once.
- **`cv_bridge` import error** — the workspace was not sourced, or
  `cv_bridge` was not installed for your ROS 2 distribution.

### Extension

{{ optional }}

Publish the detected marker's position as a TF frame (see
[fiducial markers in depth](fiducial-markers.md#a-tf-listener-for-a-detected-marker))
so that `ros2 run tf2_ros tf2_echo base_link <marker_frame>` gives you a
distance and direction, not just an ID.

## Simulation fallback

{{ simulation }}

Print an ArUco marker on paper and hold it in front of any webcam — the
detection code is identical whether the image comes from a real robot
camera or a laptop webcam. If no camera is available at all, use a static
test image saved as a file and read it with `cv2.imread()` instead of
subscribing to a topic; everything downstream of `detectMarkers` is
unchanged.

## Common mistakes

**Detection works on a still image but not live.** Motion blur — reduce
exposure time, slow down, or improve lighting.

**Poses look plausible but are numerically wrong.** Usually a calibration or
marker-size problem — see [camera calibration](camera-calibration.md) and
the size warning in [fiducial markers](fiducial-markers.md).

## Transition to session 5

Tonight a marker's position existed only while it was visible. Next week you
build a **map** that remembers the world once and localize the robot inside
it — [Mapping and Localization](../05-mapping-localization.md).

## Further reading

- [OpenCV documentation](https://docs.opencv.org/) and the
  [ArUco tutorial](https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html)
- [vision_msgs](https://github.com/ros-perception/vision_msgs)
- The deeper chapters above: [camera calibration](camera-calibration.md) ·
  [fiducial markers](fiducial-markers.md) ·
  [object detection](object-detection.md) · [data labeling](data-labeling.md)
