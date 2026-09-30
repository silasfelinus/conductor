#!/usr/bin/env python3
"""Link Cthulhuquarium fish plates to Monster rows through the admin HTTPS API.

cthulhuquarium/t-076. No DATABASE_URL needed: uses KR_API_TOKEN against
POST /api/art/image and PATCH /api/monsters/:slug (iconPath/cardPath/artImageId).
Dry-run by default; pass --write to change anything. Idempotent: a Monster that
already has artImageId and both paths is skipped. Requires the kind_robots deploy
that ships public/images/cthulhuquarium/ and the PATCH path fields (PR #3139).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ART_DIR = Path(__file__).resolve().parent.parent / "projects/cthulhuquarium/art"
PREFIX = "cthulhuquarium-fish-"
PUBLIC = "/images/cthulhuquarium/"


def call(base, token, method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        f"{base.rstrip('/')}{path}", data=data, method=method,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json",
                 "Content-Type": "application/json", "User-Agent": "conductor-cthulhu-link/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            parsed = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{method} {path} -> HTTP {e.code}: {e.read().decode(errors='replace')[:300]}")
    if not parsed.get("success"):
        raise RuntimeError(f"{method} {path} rejected: {parsed.get('message')}")
    return parsed.get("data")


def plates():
    out = []
    for p in sorted(ART_DIR.glob(f"{PREFIX}*.webp")):
        out.append((p.name[len(PREFIX):-len(".webp")], p.name))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--base", default=os.environ.get("KR_API_BASE", "https://kindrobots.org"))
    args = ap.parse_args(argv)
    token = os.environ.get("KR_API_TOKEN", "").strip()
    if not token:
        print("KR_API_TOKEN is required", file=sys.stderr)
        return 2
    summary = dict(plates=0, linked=0, skipped=0, missing=[], failed=[])
    todo = []
    for slug, fn in plates():
        summary["plates"] += 1
        try:
            m = call(args.base, token, "GET", f"/api/monsters/{slug}")
        except RuntimeError as e:
            summary["missing"].append(slug)
            print(f"missing/err {slug}: {e}")
            continue
        if m.get("artImageId") and m.get("iconPath") and m.get("cardPath"):
            summary["skipped"] += 1
            continue
        todo.append((slug, fn, m))
    if summary["missing"]:
        print("summary: " + json.dumps(summary))
        print("refusing to write: some plates have no Monster row", file=sys.stderr)
        return 1
    for slug, fn, m in todo:
        if not args.write:
            summary["linked"] += 1
            continue
        try:
            art_id = m.get("artImageId")
            if not art_id:
                img = call(args.base, token, "POST", "/api/art/image", {
                    "fileName": fn, "fileType": "webp", "imagePath": PUBLIC + fn, "path": PUBLIC + fn,
                    "isPublic": True, "isMature": False, "isActive": True,
                    "promptString": f"Cthulhuquarium species plate: {slug}"})
                art_id = img["id"]
            call(args.base, token, "PATCH", f"/api/monsters/{slug}",
                 {"artImageId": art_id, "iconPath": PUBLIC + fn, "cardPath": PUBLIC + fn})
            summary["linked"] += 1
        except RuntimeError as e:
            summary["failed"].append(slug)
            print(f"failed {slug}: {e}")
    print(("write" if args.write else "dry-run") + " summary: " + json.dumps(summary))
    return 1 if summary["failed"] else 0


if __name__ == "__main__":
    sys.exit(main())
