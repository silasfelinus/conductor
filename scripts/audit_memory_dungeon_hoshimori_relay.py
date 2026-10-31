#!/usr/bin/env python3
"""Read-only diagnosis of Hoshimori ArtJobs that never reach RUNNING.

A healthy COMFY heartbeat does not prove the relay's *claim loop* is polling:
heartbeat runs on a separate thread. This compares the twenty durable e07/e08
receipts with queue pause state, global scheduling order and recent relay claim
telemetry. Relay telemetry is in-memory and may disappear across serverless
instances, so its absence is explicitly INCONCLUSIVE, not proof of an outage.

No claim POST, queue mutation, resubmission, or production media write.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import sys
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from audit_memory_dungeon_hoshimori_gallery_readiness import ART, WORLDS
from audit_memory_dungeon_art_delivery import job_identity

POLL_FRESH_SECONDS = 300
MAX_ATTEMPTS = 3
GLOBAL_SAMPLE_SIZE = 200


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return dt.astimezone(timezone.utc) if dt.tzinfo else None


def receipt_index(directory: Path = ART) -> dict[int, tuple[str, str]]:
    """Validate real durable receipts; never guess ArtJob IDs."""
    expected: dict[int, tuple[str, str]] = {}
    for world, (_, ledger, _, validator) in WORLDS.items():
        data = yaml.safe_load((directory / ledger).read_text(encoding="utf-8"))
        for slug, job_id in validator(data, require_jobs=True).items():
            if job_id in expected:
                raise ValueError(f"duplicate Hoshimori ArtJob {job_id}")
            expected[job_id] = (
                f"memory-dungeon-hoshimori-{world}-style-{slug}",
                f"public/images/memory-dungeon/hoshimori/{world}/style-proofs/{slug}.webp",
            )
    if len(expected) != 20:
        raise ValueError("expected twenty independently verified style receipts")
    return expected


def analyze(
    receipts: dict[int, tuple[str, str]],
    jobs: list[dict[str, Any]],
    *,
    paused: bool | None,
    agents: list[dict[str, Any]] | None,
    stats: dict[str, Any] | None,
    global_pending: dict[str, Any] | None,
    now: datetime,
) -> dict[str, Any]:
    """Classify actual blockers without treating ephemeral telemetry as durable."""
    if now.tzinfo is None:
        raise ValueError("now must include a timezone")
    by_id = {}
    for job in jobs:
        try:
            key = int(job.get("id") or 0)
        except (AttributeError, ValueError, TypeError):
            continue
        if key in receipts:
            by_id[key] = job

    counts = {"pending": 0, "running": 0, "done": 0, "failed": 0,
              "cancelled": 0, "missing": 0, "identity_mismatch": 0,
              "other": 0}
    exhausted = []
    candidate_ids = []
    for job_id, (request_id, image_path) in receipts.items():
        job = by_id.get(job_id)
        if job is None:
            counts["missing"] += 1
            continue
        if job_identity(job) != (request_id, image_path, "silasfelinus/kind_robots"):
            counts["identity_mismatch"] += 1
            continue
        status = str(job.get("status") or "").lower()
        counts[status if status in counts else "other"] += 1
        if status == "pending":
            attempts = job.get("attempts")
            if isinstance(attempts, int) and not isinstance(attempts, bool):
                if attempts >= MAX_ATTEMPTS:
                    exhausted.append(job_id)
                else:
                    candidate_ids.append(job_id)

    cutoff = now.astimezone(timezone.utc) - timedelta(seconds=POLL_FRESH_SECONDS)
    fresh = []
    for agent in agents or []:
        seen = _timestamp(agent.get("lastSeenAt"))
        if seen and cutoff <= seen <= now.astimezone(timezone.utc):
            fresh.append(agent)
    compatible = [
        a for a in fresh
        if "COMFY" in (a.get("engines") or [])
    ]
    relay = {
        "telemetry": "observed" if fresh else "unobserved_ephemeral",
        "fresh_pollers": len(fresh),
        "fresh_comfy_pollers": len(compatible),
        "warning": (
            "Relay claim telemetry is process-local; absence does not prove "
            "the relay stopped polling, especially on serverless instances."
        ),
    }

    sample = (global_pending or {}).get("jobs")
    pagination = (global_pending or {}).get("pagination") or {}
    sample = sample if isinstance(sample, list) else []
    positions = [i for i, row in enumerate(sample)
                 if row.get("id") in receipts]
    top = {
        "sampled": len(sample),
        "global_pending_total": pagination.get("totalCount"),
        "first_hoshimori_position": positions[0] + 1 if positions else None,
        "none_in_first_page": bool(sample) and not positions,
        "note": "Queue page sorted by priority DESC then ID ASC; not a claimable-rank guarantee.",
    }
    depth = (stats or {}).get("queueDepth") or {}

    blockers = []
    if paused is True:
        blockers.append("Queue control is PAUSED; claim endpoint cannot hand out jobs.")
    if exhausted:
        blockers.append(
            f"{len(exhausted)} PENDING Hoshimori ArtJobs exhausted the <{MAX_ATTEMPTS} claim budget."
        )
    if counts["missing"] or counts["identity_mismatch"]:
        blockers.append("Some durable Hoshimori receipts are absent or have mismatched live identity.")
    if not fresh:
        blockers.append("No recent relay claim poll observed; process-local telemetry is inconclusive.")
    elif not compatible:
        blockers.append("Recent claim pollers did not advertise COMFY; this observation may be instance-local.")
    if top["none_in_first_page"]:
        blockers.append("No Hoshimori job appears in the first 200 global PENDING rows; scheduling backlog may delay them.")

    if paused is True:
        verdict = "queue_paused"
    elif exhausted and len(exhausted) == counts["pending"]:
        verdict = "all_pending_attempts_exhausted"
    elif counts["missing"] or counts["identity_mismatch"]:
        verdict = "receipt_integrity_blocker"
    elif not fresh:
        verdict = "claim_poll_unobserved_not_proven_down"
    elif not compatible:
        verdict = "comfy_claim_capability_unobserved"
    elif top["none_in_first_page"]:
        verdict = "behind_first_global_pending_page"
    else:
        verdict = "eligible_pending_needs_relay_claim_trace"

    return {
        "source": "read_only_live_queue_and_ephemeral_relay_telemetry",
        "style_receipts": len(receipts),
        "style_states": counts,
        "pending_attempts_exhausted_ids": sorted(exhausted),
        "pending_with_attempts_remaining": len(candidate_ids),
        "queue_paused": paused,
        "global_queue_depth": depth,
        "global_pending_sample": top,
        "relay_claim_poll": relay,
        "verdict": verdict,
        "blockers": blockers,
        "next_probe": (
            "Inspect kr-relay claim loop/pm2 logs and /api/art/queue/claim response "
            "on the render host only after checking queue pause, attempts and global priority."
        ),
    }


def _get(path: str) -> dict[str, Any] | None:
    """Read only; never print credential values or unsuccessful response bodies."""
    import consume_art_queue as consumer
    status, response = consumer.http_json(
        "GET", f"{consumer.KR_BASE_URL}{path}", timeout=35
    )
    if status != 200 or not isinstance(response, dict) or not response.get("success"):
        print(f"::warning::Hoshimori queue probe {path.split('?')[0]} HTTP {status}")
        return None
    data = response.get("data")
    return data if isinstance(data, dict) else None


def main() -> int:
    import consume_art_queue as consumer
    from reconcile_memory_dungeon_art_jobs import server_jobs

    if not consumer.KR_API_TOKEN:
        print("::warning::No KR_API_TOKEN; cannot diagnose live relay claims")
        return 2
    try:
        receipts = receipt_index()
        jobs = server_jobs()
        control = _get("/api/art/queue/control")
        agents = _get("/api/art/queue/relay-status")
        stats = _get("/api/art/queue/stats?summary=true")
        pending = _get(f"/api/art/queue?status=PENDING&pageSize={GLOBAL_SAMPLE_SIZE}&page=1")
        report = analyze(
            receipts, jobs,
            paused=control.get("paused") if control else None,
            agents=agents.get("agents") if agents else None,
            stats=stats,
            global_pending=pending,
            now=datetime.now(timezone.utc),
        )
    except (OSError, ValueError, TypeError, RuntimeError, yaml.YAMLError) as error:
        print(f"::error::Hoshimori queue diagnosis unavailable: {type(error).__name__}")
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
