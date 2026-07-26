#!/usr/bin/env python3
"""
rename_bot_slugs_to_folder.py — make each bot's slug match its actual
expression-image folder name (kind-robots/t-011 follow-up).

Root cause this closes: narrator bots got their DB `slug` auto-generated
from their full display name (e.g. "Pip the Lampkeeper" -> slug
"pip-the-lampkeeper") independently of the expression-image folder they
were actually organized under ("brass-lampkeeper/"). Two names for the
same bot, in two different places, with nothing keeping them in sync --
exactly the "bandaid" pattern Silas flagged after reconcile_expressions.py
needed a whole extra fallback-matching tier just to bridge them.

Correction from an earlier version of this script (2026-07-26, Silas):
that version derived the new slug from each bot's `avatarImage` field.
Silas: "AvatarImages were rough draft titles that we ran with... we should
derive from the folder names in expressions as those were the final
drafts." avatarImage can be stale (a rough-draft name superseded later);
the actual expression folder on the media share is the current, final
ground truth. This version walks those real folders directly (same
KR_MEDIA_IMAGES_DIR / KIND_ROBOTS_ROOT env vars, same directory layout as
reconcile_expressions.py) instead of trusting avatarImage as the source of
the new name -- avatarImage/fetch_avatar_slug_map is still used as ONE WAY
to figure out *which* owner a folder belongs to (necessary since that's
exactly the mismatch being fixed), never as the value written back.

Once run, slug == folder name for every bot with an expression folder, so
reconcile_expressions.py's direct narrator-by-folder-slug lookup succeeds
on the first try and its avatarImage-fallback tier becomes a dormant
safety net rather than something load-bearing.

Env:
  KR_API_TOKEN        required for --apply (admin or server key); reads are public
  KR_BASE_URL         default https://kind-robots.vercel.app
  KR_MEDIA_IMAGES_DIR self-hosted media share root (e.g. Z:/kindrobots/images)
                      -- checked first, same as reconcile_expressions.py
  KIND_ROBOTS_ROOT    fallback: a local kind_robots git checkout with
                      public/images/... still present; only used when
                      KR_MEDIA_IMAGES_DIR is unset

Usage:
  python scripts/rename_bot_slugs_to_folder.py             # dry-run plan
  python scripts/rename_bot_slugs_to_folder.py --apply     # perform renames
  python scripts/rename_bot_slugs_to_folder.py --type bot  # limit owner type

Exit codes: 0 = ok (plan or apply succeeded), 1 = error
"""
import argparse
import json
import sys
import urllib.error
from pathlib import Path

# Allow `python scripts/rename_bot_slugs_to_folder.py` (sys.path[0] ==
# scripts/) as well as `import scripts.rename_bot_slugs_to_folder` / tests
# (repo root on sys.path) -- same shim as scripts/select_role.py.
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import scripts.reconcile_expressions as rex

OWNER_DIRS = rex.OWNER_DIRS


def resolve_folder_owner(owner_type, folder_slug, owner_ids_cache, avatar_map_cache):
    """(owner_id, current_slug) for a single expression folder, reusing
    reconcile_expressions.py's own three-tier resolution (direct
    narrator-by-folder-slug, avatarImage fallback, bulk-list fallback) so
    this script and the reconciler never disagree about who owns a folder.
    Returns (None, None) if unresolvable -- left for reconcile_expressions.py's
    own "folder matches no {type} slug" reporting, not duplicated here."""
    try:
        owner_id, _ = rex.fetch_narrator(owner_type, folder_slug)
    except Exception:
        owner_id = None
    if owner_id:
        return owner_id, folder_slug

    if avatar_map_cache["map"] is None:
        try:
            avatar_map_cache["map"] = rex.fetch_avatar_slug_map(owner_type)
        except Exception:
            avatar_map_cache["map"] = {}
    real_slug = avatar_map_cache["map"].get(folder_slug.lower())
    if real_slug and real_slug != folder_slug:
        try:
            owner_id, _ = rex.fetch_narrator(owner_type, real_slug)
        except Exception:
            owner_id = None
        if owner_id:
            return owner_id, real_slug

    if owner_ids_cache["map"] is None:
        try:
            owner_ids_cache["map"] = rex.fetch_owner_ids(owner_type)
        except Exception:
            owner_ids_cache["map"] = {}
    lookup_slug = real_slug or folder_slug
    owner_id = owner_ids_cache["map"].get(lookup_slug)
    if owner_id:
        return owner_id, lookup_slug

    return None, None


