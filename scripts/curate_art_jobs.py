#!/usr/bin/env python3
"""Curate finished Kind Robots ArtJobs and learn from Silas's saved feedback.

This is the bridge between Conductor's aesthetic assessor and the ArtJob trainer
panel in kind_robots. It fetches recent DONE jobs, skips jobs already carrying a
CURATOR result, scores the remaining images, and writes the verdict back to the
same ArtJob through /api/art/queue/<id>/feedback.

Recent HUMAN verdicts are included as labeled visual examples on every scoring
request. The human examples are the strongest signal: they refine the general
AESTHETIC-GUIDELINES.md rubric without rewriting that file after every click.

Environment:
  KR_API_TOKEN       machine/admin token for kind_robots
  KR_BASE_URL        default https://kind-robots.vercel.app
  ANTHROPIC_API_KEY  required unless --dry-run
  ART_CURATOR_MODEL  inherited from scripts/curate_art.py

Usage:
  python scripts/curate_art_jobs.py --limit 12
  python scripts/curate_art_jobs.py --dry-run --limit 12
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any

from curate_art import API_URL, DAILY_VERDICT_SCHEMA, MODEL, daily_rubric

KR_BASE_URL = os.environ.get(
    "KR_BASE_URL", "https://kind-robots.vercel.app"
).rstrip("/")
KR_API_TOKEN = os.environ.get("KR_API_TOKEN", "").strip()
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "").strip()

MAX_EXAMPLES_PER_VERDICT = 2


def request_json(
    method: str,
    url: str,
    body: dict[str, Any] | None = None,
    *,
    token: str | None = None,
    timeout: int = 180,
) -> tuple[int, dict[str, Any] | None]:
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(url, data=data, method=method)
    request.add_header("Content-Type", "application/json")
    if token:
        request.add_header("Authorization", f"Bearer {token}")

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode() or "null")
            return response.status, payload
    except urllib.error.HTTPError as error:
        try:
            payload = json.loads(error.read().decode() or "null")
        except (ValueError, OSError):
            payload = None
        return error.code, payload


def payload_record(job: dict[str, Any]) -> dict[str, Any]:
    payload = job.get("payload")
    return payload if isinstance(payload, dict) else {}


def curation_record(job: dict[str, Any]) -> dict[str, Any]:
    curation = payload_record(job).get("curation")
    return curation if isinstance(curation, dict) else {}


def feedback_record(job: dict[str, Any], key: str) -> dict[str, Any] | None:
    feedback = curation_record(job).get(key)
    return feedback if isinstance(feedback, dict) else None


def job_prompt(job: dict[str, Any]) -> str:
    payload = payload_record(job)
    for key in ("promptString", "artPrompt", "prompt"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return " ".join(value.split())
    return ""


def fetch_jobs() -> list[dict[str, Any]]:
    status, response = request_json(
        "GET",
        f"{KR_BASE_URL}/api/art/queue?status=DONE&limit=200",
        token=KR_API_TOKEN,
    )
    if status != 200 or not response or not response.get("success"):
        message = response.get("message") if response else "no response body"
        raise RuntimeError(f"ArtJob fetch failed: HTTP {status}: {message}")
    jobs = (response.get("data") or {}).get("jobs") or []
    return [job for job in jobs if isinstance(job, dict)]


def fetch_image_source(art_image_id: int) -> dict[str, str]:
    status, response = request_json(
        "GET",
        f"{KR_BASE_URL}/api/art/image/{art_image_id}?includeImageData=true",
        token=KR_API_TOKEN,
    )
    if status != 200 or not response or not response.get("success"):
        message = response.get("message") if response else "no response body"
        raise RuntimeError(
            f"ArtImage {art_image_id} fetch failed: HTTP {status}: {message}"
        )

    image = response.get("data") or {}
    raw = str(image.get("imageData") or "").strip()
    if not raw:
        raise RuntimeError(f"ArtImage {art_image_id} has no imageData")

    file_type = str(image.get("fileType") or "png").lower()
    media_type = f"image/{'jpeg' if file_type in ('jpg', 'jpeg') else file_type}"

    if raw.startswith("data:image/"):
        header, encoded = raw.split(",", 1)
        media_type = header.split(";", 1)[0].removeprefix("data:")
        raw = encoded

    return {"type": "base64", "media_type": media_type, "data": raw}


def select_human_examples(jobs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    buckets: dict[str, list[dict[str, Any]]] = {
        "PROMOTE": [],
        "REVISE": [],
        "REJECT": [],
    }

    for job in jobs:
        human = feedback_record(job, "human")
        if not human:
            continue
        verdict = str(human.get("verdict") or "").upper()
        if verdict not in buckets:
            continue
        if len(buckets[verdict]) >= MAX_EXAMPLES_PER_VERDICT:
            continue
        if not isinstance(job.get("artImageId"), int):
            continue
        buckets[verdict].append(job)

    return buckets["PROMOTE"] + buckets["REVISE"] + buckets["REJECT"]


def human_example_content(job: dict[str, Any]) -> list[dict[str, Any]]:
    human = feedback_record(job, "human") or {}
    verdict = str(human.get("verdict") or "UNKNOWN")
    summary = str(human.get("summary") or "").strip()
    tags = human.get("tags") if isinstance(human.get("tags"), list) else []
    prompt = job_prompt(job)
    art_image_id = int(job["artImageId"])

    label = (
        f"HUMAN {verdict} example from Silas. "
        f"Prompt: {prompt or '(prompt unavailable)'}. "
        f"Feedback: {summary or '(no free-text note)'}. "
        f"Tags: {', '.join(str(tag) for tag in tags) or '(none)'}."
    )
    return [
        {"type": "text", "text": label},
        {"type": "image", "source": fetch_image_source(art_image_id)},
    ]


def call_curator(
    job: dict[str, Any], examples: list[dict[str, Any]]
) -> dict[str, Any]:
    content: list[dict[str, Any]] = [
        {
            "type": "text",
            "text": (
                "The following images were labeled directly by Silas. Treat these "
                "human verdicts and notes as stronger evidence than generic taste. "
                "Infer what to reward and avoid, then judge the final candidate."
            ),
        }
    ]

    for example in examples:
        content.extend(human_example_content(example))

    prompt = job_prompt(job)
    project = str(job.get("projectSlug") or "unscoped")
    content.extend(
        [
            {
                "type": "text",
                "text": (
                    f"CANDIDATE ArtJob #{job.get('id')} for project {project}. "
                    f"Intended prompt: {prompt or '(prompt unavailable)'}"
                ),
            },
            {
                "type": "image",
                "source": fetch_image_source(int(job["artImageId"])),
            },
            {
                "type": "text",
                "text": (
                    daily_rubric()
                    + "\n\nThe human-labeled examples above override conflicts in the "
                    "general rubric. Judge prompt fit as well as visual craft."
                ),
            },
        ]
    )

    body = {
        "model": MODEL,
        "max_tokens": 2048,
        "thinking": {"type": "adaptive"},
        "output_config": {
            "effort": "medium",
            "format": {"type": "json_schema", "schema": DAILY_VERDICT_SCHEMA},
        },
        "messages": [{"role": "user", "content": content}],
    }

    status, response = request_json(
        "POST",
        API_URL,
        body,
        token=None,
        timeout=240,
    )
    if status != 200 or not response:
        message = response.get("error") if response else "no response body"
        raise RuntimeError(f"Anthropic curator failed: HTTP {status}: {message}")

    text = next(
        (
            block.get("text", "")
            for block in response.get("content", [])
            if block.get("type") == "text"
        ),
        "",
    )
    return json.loads(text)


def anthropic_request_json(
    job: dict[str, Any], examples: list[dict[str, Any]]
) -> dict[str, Any]:
    content: list[dict[str, Any]] = [
        {
            "type": "text",
            "text": (
                "The following images were labeled directly by Silas. Treat these "
                "human verdicts and notes as stronger evidence than generic taste. "
                "Infer what to reward and avoid, then judge the final candidate."
            ),
        }
    ]

    for example in examples:
        content.extend(human_example_content(example))

    prompt = job_prompt(job)
    project = str(job.get("projectSlug") or "unscoped")
    content.extend(
        [
            {
                "type": "text",
                "text": (
                    f"CANDIDATE ArtJob #{job.get('id')} for project {project}. "
                    f"Intended prompt: {prompt or '(prompt unavailable)'}"
                ),
            },
            {
                "type": "image",
                "source": fetch_image_source(int(job["artImageId"])),
            },
            {
                "type": "text",
                "text": (
                    daily_rubric()
                    + "\n\nThe human-labeled examples above override conflicts in the "
                    "general rubric. Judge prompt fit as well as visual craft."
                ),
            },
        ]
    )

    body = json.dumps(
        {
            "model": MODEL,
            "max_tokens": 2048,
            "thinking": {"type": "adaptive"},
            "output_config": {
                "effort": "medium",
                "format": {
                    "type": "json_schema",
                    "schema": DAILY_VERDICT_SCHEMA,
                },
            },
            "messages": [{"role": "user", "content": content}],
        }
    ).encode()

    request = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=240) as response:
        payload = json.loads(response.read())

    text = next(
        (
            block.get("text", "")
            for block in payload.get("content", [])
            if block.get("type") == "text"
        ),
        "",
    )
    return json.loads(text)


def save_curator_feedback(job_id: int, verdict: dict[str, Any]) -> None:
    score = int(verdict.get("score") or 0)
    raw_verdict = str(verdict.get("verdict") or "reject").upper()
    if raw_verdict not in {"PROMOTE", "REVISE", "REJECT"}:
        raw_verdict = "REJECT"

    body = {
        "source": "CURATOR",
        "verdict": raw_verdict,
        "score": score,
        "summary": str(verdict.get("one_liner") or "").strip() or None,
        "reasons": verdict.get("reasons") or [],
        "tags": [],
        "rubricKey": "aesthetic-guidelines+human-feedback-v1",
    }
    status, response = request_json(
        "POST",
        f"{KR_BASE_URL}/api/art/queue/{job_id}/feedback",
        body,
        token=KR_API_TOKEN,
    )
    if status != 200 or not response or not response.get("success"):
        message = response.get("message") if response else "no response body"
        raise RuntimeError(
            f"feedback save failed for ArtJob {job_id}: HTTP {status}: {message}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=12)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not KR_API_TOKEN:
        print("KR_API_TOKEN is required.", file=sys.stderr)
        return 1

    jobs = fetch_jobs()
    examples = select_human_examples(jobs)
    candidates = [
        job
        for job in jobs
        if isinstance(job.get("artImageId"), int)
        and feedback_record(job, "curator") is None
    ][: max(args.limit, 0)]

    print(
        f"ArtJob curator: {len(candidates)} candidate(s), "
        f"{len(examples)} human example(s)."
    )

    if not candidates:
        return 0

    if args.dry_run:
        for job in candidates:
            print(
                f"  would curate #{job.get('id')} "
                f"[{job.get('projectSlug') or 'unscoped'}] "
                f"{job_prompt(job)[:80]}"
            )
        return 0

    if not ANTHROPIC_API_KEY:
        print("ANTHROPIC_API_KEY is required unless --dry-run.", file=sys.stderr)
        return 1

    failures = 0
    for job in candidates:
        job_id = int(job["id"])
        try:
            verdict = anthropic_request_json(job, examples)
            save_curator_feedback(job_id, verdict)
            print(
                f"  {str(verdict.get('verdict') or '').upper():8} "
                f"#{job_id} score={verdict.get('score')} "
                f"{verdict.get('one_liner') or ''}"
            )
        except Exception as error:  # noqa: BLE001 - keep curating the batch
            failures += 1
            print(f"  ERROR    #{job_id}: {error}", file=sys.stderr)

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
