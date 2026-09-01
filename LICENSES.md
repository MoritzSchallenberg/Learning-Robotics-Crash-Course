# Licenses and attribution

## Course content

**Original material:** MASKOR Institute, FH Aachen University of Applied
Sciences, and the Carologistics and ALeRT teams.

This site consolidates and rewrites three internal MASKOR teaching resources:

- the **ROS Summer School** documentation (MASCOR Institute, FH Aachen);
- the **ALeRT / Spot practical course** (MASCOR Institute, FH Aachen — Aachen
  Legged Rescue Team);
- the **Carologistics team wiki** (Team Carologistics, FH Aachen and RWTH
  Aachen).

> **TODO-REVIEW — the content license has not been decided.**
>
> The institute has not yet chosen a license for this course text, so this
> repository deliberately ships **no `LICENSE` file**. Until one is chosen, no
> terms of reuse are granted beyond what applies by default.
>
> A permissive documentation license such as **CC BY 4.0** or **CC BY-SA 4.0**
> would suit a public teaching resource and is the natural default, but that is
> a decision for the institute. This should be settled before the site is
> widely publicised.

### How the source material was used

- Overlapping explanations were **rewritten as a single consolidated text**,
  not copied and not concatenated.
- **No files were copied** from the source websites: no HTML, no CSS, no
  JavaScript, no fonts, no images.
- **No images from the source material are published.** See
  `CONTENT_REVIEW.md` §4.4.
- Short **code examples** demonstrating a technique were adapted from the
  source teaching material and from official project documentation. They are
  minimal teaching examples; where an example derives substantially from an
  external project, the page links to it.
- Attribution to the MASKOR Institute and to each source course is given on
  [Sources and licenses](docs/reference/sources.md).

### Logos

Rights for the MASKOR, ALeRT and Carologistics logos are not established, so
the site uses a **text title** instead. Replacing it with a logo requires
confirmation from the institute.

---

## Site toolchain

All installed from PyPI as declared dependencies in `requirements.txt`. None
are vendored into this repository.

| Component | Version | License |
|---|---|---|
| [Sphinx](https://www.sphinx-doc.org/) | 7.4.7 | BSD-2-Clause |
| [sphinx-rtd-theme](https://github.com/readthedocs/sphinx_rtd_theme) | 3.0.2 | MIT |
| [MyST-Parser](https://myst-parser.readthedocs.io/) | 3.0.1 | MIT |
| [sphinx-copybutton](https://github.com/executablebooks/sphinx-copybutton) | 0.5.2 | MIT |
| [sphinx-design](https://github.com/executablebooks/sphinx-design) | 0.6.1 | MIT |

The theme is used **as a dependency**, exactly as intended by its authors. The
Read the Docs theme bundles Font Awesome (SIL OFL 1.1 / MIT) and the Lato and
Roboto Slab fonts (SIL OFL 1.1); these come from the theme package and are not
redistributed separately by this repository.

### Files written for this project

| File | Notes |
|---|---|
| `docs/_static/css/custom.css` | Written from scratch. Adapts the stock RTD theme to the Summer School's look and adds task, solution, review and badge styling plus a dark palette. No CSS from any source site is included. |
| `docs/_static/js/theme.js` | Written from scratch. Light/dark toggle with OS-preference detection and `localStorage` persistence. No third-party code. |
| `docs/conf.py` | Written from scratch. |
| `.github/workflows/pages.yml` | Written from scratch, using GitHub's official first-party actions. |

The dark-mode approach is functionally similar to the
[`sphinx_rtd_dark_mode`](https://github.com/MrDogeBro/sphinx_rtd_dark_mode)
extension used by the original Summer School site. That extension is **not**
used here and none of its code is copied — see "Deviations" in `README.md` for
why it was reimplemented.

---

## Software the course teaches

Third-party open-source projects, referenced and documented here under their
own licenses. This repository claims no ownership of them and redistributes
none of them.

| Project | License |
|---|---|
| [ROS 2](https://docs.ros.org/) | Apache-2.0 |
| [Nav2](https://docs.nav2.org/) | Apache-2.0 / BSD |
| [SLAM Toolbox](https://github.com/SteveMacenski/slam_toolbox) | LGPL-2.1 |
| [OpenCV](https://opencv.org/) | Apache-2.0 |
| [MoveIt 2](https://moveit.picknik.ai/) | BSD-3-Clause |
| [Webots](https://cyberbotics.com/) | Apache-2.0 |
| [RAFCON](https://github.com/DLR-RM/RAFCON) | EPL-1.0 |
| [Ultralytics YOLO](https://docs.ultralytics.com/) | **AGPL-3.0** |
| [AprilTag](https://april.eecs.umich.edu/software/apriltag) | BSD-2-Clause |
| [apriltag_ros](https://github.com/christianrauch/apriltag_ros) | MIT |
| [Octomap](https://octomap.github.io/) | BSD / LGPL |
| [GLIM](https://koide3.github.io/glim/) | MIT |
| [PlanSys2](https://plansys2.github.io/) | Apache-2.0 |
| [Golog++](https://github.com/MASKOR/gologpp) | See repository |
| [Ansible](https://docs.ansible.com/) | GPL-3.0 |
| [MediaPipe](https://ai.google.dev/edge/mediapipe) | Apache-2.0 |
| [OpenVINO](https://docs.openvino.ai/) | Apache-2.0 |

> **Note on Ultralytics YOLO.** It is **AGPL-3.0**, which has real
> consequences: software that incorporates it and is offered over a network may
> have to be released under the same license. This matters for competition and
> research code. Ultralytics also sells a commercial license. Check before
> building on it.

License information above reflects what each project states publicly and is
given for orientation only. Always check the project's own `LICENSE` file.

---

## Third-party material referenced but not reproduced

| Material | Holder | Handling |
|---|---|---|
| RoboCup rulebooks and arena diagrams | RoboCup Federation / league organisers | Linked, never reproduced |
| Competition videos | Various | Not embedded |
| ALeRT Team Description Paper | ALeRT / MASKOR | Mentioned, not reproduced |
| Nav2 citation list | Nav2 authors | Linked to the Nav2 documentation |
| Vendor documentation (Festo, Boston Dynamics, Intel, SLAMTEC) | Respective vendors | Linked only |

---

## Excluded from publication

Recorded in full in `SECURITY_REVIEW.md` and `CONTENT_REVIEW.md`:

- credentials and access data of every kind;
- internal network configuration, addresses and hostnames;
- images served from signed, expiring URLs;
- personal names and personal account information;
- internal team organisation and competition infrastructure details;
- logos and images with unestablished rights.

---

## Corrections

If you believe material here is attributed incorrectly, or is published without
the right to do so, please open an issue on the
[repository](https://github.com/MoritzSchallenberg/Learning-Robotics-Crash-Course)
and it will be corrected or removed.
