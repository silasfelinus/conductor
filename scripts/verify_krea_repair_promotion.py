#!/usr/bin/env python3
"""Verify Krea semantic-repair replacement jobs promoted their entity art.

dream-cycle/t-006, 2026-09-05. The Krea semantic art repair (kind_robots
`.github/workflows/krea-semantic-art-repair.yml`, write mode) enqueued
NEW_OUTPUT replacement ArtJobs for every entity-art Krea job whose positive
conditioning carried contextual/app text. Promotion is not a separate step:
when the render box completes a replacement, kind_robots'
`applyEntityArtCompletion` moves the entity's slot FK to the new ArtImage and
links the prior render into EntityArtImage history (nothing is deleted). This
script asks the live API whether that actually happened, job by job, so a
later session can report drain progress and catch a completed job whose
target never flipped.

Default ranges are the 2026-09-05 production runs:
  entity  ArtJob 18480-20617  (Character/Bot/Dream/Scenario/Reward/Facet, run 33978824187)
  facet   ArtJob 20618-21615  (Facet catalog v2/v3 resubmissions + coverage, run 33981806514)

Usage:
  python scripts/verify_krea_repair_promotion.py            # sample 40 per range
  python scripts/verify_krea_repair_promotion.py --all      # every job (slow: ~3k requests)
  python scripts/verify_krea_repair_promotion.py --jobs 18480 18481 20618
  python scripts/verify_krea_repair_promotion.py --sample 100 --json

Needs KR_API_TOKEN (and optionally KR_BASE_URL). Exit 0 = every checked DONE
job is promoted; exit 1 = a DONE job did not promote or a job FAILED;
exit 2 = unresolved (no token, API unreachable).
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
import urllib.error
import urllib.request

DEFAULT_RANGES = {
    "entity": (18480, 20617),
    "facet": (20618, 21615),
}
ENTITY_ROUTES = {
    "character": "characters",
    "bot": "bots",
    "dream": "dreams",
    "scenario": "scenarios",
    "reward": "rewards",
    "facet": "facets",
}
SLOT_ID_FIELD = {
    "cardPath": "cardArtImageId",
    "heroPath": "heroArtImageId",
    "iconPath": "iconArtImageId",
}


def api_get(base: str, token: str, path: str) -> dict | None:
    request = urllib.request.Request(
        base + path,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=40) as response:
            body = response.read()
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        raise
    return json.loads(body) if body[:1] == b"{" else None


def slot_state(base: str, token: str, entity_type: str, entity_id: int, field: str):
    route = ENTITY_ROUTES.get(entity_type)
    if not route or not entity_id:
        return None
    payload = api_get(base, token, f"/api/{route}/{entity_id}")
    data = (payload or {}).get("data") or {}
    if isinstance(data.get(entity_type), dict):
        data = data[entity_type]
    id_field = SLOT_ID_FIELD.get(field, "artImageId")
    return {"artImageId": data.get(id_field), "path": data.get(field)}


def check_job(base: str, token: str, job_id: int) -> dict:
    payload = api_get(base, token, f"/api/art/queue/{job_id}")
    job = ((payload or {}).get("data") or {}).get("job") or {}
    raw = job.get("payload") or {}
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except ValueError:
            raw = {}
    entity_art = raw.get("entityArt") or {}
    entity_type = str(entity_art.get("entityType") or "").lower()
    entity_id = int(entity_art.get("entityId") or 0)
    field = str(entity_art.get("field") or "imagePath")
    slot = slot_state(base, token, entity_type, entity_id, field) if job else None
    status = job.get("status")
    art_image_id = job.get("artImageId")
    promoted = bool(art_image_id) and slot is not None and slot["artImageId"] == art_image_id
    return {
        "job": job_id,
        "status": status,
        "artImageId": art_image_id,
        "target": f"{entity_type}:{entity_id}:{field}" if job else None,
        "slotArtImageId": (slot or {}).get("artImageId"),
        "promoted": promoted,
        "error": (job.get("error") or "")[:160],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--jobs", nargs="*", type=int, help="Explicit ArtJob ids to check")
    parser.add_argument("--all", action="store_true", help="Check every job in the default ranges")
    parser.add_argument("--sample", type=int, default=40, help="Jobs sampled per range (default 40)")
    parser.add_argument("--seed", type=int, default=None, help="Sampling seed")
    parser.add_argument("--json", action="store_true", help="Emit the full per-job report as JSON")
    args = parser.parse_args()

    token = os.environ.get("KR_API_TOKEN", "").strip()
    if not token:
        print("unresolved: KR_API_TOKEN is not set", file=sys.stderr)
        return 2
    base = os.environ.get("KR_BASE_URL", "https://kindrobots.org").rstrip("/")

    groups: dict[str, list[int]] = {}
    if args.jobs:
        groups["explicit"] = list(args.jobs)
    else:
        rng = random.Random(args.seed)
        for name, (lo, hi) in DEFAULT_RANGES.items():
            ids = list(range(lo, hi + 1))
            groups[name] = ids if args.all else sorted(rng.sample(ids, min(args.sample, len(ids))))

    exit_code = 0
    report: dict[str, list[dict]] = {}
    try:
        for name, ids in groups.items():
            rows = [check_job(base, token, job_id) for job_id in ids]
            report[name] = rows
            done = [r for r in rows if r["status"] == "DONE"]
            promoted = [r for r in done if r["promoted"]]
            queued = [r for r in rows if r["status"] in ("PENDING", "RUNNING")]
            failed = [r for r in rows if r["status"] not in ("PENDING", "RUNNING", "DONE")]
            unpromoted = [r for r in done if not r["promoted"]]
            print(
                f"{name}: checked {len(rows)} | DONE {len(done)} | promoted {len(promoted)} | "
                f"queued {len(queued)} | other {len(failed)}"
            )
            for row in unpromoted:
                print(f"  DONE but not promoted: job {row['job']} -> {row['target']} "
                      f"(job image {row['artImageId']}, slot image {row['slotArtImageId']})")
            for row in failed:
                print(f"  {row['status']}: job {row['job']} -> {row['target']} {row['error']}")
            if unpromoted or failed:
                exit_code = 1
    except (urllib.error.URLError, TimeoutError) as error:
        print(f"unresolved: Kind Robots API unreachable ({error})", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(report, indent=1))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
