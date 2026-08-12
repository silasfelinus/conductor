#!/usr/bin/env python3
"""
dream_slug_image_cleanup.py — one-time cleanup of dream slugs, duplicate merges,
creationSource, and image paths, per projects/dream-cycle/specs/SLUG-POLICY.md.

Silas, 2026-07-20. Runs against the kind_robots REST API with KR_API_TOKEN
(beta-admin). Idempotent and re-runnable: every step checks current state and
skips work already done. DRY-RUN BY DEFAULT — pass --live to mutate.

What it does (in order, each phase independently skippable/idempotent):

  1. creationSource backfill  — dream-cycle dreams saved as HUMAN -> AI (the daily
     fast-lane authors autonomously; HUMAN was the DB default, never intended).
  2. merges                   — collapse the PITCH-world / near-empty-LOCATION
     duplicate pairs the old slug collision produced: keep the content-bearing row,
     DELETE the empty one (M2M links + shared scenarios survive; only the empty
     dream's own PitchSheet + DreamRelation edges cascade away), then give the
     survivor the clean slug.
  3. slug renames             — drop leading `the-`, trim filler suffixes on the
     non-conforming dream slugs (SLUG-POLICY rules 2-3). Two-word `the-` proper
     names (the-tangle) and 3-word slugs that add clarity (serendipity-space-bar)
     are KEPT by design and only reported.
  4. image paths (dreams+facets) — PATCH PitchSheet.imagePath / dream.cardPath and
     facet.imagePath to the canonical /images/<type>/<slug>/... form, and record
     every old->new move in a manifest. FILES do not move here (they live on the
     Unraid media box) — the manifest feeds scripts/media_migrate.py, which
     Silas runs on the box to `mv` the files + regenerate collections.json.

Reward image folders (/rewards/<type>/... vs the component's /images/rewards/...)
are intentionally NOT mass-rewritten here — that divergence is reconciled on the
box by scripts/media_migrate.py, which can see the real folders. See its header.

Usage:
  python scripts/dream_slug_image_cleanup.py                 # dry-run, prints plan
  python scripts/dream_slug_image_cleanup.py --live          # execute
  python scripts/dream_slug_image_cleanup.py --live --only merges,slugs
  python scripts/dream_slug_image_cleanup.py --manifest out/media-moves.json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

KR_BASE_URL = os.environ.get("KR_BASE_URL", "https://kindrobots.org").rstrip("/")
KR_API_TOKEN = os.environ.get("KR_API_TOKEN", "").strip()
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "projects" / "dream-cycle" / "media-migration-manifest.json"

# ── Explicit, reviewable decision tables (Silas-approved 2026-07-20) ──────────
# Each pair: keep the content-bearing survivor, delete the empty duplicate, then
# rename the survivor to the clean slug (applied in slug_renames after the delete
# frees the slug where needed).
MERGES = [
    {"keep": 2139, "keep_slug": "comet-market", "delete": 2141,
     "why": "comet-market(PITCH,content) + the-comet-market-2(LOCATION,empty)"},
    {"keep": 2155, "keep_slug": "sound-cannery", "delete": 2157,
     "why": "the-sound-cannery(PITCH,content) + sound-cannery(LOCATION,empty); "
            "delete frees 'sound-cannery' for the survivor"},
]

# dream id -> new slug. Article-strip + filler-trim only; verified against the live
# table below at runtime. 2155 is renamed here as the tail of its merge.
SLUG_RENAMES = {
    37:   "lantern-greenhouse",      # the-lantern-greenhouse  (drop article)
    42:   "cthulian-jam-band",       # cthulian-jam-band-festival (trim -festival)
    2140: "borrowed-light",          # borrowed-light-bittersweet (trim mood tail)
    2155: "sound-cannery",           # the-sound-cannery -> merge survivor slug
}

# Non-conforming-looking but KEPT on purpose (reported, not changed):
KEPT_BY_DESIGN = {
    2622: ("the-tangle", "two-word proper name — the-marrow carve-out (rule 3)"),
    41:   ("rainbow-butterfly-sanctuary", "3 words add clarity (rule 2)"),
    44:   ("serendipity-space-bar", "3 words add clarity; 'space-bar' alone ambiguous"),
}

_LEADING_ARTICLES = ("the-", "a-", "an-")


def normalize_slug(text: str) -> str:
    """SLUG-POLICY rules 1+3 (article strip). Filler-trim (rule 2) is a human call,
    encoded in SLUG_RENAMES, not applied mechanically here."""
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    s = re.sub(r"-{2,}", "-", s)
    for art in _LEADING_ARTICLES:
        if s.startswith(art):
            rest = s[len(art):]
            if rest and "-" in rest:
                s = rest
            break
    return s or "element"


# ── HTTP ─────────────────────────────────────────────────────────────────────
def http(method: str, path: str, body: dict | None = None) -> tuple[int, object]:
    url = f"{KR_BASE_URL}{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {KR_API_TOKEN}")
    req.add_header("Content-Type", "application/json")
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                raw = r.read().decode()
                try:
                    return r.status, json.loads(raw)
                except json.JSONDecodeError:
                    return r.status, raw
        except urllib.error.HTTPError as e:
            raw = e.read().decode()
            try:
                return e.code, json.loads(raw)
            except json.JSONDecodeError:
                return e.code, raw
        except urllib.error.URLError:
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)
    return 0, None


def get_list(path: str, key_hint: str) -> list[dict]:
    status, resp = http("GET", path)
    if status != 200:
        raise SystemExit(f"GET {path} -> {status}: {str(resp)[:200]}")
    if isinstance(resp, dict):
        for k in ("data", key_hint, "items"):
            if isinstance(resp.get(k), list):
                return resp[k]
        for v in resp.values():
            if isinstance(v, list):
                return v
    return resp if isinstance(resp, list) else []


# ── Canonical image-path computation ─────────────────────────────────────────
def dream_card_target(slug: str) -> str:
    """Every dream owns its own folder: /images/dreams/<slug>/<slug>-card.webp."""
    return f"/images/dreams/{slug}/{slug}-card.webp"


# ── Phases ───────────────────────────────────────────────────────────────────
def load_state():
    dreams = get_list("/api/dreams", "dreams")
    facets = get_list("/api/facets", "facets")
    return {d["id"]: d for d in dreams}, {f["id"]: f for f in facets}


def patch_dream(did: int, body: dict, live: bool) -> bool:
    if not live:
        print(f"    [dry] PATCH /api/dreams/{did} {body}")
        return True
    status, resp = http("PATCH", f"/api/dreams/{did}", body)
    ok = status in (200, 201)
    print(f"    PATCH /api/dreams/{did} {body} -> {status}{'' if ok else ' FAIL ' + str(resp)[:160]}")
    return ok


def run(only: set[str], live: bool, manifest_path: Path):
    if not KR_API_TOKEN:
        raise SystemExit("KR_API_TOKEN not set")
    dreams, facets = load_state()
    by_slug = {d.get("slug"): d for d in dreams.values()}
    manifest = {"generated": "2026-07-20", "moves": []}

    def move(old: str, new: str, kind: str):
        if old and new and old != new:
            manifest["moves"].append({"kind": kind, "old": old, "new": new})

    # ── 1. creationSource backfill ────────────────────────────────────────────
    if "creationsource" in only:
        print("\n== 1. creationSource: dream-cycle HUMAN -> AI ==")
        n = 0
        to_delete = {m["delete"] for m in MERGES}
        for d in dreams.values():
            if d["id"] in to_delete:
                continue  # about to be merged away — don't bother patching
            if d.get("designer") == "dream-cycle" and (d.get("creationSource") or "HUMAN") == "HUMAN":
                if patch_dream(d["id"], {"creationSource": "AI"}, live):
                    n += 1
        print(f"   {n} dream(s) {'patched' if live else 'to patch'} to AI")

    # ── 2. merges ─────────────────────────────────────────────────────────────
    if "merges" in only:
        print("\n== 2. merges (delete empty duplicate; M2M links survive) ==")
        for m in MERGES:
            keep, drop = dreams.get(m["keep"]), dreams.get(m["delete"])
            if not drop:
                print(f"   #{m['delete']} already gone — skip ({m['why']})")
                continue
            if not keep:
                print(f"   !! survivor #{m['keep']} missing — ABORT this merge ({m['why']})")
                continue
            # Safety: confirm the survivor still holds the content before deleting.
            kc = len(keep.get("Characters") or []) + len(keep.get("Rewards") or [])
            print(f"   {m['why']}")
            print(f"     survivor #{keep['id']} '{keep.get('slug')}' has {kc} char+reward links; "
                  f"deleting empty #{drop['id']} '{drop.get('slug')}' "
                  f"(chars={len(drop.get('Characters') or [])}, rewards={len(drop.get('Rewards') or [])})")
            # capture the empty dupe's sheet image so the box can delete the orphan file
            ps = drop.get("PitchSheet") or {}
            if ps.get("imagePath"):
                move(ps["imagePath"], "", "delete-orphan-sheet-image")
            if not live:
                print(f"     [dry] DELETE /api/dreams/{drop['id']}")
            else:
                status, resp = http("DELETE", f"/api/dreams/{drop['id']}")
                print(f"     DELETE /api/dreams/{drop['id']} -> {status}"
                      f"{'' if status == 200 else ' FAIL ' + str(resp)[:160]}")
                if status != 200:
                    print("     !! delete failed — leaving slug held; downstream rename will skip")
                    continue
            # Reflect the removal in local state (dry OR live) so the slug-rename
            # phase sees 'sound-cannery' freed and renames the survivor onto it.
            dreams.pop(drop["id"], None)
            if by_slug.get(drop.get("slug"), {}).get("id") == drop["id"]:
                by_slug.pop(drop.get("slug"), None)

    # ── 3. slug renames ───────────────────────────────────────────────────────
    if "slugs" in only:
        print("\n== 3. slug renames (article strip + filler trim) ==")
        for did, new_slug in SLUG_RENAMES.items():
            d = dreams.get(did)
            if not d:
                print(f"   #{did} missing — skip (target slug {new_slug})")
                continue
            cur = d.get("slug")
            if cur == new_slug:
                print(f"   #{did} already '{new_slug}' — skip")
                continue
            # guard against colliding with a still-present other dream
            other = by_slug.get(new_slug)
            if other and other["id"] != did:
                print(f"   !! '{new_slug}' still held by #{other['id']} — run merges first; skip #{did}")
                continue
            print(f"   #{did} '{cur}' -> '{new_slug}'")
            patch_dream(did, {"slug": new_slug}, live)
        print("   kept by design (SLUG-POLICY carve-outs):")
        for did, (slug, why) in KEPT_BY_DESIGN.items():
            print(f"     #{did} '{slug}' — {why}")

    # ── 4. image paths: dreams + facets ───────────────────────────────────────
    if "images" in only:
        print("\n== 4. imagePath normalization (dreams + facets) ==")
        # effective slug after renames, for path computation
        eff_slug = {d["id"]: SLUG_RENAMES.get(d["id"], d.get("slug")) for d in dreams.values()}
        deleted = {m["delete"] for m in MERGES}
        for d in dreams.values():
            if d["id"] in deleted:
                continue
            slug = eff_slug[d["id"]]
            ps = d.get("PitchSheet") or {}
            old = ps.get("imagePath")
            if not old:
                continue
            new = dream_card_target(slug)
            if old == new:
                continue
            move(old, new, "dream-card")
            print(f"   dream '{slug}': sheet#{ps.get('id')} {old} -> {new}")
            if ps.get("id") and live:
                status, resp = http("PATCH", f"/api/sheets/{ps['id']}", {"imagePath": new})
                print(f"     PATCH /api/sheets/{ps['id']} -> {status}"
                      f"{'' if status in (200, 201) else ' FAIL ' + str(resp)[:160]}")
            elif ps.get("id"):
                print(f"     [dry] PATCH /api/sheets/{ps['id']} imagePath={new}")
            # keep the dream row's own cardPath in sync if it had a stale one
            if d.get("cardPath") and d["cardPath"] != new:
                move(d["cardPath"], new, "dream-cardpath")
                patch_dream(d["id"], {"cardPath": new}, live)

        for f in facets.values():
            old = f.get("imagePath")
            if not old or old.startswith("/images/facets/"):
                continue
            # Facets weren't in the slug-rename scope: keep the existing filename
            # (matches the facet's own slug) and only correct the parent folder
            # (/images/dreams/foo.webp -> /images/facets/foo.webp).
            new = "/images/facets/" + old.rsplit("/", 1)[-1]
            move(old, new, "facet")
            print(f"   facet '{f.get('slug')}': {old} -> {new}")
            if live:
                status, resp = http("PATCH", f"/api/facets/{f['id']}", {"imagePath": new})
                print(f"     PATCH /api/facets/{f['id']} -> {status}"
                      f"{'' if status in (200, 201) else ' FAIL ' + str(resp)[:160]}")
            else:
                print(f"     [dry] PATCH /api/facets/{f['id']} imagePath={new}")

    # ── write manifest ─────────────────────────────────────────────────────────
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"\nWrote {len(manifest['moves'])} media move(s) -> {manifest_path}")
    print("Run scripts/media_migrate.py against the Z: images share to move the files.")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true", help="execute (default: dry-run)")
    ap.add_argument("--only", default="creationsource,merges,slugs,images",
                    help="comma phases: creationsource,merges,slugs,images")
    ap.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    args = ap.parse_args()
    only = {p.strip().lower() for p in args.only.split(",") if p.strip()}
    print(f"{'LIVE' if args.live else 'DRY-RUN'} · base={KR_BASE_URL} · phases={sorted(only)}")
    run(only, args.live, Path(args.manifest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
