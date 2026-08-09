#!/usr/bin/env python3
"""Submit all staged Daily Dream art requests into the real Kind Robots ArtJob queue.

The daily digest cycle needs a sharp boundary: by the time the email is assembled,
the bundle built that morning should have six durable ArtJobs, but nobody should wait
for those renders to finish. Tomorrow's digest is where that art is expected to appear.

This script therefore submits only ``source: dream-cycle`` requests and records each
returned ArtJob id immediately. It does not poll for completion or download images.
The normal auto-art consumer later resumes/finishes those requests, while the relay can
write Kind Robots targets directly to self-hosted media as each ArtJob completes.
"""

from __future__ import annotations

import sys
from typing import Any


def positive_job_id(value: Any) -> int | None:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None
    return parsed if parsed > 0 else None


def is_daily_dream_request(entry: dict[str, Any]) -> bool:
    return str(entry.get("source") or "").strip().lower() == "dream-cycle"


def pending_daily_dream_requests(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        entry
        for entry in entries
        if is_daily_dream_request(entry)
        and str(entry.get("status") or "pending").strip().lower() == "pending"
    ]


def main() -> int:
    # Import the media wrapper only in the executable path. Importing it patches
    # the shared consumer for direct-media routing; keeping that side effect out of
    # module import makes the pure selectors above safe for the full pytest suite.
    import consume_art_requests_to_media as media  # noqa: PLC0415

    requests = media.requests
    consumer = media.consumer

    if not consumer.KR_API_TOKEN:
        print("KR_API_TOKEN is required to submit Daily Dream ArtJobs.", file=sys.stderr)
        return 1

    staged = pending_daily_dream_requests(requests.load_requests())
    if not staged:
        print("No pending Daily Dream art requests need ArtJob submission.")
        return 0

    failures = 0
    submitted = 0
    already_submitted = 0
    already_ready: list[str] = []

    for entry in staged:
        request_id = str(entry.get("id") or "").strip()
        image_path = str(entry.get("image_path") or "").strip()

        if requests.already_satisfied(entry):
            if request_id:
                already_ready.append(request_id)
            print(f"  already live: {image_path}")
            continue

        existing = positive_job_id(entry.get("last_art_job_id"))
        if existing:
            already_submitted += 1
            print(f"  already submitted ArtJob {existing}: {request_id or image_path}")
            continue

        try:
            job_id = consumer.enqueue(consumer.entry_to_job(entry))
            if not requests.record_submitted_job(request_id, job_id):
                raise RuntimeError(
                    f"submitted ArtJob {job_id} but could not persist it on request {request_id!r}"
                )
            submitted += 1
            print(f"  submitted ArtJob {job_id}: {request_id or image_path}")
        except Exception as error:  # noqa: BLE001 - submit the rest of the six
            failures += 1
            print(f"  FAILED {request_id or image_path}: {error}", file=sys.stderr)

    if already_ready:
        requests.mark_done(already_ready)

    print(
        f"Daily Dream ArtJob handoff: {submitted} submitted, "
        f"{already_submitted} already submitted, {len(already_ready)} already live, "
        f"{failures} failed."
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
