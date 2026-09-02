# Sources and licenses

This course was assembled from teaching material developed at the **MASKOR
Institute, FH Aachen University of Applied Sciences**, and from the public
documentation of the tools it teaches.

## Original material

Some of this course's content originates from internal MASKOR teaching
material; the table below lists what is still actively attributed as a
source. The full provenance record, including material that has since been
fully rewritten and independently re-verified, is kept in the repository's
internal review documents rather than repeated here.

```{list-table}
:header-rows: 1
:widths: 26 30 44

* - Source
  - Attribution
  - Used for
* - **ALeRT / Spot practical course**
  - MASCOR Institute, FH Aachen — ALeRT (Aachen Legged Rescue Team)
  - Webots Spot simulation, OpenCV image processing, ArUco exercises, services
    and actions, LiDAR exercises, mapping and navigation, YOLO with OpenVINO,
    MoveIt and manipulation, RAFCON and state machines, high-level control,
    Octomap and GLIM, Spot operation
* - **Carologistics team wiki**
  - Team Carologistics (FH Aachen and RWTH Aachen)
  - System overview, Robotino hardware, Git workflows, Ansible and deployment,
    remote access practice, Webots simulation, Nav2 configuration, laser scan
    processing, the vision system, markerless MPS detection, data labeling,
    the gripper system
```

## How the material was used

