#!/usr/bin/env python3
"""Repair and requeue failed Kind Robots ArtJobs with reviewed repair policies.

The script lists FAILED jobs through the authenticated queue API and applies two
strictly scoped repair lanes:

1. one-time incident migrations for exact, reviewed ArtJob ids; and
2. the standing Kind Robots path/style normalization policy.

Everything else is reported with a bounded prompt-free diagnostic. Dry-run by
default. The exact-id incident lane is intentionally temporary and fail-closed:
it verifies the expected engine/error signature before making any request.
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

# 2026-08-12 incident cleanup. These are immutable source-row ids already
# reviewed from the authenticated production queue. The single-job retry API
# creates a replacement first and only then marks the FAILED source superseded.
# Keeping the ids exact makes this a one-shot migration rather than a policy to
# retry arbitrary future failures.
INCIDENT_RETRIES = {
    8116: {
        "engine": "A1111",
        "error_contains": "WinError 10061",
        "body": {"mode": "NEW_OUTPUT", "preset": "krea2", "refreshSeed": True},
        "reason": "obsolete site A1111 job; rebuild replacement on Krea2/Comfy",
    },
    7622: {
        "engine": "COMFY",
        "error_contains": "Kontext/SFW/acrylic.safetensors",
        "body": {"mode": "NEW_OUTPUT", "refreshSeed": False},
        "reason": "Kontext LoRA verification retry with current Resource refresh",
    },
    7623: {
        "engine": "COMFY",
        "error_contains": "Flux/SFW/3D_Cartoon_Vision_flux_v1.safetensors",
        "body": {"mode": "NEW_OUTPUT", "refreshSeed": False},
        "reason": "Kontext LoRA verification retry with current Resource refresh",
    },
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


def incident_retry_plan(job):
    """Return the reviewed exact-id retry plan, failing closed on drift."""
    try:
        job_id = int(job.get("id"))
    except (TypeError, ValueError):
        return None
    plan = INCIDENT_RETRIES.get(job_id)
    if not plan:
        return None

    engine = str(job.get("engine") or "").strip()
    error = str(job.get("error") or "")
    if engine != plan["engine"] or plan["error_contains"] not in error:
        raise RuntimeError(
            f"ArtJob {job_id} no longer matches its reviewed incident signature; "
            "refusing automatic retry."
        )
    return plan


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


def retry_incident_jobs(incident_jobs, live):
    if not incident_jobs:
        return [], []

    print(f"Reviewed incident ArtJobs ({len(incident_jobs)}):")
    for job, plan in incident_jobs:
        print(f"  ArtJob {job['id']}: {plan['reason']}")

    if not live:
        print("DRY RUN: incident replacements not created.")
        return [], []

    replacements = []
    failures = []
    for job, plan in incident_jobs:
        job_id = int(job["id"])
        status, response = consumer.http_json(
            "POST",
            f"{consumer.KR_BASE_URL}/api/art/queue/{job_id}/reenqueue",
            plan["body"],
            timeout=180,
        )
        if status != 201 or not response or not response.get("success"):
            failures.append(job_id)
            print(
                f"  FAILED ArtJob {job_id}: HTTP {status} "
                f"{response and response.get('message')}",
                file=sys.stderr,
            )
            continue

        replacement = ((response.get("data") or {}).get("job") or {}).get("id")
        replacements.append((job_id, replacement))
        print(f"  ArtJob {job_id} -> replacement ArtJob {replacement}")

    return replacements, failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--live",
        action="store_true",
        help="apply the reviewed repairs and requeue selected failed jobs",
    )
    args = parser.parse_args()

    if args.live and not consumer.KR_API_TOKEN:
        print("KR_API_TOKEN is required for --live.", file=sys.stderr)
        return 1

    jobs = list(failed_jobs())
    incident_jobs = []
    selected = []
    unhandled = []

    try:
        for job in jobs:
            plan = incident_retry_plan(job)
            if plan:
                incident_jobs.append((job, plan))
                continue

            reasons = repair_reasons(job)
            if not reasons:
                unhandled.append(job)
                continue
            selected.append(int(job["id"]))
            print(f"  ArtJob {job['id']}: {', '.join(reasons)}")
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        return 1

    replacements, incident_failures = retry_incident_jobs(incident_jobs, args.live)

    if unhandled:
        print(f"Unhandled FAILED ArtJobs ({len(unhandled)}):")
        for job in unhandled:
            print(f"  {failure_diagnostic(job)}")

    if not selected:
        print("No failed Kind Robots ArtJobs need path/style repair.")
        if incident_failures:
            print(f"Incident retry failures: {incident_failures}", file=sys.stderr)
            return 1
        if replacements:
            print(f"Created {len(replacements)} reviewed incident replacement(s).")
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
