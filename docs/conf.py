# Configuration file for the Sphinx documentation builder.
#
# ALeRT Advanced Robotics Tutorial -- ALeRT (Aachen Legged Rescue Team),
# MASKOR Institute, FH Aachen.
# Full reference: https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------

project = "ALeRT Advanced Robotics Tutorial"
author = "ALeRT, MASKOR Institute, FH Aachen"
copyright = "2026, ALeRT, MASKOR Institute, FH Aachen"
version = "0.1"
release = "0.1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "myst_parser",          # Markdown (MyST) source files
    "sphinx_copybutton",    # copy button on every code block
    "sphinx_design",        # cards, grids, dropdowns (used for solution blocks)
    "sphinx.ext.todo",
]

# Content is authored in Markdown so that it stays easy to edit.
source_suffix = {".md": "markdown", ".rst": "restructuredtext"}

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "README.md"]

language = "en"

# Warnings are errors in CI (`sphinx-build -W`), so keep the tree clean.
nitpicky = False
todo_include_todos = False

# -- MyST configuration ------------------------------------------------------

myst_enable_extensions = [
    "colon_fence",      # ::: fenced directives
    "deflist",          # definition lists
    "substitution",     # {{ platform_badges }}
    "attrs_inline",
]

# Auto-generate anchors for headings up to level 3 so cross-page links to
# sections work without manually declaring targets.
myst_heading_anchors = 3

# ---------------------------------------------------------------------------
# Platform badges.
#
# Every platform-specific instruction on this site must be marked, so that
# readers never mistake a simulation-only instruction for one verified on
# real hardware. The whole site is fixed to ROS 2 Humble (see
# docs/reference/compatibility.md), so there is deliberately no distribution
# badge -- Humble is the implicit baseline for every command on the site.
# Authors write e.g. `{{ alert }}` in Markdown; the substitution below
# expands to a styled badge (see _static/css/custom.css).
# ---------------------------------------------------------------------------


def _badge(css_class: str, label: str) -> str:
    return f'<span class="lrcc-badge lrcc-badge--{css_class}">{label}</span>'


def _level(css_class: str, label: str) -> str:
    return f'<span class="lrcc-level lrcc-level--{css_class}">{label}</span>'


myst_substitutions = {
    "simulation": _badge("simulation", "SIMULATION"),
    "alert": _badge("alert", "ALERT"),
    "unverified": _badge("unverified", "UNVERIFIED"),
    # ---------------------------------------------------------------------
    # Difficulty-level badges (Entwicklungsauftrag 8, replacing the course-
    # era Core/Optional/Common/Platform-specific scheme). These mark
    # technical difficulty, not schedule priority -- a topic is Foundation
    # because it needs no prior specialised knowledge, not because it is
    # "session 1". Mark every heading or task with exactly one.
    # ---------------------------------------------------------------------
    "foundation": _level("foundation", "FOUNDATION"),
    "intermediate": _level("intermediate", "INTERMEDIATE"),
    "advanced": _level("advanced", "ADVANCED"),
    "research": _level("research", "RESEARCH"),
    # ---------------------------------------------------------------------
    # "Try it on Spot" safety-level badges (Entwicklungsauftrag 5). Every
    # Spot exercise scattered across this site's topics is marked with
    # exactly one of these three, so a reader can tell at a glance whether
    # it is safe to try alone.
    # ---------------------------------------------------------------------
    "spotsim": _level("spot-sim", "SIMULATION EXERCISE"),
    "spotreadonly": _level("spot-readonly", "READ-ONLY ON PHYSICAL SPOT"),
    "spotsupervised": _level("spot-supervised", "SUPERVISED PHYSICAL EXERCISE"),
    # ---------------------------------------------------------------------
    # Team-claim verification badges (Entwicklungsauftrag 6, extended in
    # Entwicklungsauftrag 8). Every "how ALeRT uses this" statement is
    # marked with exactly one: confirmed by the team's own repository or
    # documentation ({{ documented }}), runnable in Webots
    # ({{ simulation }}, already defined above), actually checked on
    # running hardware ({{ hardwareverified }}), technically plausible but
    # not checked ({{ unverified }}, already defined above), a specific
    # call to actually check on real hardware before relying on it
    # ({{ hwverificationrequired }}), a working but not yet
    # production-ready approach ({{ experimental }}), no longer current but
    # kept for context ({{ historical }}), or -- written as plain text,
    # "Not documented", no badge needed -- no reliable information at all.
    # Never use {{ hardwareverified }} from a passing simulation test.
    # ---------------------------------------------------------------------
    "documented": _badge("documented", "DOCUMENTED"),
    "hardwareverified": _badge("hwverified", "HARDWARE-VERIFIED"),
    "hwverificationrequired": _badge("hwverification-required", "HARDWARE VERIFICATION REQUIRED"),
    "experimental": _badge("experimental", "EXPERIMENTAL"),
    "historical": _badge("historical", "HISTORICAL"),
}

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_title = "ALeRT Advanced Robotics Tutorial"

# Logo rights for the MASKOR / team logos found in the source material are not
# established, so the site deliberately uses a text title instead of an image.
# See LICENSES.md and CONTENT_REVIEW.md.
html_logo = None
html_favicon = None

html_theme_options = {
    "collapse_navigation": False,
    "sticky_navigation": True,
    "navigation_depth": 3,
    # Show page titles only in the sidebar. Without this, the section headings
    # of each section index page appear as siblings of the real pages, which
    # makes the course structure hard to read.
    "titles_only": True,
    "prev_next_buttons_location": "bottom",
    "style_external_links": True,
}

html_static_path = ["_static"]

html_css_files = ["css/custom.css"]
html_js_files = ["js/color-mode.js"]

# The site is served from a repository subpath on GitHub Pages
# (https://<user>.github.io/Learning-Robotics-Crash-Course/). Sphinx emits
# relative asset paths, so no absolute "/" paths must ever be introduced.
html_baseurl = "https://moritzschallenberg.github.io/Learning-Robotics-Crash-Course/"

# -- Options for the linkcheck builder ---------------------------------------
#
# linkcheck runs in CI for information only (external sites go down, rate-limit
# and block CI runners), so it must not be the reason a deploy fails. These
# settings keep it fast and reduce false positives.

linkcheck_timeout = 15
linkcheck_retries = 2
linkcheck_workers = 10

# Anchors on third-party pages are frequently generated by JavaScript, which
# linkcheck cannot see. Internal anchors are validated by the HTML build itself.
linkcheck_anchors = False

linkcheck_ignore = [
    # Requires a login, so it always reports 403.
    r"https://roboflow\.com/?$",
    # opencv.org and docs.opencv.org answer 403 to any automated request,
    # including with a browser user agent. The links are correct and work in a
    # browser; they were verified by hand on 2026-09-01.
    r"https://(docs\.)?opencv\.org/.*",
    # Festo blocks automated requests to its product pages.
    r"https://www\.festo(-didactic)?\.com/.*",
    # autodesk.com (not help.autodesk.com) answers 403 to automated requests;
    # the links are correct and work in a browser, verified by hand on
    # 2026-09-02.
    r"https://www\.autodesk\.com/.*",
]

# Sites that reject the default user agent.
user_agent = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

html_show_sourcelink = False
html_copy_source = False
html_last_updated_fmt = "%Y-%m-%d"

# Deploying via GitHub Actions does not run Jekyll, but ".nojekyll" keeps the
# "_static" directory safe if the Pages source is ever switched to a branch.
html_extra_path = ["_extra"]
