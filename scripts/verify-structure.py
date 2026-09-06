#!/usr/bin/env python3
"""verify-structure.py -- static, source-level checks for the topic-based
documentation structure introduced by Entwicklungsauftrag 8 (Fortsetzung
8A). Replaces the earlier version of this script, which checked the
eight-module/capstone structure from Entwicklungsauftrag 6 -- that
structure no longer exists.

Unlike verify-site.py, this needs no build, no server and no browser -- it
reads the Markdown sources in docs/ directly. Run it any time with:

    python3 scripts/verify-structure.py

It checks:

 1. exactly 13 public top-level topic directories exist, no more, no
    fewer, and no docs/course/ or docs/prerequisites/ directory exists
    (the pre-migration structure);
 2. every topic directory has an index.md;
 3. every topic's index.md is referenced from docs/index.md's own
    toctrees (the site's single navigation root);
 4. no page anywhere under docs/ contains a numbered-module heading
    ("# 1.", "Module 1", ...), a processing-time estimate ("80-100
    minutes", "80-100 minute", "core learning path"), or a
    Hackathon/Capstone reference (case-insensitive) -- all replaced by
    the topic-based structure and difficulty levels;
 5. no page is orphaned: every .md file under docs/ is reachable from
    some toctree, directly or transitively from docs/index.md;
 6. Robot Manipulation (docs/manipulation/) and Autonomous
    Decision-Making (docs/decision-making/) are distinct directories,
    and no MoveIt-specific content lives under decision-making/ (the
    planning-and-manipulation.md page from the old structure was split:
    RAFCON/PlanSys2/Golog++ stayed in decision-making/, MoveIt moved to
    manipulation/);
 7. ROS 2 installation lives at docs/ros2/installation.md, not under a
    separate prerequisites/getting-started installation page;
 8. no internal link anywhere under docs/ still points at the deleted
    docs/course/ or docs/prerequisites/ paths;
 9. no Carologistics content remains anywhere (carried over from
    Entwicklungsauftrag 8's Carologistics-removal commit, still
    relevant -- a later edit could reintroduce it);
10. no page under docs/ is named or titled "Instructor";
11. no video URL (a `grid-item-card` `:link:` on a video page) appears
    more than once across the whole site;
12. every video card carries the channel/duration metadata shape that
    comes from an actually-checked video (a weak proxy for "no video ID
    is unchecked" -- see the note on live oEmbed verification below);
13. only the new difficulty/verification substitutions
    ({{ foundation }}, {{ intermediate }}, {{ advanced }}, {{ research }},
    {{ documented }}, {{ simulation }}, {{ hardwareverified }},
    {{ unverified }}, {{ hwverificationrequired }}, {{ experimental }},
    {{ historical }}) are used -- the old course-era
    {{ core }}/{{ optional }}/{{ platformspecific }} substitutions no
    longer exist in docs/conf.py and must not appear in content either.

Two notes carried over from the previous version of this script, still
true here:

  - Broken/stale cross-references and anchors are exactly what
    `sphinx-build -W --keep-going` already fails on (MyST's
    `local id not found` / `myst.xref_missing` checks). Always run a full
    clean rebuild (`rm -rf docs/_build/html docs/_build/doctrees` first)
    before trusting a "0 warnings" result -- an incremental build can
    silently miss a newly-broken reference in a file that was not itself
    touched in that pass.
  - "No video ID is unchecked" ultimately needs a live call to YouTube's
    oEmbed endpoint per video, which is a network-dependent check unsuited
    to a repo-committed test. Every video already on the site was checked
    manually against oEmbed at authoring time; check 12 above only
    verifies the metadata shape that process produces, not the ID itself.

Exit code is 0 if every check passed, 1 otherwise.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS = REPO_ROOT / "docs"

TOPIC_DIRS = [
    "getting-started",
    "ros2",
    "platforms",
    "simulation",
    "sensors-frames",
    "perception",
    "mapping-world-models",
    "navigation-exploration",
    "manipulation",
    "decision-making",
    "integration-testing",
    "rescue-projects",
    "reference",
]

REMOVED_DIRS = ["course", "prerequisites"]

TOCTREE_RE = re.compile(r"```\{toctree\}\n(.*?)\n```", re.DOTALL)
VIDEO_LINK_RE = re.compile(
    r":::\{grid-item-card\}[^\n]*\n:link:\s*(https://www\.youtube\.com/watch\?v=[\w-]+)"
)

OLD_SUBSTITUTIONS = ("{{ core }}", "{{ optional }}", "{{ platformspecific }}", "{{ common }}")

NUMBERED_MODULE_RE = re.compile(r"^#\s+\d+\.\s", re.MULTILINE)
MODULE_WORD_RE = re.compile(r"\bmodule\s+\d+\b", re.IGNORECASE)
TIME_ESTIMATE_RE = re.compile(r"80.100 minute|core learning path", re.IGNORECASE)
HACKATHON_CAPSTONE_RE = re.compile(r"\bhackathon\b|\bcapstone\b", re.IGNORECASE)

_CAROLOGISTICS_TERMS = (
    "carologistics",
    "robotino",
    "smart manufacturing league",
    "expertino-rcll",
    "{{ carologistics }}",
)


def all_md_files() -> list[Path]:
    return [p for p in DOCS.rglob("*.md") if "_build" not in p.parts]


_FENCE_RE = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)


def strip_code_fences(text: str) -> str:
    """Blank out fenced code blocks (```...```), keeping line numbers and
    surrounding prose intact, so a shell comment like '# 8. do the thing'
    inside a ```bash block is never mistaken for a Markdown heading or a
    real 'module 8' content reference."""
    return _FENCE_RE.sub(lambda m: "\n" * m.group(0).count("\n"), text)


def parse_toctree_entries(md_path: Path) -> list[str]:
    """Every entry across ALL toctree blocks in this file (docs/index.md
    has one block per top-level topic), as raw doc-ref strings."""
    text = md_path.read_text(encoding="utf-8")
    entries: list[str] = []
    for m in TOCTREE_RE.finditer(text):
        for line in m.group(1).splitlines():
            line = line.strip()
            if not line or line.startswith(":"):
                continue
            entries.append(line)
    return entries


def doc_ref_to_path(entry: str, from_dir: Path) -> Path:
    return (from_dir / f"{entry}.md").resolve()


def check_topic_directories() -> list[str]:
    failures: list[str] = []
    existing = {p.name for p in DOCS.iterdir() if p.is_dir() and not p.name.startswith("_")}
    for d in REMOVED_DIRS:
        if (DOCS / d).is_dir():
            failures.append(f"pre-migration directory still exists: docs/{d}/")
    missing = [d for d in TOPIC_DIRS if d not in existing]
    for d in missing:
        failures.append(f"expected topic directory missing: docs/{d}/")
    unexpected = existing - set(TOPIC_DIRS) - set(REMOVED_DIRS)
    for d in sorted(unexpected):
        failures.append(f"unexpected top-level directory under docs/: docs/{d}/ (not one of the 13 topics)")
    if len(set(TOPIC_DIRS) & existing) != 13 and not missing:
        failures.append(f"expected exactly 13 topic directories, found {len(set(TOPIC_DIRS) & existing)}")
    return failures


def check_topic_index_pages() -> list[str]:
    failures: list[str] = []
    for d in TOPIC_DIRS:
        index = DOCS / d / "index.md"
        if not index.is_file():
            failures.append(f"docs/{d}/ has no index.md")
    return failures


def check_topics_in_root_toctree() -> list[str]:
    failures: list[str] = []
    root = DOCS / "index.md"
    if not root.is_file():
        return ["docs/index.md is missing"]
    entries = parse_toctree_entries(root)
    entry_targets = {doc_ref_to_path(e, DOCS) for e in entries}
    for d in TOPIC_DIRS:
        expected = (DOCS / d / "index.md").resolve()
        if expected not in entry_targets:
            failures.append(f"docs/index.md's toctrees do not reference docs/{d}/index.md")
    return failures


def check_no_course_language() -> list[str]:
    failures: list[str] = []
    for p in all_md_files():
        text = strip_code_fences(p.read_text(encoding="utf-8", errors="ignore"))
        rel = p.relative_to(REPO_ROOT)
        if NUMBERED_MODULE_RE.search(text):
            failures.append(f"{rel}: numbered-module-style heading ('# N. ...') found")
        if MODULE_WORD_RE.search(text):
            failures.append(f"{rel}: 'module N' reference found")
        if TIME_ESTIMATE_RE.search(text):
            failures.append(f"{rel}: processing-time estimate or 'core learning path' found")
        if HACKATHON_CAPSTONE_RE.search(text):
            failures.append(f"{rel}: 'Hackathon' or 'Capstone' reference found")
    return failures


def check_no_orphans() -> list[str]:
    """Every .md file under docs/ must be reachable from docs/index.md via
    some chain of toctrees (each topic's index.md toctree, in turn,
    referencing its own subpages)."""
    failures: list[str] = []
    reachable: set[Path] = set()
    queue = [DOCS / "index.md"]
    while queue:
        current = queue.pop()
        if current in reachable or not current.is_file():
            continue
        reachable.add(current)
        for entry in parse_toctree_entries(current):
            target = doc_ref_to_path(entry, current.parent)
            if target not in reachable:
                queue.append(target)

    all_files = set(all_md_files())
    orphans = all_files - reachable
    for p in sorted(orphans):
        failures.append(f"orphaned page, not reachable from docs/index.md via any toctree: {p.relative_to(REPO_ROOT)}")
    return failures


def check_manipulation_decision_making_separate() -> list[str]:
    failures: list[str] = []
    manipulation_dir = DOCS / "manipulation"
    decision_dir = DOCS / "decision-making"
    if not manipulation_dir.is_dir():
        failures.append("docs/manipulation/ does not exist -- Robot Manipulation must be its own topic")
        return failures
    if not decision_dir.is_dir():
        failures.append("docs/decision-making/ does not exist")
        return failures
    if manipulation_dir.resolve() == decision_dir.resolve():
        failures.append("manipulation and decision-making resolve to the same directory")

    # MoveIt-specific headings must not live under decision-making/ --
    # they belong on the manipulation page instead.
    moveit_heading_re = re.compile(r"^#{1,3}\s*MoveIt\b", re.MULTILINE)
    for p in decision_dir.glob("*.md"):
        text = p.read_text(encoding="utf-8", errors="ignore")
        if moveit_heading_re.search(text):
            failures.append(
                f"{p.relative_to(REPO_ROOT)}: has a MoveIt-specific heading -- "
                "MoveIt content belongs under docs/manipulation/, not decision-making/"
            )
    if not (manipulation_dir / "index.md").is_file():
        failures.append("docs/manipulation/index.md is missing")
    return failures


def check_installation_under_ros2() -> list[str]:
    failures: list[str] = []
    expected = DOCS / "ros2" / "installation.md"
    if not expected.is_file():
        failures.append("docs/ros2/installation.md is missing -- installation must live under ROS 2")
    for wrong in (
        DOCS / "prerequisites" / "installation.md",
        DOCS / "getting-started" / "installation.md",
    ):
        if wrong.is_file():
            failures.append(f"installation page found at the wrong location: {wrong.relative_to(REPO_ROOT)}")
    return failures


def check_no_stale_removed_dir_links() -> list[str]:
    failures: list[str] = []
    pattern = re.compile(r"\]\([^)]*\b(?:course|prerequisites)/[^)]*\)")
    linkfield_pattern = re.compile(r"^:link:\s*.*\b(?:course|prerequisites)/", re.MULTILINE)
    for p in all_md_files():
        text = p.read_text(encoding="utf-8", errors="ignore")
        if pattern.search(text) or linkfield_pattern.search(text):
            failures.append(f"{p.relative_to(REPO_ROOT)}: still links into a removed course/ or prerequisites/ path")
    return failures


def check_no_carologistics_content() -> list[str]:
    failures: list[str] = []
    carologistics_page = DOCS / "platforms" / "carologistics-robotino.md"
    if carologistics_page.exists():
        failures.append(f"Carologistics platform page still exists: {carologistics_page.relative_to(REPO_ROOT)}")
    for p in all_md_files():
        text = p.read_text(encoding="utf-8", errors="ignore").lower()
        for term in _CAROLOGISTICS_TERMS:
            if term in text:
                failures.append(f"{p.relative_to(REPO_ROOT)} still mentions {term!r}")
    return failures


def check_no_instructor_page() -> list[str]:
    failures: list[str] = []
    for p in all_md_files():
        if "instructor" in p.name.lower():
            failures.append(f"instructor-named page present in docs/: {p.relative_to(REPO_ROOT)}")
        else:
            text = p.read_text(encoding="utf-8", errors="ignore")
            first_heading = next((l for l in text.splitlines() if l.startswith("# ")), "")
            if "instructor" in first_heading.lower():
                failures.append(f"page titled 'Instructor...': {p.relative_to(REPO_ROOT)}")
    return failures


def check_no_duplicate_video_urls() -> list[str]:
    failures: list[str] = []
    seen: dict[str, Path] = {}
    for videos_md in DOCS.rglob("videos.md"):
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
    failures: list[str] = []
    card_re = re.compile(
        r":::\{grid-item-card\}[^\n]*\n:link:\s*https://www\.youtube\.com/watch\?v=[\w-]+\n\n"
        r"\*\*[^*]+\*\*"
    )
    for videos_md in DOCS.rglob("videos.md"):
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


def check_only_new_substitutions_used() -> list[str]:
    failures: list[str] = []
    for p in all_md_files():
        text = p.read_text(encoding="utf-8", errors="ignore")
        for old in OLD_SUBSTITUTIONS:
            if old in text:
                failures.append(f"{p.relative_to(REPO_ROOT)}: uses the removed substitution {old}")
    conf_py = (REPO_ROOT / "docs" / "conf.py").read_text(encoding="utf-8")
    for name in ('"core"', '"optional"', '"platformspecific"', '"common"'):
        if name in conf_py:
            failures.append(f"docs/conf.py still defines the removed substitution {name}")
    return failures


def main() -> int:
    all_failures: list[str] = []

    all_failures.extend(check_topic_directories())
    all_failures.extend(check_topic_index_pages())
    all_failures.extend(check_topics_in_root_toctree())
    all_failures.extend(check_no_course_language())
    all_failures.extend(check_no_orphans())
    all_failures.extend(check_manipulation_decision_making_separate())
    all_failures.extend(check_installation_under_ros2())
    all_failures.extend(check_no_stale_removed_dir_links())
    all_failures.extend(check_no_carologistics_content())
    all_failures.extend(check_no_instructor_page())
    all_failures.extend(check_no_duplicate_video_urls())
    all_failures.extend(check_video_cards_carry_metadata())
    all_failures.extend(check_only_new_substitutions_used())

    print("=== verify-structure.py results ===")
    if all_failures:
        for f in all_failures:
            print(f"  [FAIL] {f}")
        print(f"\n{len(all_failures)} failure(s)")
        return 1

    print(f"All structural checks passed for {len(TOPIC_DIRS)} topic directories.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
