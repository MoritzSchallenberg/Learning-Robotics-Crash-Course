# Learning Robotics Crash Course

A shared introduction to autonomous mobile robotics for the teams and research
groups of the **MASKOR Institute at FH Aachen**.

**Website:** <https://moritzschallenberg.github.io/Learning-Robotics-Crash-Course/>

Eight modules build up from the anatomy of a robot to a fully autonomous
mission, and a closing capstone project puts it all together. The site is a
semester-independent learning platform: it carries no dates, schedules or
event logistics — see [`maintainers/`](maintainers/) for that.

## Goal

New members of the robotics teams should be able to work through one course
and arrive at a shared foundation, regardless of which robot their team runs.
The general fundamentals are explained **once**; team-specific commands and
systems live on separate platform pages that link back to them.

**Audience:** new members of the robotics teams with some technical grounding.
Some programming (Python is enough), comfort with a terminal, and an interest
in how autonomous robots work. No prior ROS experience is needed, and no robot
— every module can be completed in simulation.

**Language:** English.

## Course structure

Eight modules, each built around one central concept and one practical task,
plus a closing capstone project. Module 1 has two hands-on hardware-design
sub-pages (KiCad, Fusion) reachable directly from it.

| # | Module | Focus |
|---|---|---|
| 1 | System Architecture and Robot Hardware | Components, data flows, schematics, mechanical CAD |
| 2 | ROS 2 Fundamentals | Nodes, topics, packages |
| 3 | Sensors, TF2 and RViz | Sensor data placed in space |
| 4 | Perception and Object Detection | Marker/object detection |
| 5 | Mapping and Localization | Build a map, locate the robot |
| 6 | Autonomous Navigation | Reach autonomous goals |
| 7 | Autonomous Decisions and Manipulation | Model a mission |
| 8 | System Integration and Testing | Start and debug the whole system |
| — | Capstone: Autonomous Robot Mission | Combine every module |

Three platform tracks run alongside: **Simulation**,
**Carologistics/Robotino** and **ALeRT/Spot** — all three on the same fixed
toolchain, **Ubuntu 22.04 LTS and ROS 2 Humble**
(`docs/reference/compatibility.md`). There is no distribution choice on this
site; every command assumes Humble.

## Building the site locally

Requires **Python 3.10 or newer** (3.12 is used in CI).

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
sphinx-build -W --keep-going -b html docs docs/_build/html
```

`-W` turns warnings into errors, which is what CI does — build this way and you
will not be surprised by a failing pipeline.

### Previewing

Open `docs/_build/html/index.html` in a browser, or serve it so that search
works properly:

```bash
python3 -m http.server -d docs/_build/html 8000
```

Then visit <http://localhost:8000>.

> [!NOTE]
> The site is served from a repository subpath on GitHub Pages. All asset paths
> are relative, so it works both at `/` locally and at
> `/Learning-Robotics-Crash-Course/` in production. **Never introduce an absolute
> path beginning with `/`.**

### Rebuilding on save

```bash
pip install sphinx-autobuild
sphinx-autobuild docs docs/_build/html
```

## Project structure

**`docs/`** is the entire published website — everything Sphinx builds and
everything GitHub Pages serves. Nothing outside `docs/` is ever built or
deployed; see [Learner-only site](#learner-only-site-what-is-and-is-not-published)
below for what that guarantees.

```text
.github/workflows/pages.yml   Build, secret-scan and deploy to GitHub Pages

