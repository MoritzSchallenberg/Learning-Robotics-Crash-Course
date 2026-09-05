# Content audit: source archive ("Tutorial.zip")

**Not part of the published website.** Internal working document for
Entwicklungsauftrag 8 (ALeRT Advanced Robotics Tutorial rebrand).

## What was audited

No file literally named `Tutorial.zip` was found on this machine. The
matching source material — saved HTML pages of the *ALeRT — RoboCup Rescue
Team Page* Sphinx site (theme, copyright line, and content all consistent
with the task's description) — was found already extracted at:

```text
Robotik Crash Course/00-02 Quelle 2 Spot Tutorial/Website Code/
```

19 HTML pages, ~52 MB total (mostly two JPEGs, see Section 3). Every page
was converted to plain text and read in full before any content decision
below. Copyright line on every page: "© Copyright 2024, MASCOR Institute,
FH Aachen." Site version "1.0-r1", built with Sphinx + the Read the Docs
theme (the exact theme/JS/CSS files this task explicitly says not to
carry over — see Section 3).

## 1. Security scan (performed before reading for content decisions)

Scanned all 19 HTML files for credentials, tokens, IP addresses, hostnames,
SSIDs, and personal data.

**Findings** (categories only, no values reproduced):

- **SSID.** The Spot Startup page names the team's actual Wi-Fi network by
  its real SSID. **Action: excluded, replace with `<TEAM_WIFI>` in any
  reused content.**
- **Credential-adjacent statement + a real first name.** The same page's
  troubleshooting section states that browser-saved login credentials for
  the manipulator's web interface exist, and thanks a named team member by
  first name for having saved them. No literal credential value is
  present, but the sentence itself is internal/personal information not
  suitable for a public site. **Action: excluded. Rewritten (if the
  surrounding procedure is reused) as "the manipulator's web interface
  requires separate login; ask your team lead for current access" with no
  name and no reference to saved credentials.**
- **False positive.** A version string ("WSL 2.1.5.0") in the Installation
  Guide matches an IP-address-shaped regex but is not an IP address —
  confirmed by context, not excluded.
- **No hostnames, tokens, API keys, or signed URLs found** in any of the
  19 pages.
- **No further personal data** (no other names, no photos of identifiable
  people flagged as usable — see Section 3) found in the HTML text.

No actual secret (a working password, key or token value) was found in
this archive. If one had been, this report would say so by category only,
per the task's instruction — it does not apply here.

## 2. Per-page audit table

| Source document | Topic | Reusable content | Duplicates | Security status | Technical status | Action |
| --- | --- | --- | --- | --- | --- | --- |
| ALeRT Team Page (top) | Team landing page | Team affiliation (MASKOR Institute, FH Aachen), page structure | Superseded by new site's own Home | Clean | Current | Rewritten |
| Spot Documentation (index) | Section index | None (pure navigation stub) | — | Clean | Current | Excluded |
| 00 General Information | RRL challenge categories (Maneuvering/Mobility, Dexterity, Exploration, Readiness) | General challenge-category vocabulary | Overlaps with current site's platform page | Clean | **Contains 2019-specific rules** ("Challengens 2019" section, explicit arena/task details) presented without a later update; "Updated tasks for smaller teams" section is itself dated (2021 PDF link, marked "not yet published" for 2022) | **Historical** — categories kept as general vocabulary; every 2019-dated rule detail excluded or explicitly marked historical, not current |
| 01 Gesture detection using mediapipe | MediaPipe hand-gesture → `cmd_vel` | Full working install/build/launch sequence, real repo (`mediapipe_ros2`), real topic (`/recognized_gesture`) | New — not yet on current site | Clean | Current (ROS 2 Humble) | **Merged** — becomes the core of the new Perception → Gesture Detection page |
| 02 Navigation | Nav2, 3D path planning, mesh navigation — link stubs only | Pointers to `alert_ros2`'s `plan_3d_path.py`, `naturerobots/mesh_navigation`, `MASKOR/webots_ros2_spot` mesh-nav branch | Already covered more thoroughly on current site's Navigation module and platform page | Clean | Current, but content is link-only (no procedure) | **Merged** — links carried into the new Navigation/Exploration topic, supplemented by the real `octo_navigation` README found in the repository audit |
| 03 Octomapping | OctoMap install pointer | `RRL-ALeRT/octomap_mapping`, one apt command | Already covered on current site | Clean | Current | **Merged** (already superseded by existing, fuller content) |
| 05 GLIM Mapping | GLIM install pointer | Two links | Already covered on current site | Clean | Current | **Merged** (superseded) |
| 06 High-Level | Golog++, PlanSys2 install pointers | Repo links, PlanSys2 docs links | Already covered on current site | Clean | Current | **Merged** (superseded) |
| 07 Challenges | One-sentence description of RRL challenge categories | Category names only | Duplicate of 00 General Information | Clean | Current | Excluded (fold the one sentence into the historical/overview note, not a separate page) |
| 08 Spot Startup | Full physical start/shutdown/E-Stop/manipulator-recovery procedure | **High-value, genuinely new**: two-E-Stop layout, exact startup sequence (power → Steam Deck → Wi-Fi → drivers → E-Stop slider → Start), manipulator recovery steps, confirms Kinova ("Kinova Python" driver) and Steam Deck as the real control device | New — current site has no physical start/shutdown procedure at all | **SSID and named-credit sentence excluded, see Section 1** | Current, but written in an informal/joking tone throughout ("THE ROBOT", Death-Star joke, "reconsider your role here") — must be rewritten in a neutral, factual style before reuse | **Rewritten** — becomes the core of "ALeRT Platforms and Safety → safe start/shutdown sequence, E-Stop systems" |
| Tutorials (index) | Section index | None (navigation stub) | — | Clean | Current | Excluded |
| 01 Introduction | Course framing, video list, "Course Structure" (empty) | RRL history (Kobe earthquake → RoboCup Rescue 2001), TDP link | Mentions a Carologistics/Logistics-League video alongside ALeRT's own — **must be removed per Section 2 of this task** | Clean | Current | **Rewritten** — RRL history and TDP link kept if independently verifiable; course-structure/scheduling language and the Carologistics video reference dropped entirely, consistent with de-scoping this site from a taught course |
| 02 Installation Guide | Ubuntu/ROS 2/Webots install, WSL notes | Superseded — current site's own `docs/course/02-ros2/installation.md` is already more complete and more carefully verified (checked against official ROS 2 Humble docs directly, with expected results and verification steps this page lacks) | Superseded | Clean | Current | **Excluded** (superseded by existing, better content — reuse would be a regression) |
| 03 P1: First Steps | Turtlesim circle-driving task | Superseded — current site's Turtlesim lab (module 2 subpages) is already far more developed | Superseded | Clean | Current | Excluded (superseded) |
| 04 P2: Webots Spot Simulation: Image Processing | ArUco detection + line following on Spot's gripper camera, full RViz setup steps, real code templates | Superseded — current site's perception pages already contain this same content (same dictionary, same HSV approach), verified more thoroughly | Superseded | Clean | Current | Excluded (superseded; the RViz display-setup steps were cross-checked as already present on the current site's practical-exercise pages) |
| 05 P3: Services and Actions | Spot service calls (pushups), SLAM Toolbox mapping, Nav2 | Superseded — current site's modules 2, 5 and 6 already cover this in more depth and with corrected details (e.g. this page's Nav2 explanation has garbled OCR-like text in places, e.g. "constttutes", "Environmental Representaton") | Superseded | Clean | Current, but the Nav2 conceptual paragraph in this source has visible text-encoding corruption | Excluded (superseded; the corrupted paragraph would not have been reused verbatim regardless) |
| 06 P4: YOLO and Moveit | **High-value, genuinely new**: real YOLOv8+OpenVINO node reference, real `/hazmat_signs` service call, and — most importantly — a **complete, real pick-and-place mission script** using custom action-client wrapper classes (`GripperActionClient`, `MoveitIKClientAsync`, `MoveGroupActionClient`, `NavigateToPoseActionClient`, a `GetPose` TF2-listener node) with real joint-angle values for a retract pose | New — current site has no MoveIt/manipulation content at all yet | Clean | Current; the specific approach (a custom IK-solver service + a custom MoveIt joint-goal action client, rather than the standard `MoveGroupInterface`) is the team's own real pattern, not the officially documented interface — **must be presented as "how ALeRT applies it" alongside, not instead of, the standard MoveGroupInterface path** the task requires as the primary taught interface | **Merged and rewritten** — this is the primary technical grounding for Work Packages 5, 7, 8, 9 and 10 |
| 07 P5: RAFCON Basics | Full RAFCON state-machine walkthrough (execute/GVM pattern, ports, wait states) | Superseded — current site's `07-autonomous-decisions/planning-and-manipulation.md` already documents the same `gvm.get_variable`/`execute()` pattern accurately | Superseded | Clean | Current | Excluded (superseded); a few phrasing details (e.g. "never call `rclpy.shutdown()` inside a state, since it would also shut down `init_ros2_node`") were cross-checked as already present |
| 08 ROS 2 Cheatsheet | Command reference | Superseded — current site's `docs/reference/ros2-cheatsheet.md` is already more complete | Superseded | Clean | Current | Excluded (superseded) |

## 3. Images and assets

Three non-theme assets found:

| Asset | Contents | Decision |
| --- | --- | --- |
| `award_ceremony.jpg` | Photograph of people at an award ceremony | **Excluded.** Identifiable people, no consent on record; matches this project's existing, already-established image policy (no photographs of people without separately confirmed rights). |
| `spot_gravel_sitting.jpg` | Photograph of the physical Spot robot, no people visible | **Excluded for now**, flagged as a *candidate* pending explicit rights confirmation from ALeRT/FH Aachen — consistent with the existing site's own prior "Images" policy, which already listed exactly this kind of photo as a future candidate rather than auto-including it. |
| `logo_MASKOR_rechts_square_white-bg_small.png` | MASKOR Institute logo | **Excluded**, consistent with the existing site's established policy of using a text title instead of an institute/team logo whose usage rights were not separately confirmed. |

No EXIF/metadata review was needed for the excluded images since none are
being published from this archive at this time. All Sphinx/RTD theme CSS,
JS and generated HTML from the archive were excluded entirely, per this
task's explicit instruction — nothing beyond the plain-text content above
was reused from any file in the archive.

## 4. Net effect

Of 19 archive pages: **2 pages contain genuinely new, high-value technical
content** not already on the current site (Gesture detection, Spot
Startup) plus **one page with a real, concrete manipulation code example**
(P4: YOLO and Moveit) that materially grounds several of this task's
required work packages. The remaining 16 pages are either pure navigation
stubs, already superseded by more thorough and more carefully verified
content already on the current site, or contain material (2019 competition
rules, a Carologistics video reference, an informal tone requiring a
rewrite) that needs explicit handling rather than direct reuse.
