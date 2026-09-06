# ALeRT Advanced Robotics Tutorial

A technical reference and tutorial site for **ALeRT** (Aachen Legged Rescue
Team), the RoboCup Rescue League team at the **MASKOR Institute, FH Aachen**.

**Website:** <https://moritzschallenberg.github.io/Learning-Robotics-Crash-Course/>
(repository name and Pages URL are unchanged for now — see
[`maintainers/rebrand-followups.md`](maintainers/rebrand-followups.md) for
what a later transfer to an `RRL-ALeRT` repository would require)

This is a long-lived technical reference, not a scheduled course: it
carries no dates, sessions or event logistics — see
[`maintainers/`](maintainers/) for anything organisational.

> **Note:** the site was restructured from an earlier eight-module layout
> into the 13-topic navigation described below (`feat/alert-advanced-
> robotics-tutorial`). Twelve larger content-extension work packages
> (a full BehaviorTree.CPP tutorial, a full MoveIt 2 path, a pick-and-place
> project and others) are planned but not yet written — see
> `maintainers/` for the roadmap.

## Goal

Explain the robotics, ROS 2 and ALeRT-specific systems this team's
software is built on, as a reference anyone can consult — not only
newcomers working through it top to bottom. General fundamentals are
explained **once**; ALeRT-specific commands and systems live on separate
platform pages that link back to them, each one tied to a real, current
ALeRT repository wherever possible.

**Audience:** anyone working on or learning from ALeRT's software, with
some technical grounding (Python is enough) and comfort with a terminal.
No prior ROS 2 experience is needed, and no physical robot — most topics
can be worked through in simulation.

**ALeRT on GitHub:** <https://github.com/RRL-ALeRT> — the team's public
repositories this site's topics link back to throughout.

**Language:** English.

## Current structure

Thirteen top-level topics, each with its own overview page:

| Topic | Focus |
|---|---|
| Getting Started | Linux, Git, networking |
| ROS 2 | Nodes, topics, packages, installation |
| ALeRT Platforms and Safety | Spot, hardware design (KiCad, Fusion), safety levels |
| Simulation | Webots, the ALeRT Spot simulation, simulation time |
| Sensors and Coordinate Frames | Sensor data placed in space, TF2 |
| Perception | Marker/object detection |
| Mapping and World Models | Build a map, occupancy grids, 3D mapping |
| Localization, Navigation and Exploration | AMCL, Nav2, autonomous goals |
| Robot Manipulation | Arm fundamentals, MoveIt 2 (overview; full tutorials planned) |
| Autonomous Decision-Making | State machines, behavior trees, planners |
| Integration, Diagnostics and Testing | Start and debug the whole system |
| Rescue Applications and Projects | Worked examples combining several topics |
| Reference | Cheat sheet, supported environment, glossary |

