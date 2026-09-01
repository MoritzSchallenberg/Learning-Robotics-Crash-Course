# 4. Perception and Object Detection

:::{admonition} Session 4
:class: note

Wednesday, 14 October 2026, 17:35 – 19:00
:::

{{ common }}

A camera gives you a grid of coloured pixels. Turning that into "there is a
fire extinguisher 2.1 metres ahead, slightly to the left" is perception. This
session covers the three approaches the institute's teams actually use:
classical image processing, fiducial markers, and neural networks.

## Learning objectives

After this session you can:

- explain what camera calibration produces and why it is required;
- process a camera stream with OpenCV inside a ROS 2 node;
- detect ArUco or AprilTag markers and get a 6D pose from them;
- run a pre-trained YOLO model on a camera topic;
- label a dataset and train a custom model;
- explain the difference between *detecting* an object and *localizing* it.

## Prerequisites

[Session 3](03-sensors-tf.md). You understand coordinate frames, because a
detection is only useful once you can express it in one.

## Detection versus localization

Hold on to this distinction; it is the point of the whole session.

**Detection** answers *what*, in image coordinates: "there is a cup, in a box
from pixel (120, 240) to pixel (200, 310)". That is what YOLO gives you, and on
its own it cannot tell a robot where to drive.

**Localization** answers *where*, in the world: "there is a cup at
(1.8, 0.4, 0.7) in the `map` frame". This is what the robot needs.

Getting from one to the other requires more information than the image itself:

- **A calibrated camera** — to convert pixels to directions.
- **Depth** — from a depth camera, from a marker of known size, or by
  intersecting the direction with a known surface such as the floor.
- **A transform** — to express the result in a useful frame ([session 3](03-sensors-tf.md)).

Markers are popular precisely because they collapse all of this: a marker of
known physical size gives you full 6D pose from a single image.

## Camera calibration

### Why

No two cameras and lenses are identical. Lenses distort — straight lines bow
outward near the edges — and the exact focal length and optical centre differ
from unit to unit. Calibration measures these and produces:

**Intrinsic parameters** — focal length and optical centre, which convert
between pixels and directions.

**Distortion coefficients** — which undo the lens distortion, producing a
*rectified* image.

Without calibration, any pose you compute from an image is wrong, and wrong in
a way that grows toward the edges of the frame. Marker pose estimation is
completely dependent on it.

In ROS 2, these live in `sensor_msgs/msg/CameraInfo`, published alongside the
image.

### Checking whether a camera is calibrated

```bash
ros2 topic echo /camera/camera_info --once
```

If the `k` and `d` arrays are all zeros, the camera is not calibrated.

:::{note}
Depth cameras such as the Intel RealSense arrive calibrated from the factory
and publish valid `CameraInfo` immediately. A plain USB webcam does not. It is
still worth calibrating a webcam once, because the procedure teaches you what
those numbers mean.
:::

### Calibrating a webcam

{{ common }}

```bash
sudo apt install ros-$ROS_DISTRO-usb-cam ros-$ROS_DISTRO-camera-calibration
```

Start the camera:

```bash
ros2 run usb_cam usb_cam_node_exe
```

Get a checkerboard calibration target and measure it. You need the number of
**inner** corners and the physical width of one square.

```bash
ros2 run camera_calibration cameracalibrator \
  -c webcam \
  --size 9x6 \
  --square 0.0498 \
  --no-service-check \
  --ros-args --remap image:=image_raw
```

:::{danger}
Do not copy those numbers. `--size 9x6` and `--square 0.0498` describe one
particular board. Measure yours: `--size` is the count of **inner** corners
(a board with 10×7 squares has 9×6 inner corners), and `--square` is the edge
length of one square **in metres**. Wrong values produce a calibration that
looks successful and is wrong.
:::

Then move the board through the camera's view until all four bars — X, Y, Size
and Skew — turn green. You need the board:

- at the left, right, top and bottom of the frame;
- filling the frame completely;
- tilted left, right, up and down;
- at several distances.

Hold still at each position until the pattern is highlighted.

Click **CALIBRATE** (it may take a while and appear frozen — wait), then
**SAVE**. The result lands in `/tmp/calibrationdata.tar.gz`.

Extract it and keep `ost.yaml`:

