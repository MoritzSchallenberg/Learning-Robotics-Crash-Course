# Content review

What was published, what was merged, what is platform-specific, and what was
left out — so that the next development round can decide what to remove, extend
or move.

Companion documents: `CONTENT_MAP.md` (per-source inventory) and
`SECURITY_REVIEW.md` (secrets and sensitive data).

Source identifiers (`S*`, `A*`, `K*`) refer to `CONTENT_MAP.md`.

---

## 1. Included

Content taken over in full or consolidated into the shared course.

### Prerequisites

| Page | From | Notes |
|---|---|---|
| `prerequisites/linux-terminal.md` | S2, S3, S5 | Terminal, filesystem, paths, `.bashrc`, sourcing, aliases. Rewritten as one narrative with a task and a common-mistakes section. |
| `prerequisites/installation.md` | S4, A3, K9 | Ubuntu, ROS 2, workspace, simulator, editor. Version choice is presented as a **decision** the reader must make, not a default. |
| `prerequisites/git.md` | K4, K31 | The strongest Git material in any source. Kept close to the original, including the team's branch and commit conventions. Added a warning about committing secrets. |
| `prerequisites/networking.md` | S10, S11, K9 | Domain IDs, `ROS_LOCALHOST_ONLY`, SSH, keys, subnets, the republisher concept, Cyclone DDS. All real addresses removed. |

### Course sessions

| Page | From | Notes |
|---|---|---|
| `course/01-system-hardware.md` | K13, plus hardware sections of S/A | Written largely fresh. No source had a general "how a robot is built" chapter; K13's inventory supplied the concrete detail and the Robotino/Spot comparison. |
| `course/02-ros2.md` | S4, S6, S7, S8, S9, A4, A6, A9, K9 | The largest consolidation on the site: six documents from three sources merged into one progression. |
| `course/03-sensors-tf.md` | S13, S14, A5, A6 | TF2 and LaserScan merged. The QoS troubleshooting section is assembled from warnings scattered across four source documents. |
| `course/04-perception.md` | S15, S16, S17, S22, A5, A7, K20, K36 | Calibration → OpenCV → markers → YOLO → training, in one arc. The detection-versus-localization distinction is added as the organising idea. |
| `course/05-mapping-localization.md` | S18, S19, A6, K16 | Odometry, occupancy grids, SLAM Toolbox, AMCL. Adds a diagnostic table distinguishing odometry from localization failure. |
| `course/06-navigation.md` | S20, S21, A6 | Nav2 architecture, costmaps, configuration, goals from code, exploration. |
| `course/07-autonomous-decisions.md` | A8, A15, A7 | State machines, behavior trees, RAFCON, MoveIt. The FSM-versus-BT comparison is added. |
| `course/08-integration.md` | K14, plus practice from all three | Written largely fresh. The eight-step debugging procedure is assembled from troubleshooting advice scattered across the sources. |
| `course/hackathon.md` | S23 | The scoring node is modelled on the Summer School's, restructured into three difficulty levels with an explicit point table. |

### Reference

| Page | From | Notes |
|---|---|---|
| `reference/ros2-cheatsheet.md` | A9, plus commands used throughout | A9's list roughly tripled, grouped by intent, with a diagnostic sequence. |
| `reference/compatibility.md` | K9, K34, A3, S5 | New. Exists specifically to record the version conflicts found in the sources. |
| `reference/glossary.md` | all | New. Every term used on the site. |
| `reference/sources.md` | all | New. Attribution, method, exclusions, licensing. |

---

## 2. Merged

Topics that appeared in two or three sources and are now explained **once**.
The rule applied: use the Summer School's structured version as the base,
improve it with better explanations, warnings and exercises from ALeRT and
Carologistics, and rewrite the result rather than concatenating variants.

