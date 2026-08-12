#!/usr/bin/env python3
"""
parity_migrate.py — reverse-parity migration for the kind_robots art library.

Runs ON the home box (needs disk access to the local kind_robots checkout AND
outbound HTTPS to kind_robots). It closes the gaps the Vercel side can't: it
writes real files, converts PNG->WebP, and generates thumbnails, then patches
the DB over the KR API. Work is pulled from GET /api/art/image/needs-work so we
never download every row's base64 up front.

Three independent passes (default: all three):
  --materialize  imageData-only rows -> write a .webp on disk, PATCH imagePath.
                 Deduped: if the exact bytes already exist on disk, link that
                 file instead of writing a copy.
  --png2webp     existing .png files -> .webp; delete the png; PATCH the row;
                 rewrite refs in collections.json / gallery.json; REPORT any
                 code refs (never auto-edits source).
  --thumbnails   rows with no thumbnail -> write a thumb .webp + PATCH
                 thumbnailPath and thumbnailData.

SAFE BY DEFAULT: dry-run unless you pass --live. Dry-run makes zero changes; it
reports exactly what --live would do (materialize even reports true-new vs
duplicate-of-existing-file).

Environment (same token model as relay_agent.py):
  KR_BASE_URL          default https://kindrobots.org
  KR_RELAY_TOKEN       admin apiKey / beta-admin token (Bearer)
  KR_LOCAL_IMAGES_DIR  the local checkout's public/images dir (e.g.
                       D:/code/kind_robots/public/images)
Pillow is required for --live (image conversion/thumbnails); dry-run runs
stdlib-only.

Examples:
  python parity_migrate.py                          # dry-run, all passes
  python parity_migrate.py --png2webp               # dry-run, just PNG->WebP
  python parity_migrate.py --materialize --live     # actually write files
"""

import argparse
import base64
import hashlib
import io
import json
import os
import sys
import urllib.error
import urllib.request

# Default to the Vercel origin: the kindrobots.org domain sits behind Cloudflare,
# which 403s/404s these API routes. Override with KR_BASE_URL if needed.
KR_BASE_URL = os.environ.get("KR_BASE_URL", "https://kindrobots.org").rstrip("/")
KR_TOKEN = os.environ.get("KR_RELAY_TOKEN", "").strip()
IMAGES_DIR = os.environ.get("KR_LOCAL_IMAGES_DIR", "").strip().replace("\\", "/").rstrip("/")

THUMB_MAX = 384  # px, longest edge


def log(msg):
    print(msg, flush=True)


def http_json(method, url, body=None, timeout=120):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    if KR_TOKEN:
        req.add_header("Authorization", f"Bearer {KR_TOKEN}")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode() or "null")
    except urllib.error.HTTPError as e:
        try:
            payload = json.loads(e.read().decode() or "null")
        except (ValueError, OSError):
            payload = None
        return e.code, payload


# ---- path helpers --------------------------------------------------------

def url_to_local(url):
    """/images/comfy/x.webp -> {IMAGES_DIR}/comfy/x.webp"""
    if not url:
        return None
    rel = url.split("?")[0].lstrip("/")
    if rel.startswith("images/"):
        rel = rel[len("images/"):]
    return f"{IMAGES_DIR}/{rel}"


def local_to_url(path):
    p = path.replace("\\", "/")
    if p.startswith(IMAGES_DIR):
        p = p[len(IMAGES_DIR):]
    return "/images/" + p.lstrip("/")


# ---- image encoding (Pillow, lazy) --------------------------------------

def _pil():
    from PIL import Image  # noqa: WPS433 — optional dep, only for --live
    return Image


def to_webp(raw):
    img = _pil()
    with img.open(io.BytesIO(raw)) as im:
        buf = io.BytesIO()
        im.save(buf, format="WEBP", quality=90, method=6)
        return buf.getvalue()


def to_thumb(raw):
    img = _pil()
    with img.open(io.BytesIO(raw)) as im:
        im.thumbnail((THUMB_MAX, THUMB_MAX))
        buf = io.BytesIO()
        im.save(buf, format="WEBP", quality=82, method=6)
        return buf.getvalue()


# ---- KR API --------------------------------------------------------------

def iter_needs_work(kind, limit=200):
    cursor = 0
    while True:
        status, resp = http_json(
            "GET", f"{KR_BASE_URL}/api/art/image/needs-work?kind={kind}&limit={limit}&cursorId={cursor}"
        )
        if status != 200 or not resp or not resp.get("success"):
            log(f"  ! needs-work({kind}) failed: HTTP {status} {resp and resp.get('message')}")
            return
        data = resp.get("data") or {}
        for item in data.get("items") or []:
            yield item
        if data.get("done") or data.get("nextCursor") is None:
            return
        cursor = data["nextCursor"]