```bash
mkdir -p ~/robot_ws/src/robot_bringup/config
cd ~/robot_ws/src/robot_bringup/config
mv /tmp/calibrationdata.tar.gz .
tar -xvzf calibrationdata.tar.gz
mv ost.yaml webcam.yaml
```

Point the camera node at it with a parameter file:

```yaml
/**:
  ros__parameters:
    video_device: "/dev/video0"
    framerate: 30.0
    io_method: "mmap"
    frame_id: "camera_link"
    pixel_format: "yuyv"
    image_width: 640
    image_height: 480
    camera_name: "webcam"
    camera_info_url: "package://robot_bringup/config/webcam.yaml"
```

:::{tip}
Check `ls /dev/video*` before and after plugging the camera in to find the
right `video_device`.
:::

Confirm the calibration is published:

```bash
ros2 topic echo /camera_info --once
```

The `k` matrix should now contain real numbers.

## OpenCV in a ROS 2 node

OpenCV works on NumPy arrays; ROS 2 uses `sensor_msgs/msg/Image`. `cv_bridge`
converts between them.

```bash
sudo apt install ros-$ROS_DISTRO-cv-bridge
pip install opencv-python
```

A minimal image-processing node:

```python
#!/usr/bin/env python3

import cv2
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image


class ImageProcessor(Node):

    def __init__(self):
        super().__init__('image_processor')
        self.bridge = CvBridge()
        self.subscription = self.create_subscription(
            Image, '/image_raw', self.image_callback, 10)
        self.publisher = self.create_publisher(Image, '/processed_image', 10)

    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        # ... process the frame here ...

        self.publisher.publish(self.bridge.cv2_to_imgmsg(frame, 'bgr8'))


def main():
    rclpy.init()
    node = ImageProcessor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

:::{tip}
Publish the annotated image on a topic and view it in RViz rather than calling
`cv2.imshow()`. It works over SSH, it works when the node runs on the robot,
and it can be recorded in a rosbag.
:::

### Colour detection with HSV

Finding "the red line on the floor" is much easier in **HSV** colour space than
in RGB, because hue stays roughly constant as lighting changes while RGB values
all shift together.

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
`cv2.bitwise_or`.
:::

## Fiducial markers

A **fiducial marker** is a printed pattern designed to be found reliably and
identified uniquely. Because the pattern is known and its physical size is
known, a single camera image gives you the marker's full 6D pose.

The two families in use here:

**ArUco** — built into OpenCV, no extra dependency, several dictionaries.

**AprilTag** — a separate library, generally more robust at distance and under
poor lighting.

Both work the same way and are largely interchangeable.

### ArUco with OpenCV

{{ common }} {{ alert }}

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

:::{warning}
The dictionary must match the markers you printed. `DICT_6X6_50` will not
detect a `DICT_4X4_50` marker, and there is no warning — you simply get no
detections. Check which dictionary your markers came from.
:::

:::{note}
The `cv2.aruco.ArucoDetector` class shown here is the OpenCV 4.7+ API. Older
code uses `cv2.aruco.detectMarkers(frame, dictionary, parameters=...)`
directly. If you hit an `AttributeError`, check your OpenCV version with
`python3 -c "import cv2; print(cv2.__version__)"`.
:::

### AprilTag

{{ common }}

```bash
sudo apt install ros-$ROS_DISTRO-apriltag-ros ros-$ROS_DISTRO-image-pipeline
```

The AprilTag node needs a **rectified** image, which is what the calibration
above enables:

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
distance scales linearly with it. Get it wrong and every pose is wrong by the
same factor. Measure the printed tag rather than trusting the value it was
designed at — printers scale.

Which edge to measure depends on the family. For `Standard41h12` and
`Custom48h12`, measure the **inner** black edge, not the outer border. See the
[apriltag_ros README](https://github.com/christianrauch/apriltag_ros).
:::

The node publishes a TF frame per detected tag, named `<family>:<id>` — for
example `Standard41h12:7`. That means you can immediately ask TF2 where a tag
is relative to anything else:

```bash
ros2 run tf2_ros tf2_echo base_link Standard41h12:7
```

This is the payoff of session 3: a camera detection becomes a coordinate you
can drive to, with no extra maths on your side.

## Neural networks: YOLO

Markers require you to put markers on things. For everything else — people,
doors, extinguishers, machine parts — you need a learned detector.

**YOLO** ("You Only Look Once") runs a single network pass over an image and
returns bounding boxes with class labels and confidences, fast enough for a
video stream.

### Installation

```bash
pip install ultralytics
```

If pip warns that scripts are not on your `PATH`:

```bash
export PATH=$PATH:~/.local/bin
```

Test it:

```bash
yolo predict model=yolov8n.pt source='path/to/your/image.jpg'
```

`yolov8n.pt` is the "nano" model, pre-trained on the
[COCO dataset](https://cocodataset.org/) — 80 everyday classes including
person, chair, bottle and cup. Results land in `runs/detect/predict`.

### GPU acceleration

Training on a CPU is painfully slow. With an NVIDIA GPU:

```bash
nvidia-smi                     # is the driver working?
```

Check that PyTorch can see the GPU:

```bash
python3 -c "import torch; print(torch.cuda.is_available())"
```

`True` means you are set. Expect roughly 10–50× faster training and 5–20×
faster inference than CPU.

:::{note}
Without a GPU, inference is still workable if you use an optimised runtime.
The ALeRT course uses OpenVINO for CPU inference:

```bash
pip3 install openvino-dev
```

{{ alert }} See the [ALeRT/Spot page](../platforms/alert-spot.md).
:::

### YOLO in a ROS 2 node

```python
#!/usr/bin/env python3

