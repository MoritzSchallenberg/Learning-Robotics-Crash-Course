# ALeRT / Spot

{{ alert }}

**ALeRT** — the Aachen Legged Rescue Team — is the MASKOR RoboCup Rescue League
team. The platform is a Boston Dynamics Spot: a quadruped that walks over
rubble, stairs and terrain where wheels are useless, fitted with a manipulator
arm.

This page covers what is specific to that system. The fundamentals are in the
[course modules](../course/index.md).

## System versions

```{list-table}
:header-rows: 1
:widths: 35 65

* - Component
  - Version
* - Operating system
  - Ubuntu 22.04 LTS (Jammy)
* - ROS 2 distribution
  - Humble Hawksbill
* - Simulator
  - Webots R2023b
* - Robot
  - Boston Dynamics Spot, with arm
```

This matches the course's [supported environment](../reference/compatibility.md)
exactly, so no distribution check is needed before following a command on
this page.

:::{note}
The original course notes state that only Ubuntu 22 could be actively
supported. WSL was documented as a fallback with a specific set of version
constraints and known issues; a native Ubuntu install avoids that entire class
of problem and is what this site recommends.
:::

## The RoboCup Rescue League

The competition simulates disaster response: a robot must traverse an arena
built to resemble a collapsed structure, and demonstrate capability in several
categories.

**Maneuvering and mobility** — various surfaces, obstacles, terrain.

**Dexterity** — manipulation tasks: a test board, turning valves, opening
doors.

**Exploration** — 2D and 3D mapping, detecting objects such as QR codes and
hazmat signs, avoiding holes, finding signs of life.

**Readiness** — sensor capability tests: video and thermal resolution, motion
detection, colour pattern recognition, audio acuity.

This shapes the platform completely. Legs rather than wheels because the ground
is not flat. 3D mapping rather than a 2D occupancy grid because the environment
has vertical structure. An arm because the tasks require manipulation.

## The Webots Spot simulation

Most of the course can be done entirely in simulation, using the ALeRT-built
Webots Spot model and a relaxed version of the competition arena.

### Installation