def get_image(image_id, include_data=False, include_collections=False):
    # imageData/thumbnailData/collections are opt-in on the GET; only ask for
    # what we need (bytes on --live, collections when naming files).
    params = []
    if include_data:
        params += ["includeImageData=true", "includeThumbnailData=true"]
    if include_collections:
        params.append("includeCollections=true")
    q = ("?" + "&".join(params)) if params else ""
    status, resp = http_json("GET", f"{KR_BASE_URL}/api/art/image/{image_id}{q}")
    if status != 200 or not resp:
        return None
    return resp.get("data") or resp


def patch_image(image_id, fields, live):
    if not live:
        return True
    status, resp = http_json("PATCH", f"{KR_BASE_URL}/api/art/image/{image_id}", fields)
    if status != 200 or not resp or not resp.get("success"):
        log(f"  ! patch #{image_id} failed: HTTP {status} {resp and resp.get('message')}")
        return False
    return True


def delete_image(image_id, live):
    if not live:
        return True
    status, resp = http_json("DELETE", f"{KR_BASE_URL}/api/art/image/{image_id}")
    if status != 200 or not resp or not resp.get("success"):
        log(f"  ! delete #{image_id} failed: HTTP {status} {resp and resp.get('message')}")
        return False
    return True


# ---- disk dedup index ----------------------------------------------------

IMAGE_EXTS = (".webp", ".png", ".jpg", ".jpeg", ".gif")


def build_disk_hash_index():
    """sha256(file bytes) -> public url, for every image already on disk."""
    index = {}
    if not IMAGES_DIR or not os.path.isdir(IMAGES_DIR):
        return index
    for root, _dirs, files in os.walk(IMAGES_DIR):
        for name in files:
            if not name.lower().endswith(IMAGE_EXTS):
                continue
            full = os.path.join(root, name)
            try:
                with open(full, "rb") as f:
                    h = hashlib.sha256(f.read()).hexdigest()
                index.setdefault(h, local_to_url(full))
            except OSError:
                continue
    return index


# ---- passes --------------------------------------------------------------

def decode_b64(s):
    """Decode base64 that may be a bare string or a data: URI."""
    if not s:
        return None
    if s.startswith("data:") and "," in s:
        s = s.split(",", 1)[1]
    return base64.b64decode(s)


def slug_name(text, limit=48):
    """Filesystem-safe slug from a prompt: lowercase alnum, single dashes."""
    out = []
    for ch in (text or "").lower():
        if ch.isalnum():
            out.append(ch)
        elif out and out[-1] != "-":
            out.append("-")
    return "".join(out).strip("-")[:limit].strip("-")


def name_for(rec, image_id):
    """A readable stem for a materialized file: <prompt-slug>-<id> (id keeps it
    unique across identical prompts), falling back to art-<id>."""
    base = slug_name((rec or {}).get("promptString") or (rec or {}).get("artPrompt"))
    return f"{base}-{image_id}" if base else f"art-{image_id}"


def target_for(rec, image_id, default_collection):
    """Return (folder, stem) for a materialized file. Prefer the image's art
    collection — file lands in that slug's folder as {slug}-inspiration-{id},
    matching the site's inspiration-art naming. Fall back to the default folder
    with a prompt-based name when the image has no slugged collection."""
    for c in (rec or {}).get("ArtCollections") or []:
        s = c.get("slug")
        # Skip the catch-all "unsorted-uN" buckets — those aren't a real
        # collection identity, so fall through to a prompt-based name instead.
        if s and not s.startswith("unsorted-"):
            return s, f"{s}-inspiration-{image_id}"
    return default_collection, name_for(rec, image_id)


