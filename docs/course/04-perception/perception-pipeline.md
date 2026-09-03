# Perception pipeline

{{ common }} {{ core }}

## What this topic is

The chain that turns pixels into a usable robot decision: an image
message, an OpenCV detector, and — critically — the distinction between
**detecting** something and **localizing** it.

## Why a robot needs it

**Detection** answers *what*, in image coordinates: "there is a marker,
in a box from pixel (120, 240) to (200, 310)." On its own it cannot tell
a robot where to drive. **Localization** answers *where*, in the world:
"there is a marker at (1.8, 0.4, 0.7) in the `map` frame." This is what
the robot needs, and it needs more than the image alone — a calibrated
camera, and either depth, a known object size, or a known surface. Hold
on to this distinction: it is the point of the whole module.

## How it works

```{figure} ../../_static/images/diagrams/05-perception-pipeline.svg
:alt: A left to right pipeline: Camera produces an Image message, which is rectified using CameraInfo from calibration, then passed to a Detector such as ArUco or YOLO, producing a Detection message, which combined with a TF transform gives a Pose in the map frame.
:width: 100%

Detection gives pixels; only calibration plus a known size or depth turns
it into a usable position.
```

Fiducial markers are popular precisely because they collapse this: a
marker of known physical size gives full 6D pose from a single image,
with the size supplying the missing depth information for free.

## Inputs and outputs

Input: a `sensor_msgs/msg/Image` topic. Output, at the end of the full
pipeline: a pose in a named TF frame — the same pattern
[module 3](../03-sensors-tf.md) already taught for sensor data generally,
applied specifically to a detected object.

## Small example: OpenCV in a ROS 2 node

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

## Try it yourself: generate and print your own marker

Generate and print your own ArUco marker using the same OpenCV library
the detector above uses, so you know exactly which dictionary and ID you
are working with:

```python
import cv2

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)
marker_image = cv2.aruco.generateImageMarker(dictionary, 0, 400)  # marker ID 0, 400px
cv2.imwrite('marker_0.png', marker_image)
```

Print `marker_0.png` at a convenient size (10 cm square is a reasonable
default for a desk-scale test), and repeat with a different ID for a
second marker.

Then confirm detection works before wiring it into a full node — run the
same three lines interactively in a Python shell against a single
captured frame, or against the live topic:

```bash
ros2 run usb_cam usb_cam_node_exe   # or your platform's camera driver
ros2 topic echo /image_raw --once   # confirm the topic is actually publishing
```

## Expected result

Two printed markers with known IDs, and a confirmed, live `Image` topic
you can subscribe to.

## Verification

If `detectMarkers` finds nothing on a frame you can see the marker in
clearly, the dictionary is the first thing to check — printed markers are
easy to generate in the wrong dictionary by mistake.

## How ALeRT applies it

{{ alert }} {{ simulation }} Spot's gripper camera feeds exactly this
pipeline in Webots, using the same `DICT_6X6_50` dictionary — see
[the practical exercise's Try it on Spot](practical-exercise.md#try-it-on-spot).

## How Carologistics applies it

{{ carologistics }} {{ unverified }} Robotino's vision stack (see the
[platform page](../../platforms/carologistics-robotino.md#software-stack))
includes a "Tag vision" node for ArUco-based machine identification and
an "Object tracking" node using YOLOv8-nano with triangulation — the same
detection/localization split this page teaches, at production scale. The
exact marker dictionary and camera calibration parameters used are not
documented in public repository READMEs at the time of writing.

## Common problems

- **No detections, no errors** — wrong dictionary, or the image topic
  name does not match the camera's actual topic (`ros2 topic list` to
  check).

## Next subtopic

[Practical perception exercise](practical-exercise.md) — wire this
pipeline into a real node that publishes a detected marker ID.