def build_rename_plan(owner_type, base_dir):
    """[(owner_id, current_slug, folder_name), ...] for every expression
    folder whose owner's current slug doesn't already match the folder
    name. Folders that can't be resolved to any owner are skipped here --
    that's reconcile_expressions.py's job to report, not this script's."""
    plan = []
    owner_ids_cache = {"map": None}
    avatar_map_cache = {"map": None}
    for folder in sorted(p for p in base_dir.iterdir() if p.is_dir()):
        folder_slug = folder.name
        owner_id, current_slug = resolve_folder_owner(
            owner_type, folder_slug, owner_ids_cache, avatar_map_cache)
        if owner_id and current_slug != folder_slug:
            plan.append((owner_id, current_slug, folder_slug))
    return plan


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--apply", action="store_true", help="perform the renames")
    ap.add_argument("--type", choices=("bot", "character"), help="limit owner type")
    args = ap.parse_args()

    if args.apply and not rex.KR_API_TOKEN:
        print("❌ --apply requires KR_API_TOKEN (admin or server key).", file=sys.stderr)
        return 1

    if rex.KR_MEDIA_IMAGES_DIR:
        images_root = Path(rex.KR_MEDIA_IMAGES_DIR)
        if not images_root.is_dir():
            print(f"❌ KR_MEDIA_IMAGES_DIR set but not found: {images_root}", file=sys.stderr)
            return 1
    else:
        images_root = None
        if not rex.KIND_ROBOTS_ROOT.is_dir():
            print(f"❌ kind_robots checkout not found at {rex.KIND_ROBOTS_ROOT} "
                  "(set KIND_ROBOTS_ROOT, or set KR_MEDIA_IMAGES_DIR to the "
                  "self-hosted media share root instead).", file=sys.stderr)
            return 1

    owner_types = [args.type] if args.type else ["bot", "character"]
    total_planned = 0
    total_applied = 0
    errors = []

    for owner_type in owner_types:
        rel = OWNER_DIRS[owner_type]
        base_dir = (images_root / rel.removeprefix("public/images/")
                    if images_root is not None else rex.KIND_ROBOTS_ROOT / rel)
        if not base_dir.is_dir():
            print(f"ℹ️  no {owner_type} expressions dir ({base_dir}) — skipping.", file=sys.stderr)
            continue

        try:
            plan = build_rename_plan(owner_type, base_dir)
        except Exception as e:
            print(f"❌ could not build rename plan for {owner_type}s: {e}", file=sys.stderr)
            return 1

        if not plan:
            print(f"ℹ️  {owner_type}: no slug/folder-name mismatches found.", file=sys.stderr)
            continue

        for owner_id, current_slug, folder_name in plan:
            total_planned += 1
            if not args.apply:
                print(f"  {owner_type}/{current_slug} -> {folder_name}  (id={owner_id}, dry-run)")
                continue
            patch_path = f"/api/bots/{owner_id}" if owner_type == "bot" else f"/api/characters/{owner_id}"
            try:
                rex.api(patch_path, payload={"slug": folder_name}, method="PATCH")
                print(f"✅ {owner_type}/{current_slug} -> {folder_name}  (id={owner_id})")
                total_applied += 1
            except urllib.error.HTTPError as e:
                msg = f"{owner_type}/{current_slug} -> {folder_name} (id={owner_id}): HTTP {e.code} {e.reason}"
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
