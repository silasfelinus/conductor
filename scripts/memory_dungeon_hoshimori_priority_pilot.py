#!/usr/bin/env python3
"""One-shot, bounded priority pilot for four existing Hoshimori map/atlas ArtJobs.

The shared COMFY queue has hundreds of earlier priority-zero jobs. This promotes
ONLY the already-submitted e07/e08 map and Oven atlas proofs to priority +1,
behind interactive priority-100 work. No enqueue, cancel, claim, or media write.
Default mode is dry-run; --apply requires the authenticated workflow.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Any, Callable

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import consume_art_queue as consumer  # noqa: E402
from audit_memory_dungeon_art_delivery import job_identity  # noqa: E402
from audit_memory_dungeon_hoshimori_relay import receipt_index  # noqa: E402
from reconcile_memory_dungeon_art_jobs import server_jobs  # noqa: E402

ART = ROOT / "projects/memory-dungeon/art"
LEDGERS = ("HOSHIMORI-WARM-STYLE-PROOFS.yaml", "HOSHIMORI-HORROR-STYLE-PROOFS.yaml")
CATEGORIES = {"map", "dungeon-atlas"}
TARGET_PRIORITY = 1
MAX_ATTEMPTS = 3


def pilot_receipts(directory: Path = ART) -> dict[int, tuple[str, str]]:
    """Derive the exact four immutable identities from validated durable ledgers."""
    expected = receipt_index(directory)
    selected: dict[int, tuple[str, str]] = {}
    for filename in LEDGERS:
        data = yaml.safe_load((directory / filename).read_text(encoding="utf-8"))
        rows = [r for r in data["requests"] if r.get("category") in CATEGORIES]
        if {r.get("category") for r in rows} != CATEGORIES or len(rows) != 2:
            raise ValueError(f"{filename}: expected exactly one map and one dungeon atlas")
        for row in rows:
            job_id = row.get("last_art_job_id")
            if type(job_id) is not int or job_id not in expected:
                raise ValueError(f"{filename}: invalid durable map/atlas receipt")
            if job_id in selected:
                raise ValueError("duplicate Hoshimori pilot receipt")
            selected[job_id] = expected[job_id]
    if len(selected) != 4:
        raise ValueError("priority pilot must select exactly four existing ArtJobs")
    return selected


def plan_changes(
    receipts: dict[int, tuple[str, str]], jobs: list[dict[str, Any]]
) -> tuple[list[int], dict[int, str]]:
    """Fail closed on missing, forged, exhausted or ineligible jobs BEFORE writes."""
    by_id: dict[int, dict[str, Any]] = {}
    for row in jobs:
        job_id = row.get("id")
        if type(job_id) is int and job_id in receipts:
            if job_id in by_id:
                raise ValueError(f"duplicate live ArtJob {job_id}")
            by_id[job_id] = row
    to_update: list[int] = []
    skipped: dict[int, str] = {}
    for job_id, (request_id, path) in sorted(receipts.items()):
        job = by_id.get(job_id)
        if job is None:
            raise ValueError(f"missing live Hoshimori ArtJob {job_id}")
        if job_identity(job) != (request_id, path, "silasfelinus/kind_robots"):
            raise ValueError(f"forged/mismatched Hoshimori ArtJob {job_id}")
        if job.get("projectSlug") != "memory-dungeon" or job.get("engine") != "COMFY":
            raise ValueError(f"wrong project or engine for Hoshimori ArtJob {job_id}")
        status = job.get("status")
        priority = job.get("priority")
        if type(priority) is not int:
            raise ValueError(f"missing priority on Hoshimori ArtJob {job_id}")
        if status in ("RUNNING", "DONE"):
            skipped[job_id] = status
            continue
        if status != "PENDING":
            raise ValueError(f"ArtJob {job_id} has unsafe status {status}")
        attempts = job.get("attempts")
        if type(attempts) is not int or not 0 <= attempts < MAX_ATTEMPTS:
            raise ValueError(f"ArtJob {job_id} exhausted or lacks attempt budget")
        if priority == 0:
            to_update.append(job_id)
        elif priority >= TARGET_PRIORITY:
            skipped[job_id] = f"already priority {priority}"
        else:
            raise ValueError(f"ArtJob {job_id} has unexpected negative priority")
    return to_update, skipped


def apply_changes(
    receipts: dict[int, tuple[str, str]],
    to_update: list[int],
    post: Callable[[str, str, dict[str, int]], tuple[int, Any]],
) -> list[int]:
    """Update only preflight-approved IDs, validating every server receipt."""
    applied: list[int] = []
    for job_id in to_update:
        url = f"{consumer.KR_BASE_URL}/api/art/queue/{job_id}/priority"
        status, response = post("POST", url, {"priority": TARGET_PRIORITY})
        if status == 409:
            raise RuntimeError(f"ArtJob {job_id} changed state during priority pilot; re-audit")
        if status != 200 or not isinstance(response, dict) or not response.get("success"):
            raise RuntimeError(f"ArtJob {job_id} priority update failed (HTTP {status})")
        job = (response.get("data") or {}).get("job")
        if not isinstance(job, dict) or job.get("id") != job_id:
            raise RuntimeError(f"ArtJob {job_id} priority response identity missing")
        request_id, path = receipts[job_id]
        if job_identity(job) != (request_id, path, "silasfelinus/kind_robots"):
            raise RuntimeError(f"ArtJob {job_id} priority response provenance mismatch")
        if job.get("priority") != TARGET_PRIORITY:
            raise RuntimeError(f"ArtJob {job_id} priority response did not confirm +1")
        applied.append(job_id)
        print(f"ArtJob {job_id}: priority +1 confirmed; status {job.get('status')}")
    return applied


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="change only verified pending map/atlas jobs")
    args = parser.parse_args()
    receipts = pilot_receipts()
    if not consumer.KR_API_TOKEN:
        raise RuntimeError("KR_API_TOKEN unavailable; cannot authenticate ArtJob preflight")
    before = server_jobs()
    to_update, skipped = plan_changes(receipts, before)
    print(f"Hoshimori map/atlas priority pilot: {len(to_update)} pending at zero, "
          f"{len(skipped)} already active/completed/prioritized")
    for job_id, reason in sorted(skipped.items()):
        print(f"ArtJob {job_id}: unchanged ({reason})")
    if not args.apply:
        print("DRY RUN: no ArtJob was changed")
        return 0
    applied = apply_changes(receipts, to_update, consumer.http_json)
    after = {job.get("id"): job for job in server_jobs()}
    for job_id in applied:
        row = after.get(job_id)
        if not row or row.get("priority") != TARGET_PRIORITY:
            raise RuntimeError(f"ArtJob {job_id} priority not durable after refresh")
        if row.get("status") not in ("PENDING", "RUNNING", "DONE"):
            raise RuntimeError(f"ArtJob {job_id} entered unexpected state after update")
    print(f"Verified {len(applied)} durable +1 priority updates; no new ArtJobs submitted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
