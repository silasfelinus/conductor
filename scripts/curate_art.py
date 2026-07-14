#!/usr/bin/env python3
"""
curate_art.py — vision-model curation for generated art.

The goal (Silas, 2026-07-14): let the AI move a candidate into `approved/` at a
quality that approximates the hand-picking Silas did working directly with
ChatGPT. This is the *judgment* layer on top of art_quality.py's objective floor:

  1. art_quality.py  — mechanical gate (bw==line art, not blank, right shape).
     Cheap, local, no API. Runs first as a prefilter so we never spend a vision
     call on a structurally-broken render.
  2. curate_art.py   — this file. For candidates that clear the floor, ask a
     Claude vision model to judge each one AGAINST THE APPROVED SET as the
     quality bar (few-shot: real approved images are sent as reference), scored
     against the Monster Recast rubric (subject match, camp/horror read,
     anatomy, line-art fidelity). Promote-verdict candidates are proposed for
     `approved/`.

Human gate (AGENTS.md, content projects): by default this PROPOSES — it copies
promote-verdict candidates into `sets/<set>/curation/proposed/` and writes a
manifest for Silas to confirm. `--promote` moves them straight into `approved/`
(still reversible, git-tracked). It never deletes anything.

Follows the house LLM pattern (scripts/build_conductor_summary.py): raw urllib
to the Anthropic Messages API, ANTHROPIC_API_KEY from the environment, and a
graceful fallback to the objective gate when no key is present (so a Worker
cycle without the key still does something useful instead of erroring).

Env:
  ANTHROPIC_API_KEY    required for the vision pass; without it, objective-only
  ART_CURATOR_MODEL    model id (default claude-opus-4-8)

Usage:
  python scripts/curate_art.py --set monster-recast                 # judge + propose
  python scripts/curate_art.py --set monster-recast --dry-run       # objective prefilter only, no API
  python scripts/curate_art.py --set monster-recast --promote       # move promotes into approved/
  python scripts/curate_art.py --set monster-recast --limit 4       # first 4 candidates
  python scripts/curate_art.py --set monster-recast --min-score 80  # stricter promotion bar
"""

from __future__ import annotations

import argparse
import base64
import datetime
import io
import json
import os
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Optional

import yaml

try:
    from zoneinfo import ZoneInfo
    _TZ = ZoneInfo("America/Los_Angeles")
except ImportError:  # pragma: no cover - Python < 3.9 fallback
    _TZ = datetime.timezone(datetime.timedelta(hours=-7))

sys.path.insert(0, str(Path(__file__).parent))
import art_quality  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SETS_DIR = ROOT / "projects" / "coloring-book" / "sets"
DAILY_DIR = ROOT / "projects" / "curation" / "daily"   # dated daily scoring reports
REQUESTS_FILE = ROOT / "projects" / "curation" / "requests.yaml"  # front-end curate queue
AESTHETIC_GUIDELINES = ROOT / "AESTHETIC-GUIDELINES.md"  # steerable daily rubric source
# Recently-rendered art lives in these conductor folders; served publicly via raw GitHub.
DAILY_SCAN_DIRS = [ROOT / "projects" / "images", ROOT / "projects" / "process"]
CONDUCTOR_RAW = "https://raw.githubusercontent.com/silasfelinus/conductor/main"

MODEL = os.environ.get("ART_CURATOR_MODEL", "claude-opus-4-8").strip()
API_URL = "https://api.anthropic.com/v1/messages"

# kind_robots REST (curate-request consumer): fetch ArtImage bytes + POST CURATOR
# feedback. Same conventions as scripts/build_dream_records.py.
KR_BASE_URL = os.environ.get("KR_BASE_URL", "https://kind-robots.vercel.app").rstrip("/")
KR_API_TOKEN = os.environ.get("KR_API_TOKEN", "").strip()
DEFAULT_MIN_SCORE = 75
MAX_EXEMPLARS = 2      # approved reference images per variant, the quality bar
SAMPLE_EDGE = 1024     # downscale long edge before upload to bound image tokens

