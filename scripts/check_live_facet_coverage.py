#!/usr/bin/env python3
"""
check_live_facet_coverage.py — Ask Kind Robots what Facets each built daily-dream
record ACTUALLY carries, and flag any that were requested but never landed.

Kaizen from dream-cycle/t-026 (2026-09-02). Silas, reading his digest: "I just
don't get the facets added as part of my daily digest, so there is a
discrepancy ... mostly I want parity between what is being made and what is
being reported." Following that back found that
PUT /api/characters/:id/facets ignored `facetKeys` entirely. This pipeline
addresses Facets by slug (ids go stale when catalog rows merge or are deleted),
so its body normalized to zero assignments, the handler's unconditional
deleteMany ran anyway, and it answered success with an empty catalog. Every one
of the 36 built bundles recorded `status: "complete"` with `errors: []` over a
Character carrying no Facets at all.

WHY THIS EXISTS AND apply_daily_dream_facets.py'S OWN STATUS DOES NOT SUFFICE.
That script now verifies its responses, so a fresh build cannot repeat the
original bug silently. But its record is written ONCE, at apply time, from what
the API said in that moment. It cannot see a Facet link deleted afterwards, a
catalog row merged out from under a record, or a repair that was never run on a
bundle built before the fix. Only asking the live records answers that, and
"what does production actually hold" is a different question from "what did we
believe when we wrote it down".

Read-only by default. `--repair` shells out to apply_daily_dream_facets.py
--force, which re-PUTs each bundle's stored seed selection -- the same data the
records should have carried all along.

Needs KR_API_TOKEN; exits 2 (unresolved, not clean) without one, matching
check_project_scaffold_drift.py rather than passing vacuously.

Exit codes:
  0  every recorded Facet target is present on the live record
  1  at least one live record is missing Facets it was built with
  2  could not check (no token, or the API was unreachable)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKLOG = ROOT / "projects" / "dream-cycle" / "backlog"
BASE_URL = os.environ.get("KR_BASE_URL", "https://kindrobots.org").rstrip("/")
BUILT_RE = re.compile(r"<!-- built-data\n(.*?)\n-->", re.DOTALL)

# Every model the daily dream attaches Facets to, and its REST collection.
ENDPOINTS = {
    "Dream": "dreams",
    "Character": "characters",
    "Reward": "rewards",
    "Scenario": "scenarios",
}


def _get(path: str, token: str, *, timeout: int = 45) -> dict:
    request = urllib.request.Request(
        f"{BASE_URL}{path}",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
            "User-Agent": "conductor-live-facet-coverage/1",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        return {"success": False, "message": f"HTTP {error.code}", "data": None}
    except (OSError, ValueError) as error:
        return {"success": False, "message": str(error), "data": None}


def recorded_targets() -> list[dict]:
    """Every Facet target a built bundle says it applied, with its record id."""
    targets: list[dict] = []
    for path in sorted(BACKLOG.glob("*.md")):
        match = BUILT_RE.search(path.read_text(encoding="utf-8"))
        if not match:
            continue
        try:
            built = json.loads(match.group(1))
        except ValueError:
            continue
        assignments = built.get("facet_assignments")
        if not isinstance(assignments, dict):
            continue
        for target in assignments.get("targets") or []:
            if not isinstance(target, dict):
                continue
            collection = ENDPOINTS.get(str(target.get("model")))
            if not collection or not isinstance(target.get("record_id"), int):
                continue
            targets.append({
                "bundle": path.name,
                "element": str(target.get("element") or "?"),
                "model": str(target.get("model")),
                "record_id": target["record_id"],
                "path": f"/api/{collection}/{target['record_id']}/facets",
                "requested": len(target.get("facet_keys") or [])
                or len(target.get("facet_ids") or []),
            })
    return targets


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repair",
        action="store_true",
        help="Re-apply every bundle's stored seed selection when gaps are found.",
    )
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args(argv)

    token = os.environ.get("KR_API_TOKEN", "").strip()
    if not token:
        print("KR_API_TOKEN is absent; live Facet coverage is UNRESOLVED.", file=sys.stderr)
        return 2

    targets = recorded_targets()
    if not targets:
        print("No built bundles with recorded Facet targets. Nothing to check.")
        return 0

    missing: list[dict] = []
    short: list[dict] = []
    unreachable = 0
    empty_by_element: Counter[str] = Counter()
    total_by_element: Counter[str] = Counter()
    live_links = 0

    for target in targets:
        result = _get(target["path"], token)
        rows = result.get("data") if isinstance(result.get("data"), list) else None
        if rows is None:
            unreachable += 1
            print(
                f"  ? {target['model']} #{target['record_id']} ({target['element']}): "
                f"{result.get('message')}",
                file=sys.stderr,
            )
            continue

        total_by_element[target["element"]] += 1
        live_links += len(rows)
        if not rows:
            empty_by_element[target["element"]] += 1
            missing.append({**target, "live": 0})
        elif len(rows) < target["requested"]:
            short.append({**target, "live": len(rows)})

        if args.verbose:
            print(
                f"  {target['bundle'][:34]:34} {target['element']:13} "
                f"{target['model']:9} #{target['record_id']:<6} "
                f"requested={target['requested']:<2} live={len(rows)}"
            )

    print(
        f"Checked {len(targets)} recorded Facet target(s); "
        f"{live_links} live Facet link(s)."
    )
    for element in sorted(total_by_element):
        print(f"  {element:14} {empty_by_element[element]:3} empty / {total_by_element[element]}")

    if unreachable:
        print(f"\n{unreachable} record(s) could not be read.", file=sys.stderr)

    if missing or short:
        print(f"\n{len(missing)} record(s) carry NO Facets they were built with:")
        for target in missing:
            print(
                f"  {target['model']} #{target['record_id']} ({target['element']}) "
                f"from {target['bundle']} — requested {target['requested']}, live 0"
            )
        for target in short:
            print(
                f"  {target['model']} #{target['record_id']} ({target['element']}) "
                f"from {target['bundle']} — requested {target['requested']}, "
                f"live {target['live']}"
            )
        if args.repair:
            print("\nRepairing with apply_daily_dream_facets.py --force ...")
            completed = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "apply_daily_dream_facets.py"), "--force"],
                cwd=ROOT,
                check=False,
            )
            print("Re-run this check to confirm the repair landed.")
            return completed.returncode or 1
        print("\nRe-run with --repair, or run apply_daily_dream_facets.py --force.")
        return 1

    if unreachable:
        return 2

    print("\nLive Facet coverage holds: every built record carries what it was built with.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
