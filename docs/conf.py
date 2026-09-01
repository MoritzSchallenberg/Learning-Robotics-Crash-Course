# Configuration file for the Sphinx documentation builder.
#
# Learning Robotics Crash Course -- MASKOR Institute, FH Aachen.
# Full reference: https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------

project = "Learning Robotics Crash Course"
author = "MASKOR Institute, FH Aachen"
copyright = "2026, MASKOR Institute, FH Aachen"
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
# Platform / version badges.
#
# Every platform- or distribution-specific instruction on this site must be
# marked, so that readers never mix up a Humble guide with a Jazzy one.
# Authors write e.g. `{{ carologistics }}` in Markdown; the substitution below
# expands to a styled badge (see _static/css/custom.css).
# ---------------------------------------------------------------------------


def _badge(css_class: str, label: str) -> str:
    return f'<span class="lrcc-badge lrcc-badge--{css_class}">{label}</span>'


myst_substitutions = {
    "common": _badge("common", "COMMON"),
    "simulation": _badge("simulation", "SIMULATION"),
    "carologistics": _badge("carologistics", "CAROLOGISTICS"),
    "alert": _badge("alert", "ALERT"),
    "jazzy": _badge("jazzy", "ROS 2 JAZZY"),
    "humble": _badge("humble", "ROS 2 HUMBLE"),
    "unverified": _badge("unverified", "UNVERIFIED"),
}

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_title = "Learning Robotics Crash Course"

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

html_show_sourcelink = False
html_copy_source = False
html_last_updated_fmt = "%Y-%m-%d"

# Deploying via GitHub Actions does not run Jekyll, but ".nojekyll" keeps the
# "_static" directory safe if the Pages source is ever switched to a branch.
html_extra_path = ["_extra"]