def pass_materialize(live, collection):
    log(f"\n== materialize {'(LIVE)' if live else '(dry-run)'} ==")
    # Cheap plan first (metadata only, no byte fetches).
    items = list(iter_needs_work("materialize"))
    log(f"  {len(items)} DB-only image(s) (imageData present, no file)")
    if not live:
        log(f"  dry-run: --live content-hashes each, then links an identical")
        log(f"  existing file or writes a new .webp under '{collection}/'.")
        return
    disk = build_disk_hash_index()
    log(f"  indexed {len(disk)} on-disk file(s) for dedup")
    written = linked = missing = failed = 0
    for seen, item in enumerate(items, 1):
        if seen % 100 == 0:
            log(f"  … {seen}/{len(items)} ({written} written, {linked} linked)")
        rec = get_image(item["id"], include_data=True, include_collections=True)
        try:
            raw = decode_b64((rec or {}).get("imageData"))
        except (ValueError, TypeError):
            raw = None
        if raw is None:
            missing += 1
            continue
        h = hashlib.sha256(raw).hexdigest()
        if h in disk:  # dedup: bytes already on disk -> just link
            url = disk[h]
            linked += 1
            log(f"  #{item['id']} -> link existing {url}")
            patch_image(item["id"], {"imagePath": url, "path": url, "fileType": url.rsplit('.', 1)[-1]}, live)
            continue
        folder_slug, stem = target_for(rec, item["id"], collection)
        url = f"/images/{folder_slug}/{stem}.webp"
        written += 1
        log(f"  #{item['id']} -> write {url}")
        if live:
            try:
                webp = to_webp(raw)
                dest = url_to_local(url)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                with open(dest, "wb") as f:
                    f.write(webp)
                disk[hashlib.sha256(webp).hexdigest()] = url
                if not patch_image(item["id"], {"imagePath": url, "path": url, "fileType": "webp"}, live):
                    failed += 1
            except Exception as e:  # noqa: BLE001
                log(f"  ! #{item['id']} write failed: {e}")
                failed += 1
    log(f"  materialize: {written} to write, {linked} linked (dup), {missing} no-data, {failed} failed")


def pass_png2webp(live):
    log(f"\n== png2webp {'(LIVE)' if live else '(dry-run)'} ==")
    converted = missing = failed = fixed = 0
    changed_urls = {}  # old_url -> new_url, for manifest rewrite
    for seen, item in enumerate(iter_needs_work("png"), 1):
        if seen % 100 == 0:
            log(f"  … {seen} processed ({converted} converted, {fixed} fileType-only)")
        old_url = item.get("imagePath") or item.get("path")
        if not old_url or not old_url.lower().endswith(".png"):
            # fileType said png but path isn't a .png file — just fix fileType.
            fixed += 1
            if live:
                patch_image(item["id"], {"fileType": "webp"}, live)
            continue
        src = url_to_local(old_url)
        if not src or not os.path.isfile(src):
            missing += 1
            log(f"  #{item['id']} png file missing on disk: {old_url}")
            continue
        new_url = old_url[:-4] + ".webp"
        converted += 1
        log(f"  #{item['id']} {old_url} -> {new_url}")
        changed_urls[old_url] = new_url
        if live:
            try:
                with open(src, "rb") as f:
                    webp = to_webp(f.read())
                dest = url_to_local(new_url)
                with open(dest, "wb") as f:
                    f.write(webp)
                os.remove(src)
                if not patch_image(item["id"], {"imagePath": new_url, "path": new_url, "fileType": "webp"}, live):
                    failed += 1
            except Exception as e:  # noqa: BLE001
                log(f"  ! #{item['id']} convert failed: {e}")
                failed += 1
    _rewrite_manifests(changed_urls, live)
    _report_code_refs()
    log(f"  png2webp: {converted} converted, {fixed} fileType-only, {missing} missing-on-disk, {failed} failed")


def _rewrite_manifests(changed_urls, live):
    """Rewrite ONLY the filenames we actually converted (old .png basename ->
    new .webp basename) in collections.json / per-folder gallery.json. Never a
    blanket .png->.webp replace: that would repoint manifests at .webp files
    that don't exist for pngs this run didn't convert."""
    if not IMAGES_DIR or not changed_urls:
        return
    renames = {}
    for old_url, new_url in changed_urls.items():
        old_base = old_url.rsplit("/", 1)[-1]
        new_base = new_url.rsplit("/", 1)[-1]
        renames[old_base] = new_base
        renames[old_base.rsplit(".", 1)[0] + ".png"] = new_base  # be explicit

    targets = [os.path.join(IMAGES_DIR, "collections.json")]
    for root, _dirs, files in os.walk(IMAGES_DIR):
        if "gallery.json" in files:
            targets.append(os.path.join(root, "gallery.json"))
    touched = 0
    for path in targets:
        if not os.path.isfile(path):
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        except OSError:
            continue
        new_text = text
        for old_base, new_base in renames.items():
            if old_base in new_text:
                new_text = new_text.replace(old_base, new_base)
        if new_text == text:
            continue
        touched += 1
        log(f"  manifest: {os.path.basename(path)}")
        if live:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_text)
    if touched:
        log(f"  manifests {'rewritten' if live else 'to rewrite'}: {touched}")


def _report_code_refs():
    """We deliberately do NOT auto-edit source. Remind the operator to grep the
    repo for any hardcoded .png references (components/content) and fix by hand."""
    log("  note: source code .png refs are NOT auto-edited — grep the repo and fix by hand")


