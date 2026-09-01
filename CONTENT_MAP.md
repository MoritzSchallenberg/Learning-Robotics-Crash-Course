# Content map

Inventory of every source document analysed for this website.

**Sources:** 78 HTML/HTM documents across three exports
(ROS Summer School, ALeRT/Spot, Carologistics wiki).
**Analysed:** 2026-09-01.

## Legend

| Column | Meaning |
|---|---|
| **Platform** | SS = Summer School · AL = ALeRT/Spot · CL = Carologistics · — = generic |
| **OS / ROS** | As stated in the source. `?` = not stated. |
| **General** | Suitability for the shared course: **Y** yes · **P** partly · **N** no |
| **Team** | Suitability as a team-specific addition |
| **Target** | Where it landed on the new site, or the reason it did not |

Abbreviations for targets: `C1`–`C8` = course sessions, `HK` = hackathon,
`P-sim` / `P-cl` / `P-al` = platform pages, `R-*` = reference pages,
`PR-*` = prerequisites.

---

## 1. ROS Summer School

Ubuntu release not stated in the export; ROS 2 **Humble** implied
(`/opt/ros/humble/...` paths). Written for physical hardware: an iRobot Create 3
base with an onboard mini-PC, RPLidar C1 and Intel RealSense camera.

| # | Source file | Topics | Learning goal | Assumes | Platform | OS / ROS | Hardware | Software | Duplicates | Notes | General | Team | Target |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | `index.html` | Site TOC | — | — | SS | — | — | Sphinx | — | Structure only | Y | N | Site nav model |
| S2 | `S1/1_terminal` | Terminal, Terminator, shortcuts | Operate a terminal | none | — | Linux | — | bash, terminator | AL P1, CL | — | **Y** | N | `PR-linux-terminal` |
| S3 | `S1/2_navigation` | Filesystem, paths, `ls`/`cd`/`mkdir`/`touch` | Navigate Linux | S2 | — | Linux | — | bash | — | Clearest of the three | **Y** | N | `PR-linux-terminal` |
| S4 | `S1/3_filesystem` | ROS 2 nodes, packages, workspace, `colcon` | Build a workspace | S3 | — | Humble | — | ROS 2, colcon | AL P1, CL Task1 | Uses `$ROS_DISTRO` — portable | **Y** | N | `C2`, `PR-installation` |
| S5 | `S1/4_bashrc` | `.bashrc`, sourcing, aliases | Configure the shell | S3 | — | Humble | — | bash | AL, CL | Mentions `/opt/ros/humble` explicitly | **Y** | N | `PR-linux-terminal` |
| S6 | `S1/5_nodes` | Writing a Python node, `setup.py`, entry points | Write and run a node | S4 | — | Humble | — | rclpy, VS Code | AL P1 | Contains a maintainer's local build path in a diff | **Y** | N | `C2` |
| S7 | `S1/6_launch_files` | YAML launch, namespaces, includes | Start several nodes | S6 | — | Humble | — | ROS 2 launch | CL | Good progression | **Y** | N | `C2` |
| S8 | `S1/7_parameters` | Parameters via CLI, launch and code | Configure nodes | S7 | — | Humble | — | ROS 2 | AL | FH mint-green turtlesim example kept | **Y** | N | `C2` |
| S9 | `S2/1_publishers_and_subscribers` | Pub/sub, both function and class style | Use topics | S6 | — | Humble | — | rclpy, std_msgs | AL P1 | Most thorough pub/sub treatment of the three | **Y** | N | `C2` |
| S10 | `S2/2_networking` | `ROS_DOMAIN_ID`, `ROS_LOCALHOST_ONLY`, SSH, keys, VS Code Remote | Reach a robot | S5 | SS | Humble | Create 3 | ssh | CL remote-hosts | Contains institute IP prefix and a device address | **Y** | P | `PR-networking` |
| S11 | `S2/3_republisher` | Subnets, netmasks, why topics don't cross, republisher | Understand ROS 2 networking | S10 | SS | Humble | Create 3 + NUC | `create3_examples` | — | Concept is general; the package is Create-3-specific | **P** | Y | `PR-networking` (concept) |
| S12 | `S2/4_joystick_teleop` | `joy` node, teleop, dead-man switch | Drive by gamepad | S9 | SS | Humble | Gamepad | `joy` | — | Good exercise set | **P** | N | `C2` task ideas |
| S13 | `S3/1_tf2` | Static transforms, frame tree, RViz TF | Publish and read transforms | S7 | — | Humble | — | tf2_ros | AL, CL | Concrete frame table reused verbatim as the task | **Y** | N | `C3` |
| S14 | `S3/2_lidar` | LaserScan, QoS, TF for sensors, launch composition | Visualize laser data | S13 | SS | Humble | RPLidar C1 | `rplidar_ros` | AL 2D lidar | **Contains an internal GitLab clone URL** | **Y** | P | `C3` |
| S15 | `S4/1_camera_calibration` | Intrinsics, distortion, checkerboard procedure | Calibrate a camera | S9 | — | Humble | Webcam | `usb_cam`, `camera_calibration` | — | Only calibration treatment in any source | **Y** | N | `C4` |
| S16 | `S4/2_apriltags` | AprilTag detection, tag families, TF listener, marker follower | Localize a marker | S13, S15 | SS | Humble | RealSense | `apriltag_ros` | AL ArUco | Includes a launch file that disables robot safety reflexes | **Y** | P | `C4` |
| S17 | `S4/3_aruco` | ArUco as "advanced" | — | S16 | — | Humble | — | aruco | AL P2 | **Source is truncated mid-sentence** | **P** | N | `C4` (merged with AL) |
| S18 | `S5/1_mapping` | SLAM Toolbox, config, mapping best practice, saving | Build a map | S14 | — | Humble | — | `slam_toolbox` | AL P3 | Best-practice list is excellent and was kept | **Y** | N | `C5` |
| S19 | `S5/2_localization` | Odometry, AMCL, `map_server`, lifecycle manager | Localize on a map | S18 | — | Humble | — | `nav2_amcl` | AL P3 | Contains an implausible `initial_pose` example value | **Y** | N | `C5` |
| S20 | `S6/1_nav2` | Nav2 architecture, servers, costmaps, full params | Navigate autonomously | S19 | — | Humble | — | `nav2` | AL P3, CL nav2 | Largest single document; params are Turtlebot-sized | **Y** | N | `C6` |
| S21 | `S6/2_autonomous_exploration` | Action client, random goals, workshop task list | Send goals from code | S20 | — | Humble | — | `nav2_msgs` | — | Rich set of extension tasks | **Y** | N | `C6`, `HK` |
| S22 | `S7/yolo` | YOLOv8, CUDA, ROS node, custom training, labeling | Detect objects | S15 | — | Humble | NVIDIA GPU | ultralytics, torch | AL P4, CL labeling | Includes a numpy downgrade workaround | **Y** | N | `C4` |
| S23 | `Robot Challenge/challenge` | Autonomous explorer challenge, scoring node | — | all | SS | Humble | Create 3 | rclpy | — | Scoring node reused as the hackathon model | **Y** | N | `HK` |

