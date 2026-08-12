#!/usr/bin/env python3
"""
retire_shadow_dreams.py — delete the daily-dream "shadow" Dreams.

Background
----------
Until this cleanup, build_dream_records.py created, for every Character /
Narrator / Reward in a daily-dream proposal, BOTH a real model row
(Character/Bot/Reward) AND a redundant "shadow" Dream of dreamType
CHARACTER / NARRATOR / REWARD, linked together by dreamIds. The dream index is
meant to hold only vibes (PITCH) and locations (LOCATION) — the shadow dreams
were noise.

Every shadow model was created with dreamIds = [shadow_dream, world_dream], so
each Character/Reward/Bot is ALREADY linked to its day's vibe (PITCH) dream. A
DB sweep confirmed 0 shadow models are linked to a shadow dream ONLY — so we can
simply delete the shadow dreams and every model stays attached to its vibe.
No re-linking is required.

What this does
--------------
  1. Fetch all dreams.
  2. Select shadows: dreamType in {CHARACTER, NARRATOR, REWARD}.
  3. SAFETY: for each shadow, confirm every model it links (Characters/Rewards/
     Bots) is ALSO linked to at least one NON-shadow dream. If a model would be
     orphaned, the shadow is SKIPPED and reported — never deleted blindly.
  4. DELETE each safe shadow via DELETE /api/dreams/{id}. Deleting a Dream drops
     only its M2M join rows; the Character/Reward/Bot rows and their vibe links
     are untouched.

Dry-run by default. Pass --apply to actually delete.

Env
---
  KR_BASE_URL   default https://kindrobots.org
  KR_API_TOKEN  required for --apply (Bearer beta-admin)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any

KR_BASE_URL = os.environ.get("KR_BASE_URL", "https://kindrobots.org").rstrip("/")
KR_API_TOKEN = os.environ.get("KR_API_TOKEN", "").strip()

SHADOW_TYPES = {"CHARACTER", "NARRATOR", "REWARD"}
MODEL_RELATIONS = ("Characters", "Rewards", "Bots")


def http_json(method: str, url: str, body: Any = None, timeout: int = 60):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    if KR_API_TOKEN:
        req.add_header("Authorization", f"Bearer {KR_API_TOKEN}")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode() or "null")
    except urllib.error.HTTPError as e:
        try:
            payload = json.loads(e.read().decode() or "null")
        except (ValueError, OSError):
            payload = None
        return e.code, payload
    except Exception as e:  # noqa: BLE001
        return 0, {"error": str(e)}


def fetch_all_dreams() -> list[dict]:
    status, resp = http_json("GET", f"{KR_BASE_URL}/api/dreams?page=1&pageSize=2000")
    if status != 200 or not isinstance(resp, dict):
        sys.exit(f"Failed to fetch dreams: HTTP {status} {str(resp)[:200]}")
    return resp.get("data") or []


def model_ids(dream: dict) -> list[tuple[str, int]]:
    """(relation, id) for every model linked to this dream."""
    out: list[tuple[str, int]] = []
    for rel in MODEL_RELATIONS:
        for x in dream.get(rel) or []:
            if isinstance(x, dict) and isinstance(x.get("id"), int):
                out.append((rel, x["id"]))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Delete daily-dream shadow Dreams.")
    ap.add_argument("--apply", action="store_true",
                    help="actually delete (default: dry-run)")
    args = ap.parse_args()

    if args.apply and not KR_API_TOKEN:
        sys.exit("KR_API_TOKEN is required for --apply.")

    dreams = fetch_all_dreams()
    by_type: dict[str, int] = {}
    for d in dreams:
        by_type[d.get("dreamType")] = by_type.get(d.get("dreamType"), 0) + 1
    print(f"Fetched {len(dreams)} dreams: "
          + ", ".join(f"{k}={v}" for k, v in sorted(by_type.items())))

    shadows = [d for d in dreams if d.get("dreamType") in SHADOW_TYPES]
    non_shadows = [d for d in dreams if d.get("dreamType") not in SHADOW_TYPES]

    # Every model id that is linked to at least one NON-shadow (vibe/location/…) dream.
    safe_model_ids: set[int] = set()
    for d in non_shadows:
        for _, mid in model_ids(d):
            safe_model_ids.add(mid)

    to_delete: list[dict] = []
    unsafe: list[tuple[dict, list[tuple[str, int]]]] = []
    for s in shadows:
        orphans = [(rel, mid) for rel, mid in model_ids(s) if mid not in safe_model_ids]
        if orphans:
            unsafe.append((s, orphans))
        else:
            to_delete.append(s)

    print(f"\nShadow dreams: {len(shadows)} "
          f"({len(to_delete)} safe to delete, {len(unsafe)} skipped)")

    if unsafe:
        print("\n⚠️  SKIPPED — these shadows link a model with no other dream "
              "(would orphan it). Re-link manually first:")
        for s, orphans in unsafe:
            print(f"   dream #{s.get('id')} {s.get('slug')} ({s.get('dreamType')}) "
                  f"-> orphans {orphans}")

    if not to_delete:
        print("\nNothing to delete.")
        return 0

    print(f"\n{'DELETING' if args.apply else '[dry-run] would delete'} "
          f"{len(to_delete)} shadow dreams:")
    deleted = 0
    for s in to_delete:
        label = f"#{s.get('id')} {s.get('slug')} ({s.get('dreamType')})"
        if not args.apply:
            print(f"   [dry-run] DELETE /api/dreams/{s.get('id')}  {label}")
            continue
        status, resp = http_json("DELETE", f"{KR_BASE_URL}/api/dreams/{s.get('id')}")
        if status in (200, 204):
            deleted += 1
            print(f"   ✅ deleted {label}")
        else:
            print(f"   ❌ FAIL {status} {label}: {str(resp)[:160]}", file=sys.stderr)

    if args.apply:
        print(f"\nDeleted {deleted}/{len(to_delete)} shadow dreams. "
              f"Their Character/Reward/Bot rows remain linked to their vibe dream.")
    else:
        print("\nDry-run only. Re-run with --apply (and KR_API_TOKEN set) to delete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
