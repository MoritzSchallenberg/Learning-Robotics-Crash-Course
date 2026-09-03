#!/usr/bin/env python3
"""verify-structure.py -- static, source-level checks for the hierarchical
module/subtopic navigation introduced by Entwicklungsauftrag 6.

Unlike verify-site.py, this needs no build, no server and no browser -- it
reads the Markdown sources in docs/course/ directly. Run it any time with:

    python3 scripts/verify-structure.py

It checks, per module (the 8 numbered course modules plus the capstone):

 1. an overview page exists;
 2. the overview has a subordinate toctree (a `{toctree}` block pointing
    into the module's own subdirectory);
 3. the overview mentions both ALeRT and Carologistics;
 4. the module has a videos.md;
 5. the module has a continue-learning.md;
 6. the module's toctree links both videos.md and continue-learning.md,
    with continue-learning last (videos, then continue-learning, is the
    required closing order before the next main module);
 7. no subpage in the module's own subdirectory is orphaned (missing from
    the overview's toctree);
 8. every subpage is therefore reachable via navigation (a corollary of 7:
    nothing is both present on disk and absent from every toctree).

Site-wide (not per module):

 9. every module directory's toctree entries actually exist on disk (the
    complement of 7/8 -- no toctree entry pointing at a missing file);
10. no video URL (a `grid-item-card` `:link:` on a video page) appears more
    than once across the whole site;
11. no page under docs/ is named or titled "Instructor" (an instructor-only
    page must never ship in the built artifact).

Two items from the task's 13-point list are intentionally NOT
re-implemented here because a better tool already covers them and
duplicating it would only rot out of sync:

  - "no page links to an old/no-longer-existing anchor" is exactly what
    `sphinx-build -W --keep-going` already fails on (MyST's
    `local id not found` / `myst.xref_missing` checks) -- see the
    clean-rebuild rule in every module-restructuring commit this project
    made. Run that build, not a second anchor-checker here.
  - "no video ID is unchecked" needs a live network call to YouTube's
    oEmbed endpoint per video, which is exactly the kind of thing that
    makes a CI check flaky (rate limits, network availability) rather
    than a source-level property this script can assert. Every video
    already on the site was checked manually against oEmbed at authoring
    time (see each module's Interesting videos page); this script only
    checks that every video card carries the fixed metadata shape
    (channel/duration/language) that authoring process produces, as a
    weak proxy that a card was not simply invented.

Previous/Next chain completeness (point 9 in the task's numbering) is a
built-HTML property (Sphinx's `rellinks`, driven by the *global*
`course/index.md` toctree order) -- covered by the browser-level checks
list in verify-site.py's own docstring, not here.

Also checks four regression guards added for Entwicklungsauftrag 7's
content-management changes (installation moved into module 2, module 1
reduced to KiCad/Fusion, the public sources page removed) -- see the
"Entwicklungsauftrag 7 regression checks" section below for what each one
catches and why it exists.

Exit code is 0 if every check passed, 1 otherwise.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS = REPO_ROOT / "docs"
COURSE = DOCS / "course"

# module id -> (overview file, subdirectory holding its subpages)
MODULES: dict[str, tuple[Path, Path]] = {
    "1: Hardware Design with KiCad and Fusion": (COURSE / "01-system-hardware.md", COURSE / "01-hardware"),
    "2: ROS 2 Fundamentals": (COURSE / "02-ros2.md", COURSE / "02-ros2"),
    "3: Sensors, TF2 and RViz": (COURSE / "03-sensors-tf.md", COURSE / "03-sensors-tf"),
    "4: Perception and Object Detection": (COURSE / "04-perception" / "index.md", COURSE / "04-perception"),
    "5: Mapping and Localization": (COURSE / "05-mapping-localization.md", COURSE / "05-mapping-localization"),
    "6: Autonomous Navigation": (COURSE / "06-navigation.md", COURSE / "06-navigation"),
    "7: Autonomous Decisions and Manipulation": (COURSE / "07-autonomous-decisions.md", COURSE / "07-autonomous-decisions"),
    "8: System Integration and Testing": (COURSE / "08-integration.md", COURSE / "08-integration"),
    "Capstone: Autonomous Robot Mission": (COURSE / "hackathon.md", COURSE / "hackathon"),
}

TOCTREE_RE = re.compile(r"```\{toctree\}\n(.*?)\n```", re.DOTALL)
VIDEO_LINK_RE = re.compile(
    r":::\{grid-item-card\}[^\n]*\n:link:\s*(https://www\.youtube\.com/watch\?v=[\w-]+)"
)


def parse_toctree(overview_path: Path) -> list[str]:
    """Every entry in the overview's own (first) toctree block, as raw
    strings exactly as written (relative doc refs, no .md suffix)."""
    text = overview_path.read_text(encoding="utf-8")
    m = TOCTREE_RE.search(text)
    if not m:
        return []
    entries = []
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith(":"):
            continue
        entries.append(line)
    return entries


def toctree_entry_to_path(entry: str, subdir: Path, overview_path: Path) -> Path:
    """Resolve one toctree entry to the .md file it refers to. Entries are
    written relative to the *document* they appear in (docs/course/ for
    every module except module 4, whose overview already lives inside its
    own subdirectory)."""
    base = overview_path.parent
    return (base / f"{entry}.md").resolve()


def check_module(name: str, overview: Path, subdir: Path) -> list[str]:
    failures: list[str] = []

    # 1. overview page exists
    if not overview.is_file():
        failures.append(f"[{name}] overview page missing: {overview.relative_to(REPO_ROOT)}")
        return failures  # nothing else is checkable without it

    text = overview.read_text(encoding="utf-8")

    # 2. subordinate toctree present
    entries = parse_toctree(overview)
    if not entries:
        failures.append(f"[{name}] overview has no subordinate toctree")

    # 3. mentions both ALeRT and Carologistics
    if "ALeRT" not in text:
        failures.append(f"[{name}] overview does not mention ALeRT")
    if "Carologistics" not in text:
        failures.append(f"[{name}] overview does not mention Carologistics")

    # 4 & 5. videos.md and continue-learning.md exist
    videos_md = subdir / "videos.md"
    continue_md = subdir / "continue-learning.md"
    if not videos_md.is_file():
        failures.append(f"[{name}] missing {videos_md.relative_to(REPO_ROOT)}")
    if not continue_md.is_file():
        failures.append(f"[{name}] missing {continue_md.relative_to(REPO_ROOT)}")

    # 6. toctree links both, continue-learning last
    entry_names = [Path(e).name for e in entries]
    if "videos" not in entry_names:
        failures.append(f"[{name}] toctree does not link videos")
    if "continue-learning" not in entry_names:
        failures.append(f"[{name}] toctree does not link continue-learning")
    elif entry_names[-1] != "continue-learning":
        failures.append(
            f"[{name}] toctree does not end with continue-learning "
            f"(ends with {entry_names[-1]!r}); videos-then-continue-learning "
            "must be the closing order before the next main module"
        )
    if "videos" in entry_names and "continue-learning" in entry_names:
        if entry_names.index("videos") > entry_names.index("continue-learning"):
            failures.append(f"[{name}] videos must come before continue-learning in the toctree")

    # 7/8. no orphaned subpage: every .md in subdir is in the toctree
    # (module 4's overview lives inside its own subdir, so exclude it from
    # the "subpage" set it is itself the parent of).
    on_disk = {p for p in subdir.glob("*.md") if p.resolve() != overview.resolve()}
    referenced = {toctree_entry_to_path(e, subdir, overview) for e in entries}
    orphaned = on_disk - referenced
    for p in sorted(orphaned):
        failures.append(f"[{name}] orphaned subpage, not in overview's toctree: {p.relative_to(REPO_ROOT)}")

    # 9. no toctree entry points at a missing file
    missing = referenced - on_disk - {overview.resolve()}
    for p in sorted(missing):
        if not p.is_file():
            failures.append(f"[{name}] toctree entry points at a missing file: {p.relative_to(REPO_ROOT)}")

    return failures


def check_no_duplicate_video_urls() -> list[str]:
    failures: list[str] = []
    seen: dict[str, Path] = {}
    for videos_md in COURSE.rglob("videos.md"):
        text = videos_md.read_text(encoding="utf-8")
        for url in VIDEO_LINK_RE.findall(text):
            if url in seen and seen[url] != videos_md:
                failures.append(
                    f"video URL used twice: {url} "
                    f"(in {seen[url].relative_to(REPO_ROOT)} and {videos_md.relative_to(REPO_ROOT)})"
                )
            else:
                seen[url] = videos_md
    return failures


def check_video_cards_carry_metadata() -> list[str]:
    """Weak proxy for 'no video ID is unchecked': every video card must
    carry the fixed channel/duration metadata line the authoring process
    produces when a video was actually looked up (oEmbed + duration
    scrape), not just a bare link. Does not re-verify the ID itself
    against YouTube -- see the module docstring."""
    failures: list[str] = []
    card_re = re.compile(
        r":::\{grid-item-card\}[^\n]*\n:link:\s*https://www\.youtube\.com/watch\?v=[\w-]+\n\n"
        r"\*\*[^*]+\*\*"
    )
    for videos_md in COURSE.rglob("videos.md"):
        text = videos_md.read_text(encoding="utf-8")
        cards = text.count(":link: https://www.youtube.com/watch?v=")
        metadata_cards = len(card_re.findall(text))
        if cards != metadata_cards:
            failures.append(
                f"{videos_md.relative_to(REPO_ROOT)}: {cards} video card(s) but only "
                f"{metadata_cards} carry the expected channel/duration metadata line "
                "immediately after the link -- looks unchecked"
            )
    return failures


def check_no_instructor_page() -> list[str]:
    failures: list[str] = []
    for p in DOCS.rglob("*.md"):
        if "instructor" in p.name.lower():
            failures.append(f"instructor-named page present in docs/: {p.relative_to(REPO_ROOT)}")
        else:
            text = p.read_text(encoding="utf-8", errors="ignore")
            first_heading = next((l for l in text.splitlines() if l.startswith("# ")), "")
            if "instructor" in first_heading.lower():
                failures.append(f"page titled 'Instructor...': {p.relative_to(REPO_ROOT)}")
    return failures


# -- Entwicklungsauftrag 7 regression checks --------------------------------
# Content-management fixes from Entwicklungsauftrag 7 (installation moved
# into module 2, module 1 reduced to KiCad/Fusion, the public sources page
# removed) are easy to silently reintroduce with an unrelated later edit --
# e.g. re-adding installation.md to prerequisites/index.md's toctree, or a
# stray docs/reference/sources.md reappearing. These four checks exist
# purely to catch that kind of regression, not to re-derive the module
# checks above.

def check_module_1_is_kicad_fusion_only() -> list[str]:
    """Module 1 must carry exactly kicad-schematic, fusion-mechanical-design,
    videos and continue-learning -- no sense-process-act or
    practical-exercise subpage, and no other unexpected subpage."""
    expected = {"kicad-schematic", "fusion-mechanical-design", "videos", "continue-learning"}
    overview, subdir = MODULES["1: Hardware Design with KiCad and Fusion"]
    entries = {Path(e).name for e in parse_toctree(overview)}
    failures: list[str] = []
    if entries != expected:
        missing = expected - entries
        unexpected = entries - expected
        if missing:
            failures.append(f"module 1 toctree is missing expected entries: {sorted(missing)}")
        if unexpected:
            failures.append(f"module 1 toctree has unexpected entries: {sorted(unexpected)}")
    for removed_name in ("sense-process-act.md", "practical-exercise.md"):
        if (subdir / removed_name).exists():
            failures.append(
                f"module 1 subdirectory still contains a removed page: "
                f"{(subdir / removed_name).relative_to(REPO_ROOT)}"
            )
    return failures


def check_module_2_installation_is_first() -> list[str]:
    """Module 2's toctree must list installation as its first subtopic."""
    overview, _ = MODULES["2: ROS 2 Fundamentals"]
    entries = [Path(e).name for e in parse_toctree(overview)]
    if not entries or entries[0] != "installation":
        return [
            f"module 2 toctree does not start with 'installation' "
            f"(starts with {entries[0] if entries else '(empty)'!r})"
        ]
    return []


