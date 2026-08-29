#!/usr/bin/env python3
"""Guarded Daily Dream record-builder entry point.

The transactional record-creation implementation lives in
``build_dream_records_core.py``. This facade owns proposal-selection policy so a
well-formed but stale steering proposal cannot quietly become today's dream.

Automatic builds accept proposals from the previous two Pacific calendar days.
Older ordinary proposals stay as backlog/idea inventory instead of resurfacing
weeks later. A pinned build retry may be older, because it represents a creation
that already entered the transaction lane. Every candidate, including retries,
must clear the current creative-diversity contract at consumption time.
Explicit ``--date`` builds bypass only the freshness window, not creative safety.
"""

from __future__ import annotations

import datetime
import sys
from pathlib import Path
from typing import Optional

try:  # package import under pytest
    from . import build_dream_records_core as _core
except ImportError:  # direct `python scripts/build_dream_records.py`
    import build_dream_records_core as _core

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_dream_creative_contract as _creative_contract  # noqa: E402

MAX_AUTOBUILD_AGE_DAYS = 2
_core.MAX_AUTOBUILD_AGE_DAYS = MAX_AUTOBUILD_AGE_DAYS
_core.creative_contract = _creative_contract


def eligible_proposal(date_override: Optional[str]):
    """Choose a fresh, creatively valid proposal for the record builder.

    Retry markers retain priority over fresh proposals, but no candidate can
    bypass the current creative contract merely because its file predates that
    contract. Ordinary automatic candidates age out after two Pacific days.
    """
    today_date = datetime.datetime.now(_core._TZ).date()
    today = today_date.isoformat()
    best: Optional[tuple[str, Path]] = None
    retry: Optional[tuple[str, Path]] = None
    reason = "no unbuilt proposal ready (none past its steering day)"

    for path, fm, text in _core.find_proposals():
        proposal_date = str(fm.get("proposal_date") or fm.get("created") or "")
        status = str(fm.get("status") or "outline")
        if date_override:
            if proposal_date != date_override:
                continue
        elif not (proposal_date and proposal_date < today):
            continue
        if status in ("parked", "vetoed", "built", "building"):
            continue

        proposal = _core._data_block(text, "proposal-data")
        contract_errors = _core._canonical_proposal_errors(proposal)
        if contract_errors:
            reason = (
                f"{path.name}: invalid canonical proposal — "
                + "; ".join(contract_errors)
            )
            continue
        if _core._data_block(text, "built-data"):
            continue
        if _core.has_silas_notes(text):
            reason = (
                f"{path.name}: has Notes from Silas — agent must fold them in "
                "before building"
            )
            continue

        attempt = _core._data_block(text, "build-attempt-data")
        is_retry = isinstance(attempt, dict) and attempt.get("status") == "retry"

        if not date_override and not is_retry:
            try:
                age_days = (today_date - datetime.date.fromisoformat(proposal_date)).days
            except ValueError:
                reason = f"{path.name}: invalid proposal date {proposal_date!r}"
                continue
            if age_days > MAX_AUTOBUILD_AGE_DAYS:
                reason = (
                    f"{path.name}: stale proposal ({age_days} days old); automatic "
                    f"builds accept at most {MAX_AUTOBUILD_AGE_DAYS} days of backlog"
                )
                continue

        creative_errors = _core.creative_contract.validate_path(path)
        if creative_errors:
            reason = (
                f"{path.name}: creative contract failed at build time — "
                + "; ".join(creative_errors)
            )
            continue

        if is_retry:
            if retry is None or proposal_date < retry[0]:
                retry = (proposal_date, path)
            continue
        if best is None or proposal_date > best[0]:
            best = (proposal_date, path)

    if retry:
        return retry[1], ""
    if best:
        return best[1], ""
    return None, reason


# Patch the core module's global selection function. Existing imports and tests
# should continue to see the same module surface and monkeypatch the same globals.
_core.eligible_proposal = eligible_proposal

if __name__ == "__main__":
    raise SystemExit(_core.main())

# Under normal imports, return the core module itself after installing the guard.
# This preserves the historical monkeypatch surface (BACKLOG, ART_PROMPTS, etc.).
else:
    sys.modules[__name__] = _core
