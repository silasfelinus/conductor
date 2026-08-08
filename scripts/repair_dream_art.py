#!/usr/bin/env python3
"""Repair daily-dream art that was generated under the old prompt regime.

Background (2026-08-08). Every dream art prompt ended in the literal phrase
"cohesive Kind Robots visual style", which the Kind Robots enqueue path rewrote
into a house block carrying an unconditional casting instruction: "cast
characters naturally across many species, ages, body sizes, body shapes, gender
presentations...". Krea 2 is a distilled diffusion transformer with no
instruction-following layer, so it painted that clause instead of reading it as
guidance — and on top of that, Rewards had no physical description at all
(`artPrompt` was literally `f"{name}: {grants}"`). The result was crowds of
strangers where a ladle, a place, or one character should have been.

The forward fix is `scripts/dream_art_prompts.py` plus kind_robots'
`server/utils/artJobNormalization.ts`. This script cleans up what already
rendered, across all five element kinds:

  world      Dream (PITCH)    crowd instead of an establishing view
  location   Dream (LOCATION) crowd instead of architecture
  character  Character        crowd instead of one figure
  reward     Reward           crowd instead of the object — the total failure
  scenario   Scenario         crowd instead of a readable moment

Per element it rebuilds the prompt from the proposal, PATCHes the record's
stored `artPrompt` (so the site's "Redo from prompt" workbench reproduces it),
and enqueues a Krea 2 `recreate` job with `preserveOriginal` so the old image is
kept in object history rather than destroyed. Nothing here is destructive.

Record IDs come from each proposal's `built-data` block, which is the
authoritative mapping from proposal element to live row.

Renders are throttled by the shared ArtJob queue (~44/day observed), so
`--limit` exists to stage the work in priority order rather than dumping a
hundred jobs at once.

Usage:
  python scripts/repair_dream_art.py                       # dry run, full plan
  python scripts/repair_dream_art.py --kind reward --apply
  python scripts/repair_dream_art.py --apply --limit 30
  python scripts/repair_dream_art.py --apply --skip-render # prompts only

Environment:
  KR_API_TOKEN   required with --apply
  KR_BASE_URL    defaults to https://kind-robots.vercel.app
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dream_art_prompts import (  # noqa: E402
    STYLE,
    character_prompt,
    location_prompt,
    reward_prompt,
    scenario_prompt,
    world_prompt,
)

ROOT = Path(__file__).resolve().parents[1]
BACKLOG = ROOT / "projects" / "dream-cycle" / "backlog"
KR_BASE_URL = os.environ.get("KR_BASE_URL", "https://kind-robots.vercel.app").rstrip("/")
KR_API_TOKEN = os.environ.get("KR_API_TOKEN", "").strip()

# Card art is portrait; matches CARD_SIZE in build_dream_records.py.
RENDER_WIDTH, RENDER_HEIGHT = 512, 768
ENGINE = "krea2"

# Repair order. Rewards first because their failure is total — the subject is
# simply absent — then characters, whose portraits came back as crowds.
KINDS = ("reward", "character", "location", "world", "scenario")

ENDPOINT = {
    "world": "/api/dreams",
    "location": "/api/dreams",
    "character": "/api/characters",
    "reward": "/api/rewards",
    "scenario": "/api/scenarios",
}
ENTITY_TYPE = {
    "world": "dream",
    "location": "dream",
    "character": "character",
    "reward": "reward",
    "scenario": "scenario",
}


def http_json(method: str, url: str, body: Any = None,
              timeout: int = 90) -> tuple[int, Any]:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    if KR_API_TOKEN:
        req.add_header("Authorization", f"Bearer {KR_API_TOKEN}")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode() or "null")
    except urllib.error.HTTPError as error:
        try:
            payload = json.loads(error.read().decode() or "null")
        except (ValueError, OSError):
            payload = None
        return error.code, payload
    except (OSError, ValueError) as error:
        return 0, {"message": str(error)}


def _block(text: str, name: str) -> Optional[dict[str, Any]]:
    match = re.search(rf"<!-- {name}\n(.*?)\n-->", text, re.S)
    if not match:
        return None
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError:
        return None


def built_proposals() -> list[tuple[str, dict[str, Any], dict[str, Any]]]:
    """(filename, proposal, built) for every proposal that has real records."""
    out = []
    for path in sorted(BACKLOG.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        proposal = _block(text, "proposal-data")
        built = _block(text, "built-data")
        if proposal and built and built.get("records"):
            out.append((path.name, proposal, built))
    return out


def elements(proposal: dict[str, Any],
             built: dict[str, Any]) -> list[dict[str, Any]]:
    """Pair each proposal element with its live record id and rebuilt prompt."""
    title = proposal.get("title", "")
    vibe = proposal.get("vibe") or {}
    line = vibe.get("line", "")
    records = built.get("records") or {}
    found: list[dict[str, Any]] = []

    world = records.get("world") or {}
    if world.get("id"):
        found.append({
            "kind": "world", "id": world["id"], "label": world.get("title", title),
            "prompt": world_prompt(title, proposal.get("idea", ""), line,
                                   vibe.get("art_direction", "")),
        })

    for record, source in zip(records.get("locations") or [],
                              proposal.get("locations") or []):
        if record.get("id"):
            found.append({
                "kind": "location", "id": record["id"],
                "label": source.get("title", ""),
                "prompt": location_prompt(source.get("title", ""),
                                          source.get("art_direction", ""),
                                          source.get("known_for", ""),
                                          source.get("best_scene", ""), title, line),
            })

    for record, source in zip(records.get("characters") or [],
                              proposal.get("characters") or []):
        if record.get("id"):
            found.append({
                "kind": "character", "id": record["id"],
                "label": source.get("name", ""),
                "prompt": character_prompt(source.get("name", ""), source.get("look", ""),
                                           source.get("role_drive", ""),
                                           source.get("carries", ""), title, line),
            })

    # Rewards are matched by name, not by position: the ITEM/SKILL order in
    # built-data follows creation order, which is not always proposal order.
    by_name = {str(r.get("name") or ""): r for r in (proposal.get("rewards") or [])}
    for record in records.get("rewards") or []:
        source = by_name.get(str(record.get("name") or ""))
        if record.get("id") and source:
            found.append({
                "kind": "reward", "id": record["id"], "label": source.get("name", ""),
                "prompt": reward_prompt(source.get("name", ""),
                                        source.get("reward_type", "ITEM"),
                                        source.get("look", ""), source.get("grants", ""),
                                        source.get("rarity", ""), title, line),
            })

    locations = ", ".join(l.get("title", "") for l in proposal.get("locations") or [])
    for record, source in zip(records.get("scenarios") or [],
                              proposal.get("scenarios") or []):
        if record.get("id"):
            found.append({
                "kind": "scenario", "id": record["id"],
                "label": source.get("title", ""),
                "prompt": scenario_prompt(source.get("title", ""), source.get("setup", ""),
                                          locations, title, line),
            })

    return found


def fetch_record(kind: str, record_id: int) -> Optional[dict[str, Any]]:
    status, payload = http_json("GET", f"{KR_BASE_URL}{ENDPOINT[kind]}/{record_id}")
    if status != 200:
        return None
    data = payload.get("data") if isinstance(payload, dict) else payload
    return data if isinstance(data, dict) else None


def needs_repair(record: dict[str, Any]) -> bool:
    """True when this row's art predates the new builder.

    Every prompt the new builder writes contains the house STYLE string verbatim.
    Anything with an image whose stored prompt lacks it was generated under the
    old regime and is a repair candidate. Rows with no art yet are skipped —
    their pending job already carries a rebuilt prompt.
    """
    if not record.get("imagePath"):
        return False
    return STYLE not in (record.get("artPrompt") or "")


def plan(kinds: tuple[str, ...], only: Optional[str]) -> list[dict[str, Any]]:
    work: list[dict[str, Any]] = []
    for source, proposal, built in built_proposals():
        for element in elements(proposal, built):
            if element["kind"] not in kinds:
                continue
            if only and only.lower() not in element["label"].lower() \
                    and only.lower() not in source.lower():
                continue
            record = fetch_record(element["kind"], element["id"])
            if not record:
                print(f"  ! {element['kind']} {element['id']} "
                      f"({element['label']}) not found live; skipping", file=sys.stderr)
                continue
            if not needs_repair(record):
                continue
            work.append({**element, "source": source,
                         "old_prompt": record.get("artPrompt") or "",
                         "is_public": bool(record.get("isPublic", True)),
                         "is_mature": bool(record.get("isMature", False))})
    # Rewards first, then characters, then the rest — worst damage first.
    work.sort(key=lambda item: KINDS.index(item["kind"]))
    return work


def patch_prompt(item: dict[str, Any]) -> bool:
    status, payload = http_json(
        "PATCH", f"{KR_BASE_URL}{ENDPOINT[item['kind']]}/{item['id']}",
        {"artPrompt": item["prompt"]})
    if status not in (200, 201):
        print(f"  prompt PATCH FAILED {status} {item['kind']}/{item['id']}: "
              f"{str(payload)[:160]}", file=sys.stderr)
        return False
    return True


def enqueue_render(item: dict[str, Any]) -> Optional[int]:
    body = {
        "engine": ENGINE,
        "promptString": item["prompt"],
        "width": RENDER_WIDTH,
        "height": RENDER_HEIGHT,
        "isPublic": item["is_public"],
        "isMature": item["is_mature"],
        "designer": "dream-cycle",
        # Ahead of the facet-catalog backlog: this is corrective work on art
        # that is live and wrong on the site right now.
        "priority": 10,
        "entityArt": {
            "entityType": ENTITY_TYPE[item["kind"]],
            "entityId": item["id"],
            "field": "imagePath",
            # Keep the crowd images in object history rather than deleting them.
            "preserveOriginal": True,
            "mode": "recreate",
        },
    }
    status, payload = http_json("POST", f"{KR_BASE_URL}/api/art/enqueue", body)
    if status not in (200, 201):
        print(f"  enqueue FAILED {status} {item['kind']}/{item['id']}: "
              f"{str(payload)[:200]}", file=sys.stderr)
        return None
    job_id = ((payload or {}).get("data") or {}).get("jobId")
    return int(job_id) if job_id else None


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--apply", action="store_true",
                        help="write prompts and queue renders (default is a dry run)")
    parser.add_argument("--skip-render", action="store_true",
                        help="update stored artPrompt only; queue no ArtJobs")
    parser.add_argument("--kind", choices=KINDS, action="append",
                        help="restrict to one element kind (repeatable)")
    parser.add_argument("--only", help="restrict to elements or proposals matching this text")
    parser.add_argument("--limit", type=int,
                        help="stop after this many elements, worst damage first")
    parser.add_argument("--verbose", action="store_true",
                        help="print the full old and new prompts")
    args = parser.parse_args(argv)

    if args.apply and not KR_API_TOKEN:
        print("KR_API_TOKEN is required with --apply.", file=sys.stderr)
        return 2

    work = plan(tuple(args.kind) if args.kind else KINDS, args.only)
    if args.limit:
        work = work[: args.limit]
    if not work:
        print("No dream art predating the new prompt builder. Nothing to repair.")
        return 0

    counts: dict[str, int] = {}
    for item in work:
        counts[item["kind"]] = counts.get(item["kind"], 0) + 1
    print(f"{len(work)} element(s) to repair: "
          + ", ".join(f"{n} {k}" for k, n in counts.items()))

    patched = queued = 0
    for item in work:
        print(f"\n[{item['kind']}/{item['id']}] {item['label']}  ({item['source']})")
        if args.verbose:
            print(f"  old: {item['old_prompt'][:300]}")
            print(f"  new: {item['prompt']}")
        else:
            print(f"  new: {item['prompt'][:160]}...")
        if not args.apply:
            continue
        # Enqueue BEFORE patching. `needs_repair` decides from the stored
        # artPrompt, so patching first and then failing to enqueue (one transient
        # SSL drop did exactly this to character/2800) leaves a row that still
        # shows the old crowd but no longer looks like a candidate — invisible to
        # every future run. Enqueue-first means a failure here is retryable.
        if not args.skip_render:
            job_id = enqueue_render(item)
            if not job_id:
                print("  skipping prompt update so this row stays retryable",
                      file=sys.stderr)
                continue
            queued += 1
            print(f"  queued ArtJob {job_id} (previous image preserved)")
        if patch_prompt(item):
            patched += 1

    if not args.apply:
        print(f"\nDry run. Re-run with --apply to update {len(work)} prompt(s)"
              f"{'' if args.skip_render else ' and queue their re-renders'}.")
    else:
        print(f"\nUpdated {patched} prompt(s); queued {queued} re-render(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
