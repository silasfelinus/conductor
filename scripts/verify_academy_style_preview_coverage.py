#!/usr/bin/env python3
"""
verify_academy_style_preview_coverage.py — for every AI Art Academy movement in
kind_robots' stores/seeds/academyStyles.ts that sets a `previewImageSrc`, confirm
the image is actually delivered at media.acrocatranch.com, and if not, confirm
projects/art-prompts.yaml carries a matching `kind-robots-academy-style-preview-<slug>`
request (any status). A slug that is neither delivered nor queued is the real gap
class ai-art-academy/t-055 was filed for.

Kaizen from ai-art-academy/t-055 (2026-08-05): this gap recurred three times
(fauvism; tonalism/barbizon-school; american-luminism/egyptian-painting/heidelberg-school)
because each lane-4 cycle that added a curriculum entry with previewImageSrc deferred
image generation to "a future lane 3," and no later cycle reliably caught an uncaught
gap except by re-diffing live delivery against every slug from scratch. This script
gives that diff in one command instead.

Kaizen from ai-art-academy/t-010 lane 3 (2026-08-06, kind_robots PR #1523): the checks
above only ever look at slugs that already SET previewImageSrc — a slug with no
previewImageSrc field at all (never opted in) was invisible to every category, so a
clean run meant "clean among the slugs that opted in," not "clean." This is exactly
how `mannerism` and `spanish-golden-age` sat with no preview-image slot at all until a
manual full-file sweep found them by hand. The script now separately enumerates every
`slug:` in academyStyles.ts (regardless of previewImageSrc) and reports the ones with
no previewImageSrc field as their own `no_preview_field` category, distinct from
delivered/queued/gap.

art-prompts.yaml alone is NOT a reliable signal: entries for delivered images are
pruned once fulfilled (see the file's own header), so most delivered slugs have no
entry at all — that's expected, not a gap. The live delivery check is what actually
distinguishes "already fine" from "needs a request." That's why this script does a
live HEAD check by default; pass --offline only when network access genuinely isn't
available (e.g. a sandboxed CI job), and treat its output as advisory only — an
offline "missing" is unqueued-AND-undelivered-by-art-prompts.yaml's-own-record, but
can't rule out an already-delivered-but-pruned entry the way --live can.

Usage:
    python scripts/verify_academy_style_preview_coverage.py             # live check (default)
    python scripts/verify_academy_style_preview_coverage.py --offline   # skip network, less reliable
    python scripts/verify_academy_style_preview_coverage.py --json out.json
    python scripts/verify_academy_style_preview_coverage.py --strict    # exit 1 on any real gap
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
KIND_ROBOTS_ROOT = Path(
    os.environ.get("KIND_ROBOTS_ROOT", REPO_ROOT.parent / "kind_robots")
)
ACADEMY_STYLES_PATH = KIND_ROBOTS_ROOT / "stores" / "seeds" / "academyStyles.ts"
ART_PROMPTS_PATH = REPO_ROOT / "projects" / "art-prompts.yaml"

MEDIA_BASE_URL = os.environ.get("KR_MEDIA_BASE_URL", "https://media.acrocatranch.com").rstrip("/")
PREVIEW_IMAGE_DIR = "images/academy/styles"
ART_PROMPTS_ID_PREFIX = "kind-robots-academy-style-preview-"

SLUG_RE = re.compile(r"^\s*slug:\s*'([a-z0-9-]+)',?\s*$", re.MULTILINE)
PREVIEW_RE = re.compile(
    r"^\s*previewImageSrc:\s*'/" + re.escape(PREVIEW_IMAGE_DIR) + r"/([a-z0-9-]+)\.webp',?\s*$",
    re.MULTILINE,
)


def load_all_academy_style_slugs(text: str) -> list[str]:
    """Return every `slug: '...'` in academyStyles.ts, in file order, regardless
    of whether that style object sets previewImageSrc. This is the independent
    enumeration `load_academy_style_slugs` can't provide on its own, since that
    function only ever sees slugs that already opted into previewImageSrc."""
    slug_matches = list(SLUG_RE.finditer(text))
    if not slug_matches:
        raise ValueError(f"no `slug: '...'` entries found in {ACADEMY_STYLES_PATH}")
    return [m.group(1) for m in slug_matches]


def load_academy_style_slugs(text: str) -> dict[str, str]:
    """Return {slug: previewImageSrc-slug} for every style object that sets
    previewImageSrc, parsed from academyStyles.ts's array-literal source.

    Each style is a `{ ... }` object starting with a `slug: '...'` line; the
    optional `previewImageSrc: '...'` line (if present) appears somewhere
    before the next object's `slug:` line. Regex-based rather than a real TS
    parser, matching the file's consistent single-quoted-field formatting.
    """
    slug_matches = list(SLUG_RE.finditer(text))
    if not slug_matches:
        raise ValueError(f"no `slug: '...'` entries found in {ACADEMY_STYLES_PATH}")

    result: dict[str, str] = {}
    for i, m in enumerate(slug_matches):
        slug = m.group(1)
        start = m.end()
        end = slug_matches[i + 1].start() if i + 1 < len(slug_matches) else len(text)
        block = text[start:end]
        preview_match = PREVIEW_RE.search(block)
        if preview_match:
            result[slug] = preview_match.group(1)
    return result


def load_art_prompts_slugs(text: str) -> dict[str, dict]:
    """Return {slug: entry} for every art-prompts.yaml `requests:` entry whose id
    starts with ART_PROMPTS_ID_PREFIX, keyed by the slug derived from its
    image_path basename (not the id suffix, since id and image_path could in
    principle diverge)."""
    data = yaml.safe_load(text)
    if not isinstance(data, dict) or not isinstance(data.get("requests"), list):
        raise ValueError(f"expected a top-level 'requests:' list in {ART_PROMPTS_PATH}")

    result: dict[str, dict] = {}
    for entry in data["requests"]:
        if not isinstance(entry, dict):
            continue
        entry_id = entry.get("id", "")
        if not isinstance(entry_id, str) or not entry_id.startswith(ART_PROMPTS_ID_PREFIX):
            continue
        image_path = entry.get("image_path", "")
        slug = Path(image_path).stem if image_path else entry_id[len(ART_PROMPTS_ID_PREFIX):]
        result[slug] = entry
    return result


def check_live(slug: str, timeout: float = 10.0) -> int | None:
    """HEAD-check the delivered media URL for `slug`. Returns the HTTP status code,
    or None if the request failed outright (network/DNS/timeout — not a 4xx/5xx)."""
    url = f"{MEDIA_BASE_URL}/{PREVIEW_IMAGE_DIR}/{slug}.webp"
    req = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status
    except urllib.error.HTTPError as exc:
        return exc.code
    except (urllib.error.URLError, TimeoutError, OSError):
        return None


def build_report(
    style_slugs: dict[str, str],
    prompt_slugs: dict[str, dict],
    offline: bool,
    all_slugs: list[str] | None = None,
) -> dict:
    delivered = []
    queued = []
    gaps = []

    for style_slug, preview_slug in sorted(style_slugs.items()):
        entry = prompt_slugs.get(preview_slug)
        live_status = None if offline else check_live(preview_slug)

        if live_status == 200:
            delivered.append({"slug": style_slug, "preview_slug": preview_slug})
        elif entry is not None:
            queued.append(
                {"slug": style_slug, "preview_slug": preview_slug, "status": entry.get("status")}
            )
        else:
            row = {"slug": style_slug, "preview_slug": preview_slug}
            if not offline:
                row["live_status"] = live_status
            gaps.append(row)

    # Slugs that never set previewImageSrc at all — invisible to every category
    # above, since those are all keyed off style_slugs (which only contains
    # slugs that already opted in). `all_slugs` is optional so callers that
    # only have the previewImageSrc-scoped dict (e.g. older direct callers of
    # build_report) still get a report, just without this category populated.
    no_preview_field = sorted(set(all_slugs or []) - set(style_slugs))

    return {
        "offline": offline,
        "style_count_with_preview": len(style_slugs),
        "art_prompts_academy_entry_count": len(prompt_slugs),
        "delivered_count": len(delivered),
        "queued_count": len(queued),
        "gap_count": len(gaps),
        "no_preview_field_count": len(no_preview_field),
        "delivered": delivered,
        "queued": queued,
        "gaps": gaps,
        "no_preview_field": no_preview_field,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--offline",
        action="store_true",
        help=(
            "Skip the live media.acrocatranch.com check. Faster but less reliable: "
            "a slug with no art-prompts.yaml entry is reported as a gap even if it "
            "was already delivered and its request pruned (the common case)."
        ),
    )
    parser.add_argument("--json", metavar="PATH", help="Also write the full report as JSON to PATH.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 if any real gap is found (default: always exit 0, report-only).",
    )
    args = parser.parse_args()

    if not ACADEMY_STYLES_PATH.exists():
        print(f"ERROR: {ACADEMY_STYLES_PATH} not found (set KIND_ROBOTS_ROOT?)", file=sys.stderr)
        return 1
    if not ART_PROMPTS_PATH.exists():
        print(f"ERROR: {ART_PROMPTS_PATH} not found", file=sys.stderr)
        return 1

    try:
        academy_styles_text = ACADEMY_STYLES_PATH.read_text()
        style_slugs = load_academy_style_slugs(academy_styles_text)
        all_slugs = load_all_academy_style_slugs(academy_styles_text)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    prompt_slugs = load_art_prompts_slugs(ART_PROMPTS_PATH.read_text())
    report = build_report(style_slugs, prompt_slugs, args.offline, all_slugs=all_slugs)

    if args.offline:
        print(
            "OFFLINE MODE — no live delivery check performed; 'gaps' below may include "
            "slugs that are actually already delivered with a pruned request. Re-run "
            "without --offline for a reliable read.\n"
        )

    print(
        f"{len(all_slugs)} style(s) total, {report['style_count_with_preview']} set previewImageSrc: "
        f"{report['delivered_count']} delivered, "
        f"{report['queued_count']} queued (not yet delivered), "
        f"{report['gap_count']} real gap(s) (neither delivered nor queued), "
        f"{report['no_preview_field_count']} with no previewImageSrc field at all.\n"
    )
    if report["gaps"]:
        print("GAPS — no delivered image and no art-prompts.yaml request:")
        for row in report["gaps"]:
            extra = f" (live check: HTTP {row['live_status']})" if "live_status" in row else ""
            print(f"  {row['slug']}{extra}")
    else:
        print("No gaps found.")

    if report["no_preview_field"]:
        print("\nNO PREVIEWIMAGESRC FIELD — never opted in, invisible to the categories above:")
        for slug in report["no_preview_field"]:
            print(f"  {slug}")

    if report["queued"]:
        print("\nQueued (already has a request, awaiting delivery):")
        for row in report["queued"]:
            print(f"  {row['slug']} (status={row['status']})")

    if args.json:
        Path(args.json).write_text(json.dumps(report, indent=2) + "\n")
        print(f"\nWrote report to {args.json}")

    if args.strict and (report["gap_count"] or report["no_preview_field_count"]):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
