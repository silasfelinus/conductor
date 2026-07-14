#!/usr/bin/env python3
"""
roadmap_claims.py — shared claim/staleness rules for roadmap tasks.

Used by claim_task.py (which enforces claimability before writing a claim) and
next_ready_task.py (which treats a stale claim as pickable again). Kept in one
module so the TTL and "what counts as claimed" rule can't drift between the two --
see conductor/t-040 for the rotation-collision this exists to prevent.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

# How long a `status: claimed` task stays locked with no forward progress before a
# picker may treat it as abandoned and pick it again. Generous on purpose -- a real
# burst-mode cycle (research + implementation + PR) can run long; this only needs to
# catch a session that crashed or never returned, not a merely slow one.
CLAIM_TTL_MINUTES = 90


def parse_timestamp(value: Any) -> datetime | None:
    """Parse a roadmap timestamp field into an aware UTC datetime, or None if unparseable."""
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if not isinstance(value, str):
        return None
    text = value.strip().strip("'\"")
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def claim_is_stale(claimed_at: Any, *, now: datetime | None = None) -> bool:
    """True when a `status: claimed` task's claimed_at is old enough to treat as abandoned.

    A missing/unparseable claimed_at on a `claimed` task is itself treated as stale: it
    predates this claim mechanism (or was hand-edited) and carries no fresh signal, so
    it must not be able to lock a task forever.
    """
    parsed = parse_timestamp(claimed_at)
    if parsed is None:
        return True
    now = now or datetime.now(timezone.utc)
    return now - parsed > timedelta(minutes=CLAIM_TTL_MINUTES)


def task_is_claimable(task: dict[str, Any], *, now: datetime | None = None) -> bool:
    """True when a picker may claim this task: it's ready, or an abandoned stale claim."""
    status = task.get("status")
    if status == "ready":
        return True
    if status == "claimed":
        return claim_is_stale(task.get("claimed_at"), now=now)
    return False
