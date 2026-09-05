# Repository audit: github.com/RRL-ALeRT

**Not part of the published website.** Internal working document for
Entwicklungsauftrag 8.

## Method

Fetched live from the GitHub REST API (`api.github.com`, not a cached
page) on the date this report was written. The organisation currently
lists **53 public repositories**. For each repository named in the task's
Section 8 list (29 repos), plus 6 further repositories found relevant
during the audit, the repository's actual README was fetched and read
(where one exists) to determine purpose, ROS version, and documentation
quality — not inferred from the repository name alone, per the task's
explicit warning that a repository's existence does not prove current
hardware use.

**Verification status** in the table below uses exactly the six-value
scale the task specifies: *Repository exists / Repository documented /
Build verified / Simulation verified / Hardware verified / Archived or
historical.* Nothing in this audit reached "Build verified", "Simulation
verified" or "Hardware verified" — those require actually building,
running, or testing the code, which this audit (a repository-metadata and
README review) does not do. Everything below is therefore capped at
*Repository exists* or *Repository documented*, honestly, even for
repositories that are clearly real and active.

## Repositories named in the task (29)

| Repository | Purpose | Fork/original | ROS version | Last meaningful update | Documentation quality | Tutorial topic | Verification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `alert_ros2` | Central integration workspace: SLAM (Hector + SLAM Toolbox), YOLOv8/v5+OpenVINO detection (hazmat, general objects), QR/ArUco markers, Spot integration, Geotiff generation | Original | ROS 2 (README doesn't pin a distro; site policy assumes Humble unless proven otherwise) | 2026-03-25 | Good — structured README with an overview section | Integration, Diagnostics and Testing; cross-linked from Perception and Mapping | Repository documented |
| `spot_gen3_moveit` | MoveIt 2 configuration for Spot + Kinova Gen3 arm (name implies MoveIt config package) | Original | {{ unverified }} — no README found (404) | 2026-06-19 (recently active) | **None** — no README | Robot Manipulation | Repository exists |
| `ros2_kortex` | Official-style Kinova Kortex ROS 2 driver for the Gen3 family; README confirms the real end-effector combination: **Kinova Gen3 7-DOF arm + Intel RealSense 3D Vision Module + Robotiq 2F-85 2-finger 85 mm adaptive gripper** | Fork (of Kinova's own `ros2_kortex`) | ROS 2 | 2026-03-25 | Good | Robot Manipulation, Perception-to-Grasp | Repository documented |
| `kinova-ros2` | Older Jaco2/Mico arm ROS 2 packages; README shows real Humble build/launch/MoveIt commands | Fork | ROS 2 Humble (confirmed by README's own heading) | 2023-04-20 (no activity since) | Good but **stale** — superseded per `kinova_stuffs`'s own README (see below) | Historical / Robot Manipulation (background only) | Repository documented, likely superseded |
| `kinova_stuffs` | Kortex API Python wheel + launch wrapper; **README explicitly states the team is switching to `ros2_kortex`, and that this repo "works perfectly fine with ROS2 Humble"** | Original | ROS 2 Humble (explicit) | 2026-03-19 | Minimal but decisive (the migration note is the single most useful line) | Robot Manipulation | Repository documented |
| `alert_auto_dexterity` | Name implies an autonomous-dexterity mission package (Work Package 10-style pipeline) | Original | {{ unverified }} — no README found (404) | 2026-03-04 | **None** | Autonomous Decision-Making / Rescue Applications | Repository exists |
| `pose_detection` | Human pose detection (name only) | Original | {{ unverified }} — README is a bare title, no content | 2026-06-04 | **None** (title only) | Perception | Repository exists |
| `Estop-detection` | "Code to detect Estop and the tfs" (org description) — E-Stop button/keypoint detection with TF output | Original | {{ unverified }} — no README found (404) | 2026-06-19 | **None** — description only, from the org listing | Perception | Repository exists |
| `Magnet_Sensor` | KY-025 reed-switch sensor ROS 2 package; README states it works for "any True or False value reading from serial port", not only KY-025 | Original | {{ unverified }} — no ROS distro stated | 2026-06-19 | Minimal (2 lines) | Sensors and Coordinate Frames | Repository documented |
| `mediapipe_ros2` | Hand-gesture recognition → `cmd_vel`; confirmed in the content audit as a real, working ROS 2 Humble tutorial | Original | ROS 2 Humble (confirmed via the archive tutorial page, not just the README) | 2024-09-27 | Minimal README, but the archive's own tutorial page fully documents install/build/run | Perception | Repository documented |
| `Seek-Thermal-ROS2-Wrapper` | Seek thermal camera ROS 2 wrapper; README explicitly states **"Tested on Ubuntu 22.04 with ROS2 Humble"** | Original | ROS 2 Humble (explicit) | 2025-03-31 | Good — install steps, launch command, and a full list of colour-palette/rotation launch arguments | Sensors and Coordinate Frames | Repository documented |
| `QReader_openvino` | QR-code reading, OpenVINO-accelerated | Fork (of `Eric-Canas/QReader`, an external non-ALeRT project) | Not a ROS package by itself (a Python library); ALeRT's own ROS 2 wrapping is not shown in this README | 2024-07-13 | Good (upstream project's own README) | Perception | Repository documented |
| `estop_keypoints_dataset_generation` | Synthetic training-data generation for a YOLOv8-Pose E-Stop-button keypoint detector; confirms CVAT for annotation and a phone camera for source images | Original | Not a ROS package (a dataset-generation notebook) | 2026-03-11 | Minimal but functional (points to `data/steps.md`) | Perception (data labeling) | Repository documented |
| `rrl_image_view` | Image-viewing utility (name only) | Original | {{ unverified }} — no README found (404) | 2026-02-12 | **None** | Sensors and Coordinate Frames | Repository exists |
| `octomap_mapping` | Standard OctoMap ROS stack (`octomap_server`); README explicitly separates the ROS 1 branch (`kinetic-devel`) from **the `ros2` branch for Foxy and newer** | Fork (of `OctoMap/octomap_mapping` upstream) | ROS 2 (`ros2` branch; Foxy+, Humble compatibility plausible but not separately confirmed) | 2026-06-01 | Good (upstream README) | Mapping and World Models | Repository documented |
| `octomap_rviz_plugins` | RViz plugins for OctoMap message visualisation | Fork (of `octomap/octomap_rviz_plugins`) | "ROS groovy and later" per its own README — **ROS 1 phrasing**, ROS 2 compatibility not confirmed by the README text itself | 2026-02-08 | Minimal | Mapping and World Models | Repository documented, **ROS 2 compatibility unverified from README wording alone** |
| `Map-Conversion-3D-Voxel-Map-to-2D-Occupancy-Map` | Converts OctoMap/UFOMap voxel maps into 2D occupancy grids for UAV/UGV use, plus 2D→3D path conversion | Fork (of `LTU-RAI`'s package) | **Confirmed ROS 2** (README explicitly distinguishes its `ros2` default branch from an older `ros` branch) | 2025-07-04 | Good | Mapping and World Models | Repository documented |
| `alert_exploration` | Exploration mission package (name only) | Original | {{ unverified }} — no README found (404) | 2026-06-26 (recently active) | **None** | Rescue Applications and Projects | Repository exists |
| `rrt_exploration` | Multi-robot RRT-based frontier exploration; original README is an academic-thesis package (American University of Sharjah), five-node architecture (global/local RRT detectors, filter, assigner, OpenCV-based detector) | Fork | {{ unverified }} — README does not state ROS 2; the original package's era and style suggest it may originate from ROS 1, and no ROS 2 port statement was found in the fetched text | 2024-07-18 | Good, but **ROS 2 compatibility not confirmed** | Localization, Navigation and Exploration | Repository documented, ROS 2 status unverified |
| `octo_navigation` | 3D navigation on OctoMaps for unstructured terrain; README gives a full, real launch sequence and names a concrete dependency chain (a fork of `move_base_flex` at a `humble` branch, plus `octomap_mapping`'s `feature/global_and_local_mapping` branch) | Original | ROS 2 Humble (the `move_base_flex` fork branch is explicitly named `humble`) | 2026-07-04 (most recently active repo in this table) | Good — full dependency and launch instructions | Localization, Navigation and Exploration | Repository documented |
| `Dsp` | D*+ global path planner on a 2D/3D grid, built on the `dsl` library plus OctoMap/Cartographer | Fork (`LTU-RAI/Dsp`) | **ROS 1** — README explicitly states "tested on Ubuntu 18.04 and 20.04 thus ROS melodic and noetic" and references `catkin build`, not `colcon` | 2025-03-06 | Good, but **not ROS 2** | Localization, Navigation and Exploration (must be marked historical/ROS 1 if referenced) | Repository documented — **ROS 1, not ROS 2 Humble compatible as documented** |
| `dsl` | D*-Lite graph search library, dependency of `Dsp` | Fork (`jhu-asco/dsl`) | Not a ROS package (a standalone C++ library, built with plain `cmake`) | 2025-03-06 | Minimal (one line) | Localization, Navigation and Exploration (background library only) | Repository documented |
| `frame_server` | Name-only; likely a TF/frame-serving utility given `frame_panel`'s pairing | Original | {{ unverified }} — README is a bare title | 2026-06-25 | **None** | Sensors and Coordinate Frames | Repository exists |
| `steam_deck_ros2` | Steam Deck setup as a ROS 2 operator console: SteamOS developer mode, disabling read-only mode, enabling `sshd`, `screen`, micromamba | Original | Not itself a ROS package — an OS-setup guide for the Steam Deck hardware used as the physical control device | 2026-03-13 | Good, concrete, step-by-step | ALeRT Platforms and Safety, Integration/Steam-Deck-Dashboard | Repository documented |
| `alert_dashboard_rqt` | RQT plugins for Spot control/debugging: Spot E-Stop RQT plugin, a debug-console dashboard, a GStreamer camera view; architecture uses a FastAPI + WebSocket "tmux API server" running on the robot PC | Original | ROS 2 (RQT plugins, distro not separately pinned) | 2026-02-13 | Good — names concrete components (`tmux_api_server/`, `tmux_api_client.py`, `alert_dashboard_rqt.py`, `spot_estop_rqt.py`) | Integration, Diagnostics and Testing | Repository documented |
| `spot-webots-cloud` | Browser-based Spot simulation via webots.cloud (no local Webots install required) | Original | Webots R2023a-hosted demo, ROS layer not detailed in this README | 2023-09-04 (no recent activity) | Good for what it documents | Simulation | Repository documented |
| `webots_ros2_go2` | Webots simulation, currently **Spot** (mature) with an **in-progress "For Go2 (Todo)"** section for the Unitree Go2 quadruped at the very top of the README | Original | ROS 2 Humble (CI badge references a `test_ros2_humble.yml` workflow) | 2025-09-05 (recently active) | Good for the Spot portion; **Go2 support is explicitly marked as a to-do, not finished** | ALeRT Platforms and Safety (Go2 must be marked Experimental, not a verified platform) | Repository documented — **Go2 portion explicitly unfinished per the repo's own README** |
| `go2_ros2_sdk` | Community ROS 2 SDK for the Unitree Go2 | Fork (`abizovnuralem/go2_ros2_sdk`, an explicitly **"Unofficial"** SDK per its own README) | ROS 2, Python 3.10, with optional Isaac Sim integration | 2025-07-08 | Good (upstream README) | ALeRT Platforms and Safety (background only — this is an external, unofficial dependency, not ALeRT's own code) | Repository documented |
| `gologpp-ros` | ROS platform backend for Golog++; README documents a real Blocksworld example combining Webots, Spot and the manipulator | Fork (of `MASKOR/gologpp-ros`) | ROS 2 (`ros2` branch referenced throughout) | 2026-01-21 | Good — concrete install steps (Debian package, Eclipse Prolog, a VS Code extension) | Autonomous Decision-Making | Repository documented |
| `gpp_action_examples` | Golog++ action examples | Original | {{ unverified }} — README is a bare title | 2024-07-25 (no recent activity) | **None** | Autonomous Decision-Making | Repository exists |

## Additional repositories found relevant during the audit (not in the task's list)

| Repository | Purpose | Fork/original | ROS version | Last meaningful update | Documentation quality | Tutorial topic | Verification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `spot_ros2` | Boston Dynamics Spot ROS 2 driver | Fork (of `bdaiinstitute/spot_ros2`, the Boston Dynamics AI Institute's own driver) | ROS 2, actively tested upstream (own CI badge) | 2026-01-21 | Good (upstream README) | ALeRT Platforms and Safety | Repository documented |
| `frame_panel` | Companion to `frame_server`; likely an RViz panel for the same frame-serving feature | Original | {{ unverified }} — README is a bare title | 2026-03-04 | **None** | Sensors and Coordinate Frames | Repository exists |
| `object_detection` | YOLO + depth camera → 3D object TF, with persistent (deduplicated, uniquely-ID'd, e.g. `linear_board_0`) and non-persistent mapping modes; confirms real commands `ros2 run object_detection yolo_to_map` / `yolo_to_pose` | Original | ROS 2 (uses `ultralytics`, `openvino`) | 2026-03-10 | Good, concrete | Perception, Perception-to-Grasp | Repository documented |
| `world_info_msgs_ros2` | Custom message definitions (name implies world/scene-state messages) | Original | ROS 2 (CMake/interface package) | 2025-04-08 | Not reviewed in this pass | Mapping and World Models (likely) | Repository exists |
| `convert_octomap_to_ply` | OctoMap → PLY mesh conversion utility | Original | ROS 2 (implied by pairing with `octomap_ply`) | 2026-03-10 | Not reviewed in this pass | Mapping and World Models | Repository exists |
| `octomap_ply` | "ros2 service to convert octomap to ply" (org description) | Original | ROS 2 (explicit in description) | 2026-03-10 | Not reviewed in this pass | Mapping and World Models | Repository exists |
| `Portaudio-Device-ID-finder` | Finds a plugged-in audio device's ID for use with `audio_common`'s `device:=` ROS 2 parameter | Original | ROS 2 (implied by its stated integration with `audio_common`) | 2026-03-13 | Not reviewed in this pass | Integration, Diagnostics and Testing | Repository exists |

## Remaining public repositories (not reviewed in depth this pass)

The organisation's other public repositories are mostly forks of external
tooling with no direct README review performed yet: `wpi_jaco_ros2`,
`spot_wrapper`, `flir_a320_ros2`, `ROS2-FrontierBaseExplorationForAutonomousRobot`,
`sick_scan_xd`, `rviz_2d_overlay_plugins`, `rrl-alert.github.io` (the
team's own prior static Jekyll site — **historical**, superseded by this
Sphinx project), `image_transport_plugins`, `ffmpeg_image_transport`,
`picknik_controllers`, `rosshow`, `ABR_image_transport`, `ros2_kortex_vision`,
`moveit2` (a fork of the upstream MoveIt 2 repository itself, not
ALeRT-specific code). None of these were named in the task's list; they
are noted here only so the inventory is complete, not because they are
assumed relevant.

## Cross-cutting findings worth flagging explicitly

1. **`kinova_stuffs` vs `ros2_kortex`**: the team's own README says they
   are migrating from the former to the latter, while noting the former
   "works perfectly fine with ROS2 Humble." Any manipulation tutorial
   should present `ros2_kortex` as the forward path and `kinova_stuffs` as
   a currently-working but soon-to-be-superseded alternative — not silently
   pick one without saying so.
2. **`Dsp` is a ROS 1 package** (Melodic/Noetic, `catkin build`), despite
   living in an otherwise ROS 2 organisation and being relevant to the
   D*/D*-Lite topic this task asks for. It must not be presented as ROS 2
   Humble-compatible without independent confirmation.
3. **`octomap_rviz_plugins`'s README uses ROS 1-era phrasing** ("ROS groovy
   and later") — its ROS 2 compatibility is plausible (it is commonly used
   with the ROS 2 `octomap_mapping` fork) but not confirmed by the text
   fetched in this audit.
4. **`webots_ros2_go2`'s Go2 support is explicitly unfinished** per its own
   README's "(Todo)" heading — any Go2 content on the new site must be
   marked Experimental, not presented as a working platform alongside Spot.
5. **Several named repositories have no README at all** (`spot_gen3_moveit`,
   `alert_auto_dexterity`, `Estop-detection`, `rrl_image_view`,
   `alert_exploration`, and effectively `pose_detection`, `frame_server`,
   `frame_panel`, `gpp_action_examples` whose READMEs are a bare title).
   Their purpose above is inferred from the repository name and the org's
   one-line description only — marked "Repository exists", not
   "Repository documented", throughout.
6. **The real manipulator hardware is now confirmed**: a Kinova Gen3
   7-DOF arm, a Robotiq 2F-85 gripper, and an Intel RealSense vision
   module (from `ros2_kortex`'s own README) — this is the concrete
   grounding for Work Packages 4 through 10 rather than an assumption.
