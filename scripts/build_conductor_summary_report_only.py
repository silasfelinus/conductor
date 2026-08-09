#!/usr/bin/env python3
"""Run the hourly Conductor assessment without creating Daily Dream objects.

Daily Dream creation now belongs to the ordered morning digest cycle. The existing
summary module still expects an ``ensure_records`` callable, so this compatibility
entrypoint replaces that one side effect with an explicit idle outcome before calling
the unchanged reporting logic.
"""

from __future__ import annotations

import build_conductor_summary as summary


def report_only_daily_dream(_dry_run: bool = False) -> dict:
    return {
        "status": "idle",
        "message": "Daily Dream creation is owned by the ordered daily-digest cycle.",
    }


def main() -> None:
    summary.build_dream_records.ensure_records = report_only_daily_dream
    summary.main()


if __name__ == "__main__":
    main()
