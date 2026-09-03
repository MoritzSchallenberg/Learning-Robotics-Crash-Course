# Continue learning

This page's deeper chapters already follow one connected path —
calibrate the camera ([camera calibration](camera-calibration.md)),
detect something in the image ([fiducial markers](fiducial-markers.md)
or [object detection](object-detection.md)), then turn that detection
into a pose and a TF frame
([the practical exercise's](practical-exercise.md) Optional extensions,
and [module 3](../03-sensors-tf/laserscan-and-frames.md)). The topics below
extend that same path rather than starting a new one.

## Next steps

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

**Needs.** [The practical exercise](practical-exercise.md).

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

**Needs.** [The practical exercise](practical-exercise.md) and printed
markers.

**Try it.** Print three markers in a known, measured arrangement, define
a `cv2.aruco.Board` with their positions, and estimate the board's pose
with only two of the three markers visible to the camera.

**Check.** The board pose estimate remains stable (does not jump wildly)
as you cover one of the three markers.

**Read more.** [OpenCV: ArUco board
detection](https://docs.opencv.org/4.x/db/da9/tutorial_aruco_board_detection.html)
:::

## Intermediate projects

(handling-occlusion)=
:::{dropdown} Handling occlusion — Intermediate
:icon: light-bulb

**What it is.** What a detector should do when its target is partially or
fully blocked from view — briefly missing a detection is normal and
expected, not a bug to "fix" by lowering your detection threshold until
false positives appear instead.

**Why it matters.** [The practical exercise's](practical-exercise.md)
Common problems section already notes detections "flicker on and off at
the edge of the frame" — occlusion handling is the general version of
that: deciding how many missed frames before you treat a target as
genuinely lost, versus temporarily hidden.

**Needs.** [The practical exercise](practical-exercise.md).

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

**Needs.** {ref}`PointCloud2 <pointcloud2-advanced>`
(module 3's advanced topics) and a depth camera, real or simulated.

**Try it.** {{ unverified }} — subscribe to a depth camera's `Image` topic
alongside its color image, and read the depth value at the pixel
coordinates of one of your ArUco detections from
[the practical exercise](practical-exercise.md).

**Check.** The depth-derived distance to the marker is within a plausible
range of a distance you measure by hand.

**Read more.** [RealSense ROS
wrapper](https://github.com/IntelRealSense/realsense-ros)
:::

:::{dropdown} Tracking a detection across frames — Intermediate
:icon: light-bulb

**What it is.** Assigning a stable ID to the *same* object across
consecutive frames — object **tracking** — rather than treating every
frame's detection as unrelated to the last, which is what
[the practical exercise](practical-exercise.md) does today.

**Why it matters.** Without tracking, a target that flickers between
"detected" and "not detected" for one frame looks like two different
objects, one disappearing and one appearing; a mission that needs to
"follow this object" needs it to stay the same object.

**Needs.** [The practical exercise](practical-exercise.md), or
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

## Advanced topics

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

**Try it.** {{ unverified }} — for one ArUco detection from
[the practical exercise](practical-exercise.md), look up the LiDAR range
in roughly the same direction (from `/scan`) and compare it to the
camera-derived distance to the marker.

**Check.** You can state both distances and whether they agree within a
sensible margin, or explain why they legitimately would not (e.g. the
LiDAR's beam missing the marker entirely).

**Read more.** [Module 6: costmaps built from multiple
sensors](../06-navigation.md#core-concepts) is the same principle applied
at the navigation layer.
:::
