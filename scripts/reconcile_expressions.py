#!/usr/bin/env python3
"""
reconcile_expressions.py — expression folders → ExpressionMedia rows (kind-robots/t-011)

The expression image folders in kind_robots are the source of truth for
pixels; the ExpressionMedia rows are the queryable index. This script
detects and repairs drift in ONE direction: folder → rows. It never
writes, moves, or deletes image files, never uses raw SQL, and never
creates ArtImage rows. Spec: projects/kind-robots/EXPRESSION-RECONCILE.md.

Scans (in a local kind_robots checkout, expected at ../kind_robots):
  public/images/bots/expressions/{slug}/
  public/images/characters/expressions/{slug}/

File convention (see kind_robots sample/generation/expressions.md):
  {key}_{nn}.webp       still; lowest nn (normally _01) is the promoted take
  {key}_loop.webp       looping reaction video for that key
  {from}_to_{to}.webp   transition clip (ExpressionTransition)

Actions:
  file without row                 → CREATE row (imagePath/videoPath only,
                                     designer 'reconcile-script')
  row imagePath ≠ convention path  → UPDATE imagePath (never message/label/
                                     emoticon/artPrompt — richer than a filename)
  row whose file is gone           → REPORT; --apply --deactivate soft-disables
  folder matching no bot/character → REPORT, never guess

Modes:
  (default)     dry-run: full report, no writes
  --apply       perform creates/updates via POST /api/bots/expressions
                (validated with the endpoint's dryRun:true first)
  --deactivate  with --apply: isActive:false on rows whose files are gone
  --check       exit 2 if any drift was found (CI usable)
  --owner SLUG  limit to one owner folder
  --type X      limit to 'bot' or 'character'
  --skip-transitions  don't upsert ExpressionTransition rows on --apply

Env:
  KR_API_TOKEN        required for --apply (admin or server key); reads are public
  KR_BASE_URL         default https://kindrobots.org
  KR_MEDIA_IMAGES_DIR self-hosted media share root (e.g. Windows relay's
                      Z:/kindrobots/images, see ops/home-server/SELF-HOSTED-MEDIA.md)
                      — checked first; expression images live here now that
                      Kind Robots media is served directly from the share
                      instead of the git tree
  KIND_ROBOTS_ROOT    fallback: a local kind_robots git checkout with
                      public/images/... still present; default
                      <conductor>/../kind_robots. Only used when
                      KR_MEDIA_IMAGES_DIR is unset.

Exit codes: 0 = ok / no drift, 1 = error, 2 = drift found (--check)
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KIND_ROBOTS_ROOT = Path(
    os.environ.get("KIND_ROBOTS_ROOT", REPO_ROOT.parent / "kind_robots")
)
KR_MEDIA_IMAGES_DIR = os.environ.get("KR_MEDIA_IMAGES_DIR", "").strip()
KR_BASE_URL = os.environ.get("KR_BASE_URL", "https://kindrobots.org").rstrip("/")
KR_API_TOKEN = os.environ.get("KR_API_TOKEN", "").strip()

EMOTION_KEYS = [
    "neutral", "joyful", "sorrowful", "afraid", "disgusted",
    "enraged", "surprised", "anxious", "proud", "loving",
]
ACTION_KEYS = [
    "laughing", "crying", "sleeping", "thinking", "shrugging",
    "winking", "facepalming", "cheering", "whispering", "shouting",
]
CANONICAL = {k: ("EMOTION", k.upper()) for k in EMOTION_KEYS}
CANONICAL.update({k: ("ACTION", k.upper()) for k in ACTION_KEYS})

OWNER_DIRS = {
    "bot": "public/images/bots/expressions",
    "character": "public/images/characters/expressions",
}

TRANSITION_RE = re.compile(r"^([a-z0-9][a-z0-9-]*)_to_([a-z0-9][a-z0-9-]*)$")
LOOP_RE = re.compile(r"^([a-z0-9][a-z0-9-]*)_loop$")
STILL_RE = re.compile(r"^([a-z0-9][a-z0-9-]*)_(\d+)$")


def api(path, payload=None, method=None, timeout=30):
    """GET/POST the kind_robots API. Returns parsed JSON or raises."""
    url = f"{KR_BASE_URL}{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method or ("POST" if data else "GET"))
    req.add_header("Content-Type", "application/json")
    if KR_API_TOKEN:
        req.add_header("Authorization", f"Bearer {KR_API_TOKEN}")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def fetch_owner_ids(owner_type):
    """slug -> id for all bots or characters — the FALLBACK for owners the
    narrator endpoint can't serve (inactive/private). Paginates defensively:
    the bots endpoint has historically ignored paging params (it read
    event.context.query), so stop as soon as a page adds nothing new; with
    the broken endpoint this map only covers the first 100 rows, which is
    why per-slug narrator lookup is the primary resolution path."""
    path = "/api/bots" if owner_type == "bot" else "/api/characters"
    ids, page = {}, 1
    while True:
        body = api(f"{path}?page={page}&pageSize=100")
        rows = body.get("data") or []
        if isinstance(rows, dict):
            rows = rows.get(f"{owner_type}s") or []
        before = len(ids)
        for row in rows:
            slug = (row.get("slug") or "").strip()
            if slug and row.get("id"):
                ids[slug] = row["id"]
        if len(ids) == before or len(rows) < 100:
            return ids
        page += 1


def fetch_avatar_slug_map(owner_type):
    """avatarImage-derived slug -> real DB slug, e.g. "brass-lampkeeper" ->
    "pip-the-lampkeeper". Expression folders are named after the owner's
    avatarImage filename (a short evocative descriptor picked when the art
    was made), which can drift from the owner's actual slug (auto-generated
    from its full display name at creation time, e.g. slugify("Pip the
    Lampkeeper")) -- confirmed 2026-07-26 (Silas: narrator endpoint 404s on
    "brass-lampkeeper", the real slug is "pip-the-lampkeeper"). Paginates
    the same defensively as fetch_owner_ids, off the same bulk list (prisma
    findMany returns every field including avatarImage, no extra query
    needed)."""
    path = "/api/bots" if owner_type == "bot" else "/api/characters"
    avatar_to_slug, seen_ids, page = {}, set(), 1
    while True:
        body = api(f"{path}?page={page}&pageSize=100")
        rows = body.get("data") or []
        if isinstance(rows, dict):
            rows = rows.get(f"{owner_type}s") or []
        before = len(seen_ids)
        for row in rows:
            if row.get("id"):
                seen_ids.add(row["id"])
            real_slug = (row.get("slug") or "").strip()
            avatar_image = (row.get("avatarImage") or "").strip()
            if not (real_slug and avatar_image):
                continue
            avatar_slug = Path(avatar_image).stem.strip().lower()
            if avatar_slug:
                avatar_to_slug[avatar_slug] = real_slug
        if len(seen_ids) == before or len(rows) < 100:
            return avatar_to_slug
        page += 1


def fetch_narrator(owner_type, slug):
    """(owner_id, {key: row}) via the narrator endpoint — a per-slug lookup
    that dodges list pagination entirely and returns the active rows in the
    same call. (None, None) when the owner isn't readable there (404 =
    inactive/private/unknown). NB: for characters the payload's `id` is the
    default narrator BOT id — the real id is sourceCharacterId."""
    try:
        body = api(f"/api/narrators/{owner_type}/{slug}")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None, None
        raise
    data = body.get("data") or {}
    owner_id = data.get("sourceCharacterId") if owner_type == "character" else data.get("id")
    rows = data.get("ExpressionMedia") or []
    return owner_id, {r["expressionKey"]: r for r in rows if r.get("expressionKey")}


def scan_folder(folder):
    """One owner folder -> {stills: {key: filename}, loops: {key: filename},
    transitions: [(from,to,filename)], unrecognized: [filename]}.
    Promoted still per key = lowest numbered take."""
    out = {"stills": {}, "loops": {}, "transitions": [], "unrecognized": []}
    takes = {}
    for f in sorted(folder.iterdir()):
        if not f.is_file() or f.suffix.lower() not in (".webp", ".mp4"):
            continue
        stem = f.stem.lower()
        m = TRANSITION_RE.match(stem)
        if m:
            out["transitions"].append((m.group(1), m.group(2), f.name))
            continue
        m = LOOP_RE.match(stem)
        if m:
            out["loops"][m.group(1)] = f.name
            continue
        m = STILL_RE.match(stem)
        if m and f.suffix.lower() == ".webp":
            takes.setdefault(m.group(1), []).append((int(m.group(2)), f.name))
            continue
        out["unrecognized"].append(f.name)
    for key, versions in takes.items():
        out["stills"][key] = min(versions)[1]
    return out


def key_identity(key):
    """(kind, expression enum value) for a key; customs are CUSTOM actions."""
    return CANONICAL.get(key, ("ACTION", "CUSTOM"))


def public_path(owner_type, slug, filename):
    return f"/{OWNER_DIRS[owner_type].removeprefix('public/')}/{slug}/{filename}"


def plan_owner(owner_type, slug, owner_id, scanned, existing):
    """Diff one owner's folder against its rows. Returns (creates, updates,
    missing, notes) where creates/updates are API-ready row payloads."""
    creates, updates, missing, notes = [], [], [], []
    owner_field = "botId" if owner_type == "bot" else "characterId"

    for key, filename in scanned["stills"].items():
        kind, expression = key_identity(key)
        want_image = public_path(owner_type, slug, filename)
        want_video = (
            public_path(owner_type, slug, scanned["loops"][key])
            if key in scanned["loops"] else None
        )
        row = {
            owner_field: owner_id,
            "expressionKey": key,
            "expression": expression,
            "kind": kind,
            "imagePath": want_image,
        }
        if want_video:
            row["videoPath"] = want_video

        if existing is None or key not in existing:
            if existing is None:
                notes.append(f"{key}: owner rows unreadable — upserting minimal row blind")
            row["designer"] = "reconcile-script"
            creates.append(row)
        else:
            have = existing[key]
            drift = have.get("imagePath") != want_image or (
                want_video and have.get("videoPath") != want_video
            )
            if drift:
                updates.append(row)  # minimal fields only: metadata untouched

    # Loops whose key has no still: report, don't invent a row.
    for key in scanned["loops"]:
        if key not in scanned["stills"]:
            notes.append(f"{key}: loop video with no still — skipped")

    # Rows whose file is gone (only judgeable when rows were readable).
    if existing is not None:
        for key, row in existing.items():
            if key not in scanned["stills"]:
                kind, expression = key_identity(key)
                missing.append({
                    owner_field: owner_id,
                    "expressionKey": key,
                    "expression": row.get("expression") or expression,
                    "kind": row.get("kind") or kind,
                    "isActive": False,
                })
    return creates, updates, missing, notes


def post_batch(path, rows, list_key):
    """dryRun-validate then write one batch (≤100 rows per call)."""
    for i in range(0, len(rows), 100):
        chunk = rows[i:i + 100]
        api(path, {"dryRun": True, list_key: chunk})
        api(path, {list_key: chunk})


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--apply", action="store_true", help="perform creates/updates")
    ap.add_argument("--deactivate", action="store_true",
                    help="with --apply: isActive=false on rows whose files are gone")
    ap.add_argument("--check", action="store_true", help="exit 2 if drift found")
    ap.add_argument("--owner", help="limit to one owner slug")
    ap.add_argument("--type", choices=("bot", "character"), help="limit owner type")
    ap.add_argument("--skip-transitions", action="store_true",
                    help="don't upsert ExpressionTransition rows on --apply")
    args = ap.parse_args()

    if args.apply and not KR_API_TOKEN:
        print("❌ --apply requires KR_API_TOKEN (admin or server key).", file=sys.stderr)
        return 1
    if KR_MEDIA_IMAGES_DIR:
        images_root = Path(KR_MEDIA_IMAGES_DIR)
        if not images_root.is_dir():
            print(f"❌ KR_MEDIA_IMAGES_DIR set but not found: {images_root}",
                  file=sys.stderr)
            return 1
    else:
        images_root = None
        if not KIND_ROBOTS_ROOT.is_dir():
            print(f"❌ kind_robots checkout not found at {KIND_ROBOTS_ROOT} "
                  "(set KIND_ROBOTS_ROOT, or set KR_MEDIA_IMAGES_DIR to the "
                  "self-hosted media share root instead).", file=sys.stderr)
            return 1

    totals = {"create": 0, "update": 0, "missing": 0, "transitions": 0,
              "unmatched": 0, "unrecognized": 0}
    all_creates, all_updates, all_missing, all_transitions = [], [], [], []

    for owner_type, rel in OWNER_DIRS.items():
        if args.type and owner_type != args.type:
            continue
        if images_root is not None:
            base = images_root / rel.removeprefix("public/images/")
        else:
            base = KIND_ROBOTS_ROOT / rel
        if not base.is_dir():
            print(f"ℹ️  no {owner_type} expressions dir ({base}) — skipping.", file=sys.stderr)
            continue

        owner_ids = None  # fetched lazily, only if some narrator lookup 404s
        avatar_map = None  # fetched lazily, only if slug AND avatar-map fallback both needed

        for folder in sorted(p for p in base.iterdir() if p.is_dir()):
            slug = folder.name
            if args.owner and slug != args.owner:
                continue
            scanned = scan_folder(folder)
            for name in scanned["unrecognized"]:
                totals["unrecognized"] += 1
                print(f"⚠️  {owner_type}/{slug}: unrecognized file {name}", file=sys.stderr)

            # Primary: per-slug narrator lookup (id + rows in one call).
            try:
                owner_id, existing = fetch_narrator(owner_type, slug)
            except Exception as e:
                print(f"⚠️  {owner_type}/{slug}: narrator lookup failed ({e}) — "
                      "falling back to list", file=sys.stderr)
                owner_id, existing = None, None

            # Fallback: folder names follow the owner's avatarImage-derived
            # descriptor (e.g. "brass-lampkeeper"), which can differ from
            # its real DB slug (auto-generated from the full display name,
            # e.g. "pip-the-lampkeeper"). Resolve through that mapping and
            # retry the narrator lookup under the real slug before settling
            # for the degraded bulk-list path below.
            real_slug = None
            if not owner_id:
                if avatar_map is None:
                    try:
                        avatar_map = fetch_avatar_slug_map(owner_type)
                    except Exception as e:
                        print(f"⚠️  {owner_type}/{slug}: avatar-slug map fetch failed "
                              f"({e}) — skipping that fallback", file=sys.stderr)
                        avatar_map = {}
                real_slug = avatar_map.get(slug.lower())
                if real_slug and real_slug != slug:
                    try:
                        owner_id, existing = fetch_narrator(owner_type, real_slug)
                    except Exception:
                        owner_id, existing = None, None
                    if owner_id:
                        print(f"ℹ️  {owner_type}/{slug}: resolved via avatarImage to "
                              f"slug '{real_slug}'", file=sys.stderr)

            # Last resort: bulk list, for inactive/private owners (rows unknown).
            if not owner_id:
                if owner_ids is None:
                    try:
                        owner_ids = fetch_owner_ids(owner_type)
                    except Exception as e:
                        print(f"❌ could not list {owner_type}s from the API: {e}",
                              file=sys.stderr)
                        return 1
                owner_id = owner_ids.get(real_slug or slug)
                existing = None

            if not owner_id:
                totals["unmatched"] += 1
                print(f"⚠️  {owner_type}/{slug}: folder matches no {owner_type} slug — skipped",
                      file=sys.stderr)
                continue

            creates, updates, missing, notes = plan_owner(
                owner_type, slug, owner_id, scanned, existing)
            for n in notes:
                print(f"ℹ️  {owner_type}/{slug}: {n}", file=sys.stderr)

            owner_field = "botId" if owner_type == "bot" else "characterId"
            for frm, to, filename in scanned["transitions"]:
                all_transitions.append({
                    owner_field: owner_id, "fromKey": frm, "toKey": to,
                    "videoPath": public_path(owner_type, slug, filename),
                })

            all_creates += creates
            all_updates += updates
            all_missing += missing
            totals["create"] += len(creates)
            totals["update"] += len(updates)
            totals["missing"] += len(missing)
            if creates or updates or missing:
                print(f"   {owner_type}/{slug}: +{len(creates)} create, "
                      f"~{len(updates)} update, {len(missing)} missing-file", file=sys.stderr)

    totals["transitions"] = len(all_transitions)
    drift = totals["create"] + totals["update"] + totals["missing"]

    if args.apply:
        try:
            if all_creates or all_updates:
                post_batch("/api/bots/expressions", all_creates + all_updates, "expressions")
            if all_missing and args.deactivate:
                post_batch("/api/bots/expressions", all_missing, "expressions")
            if all_transitions and not args.skip_transitions:
                post_batch("/api/bots/transitions", all_transitions, "transitions")
        except urllib.error.HTTPError as e:
            print(f"❌ API rejected a batch: {e.code} {e.read().decode(errors='replace')[:500]}",
                  file=sys.stderr)
            return 1
        applied = "applied"
    else:
        applied = "dry-run (use --apply to write)"

    print(json.dumps({"mode": applied, **totals}, indent=2))
    deactivate_note = "" if (args.deactivate or not totals["missing"]) else \
        " (missing-file rows reported only; --apply --deactivate to soft-disable)"
    print(f"{'✅' if not drift else '🔁'} {drift} drifted row(s), "
          f"{totals['transitions']} transition file(s){deactivate_note}", file=sys.stderr)

    if args.check and drift:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
