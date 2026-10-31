#!/usr/bin/env python3
"""Age-aware, read-only triage for Hoshimori production ArtJobs.

A PENDING ArtJob is a durable submission, not a render or an ArtImage.
Age bands are intentionally stable across frequent audit runs, avoiding
hourly status-file churn while exposing an accumulating queue backlog.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from typing import Any


def _created_utc(value: object) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        created = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if created.tzinfo is None:
        return None
    return created.astimezone(timezone.utc)


def _age_band(hours: float) -> str:
    if hours < 6:
        return "under_6h"
    if hours < 24:
        return "6h_to_24h"
    if hours < 72:
        return "1d_to_3d"
    return "over_3d"


def annotate_queue_age(
    report: dict[str, Any], jobs: list[dict[str, Any]], *,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Add age bands only to identity-validated PENDING/RUNNING receipts.

    Uses ArtJob creation time, not a guessed queue-entry or last-transition
    time. An old RUNNING job may have started recently; its age is advisory,
    not proof of a stuck renderer. Missing or timezone-naive timestamps stay
    unknown. This never promotes a job to DONE or changes delivery counts.
    """
    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None:
        raise ValueError("Queue triage requires timezone-aware now")
    current = current.astimezone(timezone.utc)
    by_id = {}
    for job in jobs:
        try:
            key = int(job.get("id") or 0)
        except (ValueError, TypeError, AttributeError):
            continue
        if key > 0:
            by_id[key] = job

    counts: Counter[str] = Counter()
    for row in report.get("results", []):
        state = row.get("status")
        if state not in ("pending", "running"):
            continue
        job = by_id.get(row.get("jobId"))
        created = _created_utc(job.get("createdAt")) if job else None
        if created is None or created > current:
            band = "unknown"
        else:
            band = _age_band((current - created).total_seconds() / 3600)
        row["queueAgeBand"] = band
        counts[f"{state}:{band}"] += 1

    report["queueTriage"] = {
        "pendingByAge": {band: counts[f"pending:{band}"] for band in (
            "under_6h", "6h_to_24h", "1d_to_3d", "over_3d", "unknown"
        )},
        "runningByAge": {band: counts[f"running:{band}"] for band in (
            "under_6h", "6h_to_24h", "1d_to_3d", "over_3d", "unknown"
        )},
        "meaning": "Age since ArtJob creation; not render duration or proof of failure",
    }
    return report
