#!/usr/bin/env python3
"""Run the Daily Dream builder with creative-consumption gates.

The transactional writer remains in build_dream_records.py. This scheduled
entrypoint owns automatic candidate policy so old steering proposals cannot
quietly resurface after newer creativity rules land.

Candidates are drained OLDEST FIRST, and there is deliberately no age cutoff.
Both used to be the other way round, and together they silently destroyed
creative work: selection took the newest eligible proposal, so any day the
build was blocked (Notes from Silas pending, a contract failure, a retry pin)
the next run reached past that day's proposal to a newer one, and a two-day
age cap then made the skipped proposal permanently ineligible. Five proposals
were stranded that way between 2026-08-12 and 2026-08-21 and had to be
rescued by hand with --date on 2026-08-27..30, which is why a two-week-old
world surfaced in the 2026-08-31 digest.

Dropping the age cap does not let stale creativity through the back door:
every candidate is re-validated against the CURRENT creative contract at
build time below, which is the check that actually enforces "newer creativity
rules land". The age cap was only ever a blunt proxy for that, and it cost
more than it bought.
"""

from __future__ import annotations

import datetime
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_dream_records as core  # noqa: E402
import check_dream_creative_contract as creative_contract  # noqa: E402


def eligible_proposal(date_override: Optional[str]) -> tuple[Optional[Path], str]:
    """Select the oldest proposal past its steering day that clears the contract.

    Pinned transaction retries take priority, and explicit --date builds may
    target any proposal, but every candidate re-runs the current creative
    contract before any live records are created.
    """
    today = datetime.datetime.now(core._TZ).date().isoformat()
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
        # Oldest first: drain the docket in the order it was written so a day
        # that could not build is picked up on the next run instead of orphaned.
        if best is None or proposal_date < best[0]:
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
