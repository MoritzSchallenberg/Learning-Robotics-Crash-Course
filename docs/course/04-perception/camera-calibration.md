# Camera calibration

{{ common }}

{{ optional }} **Status: preparation / reference.** This is *not* part of
the [session 4](index.md) core 85 minutes. Do this beforehand if your camera
needs it, or read it as background — it should never eat into the marker
detection task.

## Why

No two cameras and lenses are identical. Lenses distort — straight lines bow
outward near the edges — and the exact focal length and optical centre
differ from unit to unit. Calibration measures these and produces:

**Intrinsic parameters** — focal length and optical centre, converting
between pixels and directions.

**Distortion coefficients** — undo the lens distortion, producing a
*rectified* image.

Without calibration, any pose computed from an image is wrong, and wrong in
a way that grows toward the edges of the frame. Marker pose estimation
depends on it completely.

In ROS 2 these live in `sensor_msgs/msg/CameraInfo`, published alongside the
image.

## Checking whether a camera is already calibrated

```bash
ros2 topic echo /camera/camera_info --once
```

If the `k` and `d` arrays are all zeros, it is not calibrated.

:::{note}
Depth cameras such as the Intel RealSense arrive calibrated from the factory
and publish valid `CameraInfo` immediately. A plain USB webcam does not.
Simulated cameras also publish valid `CameraInfo` already — see
[session 4's simulation fallback](index.md#simulation-fallback).
:::

## Calibrating a webcam

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

Move the board through the camera's view until all four bars — X, Y, Size
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

## Further reading

- [ROS 2 image_pipeline documentation](https://docs.ros.org/en/rolling/p/image_pipeline/)
  — including the `camera_calibration` and `image_proc` packages
- Back to [session 4](index.md)
