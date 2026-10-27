#!/usr/bin/env python3
"""Reconcile and enqueue exactly 20 Space Couch giant-casino Serendipity venue paintings.

Do not assume an accepted ArtJob has rendered or has been attached to the game.
A prior partial workflow run is reconciled against the entire remote project queue
by normalized prompt before it submits anything, preventing double billing.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from urllib.parse import urlencode

try:
    from scripts import enqueue_art_requests as enq
    from scripts import consume_art_queue_core as core
except ImportError:
    import enqueue_art_requests as enq
    import consume_art_queue_core as core

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "projects/game-of-captains/art/SERENDIPITY-CASINOS-20-ROUND-1.yaml"
PROJECT = "game-of-captains"
EXPECTED = 20
PREFIX = "space-couch-serendipity-"


def normalized(value):
    return " ".join(str(value or "").split())


def parse_ledger(path=LEDGER):
    header, data = enq.load_ledger(path)
    if data.get("auto_submit") is not False or data.get("project_slug") != PROJECT:
        raise ValueError("Unexpected casino ledger auto-submit or project")
    lanes = data.get("lanes") or []
    if len(lanes) != 1 or lanes[0].get("key") != "krea2" or lanes[0].get("engine") != "krea2":
        raise ValueError("Casino paintings require exactly one Krea 2 lane")
    cells = list(enq.iter_cells(data))
    if len(cells) != EXPECTED:
        raise ValueError(f"Expected {EXPECTED} venue subjects, found {len(cells)}")
    keys, assets, seeds = set(), set(), set()
    for subject, _ in cells:
        key = subject["key"]
        asset = subject["asset"]
        seed = subject["seed"]
        if key in keys or asset in assets or seed in seeds:
            raise ValueError(f"Duplicate casino subject/asset/seed: {key}")
        keys.add(key)
        assets.add(asset)
        seeds.add(seed)
        if not key.startswith(PREFIX) or not key.endswith("-environment"):
            raise ValueError(f"Invalid casino key {key}")
        if subject.get("size") != "1344x768" or subject.get("entity") != "living-casino-franchise":
            raise ValueError(f"Wrong casino painting dimensions/entity: {key}")
        if asset != "game-of-captains/venues/" + key[len(PREFIX):-len("-environment")]:
            raise ValueError(f"Asset path doesn't match stable key: {key}")
        prompt = enq.compose_prompt(lanes[0], subject).lower()
        if len(prompt) < 350 or not all(
            token in prompt
            for token in (
                "living cobalt blue alien",
                "casino",
                "serendipity",
                "inside the casino",
                "tardigrade",
                "scarlet velvet couch",
            )
        ):
            raise ValueError(f"Missing physical scene/location continuity: {key}")
    return header, data


def existing_jobs(fetch=None):
    fetch = fetch or core.http_json
    jobs = []
    for page in range(1, 1001):
        url = core.KR_BASE_URL.rstrip("/") + "/api/art/queue?" + urlencode(
            {"projectSlug": PROJECT, "pageSize": 200, "page": page}
        )
        status, response = fetch("GET", url)
        if status != 200 or not isinstance(response, dict) or response.get("success") is not True:
            raise RuntimeError(f"Incomplete authenticated project queue: page {page} HTTP {status}")
        data = response.get("data") or {}
        batch, pagination = data.get("jobs"), data.get("pagination")
        if not isinstance(batch, list) or not isinstance(pagination, dict):
            raise RuntimeError("Invalid remote job pagination")
        if any(not isinstance(job, dict) or job.get("projectSlug") != PROJECT for job in batch):
            raise RuntimeError("Remote response included unrelated project jobs")
        jobs.extend(batch)
        if not pagination.get("hasNextPage"):
            if pagination.get("totalCount") != len(jobs):
                raise RuntimeError("Partial remote art queue, refusing to duplicate jobs")
            return jobs
    raise RuntimeError("Remote art queue exceeded safe pagination limit")


def reconcile(data, jobs):
    by_prompt = {}
    for job in jobs:
        payload = job.get("payload") or {}
        prompt = normalized(payload.get("promptString")) if isinstance(payload, dict) else ""
        if prompt:
            by_prompt.setdefault(prompt, []).append(job)
    recovered = 0
    for subject in data["subjects"]:
        if (subject.get("jobs") or {}).get("krea2"):
            continue
        prompt = normalized(enq.compose_prompt(data["lanes"][0], subject))
        matches = by_prompt.get(prompt, [])
        ids = sorted(set(job["id"] for job in matches if type(job.get("id")) is int and job["id"] > 0))
        if matches and not ids:
            raise RuntimeError(f"Remote match without valid ArtJob ID: {subject['key']}")
        if ids:
            subject.setdefault("jobs", {})["krea2"] = ids[0]
            recovered += 1
            if len(ids) > 1:
                print(f"WARNING existing duplicate jobs for {subject['key']}: {ids}")
    return recovered


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--status", action="store_true")
    args = parser.parse_args(argv)
    header, data = parse_ledger()
    accepted = sum(bool((s.get("jobs") or {}).get("krea2")) for s in data["subjects"])
    print(f"Space Couch Serendipity artwork: {accepted}/{EXPECTED} recorded ArtJob IDs.")
    if not args.live and not args.status:
        return 0
    if not core.KR_API_TOKEN:
        print("KR_API_TOKEN absent: cannot submit/inspect live venue jobs.", file=sys.stderr)
        return 2
    if args.status:
        return enq.main([str(LEDGER), "--status"])
    try:
        jobs = existing_jobs()
        recovered = reconcile(data, jobs)
        if recovered:
            enq.save_ledger(LEDGER, header, data)
        print(f"Checked {len(jobs)} remote project jobs and recovered {recovered} IDs.")
        code = enq.main([str(LEDGER), "--live"])
        recorded = enq.load_ledger(LEDGER)[1]
        accepted = sum(bool((s.get("jobs") or {}).get("krea2")) for s in recorded["subjects"])
        print(f"Space Couch Serendipity: {accepted}/{EXPECTED} accepted ArtJob IDs.")
        return code if accepted == EXPECTED else 1
    except Exception as exc:
        print(f"Casino ArtJob submission refused safely: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
