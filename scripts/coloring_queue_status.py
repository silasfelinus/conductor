#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

DEFAULT_QUEUE = Path("projects/coloring-book/color-art-jobs.yaml")
JOB_ID_PATTERN = re.compile(r"\bjob\s+#?(\d+)\b", re.IGNORECASE)
RECOMMENDED_ACTIONS = (
    "repair-queue-integrity",
    "recover-existing-jobs",
    "resolve-fresh-submission-errors",
    "submit-next-batch",
    "inspect-blocked-pending",
    "complete",
)


def load_queue(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("queue root must be a mapping")
    return data


def duplicate_values(values: list[Any]) -> list[Any]:
    counts = Counter(value for value in values if value is not None)
    return sorted(value for value, count in counts.items() if count > 1)


def semantic_gate_job_id(entry: dict[str, Any]) -> int | None:
    match = JOB_ID_PATTERN.search(str(entry.get("semantic_gate_error", "")))
    return int(match.group(1)) if match else None


def requirement_satisfied(summary: dict[str, Any], required_action: str | None) -> bool:
    return required_action is None or summary.get("recommended_action") == required_action


def summarize_queue(data: dict[str, Any], book_slug: str, batch_size: int | None = None) -> dict[str, Any]:
    books = data.get("books")
    if not isinstance(books, list):
        raise ValueError("queue books must be a list")

    book = next((item for item in books if isinstance(item, dict) and item.get("slug") == book_slug), None)
    if book is None:
        raise ValueError(f"book not found: {book_slug}")

    entries = book.get("entries")
    if not isinstance(entries, list):
        raise ValueError(f"book entries must be a list: {book_slug}")

    normalized = [entry for entry in entries if isinstance(entry, dict)]
    statuses = Counter(str(entry.get("status", "missing")) for entry in normalized)
    pending = [entry for entry in normalized if entry.get("status") == "pending"]
    errored = [entry for entry in pending if entry.get("semantic_gate_error")]
    clean_pending = [entry for entry in pending if not entry.get("semantic_gate_error")]
    recovery_candidates = [entry for entry in errored if semantic_gate_job_id(entry) is not None]
    fresh_submission_blocked = [entry for entry in errored if semantic_gate_job_id(entry) is None]

    configured_batch_size = data.get("batch_policy", {}).get("worker_pass_size", 18)
    effective_batch_size = batch_size or int(configured_batch_size)
    if effective_batch_size < 1:
        raise ValueError("batch size must be at least 1")
    next_batch = clean_pending[:effective_batch_size]

    semantic_job_ids = [job_id for entry in errored if (job_id := semantic_gate_job_id(entry)) is not None]
    duplicate_job_ids = duplicate_values(semantic_job_ids)
    duplicate_entry_ids = duplicate_values([entry.get("id") for entry in normalized])
    duplicate_slots = duplicate_values([entry.get("slot") for entry in normalized])

    def entry_summary(entry: dict[str, Any]) -> dict[str, Any]:
        return {
            "slot": entry.get("slot"),
            "id": entry.get("id"),
            "status": entry.get("status"),
            "semantic_gate_error": entry.get("semantic_gate_error"),
            "semantic_gate_error_at": entry.get("semantic_gate_error_at"),
            "semantic_gate_job_id": semantic_gate_job_id(entry),
        }

    queue_integrity_safe = len(duplicate_entry_ids) == 0 and len(duplicate_slots) == 0
    recovery_safe = len(duplicate_job_ids) == 0 and queue_integrity_safe
    recovery_batch = recovery_candidates[:effective_batch_size] if recovery_safe else []
    recovery_actionable = recovery_safe and len(recovery_batch) > 0
    retry_safe = len(errored) == 0 and recovery_safe
    actionable = retry_safe and len(next_batch) > 0

    if not queue_integrity_safe or duplicate_job_ids:
        recommended_action = "repair-queue-integrity"
    elif recovery_actionable:
        recommended_action = "recover-existing-jobs"
    elif fresh_submission_blocked:
        recommended_action = "resolve-fresh-submission-errors"
    elif actionable:
        recommended_action = "submit-next-batch"
    elif pending:
        recommended_action = "inspect-blocked-pending"
    else:
        recommended_action = "complete"

    return {
        "book": book_slug,
        "total_entries": len(normalized),
        "statuses": dict(sorted(statuses.items())),
        "pending": len(pending),
        "pending_with_semantic_gate_error": len(errored),
        "pending_without_semantic_gate_error": len(clean_pending),
        "next_batch": [entry_summary(entry) for entry in next_batch],
        "blocked_pending": [entry_summary(entry) for entry in errored],
        "recovery_candidates": [entry_summary(entry) for entry in recovery_candidates],
        "recovery_candidate_count": len(recovery_candidates) if recovery_safe else 0,
        "recovery_batch": [entry_summary(entry) for entry in recovery_batch],
        "recovery_actionable": recovery_actionable,
        "recovery_actionable_count": len(recovery_batch),
        "fresh_submission_blocked": [entry_summary(entry) for entry in fresh_submission_blocked],
        "fresh_submission_blocked_count": len(fresh_submission_blocked),
        "duplicate_semantic_gate_job_ids": duplicate_job_ids,
        "duplicate_entry_ids": duplicate_entry_ids,
        "duplicate_slots": duplicate_slots,
        "queue_integrity_safe": queue_integrity_safe,
        "recovery_safe": recovery_safe,
        "retry_safe": retry_safe,
        "actionable": actionable,
        "actionable_count": len(next_batch) if retry_safe else 0,
        "recommended_action": recommended_action,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize the canonical coloring-book ArtJob queue without mutating it.")
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--book", default="monster-recast")
    parser.add_argument("--batch-size", type=int)
    parser.add_argument("--require-retry-safe", action="store_true")
    parser.add_argument("--require-actionable", action="store_true")
    parser.add_argument("--require-recovery-candidates", action="store_true")
    parser.add_argument("--require-recovery-actionable", action="store_true")
    parser.add_argument("--require-recommended-action", choices=RECOMMENDED_ACTIONS)
    args = parser.parse_args()

    try:
        summary = summarize_queue(load_queue(args.queue), args.book, args.batch_size)
    except (OSError, ValueError, yaml.YAMLError) as error:
        print(json.dumps({"error": str(error)}, indent=2))
        return 2

    print(json.dumps(summary, indent=2))
    if args.require_retry_safe and not summary["retry_safe"]:
        return 1
    if args.require_actionable and not summary["actionable"]:
        return 1
    if args.require_recovery_candidates and summary["recovery_candidate_count"] == 0:
        return 1
    if args.require_recovery_actionable and not summary["recovery_actionable"]:
        return 1
    if not requirement_satisfied(summary, getattr(args, "require_recommended_action", None)):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