import cv2
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image
from ultralytics import YOLO
from vision_msgs.msg import Detection2D, Detection2DArray, ObjectHypothesisWithPose


class YoloNode(Node):

    def __init__(self):
        super().__init__('yolo_node')
        self.bridge = CvBridge()
        self.model = YOLO('yolov8n.pt')

        self.subscription = self.create_subscription(
            Image, '/image_raw', self.image_callback, 10)
        self.image_publisher = self.create_publisher(
            Image, '/yolo_detections', 10)
        self.detection_publisher = self.create_publisher(
            Detection2DArray, '/detections', 10)

    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

        detections = Detection2DArray()
        detections.header = msg.header

        for result in self.model(frame, verbose=False):
            for box in result.boxes:
                x1, y1, x2, y2 = (int(v) for v in box.xyxy[0])
                confidence = float(box.conf[0])
                class_name = result.names[int(box.cls[0])]

                cv2.rectangle(frame, (x1, y1), (x2, y2), (100, 0, 255), 2)
                cv2.putText(
                    frame, f'{class_name} {confidence:.2f}', (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 0, 255), 2)

                detection = Detection2D()
                detection.header = msg.header
                detection.bbox.center.position.x = float((x1 + x2) / 2)
                detection.bbox.center.position.y = float((y1 + y2) / 2)
                detection.bbox.size_x = float(x2 - x1)
                detection.bbox.size_y = float(y2 - y1)

                hypothesis = ObjectHypothesisWithPose()
                hypothesis.hypothesis.class_id = class_name
                hypothesis.hypothesis.score = confidence
                detection.results.append(hypothesis)

                detections.detections.append(detection)

        self.detection_publisher.publish(detections)
        self.image_publisher.publish(self.bridge.cv2_to_imgmsg(frame, 'bgr8'))


def main():
    rclpy.init()
    node = YoloNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

Two things worth noticing:

**Publish structured detections, not just an annotated image.** The picture is
for you; `vision_msgs/msg/Detection2DArray` is for the rest of the system.
Install it with `sudo apt install ros-$ROS_DISTRO-vision-msgs`.

**Copy `msg.header` into the output.** It carries the timestamp and the
`frame_id`, without which no downstream node can place the detection in space.

## Training a custom model

COCO does not contain fire extinguishers, hazmat signs or factory workpieces.
For those you train your own.

### 1. Collect images

Take **at least 30** photographs of the object, and vary everything: distance,
angle, lighting, background, occlusion. A model trained on 200 identical photos
will only recognise that exact photo.

### 2. Label them

