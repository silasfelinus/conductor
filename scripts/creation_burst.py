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

One bundle = one Character, one ITEM Reward, one SKILL Reward, one Scenario, all
linked to each other, all `designer: creation-burst`, all public.

    projects/kind-robots/bursts/<date>-<slug>.yaml
        -> POST /api/rewards      (x2)
        -> POST /api/characters   (rewardIds -> both rewards)
        -> POST /api/scenarios    (characterIds -> the character)
        -> four staged rows in projects/art-prompts.yaml `requests:`
           (source: creation-burst, entity_type/entity_id/entity_field)
        -> POST /api/art/queue    (one ArtJob per row, payload.entityArt set so
                                   Kind Robots attaches the ArtImage atomically
                                   when the job completes)
        -> `built:` block written back into the bundle file with every id

Idempotent: a bundle whose `built:` block already names an id for a record skips
that create; a staged row whose id is already in art-prompts.yaml is not staged
twice; an ArtJob is only enqueued for a row without `last_art_job_id`. A failed
create rolls back the rows this run created (newest first), same as the Daily
Dream builder, so a retry starts clean.

Prompts are built with `dream_art_prompts` so the Krea 2 rules that lane learned
the hard way (lead with the visible subject, never a conditional, never a
negation, decide people-or-no-people once) apply here too. `look` fields in the
bundle are therefore required to describe appearance, not function.

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


def rollback(created: list[tuple[str, int]]) -> None:
    for endpoint, rid in reversed(created):
        status, _ = http_json("DELETE", f"{KR_BASE_URL}{endpoint}/{rid}")
        print(f"  rolled back DELETE {endpoint}/{rid} -> {status}", file=sys.stderr)


# ── Prompt + request construction ────────────────────────────────────────────

def bundle_prompts(bundle: dict[str, Any]) -> dict[str, str]:
    title = _text(bundle["title"])
    vibe = _text(bundle["vibe"])
    style = _text(bundle.get("style")) or prompts.style_for_world(title)
    ch = bundle["character"]
    out = {
        "character": prompts.character_prompt(
            ch["name"], ch["look"], ch.get("drive", ""), ch.get("carries", ""),
            title, vibe, style=style,
        ),
        "scenario": prompts.scenario_prompt(
            bundle["scenario"]["title"], bundle["scenario"]["setup"],
            bundle["scenario"].get("location", ""), title, vibe, style=style,
        ),
    }
    for rw in bundle["rewards"]:
        out[f"reward:{slugify(rw['name'])}"] = prompts.reward_prompt(
            rw["name"], rw.get("reward_type", "ITEM"), rw["look"], rw.get("grants", ""),
            rw.get("rarity", "COMMON"), title, vibe, style=style,
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


# ── One bundle ───────────────────────────────────────────────────────────────

def build_bundle(path: Path, live: bool, with_art: bool) -> dict[str, Any]:
    dry_run = not live
    raw = path.read_text(encoding="utf-8")
    bundle = yaml.safe_load(raw)
    for key in ("slug", "title", "vibe", "character", "rewards", "scenario"):
        if key not in bundle:
            raise ValueError(f"{path.name}: missing {key!r}")
    if len(bundle["rewards"]) != 2 or {str(r.get("reward_type", "")).upper() for r in bundle["rewards"]} != {"ITEM", "SKILL"}:
        raise ValueError(f"{path.name}: rewards must be exactly one ITEM and one SKILL")
    for rw in bundle["rewards"]:
        if not _text(rw.get("look")):
            raise ValueError(f"{path.name}: reward {rw.get('name')!r} needs a visual `look`")
    if not _text(bundle["character"].get("look")):
        raise ValueError(f"{path.name}: character needs a visual `look`")

    bundle_slug = slugify(bundle["slug"])
    built = dict(bundle.get("built") or {})
    art_prompts = bundle_prompts(bundle)
    created: list[tuple[str, int]] = []
    print(f"== {bundle['title']} ({path.name})")

    try:
        # 1. Rewards first, so the Character can link them on create.
        reward_ids: list[int] = []
        for rw in bundle["rewards"]:
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

        # 2. The Character, carrying both rewards.
        ch = bundle["character"]
        cid = built.get("character")
        if not cid:
            backstory = " ".join(p for p in (_text(ch.get("carries")), _text(ch.get("complication"))) if p)
            body = {
                "name": _text(ch["name"]),
                "designer": DESIGNER,
                "isPublic": True,
                "species": _text(ch.get("species")) or None,
                "gender": _text(ch.get("gender")) or None,
                "presentation": _text(ch.get("presentation")) or None,
                "genre": _text(ch.get("genre")) or None,
                "role": _text(ch.get("role")) or None,
                "title": _text(ch.get("title")) or None,
                "drive": _text(ch.get("drive")),
                "backstory": backstory,
                "quirks": _text(ch.get("quirks")),
                "personality": _text(ch.get("personality")),
                "voice": _text(ch.get("voice")),
                "artPrompt": art_prompts["character"],
                "rewardIds": reward_ids,
            }
            body = {k: v for k, v in body.items() if v not in (None, "")}
            cid = kr_create("/api/characters", body, f"Character {ch['name']}", dry_run, created)
            if cid:
                built["character"] = cid

        # 3. The Scenario, cast with the Character.
        sc = bundle["scenario"]
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
                "characterIds": [int(cid)] if cid else [],
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

    # 4. Card art: one staged request per row, enqueued with an entity attach.
    if with_art:
        already = staged_ids()
        rows: list[str] = []
        entries: list[dict[str, Any]] = []
        targets = [
            ("character", slugify(ch["name"]), _text(ch["name"]), art_prompts["character"], built.get("character")),
            ("scenario", slugify(sc["title"]) + "-scenario", _text(sc["title"]), art_prompts["scenario"], built.get("scenario")),
        ]
        for rw in bundle["rewards"]:
            el = slugify(rw["name"])
            targets.append(("reward", el, _text(rw["name"]), art_prompts[f"reward:{el}"], built.get(f"reward:{el}")))
        art_state = dict(built.get("art") or {})
        for entity_type, el, label, prompt, entity_id in targets:
            if not entity_id:
                print(f"  [dry-run] would stage art for {entity_type} {label}")
                continue
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
            job_id = enqueue_card(entry, dry_run)
            if job_id:
                set_request_job_id(entry["id"], job_id)
                art_state[entry["id"]] = job_id
        if art_state:
            built["art"] = art_state

    # 5. Write the built block back so a re-run is a no-op.
    if not dry_run and built:
        stripped = re.sub(r"(?ms)^built:\s*\n(?:[ \t]+.*\n?)*", "", raw).rstrip("\n") + "\n"
        block = yaml.safe_dump({"built": built}, sort_keys=True, default_flow_style=False)
        path.write_text(stripped + "\n" + block, encoding="utf-8")
        print(f"  recorded built ids in {path}")
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
