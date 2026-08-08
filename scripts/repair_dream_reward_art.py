#!/usr/bin/env python3
"""Repair daily-dream Reward art that was generated from a barebones prompt.

Background (2026-08-08). Every dream Reward was created with
`artPrompt = f"{name}: {grants}"` — a sentence about what the thing *does*, with
no physical description at all — and the queued render prompt then appended a
house block containing an unconditional "cast characters naturally across many
species, ages, body sizes..." instruction. Krea 2 reads that clause as subject
matter, so 24 Rewards rendered as crowds of people. `item-tidefortune-ladle` is
a picture of fifteen strangers and no ladle.

This script fixes the existing damage. The forward fix lives in
`scripts/dream_art_prompts.py` (prompt construction) and in kind_robots'
`server/utils/artJobNormalization.ts` (the casting clause is now opt-in).

What it does, per affected Reward:

  1. Rebuilds the art prompt from its proposal's `look`, `grants`, rarity, and
     world context using the shared Krea 2 builder.
  2. PATCHes the Reward's stored `artPrompt`, so the site's "Redo from prompt"
     workbench reproduces the good prompt instead of the barebones one.
  3. Enqueues a Krea 2 `recreate` job against the Reward's `imagePath`, with
     `preserveOriginal` so the previous image is kept in object history rather
     than destroyed.

Nothing is destructive: step 3 keeps the old art, and step 2 only overwrites a
prompt that was demonstrably unusable.

Usage:
  python scripts/repair_dream_reward_art.py            # dry run, prints a plan
  python scripts/repair_dream_reward_art.py --apply
  python scripts/repair_dream_reward_art.py --apply --only tidefortune-ladle
  python scripts/repair_dream_reward_art.py --apply --skip-render   # prompts only

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
from dream_art_prompts import reward_prompt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BACKLOG = ROOT / "projects" / "dream-cycle" / "backlog"
KR_BASE_URL = os.environ.get("KR_BASE_URL", "https://kind-robots.vercel.app").rstrip("/")
KR_API_TOKEN = os.environ.get("KR_API_TOKEN", "").strip()

# Reward card art is portrait; matches CARD_SIZE in build_dream_records.py.
RENDER_WIDTH, RENDER_HEIGHT = 512, 768
ENGINE = "krea2"


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


def proposal_rewards() -> dict[str, dict[str, Any]]:
    """Map reward name -> {reward, world title, vibe line, proposal file}."""
    found: dict[str, dict[str, Any]] = {}
    for path in sorted(BACKLOG.glob("*.md")):
        match = re.search(r"<!-- proposal-data\n(.*?)\n-->", path.read_text(encoding="utf-8"), re.S)
        if not match:
            continue
        try:
            proposal = json.loads(match.group(1))
        except json.JSONDecodeError:
            continue
        vibe = proposal.get("vibe") or {}
        for reward in proposal.get("rewards") or []:
            name = str(reward.get("name") or "").strip()
            if name:
                found[name] = {
                    "reward": reward,
                    "world_title": proposal.get("title", ""),
                    "vibe_line": vibe.get("line", ""),
                    "source": path.name,
                }
    return found


def is_barebones(record: dict[str, Any]) -> bool:
    """The exact string the old builder produced: "Name: description"."""
    expected = f"{record.get('name', '')}: {record.get('description') or ''}".strip()
    return (record.get("artPrompt") or "").strip() == expected


def live_rewards() -> list[dict[str, Any]]:
    status, payload = http_json("GET", f"{KR_BASE_URL}/api/rewards?take=2000")
    if status != 200:
        raise SystemExit(f"Could not list rewards ({status}): {str(payload)[:200]}")
    rows = payload.get("data") if isinstance(payload, dict) else payload
    if not isinstance(rows, list):
        raise SystemExit("Unexpected /api/rewards response shape.")
    return rows


def plan(only: Optional[str]) -> list[dict[str, Any]]:
    proposals = proposal_rewards()
    work = []
    for record in live_rewards():
        if not is_barebones(record):
            continue
        slug = str(record.get("slug") or "")
        if only and only not in slug and only.lower() not in str(record.get("name", "")).lower():
            continue
        context = proposals.get(str(record.get("name") or "").strip())
        if not context:
            print(f"  ! no proposal found for reward {record.get('id')} "
                  f"{record.get('name')!r}; skipping", file=sys.stderr)
            continue
        reward = context["reward"]
        prompt = reward_prompt(
            reward.get("name", record.get("name", "")),
            reward.get("reward_type", record.get("rewardType", "ITEM")),
            reward.get("look", ""),
            reward.get("grants", record.get("description", "")),
            reward.get("rarity", record.get("rarity", "")),
            context["world_title"],
            context["vibe_line"],
        )
        work.append({
            "id": record["id"],
            "slug": slug,
            "name": record.get("name"),
            "reward_type": record.get("rewardType"),
            "has_art": bool(record.get("imagePath")),
            "is_public": bool(record.get("isPublic", True)),
            "is_mature": bool(record.get("isMature", False)),
            "old_prompt": record.get("artPrompt"),
            "new_prompt": prompt,
            "had_look": bool(reward.get("look")),
            "source": context["source"],
        })
    return work


def patch_prompt(item: dict[str, Any]) -> bool:
    status, payload = http_json(
        "PATCH", f"{KR_BASE_URL}/api/rewards/{item['id']}",
        {"artPrompt": item["new_prompt"]})
    if status not in (200, 201):
        print(f"  prompt PATCH FAILED {status} reward/{item['id']}: "
              f"{str(payload)[:160]}", file=sys.stderr)
        return False
    return True


def enqueue_render(item: dict[str, Any]) -> Optional[int]:
    body = {
        "engine": ENGINE,
        "promptString": item["new_prompt"],
        "width": RENDER_WIDTH,
        "height": RENDER_HEIGHT,
        "isPublic": item["is_public"],
        "isMature": item["is_mature"],
        "designer": "dream-cycle",
        # Ahead of the facet-catalog backlog: this is corrective work on art
        # that is live and wrong on the site right now.
        "priority": 10,
        "entityArt": {
            "entityType": "reward",
            "entityId": item["id"],
            "field": "imagePath",
            # Keep the crowd images in object history rather than deleting them.
            "preserveOriginal": True,
            "mode": "recreate",
        },
    }
    status, payload = http_json("POST", f"{KR_BASE_URL}/api/art/enqueue", body)
    if status not in (200, 201):
        print(f"  enqueue FAILED {status} reward/{item['id']}: "
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
    parser.add_argument("--only", help="restrict to rewards matching this slug or name")
    args = parser.parse_args(argv)

    if args.apply and not KR_API_TOKEN:
        print("KR_API_TOKEN is required with --apply.", file=sys.stderr)
        return 2

    work = plan(args.only)
    if not work:
        print("No rewards with barebones art prompts. Nothing to repair.")
        return 0

    missing_look = [w for w in work if not w["had_look"]]
    print(f"{len(work)} reward(s) with a barebones art prompt "
          f"({sum(1 for w in work if w['has_art'])} already showing wrong art).")
    if missing_look:
        print(f"  {len(missing_look)} have no `look` in their proposal and will get a "
              f"weaker generic framing: "
              f"{', '.join(w['name'] for w in missing_look)}")

    patched = queued = 0
    for item in work:
        print(f"\n[{item['id']}] {item['reward_type']:5} {item['name']}  ({item['source']})")
        print(f"  old: {item['old_prompt']}")
        print(f"  new: {item['new_prompt']}")
        if not args.apply:
            continue
        if patch_prompt(item):
            patched += 1
            print("  prompt updated")
        if args.skip_render:
            continue
        job_id = enqueue_render(item)
        if job_id:
            queued += 1
            print(f"  queued ArtJob {job_id} (previous image preserved)")

    if not args.apply:
        print(f"\nDry run. Re-run with --apply to update {len(work)} prompt(s)"
              f"{'' if args.skip_render else ' and queue their re-renders'}.")
    else:
        print(f"\nUpdated {patched} prompt(s); queued {queued} re-render(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
