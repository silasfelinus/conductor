#!/usr/bin/env python3
"""Run the Daily Dream builder with freshness and creative-consumption gates.

The transactional writer remains in build_dream_records.py. This scheduled
entrypoint owns automatic candidate policy so old steering proposals cannot
quietly resurface after newer creativity rules land.
"""

from __future__ import annotations

import datetime
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_dream_records as core  # noqa: E402
import check_dream_creative_contract as creative_contract  # noqa: E402

MAX_AUTOBUILD_AGE_DAYS = 2


def eligible_proposal(date_override: Optional[str]) -> tuple[Optional[Path], str]:
    """Select a fresh proposal that also clears today's creative contract.

    Ordinary automatic candidates age out after two Pacific calendar days.
    Pinned transaction retries may be older, and explicit --date builds may
    intentionally backfill an older proposal, but both still re-run the current
    creative contract before any live records are created.
    """
    today_date = datetime.datetime.now(core._TZ).date()
    today = today_date.isoformat()
    best: Optional[tuple[str, Path]] = None
    retry: Optional[tuple[str, Path]] = None
    reason = "no unbuilt proposal ready (none past its steering day)"

    for path, fm, text in core.find_proposals():
        proposal_date = str(fm.get("proposal_date") or fm.get("created") or "")
        status = str(fm.get("status") or "outline")
        if date_override:
            if proposal_date != date_override:
                continue
        elif not (proposal_date and proposal_date < today):
            continue
        if status in ("parked", "vetoed", "built", "building"):
            continue

        proposal = core._data_block(text, "proposal-data")
        contract_errors = core._canonical_proposal_errors(proposal)
        if contract_errors:
            reason = (
                f"{path.name}: invalid canonical proposal — "
                + "; ".join(contract_errors)
            )
            continue
        if core._data_block(text, "built-data"):
            continue
        if core.has_silas_notes(text):
            reason = (
                f"{path.name}: has Notes from Silas — agent must fold them in "
                "before building"
            )
            continue

        attempt = core._data_block(text, "build-attempt-data")
        is_retry = isinstance(attempt, dict) and attempt.get("status") == "retry"

        if not date_override and not is_retry:
            try:
                age_days = (
                    today_date - datetime.date.fromisoformat(proposal_date)
                ).days
            except ValueError:
                reason = f"{path.name}: invalid proposal date {proposal_date!r}"
                continue
            if age_days > MAX_AUTOBUILD_AGE_DAYS:
                reason = (
                    f"{path.name}: stale proposal ({age_days} days old); automatic "
                    f"builds accept at most {MAX_AUTOBUILD_AGE_DAYS} days of backlog"
                )
                continue

        creative_errors = creative_contract.validate_path(path)
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


def main() -> int:
    core.eligible_proposal = eligible_proposal
    return core.main()


if __name__ == "__main__":
    raise SystemExit(main())