# Daily-mode scoring: a general aesthetic verdict (no coloring-book specifics).
DAILY_VERDICT_SCHEMA = {
    "type": "object",
    "properties": {
        "score": {"type": "integer"},
        "verdict": {"type": "string", "enum": ["promote", "revise", "reject"]},
        "one_liner": {"type": "string"},
        "reasons": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["score", "verdict", "one_liner", "reasons"],
    "additionalProperties": False,
}

VERDICT_SCHEMA = {
    "type": "object",
    "properties": {
        "subject_match": {"type": "boolean"},
        "on_brief": {"type": "boolean"},
        "line_art_valid": {"type": "boolean"},
        "camp_reads": {"type": "boolean"},
        "horror_reads": {"type": "boolean"},
        "anatomy_ok": {"type": "boolean"},
        "matches_approved_bar": {"type": "boolean"},
        "score": {"type": "integer"},
        "verdict": {"type": "string", "enum": ["promote", "revise", "reject"]},
        "reasons": {"type": "array", "items": {"type": "string"}},
    },
    "required": [
        "subject_match", "on_brief", "line_art_valid", "camp_reads",
        "horror_reads", "anatomy_ok", "matches_approved_bar", "score",
        "verdict", "reasons",
    ],
    "additionalProperties": False,
}

RUBRIC = """\
You are the Reviewer curating art for the "Monster Recast" adult-and-family
coloring book: gender-recast / drag-reimagined classic movie-monster archetypes,
serious camp horror at roughly PG-13. The reference images shown first are the
APPROVED quality bar — art Silas hand-selected. Judge the candidate against that
bar, not against generic "is this a nice image".

Score 0-100 and give a verdict:
- promote: at or above the approved bar; ready for the book with no rework.
- revise: right idea but a fixable flaw (soft area, minor anatomy, background too busy).
- reject: off-brief, wrong subject, or a hard rejection-checklist hit.

Judge on:
- subject_match: is THIS character/scene depicted (matches the concept prompt), not a generic or unrelated image?
- on_brief: graphic horror illustration with serious camp — NOT a cosmic space poster, glamour portrait, painterly haze, cute cartoon, photo, or poster with a border/title bar.
- line_art_valid: (COLORING-PAGE candidates only) clean black line art on white, closed colorable regions, NO color, NO gray shading, NO halftone. For full-color candidates, set true.
- camp_reads / horror_reads: the camp lands and the horror is genuinely menacing/uncanny.
- anatomy_ok: no accidental extra limbs/fingers, believable contact points and perspective.
- matches_approved_bar: does it hold up next to the approved reference images?

Hard rejections: collage/grid/panels, readable text/logo/watermark, a copied
franchise character or actor likeness, beautified-away scars/burns, or a
conventionally-pretty substitute for an intentionally ugly/disfigured design.

Return ONLY the JSON object matching the schema."""


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def scene_prompts(set_dir: Path) -> dict[str, str]:
    """concept_id/slug -> intended scene prompt, from the source manifest."""
    manifest = set_dir / "art-modeler-request.yaml"
    if not manifest.exists():
        return {}
    entries = (load_yaml(manifest).get("batch") or {}).get("entries") or []
    out: dict[str, str] = {}
    for e in entries:
        if not isinstance(e, dict):
            continue
        prompt = " ".join(str(e.get("prompt") or "").split())
        label = str(e.get("label") or "")
        for key in (str(e.get("id") or ""), str(e.get("image_path") or "")):
            if key:
                out[key] = prompt
        if label:
            out[label.lower()] = prompt
    return out


def prompt_for(name: str, prompts: dict[str, str]) -> str:
    """Best-effort match of a filename like mr-013-ansel-bell to a scene prompt."""
    stem = Path(name).stem
    if stem in prompts:
        return prompts[stem]
    parts = stem.split("-")
    if len(parts) >= 2:
        cid = "-".join(parts[:2])           # mr-013
        if cid in prompts:
            return prompts[cid]
    for key, val in prompts.items():
        if key and key in stem:
            return val
    return ""


def encode_image(path: Path, max_edge: int = SAMPLE_EDGE) -> Optional[dict[str, str]]:
    """Return an Anthropic image source block, downscaled when PIL is available."""
    try:
        from PIL import Image

        with Image.open(path) as im:
            im = im.convert("RGB")
            if max(im.size) > max_edge:
                scale = max_edge / max(im.size)
                im = im.resize((max(1, int(im.width * scale)),
                                max(1, int(im.height * scale))))
            buf = io.BytesIO()
            im.save(buf, "WEBP", quality=88)
            data = base64.b64encode(buf.getvalue()).decode()
        return {"type": "base64", "media_type": "image/webp", "data": data}
    except ImportError:
        raw = path.read_bytes()
        media = "image/webp" if path.suffix.lower() == ".webp" else "image/png"
        return {"type": "base64", "media_type": media, "data": base64.b64encode(raw).decode()}
    except Exception:  # noqa: BLE001 - a bad file shouldn't kill the batch
        return None


def exemplars(set_dir: Path, variant: str) -> list[Path]:
    """A couple of approved images matching the variant, as the quality bar."""
    approved = set_dir / "approved"
    if not approved.is_dir():
        return []
    suffix = f"-{variant}.webp"
    picks = sorted(p for p in approved.glob(f"*{suffix}"))
    return picks[:MAX_EXEMPLARS]


def call_vision(api_key: str, candidate: Path, variant: str, scene: str,
                refs: list[Path], rubric: str = RUBRIC,
                schema: dict[str, Any] = VERDICT_SCHEMA) -> dict[str, Any]:
    content: list[dict[str, Any]] = []
    if refs:
        content.append({"type": "text",
                        "text": f"APPROVED reference {variant} art (the quality bar):"})
        for ref in refs:
            src = encode_image(ref)
            if src:
                content.append({"type": "image", "source": src})
    src = encode_image(candidate)
    if not src:
        raise RuntimeError("could not read candidate image")
    variant_label = "coloring-page line art" if variant == "bw" else "full-color illustration"
    scene_hint = f" Intended concept: {scene}" if scene else ""
    content.append({"type": "text",
                    "text": f"CANDIDATE ({variant_label}).{scene_hint}"})
    content.append({"type": "image", "source": src})
    content.append({"type": "text", "text": rubric})

    body = json.dumps({
        "model": MODEL,
        "max_tokens": 2048,
        "thinking": {"type": "adaptive"},
        "output_config": {
            "effort": "medium",
            "format": {"type": "json_schema", "schema": schema},
        },
        "messages": [{"role": "user", "content": content}],
    }).encode()

    req = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        payload = json.loads(resp.read())
    # First text block is schema-valid JSON (thinking blocks may precede it).
    text = next((b.get("text", "") for b in payload.get("content", [])
                 if b.get("type") == "text"), "")
    return json.loads(text)


def candidates(set_dir: Path) -> list[tuple[Path, str]]:
    out: list[tuple[Path, str]] = []
    for variant in ("color", "bw"):
        folder = set_dir / "generated" / variant
        if folder.is_dir():
            for p in sorted(folder.glob("*.webp")):
                if p.parent.name != "rejected":
                    out.append((p, variant))
    return out


def daily_rubric() -> str:
    """The general aesthetic bar for daily scoring — steerable via AESTHETIC-GUIDELINES.md."""
    guidelines = ""
    if AESTHETIC_GUIDELINES.exists():
        guidelines = AESTHETIC_GUIDELINES.read_text(encoding="utf-8").strip()
    intro = (
        "You are Conductor's daily style assessor. Score this freshly generated "
        "image for the site on overall aesthetic quality, against the guidelines "
        "below. Judge intentional composition, cohesive palette, light with "
        "intent, character/story, and craft — reward finished, portfolio-worthy "
        "work and knock blank/degenerate frames, watermarks, garbled anatomy, and "
        "generic filler.\n\n"
    )
    scoring = (
        "\n\nScore 0-100 and give a verdict (promote >=80, revise 60-79, "
        "reject <60), a one_liner caption (<=12 words, for the digest gallery), "
        "and brief reasons. Return ONLY the JSON object matching the schema."
    )
    return intro + (guidelines or "(no guidelines file found — use general good taste.)") + scoring


def public_url(rel: str) -> str:
    """Public URL for a conductor-tracked image, via raw GitHub (stable + public)."""
    return f"{CONDUCTOR_RAW}/{rel.lstrip('/')}"


def recent_render_paths(since: str, limit: int = 0) -> list[Path]:
    """Image files under the scan dirs touched within `since` (git history, mtime fallback)."""
    exts = {".webp", ".png", ".jpg", ".jpeg"}
    found: list[Path] = []
    seen: set[Path] = set()
    rel_dirs = [str(d.relative_to(ROOT)) for d in DAILY_SCAN_DIRS if d.exists()]
    if rel_dirs:
        try:
            out = subprocess.run(
                ["git", "-C", str(ROOT), "log", f"--since={since}",
                 "--name-only", "--pretty=format:", "--", *rel_dirs],
                capture_output=True, text=True, timeout=60,
            ).stdout
            for line in out.splitlines():
                line = line.strip()
                if not line or Path(line).suffix.lower() not in exts:
                    continue
                path = ROOT / line
                if path.exists() and path not in seen:
                    seen.add(path)
                    found.append(path)
        except Exception:  # noqa: BLE001 - fall through to mtime scan
            found = []
    if not found:  # mtime fallback (fresh checkout with shallow history, local runs)
        cutoff = datetime.datetime.now().timestamp() - 24 * 3600
        for d in DAILY_SCAN_DIRS:
            if not d.exists():
                continue
            for path in d.rglob("*"):
                if path.suffix.lower() in exts and path.is_file() and path.stat().st_mtime >= cutoff:
                    if path not in seen:
                        seen.add(path)
                        found.append(path)
    if limit > 0:
        found = found[:limit]
    return found


def run_daily(args) -> int:
    """Score the day's fresh renders and write a dated report for the digest gallery."""
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    do_vision = bool(api_key) and not args.dry_run
    todo = recent_render_paths(args.since, args.limit)
    if not todo:
        print(f"No fresh renders found under {[str(d.relative_to(ROOT)) for d in DAILY_SCAN_DIRS]} "
              f"since {args.since}.")
    rubric = daily_rubric()
    now_iso = datetime.datetime.now(_TZ).isoformat()
    results: list[dict[str, Any]] = []

    for path in todo:
        rel = str(path.relative_to(ROOT))
        variant = art_quality._variant_from_path(path)
        ok, reasons, info = art_quality.assess_file(path, variant)
        base = {"image": rel, "public_url": public_url(rel), "source": path.parent.name,
                "variant": variant, "objective": info, "scored_at": now_iso}
        if ok is False:  # objective floor rejects a broken render before any vision spend
            results.append({**base, "stage": "floor", "score": 0, "verdict": "reject",
                            "reasons": reasons})
            print(f"  FLOOR-FAIL {rel}  {'; '.join(reasons)}")
            continue
        if not do_vision:
            results.append({**base, "stage": "floor", "score": None, "verdict": "needs-vision",
                            "reasons": reasons if ok is None else []})
            print(f"  NEEDS-VISION {rel}")
            continue
        try:
            v = call_vision(api_key, path, variant, "", [], rubric=rubric,
                            schema=DAILY_VERDICT_SCHEMA)
        except Exception as error:  # noqa: BLE001 - keep scoring the batch
            results.append({**base, "stage": "vision", "score": None, "verdict": "error",
                            "reasons": [str(error)]})
            print(f"  VISION-ERR {rel}: {error}", file=sys.stderr)
            continue
        results.append({**base, "stage": "vision", "score": int(v.get("score") or 0),
                        "verdict": str(v.get("verdict") or "reject"),
                        "one_liner": v.get("one_liner", ""), "reasons": v.get("reasons", [])})
        print(f"  {str(v.get('verdict','')).upper():8} {rel}  score={v.get('score')}")

    # Sort scored entries highest-first so the digest can take the top N directly.
    results.sort(key=lambda r: (r.get("score") is not None, r.get("score") or 0), reverse=True)
    DAILY_DIR.mkdir(parents=True, exist_ok=True)
    date = datetime.datetime.now(_TZ).date().isoformat()
    report = DAILY_DIR / f"{date}.yaml"
    report.write_text(
        yaml.safe_dump({"date": date, "model": MODEL if do_vision else None,
                        "since": args.since, "scored": sum(1 for r in results if r.get("score") is not None),
                        "results": results}, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    print(f"\nReport: {report.relative_to(ROOT)}  ({len(results)} images)")
    if not do_vision:
        print("Set ANTHROPIC_API_KEY and drop --dry-run for the vision scoring pass.")
    return 0


# ── Front-end curate-request consumer (--requests) ──────────────────────────

def _kr_http_json(method: str, endpoint: str, body: Any = None, timeout: int = 60):
    """Call a kind_robots REST endpoint with the machine token. Returns (status, json)."""
    url = f"{KR_BASE_URL}{endpoint}"
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
    except Exception as e:  # noqa: BLE001 - network failures surface as (0, msg)
        return 0, {"error": str(e)}


def _fetch_art_image(art_image_id: int) -> Optional[bytes]:
    """Download an ArtImage's bytes from kind_robots (base64 imageData or a path)."""
    status, resp = _kr_http_json(
        "GET", f"/api/art/image/{art_image_id}?includeImageData=true"
    )
    if status != 200 or not isinstance(resp, dict) or not resp.get("data"):
        return None
    image = resp["data"]
    raw = str(image.get("imageData") or "").strip()
    if raw:
        if raw.startswith("data:image/") and "base64," in raw:
            raw = raw.split("base64,", 1)[1]
        try:
            return base64.b64decode(raw)
        except Exception:  # noqa: BLE001
            return None
    # Fallback: a public /images path we can fetch directly.
    path = str(image.get("imagePath") or image.get("path") or "").strip()
    if not path:
        return None
    url = path if path.startswith("http") else f"{KR_BASE_URL}{'' if path.startswith('/') else '/'}{path}"
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            return r.read()
    except Exception:  # noqa: BLE001
        return None


def run_requests(args) -> int:
    """Drain projects/curation/requests.yaml: curate each finished ArtJob and POST
    a CURATOR verdict back to kind_robots (fills the ArtJob trainer panel)."""
    if not REQUESTS_FILE.exists():
        print(f"No curate-request queue at {REQUESTS_FILE.relative_to(ROOT)} — nothing to do.")
        return 0

    doc = yaml.safe_load(REQUESTS_FILE.read_text(encoding="utf-8")) or {}
    requests_list = doc.get("requests") or []
    pending = [r for r in requests_list if isinstance(r, dict) and r.get("status") == "pending"]
    if args.limit > 0:
        pending = pending[: args.limit]

    if not pending:
        print("No pending curate requests.")
        return 0

    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    do_vision = bool(api_key) and not args.dry_run
    can_post = bool(KR_API_TOKEN) and not args.dry_run
    if not do_vision:
        why = "--dry-run" if args.dry_run else "ANTHROPIC_API_KEY not set"
        print(f"Vision disabled ({why}) — leaving {len(pending)} request(s) pending.", file=sys.stderr)
        return 0
    if not can_post:
        print("KR_API_TOKEN not set — cannot POST verdicts (leaving requests pending).", file=sys.stderr)
        return 0

    rubric = daily_rubric()
    now_iso = datetime.datetime.now(_TZ).isoformat()
    curated = 0

    for entry in pending:
        job_id = entry.get("job_id")
        art_image_id = entry.get("art_image_id")
        if not isinstance(job_id, int) or not isinstance(art_image_id, int):
            entry["status"] = "error"
            entry["error"] = "missing job_id/art_image_id"
            continue

        data = _fetch_art_image(art_image_id)
        if not data:
            entry["status"] = "error"
            entry["error"] = f"could not fetch ArtImage {art_image_id}"
            print(f"  FETCH-FAIL job {job_id} (ArtImage {art_image_id})", file=sys.stderr)
            continue

        tmp_path = Path(tempfile.gettempdir()) / f"curate-{art_image_id}.png"
        tmp_path.write_bytes(data)
        try:
            v = call_vision(api_key, tmp_path, "color", str(entry.get("prompt") or ""),
                            [], rubric=rubric, schema=DAILY_VERDICT_SCHEMA)
        except Exception as error:  # noqa: BLE001 - keep draining the queue
            entry["status"] = "error"
            entry["error"] = str(error)
            print(f"  VISION-ERR job {job_id}: {error}", file=sys.stderr)
            continue
        finally:
            tmp_path.unlink(missing_ok=True)

        verdict = str(v.get("verdict") or "reject").upper()
        score = int(v.get("score") or 0)
        feedback = {
            "source": "CURATOR",
            "verdict": verdict,
            "score": score,
            "summary": v.get("one_liner", ""),
            "reasons": v.get("reasons", []),
            "rubricKey": "conductor-curator-v1",
        }
        status, resp = _kr_http_json("POST", f"/api/art/queue/{job_id}/feedback", feedback)
        if status not in (200, 201) or not isinstance(resp, dict) or not resp.get("success"):
            entry["status"] = "error"
            entry["error"] = f"feedback POST {status}: {(resp or {}).get('message', '')}"[:240]
            print(f"  POST-FAIL job {job_id}: {status}", file=sys.stderr)
            continue

        entry["status"] = "done"
        entry["verdict"] = verdict
        entry["score"] = score
        entry["curated_at"] = now_iso
        entry.pop("error", None)
        curated += 1
        print(f"  {verdict:8} job {job_id}  score={score}  {v.get('one_liner','')}")

    REQUESTS_FILE.write_text(
        yaml.safe_dump(doc, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )
    print(f"\nCurated {curated}/{len(pending)} request(s). Queue: {REQUESTS_FILE.relative_to(ROOT)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--set", default="monster-recast", help="coloring-book set slug")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--min-score", type=int, default=DEFAULT_MIN_SCORE)
    parser.add_argument("--dry-run", action="store_true",
                        help="objective prefilter only; no API calls")
    parser.add_argument("--promote", action="store_true",
                        help="move promote-verdict candidates into approved/ (default: propose only)")
    parser.add_argument("--daily", action="store_true",
                        help="score the day's fresh renders for the digest gallery (not a coloring set)")
    parser.add_argument("--requests", action="store_true",
                        help="drain projects/curation/requests.yaml: curate finished ArtJobs "
                             "and POST CURATOR verdicts back to kind_robots")
    parser.add_argument("--since", default="24 hours ago",
                        help="daily mode: window of renders to score (git --since syntax)")
    args = parser.parse_args()

    if args.requests:
        return run_requests(args)

    if args.daily:
        return run_daily(args)

    set_dir = SETS_DIR / args.set
    if not set_dir.is_dir():
        print(f"No such set: {set_dir}", file=sys.stderr)
        return 1

    todo = candidates(set_dir)
    if args.limit > 0:
        todo = todo[: args.limit]
    if not todo:
        print(f"No candidates under {set_dir / 'generated'}.")
        return 0

    prompts = scene_prompts(set_dir)
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    do_vision = bool(api_key) and not args.dry_run
    if not do_vision:
        reason = "--dry-run" if args.dry_run else "ANTHROPIC_API_KEY not set"
        print(f"Objective prefilter only ({reason}) — no vision judgment.\n", file=sys.stderr)

    results: list[dict[str, Any]] = []
    promotes: list[dict[str, Any]] = []

    for path, variant in todo:
        rel = path.relative_to(ROOT)
        ok, reasons, info = art_quality.assess_file(path, variant)

        # Objective floor first. A structural fail never reaches the vision pass.
        if ok is False:
            print(f"  FLOOR-FAIL [{variant:5}] {rel}  {'; '.join(reasons)}")
            results.append({"image": str(rel), "variant": variant, "stage": "floor",
                            "objective": info, "verdict": "reject", "reasons": reasons})
            continue

        if not do_vision:
            note = "floor-pass (needs vision judgment)" if ok else reasons[0]
            print(f"  {'PASS ' if ok else 'SKIP '}[{variant:5}] {rel}  {note}")
            results.append({"image": str(rel), "variant": variant, "stage": "floor",
                            "objective": info, "verdict": "needs-vision"})
            continue

        try:
            v = call_vision(api_key, path, variant, prompt_for(path.name, prompts),
                            exemplars(set_dir, variant))
        except Exception as error:  # noqa: BLE001 - keep curating the batch
            print(f"  VISION-ERR [{variant:5}] {rel}: {error}", file=sys.stderr)
            results.append({"image": str(rel), "variant": variant, "stage": "vision",
                            "verdict": "error", "reasons": [str(error)]})
            continue

        score = int(v.get("score") or 0)
        verdict = str(v.get("verdict") or "reject")
        promote = verdict == "promote" and score >= args.min_score and bool(v.get("subject_match"))
        mark = "PROMOTE" if promote else verdict.upper()
        print(f"  {mark:8} [{variant:5}] {rel}  score={score}  {'; '.join(v.get('reasons', [])[:2])}")
        entry = {"image": str(rel), "variant": variant, "stage": "vision",
                 "objective": info, **v, "promoted": promote}
        results.append(entry)
        if promote:
            promotes.append(entry)

    # Write the curation report.
    report_dir = set_dir / "curation"
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "curation-report.yaml").write_text(
        yaml.safe_dump({"set": args.set, "model": MODEL if do_vision else None,
                        "min_score": args.min_score, "results": results},
                       sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    # Stage or promote the winners.
    if promotes:
        dest = (set_dir / "approved") if args.promote else (report_dir / "proposed")
        dest.mkdir(parents=True, exist_ok=True)
        for entry in promotes:
            src = ROOT / entry["image"]
            (dest / src.name).write_bytes(src.read_bytes())
        where = "approved/" if args.promote else "curation/proposed/ (awaiting Silas)"
        print(f"\n{len(promotes)} candidate(s) -> {where}")
    else:
        print("\nNo promote-verdict candidates.")

    print(f"Report: {(report_dir / 'curation-report.yaml').relative_to(ROOT)}")
    if not do_vision:
        print("Set ANTHROPIC_API_KEY and re-run for the vision judgment pass.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