---

## 2. ALeRT / Spot

**Ubuntu 22.04, ROS 2 Humble, Webots R2023b** — stated explicitly.

| # | Source file | Topics | Learning goal | Assumes | Platform | OS / ROS | Hardware | Software | Duplicates | Notes | General | Team | Target |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A1 | `ALeRT Team Page` | Team overview, TOC | — | — | AL | — | — | — | — | Structure only | N | Y | `P-al` intro |
| A2 | `Tutorials/01 Introduction` | RoboCup Rescue context, videos, TDP | Motivation | — | AL | — | — | — | — | Video links unverified; TDP link external | P | **Y** | `P-al` |
| A3 | `Tutorials/02 Installation Guide` | Ubuntu 22, Humble, Webots R2023b, WSL caveats | Install the stack | — | AL | 22.04 / Humble | — | Webots | CL setup, SS | WSL section is detailed and version-fragile | **P** | **Y** | `PR-installation`, `P-al` |
| A4 | `Tutorials/03 P1 First Steps` | Terminal, workspace, turtlesim circle task | ROS 2 basics | A3 | — | Humble | — | turtlesim | S2–S9 | Thin — mostly links to official tutorials | **P** | N | Merged into `C2` |
| A5 | `Tutorials/04 P2 Image Processing` | Webots Spot sim, RViz setup, ArUco, line following, HSV | OpenCV in ROS | A4 | AL | Humble | — | OpenCV, cv_bridge | S17, CL vision | **Best ArUco and HSV material in any source** | **Y** | **Y** | `C4`, `P-al` |
| A6 | `Tutorials/05 P3 Services and Actions` | Services, actions, 2D lidar from 3D, SLAM, Nav2 | Services, actions, mapping | A5 | AL | Humble | — | slam_toolbox, nav2 | S18–S20 | Nav2 prose has heavy OCR corruption ("navigaton", "acton") | **Y** | **Y** | `C2`, `C5`, `C6`, `P-al` |
| A7 | `Tutorials/06 P4 YOLO and Moveit` | YOLOv8 + OpenVINO, MoveIt, pick and place, IK | Manipulation | A6 | AL | Humble | — | openvino, moveit2 | S22 | Pick-and-place code is badly mangled by the export | **P** | **Y** | `C4`, `C7`, `P-al` |
| A8 | `Tutorials/07 P5 RAFCON Basics` | RAFCON FSM, states, ports, GVM, ROS in states | Build a state machine | A6 | — | Humble | — | RAFCON | — | **Only high-level-control tutorial in any source** | **Y** | **Y** | `C7` |
| A9 | `Tutorials/08 ROS 2 Cheatsheet` | CLI command reference | Reference | — | — | Humble | — | ROS 2 | — | Good base; expanded substantially | **Y** | N | `R-cheatsheet` |
| A10 | `Spot Docs/00 General Information` | RoboCup Rescue challenge categories | Context | — | AL | — | — | — | — | Mostly images; rulebook links | P | **Y** | `P-al` |
| A11 | `Spot Docs/01 Gesture detection` | MediaPipe hand gestures → `cmd_vel` | Optional project | A5 | AL | Humble | Camera | mediapipe | — | Self-contained optional project | P | **Y** | `P-al` |
| A12 | `Spot Docs/02 Navigation` | Nav2, 3D planning, mesh navigation | — | — | AL | Humble | — | mesh_navigation | S20 | **Links only — no content** | N | **P** | `P-al` (overview + TODO) |
| A13 | `Spot Docs/03 Octomapping` | Octomap install | — | — | AL | Humble | — | octomap | — | **Links only** | N | **P** | `C5` mention, `P-al` |
| A14 | `Spot Docs/05 GLIM Mapping` | GLIM install | — | — | AL | Humble | — | glim_ros2 | — | **Links only** | N | **P** | `C5` mention, `P-al` |
| A15 | `Spot Docs/06 High-Level` | Golog++, PlanSys2 | — | — | AL | Humble | — | gologpp, plansys2 | — | **Links only** | N | **P** | `C7` overview + TODO |
| A16 | `Spot Docs/07 Challenges` | One-line challenge list | — | — | AL | — | — | — | A10 | **Essentially empty** | N | P | `P-al` |
| A17 | `Spot Docs/08 Spot Startup` | Physical Spot operation, E-stops, controller, faults | Operate Spot | — | AL | — | Spot | — | — | **Wi-Fi name, saved credentials reference, personal name, device IP path** | N | **P** | `P-al` (safety summary only) |
| A18 | `Spot Docs/index`, `Tutorials/index` | TOC | — | — | AL | — | — | — | — | Structure only | N | N | — |

