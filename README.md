# Learning Robotics Crash Course

A shared introduction to autonomous mobile robotics for the teams and research
groups of the **MASKOR Institute at FH Aachen**.

**Website:** <https://moritzschallenberg.github.io/Learning-Robotics-Crash-Course/>

The course brings together teaching material that used to live in three
separate places — the ROS Summer School, the ALeRT/Spot practical course and
the Carologistics team wiki — into one path that every team can follow. Eight
evening sessions build up from the anatomy of a robot to a fully autonomous
mission, and a closing hackathon puts it all together.

## Goal

New members of the robotics teams should be able to work through one course
and arrive at a shared foundation, regardless of which robot their team runs.
The general fundamentals are explained **once**; team-specific commands and
systems live on separate platform pages that link back to them.

**Audience:** new members of the robotics teams with some technical grounding.
Some programming (Python is enough), comfort with a terminal, and an interest
in how autonomous robots work. No prior ROS experience is needed, and no robot
— every session can be followed in simulation.

**Language:** English.

## Course structure

Eight evenings, all 17:35–19:00, plus a hackathon.

| # | Date | Session |
|---|---|---|
| 1 | Mon, 05 Oct 2026 | System Architecture and Robot Hardware |
| 2 | Wed, 07 Oct 2026 | ROS 2 Fundamentals |
| 3 | Mon, 12 Oct 2026 | Sensors, TF2 and RViz |
| 4 | Wed, 14 Oct 2026 | Perception and Object Detection |
| 5 | Mon, 19 Oct 2026 | Mapping and Localization |
| 6 | Wed, 21 Oct 2026 | Autonomous Navigation |
| 7 | Mon, 26 Oct 2026 | Autonomous Decisions and Manipulation |
| 8 | Wed, 28 Oct 2026 | System Integration and Testing |
| — | Sat–Sun, 07–08 Nov 2026 | Hackathon: Autonomous Robot Challenge |

Three platform tracks run alongside: **Simulation**,
**Carologistics/Robotino** and **ALeRT/Spot**.

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

```text
.github/workflows/pages.yml   Build, secret-scan and deploy to GitHub Pages

docs/
  conf.py                     Sphinx configuration, incl. platform badges
  index.md                    Landing page

  prerequisites/              Do these before session 1
    linux-terminal.md         Terminal, filesystem, .bashrc
    installation.md           Ubuntu, ROS 2, workspace, simulator
    git.md                    Git workflow and team conventions
    networking.md             Domain IDs, SSH, subnets

  course/                     The eight sessions
    01-system-hardware.md   … 08-integration.md
    hackathon.md              Final challenge

  platforms/                  Team-specific material only
    simulation.md
    carologistics-robotino.md
    alert-spot.md

  reference/
    ros2-cheatsheet.md        Commands, grouped by intent
    compatibility.md          Version matrix and known conflicts
    glossary.md
    sources.md                Attribution and licensing

  _static/
    css/custom.css            Theme layer, badges, light/dark palette
    js/color-mode.js          Light/dark toggle (name must not be theme.js,
                              which would shadow the RTD theme's own script)
    images/                   (empty — see CONTENT_REVIEW.md §4.4)
  _extra/.nojekyll

requirements.txt              Pinned documentation toolchain
CONTENT_MAP.md                Inventory of all 78 source documents
CONTENT_REVIEW.md             Included / merged / platform-specific / excluded
SECURITY_REVIEW.md            Secret-scan findings and remediation
LICENSES.md                   Attribution and licensing
```

### Deviations from the originally proposed structure

Three, all small and reversible:

1. **Added `course/index.md`, `platforms/index.md` and `reference/index.md`.**
   Every `toctree` now has a parent page. This keeps breadcrumbs sensible,
   avoids orphan-document warnings under `-W`, and gives each section a
   landing page that orients the reader.
2. **Added `docs/_extra/.nojekyll`.** Not required when deploying via GitHub
   Actions, but it means the site still works if Pages is ever switched to
   branch-based publishing.
3. **Added `sphinx-design`** to the toolchain, for the landing-page cards and
   the collapsible solution blocks used in the exercises.

`docs/_static/images/` exists but is empty — see `CONTENT_REVIEW.md` §4.4 for
why no images are published yet.

## Editing the content

All content is **MyST Markdown**. Edit the `.md` files and rebuild.

### Platform and version badges

Instructions that only apply to one system must be marked. Write the
substitution and it renders as a styled badge:

```markdown
{{ common }}  {{ simulation }}  {{ carologistics }}  {{ alert }}
{{ jazzy }}   {{ humble }}      {{ unverified }}
```

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

Each main page aims to have: learning objectives · prerequisites · brief theory
· a walkthrough · commands or code · a practical task · the expected result ·
common mistakes · further reading · platform and version markers.

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
Carologistics and ALeRT teams. Full attribution on the site's
[Sources and licenses](docs/reference/sources.md) page and in `LICENSES.md`.

> **The content license has not yet been decided by the institute**, so this
> repository ships no `LICENSE` file. See `LICENSES.md`.

The Sphinx theme and all other tooling are installed from PyPI as declared
dependencies; nothing is vendored. No files, images, CSS or JavaScript from the
original tutorial sites are reused.

## Deployment

Pushes to `main` trigger `.github/workflows/pages.yml`, which installs
dependencies, builds with `-W`, scans the output for secrets, checks links, and
publishes to GitHub Pages.

> [!NOTE]
> **One-time manual setup required.** GitHub Pages must be set to deploy from
> GitHub Actions before the first deployment can succeed:
>
> **Settings → Pages → Build and deployment → Source → "GitHub Actions"**
>
> This cannot be done from a workflow and has to be set once by someone with
> admin rights on the repository. Until it is, the build job succeeds and the
> deploy job fails.
