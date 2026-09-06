#!/usr/bin/env python3
"""
creation_burst.py — build one small linked bundle of canonical Kind Robots objects
from a hand-written YAML brief, and queue card art for each of them.

Silas, 2026-09-04: "if there is time left, feel free to just make new objects and
submit art queue requests. Kind Robots always has room if there is nothing to do.
We always want fresh ideas." This is the tool for that idle fallback. It is NOT the
Daily Dream lane: `build_dream_records.py` stays the sole writer of dated Daily
Dream bundles, with its Facet seeds, docket and digest. A burst is a one-off idea
that would otherwise stay a paragraph in someone's head — it lands as real rows a
person can find, remix and build on, with art attached.

The classic bundle is one Character, one ITEM Reward, one SKILL Reward, one
Scenario, all linked to each other, all `designer: creation-burst`, all public.
Since 2026-09-06 a bundle may instead (or also) carry a `characters:` list and a
`locations:` list, with rewards and the scenario optional — the shape a tabletop
party needs: a hero, a companion, and the place they came from, each a real row.

    projects/kind-robots/bursts/<date>-<slug>.yaml
        -> POST /api/dreams       (one LOCATION Dream per `locations:` entry)
        -> POST /api/rewards      (x2 when `rewards:` is present)
        -> POST /api/characters   (rewardIds -> both rewards, dreamIds -> the locations)
        -> POST /api/scenarios    (characterIds -> every character, dreamIds -> the locations)
        -> one staged row per record in projects/art-prompts.yaml `requests:`
           (source: creation-burst, entity_type/entity_id/entity_field)
        -> POST /api/art/queue    (one ArtJob per row, payload.entityArt set so
                                   Kind Robots attaches the ArtImage atomically
                                   when the job completes)
        -> PUT /api/<entity>/:id/facets  (optional `facets:` slugs, verified the
                                   same way apply_daily_dream_facets.py does)
        -> `built:` block written back into the bundle file with every id

Idempotent: a bundle whose `built:` block already names an id for a record skips
that create; a staged row whose id is already in art-prompts.yaml is not staged
twice; an ArtJob is only enqueued for a row without `last_art_job_id`. A failed
create rolls back the rows this run created (newest first), same as the Daily
Dream builder, so a retry starts clean.

Prompts are built with `dream_art_prompts` so the Krea 2 rules that lane learned
the hard way (lead with the visible subject, never a conditional, never a
negation, decide people-or-no-people once) apply here too. `look` fields in the
bundle are therefore required to describe appearance, not function. An element
whose picture is a specific moment rather than a portrait may give its own
`art_prompt:` instead; it is wrapped in the same world/framing/style tail.

Bundle-level knobs: `designer:` (default creation-burst) names who the rows are
credited to; `creation_source:` (default AI) is stamped on the LOCATION Dreams —
use HYBRID when a person seeded the idea and an agent wrote it up.

Dry-run by default. `--live` needs KR_API_TOKEN.

Usage:
    python scripts/creation_burst.py projects/kind-robots/bursts/2026-09-04-dust-choir.yaml
    python scripts/creation_burst.py projects/kind-robots/bursts/*.yaml --live
    python scripts/creation_burst.py <bundle> --live --no-art   # rows only
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Optional

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import consume_art_queue as art  # noqa: E402  (patches the shared consumer core)
import dream_art_prompts as prompts  # noqa: E402

ART_PROMPTS = ROOT / "projects" / "art-prompts.yaml"
DESIGNER = "creation-burst"
SOURCE = "creation-burst"
CARD_SIZE = "512x768"
PAGE_URL = "https://kindrobots.org"
TARGET_REPO = "silasfelinus/kind_robots"
# Below the Daily Dream tier (200) so a morning digest bundle is never queued
# behind an idle-fallback burst, above the generic missing-image drip (0).
PRIORITY = 120
VALID_RARITIES = {"COMMON", "UNCOMMON", "RARE", "EPIC", "LEGENDARY"}
VALID_CREATION_SOURCES = {"HUMAN", "AI", "HYBRID", "UPLOAD", "UNKNOWN"}
# Character stat columns are Rarity enums on the Kind Robots side.
STAT_FIELDS = ("luck", "might", "wits", "grace", "charm", "empathy")
FACET_COLLECTIONS = {
    "character": "characters",
    "reward": "rewards",
    "scenario": "scenarios",
    "dream": "dreams",
}

KR_BASE_URL = art.KR_BASE_URL
KR_API_TOKEN = art.KR_API_TOKEN
http_json = art.http_json


def slugify(value: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", str(value or "").lower()).strip("-")
    return re.sub(r"-{2,}", "-", text) or "item"


def _yq(value: str) -> str:
    """Single-quoted YAML scalar, the style art-prompts.yaml already uses."""
    return "'" + " ".join(str(value or "").split()).replace("'", "''") + "'"


def _text(value: object) -> str:
    return " ".join(str(value or "").split())


# ── Bundle shape ─────────────────────────────────────────────────────────────

def normalize_bundle(bundle: dict[str, Any], name: str = "bundle") -> dict[str, Any]:
    """Return the bundle's elements in list form, whichever shape it was written in.

    The classic shape has a singular `character:`; the party shape has
    `characters:` and `locations:`. Both may appear (the singular one is listed
    first and keeps its legacy `built.character` key so older bundles re-run as
    no-ops). Rewards keep their ITEM+SKILL pair rule when present, and are simply
    absent otherwise. At least one element of any kind is required.
    """
    for key in ("slug", "title", "vibe"):
        if not _text(bundle.get(key)):
            raise ValueError(f"{name}: missing {key!r}")

    characters: list[dict[str, Any]] = []
    legacy = isinstance(bundle.get("character"), dict)
    if legacy:
        characters.append(bundle["character"])
    characters.extend(bundle.get("characters") or [])
    locations = list(bundle.get("locations") or [])
    rewards = list(bundle.get("rewards") or [])
    scenario = bundle.get("scenario") or None

    if not (characters or locations or rewards or scenario):
        raise ValueError(f"{name}: a bundle needs at least one character, location, reward or scenario")
    if rewards and (
        len(rewards) != 2
        or {str(r.get("reward_type", "")).upper() for r in rewards} != {"ITEM", "SKILL"}
    ):
        raise ValueError(f"{name}: rewards must be exactly one ITEM and one SKILL")
    for rw in rewards:
        if not _text(rw.get("look")):
            raise ValueError(f"{name}: reward {rw.get('name')!r} needs a visual `look`")
    for ch in characters:
        if not _text(ch.get("name")):
            raise ValueError(f"{name}: every character needs a `name`")
        if not (_text(ch.get("look")) or _text(ch.get("art_prompt"))):
            raise ValueError(f"{name}: character {ch.get('name')!r} needs a visual `look` or an `art_prompt`")
        for stat in STAT_FIELDS:
            value = _text(ch.get(stat)).upper()
            if value and value not in VALID_RARITIES:
                raise ValueError(f"{name}: character {ch.get('name')!r} {stat} must be one of {sorted(VALID_RARITIES)}")
    for loc in locations:
        if not _text(loc.get("title")):
            raise ValueError(f"{name}: every location needs a `title`")
        if not (_text(loc.get("art_direction")) or _text(loc.get("art_prompt"))):
            raise ValueError(f"{name}: location {loc.get('title')!r} needs an `art_direction` or an `art_prompt`")
    if scenario is not None:
        for key in ("title", "setup"):
            if not _text(scenario.get(key)):
                raise ValueError(f"{name}: scenario needs a `{key}`")

    designer = _text(bundle.get("designer")) or DESIGNER
    creation_source = (_text(bundle.get("creation_source")) or "AI").upper()
    if creation_source not in VALID_CREATION_SOURCES:
        raise ValueError(f"{name}: creation_source must be one of {sorted(VALID_CREATION_SOURCES)}")

    return {
        "characters": characters,
        "locations": locations,
        "rewards": rewards,
        "scenario": scenario,
        "legacy_character": legacy,
        "designer": designer,
        "creation_source": creation_source,
    }


def character_key(index: int, ch: dict[str, Any], legacy: bool) -> str:
    """`built:`/prompt key for one character: the legacy singular keeps `character`."""
    if legacy and index == 0:
        return "character"
    return f"character:{slugify(ch['name'])}"


# ── Kind Robots writes ───────────────────────────────────────────────────────

def kr_create(endpoint: str, body: dict[str, Any], label: str, dry_run: bool,
              created: list[tuple[str, int]]) -> Optional[int]:
    if dry_run:
        print(f"  [dry-run] POST {endpoint}: {label}")
        return None
    status, resp = http_json("POST", f"{KR_BASE_URL}{endpoint}", body)
    data = (resp or {}).get("data") if isinstance(resp, dict) else None
    rid = data.get("id") if isinstance(data, dict) else None
    if status not in (200, 201) or not isinstance(resp, dict) or not resp.get("success") or not rid:
        message = resp.get("message") if isinstance(resp, dict) else resp
        raise RuntimeError(f"POST {endpoint} ({label}) -> HTTP {status}: {message}")
    created.append((endpoint, int(rid)))
    print(f"  created {endpoint}/{rid}: {label}")
    return int(rid)


def apply_facets(entity_type: str, entity_id: int, slugs: list[str], label: str,
                 dry_run: bool) -> list[int]:
    """Attach catalog Facets by slug and return the ids Kind Robots reports.

    A 200 is not proof the Facets landed (dream-cycle/t-026: PUT .../facets once
    ignored facetKeys and answered success over an empty list), so an empty
    response is an error, not a success.
    """
    path = f"/api/{FACET_COLLECTIONS[entity_type]}/{int(entity_id)}/facets"
    if dry_run:
        print(f"  [dry-run] PUT {path}: {label} <- {', '.join(slugs)}")
        return []
    status, resp = http_json("PUT", f"{KR_BASE_URL}{path}", {"facetKeys": list(dict.fromkeys(slugs))})
    rows = (resp or {}).get("data") if isinstance(resp, dict) else None
    ids = [row.get("id") for row in rows if isinstance(row, dict) and isinstance(row.get("id"), int)] if isinstance(rows, list) else []
    if status != 200 or not isinstance(resp, dict) or not resp.get("success") or not ids:
        message = resp.get("message") if isinstance(resp, dict) else resp
        raise RuntimeError(f"PUT {path} ({label}) attached no Facets -> HTTP {status}: {message}")
    print(f"  facets {path}: {len(ids)} attached ({', '.join(slugs)})")
    return ids


def rollback(created: list[tuple[str, int]]) -> None:
    for endpoint, rid in reversed(created):
        status, _ = http_json("DELETE", f"{KR_BASE_URL}{endpoint}/{rid}")
        print(f"  rolled back DELETE {endpoint}/{rid} -> {status}", file=sys.stderr)


# ── Prompt + request construction ────────────────────────────────────────────

def bundle_prompts(bundle: dict[str, Any]) -> dict[str, str]:
    """One Krea 2 prompt per record, keyed the same way `built:` is."""
    shape = normalize_bundle(bundle)
    title = _text(bundle["title"])
    vibe = _text(bundle["vibe"])
    style = _text(bundle.get("style")) or prompts.style_for_world(title)

    def custom(element: dict[str, Any]) -> Optional[str]:
        scene = _text(element.get("art_prompt"))
        return prompts.scene_prompt(scene, title, vibe, style=style) if scene else None

    out: dict[str, str] = {}
    for index, ch in enumerate(shape["characters"]):
        out[character_key(index, ch, shape["legacy_character"])] = custom(ch) or prompts.character_prompt(
            ch["name"], ch.get("look", ""), ch.get("drive", ""), ch.get("carries", ""),
            title, vibe, style=style,
        )
    for loc in shape["locations"]:
        out[f"location:{slugify(loc['title'])}"] = custom(loc) or prompts.location_prompt(
            loc["title"], loc.get("art_direction", ""), loc.get("known_for", ""),
            loc.get("best_scene", ""), title, vibe, style=style,
        )
    for rw in shape["rewards"]:
        out[f"reward:{slugify(rw['name'])}"] = custom(rw) or prompts.reward_prompt(
            rw["name"], rw.get("reward_type", "ITEM"), rw["look"], rw.get("grants", ""),
            rw.get("rarity", "COMMON"), title, vibe, style=style,
        )
    sc = shape["scenario"]
    if sc:
        out["scenario"] = custom(sc) or prompts.scenario_prompt(
            sc["title"], sc["setup"], sc.get("location", ""), title, vibe, style=style,
        )
    return out


def request_row(bundle_slug: str, element_slug: str, label: str, prompt: str,
                entity_type: str, entity_id: int) -> tuple[str, str, str]:
    req_id = f"{SOURCE}-{bundle_slug}-{element_slug}"
    image_path = f"public/images/{SOURCE}/{bundle_slug}/{element_slug}-card.webp"
    text = (
        f"- id: {req_id}\n"
        f"  source: {SOURCE}\n"
        f"  status: pending\n"
        f"  target_repo: {TARGET_REPO}\n"
        f"  image_path: {image_path}\n"
        f"  source_url: /images/{SOURCE}/{bundle_slug}/{element_slug}-card.webp\n"
        f"  page_url: {PAGE_URL}\n"
        f"  variant: card\n"
        f"  engine: krea2\n"
        f"  size: {CARD_SIZE}\n"
        f"  label: {_yq(label)}\n"
        f"  prompt: {_yq(prompt)}\n"
        f"  entity_type: {entity_type}\n"
        f"  entity_id: {int(entity_id)}\n"
        f"  entity_field: imagePath\n"
    )
    return req_id, image_path, text


def staged_ids() -> set[str]:
    if not ART_PROMPTS.exists():
        return set()
    data = yaml.safe_load(ART_PROMPTS.read_text(encoding="utf-8")) or {}
    return {str(r.get("id")) for r in (data.get("requests") or []) if isinstance(r, dict)}


def append_rows(rows: list[str], dry_run: bool) -> None:
    if not rows:
        return
    if dry_run:
        print(f"  [dry-run] would append {len(rows)} request row(s) to {ART_PROMPTS.name}")
        return
    text = ART_PROMPTS.read_text(encoding="utf-8")
    if not re.search(r"(?m)^requests:\s*$", text):
        raise ValueError("art-prompts.yaml has no requests: section")
    # `requests:` is the last top-level section of the file, so appending at the
    # end keeps every row inside it. Guard that assumption rather than trust it.
    sections = re.findall(r"(?m)^([A-Za-z][A-Za-z0-9_-]*):\s*$", text)
    if sections[-1] != "requests":
        raise ValueError(f"requests: is not the last section (last is {sections[-1]!r})")
    if not text.endswith("\n"):
        text += "\n"
    ART_PROMPTS.write_text(text + "".join(rows), encoding="utf-8")
    print(f"  appended {len(rows)} request row(s) to {ART_PROMPTS.relative_to(ROOT)}")


def set_request_job_id(req_id: str, job_id: int) -> None:
    """Record last_art_job_id on one staged row without re-dumping the file."""
    lines = ART_PROMPTS.read_text(encoding="utf-8").splitlines(keepends=True)
    id_pat = re.compile(r"^-\s+id:\s*['\"]?" + re.escape(req_id) + r"['\"]?\s*$")
    for i, line in enumerate(lines):
        if id_pat.match(line):
            lines.insert(i + 1, f"  last_art_job_id: {int(job_id)}\n")
            ART_PROMPTS.write_text("".join(lines), encoding="utf-8")
            return
    raise KeyError(req_id)


def enqueue_card(entry: dict[str, Any], dry_run: bool) -> Optional[int]:
    job = art.entry_to_job(entry)
    job["priority"] = PRIORITY
    job["idempotencyKey"] = entry["id"]
    job["projectSlug"] = "kind-robots"
    job["payload"]["collection"] = f"{SOURCE}/{entry['bundle']}"
    job["payload"]["entityArt"] = {
        "entityType": entry["entity_type"],
        "entityId": int(entry["entity_id"]),
        "field": "imagePath",
        "preserveOriginal": True,
        "mode": "recreate",
    }
    job.pop("resolvedSeed", None)
    if dry_run:
        print(f"  [dry-run] POST /api/art/queue: {entry['id']} ({job['payload']['width']}x{job['payload']['height']})")
        return None
    job_id = art.enqueue(job)
    print(f"  ArtJob {job_id} <- {entry['id']}")
    return int(job_id)


# ── Record bodies ────────────────────────────────────────────────────────────

def _compact(body: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in body.items() if v not in (None, "")}


def location_body(loc: dict[str, Any], art_prompt: str, designer: str,
                  creation_source: str) -> dict[str, Any]:
    """A LOCATION Dream, the same shape the Daily Dream builder writes for its
    locations: the three card-copy sentences joined as prose, the local rule as
    the flavor line, map-pin icon."""
    description = _text(loc.get("description")) or " ".join(
        part for part in (_text(loc.get("known_for")), _text(loc.get("local_rule")), _text(loc.get("best_scene")))
        if part
    )
    return _compact({
        "title": _text(loc["title"]),
        "slug": _text(loc.get("slug")) or None,
        "dreamType": "LOCATION",
        "designer": designer,
        "creationSource": creation_source,
        "isPublic": True,
        "description": description,
        "flavorText": (_text(loc.get("local_rule")) or _text(loc.get("flavor")))[:500] or None,
        "artPrompt": art_prompt,
        "icon": "kind-icon:map-pin",
    })


def character_body(ch: dict[str, Any], art_prompt: str, designer: str,
                   reward_ids: list[int], dream_ids: list[int]) -> dict[str, Any]:
    backstory = _text(ch.get("backstory")) or " ".join(
        p for p in (_text(ch.get("carries")), _text(ch.get("complication"))) if p
    )
    body: dict[str, Any] = {
        "name": _text(ch["name"]),
        "slug": _text(ch.get("slug")) or None,
        "designer": designer,
        "isPublic": True,
        "species": _text(ch.get("species")) or None,
        "gender": _text(ch.get("gender")) or None,
        "presentation": _text(ch.get("presentation")) or None,
        "genre": _text(ch.get("genre")) or None,
        "role": _text(ch.get("role")) or None,
        "title": _text(ch.get("title")) or None,
        "honorific": _text(ch.get("honorific")) or None,
        "class": _text(ch.get("class")) or None,
        "alignment": _text(ch.get("alignment")) or None,
        "drive": _text(ch.get("drive")),
        "backstory": backstory,
        "quirks": _text(ch.get("quirks")),
        "personality": _text(ch.get("personality")),
        "voice": _text(ch.get("voice")),
        "sampleResponse": _text(ch.get("sample_response")) or None,
        "achievements": _text(ch.get("achievements")) or None,
        "artPrompt": art_prompt,
        "rewardIds": reward_ids,
        "dreamIds": dream_ids,
    }
    if ch.get("level") is not None:
        body["level"] = int(ch["level"])
    for stat in STAT_FIELDS:
        value = _text(ch.get(stat)).upper()
        if value:
            body[stat] = value
    return _compact(body)


# ── One bundle ───────────────────────────────────────────────────────────────

def build_bundle(path: Path, live: bool, with_art: bool) -> dict[str, Any]:
    dry_run = not live
    raw = path.read_text(encoding="utf-8")
    bundle = yaml.safe_load(raw)
    shape = normalize_bundle(bundle, path.name)
    characters, locations = shape["characters"], shape["locations"]
    rewards, sc = shape["rewards"], shape["scenario"]
    designer, creation_source = shape["designer"], shape["creation_source"]

    bundle_slug = slugify(bundle["slug"])
    built = dict(bundle.get("built") or {})
    art_prompts = bundle_prompts(bundle)
    created: list[tuple[str, int]] = []
    print(f"== {bundle['title']} ({path.name})")

    try:
        # 1. Locations first, so Characters and the Scenario can link them on create.
        location_ids: list[int] = []
        for loc in locations:
            key = f"location:{slugify(loc['title'])}"
            lid = built.get(key)
            if not lid:
                body = location_body(loc, art_prompts[key], designer, creation_source)
                lid = kr_create("/api/dreams", body, f"Location {loc['title']}", dry_run, created)
                if lid:
                    built[key] = lid
            if lid:
                location_ids.append(int(lid))

        # 2. Rewards, so the Characters can link them on create.
        reward_ids: list[int] = []
        for rw in rewards:
            el = slugify(rw["name"])
            key = f"reward:{el}"
            rtype = str(rw.get("reward_type", "ITEM")).upper()
            rarity = str(rw.get("rarity", "COMMON")).upper()
            rid = built.get(key)
            if not rid:
                body = {
                    "name": _text(rw["name"]),
                    "rewardType": rtype,
                    "rarity": rarity if rarity in VALID_RARITIES else "COMMON",
                    "description": _text(rw.get("grants")),
                    "effect": _text(rw.get("grants")),
                    "flavorText": _text(rw.get("catch"))[:500],
                    "icon": "kind-icon:gift",
                    "artPrompt": art_prompts[key],
                    "isPublic": True,
                }
                rid = kr_create("/api/rewards", body, f"{rtype} {rw['name']}", dry_run, created)
                if rid:
                    built[key] = rid
            if rid:
                reward_ids.append(int(rid))

        # 3. The Characters, carrying the rewards and standing in the locations.
        character_ids: list[int] = []
        for index, ch in enumerate(characters):
            key = character_key(index, ch, shape["legacy_character"])
            cid = built.get(key)
            if not cid:
                body = character_body(ch, art_prompts[key], designer, reward_ids, location_ids)
                cid = kr_create("/api/characters", body, f"Character {ch['name']}", dry_run, created)
                if cid:
                    built[key] = cid
            if cid:
                character_ids.append(int(cid))

        # 4. The Scenario, cast with every Character.
        if sc:
            sid = built.get("scenario")
            if not sid:
                setup = _text(sc["setup"])
                body = {
                    "title": _text(sc["title"])[:190],
                    "description": setup,
                    "intros": setup,
                    "locations": _text(sc.get("location")) or None,
                    "genres": _text(sc.get("genres")) or None,
                    "inspirations": _text(sc.get("inspirations")) or None,
                    "artPrompt": art_prompts["scenario"],
                    "isPublic": True,
                    "characterIds": character_ids,
                    "dreamIds": location_ids,
                }
                body = {k: v for k, v in body.items() if v not in (None, "", [])}
                sid = kr_create("/api/scenarios", body, f"Scenario {sc['title']}", dry_run, created)
                if sid:
                    built["scenario"] = sid
    except Exception:
        if created:
            print(f"  build failed; rolling back {len(created)} row(s)", file=sys.stderr)
            rollback(created)
        raise

    # Every record this bundle owns: (entity_type, element slug, label, prompt key, id, own facets)
    records: list[tuple[str, str, str, str, Optional[int], list[str]]] = []
    for loc in locations:
        key = f"location:{slugify(loc['title'])}"
        records.append(("dream", slugify(loc["title"]), _text(loc["title"]), key, built.get(key),
                        [str(x) for x in (loc.get("facets") or [])]))
    for index, ch in enumerate(characters):
        key = character_key(index, ch, shape["legacy_character"])
        records.append(("character", slugify(ch["name"]), _text(ch["name"]), key, built.get(key),
                        [str(x) for x in (ch.get("facets") or [])]))
    for rw in rewards:
        el = slugify(rw["name"])
        records.append(("reward", el, _text(rw["name"]), f"reward:{el}", built.get(f"reward:{el}"),
                        [str(x) for x in (rw.get("facets") or [])]))
    if sc:
        records.append(("scenario", slugify(sc["title"]) + "-scenario", _text(sc["title"]), "scenario",
                        built.get("scenario"), [str(x) for x in (sc.get("facets") or [])]))

    # 5. Card art: one staged request per row, enqueued with an entity attach.
    art_failures: list[str] = []
    if with_art:
        already = staged_ids()
        rows: list[str] = []
        entries: list[dict[str, Any]] = []
        art_state = dict(built.get("art") or {})
        for entity_type, el, label, prompt_key, entity_id, _ in records:
            if not entity_id:
                print(f"  [dry-run] would stage art for {entity_type} {label}")
                continue
            prompt = art_prompts[prompt_key]
            req_id, image_path, text = request_row(bundle_slug, el, label, prompt, entity_type, int(entity_id))
            if req_id not in already:
                rows.append(text)
            entries.append({
                "id": req_id, "bundle": bundle_slug, "image_path": image_path,
                "prompt": prompt, "engine": "krea2", "size": CARD_SIZE,
                "entity_type": entity_type, "entity_id": int(entity_id), "label": label,
            })
        append_rows(rows, dry_run)
        for entry in entries:
            if art_state.get(entry["id"]):
                print(f"  ArtJob {art_state[entry['id']]} already recorded for {entry['id']}")
                continue
            try:
                job_id = enqueue_card(entry, dry_run)
            except RuntimeError as exc:
                # A rejected prompt (Kind Robots' prompt contract returns 422) must
                # not orphan the rows already created: record what did land, keep
                # the staged row pending for a repaired re-run, and report it.
                art_failures.append(f"{entry['id']}: {exc}")
                print(f"  art NOT queued for {entry['id']}: {exc}", file=sys.stderr)
                continue
            if job_id:
                set_request_job_id(entry["id"], job_id)
                art_state[entry["id"]] = job_id
        if art_state:
            built["art"] = art_state

    # 5b. Facets: bundle-level slugs apply to every row; a row may add its own.
    facet_state = dict(built.get("facets") or {})
    facet_failures: list[str] = []
    bundle_facets = [str(x) for x in (bundle.get("facets") or [])]
    for entity_type, _, label, _, entity_id, own_facets in records:
        slugs = bundle_facets + own_facets
        key = f"{entity_type}:{entity_id}"
        if not slugs or not entity_id:
            continue
        if facet_state.get(key) and set(facet_state[key].get("slugs", [])) == set(slugs):
            continue
        try:
            ids = apply_facets(entity_type, int(entity_id), slugs, label, dry_run)
        except RuntimeError as exc:
            facet_failures.append(str(exc))
            print(f"  facets NOT applied for {label}: {exc}", file=sys.stderr)
            continue
        if not dry_run:
            facet_state[key] = {"slugs": list(dict.fromkeys(slugs)), "facet_ids": ids}
    if facet_state:
        built["facets"] = facet_state

    # 6. Write the built block back so a re-run is a no-op.
    if not dry_run and built:
        stripped = re.sub(r"(?ms)^built:\s*\n(?:[ \t]+.*\n?)*", "", raw).rstrip("\n") + "\n"
        block = yaml.safe_dump({"built": built}, sort_keys=True, default_flow_style=False)
        path.write_text(stripped + "\n" + block, encoding="utf-8")
        print(f"  recorded built ids in {path}")
    if art_failures or facet_failures:
        raise RuntimeError(
            "; ".join(
                ([f"{len(art_failures)} card(s) not queued; fix the prompt and re-run: " + "; ".join(art_failures)] if art_failures else [])
                + ([f"{len(facet_failures)} Facet link(s) failed: " + "; ".join(facet_failures)] if facet_failures else [])
            )
        )
    return built


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("bundles", nargs="+", type=Path, help="bundle YAML file(s)")
    parser.add_argument("--live", action="store_true", help="actually create rows and enqueue art (needs KR_API_TOKEN)")
    parser.add_argument("--no-art", action="store_true", help="create rows only; stage and enqueue no art")
    args = parser.parse_args(argv)
    if args.live and not KR_API_TOKEN:
        print("KR_API_TOKEN is required for --live", file=sys.stderr)
        return 2
    failures = 0
    for path in args.bundles:
        try:
            built = build_bundle(path, live=args.live, with_art=not args.no_art)
            print("  " + json.dumps(built, sort_keys=True))
        except Exception as exc:  # noqa: BLE001 - report and continue to the next bundle
            failures += 1
            print(f"  FAILED {path.name}: {exc}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
