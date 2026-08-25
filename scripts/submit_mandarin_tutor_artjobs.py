#!/usr/bin/env python3
"""Submit a staged Mandarin Tutor batch to Kind Robots without waiting for renders.

The shared request consumer normally enqueues one request and waits for its media
before moving to the next. Mandarin coverage is intentionally batched, so this
small producer submits the whole bounded batch first. The normal consumer still
runs afterward and performs the existing wait/download/media-verification path.
Stable request ids become ArtJob idempotency keys, making the second enqueue a
safe lookup/dedupe rather than a distinct render.
"""

from __future__ import annotations

import argparse
import sys

try:
    from scripts import consume_art_queue as consumer
    from scripts import consume_art_requests as requests
except ImportError:
    import consume_art_queue as consumer
    import consume_art_requests as requests

ID_PREFIX = "mandarin-tutor-v1-"
DEFAULT_LIMIT = 40


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    args = parser.parse_args(argv)
    if args.limit < 1:
        parser.error("--limit must be >= 1")

    if not consumer.KR_API_TOKEN:
        print("KR_API_TOKEN is required to submit Mandarin ArtJobs.", file=sys.stderr)
        return 1

    candidates = requests.filter_by_id_prefix(
        [entry for entry in requests.load_requests() if requests.is_pending(entry)],
        ID_PREFIX,
    )
    safe = [entry for entry in candidates if not requests.weak_prompt_reason(entry)]
    todo = safe[: args.limit]
    requests.apply_default_steps(todo, requests.FILLER_STEPS)

    if not todo:
        print("No pending Mandarin Tutor art requests to submit.")
        return 0

    submitted = 0
    failures = 0
    for entry in todo:
        try:
            job_id = consumer.enqueue(consumer.entry_to_job(entry))
            requests.record_submitted_job(entry.get("id"), job_id)
            submitted += 1
            print(f"  submitted ArtJob {job_id}: {entry.get('id')} -> {entry.get('image_path')}")
        except Exception as error:  # noqa: BLE001 - submit the rest of the batch
            failures += 1
            print(f"  FAILED {entry.get('id')}: {error}", file=sys.stderr)

    print(f"Mandarin ArtJobs submitted: {submitted}/{len(todo)} ({failures} failure(s)).")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
