#!/usr/bin/env python3
"""Submit and refresh every art ledger that opts in with ``auto_submit: true``.

WHY THIS EXISTS. Until 2026-10-22 every ``enqueue_art_requests.py`` ledger needed its own
hand-written step in auto-art-generate.yml. A ledger nobody wired in never reached the render
box: Shifting Lands t-033's 74-card ROUND-4 sat drafted and unsubmitted while the box (about 60
renders an hour) idled with an empty queue, and Silas read the silence as "art gen is not moving".
This sweep finds the opted-in ledgers itself, so drafting a ledger with ``auto_submit: true`` and
merging it is enough.

Per ledger it runs ``--live`` (cells without a job id; ids are written back, so re-runs never
duplicate) and then ``--status`` (records DONE/FAILED and ArtImage ids). A ledger without the flag
is left alone, which keeps drafts private until their author opts in.

Usage:
    python scripts/sweep_art_ledgers.py            # list opted-in ledgers and their open cells
    python scripts/sweep_art_ledgers.py --live     # submit open cells, then refresh status

Environment: KR_API_TOKEN (for --live), KR_BASE_URL.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PATTERNS = ("projects/*/art/*.yaml", "projects/*/art/**/*.yaml")


def is_auto_ledger(data) -> bool:
    """A ledger opts in with a top-level ``auto_submit: true`` and has lanes and subjects."""
    return (
        isinstance(data, dict)
        and data.get("auto_submit") is True
        and isinstance(data.get("lanes"), list)
        and isinstance(data.get("subjects"), list)
    )


def find_ledgers(root: Path | None = None) -> list[Path]:
    root = root or ROOT
    found = set()
    for pattern in PATTERNS:
        for path in root.glob(pattern):
            try:
                data = yaml.safe_load(path.read_text())
            except (OSError, yaml.YAMLError):
                continue
            if is_auto_ledger(data):
                found.add(path)
    return sorted(found)


def open_cells(data) -> int:
    """Cells (subject x lane) that have no job id yet."""
    lanes = [lane["key"] for lane in data.get("lanes") or [] if isinstance(lane, dict) and lane.get("key")]
    count = 0
    for subject in data.get("subjects") or []:
        if not isinstance(subject, dict):
            continue
        jobs = subject.get("jobs") or {}
        # A subject that names its lane renders there only (enqueue_art_requests.iter_cells).
        own = ([subject["lane"]] if subject["lane"] in lanes else []) if subject.get("lane") else lanes
        count += sum(1 for lane in own if not jobs.get(lane))
    return count


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--live", action="store_true", help="submit open cells, then refresh status")
    args = parser.parse_args(argv)

    ledgers = find_ledgers()
    if not ledgers:
        print("no ledgers opt in with auto_submit: true")
        return 0
    if not args.live:
        for path in ledgers:
            print(f"{path.relative_to(ROOT)}: {open_cells(yaml.safe_load(path.read_text()))} open cell(s)")
        return 0

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import enqueue_art_requests as enq

    failed = 0
    for path in ledgers:
        rel = str(path.relative_to(ROOT))
        print(f"== {rel}")
        if enq.main([str(path), "--live"]) != 0:
            failed += 1
        enq.main([str(path), "--status"])
    print(f"swept {len(ledgers)} ledger(s), {failed} with submission failures")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
