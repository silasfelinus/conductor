#!/usr/bin/env python3
"""Repair and requeue failed Kind Robots ArtJobs with reviewed repair policies.

The standing repair policy is intentionally narrow: only Kind Robots-targeted
FAILED jobs with a legacy image path or retired vague style token are selected.
Everything else is reported with a bounded, prompt-free diagnostic.

A temporary exact-ID cleanup for the 2026-08-12 incident removes the redundant
replacement pair created when the independent repair and auto-art workflows ran
concurrently. It never deletes an ArtJob or image: it keeps the most-progressed
member of each duplicate pair and cancels only the redundant queue row.
Dry-run by default.
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import consume_art_queue as consumer  # noqa: E402

KIND_ROBOTS_REPO = "silasfelinus/kind_robots"
PAGE_SIZE = 200
REQUEUE_BATCH_SIZE = 100
DIAGNOSTIC_ERROR_LIMIT = 1000
VAGUE_ART_DIRECTION = re.compile(
    r"\b(?:(?:rich|cohesive|friendly)\s+)?Kind\s+Robots\s+"
    r"(?:visual\s+)?(?:style|language)\b",
    re.IGNORECASE,
)

# One-shot cleanup after the 2026-08-12 failed-job migration. The standalone
# repair workflow created 8276/8278; the simultaneously-started Auto Art
# Generate workflow created 8277/8279 from an earlier FAILED-list snapshot.
# Prefer whichever member has already progressed farther, otherwise keep the
# first-created replacement. 8275 is the single A1111 -> Krea2 replacement and
# is status-reported only.
INCIDENT_STATUS_JOB_ID = 8275
INCIDENT_DUPLICATE_PAIRS = ((8276, 8277), (8278, 8279))
STATUS_RANK = {
    "DONE": 5,
    "RUNNING": 4,
    "PENDING": 3,
    "FAILED": 2,
    "CANCELLED": 1,
}


def failed_jobs():
    page = 1
    while True:
        status, response = consumer.http_json(
            "GET",
            f"{consumer.KR_BASE_URL}/api/art/queue"
            f"?status=FAILED&page={page}&pageSize={PAGE_SIZE}",
        )
        if status != 200 or not response or not response.get("success"):
            raise RuntimeError(
                f"failed ArtJob listing returned HTTP {status}: "
                f"{response and response.get('message')}"
            )

        data = response.get("data") or {}
        jobs = data.get("jobs") or []
        for job in jobs:
            if isinstance(job, dict):
                yield job

        pagination = data.get("pagination") or {}
        if not pagination.get("hasNextPage"):
            break
        page += 1


def fetch_job(job_id):
    status, response = consumer.http_json(
        "GET", f"{consumer.KR_BASE_URL}/api/art/queue/{job_id}"
    )
    if status != 200 or not response or not response.get("success"):
        raise RuntimeError(
            f"ArtJob {job_id} lookup returned HTTP {status}: "
            f"{response and response.get('message')}"
        )
    job = ((response.get("data") or {}).get("job"))
    if not isinstance(job, dict):
        raise RuntimeError(f"ArtJob {job_id} lookup returned no job payload.")
    return job


def choose_duplicate_keeper(first, second):
    """Keep the farther-progressed row; ties keep the first-created row."""
    first_rank = STATUS_RANK.get(str(first.get("status") or ""), 0)
    second_rank = STATUS_RANK.get(str(second.get("status") or ""), 0)
    return second if second_rank > first_rank else first


def cleanup_incident_duplicates(live):
    """Report the incident replacements and cancel only redundant queue rows."""
    primary = fetch_job(INCIDENT_STATUS_JOB_ID)
    print(
        f"Incident replacement ArtJob {INCIDENT_STATUS_JOB_ID}: "
        f"status={primary.get('status')}; engine={primary.get('engine')}"
    )

    failures = []
    for first_id, second_id in INCIDENT_DUPLICATE_PAIRS:
        first = fetch_job(first_id)
        second = fetch_job(second_id)
        keeper = choose_duplicate_keeper(first, second)
        duplicate = second if keeper is first else first
        keeper_id = int(keeper["id"])
        duplicate_id = int(duplicate["id"])
        duplicate_status = str(duplicate.get("status") or "")
        print(
            f"Incident duplicate pair {first_id}/{second_id}: "
            f"keep {keeper_id} ({keeper.get('status')}), "
            f"redundant {duplicate_id} ({duplicate_status})"
        )

        if duplicate_status == "CANCELLED":
            continue
        if duplicate_status == "DONE":
            print(
                f"  ArtJob {duplicate_id} already DONE; preserving history/image "
                "instead of destructively deleting output."
            )
            continue
        if not live:
            print(f"  DRY RUN: would cancel redundant ArtJob {duplicate_id}.")
            continue

        status, response = consumer.http_json(
            "POST",
            f"{consumer.KR_BASE_URL}/api/art/queue/{duplicate_id}/cancel",
            {
                "reason": (
                    f"Cancelled as duplicate of ArtJob {keeper_id}; concurrent "
                    "2026-08-12 failed-job repair workflows created both rows."
                )
            },
        )
        if status != 200 or not response or not response.get("success"):
            failures.append(duplicate_id)
            print(
                f"  FAILED cancelling duplicate ArtJob {duplicate_id}: HTTP {status} "
                f"{response and response.get('message')}",
                file=sys.stderr,
            )
        else:
            print(f"  Cancelled redundant ArtJob {duplicate_id}.")

    return failures


def repair_reasons(job):
    payload = job.get("payload") or {}
    if not isinstance(payload, dict):
        return []
    if str(payload.get("targetRepo") or "").strip() != KIND_ROBOTS_REPO:
        return []

    reasons = []
    image_path = str(payload.get("imagePath") or "").strip().replace("\\", "/")
    prompt = str(
        payload.get("promptString")
        or payload.get("artPrompt")
        or payload.get("prompt")
        or ""
    )

    if image_path and not image_path.lstrip("/").startswith("public/images/"):
        reasons.append(f"legacy imagePath {image_path}")
    if VAGUE_ART_DIRECTION.search(prompt):
        reasons.append("vague Kind Robots style token")
    return reasons


def failure_diagnostic(job):
    """Return a prompt-free, bounded diagnostic for an unhandled FAILED row."""
    job_id = job.get("id", "?")
    engine = str(job.get("engine") or "unknown").strip() or "unknown"
    error = " ".join(str(job.get("error") or "(no error text)").split())
    if len(error) > DIAGNOSTIC_ERROR_LIMIT:
        error = error[: DIAGNOSTIC_ERROR_LIMIT - 1] + "…"
    return f"ArtJob {job_id}: engine={engine}; error={error}"


def chunks(values, size):
    for index in range(0, len(values), size):
        yield values[index : index + size]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--live",
        action="store_true",
        help="apply reviewed repairs and cancel reviewed duplicate replacement rows",
    )
    args = parser.parse_args()

    if args.live and not consumer.KR_API_TOKEN:
        print("KR_API_TOKEN is required for --live.", file=sys.stderr)
        return 1

    try:
        incident_failures = cleanup_incident_duplicates(args.live)
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        return 1

    selected = []
    unhandled = []
    for job in failed_jobs():
        reasons = repair_reasons(job)
        if not reasons:
            unhandled.append(job)
            continue
        selected.append(int(job["id"]))
        print(f"  ArtJob {job['id']}: {', '.join(reasons)}")

    if unhandled:
        print(f"Unhandled FAILED ArtJobs ({len(unhandled)}):")
        for job in unhandled:
            print(f"  {failure_diagnostic(job)}")

    if not selected:
        print("No failed Kind Robots ArtJobs need path/style repair.")
        if incident_failures:
            print(f"Duplicate cleanup failures: {incident_failures}", file=sys.stderr)
            return 1
        return 0

    print(
        f"{'LIVE' if args.live else 'DRY RUN'}: "
        f"{len(selected)} failed ArtJob(s) selected for path/style repair"
    )
    if not args.live:
        print("Pass --live to repair and requeue these exact IDs.")
        return 0

    repaired = 0
    failures = []
    for batch in chunks(selected, REQUEUE_BATCH_SIZE):
        status, response = consumer.http_json(
            "POST",
            f"{consumer.KR_BASE_URL}/api/art/queue/reenqueue-failed",
            {"jobIds": batch},
            timeout=180,
        )
        if status != 200 or not response or not response.get("success"):
            failures.extend(batch)
            print(
                f"  FAILED batch {batch[0]}..{batch[-1]}: HTTP {status} "
                f"{response and response.get('message')}",
                file=sys.stderr,
            )
            continue

        data = response.get("data") or {}
        queued = data.get("requeuedJobIds") or []
        repaired += len(queued)
        failures.extend(data.get("failedSourceJobIds") or [])
        print(
            f"  repaired/requeued {len(queued)} job(s); "
            f"paths fixed {data.get('repairedImagePathCount', 0)}, "
            f"prompts fixed {data.get('repairedPromptCount', 0)}"
        )

    print(f"Repaired and requeued {repaired}/{len(selected)} selected ArtJobs.")
    failures.extend(incident_failures)
    if failures:
        print(f"Failed IDs: {sorted(set(failures))}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
