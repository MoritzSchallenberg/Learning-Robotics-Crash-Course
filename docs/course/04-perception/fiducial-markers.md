# Fiducial markers in depth

{{ common }}

{{ advanced }} **Status: advanced reading.** [Session 4](index.md) core
task covers a minimal ArUco detector. This page goes further: AprilTag, the
full node with TF publishing, and colour-based detection for comparison.

## ArUco and AprilTag

A **fiducial marker** is a printed pattern designed to be found reliably and
identified uniquely. Because the pattern and its physical size are known, a
single camera image gives you the marker's full 6D pose.

**ArUco** — built into OpenCV, no extra dependency, several dictionaries.

**AprilTag** — a separate library, generally more robust at distance and
under poor lighting.

Both work the same way and are largely interchangeable for this course.

## ArUco with OpenCV

The complete node — [session 4](index.md) has you fill in the two marked
gaps; this is the finished version:

```python
#!/usr/bin/env python3

import cv2
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image


class ArucoDetector(Node):

    def __init__(self):
        super().__init__('aruco_detector')
        self.bridge = CvBridge()

        dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)
        self.detector = cv2.aruco.ArucoDetector(dictionary)

        self.subscription = self.create_subscription(
            Image, '/camera/image_raw', self.camera_callback, 10)
        self.publisher = self.create_publisher(Image, '/aruco_detections', 10)

    def camera_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        corners, ids, _rejected = self.detector.detectMarkers(frame)

        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            for marker_id in ids.flatten():
                self.get_logger().info(f'Detected marker {marker_id}')

        self.publisher.publish(self.bridge.cv2_to_imgmsg(frame, 'bgr8'))


def main():
    rclpy.init()
    node = ArucoDetector()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

:::{note}
The `cv2.aruco.ArucoDetector` class is the OpenCV 4.7+ API. Older code uses
`cv2.aruco.detectMarkers(frame, dictionary, parameters=...)` directly. If you
hit an `AttributeError`, check your OpenCV version with
`python3 -c "import cv2; print(cv2.__version__)"`.
:::

## AprilTag

{{ common }}

```bash
sudo apt install ros-$ROS_DISTRO-apriltag-ros ros-$ROS_DISTRO-image-pipeline
```

The AprilTag node needs a **rectified** image, which is what
[calibration](camera-calibration.md) enables:

```bash
ros2 run image_proc rectify_node --ros-args --remap image:=image_raw
```

Then configure the detector:

```yaml
launch:

- node:
    pkg: "apriltag_ros"
    exec: "apriltag_node"
    name: "apriltag_node"
    param:
    - name: "image_transport"
      value: "raw"
    - name: "family"
      value: "Standard41h12"
    - name: "size"
      value: 0.16          # tag edge length in metres -- MEASURE YOURS

    remap:
    - from: /image_rect
      to: /camera/image_raw
    - from: /camera_info
      to: /camera/camera_info
```

:::{danger}
`size` is the physical edge length of the tag in metres, and the computed
distance scales linearly with it. Get it wrong and every pose is wrong by
the same factor. Measure the printed tag rather than trusting the value it
was designed at — printers scale.

Which edge to measure depends on the family. For `Standard41h12` and
`Custom48h12`, measure the **inner** black edge, not the outer border. See
the [apriltag_ros README](https://github.com/christianrauch/apriltag_ros).
:::

The node publishes a TF frame per detected tag, named `<family>:<id>` — for
example `Standard41h12:7`. That means you can immediately ask TF2 where a
tag is relative to anything else:

```bash
ros2 run tf2_ros tf2_echo base_link Standard41h12:7
```

### A TF listener for a detected marker

Adapting the [session 3](../03-sensors-tf.md#advanced-looking-up-a-transform-from-code)
listener pattern to a marker:

```python
def timer_callback(self):
    try:
        t = self.tf_buffer.lookup_transform('base_link', 'Standard41h12:7', rclpy.time.Time())
    except TransformException as ex:
        self.get_logger().info(f'marker not currently visible: {ex}')
        return
    self.get_logger().info(
        f'marker at x={t.transform.translation.x:.2f} '
        f'y={t.transform.translation.y:.2f}')
```

## Colour detection with HSV

Finding "the red line on the floor" is much easier in **HSV** colour space
than in RGB, because hue stays roughly constant as lighting changes while
RGB values all shift together.

```python
import cv2
import numpy as np

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# Red wraps around the hue axis, so it needs two ranges
red_lower = np.array([170, 100, 100], dtype='uint8')
red_upper = np.array([180, 255, 255], dtype='uint8')
red_mask = cv2.inRange(hsv, red_lower, red_upper)

contours, _ = cv2.findContours(
    red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    if w * h < 500:          # ignore specks of noise
        continue
    cv2.rectangle(frame, (x, y), (x + w, y + h), (36, 255, 12), 2)
```

:::{note}
OpenCV's hue range is 0–179, not 0–359. Red sits at both ends of that range,
which is why detecting it usually needs two masks combined with
`cv2.bitwise_or`. {{ alert }} See the ALeRT line-following exercise on the
[ALeRT/Spot platform page](../../platforms/alert-spot.md#line-following).
:::

## Further reading

- [ArUco tutorial](https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html)
- [AprilTag](https://april.eecs.umich.edu/software/apriltag) and the
  [apriltag_ros wrapper](https://github.com/christianrauch/apriltag_ros)
- Back to [session 4](index.md)
