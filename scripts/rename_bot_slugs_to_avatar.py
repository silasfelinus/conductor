#!/usr/bin/env python3
"""
rename_bot_slugs_to_avatar.py — make each bot's slug match its avatarImage
filename (kind-robots/t-011 follow-up).

Root cause this closes: narrator bots got their DB `slug` auto-generated
from their full display name (e.g. "Pip the Lampkeeper" -> slug
"pip-the-lampkeeper") independently of their `avatarImage` field (e.g.
"/images/bots/brass-lampkeeper.webp") and the expression-image folder
named after it ("brass-lampkeeper/"). Two names for the same bot, in two
different places, with nothing keeping them in sync -- exactly the
"bandaid" pattern Silas flagged after reconcile_expressions.py needed a
whole extra fallback-matching tier just to bridge them.

This script goes the other direction from that fallback: instead of
teaching more code to reconcile two names, it makes the slug BE the
avatarImage name, so there is only one name again. Once run,
reconcile_expressions.py's avatarImage-fallback tier becomes a no-op
safety net for these bots rather than something load-bearing.

Scope: only touches bots (and, if ever relevant, characters) whose current
slug differs from their avatarImage filename stem. A bot with no
avatarImage, or whose slug already matches, is left untouched. Renames go
through the existing PATCH /api/bots/{id} endpoint, which already runs the
new slug through getUniqueBotSlug(..., excludeId) -- a collision auto-
suffixes rather than silently overwriting another bot's slug.

Env:
  KR_API_TOKEN  required for --apply (admin or server key); reads are public
  KR_BASE_URL   default https://kind-robots.vercel.app

Usage:
  python scripts/rename_bot_slugs_to_avatar.py             # dry-run plan
  python scripts/rename_bot_slugs_to_avatar.py --apply      # perform renames
  python scripts/rename_bot_slugs_to_avatar.py --type bot   # limit owner type

Exit codes: 0 = ok (plan or apply succeeded), 1 = error
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

KR_BASE_URL = os.environ.get("KR_BASE_URL", "https://kind-robots.vercel.app").rstrip("/")
KR_API_TOKEN = os.environ.get("KR_API_TOKEN", "").strip()


def api(path, payload=None, method=None, timeout=30):
    """GET/PATCH the kind_robots API. Returns parsed JSON or raises."""
    url = f"{KR_BASE_URL}{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method or ("POST" if data else "GET"))
    req.add_header("Content-Type", "application/json")
    if KR_API_TOKEN:
        req.add_header("Authorization", f"Bearer {KR_API_TOKEN}")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def fetch_all_owners(owner_type):
    """Every bot/character row (id, slug, avatarImage), paginated
    defensively the same way reconcile_expressions.py does: stop as soon as
    a page adds nothing new, so a pagination regression can't loop
    forever."""
    path = "/api/bots" if owner_type == "bot" else "/api/characters"
    rows_out, seen_ids, page = [], set(), 1
    while True:
        body = api(f"{path}?page={page}&pageSize=100")
        rows = body.get("data") or []
        if isinstance(rows, dict):
            rows = rows.get(f"{owner_type}s") or []
        before = len(seen_ids)
        for row in rows:
            if row.get("id") is not None and row["id"] not in seen_ids:
                seen_ids.add(row["id"])
                rows_out.append(row)
        if len(seen_ids) == before or len(rows) < 100:
            return rows_out
        page += 1


def build_rename_plan(owner_type):
    """[(id, old_slug, new_slug), ...] for every owner whose slug doesn't
    already match its avatarImage filename stem. Skips owners with no
    avatarImage or whose slug already matches (nothing to do)."""
    plan = []
    for row in fetch_all_owners(owner_type):
        old_slug = (row.get("slug") or "").strip()
        avatar_image = (row.get("avatarImage") or "").strip()
        if not (old_slug and avatar_image):
            continue
        new_slug = Path(avatar_image).stem.strip().lower()
        if new_slug and new_slug != old_slug:
            plan.append((row["id"], old_slug, new_slug))
    return plan


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--apply", action="store_true", help="perform the renames")
    ap.add_argument("--type", choices=("bot", "character"), help="limit owner type")
    args = ap.parse_args()

    if args.apply and not KR_API_TOKEN:
        print("❌ --apply requires KR_API_TOKEN (admin or server key).", file=sys.stderr)
        return 1

    owner_types = [args.type] if args.type else ["bot", "character"]
    total_planned = 0
    total_applied = 0
    errors = []

    for owner_type in owner_types:
        try:
            plan = build_rename_plan(owner_type)
        except Exception as e:
            print(f"❌ could not list {owner_type}s from the API: {e}", file=sys.stderr)
            return 1

        if not plan:
            print(f"ℹ️  {owner_type}: no slug/avatarImage mismatches found.", file=sys.stderr)
            continue

        for owner_id, old_slug, new_slug in plan:
            total_planned += 1
            if not args.apply:
                print(f"  {owner_type}/{old_slug} -> {new_slug}  (id={owner_id}, dry-run)")
                continue
            patch_path = f"/api/bots/{owner_id}" if owner_type == "bot" else f"/api/characters/{owner_id}"
            try:
                api(patch_path, payload={"slug": new_slug}, method="PATCH")
                print(f"✅ {owner_type}/{old_slug} -> {new_slug}  (id={owner_id})")
                total_applied += 1
            except urllib.error.HTTPError as e:
                msg = f"{owner_type}/{old_slug} -> {new_slug} (id={owner_id}): HTTP {e.code} {e.reason}"
                print(f"❌ {msg}", file=sys.stderr)
                errors.append(msg)

    print(json.dumps({
        "mode": "applied" if args.apply else "dry-run",
        "planned": total_planned,
        "applied": total_applied,
        "errors": len(errors),
    }))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