---

## 3. Carologistics

**Ubuntu 24.04 / ROS 2 Jazzy** per the introductory task; **Fedora** on robots
and some workstations; several repositories document **Humble**. Exported from
a GitHub wiki, so many pages carry heavy site chrome and several failed to
render.

| # | Source file | Topics | Learning goal | Assumes | Platform | OS / ROS | Hardware | Software | Duplicates | Notes | General | Team | Target |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K1 | `00 Home` | Wiki TOC | — | — | CL | — | — | — | — | Structure only | N | N | — |
| K2 | `01/01 First-Steps` | Team onboarding, Slack, meetings, IP request | Join the team | — | CL | — | — | — | — | Internal onboarding + fixed-IP request | N | **P** | Excluded (internal org) |
| K3 | `01/02 Network-Setup` | SSID, addressing, gateway, device admin, resets | — | — | CL | — | — | — | — | **Cleartext credentials ×2, SSID, full internal addressing** | N | N | **Excluded — see SECURITY_REVIEW C-1, C-2** |
| K4 | `01/03 Git-Workflows` | Git config, branches, commit format, rebase, recovery | Use Git the team's way | — | — | — | — | git, pre-commit | — | **Best Git material in any source** | **Y** | **Y** | `PR-git` |
| K5 | `01/04 Working-on-Remote-Hosts` | IP map, SSH, screen, scp, git diffs, VNC | Work on robots | K3 | CL | — | — | ssh, screen | S10 | **Cleartext credential, full host/IP table** | **P** | **P** | Practices → `PR-networking`, `P-cl`; **rest excluded** |
| K6 | `01/05 Licensing-of-Software` | — | — | — | CL | — | — | — | — | **Page does not exist ("Create new page")** | N | N | Excluded (empty) |
| K7 | `02/01 Agenda` | Meeting notes, motors, sponsors, travel | — | — | CL | — | — | — | — | **Personal names, travel/visa discussion** | N | N | **Excluded — personal data** |
| K8 | `02/02 Milestones` | Milestone table with owners and deadlines | — | — | CL | — | — | — | — | **Personal names** | N | N | **Excluded — personal data** |
| K9 | `03 Ros2-Introductory-Task` | Ubuntu 24.04, Jazzy, Cyclone DDS, Webots, task list | Onboard to ROS 2 | — | CL | 24.04 / Jazzy | — | ROS 2, Webots | S4–S9, A4 | **The Jazzy/Humble conflict originates here**; DDS config is genuinely useful | **P** | **Y** | `PR-networking` (DDS), `P-cl`, `R-compatibility` |
| K10 | `04/01 Installing Programs` | Fusion 360, KiCad, PrusaSlicer | Install CAD tools | — | CL | — | — | — | — | Hardware-team tooling, not robotics software | N | **Y** | `P-cl` (brief) |
| K11 | `04/02 CAD-Tutorial` | Fusion tutorial link, cloud access | — | K10 | CL | — | — | Fusion | — | **Names an individual; "send account details"** | N | P | `P-cl` (tool only); rest excluded |
| K12 | `04/03 Circuit-Diagram-Tutorial` | KiCad | — | K10 | CL | — | — | KiCad | — | Out of scope for a ROS 2 course | N | P | Excluded (out of scope) |
| K13 | `04/04 System-Overview` | Full hardware and software inventory | Understand the system | — | CL | — | Robotino | — | — | **Excellent architecture source**; many TODOs | **Y** | **Y** | `C1`, `P-cl` |
| K14 | `05/01 Automated-Setup-using-Ansible` | Ansible concepts, playbooks, tags, deployment | Deploy software | K5 | CL | Fedora | — | ansible | K21 | Clear explanation of idempotence and tags | **Y** | **Y** | `C8`, `P-cl` |
| K15 | `05/02 Setting-up-Fedora` | Fedora setup, ssh keys, `ansible-pull` | Set up a workstation | — | CL | Fedora | — | ansible | — | Fedora-only commands | N | **Y** | `P-cl` |
| K16 | `05/03 Starting-a-Robot` | Power on, screen session, RViz localization, deploy | Start a robot | K5, K14 | CL | — | Robotino | — | S19 | Localization procedure is the general one | **P** | **Y** | `P-cl` |
| K17 | `05/04 Setting-up-the-Refbox` | Referee box setup | — | — | CL | — | — | refbox | — | Competition infrastructure | N | **P** | Excluded (internal ops) |
| K18 | `05/05 Starting-a-Test-Game` | Central agent startup | — | K16, K17 | CL | — | — | fawkes | — | Internal paths and scripts | N | **P** | `P-cl` (brief) |
| K19 | `05/06 Official-Competitions` | — | — | — | CL | — | — | — | — | **Content is "TBD"** | N | N | Excluded (empty) |
| K20 | `05/07 Labeling-Data` | Roboflow workflow, conveyor/slide/workpiece label rules | Label a dataset | — | CL | — | — | Roboflow | S22 | **10 signed JWT image URLs**; label rules are excellent | **Y** | **Y** | `C4` (rules), `P-cl`; **images excluded** |
| K21 | `05/08 VNC Connection to Robot` | TigerVNC, SSH tunnel, server setup | Remote desktop | K5 | CL | — | — | tigervnc | K5 | VNC password *setup* described, no value shown | **P** | **Y** | `P-cl` (mention) |
| K22 | `06/01 ansible` | Ansible project detail | — | K14 | CL | Fedora | — | ansible | K14 | Duplicate of K14 | N | Y | Merged into K14 target |
| K23 | `06/02 expertino-rcll` | Central goal reasoning agent | — | — | CL | — | — | CLIPS | — | **GitHub page with no README** | N | **P** | `P-cl` (name only) |
| K24 | `06/03 fawkes-robotino` | Fawkes framework | — | — | CL | — | — | fawkes | — | Links to an internal wiki and KBSG VNC | N | **P** | Excluded (internal links) |
| K25 | `06/04 gripper-pi-img` | Raspberry Pi network boot image | — | — | CL | Raspbian | Pi | nfs | — | **Internal NFS server address** | N | P | **Excluded — SECURITY_REVIEW N-3** |
| K26 | `06/05 hardware` | Hardware wiki landing page | — | — | CL | — | — | — | — | **Nearly empty** | N | P | Excluded (empty) |
| K27 | `06/06 laser_scan_integrator` | Merge two laser scans using TF | — | — | CL | — | 2× SICK | — | — | **No README**; description from repo metadata | N | **Y** | `P-cl` |
| K28 | `06/07 mps-map-gen` | Extend a map with machines and field bounds | — | — | CL | — | — | nav2 | — | Genuinely informative wiki page | N | **Y** | `P-cl` |
| K29 | `06/08 new gripper calculation` | — | — | — | CL | — | — | — | — | **A PDF file listing, no content** | N | N | Excluded (no content) |
| K30 | `06/09 navigation2` | Upstream Nav2 README (team fork) | — | — | — | Humble/Iron | — | nav2 | S20 | **Upstream project README, not team content** | N | N | Excluded (upstream; linked instead) |
| K31 | `06/09 pre-commit` | Team pre-commit configuration | — | K4 | CL | — | — | pre-commit | — | Repo listing; concept covered in K4 | **P** | Y | `PR-git` |
| K32 | `06/10 rcll_simulation_webots` | RCLL Webots simulation description | — | — | CL | — | — | Webots | A5 | Good description, no procedure | **P** | **Y** | `P-cl`, `P-sim` |
| K33 | `06/11 rcll-protobuf` | Refbox protobuf interface | — | — | CL | — | — | protobuf | — | **Empty README section** | N | P | `P-cl` (name only) |
| K34 | `06/12 robotino_navigation` | Nav2 config for Robotino, 2× SICK TiM571 | — | S20 | CL | **Humble** | Robotino | nav2 | S20 | **States Humble — conflicts with K9's Jazzy** | N | **Y** | `P-cl`, `R-compatibility` |
| K35 | `06/13 ros2-markerless-mps` | Markerless machine detection | — | — | CL | — | — | — | K36 | **No README** | N | **Y** | `P-cl` |
| K36 | `06/14 Vision-System` | Tag vision, Pi cam, object tracking, markerless MPS | Understand the vision stack | — | CL | — | Robotino | YOLOv8 | S22, A5 | **Best CL technical page**; laser-line triangulation is the key idea | **P** | **Y** | `C4`, `P-cl` |

