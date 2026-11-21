#!/usr/bin/env python3
"""Repair duplicate `updated:` keys inside one roadmap task block.

Hand-edited claim commits pushed straight to main have twice added a fresh
`updated:` beside `claimed_at` while the task's original `updated:` (usually
after a long `note: |-` block) stayed in place. validate_roadmaps.py and
set_task_field.py then refuse the task and process-task-events.yml goes red for
every queued event (emperor-of-dust/t-052 and interface-vision/t-104 on
2026-11-21).

`updated` is a pure last-touched timestamp, so keeping the newest value and
dropping the other line loses nothing. Any OTHER duplicate key is left for
validate_roadmaps.py to fail on: those need a human/agent decision.

Usage: repair_duplicate_updated.py [--check] [roadmap.yaml ...]
Default scans projects/*/roadmap.yaml. --check reports without writing and
exits 1 when a repair is needed.
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASK_START = re.compile(r"^(\s*)- id: (\S+)\s*$")
UPDATED = re.compile(r"^(\s*)updated:\s*['\"]?([^'\"\s#]+)['\"]?\s*$")


def _parse(value: str) -> datetime:
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return datetime.min.replace(tzinfo=timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def repair_text(text: str) -> tuple[str, list[str]]:
    """Return (new_text, [task ids repaired])."""
    lines = text.splitlines(keepends=True)
    drop: set[int] = set()
    repaired: list[str] = []

    starts = [(i, m) for i, line in enumerate(lines) if (m := TASK_START.match(line))]
    for n, (start, m) in enumerate(starts):
        end = starts[n + 1][0] if n + 1 < len(starts) else len(lines)
        field_indent = m.group(1) + "  "
        hits = []
        for i in range(start + 1, end):
            u = UPDATED.match(lines[i])
            if u and u.group(1) == field_indent:
                hits.append((i, u.group(2)))
            elif lines[i].strip() and not lines[i].startswith(field_indent) \
                    and len(lines[i]) - len(lines[i].lstrip()) < len(field_indent):
                break  # left the task mapping (e.g. top-level key after tasks)
        if len(hits) < 2:
            continue
        keep = max(hits, key=lambda h: _parse(h[1]))
        drop.update(i for i, _ in hits if i != keep[0])
        repaired.append(m.group(2))

    if not drop:
        return text, []
    return "".join(l for i, l in enumerate(lines) if i not in drop), repaired


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true")
    ap.add_argument("paths", nargs="*", type=Path)
    args = ap.parse_args(argv)
    paths = args.paths or sorted((ROOT / "projects").glob("*/roadmap.yaml"))

    needed = False
    for path in paths:
        text = path.read_text(encoding="utf-8")
        new, ids = repair_text(text)
        if not ids:
            continue
        needed = True
        verb = "needs repair" if args.check else "repaired"
        print(f"{path.relative_to(ROOT) if path.is_absolute() else path}: {verb} duplicate 'updated' on {', '.join(ids)}")
        if not args.check:
            path.write_text(new, encoding="utf-8")
    return 1 if (needed and args.check) else 0


if __name__ == "__main__":
    sys.exit(main())
