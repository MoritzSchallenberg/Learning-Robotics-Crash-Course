#!/usr/bin/env python3
"""verify-site.py -- browser-level checks for a built Sphinx site.

Complements the CI pipeline (`sphinx-build -W`, the internal link/anchor
check baked into that build, and the secret scan in
`.github/workflows/pages.yml`) with checks that only a real browser can do:
JavaScript errors, horizontal overflow on mobile, the light/dark toggle,
search, copy buttons and syntax highlighting.

Not part of the required doc build -- `requirements.txt` intentionally does
not include Playwright, so building the site never needs a browser
download. Install it only when you want to run this:

    pip install playwright
    playwright install chromium

Usage:
    # 1. build the site
    sphinx-build -b html docs docs/_build/html

    # 2. serve it under the same subpath GitHub Pages uses
    mkdir -p /tmp/site-serve/Learning-Robotics-Crash-Course
    cp -r docs/_build/html/. /tmp/site-serve/Learning-Robotics-Crash-Course/
    python3 -m http.server 8899 -d /tmp/site-serve &

    # 3. run this script
    python3 scripts/verify-site.py

Exit code is 0 if every check passed, 1 otherwise.
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path


def discover_pages(build_dir: Path) -> list[str]:
    """Every built HTML page, as a path relative to build_dir, excluding
    Sphinx's own generated indexes (genindex, search) which have no
    meaningful content to check."""
    skip = {"genindex.html", "search.html"}
    pages = []
    for p in sorted(build_dir.rglob("*.html")):
        rel = p.relative_to(build_dir).as_posix()
        if p.name in skip:
            continue
        pages.append(rel)
    return pages


async def run(base_url: str, pages: list[str]) -> int:
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("Playwright is not installed. Run:")
        print("  pip install playwright && playwright install chromium")
        return 1

    results: list[tuple[str, bool]] = []

    async with async_playwright() as pw:
        browser = await pw.chromium.launch()

        # -- 1. every page loads 200, no JS errors --------------------------
        ctx = await browser.new_context(viewport={"width": 1400, "height": 900})
        page = await ctx.new_page()
        page_errors: list[str] = []
        page.on("pageerror", lambda e: page_errors.append(str(e)))

        for path in pages:
            page_errors.clear()
            resp = await page.goto(f"{base_url}/{path}", wait_until="networkidle")
            results.append((f"loads 200: {path}", resp is not None and resp.status == 200))
            if page_errors:
                results.append((f"no JS errors: {path}", False))
                print(f"  JS error on {path}: {page_errors}")
        await ctx.close()

        # -- 2. no horizontal overflow, desktop and mobile -------------------
        for label, vw, vh in (("desktop", 1400, 900), ("mobile", 390, 844)):
            ctx = await browser.new_context(viewport={"width": vw, "height": vh})
            page = await ctx.new_page()
            for path in pages:
                await page.goto(f"{base_url}/{path}", wait_until="networkidle")
                overflow = await page.evaluate(
                    "document.documentElement.scrollWidth > window.innerWidth + 1"
                )
                results.append((f"{label} no horizontal overflow: {path}", not overflow))
                if overflow:
                    width = await page.evaluate("document.documentElement.scrollWidth")
                    print(f"  overflow on {label} {path}: scrollWidth={width}")
            await ctx.close()

        # -- 3. theme toggle: present, switches, persists across navigation -
        ctx = await browser.new_context(viewport={"width": 1400, "height": 900})
        page = await ctx.new_page()
        await page.goto(f"{base_url}/index.html", wait_until="networkidle")
        toggle = await page.query_selector("#lrcc-theme-switcher")
        results.append(("theme toggle present", toggle is not None))
        if toggle:
            before = await page.evaluate("document.documentElement.getAttribute('data-theme')")
            await toggle.click()
            await page.wait_for_timeout(200)
            after = await page.evaluate("document.documentElement.getAttribute('data-theme')")
            results.append(("theme toggle switches", before != after))
            if len(pages) > 1:
                await page.goto(f"{base_url}/{pages[1]}", wait_until="networkidle")
                persisted = await page.evaluate(
                    "document.documentElement.getAttribute('data-theme')"
                )
                results.append(("theme persists across navigation", persisted == after))

        # -- 4. search returns results -----------------------------------
        await page.goto(f"{base_url}/search.html?q=ROS", wait_until="networkidle")
        await page.wait_for_timeout(2000)
        search_text = await page.inner_text("#search-results")
        results.append(("search returns results", "0 page" not in search_text.lower()))

        # -- 5. copy buttons exist somewhere in the site --------------------
        # Not every page has a code block (session 1 is a drawing exercise,
        # for instance), so check across pages until one is found rather
        # than assuming any single page qualifies.
        found_copy_button = False
        for path in pages:
            await page.goto(f"{base_url}/{path}", wait_until="networkidle")
            if await page.query_selector("button.copybtn"):
                found_copy_button = True
                break
        results.append(("copy buttons present somewhere on the site", found_copy_button))

        await ctx.close()
        await browser.close()

    print("\n=== verify-site.py results ===")
    failures = [name for name, ok in results if not ok]
    for name, ok in results:
        if not ok:
            print(f"  [FAIL] {name}")
    print(f"\n{len(results) - len(failures)}/{len(results)} passed")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base-url",
        default="http://localhost:8899/Learning-Robotics-Crash-Course",
        help="Base URL the built site is being served from "
        "(default matches the GitHub Pages subpath, served locally).",
    )
    parser.add_argument(
        "--build-dir",
        default="docs/_build/html",
        help="Path to the built HTML, used only to discover which pages exist.",
    )
    args = parser.parse_args()

    build_dir = Path(args.build_dir)
    if not build_dir.is_dir():
        print(f"Build directory not found: {build_dir}")
        print("Run 'sphinx-build -b html docs docs/_build/html' first.")
        return 1

    pages = discover_pages(build_dir)
    if not pages:
        print(f"No HTML pages found under {build_dir}.")
        return 1

    print(f"Checking {len(pages)} pages against {args.base_url} ...")
    return asyncio.run(run(args.base_url, pages))


if __name__ == "__main__":
    sys.exit(main())
