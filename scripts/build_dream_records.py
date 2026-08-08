#!/usr/bin/env python3
"""
Build one eligible dated Daily Dream proposal into real kind_robots records.

The current bundle is exact: one PITCH world, one LOCATION Dream, one real
Character, one ITEM Reward, one SKILL Reward, and one Scenario. Daily Dream
proposals do not create narrator Bots, shadow Dreams, or a GENRE Dream row.

Hourly Conductor is the only caller. The transaction records every resulting
ID in proposal built-data, rolls back owned rows after a partial failure, and
queues exactly six stable art requests. Facets and art attachment enrich the
recorded bundle afterward. The daily digest is read-only.

Usage:
  python scripts/build_dream_records.py
  python scripts/build_dream_records.py --dry-run
  python scripts/build_dream_records.py --date YYYY-MM-DD
  python scripts/build_dream_records.py --attach

Environment:
  KR_API_TOKEN   required for live record creation and attachment
  KR_BASE_URL    defaults to https://kind-robots.vercel.app
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
import urllib.parse
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
# Rendered images live on the self-hosted media origin (200); the app origin
# only 307-redirects /images/, so HEAD-check the media origin directly.
KR_MEDIA_ORIGIN = os.environ.get(
    "KR_MEDIA_ORIGIN", "https://media.acrocatranch.com").rstrip("/")
KR_API_TOKEN = os.environ.get("KR_API_TOKEN", "").strip()
DESIGNER = "dream-cycle"
# The dated proposal lane authors dreams autonomously, so its rows are AI, not HUMAN. Override to HYBRID via env when the loop
# builds a Silas-seeded proposal. See specs/SLUG-POLICY.md (creationSource note).
CREATION_SOURCE = os.environ.get("DREAM_CREATION_SOURCE", "AI").strip().upper() or "AI"
PAGE_URL = KR_BASE_URL

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


REQUIRED_SEED_ASSETS = {"vibe", "location", "character", "reward_item", "reward_skill", "scenario"}


def _canonical_proposal_errors(proposal: Optional[dict]) -> list[str]:
    """Return violations of the exact version-2 six-asset input contract."""
    if not isinstance(proposal, dict):
        return ["missing or invalid proposal-data block"]
    errors: list[str] = []
    facets = proposal.get("seed_facets")
    if not isinstance(facets, dict) or int(facets.get("version") or 0) < 2:
        errors.append("seed_facets.version must be at least 2")
    elements = facets.get("elements") if isinstance(facets, dict) else None
    if not isinstance(elements, dict) or not REQUIRED_SEED_ASSETS.issubset(elements):
        errors.append("seed_facets.elements must cover all six assets")
    vibe = proposal.get("vibe")
    if not isinstance(vibe, dict) or not vibe.get("title") or not vibe.get("line"):
        errors.append("one complete vibe is required")
    for field, expected in (("locations", 1), ("characters", 1), ("rewards", 2), ("scenarios", 1)):
        value = proposal.get(field)
        actual = len(value) if isinstance(value, list) else 0
        if actual != expected:
            errors.append(f"{field} has {actual}; expected exactly {expected}")
    rewards = proposal.get("rewards") if isinstance(proposal.get("rewards"), list) else []
    reward_types = {
        str(row.get("reward_type", "")).upper()
        for row in rewards if isinstance(row, dict)
    }
    if reward_types != {"ITEM", "SKILL"}:
        errors.append("rewards must contain exactly one ITEM and one SKILL")
    if proposal.get("narrator"):
        errors.append("Daily Dream proposals must not contain a narrator")
    return errors


def _outcome(status: str, message: str, **details: Any) -> dict[str, Any]:
    """Return the small, serializable contract consumed by the hourly report.

    ``failed`` is deliberately distinct from ``idle``.  Before this contract the
    scheduler could roll back a broken build, print an error, and still finish green;
    neither GitHub nor the next digest retained evidence that creation had failed.
    """
    return {"status": status, "message": message, **details}


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
    """Choose the proposal to build.

    A proposal whose previous attempt failed stays at the head of the line until it
    succeeds.  Otherwise a new calendar day could strand yesterday's creation simply
    because a newer proposal now exists.
    """
    today = datetime.datetime.now(_TZ).date().isoformat()
    best: Optional[tuple[str, Path]] = None
    retry: Optional[tuple[str, Path]] = None
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
        proposal = _data_block(text, "proposal-data")
        contract_errors = _canonical_proposal_errors(proposal)
        if contract_errors:
            reason = f"{p.name}: invalid canonical proposal — " + "; ".join(contract_errors)
            continue
        if _data_block(text, "built-data"):
            continue  # already built
        if has_silas_notes(text):
            reason = f"{p.name}: has Notes from Silas — agent must fold them in before building"
            continue
        attempt = _data_block(text, "build-attempt-data")
        if isinstance(attempt, dict) and attempt.get("status") == "retry":
            if retry is None or pdate < retry[0]:
                retry = (pdate, p)
            continue
        if best is None or pdate > best[0]:
            best = (pdate, p)
    if retry:
        return retry[1], ""
    if best:
        return best[1], ""
    return None, reason


_LEADING_ARTICLES = ("the-", "a-", "an-")


def slugify(text: str) -> str:
    """kebab-case a title per specs/SLUG-POLICY.md. Drops a leading article
    (the-/a-/an-) unless doing so would leave a single bare word (so genuine
    two-word proper names like `the-marrow` / `the-tangle` survive; multi-word
    `the-comet-market` becomes `comet-market`)."""
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    s = re.sub(r"-{2,}", "-", s)
    for art in _LEADING_ARTICLES:
        if s.startswith(art):
            rest = s[len(art):]
            if rest and "-" in rest:  # still ≥2 words after strip → drop article
                s = rest
            break
    return s or "element"


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


def _art_request_id(entry: str) -> Optional[str]:
    """Extract one request ID from a comment-preserving YAML fragment."""
    match = re.search(r"(?m)^-\s+id:\s*(['\"]?)([^'\"\n]+)\1\s*$", entry)
    return match.group(2).strip() if match else None


def append_art_requests(entries: list[str], dry_run: bool) -> None:
    if not entries:
        return
    text = ART_PROMPTS.read_text(encoding="utf-8")
    if "\nrequests:" not in text and not text.startswith("requests:"):
        text += "\nrequests:\n"

    # Only inspect the requests collection. Other top-level collections can
    # legitimately contain unrelated id fields.
    request_header = re.search(r"(?m)^requests:\s*$", text)
    if request_header is None:
        raise ValueError("art prompt queue has no requests section")
    request_start = request_header.end()
    next_section = re.search(
        r"(?m)^[A-Za-z][A-Za-z0-9_-]*:\s*$",
        text[request_start:],
    )
    insertion = request_start + next_section.start() if next_section else len(text)
    request_id_pattern = re.compile(
        r"(?m)^-\s+id:\s*(['\"]?)([^'\"\n]+)\1\s*$"
    )
    existing_ids = {
        match.group(2).strip()
        for match in request_id_pattern.finditer(text[request_start:insertion])
    }

    unique_entries: list[str] = []
    seen_ids = set(existing_ids)
    skipped = 0
    for entry in entries:
        request_id = _art_request_id(entry)
        if request_id and request_id in seen_ids:
            skipped += 1
            continue
        if request_id:
            seen_ids.add(request_id)
        unique_entries.append(entry)

    if not unique_entries:
        print(f"  skipped {skipped} already-queued art request(s)")
        return

    request_yaml = "".join(unique_entries)
    if next_section:
        before = text[:insertion].rstrip() + "\n"
        after = text[insertion:].lstrip("\n")
        text = before + request_yaml + "\n" + after
    else:
        if not text.endswith("\n"):
            text += "\n"
        text += request_yaml
    if dry_run:
        print(
            f"  [dry-run] would append {len(unique_entries)} art request(s) "
            f"and skip {skipped} duplicate(s)"
        )
        return
    ART_PROMPTS.write_text(text, encoding="utf-8")
    print(
        f"  appended {len(unique_entries)} art request(s) "
        f"and skipped {skipped} duplicate(s)"
    )

# ── Backlog file bookkeeping ───────────────────────────────────────────

def record_built(path: Path, built: dict, dry_run: bool) -> None:
    """Flip status→built, append Build log line, embed built-data JSON."""
    text = path.read_text(encoding="utf-8")
    today = datetime.datetime.now(_TZ).date().isoformat()
    text = re.sub(r"^status:\s*.+$", "status: built", text, count=1, flags=re.MULTILINE)
    text = re.sub(
        r"\n?<!--\s*build-attempt-data\s*\n.*?\n-->\n?",
        "\n",
        text,
        count=1,
        flags=re.DOTALL,
    )
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


def record_build_failure(path: Path, failure: dict[str, Any], dry_run: bool) -> None:
    """Persist a retry marker without pretending that any object was created."""
    if dry_run:
        return
    text = path.read_text(encoding="utf-8")
    block = f"<!-- build-attempt-data\n{json.dumps(failure, ensure_ascii=False)}\n-->"
    text, count = re.subn(
        r"<!--\s*build-attempt-data\s*\n.*?\n-->",
        block,
        text,
        count=1,
        flags=re.DOTALL,
    )
    if not count:
        text = text.rstrip() + "\n\n" + block + "\n"
    path.write_text(text, encoding="utf-8")


def update_built_data(path: Path, built: dict) -> None:
    text = path.read_text(encoding="utf-8")
    new_block = f"<!-- built-data\n{json.dumps(built, ensure_ascii=False)}\n-->"
    text, n = re.subn(r"<!--\s*built-data\s*\n.*?\n-->", new_block, text, count=1, flags=re.DOTALL)
    if n:
        path.write_text(text, encoding="utf-8")


# ── Record creation (kind_robots REST) ─────────────────────────────────────
# Contracts verified against kind_robots server/api/* (2026-08-02):
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
               if r.get("ok") and r.get("created") and r.get("id")]
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


def _matching_existing(endpoint: str, identity: dict[str, Any]) -> Optional[dict]:
    """Return one exact live row after a create conflict, or None.

    A retry may encounter rows created by an earlier attempt whose ledger commit
    was lost.  Adoption is intentionally stricter than the API's uniqueness rule:
    every supplied identity field must equal the live value.  A same-name row with
    different content remains a failure and is never silently claimed.
    """
    params: dict[str, str] = {}
    if endpoint == "/api/dreams":
        params = {
            "search": str(identity.get("title") or ""),
            "mine": "true",
            "includeInactive": "true",
            "includeMature": "true",
            "take": "200",
        }
    elif endpoint == "/api/bots":
        params = {"pageSize": "1000"}
    query = f"?{urllib.parse.urlencode(params)}" if params else ""
    status, resp = http_json("GET", f"{KR_BASE_URL}{endpoint}{query}")
    if status != 200 or not isinstance(resp, dict):
        return None
    rows = resp.get("data")
    if isinstance(rows, dict):
        rows = rows.get("rows") or rows.get("items") or rows.get("bot")
    if isinstance(rows, dict):
        rows = [rows]
    if not isinstance(rows, list):
        return None
    matches = [
        row for row in rows
        if isinstance(row, dict)
        and all(row.get(key) == value for key, value in identity.items())
    ]
    return matches[0] if len(matches) == 1 else None


def kr_call(method: str, endpoint: str, body: dict, dry_run: bool,
            results: list, label: str = "",
            conflict_identity: Optional[dict[str, Any]] = None) -> Optional[dict]:
    """One API call; returns the record dict from data (with id) or None.

    Each result carries `id` + `delete_base` so a failed build can roll back the rows
    it already created (see rollback_created)."""
    if dry_run:
        print(f"  [dry-run] {method} {endpoint}: {label}")
        results.append({"endpoint": endpoint, "status": 0, "ok": True, "label": label,
                        "id": None, "delete_base": _delete_base(endpoint),
                        "created": False})
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
    adopted = False
    if status == 409 and conflict_identity:
        record = _matching_existing(endpoint, conflict_identity)
        adopted = record is not None
        if adopted:
            print(f"  adopted existing: {label} (ID {record.get('id')})")
    ok = (status in (200, 201, 207) and record is not None) or adopted
    # DreamRelation POST is an upsert but always returns 201, including when the
    # edge already existed. Treat it as non-owned: deleting a newly-created Dream
    # cascades its edge during rollback, while deleting an adopted edge would damage
    # the interrupted build we are recovering.
    created = (
        ok and not adopted and status in (201, 207)
        and endpoint != "/api/dream-relations"
    )
    failure_message = None
    if not ok:
        if isinstance(resp, dict):
            failure_message = str(resp.get("message") or resp.get("error") or resp)
        else:
            failure_message = str(resp)
    results.append({"endpoint": endpoint, "status": status, "ok": ok, "label": label,
                    "id": record.get("id") if (ok and isinstance(record, dict)) else None,
                    "delete_base": _delete_base(endpoint),
                    "created": created,
                    "adopted": adopted,
                    "message": failure_message})
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

    # Dream slugs are globally unique in kind_robots; two same-titled elements
    # (e.g. a world and a location both named "The Comet Market") would collide
    # (409). Pass an explicit slug per dream, de-duplicated within this build.
    used_slugs: set[str] = set()
    # Art request IDs and paths have the same collision risk. Keep the world on
    # the canonical slug, then suffix a colliding child with its semantic kind
    # (Lantern Post world + LOCATION becomes lantern-post-location).
    used_art_slugs: set[str] = set()

    def uniq_slug(base: str) -> str:
        s = slugify(base) or "dream"
        out, n = s, 2
        while out in used_slugs:
            out, n = f"{s}-{n}", n + 1
        used_slugs.add(out)
        return out

    def uniq_art_slug(base: str, kind: str) -> str:
        s = slugify(base) or "element"
        out = s
        if out in used_art_slugs:
            suffix = slugify(kind) or "element"
            out = f"{s}-{suffix}"
            n = 2
            while out in used_art_slugs:
                out = f"{s}-{suffix}-{n}"
                n += 1
        used_art_slugs.add(out)
        return out

    def queue_art(element_slug: str, element_kind: str, label: str, art_prompt: str,
                  target_endpoint: str, target_id: Optional[int]) -> None:
        # Art attaches to the created entity's own imagePath (a Dream for the
        # world/locations, or the real Character/Bot/Reward/Scenario row) — not
        # to a shadow dream's PitchSheet. The durable request carries the target
        # entity metadata so Kind Robots can attach the ArtImage atomically when
        # the ArtJob completes; attach_art remains a legacy/static-path fallback.
        resolved_art_slug = uniq_art_slug(element_slug, element_kind)
        req_id, image_path, yaml_text = art_request_entry(
            slug, resolved_art_slug, label, art_prompt
        )
        entity_type = {
            "/api/dreams": "dream",
            "/api/characters": "character",
            "/api/bots": "bot",
            "/api/rewards": "reward",
            "/api/scenarios": "scenario",
        }.get(target_endpoint)
        if entity_type and target_id is not None:
            yaml_text += (
                f"  entity_type: {entity_type}\n"
                f"  entity_id: {int(target_id)}\n"
                f"  entity_field: imagePath\n"
            )
        art_entries.append(yaml_text)
        built["art"].append({"request_id": req_id, "image_path": image_path,
                             "public_path": "/" + image_path.removeprefix("public/"),
                             "attached": False, "element": resolved_art_slug,
                             "entity_type": entity_type, "entity_id": target_id,
                             "entity_field": "imagePath",
                             "target_endpoint": target_endpoint, "target_id": target_id})

    def card_dream(dream_type: str, dtitle: str, description: str, flavor: str,
                   art_prompt: str, icon: str, element_slug: str,
                   sheet_overrides: dict, dream_slug: Optional[str] = None) -> Optional[dict]:
        """Create a card Dream + its PitchSheet (via by-dream). Returns the dream.

        `dream_slug` pins an explicit, policy-clean slug (used for the world card,
        which must own the proposal's canonical slug so it never collides with a
        same-titled LOCATION — the old bug behind `comet-market` + `the-comet-market-2`).
        Callers that omit it get a de-duplicated slugify of the title. See
        specs/SLUG-POLICY.md."""
        resolved_slug = dream_slug or uniq_slug(dtitle)
        dream_body = {
            "title": dtitle, "slug": resolved_slug,
            "dreamType": dream_type, "designer": DESIGNER, "creationSource": CREATION_SOURCE,
            "isPublic": True, "description": description,
            "flavorText": flavor[:500] if flavor else None,
            "artPrompt": art_prompt or None, "icon": icon,
        }
        dream = kr_call(
            "POST", "/api/dreams", dream_body, dry_run, results,
            f"{dream_type} dream: {dtitle}",
            conflict_identity={
                "title": dtitle,
                "slug": resolved_slug,
                "dreamType": dream_type,
                "designer": DESIGNER,
                "description": description,
            },
        )
        if not dream:
            return None
        sheet_body = {
            "designer": DESIGNER, "isPublic": True,
            # extraData is a String @db.LongText column — send JSON as a string,
            # not a raw object (an object 400s with a Prisma-invalid error).
            "extraData": json.dumps({**extra_base, "elementType": dream_type,
                                     "element": element_slug}),
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
    #    It OWNS the proposal's canonical slug (registered first) so a same-titled
    #    LOCATION can never steal it and get a `-2`/`the-` collision slug instead
    #    (specs/SLUG-POLICY.md rule 4).
    world_slug = slugify(slug)
    used_slugs.add(world_slug)
    world = card_dream(
        "PITCH", title, proposal.get("idea", ""), vibe_line,
        f"establishing key art for {title}: {vibe_line}, {HOUSE_PROMPT_TAIL}",
        "kind-icon:moon", slug,
        {"title": title, "hook": vibe.get("title", ""), "pitch": proposal.get("idea", ""),
         **trio([("Promise", vibe_line),
                 ("Builds Into", "one location, one character, two rewards, one scenario"),
                 ("Status", f"proposed {pdate}, built by dream-cycle")])},
        dream_slug=world_slug,
    )
    if world:
        built["records"]["world"] = {"model": "Dream", "id": world.get("id"), "title": title}
        queue_art(slug, "world", title,
                  f"establishing key art for the world of {title}: {proposal.get('idea', '')} "
                  f"{vibe_line}, portrait key-art composition, {HOUSE_PROMPT_TAIL}",
                  "/api/dreams", world.get("id"))
    world_id = world.get("id") if world else None

    # 2. The authored vibe describes the world. Reusable genre/style/theme data
    #    lives in Facets now; apply_daily_dream_facets.py attaches the proposal's
    #    persisted seed Facets after these records are created. Do not recreate the
    #    retired GENRE Dream type as a shadow row.

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
        queue_art(el, "location", loc.get("title", "Location"),
                  f"{loc.get('art_direction', '')}, {vibe_line}, "
                  f"portrait key-art composition, {HOUSE_PROMPT_TAIL}",
                  "/api/dreams", dream.get("id") if dream else None)

    # 4. Characters (real Character rows linked to the world Dream — no
    #    shadow CHARACTER dream; art attaches to the Character's own imagePath).
    built["records"]["characters"] = []
    link_ids = [world_id] if world_id else []
    for ch in proposal.get("characters", []):
        el = slugify(ch.get("name", "character"))
        character_body = {
            "name": ch.get("name", "Character"), "designer": DESIGNER, "isPublic": True,
            "drive": ch.get("role_drive", ""),
            "quirks": ch.get("complication", ""),
            "backstory": f"Carries {ch.get('carries', '')}. {ch.get('complication', '')}".strip(),
            "artPrompt": ch.get("look", ""),
            "genre": vibe.get("title", ""),
            "dreamIds": link_ids,
        }
        rec = kr_call(
            "POST", "/api/characters", character_body, dry_run, results,
            f"Character: {ch.get('name')}",
            conflict_identity={key: character_body[key] for key in
                               ("name", "designer", "drive", "artPrompt")},
        )
        if rec:
            built["records"]["characters"].append(
                {"model": "Character", "id": rec.get("id"), "name": ch.get("name")})
        queue_art(el, "character", ch.get("name", "Character"),
                  f"character portrait of {ch.get('name', '')}: {ch.get('look', '')}, "
                  f"in the world of {title} ({vibe_line}), {HOUSE_PROMPT_TAIL}",
                  "/api/characters", rec.get("id") if rec else None)

    # 5. Rewards (one SKILL and one ITEM; art attaches to each real Reward)
    built["records"]["rewards"] = []
    for rw in proposal.get("rewards", []):
        el = slugify(rw.get("name", "reward"))
        rtype = str(rw.get("reward_type", "ITEM")).upper()
        rarity = str(rw.get("rarity", "COMMON")).upper()
        if rarity not in VALID_RARITIES:
            rarity = "COMMON"
        link_ids = [world_id] if world_id else []
        reward_body = {
            "name": rw.get("name", "Reward"), "isPublic": True,
            "description": rw.get("grants", ""),
            "flavorText": (rw.get("catch", "") or "")[:500],
            "effect": rw.get("grants", ""),
            "icon": "kind-icon:gift",
            "rarity": rarity,
            "rewardType": rtype if rtype in ("SKILL", "ITEM") else "ITEM",
            "artPrompt": f"{rw.get('name', '')}: {rw.get('grants', '')}",
            "dreamIds": link_ids,
        }
        rec = kr_call(
            "POST", "/api/rewards", reward_body, dry_run, results,
            f"Reward: {rw.get('name')}",
            conflict_identity={key: reward_body[key] for key in
                               ("name", "description", "rewardType", "artPrompt")},
        )
        if rec:
            built["records"]["rewards"].append(
                {"model": "Reward", "id": rec.get("id"), "name": rw.get("name"),
                 "reward_type": rtype})
        queue_art(el, "reward", rw.get("name", "Reward"),
                  f"iconic treasure-card illustration of {rw.get('name', '')} ({rtype}): "
                  f"{rw.get('grants', '')}, atmospheric background, world of {title} "
                  f"({vibe_line}), {HOUSE_PROMPT_TAIL}",
                  "/api/rewards", rec.get("id") if rec else None)

    # 6. Scenario (one real Scenario linked to the world and location)
    built["records"]["scenarios"] = []
    loc_titles = ", ".join(l.get("title", "") for l in proposal.get("locations", []))
    scenario_links = [i for i in [world_id, *location_ids] if i]
    for sc in proposal.get("scenarios", []):
        el = slugify(sc.get("title", "scenario")) + "-scenario"
        setup = sc.get("setup", "")
        scenario_body = {
            "title": (sc.get("title", "Scenario"))[:190], "isPublic": True,
            "description": setup,
            "intros": setup,
            "locations": loc_titles,
            "genres": vibe.get("title", ""),
            "dreamIds": scenario_links,
        }
        rec = kr_call(
            "POST", "/api/scenarios", scenario_body, dry_run, results,
            f"Scenario: {sc.get('title')}",
            conflict_identity={
                "title": scenario_body["title"],
                "description": scenario_body["description"],
                # The API normalizes a plain intro string to a JSON-array string.
                "intros": json.dumps([setup], ensure_ascii=False),
                "locations": scenario_body["locations"],
            },
        )
        if rec:
            built["records"]["scenarios"].append(
                {"model": "Scenario", "id": rec.get("id"), "title": sc.get("title")})
        queue_art(el, "scenario", sc.get("title", "Scenario"),
                  f"establishing scene art for {sc.get('title', '')}: {sc.get('setup', '')}, "
                  f"world of {title} ({vibe_line}), {HOUSE_PROMPT_TAIL}",
                  "/api/scenarios", rec.get("id") if rec else None)

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
            if not public_path or not head_ok(KR_MEDIA_ORIGIN + public_path):
                continue
            # Attach to the created entity's own imagePath (Dream / Character /
            # Bot / Reward / Scenario). Fall back to the legacy sheet target for
            # any art queued before this pipeline change.
            endpoint = art.get("target_endpoint")
            target_id = art.get("target_id")
            if not (endpoint and target_id):
                sheet_id = (built.get("sheets") or {}).get(art.get("element"))
                if sheet_id:
                    endpoint, target_id = "/api/sheets", sheet_id
            if not (endpoint and target_id):
                continue
            if not dry_run:
                status, resp = http_json("PATCH", f"{KR_BASE_URL}{endpoint}/{target_id}",
                                         {"imagePath": public_path})
                if status not in (200, 201):
                    print(f"  attach FAIL {status} {endpoint}/{target_id} ← {public_path}: "
                          f"{str(resp)[:120]}", file=sys.stderr)
                    continue
            art["attached"] = True
            attached += 1
            changed = True
            print(f"  attached {public_path} → {endpoint}/{target_id}")
        if changed and not dry_run:
            update_built_data(p, built)
    if attached == 0:
        print("  no new art to attach")
    return attached


# ── Entry point ──────────────────────────────────────────────────────────

def run_build(date_override: Optional[str], dry_run: bool) -> dict[str, Any]:
    path, reason = eligible_proposal(date_override)
    if path is None:
        print(f"Nothing to build: {reason}")
        return _outcome("idle", reason)
    if not KR_API_TOKEN and not dry_run:
        message = "KR_API_TOKEN not set — daily objects cannot be created."
        failure = {
            "status": "retry",
            "attempted_at": datetime.datetime.now(_TZ).isoformat(),
            "message": message,
        }
        record_build_failure(path, failure, dry_run)
        print(message, file=sys.stderr)
        return _outcome("failed", message, proposal=path.name, retry=True)
    text = path.read_text(encoding="utf-8")
    fm = _frontmatter(text)
    proposal = _data_block(text, "proposal-data")
    contract_errors = _canonical_proposal_errors(proposal)
    if contract_errors:
        message = f"{path.name}: invalid canonical proposal — " + "; ".join(contract_errors)
        failure = {
            "status": "retry",
            "attempted_at": datetime.datetime.now(_TZ).isoformat(),
            "message": message,
        }
        record_build_failure(path, failure, dry_run)
        print(message, file=sys.stderr)
        return _outcome("failed", message, proposal=path.name, retry=True)
    slug = str(fm.get("slug") or slugify(proposal.get("title", "dream")))
    pdate = str(fm.get("proposal_date") or fm.get("created") or "")
    print(f"Building {path.name} (slug={slug}, proposal_date={pdate})"
          f"{' [dry-run]' if dry_run else ''}")

    try:
        built, results, art_entries = build_records(proposal, slug, pdate, dry_run)
    except Exception as error:  # noqa: BLE001 - persist the retry before surfacing it
        message = f"{slug}: object creation crashed before the bundle could be recorded: {error}"
        failure = {
            "status": "retry",
            "attempted_at": datetime.datetime.now(_TZ).isoformat(),
            "message": message,
        }
        record_build_failure(path, failure, dry_run)
        print(message, file=sys.stderr)
        return _outcome("failed", message, proposal=path.name, retry=True)
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
        statuses = sorted({int(row.get("status") or 0) for row in failures})
        message = (
            f"{slug}: {len(failures)}/{len(results)} API calls failed "
            f"(HTTP {', '.join(map(str, statuses))}); rolled back {n_deleted} rows."
        )
        failure = {
            "status": "retry",
            "attempted_at": datetime.datetime.now(_TZ).isoformat(),
            "message": message,
            "failed_calls": [
                {
                    "endpoint": row.get("endpoint"),
                    "status": row.get("status"),
                    "label": row.get("label"),
                    "message": row.get("message"),
                }
                for row in failures
            ],
            "rolled_back": n_deleted,
        }
        record_build_failure(path, failure, dry_run)
        return _outcome(
            "failed",
            message,
            proposal=path.name,
            retry=True,
            failed_calls=len(failures),
            rolled_back=n_deleted,
        )

    append_art_requests(art_entries, dry_run)
    record_built(path, built, dry_run)
    ok_n = sum(1 for r in results if r["ok"])
    print(f"Done: {ok_n}/{len(results)} API calls ok, {len(art_entries)} art requests queued.")
    return _outcome(
        "dry-run" if dry_run else "built",
        f"{slug}: created and recorded the bundle; queued {len(art_entries)} art requests.",
        proposal=path.name,
        built_at=built.get("built_at"),
        api_calls=ok_n,
        art_requests=len(art_entries),
    )


def ensure_records(dry_run: bool = False) -> dict[str, Any]:
    """Sweep entry point: build the eligible proposal (if any), then attach art.

    Guarded + soft-failing: safe to call every hourly sweep."""
    try:
        outcome = run_build(None, dry_run)
    except Exception as e:  # noqa: BLE001
        message = f"Daily-dream build crashed before it could record a bundle: {e}"
        print(message, file=sys.stderr)
        outcome = _outcome("failed", message, retry=True)
    try:
        outcome["art_attached"] = attach_art(dry_run)
    except Exception as e:  # noqa: BLE001
        print(f"art attach skipped: {e}", file=sys.stderr)
        outcome["art_attach_error"] = str(e)
    return outcome


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
    outcome = run_build(args.date, args.dry_run)
    attach_art(args.dry_run)
    return 1 if outcome.get("status") == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