Use any labelling tool — [MakeSense.ai](https://www.makesense.ai/) runs in the
browser and needs no account; [Roboflow](https://roboflow.com/) and
[CVAT](https://www.cvat.ai/) manage larger team datasets.

Draw a box around each object and export in **YOLO format**.

:::{warning}
Draw the box tightly around the object's actual boundary. Loose boxes teach the
model that the surrounding background is part of the object, and detection
accuracy collapses. If an image is blurred, estimate the true extent rather
than guessing generously.
:::

### 3. Organise the dataset

```text
my_model/
└── dataset/
    ├── images/
    │   ├── train/     ~80% of your images
    │   └── val/       ~20%, used to check the model during training
    └── labels/
        ├── train/
        └── val/
```

### 4. Write the configuration

```yaml
# dataset.yaml
path: /home/<username>/my_model/dataset
train: images/train
val: images/val

names:
  0: my_custom_label
```

### 5. Train

```bash
yolo train data=dataset.yaml model=yolov8n.pt epochs=100 imgsz=640
```

Results appear in `runs/detect/train`: the weights in `weights/best.pt` and
`weights/last.pt`, plus performance plots and annotated validation images.

:::{tip}
Look at the validation images before anything else. If the model found nothing
in them, training failed, and no amount of tuning the ROS node will help.
:::

### 6. Use it

```python
self.model = YOLO('/absolute/path/to/best.pt')
```

## Task

:::{admonition} Task: detect something and publish where it is
:class: task

**Part 1 — Get a camera stream.**

Bring up your camera (real or simulated) and view the image in RViz. Confirm
`camera_info` is published and contains real numbers.

**Part 2 — Detect a marker.**

Write a node that subscribes to the camera image, detects ArUco markers, draws
a box around each one, and publishes the annotated image. Verify in RViz.

**Part 3 — From detection to localization.**

Choose **one**:

- *Marker route*: configure AprilTag detection, confirm a TF frame appears per
  tag, and use a TF listener from [session 3](03-sensors-tf.md) to print the
  tag's position relative to `base_link`.
- *YOLO route*: run a pre-trained YOLO model on the camera topic and publish
  `Detection2DArray`. Then explain in writing what additional information you
  would need to turn a bounding box into a position in the `map` frame.

**Part 4 (optional) — Train a model.**

Photograph an object of your choice, label 30+ images, train, and run your
model in the ROS node.
:::

:::{admonition} Expected result
:class: result

Part 2: markers are outlined in the published image, and the marker ID is
logged.

Part 3, marker route: `ros2 run tf2_ros tf2_echo base_link <family>:<id>`
prints a position that changes sensibly as you move the tag — closer, and the
distance shrinks.

Part 3, YOLO route: `ros2 topic echo /detections` shows structured detections
with class names and confidences.
:::

:::{dropdown} Hint: what turns a bounding box into a position?
:icon: light-bulb

The bounding box gives you a **direction** — with the calibration matrix, the
box centre becomes a ray from the camera. What it does not give you is
**distance along that ray**. You need one of:

- a **depth camera**: read the depth at the box centre;
- a **known object size**: if you know the object is 0.3 m wide, its width in
  pixels gives the distance;
- a **known surface**: assume the object stands on the floor and intersect the
  ray with the floor plane;
- a **second viewpoint**: triangulate from two images.

Then apply the TF transform from the camera frame to `map`. This is exactly why
markers are convenient: known size means the distance comes for free.
:::

## Common mistakes

**No detections at all, no errors.**
Wrong ArUco dictionary or wrong AprilTag family. Both fail silently.

**Poses are consistently off by a factor.**
The marker size parameter does not match the printed marker. Measure it.

**Detection works on a still image but not on the robot.**
Motion blur. Reduce the exposure time, slow the robot down, or increase the
lighting.

**The node lags badly.**
You are running a large model on full-resolution images on a CPU. Reduce the
resolution, use the nano model, or drop frames — detecting at 5 Hz is usually
enough.

**`cv_bridge` encoding errors.**
Match the encoding to the source. `bgr8` is the usual choice for colour;
depth images use `16UC1` or `32FC1` and must not be requested as `bgr8`.

**The custom model detects everything as one class.**
Your labels are loose, or the training and validation sets overlap. Check the
validation images in `runs/detect/train`.

## Further reading

- [OpenCV documentation](https://docs.opencv.org/) and the
  [ArUco tutorial](https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html)
- [AprilTag](https://april.eecs.umich.edu/software/apriltag) and the
  [apriltag_ros wrapper](https://github.com/christianrauch/apriltag_ros)
- [Ultralytics YOLO documentation](https://docs.ultralytics.com/)
- [ROS 2 image_pipeline documentation](https://docs.ros.org/en/rolling/p/image_pipeline/)
  — including the `camera_calibration` and `image_proc` packages
- [vision_msgs](https://github.com/ros-perception/vision_msgs)