| Topic | Sources | New home | What each contributed |
|---|---|---|---|
| Terminal and shortcuts | S2, A4, K9 | `PR-linux-terminal` | S2 base; A4's shortcut list confirmed it |
| Linux filesystem, paths | S3 | `PR-linux-terminal` | Only full treatment |
| `.bashrc`, sourcing, aliases | S5, A3, K9 | `PR-linux-terminal` | S5 base; K9's DDS variables moved to networking |
| Workspace, packages, colcon | S4, A4, K9 | `C2` | S4 base; A4's official-tutorial links kept as further reading |
| Nodes | S6, A4 | `C2` | S6 base, with its clean shutdown pattern |
| Topics, publisher, subscriber | S9, A4 | `C2` | S9 base; class-based style preferred over the global-variable version |
| Parameters | S8 | `C2` | S8, condensed |
| Launch files | S7, A9, K9 | `C2` | S7 base; the YAML-plus-Python composition idea from S11/S14 |
| Services and actions | S21, A6, A9 | `C2` intro, `C7` use | A6 supplied the service examples, S21 the action client |
| ROS 2 CLI | S4, A9 | `R-cheatsheet` | A9 base, substantially extended |
| Networking and SSH | S10, S11, K5, K9 | `PR-networking` | S10 base; S11's subnet explanation; K5's practices; K9's DDS config |
| Webots | A3, A5, K9, K32 | `P-sim` + platform pages | Shared concepts on `P-sim`, specifics on the platform pages |
| RViz | S13, S14, A5, A6 | `C3` | A5's explicit display list; the QoS warnings from all four |
| TF2 | S13, S16 | `C3` | S13's frame table became the task; S16's listener became the code example |
| LiDAR and LaserScan | S14, A6 | `C3` | S14 base; A6 supplied the annotated message and the `.inf` caution |
| ArUco and AprilTags | S16, S17, A5, K36 | `C4` | A5's ArUco code is the best; S16 supplied AprilTag and the size warning |
| YOLO | S22, A7, K36 | `C4` | S22 base; A7's OpenVINO path noted for CPU-only machines |
| Data labeling | S22, K20 | `C4` + `P-cl` | S22's workflow; K20's tight-boxes rule, which is the important part |
| Mapping and SLAM | S18, A6 | `C5` | S18 base, including its best-practice driving list |
| Localization and AMCL | S19, A6, K16 | `C5` | S19 base; the lifecycle-manager warning made explicit |
| Nav2 | S20, A6, K30, K34 | `C6` | S20 base; K30 excluded as upstream content |
| Autonomous missions | S21, A8, A15 | `C7` | A8 base for RAFCON; Nav2's own BT used as the worked example |
| Ansible | K14, K15, K22 | `C8` + `P-cl` | K14's concepts are general; K15's Fedora specifics are team-only |

**Duplication removed:** 23 topics that appeared 2–4 times across the sources
are now single pages. No page contains two variants of the same explanation.

---

## 3. Platform-specific

Content that applies to one system only, kept off the shared pages.

### `platforms/simulation.md` {SIMULATION}

From A3, A5, K9, K32 and the `webots_ros2` documentation. Webots installation,
simulation-time handling, finding topic names, a session-by-session note on
what differs, and a route through the whole course with no team hardware.

### `platforms/carologistics-robotino.md` {CAROLOGISTICS}

| Content | From |
|---|---|
| RCLL context, exploration phase, why precision matters | K13, K28 |
| Robotino hardware, omnidirectional drive | K13 |
| Software stack overview | K13 |
| Key repositories and what each does | K27, K28, K32, K34, K35, K23, K33 |
| Ansible workstation setup | K15 |
| Robot startup, screen sessions, localization | K16 |
| Deployment | K14 |
| Test game startup | K18 |
| Tag vision, laser lines, object tracking | K36 |
| Markerless MPS detection | K36, K35 |
| Data labeling class rules | K20 |
| CAD and hardware tooling | K10 |

**Version conflict flagged prominently:** the Jazzy/Humble contradiction between
K9 and K34.

### `platforms/alert-spot.md` {ALERT}

| Content | From |
|---|---|
| Rescue League context and challenge categories | A2, A10 |
| Webots Spot simulation, launch, topics, RViz | A5, A6 |
| 3D-to-2D scan conversion, cone scan exercise | A6 |
| Services and actions on Spot | A6 |
| Image processing exercises | A5 |
| Mapping and navigation launch files | A6 |
| Octomap, GLIM, mesh navigation | A12, A13, A14 — overview + TODO |
| MoveIt | A7 |
| YOLO with OpenVINO, hazmat signs | A7 |
| Gesture control | A11 |
| High-level control links | A15 |
| Physical Spot operation | A17 — safety-focused summary only |

### Version-specific markers

Platform and distribution badges are applied throughout:
`COMMON`, `SIMULATION`, `CAROLOGISTICS`, `ALERT`, `ROS 2 JAZZY`,
`ROS 2 HUMBLE`, `UNVERIFIED`.

---

## 4. Excluded or pending

### 4.1 Excluded — secrets or personal data

Full detail in `SECURITY_REVIEW.md`. No values are repeated here.

| Source | Category | Reason |
|---|---|---|
| K3 `Network-Setup` | Credentials, SSID, internal addressing | Cannot be published; not needed for a course |
| K5 `Working-on-Remote-Hosts` | Credential, host/IP table | Practices extracted; the rest excluded |
| K7 `Agenda` | Personal names, travel plans | Personal data; internal organisation |
| K8 `Milestones` | Personal names and assignments | Personal data; internal organisation |
| K11 `CAD-Tutorial` | Named individual, account-detail request | Personal data |
| K25 `gripper-pi-img` | Internal NFS address | Internal infrastructure |
| A17 `Spot Startup` | Wi-Fi name, stored-credential reference, device path | Reduced to a safety summary |

### 4.2 Excluded — internal operations, not course content