The simulation lives at
[MASKOR/webots_ros2_spot](https://github.com/MASKOR/webots_ros2_spot). Follow
the installation instructions in the repository README — it is the authority on
the current branch and dependencies.

Additional packages the tutorials use:

```bash
sudo apt install python3-colcon-common-extensions
sudo apt install ros-humble-teleop-twist-keyboard
pip install opencv-python
```

### Launching

```bash
ros2 launch webots_spot spot_launch.py
```

Then drive it:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

:::{tip}
Before anything else, explore what the simulation offers. It publishes
considerably more than turtlesim did:

```bash
ros2 topic list
ros2 service list
ros2 action list
```
:::

### Topics and frames

Spot's topics are namespaced. Some you will need:

```{list-table}
:header-rows: 1
:widths: 45 55

* - Topic
  - Contents
* - `/Spot/Velodyne_Puck/point_cloud`
  - 3D LiDAR point cloud
* - `/scan`
  - 2D laser scan, derived from the point cloud
* - `/Spot/odometry`
  - Odometry
* - `/SpotArm/gripper_camera/image_color`
  - Gripper camera image
* - `/robot_description`
  - Robot model, for the RViz RobotModel display
* - `/cmd_vel`
  - Velocity commands
```

:::{warning}
Verify these against `ros2 topic list` on your own installation. Topic names
change between branches of the simulation repository, and the list above
reflects the tutorial material rather than a guaranteed current state.
:::

### RViz setup

Set **Fixed Frame** to `base_footprint`, then add:

- `TF`
- `PointCloud2` on `/Spot/Velodyne_Puck/point_cloud`
- `Odometry` on `/Spot/odometry`
- `LaserScan` on `/scan` — **set Reliability to Best Effort**
- `Image` on `/SpotArm/gripper_camera/image_color`
- `RobotModel` with Description Topic `/robot_description`

:::{note}
The Best Effort setting on `/scan` is not optional. The publisher uses it, and
an RViz display left on Reliable shows nothing at all, with no error. See
[module 3](../course/03-sensors-tf/practical-exercise.md#common-problems).
:::

Save the configuration once it works.

### From 3D to 2D

Spot carries a Velodyne producing a 3D point cloud. A node flattens that into a
2D `LaserScan` on `/scan`, which is what SLAM Toolbox and Nav2 consume.

To see the LiDAR rays in Webots: *View → Optional Rendering → Show Lidar Ray
Paths*.

:::{tip}
A useful exercise from the source course: subscribe to `/scan`, keep only the
points within roughly ±20° of straight ahead, and republish on `/cone_scan`.
That gives you a simple "how far to the wall in front of me" signal — enough to
walk forward and stop before a wall, and a good introduction to manipulating
a `LaserScan` message.
:::

## Services and actions

Spot exposes its postures as **services** — a natural fit, since standing up is
quick and either succeeds or does not.

```bash
ros2 service list -t
ros2 interface show webots_spot_msgs/srv/SpotMotion
ros2 service call /Spot/sit_down webots_spot_msgs/srv/SpotMotion
```

`rqt` provides a graphical interface for calling services, which is convenient
while exploring.

A service client in Python:

```python
import rclpy
from rclpy.node import Node
from webots_spot_msgs.srv import SpotMotion


class PushUpNode(Node):

    def __init__(self):
        super().__init__('pushup_node')
        self.lie_client = self.create_client(SpotMotion, '/Spot/lie_down')
        self.stand_client = self.create_client(SpotMotion, '/Spot/stand_up')
        self.request = SpotMotion.Request()
        self.is_lying = False

    def toggle(self):
        client = self.stand_client if self.is_lying else self.lie_client
        self.is_lying = not self.is_lying
        return client.call_async(self.request)
```

:::{tip}
Wait for the service before calling it — `client.wait_for_service()` — and
check that the future actually completed. A call to a service that is not up
yet fails silently in a way that looks like the robot ignoring you.
:::

## Image processing

The ALeRT tutorials use OpenCV directly on the gripper camera, which is a good
way to learn perception before reaching for a neural network. Both exercises
are described in general terms in
[module 4](../course/04-perception/index.md).

### ArUco detection

Detect markers in the gripper camera image and draw a bounding box around each.
The simulation uses the **`DICT_6X6_50`** dictionary:

```python
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)
detector = cv2.aruco.ArucoDetector(dictionary)
corners, ids, rejected = detector.detectMarkers(image)
```

Full node structure in
[module 4](../course/04-perception/fiducial-markers.md#aruco-with-opencv).

### Line following

Detect the red line on the floor and follow it by publishing `Twist` messages
to `/cmd_vel`. The technique — convert to HSV, threshold, find contours — is in
[module 4](../course/04-perception/fiducial-markers.md#colour-detection-with-hsv).

The interesting part is the control: given the line's horizontal position in
the image, compute a turn rate that keeps it centred. A proportional controller
on the offset between the line's centroid and the image centre is enough to
start.

## Mapping and navigation

The general workflow is [module 5](../course/05-mapping-localization.md) and
[module 6](../course/06-navigation.md). Spot-specific launch files:

```bash
# SLAM
ros2 launch webots_spot slam_launch.py

# Navigation
ros2 launch webots_spot nav_launch.py
```

Install Nav2 for Humble:

```bash
sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup
```

Save a map as usual:

```bash
ros2 run nav2_map_server map_saver_cli -f ~/map
```

:::{note}
To navigate with a saved map, the map must be placed where the package expects
it — a `map` folder inside the simulation package, registered in `setup.py` so
it is installed. Read `nav_launch.py` to see the path it uses rather than
guessing.
:::

## 3D mapping

{{ advanced }} A 2D occupancy grid cannot represent a rescue arena. Two 3D
approaches, explained for general understanding in
[module 5's 3D mapping subtopic](../course/05-mapping-localization/localization-and-3d-mapping.md#mapping-rough-3d-terrain)
— this page adds only the ALeRT-specific repository pointers.

### Octomap

```bash
sudo apt install ros-humble-octomap*
```

The team maintains a fork at
[RRL-ALeRT/octomap_mapping](https://github.com/RRL-ALeRT/octomap_mapping). Use
the launch file from that repository. It feeds 3D path planning — the team has
a [3D planner working on the octomap](https://github.com/RRL-ALeRT/alert_ros2).

### GLIM

[GLIM](https://github.com/koide3/glim_ros2) is a LiDAR–inertial SLAM system
that tightly couples 3D LiDAR with IMU data to build accurate point cloud
maps — see module 5 for when this matters over 2D SLAM. Installation is
documented at
[koide3.github.io/glim](https://koide3.github.io/glim/installation.html).

### Mesh navigation

{{ unverified }} For navigating on non-flat surfaces, the team has
experimented with
[mesh_navigation](https://github.com/naturerobots/mesh_navigation), which
plans on a triangle mesh of the terrain rather than a grid — the natural
generalisation when "the floor" is not a plane.

:::{note}
All three of Octomap, GLIM and mesh navigation are referenced here by
repository link with the install command each repository documents, and no
further tested configuration. Treat this section as orientation — read the
linked repository's own documentation for a working parameter set, rather
than expecting a tested walkthrough here. None of the three is part of any
module's core task.
:::

## Manipulation with MoveIt

```bash
ros2 launch webots_spot moveit_launch.py
```

RViz opens with the arm controllable. Drag the interactive marker at the
gripper to a target pose, click **Plan**, inspect the trajectory, then
**Execute**.

If planning fails, the joints are colliding or the target is outside the arm's
reachable workspace. The Joints panel lets you adjust individual motors with
sliders, which is often the quickest way to get out of an awkward
configuration.

The general concepts and a pick-and-place structure are in
[module 7](../course/07-autonomous-decisions.md).

:::{tip}
The simulation publishes TF frames for objects — for example the target
workpiece and the place box. That means you can get a grasp pose with a TF
listener ([module 3](../course/03-sensors-tf.md)) rather than computing it
from an image, which makes the manipulation exercise tractable.
:::

## Object detection

### YOLO on CPU with OpenVINO

Spot's onboard compute may not have a usable GPU, so the ALeRT tutorials use
OpenVINO for CPU inference:

```bash
pip3 install openvino-dev
```

The team provides an inference node in the simulation repository
([`scripts/yolov8_openvino.py`](https://github.com/MASKOR/webots_ros2_spot)),
adapted from the
[yolov8_openvino](https://github.com/openvino-book/yolov8_openvino) project.

The provided model is trained on COCO, and the objects in the simulation are
drawn from that dataset — so for the basic exercise, no custom training is
needed. Point the gripper camera at the wall and a clock should be detected.

With an NVIDIA GPU available, the standard PyTorch models from
[Ultralytics](https://docs.ultralytics.com/usage/cli/) are faster.

### Hazmat signs

A service switches the images in the simulation to hazmat signs, which are
**not** in COCO:

```bash
ros2 service call /hazmat_signs std_srvs/srv/Empty "{}"
```

This is the trigger for training a custom model — see
[module 4](../course/04-perception/object-detection.md#training-a-custom-model).

### Gesture control

An optional project uses [MediaPipe](https://developers.google.com/edge/mediapipe/solutions/guide) for
hand gesture recognition, translating gestures into `cmd_vel` commands:

```bash
sudo apt install ros-humble-v4l2-camera -y
pip3 install mediapipe tensorflow scikit-learn loguru
git clone https://github.com/RRL-ALeRT/mediapipe_ros2.git
```

```bash
ros2 launch mediapipe_ros2 hand_gesture.launch.py
ros2 topic echo /recognized_gesture
```

You will need to point the node's subscription at whichever camera topic your
setup publishes.

## High-level control

The ALeRT stack uses several approaches, covered generally in
[module 7](../course/07-autonomous-decisions.md):

**RAFCON** — graphical state machines, the main tool in the tutorials.

**Golog++** — an action language developed with institute involvement
([MASKOR/gologpp](https://github.com/MASKOR/gologpp), with a
[ROS 2 interface](https://github.com/MASKOR/gologpp-ros/tree/ros2)).

**PlanSys2** — PDDL-based planning ([plansys2.github.io](https://plansys2.github.io/)).

## Operating the physical robot

:::{danger}
Do not operate Spot without supervision and training from the team. It is heavy,
it moves fast, and an emergency stop drops it where it stands.

There are separate E-stops for the robot and for the arm. Pressing one stops
the motors immediately: Spot falls, and the manipulator stops and falls
mid-action. Use them only when someone or something is genuinely about to be
hurt — an unnecessary press means a full restart.
:::

The general operating sequence, as documented by the team:

1. Check that the robot and controller are charged, and that there is clear
   space around the robot — Spot needs room to manoeuvre.
2. Power on Spot and release the motor cut-off. Wait for the startup sequence.
3. Power on the controller and connect to the team's operations network.
4. Start the drivers, then enable the robot with the E-stop control in the
   operator interface. A terminal should confirm the E-stop is found and the
   driver started.
5. Confirm the robot model, map and camera feeds appear in RViz.
6. Control is enabled with a button combination on the controller; the team
   maintains a control schematic.
7. The manipulator has its own driver, started separately.

To shut down: command Spot to sit, then hold the power button until the
indicator goes out.

:::{note}
Exact button sequences, network names, device addresses and interface
credentials are internal operating information and are not published on this
public site. Get the current procedure and a hands-on briefing from the team
before touching the robot.
:::

## Working through the course

```{list-table}
:header-rows: 1
:widths: 30 70

* - Where the course says
  - On Spot
* - `/scan`
  - Present, derived from the 3D point cloud — Best Effort QoS
* - Generic camera topic
  - `/SpotArm/gripper_camera/image_color` and others
* - `/odom`
  - `/Spot/odometry`
* - 2D occupancy grid
  - Works, but Octomap or GLIM is the real answer for 3D terrain
* - Generic markers
  - ArUco `DICT_6X6_50` in the simulation
* - Manipulation
  - MoveIt 2 with the Spot arm
```

## Try it on Spot: where each exercise lives

Every course module carries its own **Try it on Spot** section, applying
that module's exercise directly to this platform rather than only to a
generic robot. This table is an index into them — the exercises
themselves are not repeated here.

```{list-table}
:header-rows: 1
:widths: 8 30 30 32

* - Module
  - Spot exercise
  - Environment
  - Safety level
* - 1
  - [Identify sensors, compute, actuators and the safety chain](../course/01-hardware/practical-exercise.md#try-it-on-spot)
  - Real Spot (inspection only) or the diagram above
  - {{ spotreadonly }}
* - 2
  - [Inspect the Webots Spot node/topic graph](../course/02-ros2/practical-exercises.md#try-it-on-spot)
  - Simulation
  - {{ spotsim }}
* - 3
  - [Build the RViz setup yourself, then diagnose a fault in it](../course/03-sensors-tf/practical-exercise.md#try-it-on-spot)
  - Simulation (or read-only on real Spot)
  - {{ spotsim }} / {{ spotreadonly }}
* - 4
  - [ArUco detection and line following on the gripper camera](../course/04-perception/practical-exercise.md#try-it-on-spot)
  - Simulation
  - {{ spotsim }}
* - 5
  - [SLAM, map saving and localization](../course/05-mapping-localization/practical-exercise.md#try-it-on-spot)
  - Simulation; real Spot supervised only
  - {{ spotsim }} / {{ spotsupervised }}
* - 6
  - [Nav2 goals, recovery behaviour and a before/after comparison](../course/06-navigation/practical-exercise.md#try-it-on-spot)
  - Simulation
  - {{ spotsim }}
* - 7
  - [A stand → navigate → detect → return → sit mission state machine](../course/07-autonomous-decisions/practical-exercise.md#try-it-on-spot)
  - Simulation; real Spot supervised only
  - {{ spotsim }} / {{ spotsupervised }}
* - 8
  - [Full-system diagnostics and a fault-injection exercise](../course/08-integration.md#try-it-on-spot)
  - Simulation (or read-only on real Spot)
  - {{ spotsim }} / {{ spotreadonly }}
```

:::{note}
**Simulation exercise** — free to run in Webots on your own. **Read-only
on physical Spot** — inspection or observation only, no movement, no
actuator freed. **Supervised physical exercise** — real Spot movement,
only with a trained team member present; see [Operating the physical
robot](#operating-the-physical-robot).
:::

## Further reading

- [webots_ros2_spot](https://github.com/MASKOR/webots_ros2_spot) — the
  simulation, and the authority on its own setup
- [RRL-ALeRT on GitHub](https://github.com/RRL-ALeRT)
- [RoboCup Rescue League](https://rescuesim.robocup.org/)
- [Boston Dynamics Spot](https://bostondynamics.com/products/spot/)
- [MoveIt 2](https://moveit.picknik.ai/)
- [GLIM](https://koide3.github.io/glim/) · [Octomap](https://octomap.github.io/)
