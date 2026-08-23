#!/usr/bin/env python3
"""
daily_gate.py — detect a same-day-gated recurring task that's already done for today.

Kaizen from conductor/t-123 (2026-08-23 scheduled sweep, conductor#2720): a recurring
task gated on "at most once per Pacific calendar day" (e.g. mermaids-of-venice/t-013)
sits at `status: ready` between runs the same as any ordinary claimable task --
`claim_task.py`'s live-status check alone can't tell "genuinely unclaimed" from
"already completed today, just re-armed." A session picked t-013 via the normal
selection path, found an earlier same-day session had already run and recorded it,
and had to release the claim with a no-op explanatory note instead of doing real
work -- wasted a claim/PR cycle, though no roadmap state was corrupted.

This module is deliberately narrow, matching the task's own scoping: it flags tasks
whose note carries an explicit daily/progress-gated contract (the literal phrase
"Pacific calendar day", the same wording every such contract in this repo uses --
see mermaids-of-venice/t-013 and dream-cycle/t-006), not a general-purpose parser
for every recurring task's history. It is pure/read-only -- callers (next_ready_task.py,
run_worker.py's find_ready_task) skip a flagged task and continue to the next
candidate; this never mutates a roadmap or claims anything itself.

The freshness check looks for today's Pacific-calendar date near the word "Pacific"
in the note -- every existing daily-gated task's convention records its outcome as
"... on YYYY-MM-DD Pacific: ..." (a successful batch or a verified no-op), so this
matches the established note-writing convention rather than inventing a new one.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any

try:
    from zoneinfo import ZoneInfo

    _PACIFIC = ZoneInfo("America/Los_Angeles")
except Exception:  # pragma: no cover - zoneinfo is stdlib on 3.9+, this is a defensive fallback
    _PACIFIC = None

# The exact phrase every daily/progress-gated task contract in this repo uses (see
# mermaids-of-venice/t-013, dream-cycle/t-006). Scoped narrowly on purpose -- see
# module docstring.
DAILY_GATE_MARKER = "Pacific calendar day"

# Matches a YYYY-MM-DD date that appears shortly before the word "Pacific" on the
# same line/entry, e.g. "Verified no-op on 2026-08-23 Pacific: ..." or
# "on 2026-08-23 Pacific,". `[^\n]{0,60}?` keeps the match within one written
# sentence/entry rather than spanning unrelated text.
_DATE_NEAR_PACIFIC_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b[^\n]{0,60}?Pacific")


def is_daily_gated(note: Any) -> bool:
    """True when a task's note declares an explicit daily/progress-gated contract."""
    return isinstance(note, str) and DAILY_GATE_MARKER in note


def dates_recorded_in_note(note: Any) -> set[str]:
    """All YYYY-MM-DD dates the note records an outcome for, per the "on <date>
    Pacific" convention. Empty set for a non-string or a note with no such entries."""
    if not isinstance(note, str):
        return set()
    return set(_DATE_NEAR_PACIFIC_RE.findall(note))


def today_pacific(*, now: datetime | None = None) -> str:
    """Today's date (YYYY-MM-DD) in US Pacific time, matching how these contracts
    are written and evaluated. Falls back to the given/UTC instant's own date if
    the `America/Los_Angeles` timezone database is unavailable."""
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    if _PACIFIC is not None:
        now = now.astimezone(_PACIFIC)
    return now.strftime("%Y-%m-%d")


def already_recorded_today(task: dict[str, Any], *, now: datetime | None = None) -> bool:
    """True when `task` carries a daily/progress-gated contract AND its note
    already records an outcome (batch or no-op) for today's Pacific date --
    i.e. claiming it now would just repeat work an earlier session already did.

    False for a task with no daily-gate marker at all, or one gated but not yet
    touched today -- both of those are genuinely claimable.
    """
    note = task.get("note")
    if not is_daily_gated(note):
        return False
    return today_pacific(now=now) in dates_recorded_in_note(note)
