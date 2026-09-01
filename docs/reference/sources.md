# Sources and licenses

This course was assembled from teaching material developed at the **MASKOR
Institute, FH Aachen University of Applied Sciences**, and from the public
documentation of the tools it teaches.

## Original material

The content on this site is a consolidation of three internal MASKOR teaching
resources. All three are the work of the institute and its teams; this site
restructures and rewrites that work into a single course.

```{list-table}
:header-rows: 1
:widths: 26 30 44

* - Source
  - Attribution
  - Used for
* - **ROS Summer School**
  - MASCOR Institute, FH Aachen
  - Linux and terminal basics, ROS 2 fundamentals, nodes and packages,
    parameters and launch files, publishers and subscribers, networking and
    SSH, TF2, LiDAR, camera calibration, AprilTags and ArUco, SLAM Toolbox,
    localization, Nav2, autonomous exploration, YOLO, the robot challenge —
    and the visual structure of this site
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

**Explanations were rewritten.** The three sources overlapped heavily —
terminal basics, ROS 2 concepts, TF2, SLAM, Nav2 and YOLO each appeared in two
or three of them, in different words and at different depths. Rather than
copying one version or concatenating several, each shared topic was rewritten
once as a single explanation, drawing on the clearest treatment from each
source. Where one source had a better exercise or a better warning, that was
incorporated.

**Structure follows the Summer School.** The site's layout — a Sphinx
documentation site with hierarchical navigation, breadcrumbs, previous/next
links, search and a light/dark toggle — follows the ROS Summer School's
documentation, which is itself built on the widely used
[Read the Docs Sphinx theme](https://github.com/readthedocs/sphinx_rtd_theme).

**No files were copied from the source sites.** The theme is installed as a
Python dependency from PyPI, not copied. The CSS and JavaScript in
`docs/_static/` were written for this project. No rendered HTML from the source
sites is reused.

**Code examples are documented.** Short code examples that demonstrate a
technique — a minimal publisher, a TF listener, an ArUco detector — were
adapted from the source teaching material and from official ROS 2, OpenCV and
Nav2 documentation. They are teaching examples, deliberately minimal, and
attribution to the source course is given above. Where an example came
substantially from an external project, the page links to that project.

**Technical claims were checked against primary sources.** Commands, package
names, topic names and message types were verified against the official ROS 2,
Nav2, OpenCV, MoveIt and package documentation where possible. Where the source
material could not be verified — because it depends on hardware, on an internal
repository, or because the sources contradict each other — the page says so
explicitly with a **TODO-REVIEW** marker or the {{ unverified }} badge, rather
than guessing. See [Versions and compatibility](compatibility.md).

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
* - [Sphinx](https://www.sphinx-doc.org/)
  - BSD-2-Clause
  - Documentation generator
* - [sphinx-rtd-theme](https://github.com/readthedocs/sphinx_rtd_theme)
  - MIT
  - The visual theme
* - [MyST-Parser](https://myst-parser.readthedocs.io/)
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

:::{admonition} TODO-REVIEW
:class: todo-review

The content license for this course has not yet been decided by the institute.
Until it is, no license file declares terms of reuse for the course text, and
`LICENSES.md` in the repository records this as an open question. This needs a
decision from the institute before the site is widely publicised.
:::
