#!/usr/bin/env python3
"""Pure scheduling helpers for Conductor's pre-ArtJob request staging ledger."""

from __future__ import annotations

from typing import Any, Iterable


def submission_priority(
    entry: dict[str, Any], *, daily_dream_priority: int
) -> int:
    """Return one staged request's scheduling priority.

    Canonical Daily Dream requests use the reserved priority supplied by the
    consumer. Other request producers may set an explicit numeric priority;
    ordinary repair/filler requests remain zero.
    """
    if str(entry.get("source") or "").strip().lower() == "dream-cycle":
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