def pass_thumbnails(live):
    log(f"\n== thumbnails {'(LIVE)' if live else '(dry-run)'} ==")
    # Cheap plan first (metadata only). Every candidate has a source per the
    # needs-work filter (a path or imageData), so the count is the plan.
    items = list(iter_needs_work("thumbnail"))
    log(f"  {len(items)} image(s) need a thumbnail")
    if not live:
        log("  dry-run: --live reads each source (on-disk file, else DB bytes),")
        log("  writes a thumb .webp, and patches thumbnailPath + thumbnailData.")
        return
    made = missing = failed = 0
    for seen, item in enumerate(items, 1):
        if seen % 100 == 0:
            log(f"  … {seen}/{len(items)} ({made} made, {missing} no-source)")
        src_url = item.get("imagePath") or item.get("path")
        raw = None
        if src_url:
            local = url_to_local(src_url)
            if local and os.path.isfile(local):
                with open(local, "rb") as f:
                    raw = f.read()
        if raw is None:  # fall back to DB bytes (opt-in include)
            rec = get_image(item["id"], include_data=True)
            try:
                raw = decode_b64((rec or {}).get("imageData"))
            except (ValueError, TypeError):
                raw = None
        if raw is None:
            missing += 1
            continue
        base_url = src_url or f"/images/generated/generated-{item['id']}.webp"
        folder, name = base_url.rsplit("/", 1)
        thumb_url = f"{folder}/thumb/{name.rsplit('.', 1)[0]}.webp"
        made += 1
        log(f"  #{item['id']} -> thumb {thumb_url}")
        try:
            tb = to_thumb(raw)
            dest = url_to_local(thumb_url)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "wb") as f:
                f.write(tb)
            # Path-first: set thumbnailPath only; the file is the source of
            # truth, so we do NOT store base64 thumbnailData in the DB.
            if not patch_image(item["id"], {"thumbnailPath": thumb_url}, live):
                failed += 1
        except Exception as e:  # noqa: BLE001
            log(f"  ! #{item['id']} thumb failed: {e}")
            failed += 1
    log(f"  thumbnails: {made} made, {missing} no-source, {failed} failed")


def pass_clear_data(live):
    """Path-first DB shrink: null imageData for rows that already have a served
    file path (kind=clearable). Opt-in only, never part of the default run.
    Guarded: only clears a row whose file actually exists on local disk, so we
    never drop the bytes for an image that isn't really on disk yet. Run this
    only AFTER the files are committed + deployed."""
    log(f"\n== clear-data {'(LIVE)' if live else '(dry-run)'} ==")
    items = list(iter_needs_work("clearable"))
    log(f"  {len(items)} row(s) carry imageData while also having a file path")
    if not live:
        log("  dry-run: --live nulls imageData for rows whose file exists on disk")
        log("  (run ONLY after those files are committed + deployed).")
        return
    cleared = skipped = failed = 0
    for seen, item in enumerate(items, 1):
        if seen % 100 == 0:
            log(f"  … {seen}/{len(items)} ({cleared} cleared, {skipped} skipped)")
        local = url_to_local(item.get("imagePath") or item.get("path"))
        if not local or not os.path.isfile(local):
            skipped += 1  # no local file — don't drop the only copy
            continue
        if patch_image(item["id"], {"imageData": None}, live):
            cleared += 1
        else:
            failed += 1
    log(f"  clear-data: {cleared} cleared, {skipped} skipped (no local file), {failed} failed")


def pass_prune_unreachable(live):
    """Delete dead ArtImage rows that point at nothing: no file path AND no
    imageData (kind=unreachable). Opt-in and destructive — dry-run lists them
    so you can eyeball before deleting."""
    log(f"\n== prune-unreachable {'(LIVE)' if live else '(dry-run)'} ==")
    items = list(iter_needs_work("unreachable"))
    log(f"  {len(items)} dead row(s) (no file path, no imageData)")
    if not live:
        for item in items[:20]:
            log(f"  would delete #{item['id']}")
        if len(items) > 20:
            log(f"  … and {len(items) - 20} more")
        log("  dry-run: --live DELETEs these ArtImage rows.")
        return
    deleted = failed = 0
    for seen, item in enumerate(items, 1):
        if seen % 100 == 0:
            log(f"  … {seen}/{len(items)} ({deleted} deleted)")
        if delete_image(item["id"], live):
            deleted += 1
        else:
            failed += 1
    log(f"  prune-unreachable: {deleted} deleted, {failed} failed")


