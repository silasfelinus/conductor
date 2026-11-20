#!/usr/bin/env python3
"""Flag opted-in art ledgers whose accepted ArtJob receipts never reached Git."""

from __future__ import annotations

import argparse
import subprocess
import time
from pathlib import Path

import yaml

from sweep_art_ledgers import ROOT, find_ledgers, open_cells


def last_commit_timestamp(path: Path, root: Path = ROOT) -> int | None:
    result = subprocess.run(
        ["git", "log", "-1", "--format=%ct", "--", str(path.relative_to(root))],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    stamp = result.stdout.strip()
    return int(stamp) if result.returncode == 0 and stamp.isdecimal() else None


def missing_receipts(path: Path, *, now: int, max_age_hours: int = 24, root: Path = ROOT) -> bool:
    data = yaml.safe_load(path.read_text()) or {}
    subjects = data.get("subjects") or []
    if not subjects or open_cells(data) == 0:
        return False
    if any((subject.get("jobs") or {}).get(lane.get("key")) for subject in subjects
           if isinstance(subject, dict) for lane in data.get("lanes") or []
           if isinstance(lane, dict)):
        return False
    timestamp = last_commit_timestamp(path, root)
    return timestamp is not None and now - timestamp >= max_age_hours * 3600


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-age-hours", type=int, default=24)
    args = parser.parse_args(argv)
    overdue = [
        path for path in find_ledgers()
        if missing_receipts(path, now=int(time.time()), max_age_hours=args.max_age_hours)
    ]
    for path in overdue:
        print(f"OVERDUE art ledger without recorded ArtJob receipts: {path.relative_to(ROOT)}")
    return 1 if overdue else 0


if __name__ == "__main__":
    raise SystemExit(main())
