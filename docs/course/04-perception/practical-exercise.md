# Practical perception exercise

{{ common }} {{ core }}

## Goal

Detect an ArUco marker in a live camera stream, draw a box around it, and
publish the detected marker ID on a ROS 2 topic.

## Starting point

A new package (call it `perception_demo`) with an empty node file
`aruco_node.py`, and a running, calibrated camera topic — either your
platform's real driver, or [Webots'](../../platforms/simulation.md)
simulated camera. [The perception pipeline
page](perception-pipeline.md) already gave you every piece of code the
node needs (`cv_bridge` conversion, the ArUco detector,
`generateImageMarker`); this task is wiring them together into one
subscriber-callback node, not a fill-in-the-blank template.

## Steps

1. Create the package: `ros2 pkg create --build-type ament_python
   perception_demo`, add `rclpy`, `sensor_msgs`, `std_msgs` and
   `cv_bridge` as `exec_depend` entries in `package.xml`.
2. In `aruco_node.py`, subscribe to your camera's image topic (confirm
   the exact name with `ros2 topic list` first — do not assume
   `/camera/image_raw`), convert each frame with `cv_bridge`, and run the
   `detectMarkers` call from [the perception pipeline
   page](perception-pipeline.md) inside the callback.
3. Add a publisher for `/detected_marker_id`
   (`std_msgs/msg/Int32`, or a custom type from
   {ref}`module 2's Continue learning <custom-message-and-service-types>` if
   you want to publish more than an ID) and publish whenever a marker is
   found.
4. Register the node as a console script in `setup.py`, then build:
   `colcon build --packages-select perception_demo`.
5. Run it: `ros2 run perception_demo aruco_node`.
6. Confirm the image is actually arriving first — add an `Image` display
   in RViz on your camera's real topic name, or `ros2 topic hz` it.
7. Hold a printed marker (from [the perception pipeline
   page](perception-pipeline.md)) in front of the camera.
8. Confirm in a second terminal: `ros2 topic echo /detected_marker_id`.

## Expected result

The marker is outlined in the published annotated image, and its ID is
printed every time `ros2 topic echo /detected_marker_id` receives a
message.

## Verification

```bash
ros2 topic hz /detected_marker_id
```

Publishes at a steady rate whenever a marker is visible, and stops
publishing new IDs when it is removed from view (the node should not
report a marker that is not there).

## Common problems

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
printed marker works as this test image.

**Test under changed lighting.** Dim the room, or point a lamp directly
at the marker to create glare, and re-run your node without changing any
code. Record at what point detection starts missing frames it caught
easily before — a concrete first data point for
{ref}`this module's occlusion-handling topic <handling-occlusion>` in
Continue learning, since inconsistent lighting produces the same kind of
intermittent "sometimes not detected" symptom as physical occlusion does.

## Try it on Spot

{{ alert }} {{ spotsim }}

The [platform page](../../platforms/alert-spot.md#image-processing)
already names the two ALeRT tutorial exercises this module's techniques
map onto; do them yourself here, against Webots Spot:

1. Subscribe to the gripper camera
   (`/SpotArm/gripper_camera/image_color`) and confirm it with an `Image`
   display in RViz before writing any code — the same "check the data
   exists first" habit from this page's own Common problems section.
2. Run this page's ArUco detector against that subscription instead of
   a generic webcam topic. The simulation uses the same `DICT_6X6_50`
   dictionary as [the perception pipeline page](perception-pipeline.md),
   so no code changes to the detector itself should be needed — only the
   topic name.
3. Publish the detected marker ID, exactly as in this page's practical
   task.
4. **Optional**: also publish the marker's pose as a TF frame (this
   page's Optional extensions), using the gripper camera's real
   calibration rather than an assumed one.
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
[module 7](../07-autonomous-decisions/practical-exercise.md#try-it-on-spot).
:::

**Verification**: `ros2 topic echo /detected_marker_id` reports a value
only while a marker is actually visible in the gripper camera's real
field of view, not the field of view you assumed it had.

## Next subtopic

[Interesting videos](videos.md), then
[Continue learning](continue-learning.md) for what to build next.
