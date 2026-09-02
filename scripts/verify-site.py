#!/usr/bin/env python3
"""verify-site.py -- browser-level checks for a built Sphinx site.

Complements the CI pipeline (`sphinx-build -W`, the internal link/anchor
check baked into that build, and the secret scan in
`.github/workflows/pages.yml`) with checks that only a real browser can do:
JavaScript errors, horizontal overflow on mobile, the light/dark toggle,
search, copy buttons, syntax highlighting, and WCAG AA contrast (plus, for
dropdowns, keyboard focus) inside every collapsible dropdown and the
sidebar's auto-expanded current-page branch, in both themes.

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


# Shared by both contrast checks below: parses a computed color, composites
# translucent background layers (a raw rgba() read alone is not the actual
# rendered color -- see RTD's zebra-stripe table overlay), and computes WCAG
# relative luminance / contrast ratio.
_CONTRAST_HELPERS_JS = """
    function parseColor(c) {
        const m = c.match(/rgba?\\(([\\d.]+),\\s*([\\d.]+),\\s*([\\d.]+)(?:,\\s*([\\d.]+))?\\)/);
        if (!m) return null;
        return [parseFloat(m[1]), parseFloat(m[2]), parseFloat(m[3]), m[4] === undefined ? 1 : parseFloat(m[4])];
    }
    function compositedBg(el) {
        // Walk up to <html>, alpha-blending each translucent layer onto a
        // white canvas -- a raw rgba() read (e.g. RTD's zebra-stripe
        // overlay) is not the actual rendered color on its own.
        let layers = [];
        let cur = el;
        while (cur) {
            const p = parseColor(getComputedStyle(cur).backgroundColor);
            if (p && p[3] > 0) layers.push(p);
            if (p && p[3] >= 0.999) break;
            cur = cur.parentElement;
        }
        layers.reverse();
        let acc = [255, 255, 255];
        for (const [r, g, b, a] of layers) {
            acc = [r * a + acc[0] * (1 - a), g * a + acc[1] * (1 - a), b * a + acc[2] * (1 - a)];
        }
        return acc;
    }
    function relLum([r, g, b]) {
        const chan = (c) => { c /= 255; return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4; };
        return 0.2126 * chan(r) + 0.7152 * chan(g) + 0.0722 * chan(b);
    }
    function contrast(a, b) {
        const la = relLum(a) + 0.05, lb = relLum(b) + 0.05;
        return Math.max(la, lb) / Math.min(la, lb);
    }
"""

_CONTRAST_JS = (
    "() => {\n"
    + _CONTRAST_HELPERS_JS
    + """
    const findings = [];
    document.querySelectorAll('details.sd-dropdown').forEach((det, i) => {
        const body = det.querySelector('.sd-summary-content');
        if (!body) return;
        const nodes = body.querySelectorAll('p, li, a, code, td, th, .admonition-title');
        nodes.forEach((el) => {
            const text = (el.textContent || '').trim();
            if (!text) return;
            const fg = parseColor(getComputedStyle(el).color);
            const bg = compositedBg(el);
            if (!fg) return;
            const ratio = contrast([fg[0], fg[1], fg[2]], bg);
            if (ratio < 4.5) {
                findings.push(`dropdown ${i} <${el.tagName.toLowerCase()}> "${text.slice(0, 30)}" ratio=${ratio.toFixed(2)}`);
            }
        });
    });
    return findings;
}
"""
)

# Regression check for the sidebar-specific variant of the same bug: the
# stock RTD theme paints every link inside an *expanded, non-current*
# branch with a hardcoded light gray background
# (`li.toctree-l2.current li.toctree-l3>a{background:#c9c9c9}`), which is
# specific enough to survive this site's own dark-sidebar override and,
# combined with the sidebar's light link text, renders near-invisible.
_SIDEBAR_CONTRAST_JS = (
    "() => {\n"
    + _CONTRAST_HELPERS_JS
    + """
    const findings = [];
    document.querySelectorAll('.wy-menu-vertical a').forEach((el) => {
        const text = (el.textContent || '').trim();
        if (!text) return;
        const fg = parseColor(getComputedStyle(el).color);
        const bg = compositedBg(el);
        if (!fg) return;
        const ratio = contrast([fg[0], fg[1], fg[2]], bg);
        if (ratio < 4.5) {
            findings.push(`sidebar link "${text.slice(0, 40)}" ratio=${ratio.toFixed(2)}`);
        }
    });
    return findings;
}
"""
)


async def _check_dropdown_and_sidebar_contrast(
    browser, base_url: str, pages: list[str]
) -> tuple[list[str], list[str]]:
    """One page-visiting pass, in both themes, covering two related but
    distinct contrast bugs: a dropdown's open body, and the sidebar's
    auto-expanded branch for whichever page is current (every page
    exercises some part of the sidebar tree, not just pages with a
    dropdown, so this runs unconditionally per page rather than only when
    a dropdown is present)."""
    dropdown_failures: list[str] = []
    sidebar_failures: list[str] = []
    ctx = await browser.new_context(viewport={"width": 1280, "height": 900})
    page = await ctx.new_page()
    for theme in ("light", "dark"):
        for path in pages:
            resp = await page.goto(f"{base_url}/{path}", wait_until="networkidle")
            if resp is None or resp.status != 200:
                continue
            await page.evaluate(f"document.documentElement.setAttribute('data-theme', '{theme}')")

            sidebar_findings = await page.evaluate(_SIDEBAR_CONTRAST_JS)
            for f in sidebar_findings:
                sidebar_failures.append(f"{theme} {path}: {f}")

            count = await page.locator("details.sd-dropdown").count()
            if count == 0:
                continue
            for i in range(count):
                summary = page.locator("details.sd-dropdown summary").nth(i)
                await summary.click()
                await page.wait_for_timeout(50)
            findings = await page.evaluate(_CONTRAST_JS)
            for f in findings:
                dropdown_failures.append(f"{theme} {path}: {f}")
            # Keyboard focus must stay visible once sphinx-design's default
            # outline is removed.
            first_summary = page.locator("details.sd-dropdown summary").first
            await first_summary.focus()
            outline = await first_summary.evaluate("el => getComputedStyle(el).outlineStyle")
            if outline == "none":
                dropdown_failures.append(f"{theme} {path}: dropdown summary has no visible keyboard focus outline")
    await ctx.close()
    return dropdown_failures, sidebar_failures


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

        # -- 6. dropdown and sidebar contrast, keyboard focus, light/dark ---
        # Regression check for two related light/dark contrast bugs: a
        # `sphinx-design` dropdown's open body, and the sidebar's
        # auto-expanded branch for the current page -- both fail if any
        # text falls below WCAG AA (4.5:1) against its actual
        # (alpha-composited) background; the dropdown check additionally
        # fails if a summary loses its visible keyboard focus outline.
        dropdown_failures, sidebar_failures = await _check_dropdown_and_sidebar_contrast(
            browser, base_url, pages
        )
        results.append(("dropdown contrast >= 4.5:1 in light and dark", not dropdown_failures))
        for f in dropdown_failures[:20]:
            print(f"  low contrast (dropdown): {f}")
        results.append(("sidebar contrast >= 4.5:1 in light and dark", not sidebar_failures))
        for f in sidebar_failures[:20]:
            print(f"  low contrast (sidebar): {f}")

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
