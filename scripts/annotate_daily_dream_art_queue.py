#!/usr/bin/env python3
"""Annotate Daily Dream digest assets with the real pre-render queue state.

``enrich_daily_dream_digest.py`` knows whether the object builder emitted an art
request, but the durable request first lands in Conductor's ``art-prompts.yaml``
staging ledger. Only later does that request become a Kind Robots ArtJob. Calling
both states "queued" hid a scheduling boundary and made a staged request look as
though the renderer was already working on it.

This read-only post-processor joins digest assets to the staging ledger by stable
request id. When ``KR_API_TOKEN`` is available it also reads each recorded ArtJob
from Kind Robots so a completed render cannot be mislabeled from stale staging
metadata. It never changes the art queue.
"""

from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from pathlib import Path
from typing import Any, Callable

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QUEUE = ROOT / "projects" / "art-prompts.yaml"


def _live_job_fetcher() -> Callable[[int], dict[str, Any] | None] | None:
    """Return the canonical ArtJob reader when this run has Kind Robots auth."""
    if not os.environ.get("KR_API_TOKEN"):
        return None
    try:
        from scripts import consume_art_requests as requests  # noqa: PLC0415
    except ImportError:
        try:
            import consume_art_requests as requests  # noqa: PLC0415
        except ImportError:
            return None
    return requests.fetch_job


def load_request_states(path: Path = DEFAULT_QUEUE) -> dict[str, dict[str, Any]]:
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    requests = data.get("requests") if isinstance(data, dict) else []
    if not isinstance(requests, list):
        return {}
    return {
        str(row.get("id")): row
        for row in requests
        if isinstance(row, dict) and row.get("id")
    }


def annotate_asset(
    asset: dict[str, Any],
    request_states: dict[str, dict[str, Any]],
    *,
    fetch_job: Callable[[int], dict[str, Any] | None] | None = None,
) -> dict[str, Any]:
    annotated = dict(asset)

    if annotated.get("image_url") or annotated.get("art_status") == "ready":
        return annotated

    request_id = str(annotated.get("request_id") or "").strip()
    if not request_id:
        return annotated

    request = request_states.get(request_id)
    if request is None:
        if annotated.get("art_status") == "queued":
            annotated["art_status"] = "queue metadata missing"
        return annotated

    request_status = str(request.get("status") or "pending").strip().lower()
    raw_job_id = request.get("last_art_job_id")
    try:
        job_id = int(raw_job_id) if raw_job_id is not None else None
    except (TypeError, ValueError):
        job_id = None
    if job_id is not None and job_id > 0:
        annotated["art_job_id"] = job_id

    # The staging row deliberately remains pending until its public media path
    # is delivered. That lifecycle is not the ArtJob lifecycle. Ask Kind Robots
    # for the live job before interpreting "pending + last_art_job_id" as queued.
    if job_id is not None and job_id > 0 and fetch_job is not None:
        try:
            live_job = fetch_job(job_id)
        except Exception:  # noqa: BLE001 - digest status must degrade safely
            live_job = None
        if isinstance(live_job, dict):
            live_status = str(live_job.get("status") or "").strip().upper()
            status_labels = {
                "DONE": "rendered, awaiting public image",
                "RUNNING": "rendering",
                "PENDING": "queued",
                "FAILED": "failed",
                "CANCELLED": "cancelled",
            }
            if live_status in status_labels:
                annotated["art_status"] = status_labels[live_status]
                raw_image_id = live_job.get("artImageId")
                try:
                    image_id = int(raw_image_id) if raw_image_id is not None else None
                except (TypeError, ValueError):
                    image_id = None
                if image_id is not None and image_id > 0:
                    annotated["art_image_id"] = image_id
                return annotated

    if request_status in {"done", "complete", "completed"}:
        annotated["art_status"] = "rendered, awaiting attachment"
    elif job_id is not None and job_id > 0:
        annotated["art_status"] = "queued"
    elif request_status == "pending":
        annotated["art_status"] = "awaiting ArtJob"
    else:
        annotated["art_status"] = f"request {request_status}"

    return annotated


def annotate_proposal(
    proposal: Any,
    request_states: dict[str, dict[str, Any]],
    *,
    fetch_job: Callable[[int], dict[str, Any] | None] | None = None,
) -> Any:
    if not isinstance(proposal, dict):
        return proposal
    output = dict(proposal)
    assets = proposal.get("assets")
    if isinstance(assets, list):
        output["assets"] = [
            annotate_asset(asset, request_states, fetch_job=fetch_job)
            if isinstance(asset, dict)
            else asset
            for asset in assets
        ]
    return output


def annotate_digest(
    digest: dict[str, Any],
    request_states: dict[str, dict[str, Any]],
    *,
    fetch_job: Callable[[int], dict[str, Any] | None] | None = None,
) -> dict[str, Any]:
    output = dict(digest)
    for key in ("current_dream_output", "previous_dream_output"):
        output[key] = annotate_proposal(
            output.get(key), request_states, fetch_job=fetch_job
        )

    recent = output.get("recent_dream_outputs")
    if isinstance(recent, list):
        output["recent_dream_outputs"] = [
            annotate_proposal(proposal, request_states, fetch_job=fetch_job)
            for proposal in recent
        ]
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", default="digest.json")
    parser.add_argument("--queue", default=str(DEFAULT_QUEUE))
    parser.add_argument("--output")
    args = parser.parse_args(argv)

    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else input_path
    digest = json.loads(input_path.read_text(encoding="utf-8"))
    annotated = annotate_digest(
        digest,
        load_request_states(Path(args.queue)),
        fetch_job=_live_job_fetcher(),
    )
    output_path.write_text(
        json.dumps(annotated, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    statuses = Counter(
        str(asset.get("art_status") or "unknown")
        for section in (
            annotated.get("previous_dream_output"),
            annotated.get("current_dream_output"),
        )
        if isinstance(section, dict)
        for asset in section.get("assets", [])
        if isinstance(asset, dict)
    )
    summary = ", ".join(f"{status}={count}" for status, count in sorted(statuses.items()))
    print(f"Annotated Daily Dream art queue state: {summary or 'no assets'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
