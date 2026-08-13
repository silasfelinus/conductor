#!/usr/bin/env python3
"""Repair and requeue failed Kind Robots ArtJobs with legacy paths/prompts.

The script first lists FAILED jobs through the authenticated queue API, selects
only Kind Robots-targeted jobs whose imagePath is not canonical or whose prompt
contains the retired brand-style token, then sends those exact IDs to the
scoped requeue endpoint. Dry-run by default.

Failures outside that deliberately narrow repair policy are reported with a
bounded diagnostic (id, engine, and error only). This keeps scheduled repair
runs useful for incident diagnosis without dumping prompts or silently implying
that an unselected failure was not seen.
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
        help="repair payloads and requeue the selected failed jobs",
    )
    args = parser.parse_args()

    if args.live and not consumer.KR_API_TOKEN:
        print("KR_API_TOKEN is required for --live.", file=sys.stderr)
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
        return 0

    print(
        f"{'LIVE' if args.live else 'DRY RUN'}: "
        f"{len(selected)} failed ArtJob(s) selected"
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
    if failures:
        print(f"Failed IDs: {sorted(set(failures))}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
