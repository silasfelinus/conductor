#!/usr/bin/env python3
"""Pure scheduling helpers for Conductor's pre-ArtJob request staging ledger."""

from __future__ import annotations

from typing import Any, Iterable


def is_daily_dream_request(entry: dict[str, Any]) -> bool:
    return str(entry.get("source") or "").strip().lower() == "dream-cycle"


def positive_job_id(value: Any) -> int | None:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None
    return parsed if parsed > 0 else None


def submission_priority(
    entry: dict[str, Any], *, daily_dream_priority: int
) -> int:
    """Return one staged request's scheduling priority."""
    if is_daily_dream_request(entry):
        return daily_dream_priority
    try:
        return int(entry.get("priority") or 0)
    except (TypeError, ValueError):
        return 0


def prioritize_requests(
    entries: Iterable[dict[str, Any]], *, daily_dream_priority: int
) -> list[dict[str, Any]]:
    """Sort highest priority first while preserving FIFO inside equal tiers."""
    return sorted(
        entries,
        key=lambda entry: submission_priority(
            entry, daily_dream_priority=daily_dream_priority
        ),
        reverse=True,
    )


def should_consume_after_submission(
    entry: dict[str, Any], *, already_satisfied: bool
) -> bool:
    """Avoid re-POSTing a Daily Dream request that already owns an ArtJob.

    Once media is live, let the normal request consumer see the row again so it can
    mark the staging request done. Until then, the relay owns the in-flight ArtJob.
    Other request sources retain their existing behavior.
    """
    if not is_daily_dream_request(entry):
        return True
    if positive_job_id(entry.get("last_art_job_id")) is None:
        return True
    return already_satisfied
