#!/usr/bin/env python3
"""Check the authored private Dead Air runway without pretending drafts are films."""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml

ROOT = Path(__file__).resolve().parents[1]
EPISODES = ROOT / "projects/dead-air/episodes"


def check_runway(today: str, episodes_dir: Path = EPISODES, days: int = 7) -> list[str]:
    available: set[str] = set()
    for path in sorted(episodes_dir.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if (isinstance(data, dict) and data.get("status") == "authored"
                and isinstance(data.get("date"), str)):
            available.add(data["date"])
    first = datetime.strptime(today, "%Y-%m-%d").date()
    return [
        day for offset in range(days)
        if (day := (first + timedelta(days=offset)).isoformat()) not in available
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--date", default=None)
    args = parser.parse_args()
    if args.days < 1:
        parser.error("--days must be positive")
    today = args.date or datetime.now(ZoneInfo("America/Los_Angeles")).date().isoformat()
    missing = check_runway(today, days=args.days)
    if missing:
        print(f"::warning::Dead Air authored film runway missing {len(missing)} "
              f"of {args.days} upcoming day(s): {', '.join(missing)}. "
              "Author original dated episode briefs; queued ArtJobs do not count.")
    else:
        print(f"Dead Air authored screenplay runway: {args.days}/{args.days} "
              f"dated briefs present from {today}. This is NOT rendered-film proof.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