Simulation and ALeRT/Spot both run on the same fixed toolchain, **Ubuntu
22.04 LTS and ROS 2 Humble** (`docs/reference/compatibility.md`), unless a
specific ALeRT repository is documented to need something else. There is
no distribution choice on this site by default; every command assumes
Humble unless stated otherwise.

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
  conf.py                     Sphinx configuration, incl. badges
  index.md                    Landing page, one toctree per topic

  getting-started/             Linux, Git, networking
  ros2/                        Nodes, topics, packages, installation
  platforms/                   ALeRT Platforms and Safety
    spot/                      ALeRT / Spot platform reference
    hardware-design/           KiCad and Fusion tutorials
  simulation/                  Webots, the ALeRT Spot simulation
  sensors-frames/               Sensors and Coordinate Frames (TF2, RViz)
  perception/                  Core page + 4 deeper chapters
  mapping-world-models/         Mapping and World Models
  navigation-exploration/       Localization, Navigation and Exploration
  manipulation/                 Robot Manipulation (overview page)
  decision-making/              Autonomous Decision-Making
  integration-testing/          Integration, Diagnostics and Testing
  rescue-projects/              Rescue Applications and Projects
                                (autonomous-rescue-mission.md is the
                                worked-example mission)

  reference/
    ros2-cheatsheet.md        Commands, grouped by intent
    compatibility.md          "Supported environment": the fixed toolchain
                              (Ubuntu 22.04 / ROS 2 Humble), per-path
                              versions, and the difficulty/verification
                              badge legend
    glossary.md

  _static/
    css/custom.css            Theme layer, badges, light/dark palette
    js/color-mode.js          Light/dark toggle (name must not be theme.js,
                              which would shadow the RTD theme's own script)
    images/diagrams/          Original SVG diagrams
  _extra/.nojekyll

maintainers/                   NOT built, NOT deployed, NOT in any toctree
  instructors/                 Facilitator/event material -- see below
  content-audit.md             Audit of the archived Spot-tutorial source
  repository-audit.md          Live inventory of public RRL-ALeRT repos
  rebrand-followups.md         What a future repo transfer would need

examples/                      Real, colcon-buildable starter packages
  ros2_turtlesim/               ROS 2 topic's practical task
    turtle_tutorial/            The actual ROS 2 package -- build this
    solutions/                 Reference solution, kept separate from
                               the package so it is never accidentally
                               built or imported by it

scripts/
  tutorial-preflight.sh        Read-only environment check (linked from the site)
  verify-structure.py           Source-level structure checks (no build needed)
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
`tutorial-preflight.sh` and `verify-site.py` remain in the repository root /
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
10. **Added `examples/ros2_turtlesim/`** (renamed from `module02_turtlesim`
    during the ALeRT Advanced Robotics Tutorial migration) — a real,
    `colcon`-buildable ROS 2 Humble package (`turtle_tutorial`, renamed
    from `turtle_course`) backing the ROS 2 topic's practical task, with
    its own CI job (`.github/workflows/pages.yml`, the `examples` job)
    that builds and lints it on every push, independent of the Sphinx
    site build/deploy.
11. **Added three "Try it on Spot" safety-level badges**
    (`{{ spotsim }}` / `{{ spotreadonly }}` / `{{ spotsupervised }}`) and
    a matching section in every topic, indexed from
    `platforms/spot/index.md`.
12. **Restructured the whole `course/` tree into 13 topic-based
    directories** (Entwicklungsauftrag 8 / 8A: rebrand to "ALeRT Advanced
    Robotics Tutorial", removal of all Carologistics/Robotino content,
    migration to the topic layout in "Project structure" above). Module
    numbers, "Core Learning Path" headings and processing-time estimates
    were removed; `{{ core }}` / `{{ optional }}` / `{{ common }}` /
    `{{ platformspecific }}` were replaced by the Foundation / Intermediate
    / Advanced / Research difficulty badges described in "Content levels"
    below. Items 1–10 above describe decisions made against the earlier
    `course/`-based layout and are kept here as a historical record; the
    "Project structure" tree above is the current, authoritative one.

## Editing the content

All content is **MyST Markdown**. Edit the `.md` files and rebuild.

### Platform and verification badges

Content that is ALeRT-specific, simulation-only, or of a given verification
status must be marked. Write the substitution and it renders as a styled
badge:

```markdown
{{ alert }}  {{ simulation }}  {{ documented }}  {{ hardwareverified }}
{{ unverified }}  {{ hwverificationrequired }}  {{ experimental }}  {{ historical }}
```

See `docs/reference/compatibility.md`'s "Status legend" for what each one
means. The whole site is fixed to one toolchain — Ubuntu 22.04 LTS, ROS 2
Humble (see the same page) — so there is deliberately no distribution
badge; Humble is the implicit baseline for every command on the site.

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

### Page templates

Every one of the 13 top-level topics has its own overview page (what
belongs to it, where ALeRT uses it, its subtopics as cards, content
already present versus planned, required knowledge, related ALeRT
repositories, verification status) — see `docs/platforms/index.md` or
`docs/manipulation/index.md` for the current template.

Individual tutorial subpages below a topic follow the older, still-current
structure described in "Content levels" below.

## Contributing

1. Branch from `main`. Name it `<scope>/<description>` — for example
   `jdoe/fix-nav2-params`.
2. Build with `-W` before you push. CI will reject warnings.
3. Keep the general/specific split: shared concepts on the general topic
   pages (`docs/ros2/`, `docs/perception/`, etc.), team-specific detail
   under `docs/platforms/`, linking back rather than repeating.
4. Explain each thing once. If you find yourself writing something that already
   exists elsewhere, link to it instead.
5. **Never invent** a command, topic name or package name. If you are unsure,
   add a `TODO-REVIEW` block rather than a plausible guess.
6. Mark anything platform-, difficulty- or verification-specific with a badge.
7. Update `CONTENT_REVIEW.md` if you add, remove or move substantial content.

### Verify technical claims

Check against primary sources before writing: the
[ROS 2](https://docs.ros.org/), [Nav2](https://docs.nav2.org/),
[OpenCV](https://docs.opencv.org/) and [MoveIt](https://moveit.picknik.ai/)
documentation, and the README of whichever package you are describing.

### Content levels

Every tutorial subpage marks its content by genuine technical difficulty,
using four badges — `{{ foundation }}` (needs no prior topic beyond its own
Prerequisites section), `{{ intermediate }}` (builds directly on one or
more Foundation topics), `{{ advanced }}` (a real capability, actively
used by ALeRT, that takes more background or care) or `{{ research }}`
(documented for completeness, not part of ALeRT's competition-ready path
today) — defined in `docs/conf.py` as MyST substitutions and explained in
`docs/reference/compatibility.md`. Check that a Foundation page's practical
task is genuinely completable as described, not just plausible. See any
existing page under `docs/ros2/` or `docs/perception/` for the pattern.

Each tutorial subpage follows the same structure: Overview, Learning
objectives, Prerequisites, Core concepts, Guided example, Practical task,
Expected result, Verification, Common problems, Optional extensions,
Advanced topics, Continue learning, Connection to the next topic. Write for
a participant working through the material independently — no "tonight",
"next week", "your facilitator provides X", or references to a live
audience. Where a demonstration would traditionally be shown live, write it
as a **Guided example** the reader can run themselves.

**Continue learning** is every subpage's deep-dive section — deliberately
more than a keyword list. Each topic inside it is a `:::{dropdown}` with:
what it is, why it matters, what it needs, a concrete first task or
mini-project, a way to check the result, an official further-reading link,
and a **Next step / Intermediate / Advanced** label in its title. A topic
big enough to need more than that (KiCad, Fusion) gets its own page instead,
linked as a card from the parent topic. Keep every dropdown title on its
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
**ALeRT** team. The public site deliberately carries no separate
source/provenance chapter; full attribution and licensing detail lives in
`LICENSES.md` in this repository instead.

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
