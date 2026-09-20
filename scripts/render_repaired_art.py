#!/usr/bin/env python3
"""Queue the re-renders that scripts/repair_negation_art_prompts.py could not.

WHY A SEPARATE SCRIPT

The repair script's `--apply --render` does both halves in one pass, which is
the intended usage. On 2026-09-19 they were run separately, and then the
KR_API_TOKEN expired partway through the render half: 746 of 1,154 jobs were
queued and 408 were refused with a 401. By then the prompts were already clean,
so re-running the repair script found nothing to render -- it keys on records
that still violate, and none did.

Hence the manifest. `projects/kind-robots/repairs/2026-09-20-negation-repair.json`
records every record that pass touched, split into the ones that reached the
queue and the ones that did not. This script takes the `not_queued` list, reads
each record's CURRENT prompt from the live API (the repaired text is already
stored there -- the manifest deliberately holds no prompt copies to go stale),
and enqueues it.

Safe to re-run: `--skip-queued` asks the ArtJob queue which of these already
have a `designer: negation-repair` job and leaves those alone, so a partial run
resumes rather than double-queueing.

Priority matches the repair script: rewards 60, everything else 40. Between
/api/art/enqueue's interactive default (100) and the bulk lanes (0 and below),
so repairs keep the relay busy without making a human who just clicked Generate
wait behind hundreds of them.

Usage:
  python scripts/render_repaired_art.py                    # dry run
  python scripts/render_repaired_art.py --apply
  python scripts/render_repaired_art.py --apply --kind dream --kind scenario

Environment:
  KR_API_TOKEN   required with --apply
  KR_BASE_URL    defaults to https://kindrobots.org

Exit codes:
  0  nothing left to queue, or every job was accepted
  1  some records were refused (the reason is printed per record)
  2  could not run (no token, or the API was unreachable)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "projects" / "kind-robots" / "repairs" / "2026-09-20-negation-repair.json"

KR_BASE_URL = os.environ.get("KR_BASE_URL", "https://kindrobots.org").rstrip("/")
KR_API_TOKEN = os.environ.get("KR_API_TOKEN", "").strip()

DETAIL = {
    "reward": "/api/rewards",
    "facet": "/api/facets",
    "character": "/api/characters",
    "scenario": "/api/scenarios",
    "dream": "/api/dreams",
    "bot": "/api/bots",
    "achievement": "/api/achievements",
    "resource": "/api/resources",
}
ORDER = ("reward", "facet", "dream", "scenario", "bot", "achievement", "resource", "character")
RENDER_PRIORITY = {"reward": 60}
DEFAULT_RENDER_PRIORITY = 40

# The entityArt slot each kind writes its ONE main image into. Every kind in
# this manifest uses `imagePath` except bot, whose primary slot is
# `avatarImage` (server/utils/entityArt.ts). Sending `imagePath` for a bot is
# refused with 400 "Invalid bot image field." -- and because the first repair
# pass died before it reached a single bot, all 64 of them hit that for the
# first time here.
PRIMARY_FIELD = {"bot": "avatarImage"}
DEFAULT_PRIMARY_FIELD = "imagePath"

# /api/art/queue caps `limit` at 200 whatever is asked for -- a limit=1000 read
# silently answers with the first 200 of 1,132 and looks complete.
QUEUE_PAGE = 200


def http_json(method: str, url: str, body: Any = None, timeout: int = 180):
    """Returns (status, payload). A 4xx comes back as a value, not an exception.

    The run this script exists to finish logged every failure as the string
    "HTTP Error 422" because urllib raises on 4xx and the caller caught it in a
    generic except. Genuine contract rejections and an expired token were
    indistinguishable in the log. Read the body.
    """
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(url, data=data, method=method)
    request.add_header("Accept", "application/json")
    if data is not None:
        request.add_header("Content-Type", "application/json")
    if KR_API_TOKEN:
        request.add_header("Authorization", f"Bearer {KR_API_TOKEN}")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode()
            return response.status, (json.loads(raw) if raw.strip() else {})
    except urllib.error.HTTPError as error:
        raw = error.read().decode(errors="replace")
        try:
            return error.code, json.loads(raw)
        except json.JSONDecodeError:
            return error.code, {"message": raw[:400]}
    except OSError as error:
        return 0, {"message": str(error)}


def already_queued() -> set[tuple[str, int]]:
    """(entityType, entityId) pairs that already hold a negation-repair job.

    Two things made the first version of this return an empty set and say
    nothing about it, so every run looked like a clean first run:

    - `designer` is not a top-level payload key. The enqueue endpoint files it
      under `payload.save.designer`, so `payload["designer"]` was always None
      and the `!= "negation-repair"` test skipped every job there was.
    - `limit` is capped at 200 server-side. A `limit=1000` read answers "200 of
      1132 job(s)" with a 200-row body, so even a correct designer test would
      have seen a sixth of the queue.
    """
    seen: set[tuple[str, int]] = set()
    for status in ("PENDING", "RUNNING", "DONE"):
        skip = 0
        while True:
            code, payload = http_json(
                "GET",
                f"{KR_BASE_URL}/api/art/queue?limit={QUEUE_PAGE}&skip={skip}&status={status}",
            )
            if code != 200:
                print(f"  (could not read {status} jobs: {code} {str(payload)[:120]})", file=sys.stderr)
                break
            jobs = (payload.get("data") or {}).get("jobs") or []
            if not jobs:
                break
            for job in jobs:
                job_payload = job.get("payload") or {}
                save = job_payload.get("save") or {}
                if save.get("designer") != "negation-repair":
                    continue
                art = job_payload.get("entityArt") or {}
                kind, row_id = art.get("entityType"), art.get("entityId")
                if kind and isinstance(row_id, int):
                    seen.add((kind, row_id))
            if len(jobs) < QUEUE_PAGE:
                break
            skip += QUEUE_PAGE
    return seen


# /api/facets/:id resolves a SLUG, not a numeric id: "/api/facets/3d-render"
# answers 200 and "/api/facets/1417" answers 404 "Facet not found." for the
# same row. The manifest stores numeric ids, so the detail route refused all
# 575 facets -- reported per record as "no artPrompt on the live record", which
# reads like missing data rather than a wrong URL. The repair script never hit
# this because it works from the paged list, which carries artPrompt on every
# row; so does this, now.
_FACET_ROWS: Optional[dict[int, dict[str, Any]]] = None


def facet_rows() -> dict[int, dict[str, Any]]:
    global _FACET_ROWS
    if _FACET_ROWS is not None:
        return _FACET_ROWS
    rows: dict[int, dict[str, Any]] = {}
    skip = 0
    while True:
        code, payload = http_json("GET", f"{KR_BASE_URL}/api/facets?take=250&skip={skip}")
        batch = ((payload.get("data") if code == 200 else None) or [])
        if not batch:
            break
        before = len(rows)
        for row in batch:
            if isinstance(row.get("id"), int):
                rows[row["id"]] = row
        # An endpoint that ignored `skip` would hand back the same page forever.
        if len(rows) == before:
            break
        skip += 250
    _FACET_ROWS = rows
    return rows


def fetch_prompt(kind: str, row_id: int) -> Optional[dict[str, Any]]:
    if kind == "facet":
        return facet_rows().get(row_id)
    status, payload = http_json("GET", f"{KR_BASE_URL}{DETAIL[kind]}/{row_id}")
    if status != 200:
        return None
    row = payload.get("data") or payload
    if isinstance(row, dict) and kind in row:
        row = row[kind]
    return row if isinstance(row, dict) else None


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--kind", choices=ORDER, action="append", help="limit to one kind (repeatable)")
    parser.add_argument("--apply", action="store_true", help="actually enqueue")
    parser.add_argument("--skip-queued", action="store_true", default=True,
                        help="skip records that already hold a negation-repair job (default)")
    parser.add_argument("--no-skip-queued", dest="skip_queued", action="store_false")
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.apply and not KR_API_TOKEN:
        print("KR_API_TOKEN is required for --apply.", file=sys.stderr)
        return 2
    if not MANIFEST.exists():
        print(f"Manifest not found: {MANIFEST}", file=sys.stderr)
        return 2

    manifest = json.loads(MANIFEST.read_text())
    targets: list[tuple[str, int]] = []
    for entry in manifest.get("not_queued") or []:
        kind, _, raw_id = entry.partition("/")
        if args.kind and kind not in args.kind:
            continue
        targets.append((kind, int(raw_id)))

    print(f"Manifest: {manifest.get('total')} repaired, "
          f"{len(manifest.get('queued') or [])} already queued, "
          f"{len(manifest.get('not_queued') or [])} outstanding.")
    print(f"Selected: {len(targets)}  {Counter(k for k, _ in targets).most_common()}")

    if args.skip_queued and args.apply:
        seen = already_queued()
        before = len(targets)
        targets = [t for t in targets if t not in seen]
        if before != len(targets):
            print(f"Skipping {before - len(targets)} that already hold a negation-repair job.")

    if not args.apply:
        print("\nDry run. Re-run with --apply to enqueue.")
        return 0

    targets.sort(key=lambda t: (ORDER.index(t[0]) if t[0] in ORDER else 99, t[1]))
    queued = Counter()
    refused: list[str] = []

    for n, (kind, row_id) in enumerate(targets, 1):
        row = fetch_prompt(kind, row_id)
        if not row or not (row.get("artPrompt") or "").strip():
            refused.append(f"{kind}/{row_id}: no artPrompt on the live record")
            continue
        body = {
            "engine": "krea2",
            "promptString": row["artPrompt"],
            "width": 1024,
            "height": 1024,
            "isPublic": bool(row.get("isPublic", True)),
            "isMature": bool(row.get("isMature", False)),
            "designer": "negation-repair",
            "priority": RENDER_PRIORITY.get(kind, DEFAULT_RENDER_PRIORITY),
            "entityArt": {
                "entityType": kind,
                "entityId": row_id,
                "field": PRIMARY_FIELD.get(kind, DEFAULT_PRIMARY_FIELD),
                # Keep the old image in the record's art history.
                "preserveOriginal": True,
                "mode": "recreate",
            },
        }
        status, payload = http_json("POST", f"{KR_BASE_URL}/api/art/enqueue", body)
        if status in (200, 201):
            queued[kind] += 1
        else:
            message = (payload or {}).get("message") or str(payload)
            refused.append(f"{kind}/{row_id}: {status} {str(message)[:220]}")
            if status == 401:
                print("\n401 Unauthorized -- the token is not being accepted. Stopping rather "
                      "than logging hundreds of identical failures.", file=sys.stderr)
                break
        if n % 50 == 0:
            print(f"  {n}/{len(targets)} queued={sum(queued.values())} refused={len(refused)}", flush=True)

    print(f"\nQueued {sum(queued.values())}: {dict(queued)}")
    if refused:
        print(f"Refused {len(refused)}:")
        for line in refused[:40]:
            print("  ", line)
        if len(refused) > 40:
            print(f"   ... and {len(refused) - 40} more")
    return 1 if refused else 0


if __name__ == "__main__":
    raise SystemExit(main())
