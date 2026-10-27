#!/usr/bin/env python3
"""Reconcile and submit only Prom of Doom's 144 personal outcome art requests.

The ledger has no ArtJob IDs, but an earlier cancelled workflow could have
POSTed jobs before committing them. Read the existing project's entire queue
FIRST and recover exact prompt matches before submitting missing cells.

Usage:
  python scripts/submit_prom_personal_outcomes.py              # offline ledger audit
  python scripts/submit_prom_personal_outcomes.py --live       # reconcile + submit
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from urllib.parse import urlencode

import yaml

try:
    from scripts import consume_art_queue_core as core
    from scripts import enqueue_art_requests as enq
except ImportError:
    import consume_art_queue_core as core
    import enqueue_art_requests as enq

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "projects/comet-city-academy/art/PERSONAL-CONSEQUENCES-ROUND-1.yaml"
EXPECTED = 144
PROJECT = "comet-city-academy"


def normalize(text: str) -> str:
    return " ".join(str(text or "").split())


def parse_ledger(path: Path = LEDGER):
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("auto_submit") is not True:
        raise ValueError("Refusing to submit non-opted-in art ledger")
    subjects = data.get("subjects")
    if not isinstance(subjects, list) or len(subjects) != EXPECTED:
        raise ValueError("Expected exactly 144 personal outcomes, not another art round")
    keys = [s.get("key") for s in subjects]
    seeds = [s.get("seed") for s in subjects]
    assets = [s.get("asset") for s in subjects]
    if len(set(keys)) != EXPECTED or len(set(seeds)) != EXPECTED or len(set(assets)) != EXPECTED:
        raise ValueError("Art request keys, seeds and assets must be unique")
    if any(not str(s).startswith("pod-personal-") for s in keys):
        raise ValueError("Refusing non-personal-quest request")
    lanes = data.get("lanes")
    if not isinstance(lanes, list) or len(lanes) != 1 or lanes[0].get("key") != "krea2":
        raise ValueError("Expected one krea2 lane")
    if any(s.get("lane") != "krea2" for s in subjects):
        raise ValueError("Unexpected art lane")
    return data


def fetch_existing_jobs(fetch=None):
    """Fail closed if any API page is inaccessible or incomplete."""
    fetch = fetch or core.http_json
    jobs, page = [], 1
    while True:
        query = urlencode({"projectSlug": PROJECT, "pageSize": 200, "page": page})
        url = f"{core.KR_BASE_URL}/api/art/queue?{query}"
        status, response = fetch("GET", url)
        if status != 200 or not isinstance(response, dict) or response.get("success") is not True:
            raise RuntimeError(f"ArtJob listing failed on page {page}: HTTP {status}")
        data = response.get("data") or {}
        batch, pagination = data.get("jobs"), data.get("pagination")
        if not isinstance(batch, list) or not isinstance(pagination, dict):
            raise RuntimeError("ArtJob response lacks jobs or pagination")
        if any(not isinstance(job, dict) or job.get("projectSlug") != PROJECT for job in batch):
            raise RuntimeError("ArtJob API leaked an unrelated project into a scoped listing")
        jobs.extend(batch)
        if not pagination.get("hasNextPage"):
            count = pagination.get("totalCount")
            if len(jobs) != count:
                raise RuntimeError(f"Incomplete ArtJob pages: {len(jobs)} of {count}")
            return jobs
        page += 1
        if page > 1000:
            raise RuntimeError("ArtJob listing pagination exceeded safety bound")


def recover_submitted(data, jobs):
    """Record previously accepted ArtJob IDs without sending a single POST."""
    by_prompt = {}
    for job in jobs:
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
        ids = sorted({job.get("id") for job in matches if isinstance(job.get("id"), int) and job["id"] > 0})
        if not ids:
            raise RuntimeError("Existing matching ArtJobs lack positive IDs")
        # A prior duplicate may exist. Recover the earliest accepted job, never add another.
        subject.setdefault("jobs", {})["krea2"] = ids[0]
        if len(ids) > 1:
            print(f"  duplicate already on server for {subject['key']}: {len(ids)} matches; reused {ids[0]}")
        recovered += 1
    return recovered


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args(argv)
    data = parse_ledger()
    submitted = sum(bool((s.get("jobs") or {}).get("krea2")) for s in data["subjects"])
    if not args.live:
        print(f"Personal outcomes: {EXPECTED} requests, {submitted} recorded ArtJob IDs, {EXPECTED - submitted} unrecorded")
        return 0
    if not core.KR_API_TOKEN:
        print("KR_API_TOKEN not configured; refusing submission without live reconciliation", file=sys.stderr)
        return 2
    try:
        jobs = fetch_existing_jobs()
        recovered = recover_submitted(data, jobs)
        if recovered:
            header = enq.split_header(LEDGER.read_text(encoding="utf-8"))[0]
            enq.save_ledger(LEDGER, header, data)
        print(f"Reconciled {len(jobs)} existing project jobs; recovered {recovered} personal outcomes.")
        # Existing enqueue script checks the prompt contract and persists each ID
        # immediately after a successful POST, preserving partial successes.
        result = enq.main([str(LEDGER), "--live"])
        updated = parse_ledger()
        recorded = sum(bool((s.get("jobs") or {}).get("krea2")) for s in updated["subjects"])
        print(f"ArtJob IDs recorded: {recorded}/{EXPECTED}.")
        if result != 0 or recorded != EXPECTED:
            return 1
        # Status is best-effort; job IDs are already preserved.
        try:
            enq.main([str(LEDGER), "--status"])
        except Exception as exc:
            print(f"Status refresh failed; accepted IDs retained: {type(exc).__name__}", file=sys.stderr)
        return 0
    except Exception as exc:
        print(f"Targeted art reconciliation/submission failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