**Explanations are independently written and checked against primary
sources, not transcribed from any one source.** Every module has gone
through more than one full rewrite since this course's first version: once
to restructure it into a self-contained practical-task format, and again to
remove every trace of a live-session, presenter's-eye-view framing so it
reads as independent, self-directed material. Each rewrite re-verified the underlying technical
claims — commands, package names, API calls — against the official
documentation for the tool in question, rather than carrying forward
earlier wording unchecked. See [Sources standard](#sources-standard) below
for exactly which primary sources.

**Structure follows a widely used documentation convention.** The site's
layout — hierarchical navigation, breadcrumbs, previous/next links, search
and a light/dark toggle — is the standard shape of a
[Read the Docs Sphinx theme](https://github.com/readthedocs/sphinx_rtd_theme)
site, not something borrowed from any one course's documentation.

**No files were copied from any source site.** The theme is installed as a
Python dependency from PyPI, not copied. The CSS and JavaScript in
`docs/_static/` were written for this project. No rendered HTML from any
source site is reused.

**Code examples are documented.** Short code examples that demonstrate a
technique — a minimal publisher, a TF listener, an ArUco detector — were
adapted from teaching material and from official documentation, and
verified against the current documentation for the ROS 2 distribution this
course targets. They are teaching examples, deliberately minimal. Where an
example came substantially from an external project, the page links to that
project.

(sources-standard)=
### Sources standard

Technical claims on this site are checked, in order of preference, against:

```{list-table}
:header-rows: 1
:widths: 30 70

* - Topic
  - Primary source
* - ROS 2 core, installation
  - [ROS 2 Humble documentation](https://docs.ros.org/en/humble/)
* - Navigation
  - [Nav2 documentation](https://docs.nav2.org/humble/), checked for
    Humble-compatible functionality
* - Manipulation
  - [MoveIt 2 documentation](https://moveit.picknik.ai/)
* - Computer vision
  - [OpenCV documentation](https://docs.opencv.org/)
* - 2D SLAM
  - [SLAM Toolbox repository](https://github.com/SteveMacenski/slam_toolbox)
    and its own documentation
* - Electrical schematics
  - [KiCad documentation](https://docs.kicad.org/)
* - Mechanical CAD
  - [Autodesk Fusion help](https://help.autodesk.com/view/fusion360/ENU/)
    and its
    [system requirements](https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/System-requirements-for-Autodesk-Fusion-360.html)
```

Where a claim could not be verified — because it depends on hardware, on an
internal repository, or because sources contradict each other — the page
says so explicitly with the {{ unverified }} badge rather than guessing.
See [Supported environment](compatibility.md) for the exact software
versions this checking was done against, and each page's own **Further
reading** section for the specific pages consulted, several of them
retrieved and re-checked on 2026-09-02 for this course's move to a single
fixed ROS 2 Humble baseline.

## What was deliberately excluded

Some material in the sources is not appropriate for a public course website:

- **Internal network configuration** — network names, address ranges, host
  names and device credentials.
- **Access credentials of any kind** — these were present in cleartext in some
  source material and are excluded entirely.
- **Team organisation** — meeting agendas, milestone assignments, personal
  names, travel and competition logistics.
- **Images with unclear rights** — screenshots, photographs and diagrams whose
  origin or licensing could not be established, including images served from
  time-limited private URLs.
- **Team and institute logos** — logo usage rights were not established, so the
  site uses a text title instead.

The full record is in `CONTENT_REVIEW.md` and `SECURITY_REVIEW.md` in the
[repository](https://github.com/MoritzSchallenberg/Learning-Robotics-Crash-Course).

## Images

This first version of the site contains **no images from the source material**.
Every diagram is drawn as text, and the layout relies on typography rather than
screenshots.

This is a deliberate, reversible decision: the source material's images —
screenshots of RViz, photographs of robots and arenas, diagrams from
competition rulebooks — have mixed and largely undocumented provenance, and
several were served from signed, expiring URLs. Rather than publish images
whose rights are unclear, the first version publishes none, and images can be
added once their origin is established.

Candidates for a future version, once rights are confirmed:

- photographs of Robotino and Spot taken by the teams themselves;
- RViz and Webots screenshots produced fresh for this course;
- diagrams redrawn as SVG.

## Software this course teaches

All of the following are third-party open-source projects, used and documented
here under their own licenses. This site claims no ownership of them.

```{list-table}
:header-rows: 1
:widths: 24 18 58

* - Project
  - License
  - Role
* - [ROS 2](https://docs.ros.org/)
  - Apache-2.0
  - The middleware the whole course is built on
* - [Nav2](https://docs.nav2.org/)
  - Apache-2.0 / BSD
  - Autonomous navigation
* - [SLAM Toolbox](https://github.com/SteveMacenski/slam_toolbox)
  - LGPL-2.1
  - 2D SLAM
* - [OpenCV](https://opencv.org/)
  - Apache-2.0
  - Computer vision
* - [MoveIt 2](https://moveit.picknik.ai/)
  - BSD-3-Clause
  - Motion planning for manipulators
* - [Webots](https://cyberbotics.com/)
  - Apache-2.0
  - Robot simulation
* - [RAFCON](https://github.com/DLR-RM/RAFCON)
  - EPL-1.0
  - Graphical state machines
* - [Ultralytics YOLO](https://docs.ultralytics.com/)
  - AGPL-3.0
  - Object detection
* - [AprilTag](https://april.eecs.umich.edu/software/apriltag)
  - BSD-2-Clause
  - Fiducial markers
* - [Octomap](https://octomap.github.io/)
  - BSD / LGPL
  - 3D occupancy mapping
* - [GLIM](https://koide3.github.io/glim/)
  - MIT
  - LiDAR-inertial SLAM
* - [PlanSys2](https://plansys2.github.io/)
  - Apache-2.0
  - PDDL planning
* - [Ansible](https://docs.ansible.com/)
  - GPL-3.0
  - Deployment automation
* - [KiCad](https://www.kicad.org/)
  - GPL-3.0 (software); CC-BY-SA-4.0 (libraries)
  - Electrical schematic design
* - [Autodesk Fusion](https://www.autodesk.com/products/fusion-360/)
  - Proprietary, subscription/entitlement-based
  - Mechanical CAD — {{ unverified }} confirm current licensing terms and
    platform availability before relying on this course's Fusion page
```

:::{note}
License information is given for orientation and reflects what the projects
state publicly. Always check the project's own `LICENSE` file before using it
in your own work — particularly Ultralytics YOLO, whose AGPL-3.0 license has
real implications for anything you distribute.
:::

## This site's toolchain

```{list-table}
:header-rows: 1
:widths: 34 18 48

* - Component
  - License
  - Role
* - [Sphinx](https://www.sphinx-doc.org/en/master/)
  - BSD-2-Clause
  - Documentation generator
* - [sphinx-rtd-theme](https://github.com/readthedocs/sphinx_rtd_theme)
  - MIT
  - The visual theme
* - [MyST-Parser](https://myst-parser.readthedocs.io/en/latest/)
  - MIT
  - Markdown support
* - [sphinx-copybutton](https://github.com/executablebooks/sphinx-copybutton)
  - MIT
  - Copy buttons on code blocks
* - [sphinx-design](https://github.com/executablebooks/sphinx-design)
  - MIT
  - Cards, grids and collapsible blocks
```

All are installed from PyPI as declared dependencies. None are vendored into
this repository.

## Citing and reusing

If you use this material, please credit the **MASKOR Institute, FH Aachen** and
the original teaching resources listed above.

Corrections and improvements are welcome — see the contributing section of the
[repository README](https://github.com/MoritzSchallenberg/Learning-Robotics-Crash-Course).

:::{admonition} Decision needed: content license
:class: todo-review

The content license for this course has not yet been decided by the
institute and the original rights holders. Until it is, no license file
declares terms of reuse for the course text — this site deliberately does
not pick one on their behalf, and no option (including a permissive one
such as CC BY 4.0) is assumed by default.

See `LICENSES.md` in the repository for the full statement of what is and
is not currently licensed.
:::
