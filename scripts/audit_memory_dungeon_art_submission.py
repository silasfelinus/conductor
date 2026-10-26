#!/usr/bin/env python3
"""Check every authored Memory Dungeon request reached the durable ArtJob queue.

This is a submission gate, NOT a claim of completed renders or accepted images.
Reading both ledgers, without page limits, catches partially submitted batches
that otherwise look successful while Kind Robots' relay drains in the background.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PREFIX = "memory-dungeon-saturate-"
LEDGERS = (
    ROOT / "projects/art-prompts.yaml",
    ROOT / "projects/memory-dungeon/art/KNOWN-ART-REQUESTS.yaml",
)


def positive_job_id(value: object) -> bool:
    try:
        return int(value) > 0
    except (TypeError, ValueError):
        return False


def summarize(ledgers: tuple[Path, ...] = LEDGERS) -> dict:
    """Return counts and unresolved IDs; never silently truncate to one page."""
    ids: set[str] = set()
    duplicated: list[str] = []
    unresolved: list[str] = []
    submitted = 0
    satisfied = 0
    per_ledger: dict[str, int] = {}
    for path in ledgers:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        rows = [
            row for row in data.get("requests", [])
            if isinstance(row, dict) and str(row.get("id") or "").startswith(PREFIX)
        ]
        per_ledger[str(path)] = len(rows)
        for row in rows:
            key = str(row["id"])
            if key in ids:
                duplicated.append(key)
            ids.add(key)
            if positive_job_id(row.get("last_art_job_id")):
                submitted += 1
            elif str(row.get("status") or "").lower() == "done":
                # The consumer verified an existing media destination and
                # closed the request without needing a new job.
                satisfied += 1
            else:
                unresolved.append(key)
    return {
        "total": sum(per_ledger.values()),
        "submitted": submitted,
        "satisfied_without_job": satisfied,
        "unresolved": unresolved,
        "duplicate_ids": duplicated,
        "per_ledger": per_ledger,
    }


def main() -> int:
    try:
        report = summarize()
    except (OSError, yaml.YAMLError) as exc:
        print(f"Cannot audit Memory Dungeon art submission: {exc}", file=sys.stderr)
        return 1
    for path, count in report["per_ledger"].items():
        print(f"{Path(path).relative_to(ROOT)}: {count} authored requests")
    print(
        f"Memory Dungeon: {report['total']} total, "
        f"{report['submitted']} ArtJob IDs recorded, "
        f"{report['satisfied_without_job']} previously satisfied, "
        f"{len(report['unresolved'])} NOT submitted"
    )
    if report["total"] < 700 or report["duplicate_ids"] or report["unresolved"]:
        for key in report["duplicate_ids"][:20]:
            print(f"  DUPLICATE {key}", file=sys.stderr)
        for key in report["unresolved"][:30]:
            print(f"  UNSUBMITTED {key}", file=sys.stderr)
        print(
            "::error::Incomplete Memory Dungeon art handoff; do not report "
            "success or art delivery until all requests are accounted for.",
            file=sys.stderr,
        )
        return 1
    print("Submission ledger coverage verified. Rendering and visual QA remain separate gates.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