def pass_rename(live, collection):
    """Give already-materialized files readable names: rename
    {collection}/{collection}-{id}.ext -> {collection}/<prompt-slug>-{id}.ext
    (on disk) and PATCH imagePath/path to match. Opt-in; run before you commit
    the materialized files (or expect a rename churn in git if already committed)."""
    log(f"\n== rename {'(LIVE)' if live else '(dry-run)'} ==")
    folder = f"{IMAGES_DIR}/{collection}"
    if not os.path.isdir(folder):
        log(f"  no '{collection}/' folder on disk — nothing to rename")
        return
    prefix = f"{collection}-"
    renamed = skipped = failed = 0
    for fname in sorted(os.listdir(folder)):
        stem, ext = os.path.splitext(fname)
        if not stem.startswith(prefix) or not stem[len(prefix):].isdigit():
            continue  # not an auto-named file
        image_id = int(stem[len(prefix):])
        rec = get_image(image_id, include_collections=True)
        folder_slug, new_stem = target_for(rec, image_id, collection)
        new_fname = f"{new_stem}{ext}"
        old_url = f"/images/{collection}/{fname}"
        new_url = f"/images/{folder_slug}/{new_fname}"
        if new_url == old_url:
            skipped += 1
            continue
        renamed += 1
        log(f"  #{image_id} {old_url} -> {new_url}")
        if live:
            try:
                dest_abs = url_to_local(new_url)
                os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
                os.rename(os.path.join(folder, fname), dest_abs)  # may cross folders
                if not patch_image(image_id, {"imagePath": new_url, "path": new_url}, live):
                    failed += 1
            except Exception as e:  # noqa: BLE001
                log(f"  ! #{image_id} rename failed: {e}")
                failed += 1
    log(f"  rename: {renamed} renamed, {skipped} already-named, {failed} failed")


def main():
    ap = argparse.ArgumentParser(description="Reverse-parity art migration (dry-run by default).")
    ap.add_argument("--live", action="store_true", help="apply changes (default: dry-run)")
    ap.add_argument("--materialize", action="store_true", help="run the materialize pass")
    ap.add_argument("--png2webp", action="store_true", help="run the PNG->WebP pass")
    ap.add_argument("--thumbnails", action="store_true", help="run the thumbnail pass")
    ap.add_argument("--clear-data", dest="clear_data", action="store_true",
                    help="null imageData for rows that already have a file (opt-in; run after deploy)")
    ap.add_argument("--rename", action="store_true",
                    help="rename already-materialized {collection}-{id} files to <prompt-slug>-{id} (opt-in)")
    ap.add_argument("--prune-unreachable", dest="prune_unreachable", action="store_true",
                    help="DELETE dead rows with no file and no data (opt-in, destructive)")
    ap.add_argument("--materialize-collection", default="generated",
                    help="folder for newly-written files (default: generated)")
    args = ap.parse_args()

    if not KR_TOKEN:
        log("KR_RELAY_TOKEN is required (admin apiKey / beta-admin token).")
        sys.exit(1)
    if not IMAGES_DIR or not os.path.isdir(IMAGES_DIR):
        log(f"KR_LOCAL_IMAGES_DIR must point at the local public/images dir (got: {IMAGES_DIR!r}).")
        sys.exit(1)

    # The three file-writing passes run by default; clear-data and rename are
    # opt-in only, so they never ride along with a default run.
    run_default = not (
        args.materialize or args.png2webp or args.thumbnails
        or args.clear_data or args.rename or args.prune_unreachable
    )
    do_materialize = run_default or args.materialize
    do_png2webp = run_default or args.png2webp
    do_thumbnails = run_default or args.thumbnails

    # Pillow is only needed by the byte-processing passes, not clear-data.
    if args.live and (do_materialize or do_png2webp or do_thumbnails):
        try:
            _pil()
        except Exception:  # noqa: BLE001
            log("--live needs Pillow for image conversion: pip install Pillow")
            sys.exit(1)

    log(f"parity_migrate {'LIVE' if args.live else 'DRY-RUN'} against {KR_BASE_URL}")
    if not args.live:
        log("(dry-run: no files or DB rows will change; pass --live to apply)")

    if do_materialize:
        pass_materialize(args.live, args.materialize_collection)
    if do_png2webp:
        pass_png2webp(args.live)
    if do_thumbnails:
        pass_thumbnails(args.live)
    if args.rename:
        pass_rename(args.live, args.materialize_collection)
    if args.prune_unreachable:
        pass_prune_unreachable(args.live)
    if args.clear_data:
        pass_clear_data(args.live)

    log("\nDone. Review the plan above; re-run with --live to apply. Commit + push public/images after a live run.")


if __name__ == "__main__":
    main()
