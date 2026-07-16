#!/usr/bin/env python3
"""
build_dream_records.py — build a daily-dream proposal into real kind_robots records.

Phase 2 of the rolling daily-dream pipeline (dream-cycle t-012). Takes the
newest UNBUILT daily proposal that has had its steering day (proposal_date <
today, Pacific) and creates the actual content rows via the kind_robots REST
API (machine auth: Authorization: Bearer KR_API_TOKEN — the beta-admin token;
rows attribute to the system admin user server-side).

What gets created (per the kind_robots data philosophy, where a Dream row is
the universal "card hub" and PitchSheets hang off Dreams 1:1):

  * 1 PITCH Dream — the world card (title + idea + vibe)
  * 1 GENRE Dream — the vibe (world-graph fidelity; no card)
  * 2 LOCATION Dreams
  * 3 CHARACTER Dreams + 3 real Character rows (linked via dreamIds)
  * 1 NARRATOR Dream + 1 real Bot row
  * 2 REWARD Dreams + 2 real Reward rows (one SKILL, one ITEM)
  * 1-2 Scenario rows (linked to the world + locations)
  * a PitchSheet per card Dream via POST /api/sheets/by-dream/{id}
    (NOTE: POST /api/sheets is a known-broken handler — never use it)

Every row carries designer: "dream-cycle", and every sheet carries
extraData: {dreamCycle, proposalDate, elementType, element} so the site's
/daily-dream page can group and render a whole dream — and so the whole
creation is traceable and removable (the reversibility contract).

World-graph edges (kind-robots/t-017): the world (PITCH) Dream RELATED to the
GENRE Dream, world CONTAINS each LOCATION Dream, and each LOCATION RELATED to
the GENRE Dream — via POST /api/dream-relations. Character/narrator/reward
cohesion still comes from extraData tags + the dreamIds relation arrays.

Art is queued through the EXISTING self-draining pipeline: one `requests:`
entry per card appended to projects/art-prompts.yaml targeting kind_robots
public/images/dreams/<slug>/… — the nightly auto-art-generate workflow renders
them and distribute_images.py lands them in the site repo. The `--attach`
pass (run every hourly sweep) HEAD-checks the public URLs and PATCHes each
PitchSheet's imagePath once its art is live.

Steering contract: if the proposal file's `## Notes from Silas` section has
real content, this script REFUSES to auto-build (agents must fold notes in
first — see backlog/README.md). `status: parked/vetoed` are never built.

Runs during the conductor sweeps (no LLM calls here — pure REST), NOT in the
daily-digest cron.

Usage:
  python scripts/build_dream_records.py                # build the eligible proposal (if any)
  python scripts/build_dream_records.py --dry-run      # show what would be created
  python scripts/build_dream_records.py --date 2026-07-13   # build a specific proposal_date
  python scripts/build_dream_records.py --attach       # only attach live art to built proposals
Env:
  KR_API_TOKEN   required for live record creation / attach
  KR_BASE_URL    default https://kind-robots.vercel.app
"""

from __future__ import annotations

import argparse
import datetime
import glob
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Optional

try:
    from zoneinfo import ZoneInfo
    _TZ = ZoneInfo("America/Los_Angeles")
except ImportError:  # pragma: no cover
    _TZ = datetime.timezone(datetime.timedelta(hours=-7))

ROOT = Path(__file__).resolve().parents[1]
BACKLOG = ROOT / "projects" / "dream-cycle" / "backlog"
ART_PROMPTS = ROOT / "projects" / "art-prompts.yaml"

KR_BASE_URL = os.environ.get("KR_BASE_URL", "https://kind-robots.vercel.app").rstrip("/")
KR_API_TOKEN = os.environ.get("KR_API_TOKEN", "").strip()
DESIGNER = "dream-cycle"
PAGE_URL = f"{KR_BASE_URL}/daily-dream"

