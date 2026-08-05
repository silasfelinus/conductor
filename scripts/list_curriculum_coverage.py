#!/usr/bin/env python3
"""
list_curriculum_coverage.py — print every AI Art Academy curriculum movement's
slug/name/era/artist coverage in one shot, parsed straight from the
"Machine-readable skeleton" YAML block in
projects/ai-art-academy/docs/curriculum-outline.md.

Kaizen from conductor PR #1745 (2026-08-05, ai-art-academy/t-010 lane 4):
every lane-4 cycle so far independently re-derived "check
curriculum-outline.md's existing sections and academyStyles.ts's existing
slugs for coverage gaps" from scratch by prose/manual grep. This gives a
future lane-4 (or lane-2 roadmap-accuracy) session the same view in seconds:
which eras are covered, which look thin, and whether any two entries' era
ranges overlap enough to be worth double-checking before adding a new one.

Read-only. No roadmap/YAML mutation, no network access.

Usage:
    python scripts/list_curriculum_coverage.py                # file order (as written)
    python scripts/list_curriculum_coverage.py --sort era      # chronological (parsed from era text)
    python scripts/list_curriculum_coverage.py --sort slug     # alphabetical by slug
    python scripts/list_curriculum_coverage.py --overlaps      # flag era ranges that overlap
    python scripts/list_curriculum_coverage.py --json out.json # also write the parsed list as JSON
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CURRICULUM_OUTLINE = ROOT / "projects" / "ai-art-academy" / "docs" / "curriculum-outline.md"

SKELETON_HEADING = "## Machine-readable skeleton"

# Matches a leading integer in an era string, e.g. "c. 600-400 BCE" -> 600,
# "c. 1600-1750" -> 1600. Good enough for relative ordering/overlap checks,
# not for precise historiography.
YEAR_RE = re.compile(r"(\d{1,4})")


def load_skeleton(text: str) -> list[dict]:
    """Extract and parse the fenced ```yaml block following SKELETON_HEADING."""
    heading_idx = text.find(SKELETON_HEADING)
    if heading_idx == -1:
        raise ValueError(f"'{SKELETON_HEADING}' not found in {CURRICULUM_OUTLINE}")
    remainder = text[heading_idx:]

    fence_start = remainder.find("```yaml")
    if fence_start == -1:
        raise ValueError("no ```yaml fence found after the machine-readable skeleton heading")
    fence_start = remainder.find("\n", fence_start) + 1
    fence_end = remainder.find("\n```", fence_start)
    if fence_end == -1:
        raise ValueError("unterminated ```yaml fence for the machine-readable skeleton")

    block = remainder[fence_start:fence_end]
    data = yaml.safe_load(block)
    if not isinstance(data, dict) or not isinstance(data.get("movements"), list):
        raise ValueError("parsed skeleton block did not contain a 'movements' list")
    return data["movements"]


def era_sort_key(era: str) -> tuple[int, str]:
    """Best-effort chronological sort key: (start_year, original era string).

    BCE eras are negated so they sort before CE ones. Eras with no parseable
    year sort last (int max) rather than crashing or silently sorting first.
    """
    if not era:
        return (sys.maxsize, era or "")
    match = YEAR_RE.search(era)
    if not match:
        return (sys.maxsize, era)
    year = int(match.group(1))
    if "BCE" in era.upper():
        year = -year
    return (year, era)


def era_range(era: str) -> tuple[int, int] | None:
    """Best-effort (start_year, end_year) for overlap checks. None if unparseable."""
    if not era:
        return None
    years = [int(y) for y in YEAR_RE.findall(era)]
    if not years:
        return None
    is_bce = "BCE" in era.upper()
    if is_bce:
        years = [-y for y in years]
    if len(years) == 1:
        return (years[0], years[0])
    return (min(years), max(years))


def find_overlaps(movements: list[dict]) -> list[tuple[dict, dict]]:
    """Pairs of movements whose parsed era ranges overlap. Order-independent, no self-pairs."""
    ranged = []
    for m in movements:
        r = era_range(m.get("era", ""))
        if r is not None:
            ranged.append((m, r))

    overlaps = []
    for i, (m1, r1) in enumerate(ranged):
        for m2, r2 in ranged[i + 1 :]:
            if r1[0] <= r2[1] and r2[0] <= r1[1]:
                overlaps.append((m1, m2))
    return overlaps


def format_row(m: dict) -> str:
    slug = m.get("slug", "?")
    name = m.get("name", "?")
    era = m.get("era", "?")
    artist_count = len(m.get("artist_slugs") or [])
    example_count = m.get("example_count", "?")
    return f"{slug:<28} {name:<38} {era:<20} artists={artist_count:<3} examples={example_count}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--sort",
        choices=["file", "era", "slug"],
        default="file",
        help="Ordering: 'file' (as written), 'era' (parsed chronological), 'slug' (alphabetical). Default: file.",
    )
    parser.add_argument(
        "--overlaps",
        action="store_true",
        help="Additionally list movement pairs whose parsed era ranges overlap.",
    )
    parser.add_argument(
        "--json",
        metavar="PATH",
        help="Also write the parsed movement list as JSON to PATH.",
    )
    args = parser.parse_args()

    if not CURRICULUM_OUTLINE.exists():
        print(f"ERROR: {CURRICULUM_OUTLINE} not found", file=sys.stderr)
        return 1

    try:
        movements = load_skeleton(CURRICULUM_OUTLINE.read_text())
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    ordered = list(movements)
    if args.sort == "era":
        ordered.sort(key=lambda m: era_sort_key(m.get("era", "")))
    elif args.sort == "slug":
        ordered.sort(key=lambda m: m.get("slug", ""))

    print(f"{len(ordered)} movements ({args.sort} order):\n")
    for m in ordered:
        print(format_row(m))

    if args.overlaps:
        overlaps = find_overlaps(movements)
        print(f"\nEra-range overlaps ({len(overlaps)} pair(s)):")
        if not overlaps:
            print("  none")
        else:
            for m1, m2 in overlaps:
                print(f"  {m1.get('slug')} ({m1.get('era')})  <->  {m2.get('slug')} ({m2.get('era')})")

    if args.json:
        Path(args.json).write_text(json.dumps(movements, indent=2) + "\n")
        print(f"\nWrote {len(movements)} movements to {args.json}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