def check_prerequisites_has_no_installation_page() -> list[str]:
    """The public Prerequisites navigation must not list an installation
    page -- that content now lives at docs/course/02-ros2/installation.md."""
    failures: list[str] = []
    prereq_dir = DOCS / "prerequisites"
    if (prereq_dir / "installation.md").exists():
        failures.append("docs/prerequisites/installation.md still exists on disk")
    index = prereq_dir / "index.md"
    if index.is_file():
        text = index.read_text(encoding="utf-8")
        m = TOCTREE_RE.search(text)
        if m and "installation" in {l.strip() for l in m.group(1).splitlines()}:
            failures.append("docs/prerequisites/index.md's toctree still lists 'installation'")
    return failures


def check_reference_has_no_sources_page() -> list[str]:
    """The Reference section must not list a sources/licenses page."""
    failures: list[str] = []
    if (DOCS / "reference" / "sources.md").exists():
        failures.append("docs/reference/sources.md still exists on disk")
    index = DOCS / "reference" / "index.md"
    if index.is_file():
        text = index.read_text(encoding="utf-8")
        m = TOCTREE_RE.search(text)
        if m and "sources" in {l.strip() for l in m.group(1).splitlines()}:
            failures.append("docs/reference/index.md's toctree still lists 'sources'")
    return failures


def main() -> int:
    all_failures: list[str] = []

    for name, (overview, subdir) in MODULES.items():
        all_failures.extend(check_module(name, overview, subdir))

    all_failures.extend(check_no_duplicate_video_urls())
    all_failures.extend(check_video_cards_carry_metadata())
    all_failures.extend(check_no_instructor_page())
    all_failures.extend(check_module_1_is_kicad_fusion_only())
    all_failures.extend(check_module_2_installation_is_first())
    all_failures.extend(check_prerequisites_has_no_installation_page())
    all_failures.extend(check_reference_has_no_sources_page())

    print("=== verify-structure.py results ===")
    if all_failures:
        for f in all_failures:
            print(f"  [FAIL] {f}")
        print(f"\n{len(all_failures)} failure(s)")
        return 1

    n_modules = len(MODULES)
    print(f"All structural checks passed for {n_modules} modules (8 course modules + capstone).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