CARD_SIZE = "512x768"  # pitch-card portrait, matches the site's card asset standard
NOTES_PLACEHOLDER = "(leave notes here"
VALID_RARITIES = {"COMMON", "UNCOMMON", "RARE", "EPIC", "LEGENDARY"}

HOUSE_PROMPT_TAIL = (
    "cohesive Kind Robots visual style, cinematic light with intent, "
    "no readable text, no logos, no watermark"
)


# ── HTTP (house pattern: consume_art_queue.http_json) ───────────────────────

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
    except Exception as e:  # noqa: BLE001 - network failures surface as (0, msg)
        return 0, {"error": str(e)}


def head_ok(url: str, timeout: int = 20) -> bool:
    req = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return 200 <= resp.status < 300
    except Exception:  # noqa: BLE001
        return False


# ── Proposal discovery / parsing ─────────────────────────────────────────

def _frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return {}
    import yaml
    try:
        return yaml.safe_load(m.group(1)) or {}
    except Exception:  # noqa: BLE001
        return {}


def _data_block(text: str, name: str) -> Optional[dict]:
    m = re.search(rf"<!--\s*{name}\s*\n(.*?)\n-->", text, re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return None


def has_silas_notes(text: str) -> bool:
    """True if the Notes from Silas section holds anything beyond the placeholder."""
    m = re.search(r"^##\s+Notes from Silas\s*\n(.*?)(?=^##\s|\Z)", text, re.DOTALL | re.MULTILINE)
    if not m:
        return False
    for line in m.group(1).splitlines():
        stripped = line.strip().lstrip("-").strip()
        if stripped and NOTES_PLACEHOLDER not in stripped:
            return True
    return False


def find_proposals() -> list[tuple[Path, dict, str]]:
    out = []
    for path in sorted(glob.glob(str(BACKLOG / "*.md"))):
        p = Path(path)
        if p.name.startswith("_") or p.name == "README.md":
            continue
        text = p.read_text(encoding="utf-8")
        fm = _frontmatter(text)
        if fm.get("proposal"):
            out.append((p, fm, text))
    return out


def eligible_proposal(date_override: Optional[str]) -> tuple[Optional[Path], str]:
    """Newest proposal with proposal_date < today (or == override), unbuilt, buildable."""
    today = datetime.datetime.now(_TZ).date().isoformat()
    best: Optional[tuple[str, Path]] = None
    reason = "no unbuilt proposal ready (none past its steering day)"
    for p, fm, text in find_proposals():
        pdate = str(fm.get("proposal_date") or fm.get("created") or "")
        status = str(fm.get("status") or "outline")
        if date_override:
            if pdate != date_override:
                continue
        elif not (pdate and pdate < today):
            continue  # still in its steering day
        if status in ("parked", "vetoed", "built", "building"):
            continue
        if _data_block(text, "built-data"):
            continue  # already built
        if has_silas_notes(text):
            reason = f"{p.name}: has Notes from Silas — agent must fold them in before building"
            continue
        if best is None or pdate > best[0]:
            best = (pdate, p)
    if best:
        return best[1], ""
    return None, reason


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return re.sub(r"-{2,}", "-", s) or "element"


# ── Art queueing (append to art-prompts.yaml requests:, comment-preserving) ──

def _yq(value: str) -> str:
    """Single-quote a YAML scalar."""
    return "'" + str(value).replace("'", "''") + "'"


def art_request_entry(slug: str, element_slug: str, label: str, prompt: str) -> tuple[str, str, str]:
    """Return (request_id, image_path, yaml_text) for one element's card art."""
    req_id = f"dream-cycle-{slug}-{element_slug}"
    image_path = f"public/images/dreams/{slug}/{element_slug}-card.webp"
    yaml_text = (
        f"- id: {req_id}\n"
        f"  source: dream-cycle\n"
        f"  status: pending\n"
        f"  target_repo: silasfelinus/kind_robots\n"
        f"  image_path: {image_path}\n"
        f"  source_url: /images/dreams/{slug}/{element_slug}-card.webp\n"
        f"  page_url: {PAGE_URL}\n"
        f"  variant: card\n"
        f"  size: {CARD_SIZE}\n"
        f"  label: {_yq(label)}\n"
        f"  prompt: {_yq(' '.join(prompt.split()))}\n"
    )
    return req_id, image_path, yaml_text


def append_art_requests(entries: list[str], dry_run: bool) -> None:
    if not entries:
        return
    text = ART_PROMPTS.read_text(encoding="utf-8")
    if "\nrequests:" not in text and not text.startswith("requests:"):
        text += "\nrequests:\n"
    if not text.endswith("\n"):
        text += "\n"
    text += "".join(entries)
    if dry_run:
        print(f"  [dry-run] would append {len(entries)} art request(s) to projects/art-prompts.yaml")
        return
    ART_PROMPTS.write_text(text, encoding="utf-8")
    print(f"  appended {len(entries)} art request(s) to projects/art-prompts.yaml")


# ── Backlog file bookkeeping ───────────────────────────────────────────

def record_built(path: Path, built: dict, dry_run: bool) -> None:
    """Flip status→built, append Build log line, embed built-data JSON."""
    text = path.read_text(encoding="utf-8")
    today = datetime.datetime.now(_TZ).date().isoformat()
    text = re.sub(r"^status:\s*.+$", "status: built", text, count=1, flags=re.MULTILINE)
    n_records = sum(len(v) if isinstance(v, list) else 1
                    for v in built.get("records", {}).values())
    log_line = (f"- {today} | records | created {n_records} kind_robots rows + "
                f"{len(built.get('art', []))} art requests | auto (build_dream_records.py)")
    text = re.sub(r"(^## Build log\s*\n)", rf"\1{log_line}\n", text, count=1, flags=re.MULTILINE)
    block = f"\n<!-- built-data\n{json.dumps(built, ensure_ascii=False)}\n-->\n"
    text = text.rstrip() + "\n" + block
    if dry_run:
        print(f"  [dry-run] would mark {path.name} built with built-data "
              f"({n_records} records, {len(built.get('art', []))} art)")
        return
    path.write_text(text, encoding="utf-8")
    print(f"  marked {path.name} built (+built-data)")


def update_built_data(path: Path, built: dict) -> None:
    text = path.read_text(encoding="utf-8")
    new_block = f"<!-- built-data\n{json.dumps(built, ensure_ascii=False)}\n-->"
    text, n = re.subn(r"<!--\s*built-data\s*\n.*?\n-->", new_block, text, count=1, flags=re.DOTALL)
    if n:
        path.write_text(text, encoding="utf-8")


# ── Record creation (kind_robots REST) ─────────────────────────────────────
# Contracts verified against kind_robots server/api/* (2026-07-14):
#   * response envelope {success, message, data, statusCode}; new id at data.id
#   * POST /api/dreams, /api/characters: requireApiUser (Bearer beta-admin ok)
#   * POST /api/rewards, /api/scenarios: validateApiKey (Bearer beta-admin ok)
#   * POST /api/sheets is BROKEN — use POST /api/sheets/by-dream/{dreamId}
#     (idempotent: returns the existing sheet with 200 if one exists)
#   * PATCH /api/sheets/{id} accepts imagePath (whitelist: sanitizePitchSheetPayload)

def _delete_base(endpoint: str) -> str:
    """The DELETE collection path for a row created via `endpoint`. Every POST
    endpoint is its own collection base except sheets, whose create is
    POST /api/sheets/by-dream/{dreamId} but whose delete is DELETE /api/sheets/{id}."""
    if endpoint.startswith("/api/sheets"):
        return "/api/sheets"
    return endpoint


def rollback_created(results: list, dry_run: bool = False) -> int:
    """DELETE every row created this run (newest first), best-effort. Used to keep a
    build ATOMIC: if any call fails (e.g. an intermittent DB 503 mid-sequence) we undo
    the rows that did land so the proposal can be retried clean — no orphans, no
    duplicates on the next sweep. Returns the number of rows deleted."""
    created = [(r["delete_base"], r["id"]) for r in results
               if r.get("ok") and r.get("id")]
    if dry_run or not created:
        return 0
    deleted = 0
    for base, rid in reversed(created):
        status, _ = http_json("DELETE", f"{KR_BASE_URL}{base}/{rid}")
        if status in (200, 204):
            deleted += 1
            print(f"  rolled back: DELETE {base}/{rid}")
        else:
            print(f"  WARN rollback failed: DELETE {base}/{rid} -> {status}",
                  file=sys.stderr)
    return deleted


def kr_call(method: str, endpoint: str, body: dict, dry_run: bool,
            results: list, label: str = "") -> Optional[dict]:
    """One API call; returns the record dict from data (with id) or None.

    Each result carries `id` + `delete_base` so a failed build can roll back the rows
    it already created (see rollback_created)."""
    if dry_run:
        print(f"  [dry-run] {method} {endpoint}: {label}")
        results.append({"endpoint": endpoint, "status": 0, "ok": True, "label": label,
                        "id": None, "delete_base": _delete_base(endpoint)})
        return {"id": 0}
    status, resp = http_json(method, f"{KR_BASE_URL}{endpoint}", body)
    record = None
    if isinstance(resp, dict):
        data = resp.get("data")
        if isinstance(data, dict) and "id" in data:
            record = data
        elif isinstance(data, dict) and isinstance(data.get("created"), list) \
                and data["created"] and isinstance(data["created"][0], dict):
            record = data["created"][0]  # scenarios array-mode envelope
        elif "id" in resp:
            record = resp
    ok = status in (200, 201, 207) and record is not None
    results.append({"endpoint": endpoint, "status": status, "ok": ok, "label": label,
                    "id": record.get("id") if (ok and isinstance(record, dict)) else None,
                    "delete_base": _delete_base(endpoint)})
    if not ok:
        print(f"  FAIL {status} {method} {endpoint} ({label}): {str(resp)[:200]}",
              file=sys.stderr)
        return None
    return record


def build_records(proposal: dict, slug: str, pdate: str, dry_run: bool) -> tuple[dict, list, list[str]]:
    """Create all rows + sheets; returns (built-data dict, results log, art yaml entries)."""
    results: list = []
    art_entries: list[str] = []
    built: dict[str, Any] = {
        "built_at": datetime.datetime.now(_TZ).isoformat(),
        "designer": DESIGNER,
        "page": PAGE_URL,
        "records": {},
        "sheets": {},
        "art": [],
    }
    title = proposal.get("title", slug)
    vibe = proposal.get("vibe", {})
    vibe_line = vibe.get("line", "")
    extra_base = {"dreamCycle": slug, "proposalDate": pdate}

    def queue_art(element_slug: str, label: str, art_prompt: str) -> None:
        req_id, image_path, yaml_text = art_request_entry(slug, element_slug, label, art_prompt)
        art_entries.append(yaml_text)
        built["art"].append({"request_id": req_id, "image_path": image_path,
                             "public_path": "/" + image_path.removeprefix("public/"),
                             "attached": False, "element": element_slug})

    def card_dream(dream_type: str, dtitle: str, description: str, flavor: str,
                   art_prompt: str, icon: str, element_slug: str,
                   sheet_overrides: dict) -> Optional[dict]:
        """Create a card Dream + its PitchSheet (via by-dream). Returns the dream."""
        dream = kr_call("POST", "/api/dreams", {
            "title": dtitle, "dreamType": dream_type, "designer": DESIGNER,
            "isPublic": True, "description": description,
            "flavorText": flavor[:500] if flavor else None,
            "artPrompt": art_prompt or None, "icon": icon,
        }, dry_run, results, f"{dream_type} dream: {dtitle}")
        if not dream:
            return None
        sheet_body = {
            "designer": DESIGNER, "isPublic": True,
            "extraData": {**extra_base, "elementType": dream_type, "element": element_slug},
            **sheet_overrides,
        }
        sheet = kr_call("POST", f"/api/sheets/by-dream/{dream['id']}", sheet_body,
                        dry_run, results, f"sheet: {dtitle}")
        if sheet:
            built["sheets"][element_slug] = sheet.get("id")
        return dream

    def trio(labels_values: list[tuple[str, str]]) -> dict:
        body: dict[str, Any] = {}
        for i, (lab, val) in enumerate(labels_values[:3], start=1):
            body[f"highlight{i}Label"] = lab
            body[f"highlight{i}Value"] = (val or "")[:500]
        return body

    # 1. The world card (PITCH Dream) — the header card for the page + digest.
    world = card_dream(
        "PITCH", title, proposal.get("idea", ""), vibe_line,
        f"establishing key art for {title}: {vibe_line}, {HOUSE_PROMPT_TAIL}",
        "kind-icon:moon", slug,
        {"title": title, "hook": vibe.get("title", ""), "pitch": proposal.get("idea", ""),
         **trio([("Promise", vibe_line),
                 ("Builds Into", "characters, locations, rewards, a narrator"),
                 ("Status", f"proposed {pdate}, built by dream-cycle")])},
    )
    if world:
        built["records"]["world"] = {"model": "Dream", "id": world.get("id"), "title": title}
        queue_art(slug, title,
                  f"establishing key art for the world of {title}: {proposal.get('idea', '')} "
                  f"{vibe_line}, portrait key-art composition, {HOUSE_PROMPT_TAIL}")
    world_id = world.get("id") if world else None

    # 2. The vibe (GENRE Dream) — world-graph fidelity; no card/sheet.
    genre = kr_call("POST", "/api/dreams", {
        "title": vibe.get("title", f"{title} Vibe"), "dreamType": "GENRE",
        "designer": DESIGNER, "isPublic": True, "description": vibe_line,
        "flavorText": vibe_line[:500], "icon": "kind-icon:palette",
    }, dry_run, results, f"GENRE dream: {vibe.get('title')}")
    if genre:
        built["records"]["vibe"] = {"model": "Dream", "id": genre.get("id"),
                                    "title": vibe.get("title")}
    genre_id = genre.get("id") if genre else None
    if world_id and genre_id:
        kr_call("POST", "/api/dream-relations",
                {"fromDreamId": world_id, "toDreamId": genre_id, "relationType": "RELATED"},
                dry_run, results, f"relation: {title} -> {vibe.get('title')} (RELATED)")

    # 3. Locations (LOCATION Dreams + cards)
    built["records"]["locations"] = []
    location_ids: list[int] = []
    for loc in proposal.get("locations", []):
        el = slugify(loc.get("title", "location"))
        desc = (f"Known for {loc.get('known_for', '')} "
                f"Local rule: {loc.get('local_rule', '')} "
                f"Best scene: {loc.get('best_scene', '')}").strip()
        dream = card_dream(
            "LOCATION", loc.get("title", "Location"), desc, loc.get("local_rule", ""),
            loc.get("art_direction", ""), "kind-icon:map-pin", el,
            {"title": loc.get("title", ""), "subtitle": "Location",
             "hook": loc.get("art_direction", ""),
             **trio([("Known For", loc.get("known_for", "")),
                     ("Local Rule", loc.get("local_rule", "")),
                     ("Best Scene", loc.get("best_scene", ""))])},
        )
        if dream:
            built["records"]["locations"].append(
                {"model": "Dream", "id": dream.get("id"), "title": loc.get("title")})
            location_ids.append(dream.get("id"))
            loc_id = dream.get("id")
            if world_id and loc_id:
                kr_call("POST", "/api/dream-relations",
                        {"fromDreamId": world_id, "toDreamId": loc_id, "relationType": "CONTAINS"},
                        dry_run, results, f"relation: {title} -> {loc.get('title')} (CONTAINS)")
            if loc_id and genre_id:
                kr_call("POST", "/api/dream-relations",
                        {"fromDreamId": loc_id, "toDreamId": genre_id, "relationType": "RELATED"},
                        dry_run, results, f"relation: {loc.get('title')} -> {vibe.get('title')} (RELATED)")
        queue_art(el, loc.get("title", "Location"),
                  f"{loc.get('art_direction', '')}, {vibe_line}, "
                  f"portrait key-art composition, {HOUSE_PROMPT_TAIL}")

    # 4. Characters (CHARACTER card Dream + real Character row)
    built["records"]["characters"] = []
    for ch in proposal.get("characters", []):
        el = slugify(ch.get("name", "character"))
        dream = card_dream(
            "CHARACTER", ch.get("name", "Character"), ch.get("role_drive", ""),
            ch.get("carries", ""), ch.get("look", ""), "kind-icon:user-round", el,
            {"title": ch.get("name", ""), "subtitle": "Character",
             "hook": ch.get("look", ""),
             **trio([("Wants", ch.get("role_drive", "")),
                     ("Carries", ch.get("carries", "")),
                     ("Complication", ch.get("complication", ""))])},
        )
        link_ids = [i for i in ([dream.get("id")] if dream else []) + [world_id] if i]
        rec = kr_call("POST", "/api/characters", {
            "name": ch.get("name", "Character"), "designer": DESIGNER, "isPublic": True,
            "drive": ch.get("role_drive", ""),
            "quirks": ch.get("complication", ""),
            "backstory": f"Carries {ch.get('carries', '')}. {ch.get('complication', '')}".strip(),
            "artPrompt": ch.get("look", ""),
            "genre": vibe.get("title", ""),
            "dreamIds": link_ids,
        }, dry_run, results, f"Character: {ch.get('name')}")
        if rec:
            built["records"]["characters"].append(
                {"model": "Character", "id": rec.get("id"), "name": ch.get("name")})
        queue_art(el, ch.get("name", "Character"),
                  f"character portrait of {ch.get('name', '')}: {ch.get('look', '')}, "
                  f"in the world of {title} ({vibe_line}), {HOUSE_PROMPT_TAIL}")

    # 5. Narrator (NARRATOR card Dream + real Bot row)
    nar = proposal.get("narrator", {})
    if nar:
        el = slugify(nar.get("name", "narrator")) + "-narrator"
        dream = card_dream(
            "NARRATOR", nar.get("name", "Narrator"), nar.get("personality", ""),
            nar.get("voice", ""), nar.get("appears_as", ""), "kind-icon:book-open", el,
            {"title": nar.get("name", ""), "subtitle": "Narrator bot",
             "hook": nar.get("voice", ""),
             **trio([("Mission", nar.get("personality", "")),
                     ("Appears As", nar.get("appears_as", "")),
                     ("Best For", nar.get("best_for", ""))])},
        )
        link_ids = [i for i in ([dream.get("id")] if dream else []) + [world_id] if i]
        rec = kr_call("POST", "/api/bots", {
            "name": nar.get("name", "Narrator"), "BotType": "NARRATOR",
            "designer": DESIGNER, "isPublic": True,
            "subtitle": f"Narrator of {title}",
            "description": nar.get("personality", ""),
            "botIntro": nar.get("appears_as", ""),
            "userIntro": nar.get("best_for", ""),
            "narrativeVoice": nar.get("voice", ""),
            "personality": nar.get("personality", ""),
            "artPrompt": nar.get("appears_as", ""),
            "prompt": (f"You are {nar.get('name', '')}, narrator of {title}. "
                       f"Voice: {nar.get('voice', '')} "
                       f"Personality: {nar.get('personality', '')} "
                       f"Expressions: {nar.get('expressions', '')} "
                       f"Topics: {'; '.join(nar.get('topics', []))}"),
            "dreamIds": link_ids,
        }, dry_run, results, f"Bot: {nar.get('name')}")
        if rec:
            built["records"]["narrator"] = {"model": "Bot", "id": rec.get("id"),
                                            "name": nar.get("name")}
        queue_art(el, nar.get("name", "Narrator"),
                  f"narrator portrait of {nar.get('name', '')}: {nar.get('appears_as', '')}, "
                  f"{nar.get('personality', '')}, world of {title} ({vibe_line}), {HOUSE_PROMPT_TAIL}")

    # 6. Rewards (REWARD card Dream + real Reward row; one SKILL, one ITEM)
    built["records"]["rewards"] = []
    for rw in proposal.get("rewards", []):
        el = slugify(rw.get("name", "reward"))
        rtype = str(rw.get("reward_type", "ITEM")).upper()
        rarity = str(rw.get("rarity", "COMMON")).upper()
        if rarity not in VALID_RARITIES:
            rarity = "COMMON"
        dream = card_dream(
            "REWARD", rw.get("name", "Reward"), rw.get("grants", ""),
            rw.get("catch", ""), f"{rw.get('name', '')}: {rw.get('grants', '')}",
            "kind-icon:gift", el,
            {"title": rw.get("name", ""), "subtitle": f"{rtype} · {rarity}",
             **trio([("Grants", rw.get("grants", "")),
                     ("Best Used When", rw.get("best_used_when", "")),
                     ("The Catch", rw.get("catch", ""))])},
        )
        link_ids = [i for i in ([dream.get("id")] if dream else []) + [world_id] if i]
        rec = kr_call("POST", "/api/rewards", {
            "name": rw.get("name", "Reward"), "designer": DESIGNER, "isPublic": True,
            "description": rw.get("grants", ""),
            "flavorText": (rw.get("catch", "") or "")[:500],
            "effect": rw.get("grants", ""),
            "icon": "kind-icon:gift",
            "rarity": rarity,
            "rewardType": rtype if rtype in ("SKILL", "ITEM") else "ITEM",
            "artPrompt": f"{rw.get('name', '')}: {rw.get('grants', '')}",
            "dreamIds": link_ids,
        }, dry_run, results, f"Reward: {rw.get('name')}")
        if rec:
            built["records"]["rewards"].append(
                {"model": "Reward", "id": rec.get("id"), "name": rw.get("name"),
                 "reward_type": rtype})
        queue_art(el, rw.get("name", "Reward"),
                  f"iconic treasure-card illustration of {rw.get('name', '')} ({rtype}): "
                  f"{rw.get('grants', '')}, atmospheric background, world of {title} "
                  f"({vibe_line}), {HOUSE_PROMPT_TAIL}")

    # 7. Scenarios (real Scenario rows, linked to the world + locations)
    built["records"]["scenarios"] = []
    loc_titles = ", ".join(l.get("title", "") for l in proposal.get("locations", []))
    scenario_links = [i for i in [world_id, *location_ids] if i]
    for sc in proposal.get("scenarios", []):
        rec = kr_call("POST", "/api/scenarios", {
            "title": (sc.get("title", "Scenario"))[:190], "designer": DESIGNER,
            "isPublic": True,
            "description": sc.get("setup", ""),
            "intros": sc.get("setup", ""),
            "locations": loc_titles,
            "genres": vibe.get("title", ""),
            "dreamIds": scenario_links,
        }, dry_run, results, f"Scenario: {sc.get('title')}")
        if rec:
            built["records"]["scenarios"].append(
                {"model": "Scenario", "id": rec.get("id"), "title": sc.get("title")})

    return built, results, art_entries


# ── Attach pass: patch sheets once art is live ───────────────────────────────

def attach_art(dry_run: bool) -> int:
    """For built proposals, HEAD-check pending art; patch sheet imagePath when live."""
    attached = 0
    for p, fm, text in find_proposals():
        built = _data_block(text, "built-data")
        if not built:
            continue
        changed = False
        for art in built.get("art", []):
            if art.get("attached"):
                continue
            public_path = art.get("public_path", "")
            if not public_path or not head_ok(KR_BASE_URL + public_path):
                continue
            sheet_id = (built.get("sheets") or {}).get(art.get("element"))
            if sheet_id and not dry_run:
                status, resp = http_json("PATCH", f"{KR_BASE_URL}/api/sheets/{sheet_id}",
                                         {"imagePath": public_path})
                if status not in (200, 201):
                    print(f"  attach FAIL {status} sheet {sheet_id} ← {public_path}: "
                          f"{str(resp)[:120]}", file=sys.stderr)
                    continue
            art["attached"] = True
            attached += 1
            changed = True
            print(f"  attached {public_path} → sheet {sheet_id}")
        if changed and not dry_run:
            update_built_data(p, built)
    if attached == 0:
        print("  no new art to attach")
    return attached


# ── Entry point ──────────────────────────────────────────────────────────

def run_build(date_override: Optional[str], dry_run: bool) -> int:
    path, reason = eligible_proposal(date_override)
    if path is None:
        print(f"Nothing to build: {reason}")
        return 0
    if not KR_API_TOKEN and not dry_run:
        print("KR_API_TOKEN not set — cannot create records (soft no-op).", file=sys.stderr)
        return 0
    text = path.read_text(encoding="utf-8")
    fm = _frontmatter(text)
    proposal = _data_block(text, "proposal-data")
    if not proposal:
        print(f"{path.name}: no proposal-data block — cannot auto-build.", file=sys.stderr)
        return 0
    slug = str(fm.get("slug") or slugify(proposal.get("title", "dream")))
    pdate = str(fm.get("proposal_date") or fm.get("created") or "")
    print(f"Building {path.name} (slug={slug}, proposal_date={pdate})"
          f"{' [dry-run]' if dry_run else ''}")

    built, results, art_entries = build_records(proposal, slug, pdate, dry_run)
    failures = [r for r in results if not r["ok"]]
    if not dry_run and failures:
        # Atomic build: never mark a partially-built proposal `built`. Roll back any
        # rows that DID land (e.g. an intermittent DB 503 mid-sequence) so the next
        # sweep retries clean — no orphans, no duplicate dreams. Previously this only
        # bailed when EVERY call failed, so a partial failure shipped an incomplete
        # dream flagged built and never retried.
        n_deleted = rollback_created(results)
        print(f"Build failed: {len(failures)}/{len(results)} call(s) failed; "
              f"rolled back {n_deleted} created row(s); {slug} left UNBUILT for the "
              "next sweep.", file=sys.stderr)
        return 0

    append_art_requests(art_entries, dry_run)
    record_built(path, built, dry_run)
    ok_n = sum(1 for r in results if r["ok"])
    print(f"Done: {ok_n}/{len(results)} API calls ok, {len(art_entries)} art requests queued.")
    return 0


def ensure_records(dry_run: bool = False) -> None:
    """Sweep entry point: build the eligible proposal (if any), then attach art.

    Guarded + soft-failing: safe to call every hourly sweep."""
    try:
        run_build(None, dry_run)
    except Exception as e:  # noqa: BLE001
        print(f"record build skipped: {e}", file=sys.stderr)
    try:
        attach_art(dry_run)
    except Exception as e:  # noqa: BLE001
        print(f"art attach skipped: {e}", file=sys.stderr)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="print actions, write nothing")
    ap.add_argument("--date", default=None, help="build the proposal with this proposal_date")
    ap.add_argument("--attach", action="store_true",
                    help="only run the art-attach pass for built proposals")
    args = ap.parse_args()
    if args.attach:
        attach_art(args.dry_run)
        return 0
    rc = run_build(args.date, args.dry_run)
    attach_art(args.dry_run)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
