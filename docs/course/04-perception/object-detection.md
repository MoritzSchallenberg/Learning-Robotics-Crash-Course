# Object detection with YOLO

{{ common }}

{{ advanced }} **Status: advanced reading.** Not required for
[module 4](index.md)'s core task, which uses a fiducial marker. This page
is for objects that cannot carry a marker — people, tools, hazmat signs —
and for teams whose platform track uses YOLO
({{ carologistics }} {{ alert }}).

Markers require you to put markers on things. For everything else you need
a learned detector. **YOLO** ("You Only Look Once") runs a single network
pass over an image and returns bounding boxes with class labels and
confidences, fast enough for a video stream.

## Installation

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

## GPU acceleration

Training on a CPU is painfully slow. With an NVIDIA GPU:

```bash
nvidia-smi                     # is the driver working?
python3 -c "import torch; print(torch.cuda.is_available())"
```

`True` means you are set. Expect roughly 10–50× faster training and 5–20×
faster inference than CPU.

:::{note}
Without a GPU, inference is still workable with an optimised runtime. The
ALeRT course uses OpenVINO for CPU inference: `pip3 install openvino-dev`.
{{ alert }} See the [ALeRT/Spot page](../../platforms/alert-spot.md).
:::

## YOLO in a ROS 2 node

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
```

Two things worth noticing: **publish structured detections, not just an
annotated image** — install `vision_msgs`
(`sudo apt install ros-$ROS_DISTRO-vision-msgs`) — and **copy `msg.header`
into the output**, which carries the timestamp and `frame_id` without which
no downstream node can place the detection in space (see
[detection versus localization](perception-pipeline.md#why-a-robot-needs-it)).

## Training a custom model

COCO does not contain fire extinguishers, hazmat signs or factory
workpieces. For those you train your own — the dataset preparation is
covered in full on [Data labeling](data-labeling.md); this is the training
step once you have one.

```yaml
# dataset.yaml
path: /home/<username>/my_model/dataset
train: images/train
val: images/val

names:
  0: my_custom_label
```

```bash
yolo train data=dataset.yaml model=yolov8n.pt epochs=100 imgsz=640
```

Results appear in `runs/detect/train`: the weights in `weights/best.pt` and
`weights/last.pt`, plus performance plots and annotated validation images.

:::{tip}
Look at the validation images before anything else. If the model found
nothing in them, training failed, and no amount of tuning the ROS node will
help.
:::

Use it:

```python
self.model = YOLO('/absolute/path/to/best.pt')
```

## Common mistakes

**The node lags badly.** A large model at full resolution on a CPU. Reduce
resolution, use the nano model, or detect at 5 Hz instead of every frame.

**`cv_bridge` encoding errors.** Match the encoding to the source — `bgr8`
for colour; depth images use `16UC1` or `32FC1`.

**The custom model detects everything as one class.** Loose labels, or the
training and validation sets overlap — see
[data labeling](data-labeling.md).

## Further reading

- [Ultralytics YOLO documentation](https://docs.ultralytics.com/)
- [vision_msgs](https://github.com/ros-perception/vision_msgs)
- Back to [module 4](index.md)
