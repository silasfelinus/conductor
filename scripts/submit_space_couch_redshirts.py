#!/usr/bin/env python3
"""Safely enqueue the 200 original Space Couch redshirt illustrations.

Exactly one submission owner. Compare each composed prompt with ALL currently
recorded game-of-captains ArtJobs before sending any missing cells. If the
previous workflow was interrupted between POST and git push, recover that
job instead of creating a duplicate.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from urllib.parse import urlencode

import yaml

try:
    from scripts import enqueue_art_requests as enq
    from scripts import consume_art_queue_core as core
except ImportError:
    import enqueue_art_requests as enq
    import consume_art_queue_core as core

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "projects/game-of-captains/art/REDSHIRTS-200-ROUND-1.yaml"
PROJECT = "game-of-captains"
EXPECTED = 200
PREFIX = "space-couch-redshirt-"


def normalize(value):
    return " ".join(str(value or "").split())


def parse_ledger(path=LEDGER):
    header, data = enq.load_ledger(path)
    if data.get("auto_submit") is not False:
        raise ValueError("Dedicated redshirt submitter requires auto_submit:false")
    if data.get("project_slug") != PROJECT:
        raise ValueError("Unexpected art project")
    lanes = data.get("lanes") or []
    if len(lanes) != 1 or lanes[0].get("key") != "krea2" or lanes[0].get("engine") != "krea2":
        raise ValueError("Redshirt art must use exactly one Krea2 lane")
    cells = list(enq.iter_cells(data))
    if len(cells) != EXPECTED:
        raise ValueError(f"Expected {EXPECTED} exact redshirt cells; got {len(cells)}")
    keys = [s["key"] for s, _ in cells]
    paths = [s["asset"] for s, _ in cells]
    seeds = [s["seed"] for s, _ in cells]
    if len(set(keys)) != EXPECTED or len(set(paths)) != EXPECTED or len(set(seeds)) != EXPECTED:
        raise ValueError("Duplicate redshirt subject key, asset path, or seed")
    for number in range(1, 101):
        target = f"rs-{number:03d}"
        for variant, size in (("portrait", "1024x1024"), ("secret-power", "1344x768")):
            key = f"{PREFIX}{target}-{variant}"
            subjects = [s for s, _ in cells if s["key"] == key]
            if len(subjects) != 1 or subjects[0]["size"] != size:
                raise ValueError(f"Missing or incorrect {key}")
            prompt = enq.compose_prompt(lanes[0], subjects[0])
            if "crimson" not in prompt.lower() or "uniform" not in prompt.lower():
                raise ValueError(f"Missing required bright-red uniform: {key}")
            if len(prompt) < 280:
                raise ValueError(f"Weak prompt: {key}")
    return header, data


def fetch_existing_jobs(fetch=None):
    """Fail closed when pagination or authentication is incomplete."""
    fetch = fetch or core.http_json
    jobs = []
    for page in range(1, 1001):
        url = core.KR_BASE_URL.rstrip("/") + "/api/art/queue?" + urlencode({
            "projectSlug": PROJECT, "pageSize": 200, "page": page
        })
        status, response = fetch("GET", url)
        if status != 200 or not isinstance(response, dict) or response.get("success") is not True:
            raise RuntimeError(f"ArtJob queue unavailable at page {page}: HTTP {status}")
        data = response.get("data") or {}
        batch = data.get("jobs")
        pagination = data.get("pagination")
        if not isinstance(batch, list) or not isinstance(pagination, dict):
            raise RuntimeError("ArtJob response omitted job pagination")
        if any(not isinstance(item, dict) or item.get("projectSlug") != PROJECT for item in batch):
            raise RuntimeError("Job response contains unrelated project")
        jobs.extend(batch)
        if not pagination.get("hasNextPage"):
            if len(jobs) != pagination.get("totalCount"):
                raise RuntimeError("Partial ArtJob project queue, refusing to post duplicates")
            return jobs
    raise RuntimeError("Exceeded pagination safety limit")


def reconcile(data, existing):
    """Keep the oldest proven job for a matching exact prompt."""
    by_prompt = {}
    for job in existing:
        payload = job.get("payload") or {}
        if not isinstance(payload, dict):
            continue
        prompt = normalize(payload.get("promptString"))
        if prompt:
            by_prompt.setdefault(prompt, []).append(job)
    recovered = 0
    for subject in data["subjects"]:
        if (subject.get("jobs") or {}).get("krea2"):
            continue
        prompt = normalize(enq.compose_prompt(data["lanes"][0], subject))
        matches = by_prompt.get(prompt, [])
        if not matches:
            continue
        ids = sorted({job["id"] for job in matches if type(job.get("id")) is int and job["id"] > 0})
        if not ids:
            raise RuntimeError(f"Matching job lacks a positive ID: {subject['key']}")
        subject.setdefault("jobs", {})["krea2"] = ids[0]
        if len(ids) > 1:
            print(f"WARNING: pre-existing duplicate job requests for {subject['key']}: {ids}")
        recovered += 1
    return recovered


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="Reconcile full remote queue and submit missing jobs")
    parser.add_argument("--status", action="store_true", help="Refresh statuses only")
    args = parser.parse_args(argv)
    header, data = parse_ledger()
    accepted = sum(bool((s.get("jobs") or {}).get("krea2")) for s in data["subjects"])
    print(f"Redshirt art: {accepted}/{EXPECTED} ArtJob IDs present in committed ledger.")
    if not args.live and not args.status:
        return 0
    if not core.KR_API_TOKEN:
        print("KR_API_TOKEN is unavailable, cannot submit or verify live jobs", file=sys.stderr)
        return 2
    if args.status:
        return enq.main([str(LEDGER), "--status"])
    try:
        existing = fetch_existing_jobs()
        recovered = reconcile(data, existing)
        if recovered:
            enq.save_ledger(LEDGER, header, data)
        print(f"Verified {len(existing)} existing project jobs and recovered {recovered} IDs.")
        code = enq.main([str(LEDGER), "--live"])
        recorded = enq.load_ledger(LEDGER)[1]
        accepted = sum(bool((s.get("jobs") or {}).get("krea2")) for s in recorded["subjects"])
        print(f"Redshirt art submission: {accepted}/{EXPECTED} accepted ArtJob IDs.")
        if accepted != EXPECTED:
            print(f"Missing {EXPECTED-accepted} ArtJob IDs after submission.", file=sys.stderr)
            return 1
        return code
    except Exception as exc:
        print(f"ArtJob submission refused safely: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
