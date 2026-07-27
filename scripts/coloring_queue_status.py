#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

DEFAULT_QUEUE = Path("projects/coloring-book/color-art-jobs.yaml")


def load_queue(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("queue root must be a mapping")
    return data


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

    configured_batch_size = data.get("batch_policy", {}).get("worker_pass_size", 18)
    effective_batch_size = batch_size or int(configured_batch_size)
    if effective_batch_size < 1:
        raise ValueError("batch size must be at least 1")
    next_batch = clean_pending[:effective_batch_size]

    job_ids: list[int] = []
    duplicate_job_ids: list[int] = []
    for entry in errored:
        message = str(entry.get("semantic_gate_error", ""))
        parts = message.split()
        if len(parts) >= 2 and parts[0] == "job" and parts[1].isdigit():
            job_id = int(parts[1])
            if job_id in job_ids and job_id not in duplicate_job_ids:
                duplicate_job_ids.append(job_id)
            job_ids.append(job_id)

    def entry_summary(entry: dict[str, Any]) -> dict[str, Any]:
        return {
            "slot": entry.get("slot"),
            "id": entry.get("id"),
            "status": entry.get("status"),
            "semantic_gate_error": entry.get("semantic_gate_error"),
            "semantic_gate_error_at": entry.get("semantic_gate_error_at"),
        }

    retry_safe = len(errored) == 0 and len(duplicate_job_ids) == 0
    actionable = retry_safe and len(next_batch) > 0

    return {
        "book": book_slug,
        "total_entries": len(normalized),
        "statuses": dict(sorted(statuses.items())),
        "pending": len(pending),
        "pending_with_semantic_gate_error": len(errored),
        "pending_without_semantic_gate_error": len(clean_pending),
        "next_batch": [entry_summary(entry) for entry in next_batch],
        "blocked_pending": [entry_summary(entry) for entry in errored],
        "duplicate_semantic_gate_job_ids": duplicate_job_ids,
        "retry_safe": retry_safe,
        "actionable": actionable,
        "actionable_count": len(next_batch) if retry_safe else 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize the canonical coloring-book ArtJob queue without mutating it.")
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--book", default="monster-recast")
    parser.add_argument("--batch-size", type=int)
    parser.add_argument("--require-retry-safe", action="store_true")
    parser.add_argument("--require-actionable", action="store_true")
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