docs/                          <-- published website; nothing else is built
  conf.py                     Sphinx configuration, incl. platform badges
  index.md                    Landing page

  prerequisites/
    linux-terminal.md         Terminal, filesystem, .bashrc
    installation.md           Ubuntu, ROS 2, workspace, simulator, preflight
    git.md                    Git workflow and team conventions
    networking.md             Domain IDs, SSH, subnets

  course/                     The eight modules
    01-system-hardware.md   … 08-integration.md
    01-hardware/              KiCad and Fusion sub-pages, linked from module 1
      kicad-schematic.md
      fusion-mechanical-design.md
    04-perception/           Split into a core page + 4 deeper chapters
    hackathon.md              Capstone: Autonomous Robot Mission

  platforms/                  Team-specific material only
    simulation.md
    carologistics-robotino.md
    alert-spot.md

  reference/
    ros2-cheatsheet.md        Commands, grouped by intent
    compatibility.md          "Supported environment": the fixed toolchain
                              (Ubuntu 22.04 / ROS 2 Humble) and per-track versions
    glossary.md

  _static/
    css/custom.css            Theme layer, badges, light/dark palette
    js/color-mode.js          Light/dark toggle (name must not be theme.js,
                              which would shadow the RTD theme's own script)
    images/diagrams/          10 original SVG diagrams
  _extra/.nojekyll

maintainers/                   NOT built, NOT deployed, NOT in any toctree
  instructors/                 Facilitator/event material -- see below

examples/                      Real, colcon-buildable starter packages
  module02_turtlesim/          Module 2's practical task
    turtle_course/             The actual ROS 2 package -- build this
    solutions/                 Reference solution, kept separate from
                               the package so it is never accidentally
                               built or imported by it

scripts/
  course-preflight.sh          Read-only environment check (linked from the site)
  verify-site.py                Browser-level checks (not part of the build)

requirements.txt              Pinned documentation toolchain
CONTENT_MAP.md                Inventory of all 78 source documents
CONTENT_REVIEW.md             Included / merged / platform-specific / excluded
SECURITY_REVIEW.md            Secret-scan findings and remediation
LICENSES.md                   Attribution and licensing
DECISIONS_NEEDED.md           Open organisational decisions (repo only,
                              not linked from the public site)
```

### Learner-only site: what is and is not published

The published website contains only what a participant needs to learn,
practise, look something up, or fix a technical problem — no dates,
schedules, facilitator instructions, room planning, or event roles. See the
guiding question in `DECISIONS_NEEDED.md` and the "Editing the content"
section below for what that means when adding new pages.

`maintainers/instructors/` holds facilitator-facing material that was
previously part of the site (`docs/instructors/`) and has been moved out:
it is not in `docs/`, not referenced by any `toctree`, not linked from any
public page, and consequently never reaches the Sphinx build, the search
index, or the GitHub Pages artifact. `DECISIONS_NEEDED.md`,
`course-preflight.sh` and `verify-site.py` remain in the repository root /
`scripts/` because they are genuinely useful to keep versioned, without
being part of the website either.

### Deviations from the originally proposed structure

1. **Added `course/index.md`, `platforms/index.md` and `reference/index.md`.**
   Every `toctree` now has a parent page. This keeps breadcrumbs sensible,
   avoids orphan-document warnings under `-W`, and gives each section a
   landing page that orients the reader.
2. **Added `docs/_extra/.nojekyll`.** Not required when deploying via GitHub
   Actions, but it means the site still works if Pages is ever switched to
   branch-based publishing.
3. **Added `sphinx-design`** to the toolchain, for the landing-page cards and
   the collapsible solution blocks used in the exercises.
4. **Split `course/04-perception.md`** into a core page plus four deeper
   chapters (`camera-calibration`, `fiducial-markers`, `object-detection`,
   `data-labeling`) under `course/04-perception/`, to keep the core module
   page focused on its one practical task.
5. **Moved `docs/instructors/` to `maintainers/instructors/`**, out of the
   Sphinx source tree entirely, so the published site carries no
   event-organisation content — see above.
6. **Fixed the whole course to ROS 2 Humble on Ubuntu 22.04.** Removed the
   Jazzy/Humble comparison and per-command distribution badges; the
   `{{ jazzy }}` and `{{ humble }}` substitutions no longer exist.
   `reference/compatibility.md` ("Supported environment") documents the
   single fixed toolchain instead of a matrix of alternatives.
7. **Added `course/01-hardware/`** — a KiCad schematic tutorial and an
   Autodesk Fusion mechanical-CAD tutorial, linked as cards from module 1
   and included in its `toctree`, each with its own practical task.
8. **Added a dropdown-contrast regression check to `verify-site.py`.**
   Every `sphinx-design` dropdown is opened in both light and dark mode and
   checked for WCAG AA contrast (composited backgrounds, not raw `rgba()`
   values) and a visible keyboard focus outline — see `custom.css`'s
   `--lrcc-accent-solid` design-token comment for why a "banner with white
   text" needs a different color than a "text/border accent".
9. **Added a matching sidebar-contrast check.** The same rgba-compositing
   helper is reused to check every `.wy-menu-vertical a` link on every
   page, catching a related stock-theme bug where a non-current link
   inside an expanded branch was painted with a hardcoded light-gray
   background the site's own dark-sidebar override did not reach.
10. **Added `examples/module02_turtlesim/`** — a real, `colcon`-buildable
    ROS 2 Humble package (`turtle_course`) backing module 2's practical
    task, with its own CI job (`.github/workflows/pages.yml`, the
    `examples` job) that builds and lints it on every push, independent
    of the Sphinx site build/deploy.
11. **Added three "Try it on Spot" safety-level badges**
    (`{{ spotsim }}` / `{{ spotreadonly }}` / `{{ spotsupervised }}`) and
    a matching section in every course module, indexed from
    `platforms/alert-spot.md`.

## Editing the content

All content is **MyST Markdown**. Edit the `.md` files and rebuild.

### Platform and version badges

Instructions that only apply to one system must be marked. Write the
substitution and it renders as a styled badge:

```markdown
{{ common }}  {{ simulation }}  {{ carologistics }}  {{ alert }}  {{ unverified }}
```

The whole course is fixed to one toolchain — Ubuntu 22.04 LTS, ROS 2 Humble
(see `docs/reference/compatibility.md`) — so there is deliberately no
distribution badge; Humble is the implicit baseline for every command on the
site.

Badges are defined in `docs/conf.py` and styled in `custom.css`.

> [!WARNING]
> Do **not** put a badge inside a heading. It becomes part of the generated
> anchor and breaks links to that section. Put it on its own line underneath.

### Task, result and review blocks

```markdown
:::{admonition} Task: do the thing
:class: task
...
:::

:::{admonition} Expected result
:class: result
...
:::

:::{dropdown} Hint
:icon: light-bulb
...
:::

:::{admonition} TODO-REVIEW
:class: todo-review
What needs checking, and why.
:::
```

### Page template

See "Content levels" below for the current 12-part module structure and the
"Continue learning" convention — this replaced an earlier, shorter template
from the first version of the site.

## Contributing

1. Branch from `main`. Name it `<scope>/<description>` — for example
   `jdoe/fix-nav2-params`.
2. Build with `-W` before you push. CI will reject warnings.
3. Keep the general/specific split: shared concepts in `course/`,
   team-specific detail in `platforms/`, linking back rather than repeating.
4. Explain each thing once. If you find yourself writing something that already
   exists elsewhere, link to it instead.
5. **Never invent** a command, topic name or package name. If you are unsure,
   add a `TODO-REVIEW` block rather than a plausible guess.
6. Mark anything platform- or version-specific with a badge.
7. Update `CONTENT_REVIEW.md` if you add, remove or move substantial content.

### Verify technical claims

Check against primary sources before writing: the
[ROS 2](https://docs.ros.org/), [Nav2](https://docs.nav2.org/),
[OpenCV](https://docs.opencv.org/) and [MoveIt](https://moveit.picknik.ai/)
documentation, and the README of whichever package you are describing.

### Content levels

Every course module marks its content by how essential it is, using four
badges — `{{ core }}` (the module's central concept and task), `{{ optional }}`
(worth doing with extra time), `{{ advanced }}` (deliberately beyond the
module's core scope, for later reading) or `{{ platformspecific }}` —
defined in `docs/conf.py` as MyST substitutions. Check that a module's Core
practical task is genuinely completable as described, not just plausible.
See any existing `course/0*.md` file for the pattern.

Each module follows the same structure: Overview, Learning objectives,
Prerequisites, Core concepts, Guided example, Practical task, Expected
result, Verification, Common problems, Optional extensions, Advanced
topics, Continue learning, Connection to the next module. Write for a
participant working through the material independently — no "tonight",
"next week", "your facilitator provides X", or references to a live
audience. Where a demonstration would traditionally be shown live, write it
as a **Guided example** the reader can run themselves.

**Continue learning** is every module's deep-dive section — deliberately
more than a keyword list. Each topic inside it is a `:::{dropdown}` with:
what it is, why it matters, what it needs, a concrete first task or
mini-project, a way to check the result, an official further-reading link,
and a **Next step / Intermediate / Advanced** label in its title. A topic
big enough to need more than that (KiCad, Fusion) gets its own page instead,
linked as a card from the parent module. Keep every dropdown title on its
own line, on a `(target-name)=` MyST anchor line if you need to link to it
from elsewhere — dropdown titles are not headings and get no automatic
anchor.

### Testing beyond the build

`sphinx-build -W` catches broken internal links, anchors and Markdown
errors, but not what only a browser can check — JavaScript errors, mobile
overflow, the light/dark toggle, search. `scripts/verify-site.py` covers
that:

```bash
sphinx-build -b html docs docs/_build/html
pip install playwright && playwright install chromium

mkdir -p /tmp/site-serve/Learning-Robotics-Crash-Course
cp -r docs/_build/html/. /tmp/site-serve/Learning-Robotics-Crash-Course/
python3 -m http.server 8899 -d /tmp/site-serve &

python3 scripts/verify-site.py
```

Playwright is intentionally **not** in `requirements.txt` — building the
site itself should never need a browser download. Install it only when
running this script.

## Security

> **This repository is public.**

The material it was built from contained credentials in cleartext, internal
network configuration and signed URLs carrying authentication material. None of
it is here, and none of it may be added.

**Never commit:**

- passwords, keys, tokens or credentials of any kind;
- internal IP addresses, hostnames, or network configuration;
- Wi-Fi names or wireless credentials;
- personal names, personal accounts or personal data;
- signed or expiring URLs;
- private repository links or internal wiki links;
- competition or infrastructure details;
- the raw source material (`.gitignore` blocks the usual paths, but check).

Run a scan before pushing:

```bash
grep -rniE '(password|passwd|secret|api[_-]?key|token|credential)[[:space:]]*[:=]' \
  --include='*.md' --include='*.py' --include='*.yml' --include='*.yaml' .
grep -rnE '\b(10\.|192\.168\.|172\.(1[6-9]|2[0-9]|3[01])\.)[0-9]{1,3}\.[0-9]{1,3}' \
  --include='*.md' .
grep -rnE 'X-Amz-|Signature=|[?&]jwt=|[?&]token=' .
```

CI runs an equivalent scan over the built HTML and fails the build on a hit.

If a secret is ever committed: **tell the team immediately** so it can be
rotated. Deleting the commit does not remove it from clones.

See `SECURITY_REVIEW.md` for the full review of the source material.

## Sources and licenses

Built from teaching material by the **MASKOR Institute, FH Aachen** and the
Carologistics and ALeRT teams. The public site deliberately carries no
separate source/provenance chapter; full attribution and licensing detail
lives in `LICENSES.md` in this repository instead.

> **The content license has not yet been decided by the institute**, so this
> repository ships no `LICENSE` file. See `LICENSES.md`.

The Sphinx theme and all other tooling are installed from PyPI as declared
dependencies; nothing is vendored. No files, images, CSS or JavaScript from the
original tutorial sites are reused.

## Deployment

Pushes to `main` trigger `.github/workflows/pages.yml`, which installs
dependencies, builds with `-W`, scans the output for secrets, checks links, and
publishes to GitHub Pages. GitHub Pages is enabled and live:
<https://moritzschallenberg.github.io/Learning-Robotics-Crash-Course/> —
every push to `main` redeploys it automatically, no manual step needed.