---

## 4. Aggregate

### By disposition

| Disposition | Count |
|---|---|
| Used substantially for the general course | 27 |
| Used for platform pages only | 18 |
| Merged into another page (duplicate) | 12 |
| Excluded — secrets or personal data | 6 |
| Excluded — empty, truncated, or upstream content | 9 |
| Excluded — internal operations or out of scope | 6 |
| Structure only (navigation pages) | 5 |

### Cross-source duplication

The topics that appeared in more than one source, and where each is now
explained **once**:

| Topic | Sources | Single home |
|---|---|---|
| Terminal, shortcuts | S2, A4, K9 | `PR-linux-terminal` |
| Linux filesystem, paths | S3 | `PR-linux-terminal` |
| `.bashrc`, sourcing | S5, A3, K9 | `PR-linux-terminal` |
| Workspace, packages, colcon | S4, A4, K9 | `C2` |
| Nodes | S6, A4 | `C2` |
| Topics, pub/sub | S9, A4, A9 | `C2` |
| Parameters | S8, A9 | `C2` |
| Launch files | S7, A9, K9 | `C2` |
| Services and actions | S21, A6, A9 | `C2` (intro), `C7` (use) |
| ROS 2 CLI | S4, A9 | `R-cheatsheet` |
| Networking, SSH | S10, S11, K5, K9 | `PR-networking` |
| Webots | A3, A5, K9, K32 | `P-sim` + platform pages |
| RViz | S13, S14, A5, A6 | `C3` |
| TF2 | S13, S16, A7 | `C3` |
| LiDAR, LaserScan | S14, A6 | `C3` |
| ArUco, AprilTags | S16, S17, A5, K36 | `C4` |
| YOLO | S22, A7, K36 | `C4` |
| Data labeling | S22, K20 | `C4` |
| Mapping, SLAM | S18, A6 | `C5` |
| Localization, AMCL | S19, A6, K16 | `C5` |
| Nav2 | S20, A6, A12, K30, K34 | `C6` |
| Autonomous missions | S21, A8, A15 | `C7` |
| Ansible | K14, K22, K15 | `C8` + `P-cl` |

### Source quality notes

**Truncated or corrupted in the export:**
S17 (ends mid-sentence), A6 (OCR damage in the Nav2 prose), A7 (code flattened
into a single line).

**Link-only pages with no substance:**
A12, A13, A14, A15, A16, K23, K26, K27, K29, K33, K35.
These became overview mentions with a **TODO-REVIEW** marker rather than
invented instructions.

**Internally contradictory:**
K9 (Jazzy) versus K34 (Humble) — recorded in
[`docs/reference/compatibility.md`](docs/reference/compatibility.md).

**Hardware-specific content that was generalised:**
The Summer School material assumed an iRobot Create 3 with a specific
mini-PC, LiDAR and camera. Topic names, driver packages and addresses were
replaced with the general concept, and platform specifics moved to the platform
pages.

---

See also: `CONTENT_REVIEW.md` (included / merged / platform-specific /
excluded) and `SECURITY_REVIEW.md` (findings and remediation).
