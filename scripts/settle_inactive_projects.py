#!/usr/bin/env python3
"""settle_inactive_projects.py — no live claims or reviews in paused/finished/retired projects.

WHY (2026-11-01 token-essentialization pass 2). Workers already skip projects
whose `project-overrides.yaml` status is not active/continuous, so a task left
`claimed` or `review` inside an inactive project is never picked up again: it
shows on the Kind Robots board as in-progress work forever, keeps a stale claim
alive, and gets re-reported by sweeps. The 2026-11-01 audit found 11 such tasks
(oldest claim 2026-09-27), including kind-robots/t-131 whose PR #3261 had merged
on 2026-10-06.

What counts: a task in an inactive project whose status is `claimed`,
`in-progress` or `review`. A leftover `claimed_by` on a gated or waiting task
is provenance, not a live claim, and is not touched (resetting it would erase
the gate). `ready`,
`waiting`, `needs-human` and `blocked` tasks in a paused project are parked
for revival and are left alone; they are only counted.

--apply returns each live task to `ready`, clears `claimed_by`/`claimed_at`,
and appends a one-line dated note. It never marks anything `done` — a merged
PR is a reconciliation for `check_pr_merged_drift.py --include-inactive` or
a human, and it never deletes tasks.

Usage:
  python scripts/settle_inactive_projects.py            # report (exit 1 if live work found)
  python scripts/settle_inactive_projects.py --apply    # settle it in the working tree
  python scripts/settle_inactive_projects.py --json

Exit codes: 0 = clean (or applied), 1 = live work found in an inactive project.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from close_task import apply_close  # noqa: E402
from project_lifecycle import WORKABLE_PROJECT_STATUSES, lifecycle_status, load_project_overrides  # noqa: E402

LIVE_STATUSES = {"claimed", "in-progress", "review"}
PARKED_STATUSES = {"ready", "waiting", "needs-human", "blocked", "challenged"}


def scan(root: Path = ROOT) -> dict:
    overrides = load_project_overrides(root / "project-overrides.yaml")
    live, parked = [], {}
    for path in sorted((root / "projects").glob("*/roadmap.yaml")):
        slug = path.parent.name
        if slug.startswith("_"):
            continue
        status = lifecycle_status(overrides, slug)
        if status in WORKABLE_PROJECT_STATUSES:
            continue
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for task in data.get("tasks") or []:
            tstatus = str(task.get("status"))
            if tstatus in LIVE_STATUSES:
                live.append({"project": slug, "lifecycle": status, "task": str(task.get("id")),
                             "status": tstatus, "claimed_at": task.get("claimed_at")})
            elif tstatus in PARKED_STATUSES:
                parked.setdefault(slug, {"lifecycle": status, "count": 0})["count"] += 1
    return {"live": live, "parked": parked}


def settle(root: Path, live: list[dict], today: str) -> None:
    by_project: dict[str, list[dict]] = {}
    for item in live:
        by_project.setdefault(item["project"], []).append(item)
    for slug, items in by_project.items():
        path = root / "projects" / slug / "roadmap.yaml"
        text = path.read_text(encoding="utf-8")
        for item in items:
            note = (f"{today} PT: claim/review released by settle_inactive_projects.py — project is "
                    f"`{item['lifecycle']}`, so no worker will pick this up; was `{item['status']}`. "
                    "Re-check any referenced branch/PR before resuming if the project is reopened.")
            text = apply_close(text, item["task"], "ready", {"claimed_by": "null", "claimed_at": "null"}, note)
        path.write_text(text, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = scan()
    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        parked = sum(v["count"] for v in result["parked"].values())
        print(f"inactive-project live work: {len(result['live'])} task(s); "
              f"parked open tasks: {parked} across {len(result['parked'])} inactive project(s)")
        for item in result["live"]:
            print(f"  - {item['project']}/{item['task']} [{item['lifecycle']}] {item['status']} "
                  f"(claimed_at {item['claimed_at']})")
    if not result["live"]:
        return 0
    if args.apply:
        today = datetime.now(ZoneInfo("America/Los_Angeles")).date().isoformat()
        settle(ROOT, result["live"], today)
        print(f"settled {len(result['live'])} task(s) back to ready")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