| Source | Reason | Reconsider? |
|---|---|---|
| K2 `First Steps` | Team onboarding: Slack, meetings, IP request | Belongs in an internal wiki |
| K17 `Setting-up-the-Refbox` | Competition infrastructure | Possibly on `P-cl` if made generic |
| K19 `Official-Competitions` | Content is literally "TBD" | If it is ever written |
| K24 `fawkes-robotino` | Links to an internal wiki and internal VNC | Only if a public description exists |
| K12 `Circuit-Diagram-Tutorial` | KiCad tutorial — out of scope for a ROS 2 course | Fits a hardware course, not this one |

### 4.3 Excluded — empty, truncated or upstream content

| Source | Reason |
|---|---|
| K6 `Licensing-of-Software` | The page does not exist; the export captured "Create new page" |
| K26 `hardware` | Wiki landing page with one line |
| K29 `new gripper calculation` | A PDF file listing with no readable content |
| K30 `navigation2` | The upstream Nav2 README, not team content — linked instead of copied |
| A16 `Challenges` | One sentence, duplicating A10 |
| S17 `Aruco (Advanced)` | Truncated mid-sentence in the source; merged with A5's complete ArUco material |

### 4.4 Images — all excluded, pending provenance

**No image from the source material is published.** This is the largest
deliberate omission and the most reversible.

| Image group | Source | Why excluded | To resolve |
|---|---|---|---|
| Labeling reference images (10) | K20 | Served from signed, expiring private URLs carrying credential material | Re-host from the original files, confirm rights |
| Site and team logos | S, A | Logo usage rights not established | Institute confirmation; site currently uses a text title |
| RViz and tool screenshots | S, A | Origin clear (team-made) but not licensed for publication | Simple: teams confirm, or new screenshots are taken |
| Robot and arena photographs | A, K | Mixed provenance; some may be from competition organisers | Identify photographers; use only team-owned images |
| Competition rulebook diagrams | A10 | Copyright held by RoboCup organisers | Link to the rulebook instead |
| Hardware diagrams, CAD, circuits | K | Team-owned but not reviewed | Team confirmation |

**Consequence:** the site currently relies on typography and text diagrams. It
reads well, but several topics would be clearer with a picture — the TF tree,
the Nav2 architecture, the marker examples, and the labeling rules in
particular.

**Recommendation:** producing a small set of newly made screenshots is likely
faster than establishing provenance for the existing ones.

### 4.5 Pending technical review

Marked on the site with a visible **TODO-REVIEW** admonition.

| Location | What needs review | Why |
|---|---|---|
| `C5` — Octomap and GLIM | Configuration, parameters, a tested procedure | Sources are link-only (A13, A14) |
| `C7` — PlanSys2 and Golog++ | A worked example and tested installation | Sources are link-only (A15) |
| `P-al` — Octomap, GLIM, mesh navigation | The same, plus current branch status | A12, A13, A14 |
| `P-cl` — markerless MPS detection | Current status: research or deployed? | K36 describes work in progress |
| `P-cl` — gripper | The control interface | K13 lists hardware; no interface documentation exists |
| `hackathon.md` | Point values, time limit, arena layout | Published as an explicit draft for criticism |
| `reference/sources.md` | The content license | Not yet decided by the institute |
| `reference/compatibility.md` | The Carologistics Jazzy/Humble conflict | Requires testing on real hardware |

### 4.6 Content deliberately generalised

Not excluded, but changed enough to note.

| Original | Change | Why |
|---|---|---|
| Summer School hardware specifics (Create 3, RPLidar, RealSense, NUC) | Replaced with general concepts; topic names shown as placeholders | The course must serve three platforms, not one |
| S14's LiDAR driver clone URL | Removed | Internal GitLab, personal namespace |
| S16's launch file disabling safety reflexes | Excluded; replaced with a general warning about disabling safety features | Publishing a copy-pasteable safety override on a public site is unwise |
| S19's `initial_pose` example | Removed | The value in the source is implausible and would confuse |
| S22's numpy downgrade workaround | Omitted | Version-specific workaround, likely already stale |
| A3's WSL instructions | Reduced to a note | Version-fragile; native Linux is recommended instead |
| K5, K16's screen-session usage | Kept as practice, hosts removed | The technique is useful; the hosts are internal |

---

## 5. Recommendations for the next round

**Content**

1. Resolve the Jazzy/Humble question with the Carologistics team and update
   `compatibility.md`. This blocks confident setup instructions.
2. Establish image rights, or take new screenshots. This is the biggest
   available improvement to readability.
3. Give Octomap, GLIM, PlanSys2 and Golog++ real content or remove the sections
   — right now they promise more than they deliver.
4. Have the hackathon scoring reviewed against the real arena.
5. Decide the content license.

**Structure**

6. Consider splitting `course/04-perception.md`; it is the longest page and
   covers three distinct techniques.
7. Add a per-platform "first 30 minutes" quick-start.
8. Consider whether the Carologistics gripper and vision material deserves its
   own page rather than sections.

**Process**

9. Have each team review its own platform page for accuracy. Nothing on those
   pages has been verified against running hardware.
10. Add a link checker to CI once the external links have been reviewed once by
    hand.
