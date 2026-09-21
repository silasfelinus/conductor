#!/usr/bin/env python3
"""Submit all staged Daily Dream art requests into the real Kind Robots ArtJob queue.

The daily digest cycle needs a sharp boundary: by the time the email is assembled,
the bundle built that morning should have six durable priority ArtJobs. When requested,
this script also gives those jobs a bounded same-cycle render window so the digest can
show the newest art instead of deliberately lagging one day behind.

This script submits only ``source: dream-cycle`` requests and records each returned
ArtJob id immediately. Waiting only polls the durable ArtJobs; it never re-enqueues or
downloads them. The relay writes Kind Robots targets directly to self-hosted media as
each ArtJob completes, and the digest probes those public paths afterward.
"""

from __future__ import annotations

import argparse
import sys
import time
from typing import Any, Callable


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


def wait_for_daily_dream_jobs(
    jobs: dict[int, str],
    *,
    timeout: int,
    fetch_job: Callable[..., dict[str, Any] | None],
    poll_seconds: float = 5.0,
    sleeper: Callable[[float], None] = time.sleep,
    clock: Callable[[], float] = time.monotonic,
) -> tuple[set[int], dict[int, str], set[int]]:
    """Poll a batch concurrently until DONE, terminal failure, or one global deadline.

    The timeout is for the whole six-image bundle, not six serial per-job timeouts.
    A missing/unreadable job remains pending and the caller can still send the digest
    with a truthful queue placeholder rather than blocking delivery indefinitely.
    """

    pending = set(jobs)
    done: set[int] = set()
    failed: dict[int, str] = {}
    deadline = clock() + max(0, timeout)

    while pending and clock() < deadline:
        for job_id in list(pending):
            job = fetch_job(job_id, timeout=10)
            if not job:
                continue
            status = str(job.get("status") or "").upper()
            if status == "DONE":
                pending.remove(job_id)
                done.add(job_id)
            elif status in {"FAILED", "CANCELLED"}:
                pending.remove(job_id)
                failed[job_id] = status

        if pending:
            remaining = deadline - clock()
            if remaining > 0:
                sleeper(min(poll_seconds, remaining))

    return done, failed, pending


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--wait-timeout",
        type=int,
        default=0,
        help="seconds to give submitted Daily Dream ArtJobs to finish before returning (0 = submit only)",
    )
    args = parser.parse_args(argv)

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
    jobs_to_wait: dict[int, str] = {}

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
            jobs_to_wait[existing] = request_id or image_path
            print(f"  already submitted ArtJob {existing}: {request_id or image_path}")
            continue

        try:
            job_id = consumer.enqueue(consumer.entry_to_job(entry))
            if not requests.record_submitted_job(request_id, job_id):
                raise RuntimeError(
                    f"submitted ArtJob {job_id} but could not persist it on request {request_id!r}"
                )
            submitted += 1
            jobs_to_wait[job_id] = request_id or image_path
            print(f"  submitted ArtJob {job_id}: {request_id or image_path}")
        except Exception as error:  # noqa: BLE001 - submit the rest of the six
            failures += 1
            print(f"  FAILED {request_id or image_path}: {error}", file=sys.stderr)

    if already_ready:
        requests.mark_done(already_ready)

    render_failures = 0
    if args.wait_timeout > 0 and jobs_to_wait:
        print(
            f"Giving {len(jobs_to_wait)} priority Daily Dream ArtJob(s) up to "
            f"{args.wait_timeout}s to finish before digest assembly..."
        )
        done_jobs, failed_jobs, pending_jobs = wait_for_daily_dream_jobs(
            jobs_to_wait,
            timeout=args.wait_timeout,
            fetch_job=requests.fetch_job,
        )
        for job_id in sorted(done_jobs):
            print(f"  rendered ArtJob {job_id}: {jobs_to_wait[job_id]}")
        for job_id, status in sorted(failed_jobs.items()):
            render_failures += 1
            print(
                f"  FAILED ArtJob {job_id} ({status}): {jobs_to_wait[job_id]}",
                file=sys.stderr,
            )
        if pending_jobs:
            pending_list = ", ".join(str(job_id) for job_id in sorted(pending_jobs))
            print(
                f"  {len(pending_jobs)} ArtJob(s) still queued/running at the digest "
                f"deadline ({pending_list}); the email will show queue placeholders."
            )

    print(
        f"Daily Dream ArtJob handoff: {submitted} submitted, "
        f"{already_submitted} already submitted, {len(already_ready)} already live, "
        f"{failures + render_failures} failed."
    )
    return 1 if failures or render_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
