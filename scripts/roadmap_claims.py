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

# No-op backoff for recurring tasks (2026-09-30, token essentialization). A recurring
# task re-armed straight back to `ready` after a cycle that found nothing to do is picked
# up again by the very next hourly session: coloring-book/t-022 was claimed 40 times in
# 48h while every next step was gated on Silas, and model-builder/t-029 ran 122 full
# agent sessions that each concluded "no model-builder commits, re-arming". Each of those
# is a whole session's worth of Max-plan usage. `close_task.py --noop` records a
# `noop_streak` and a `rest_until` timestamp; every picker skips the task until then.
# The rest grows with the streak and resets on the first cycle that does real work.
NOOP_REST_HOURS = (2, 6, 12, 24, 48)


def noop_rest_hours(streak: int, max_hours: float | None = None) -> float:
    """Hours a recurring task rests after its `streak`-th consecutive no-op cycle."""
    streak = max(1, int(streak))
    hours = float(NOOP_REST_HOURS[min(streak, len(NOOP_REST_HOURS)) - 1])
    if max_hours is not None:
        hours = min(hours, float(max_hours))
    return hours


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


def task_is_resting(task: dict[str, Any], *, now: datetime | None = None) -> bool:
    """True while a task's `rest_until` timestamp is still in the future.

    An unparseable `rest_until` is ignored (never locks a task), same spirit as
    claim_is_stale treating a bad claimed_at as stale.
    """
    until = parse_timestamp(task.get("rest_until"))
    if until is None:
        return False
    now = now or datetime.now(timezone.utc)
    return now < until


def remaining_scope_delegate_open(task: dict[str, Any], tasks_by_id: dict[str, dict[str, Any]]) -> bool:
    """True when `task` has delegated all its remaining scope to a sibling task
    (via `remaining_scope_task: <task-id>`) that has not reached `status: done` yet.

    An umbrella sweep task can reach a state where every bucket it tracks is at
    zero except one already-owned by a dedicated follow-on task -- claiming the
    umbrella directly at that point only duplicates or collides with the
    follow-on (conductor issue #1627, interface-vision/t-017 vs. t-058). Selectors
    should treat the umbrella as not-yet-claimable for as long as the delegate is
    still open. A missing/unknown delegate id is not itself blocking -- it just
    means this check can't confirm anything, so it falls through to "not delegated".
    """
    delegate_id = task.get("remaining_scope_task")
    if not delegate_id:
        return False
    delegate = tasks_by_id.get(str(delegate_id))
    if delegate is None:
        return False
    return delegate.get("status") != "done"


def task_is_claimable(
    task: dict[str, Any],
    *,
    tasks_by_id: dict[str, dict[str, Any]] | None = None,
    now: datetime | None = None,
) -> bool:
    """True when a picker may claim this task: it's ready, or an abandoned stale claim,
    it isn't resting after a no-op cycle (`rest_until`), and (when `tasks_by_id` is
    supplied) it isn't delegating its remaining scope to a still-open sibling task."""
    status = task.get("status")
    if status == "ready":
        pass
    elif status == "claimed":
        if not claim_is_stale(task.get("claimed_at"), now=now):
            return False
    else:
        return False

    if tasks_by_id is not None and remaining_scope_delegate_open(task, tasks_by_id):
        return False
    if task_is_resting(task, now=now):
        return False
    return True
