#!/usr/bin/env python3
"""Apply human-requested creative revisions to Daily Dream proposals.

A revision request may replace an unbuilt steering proposal, or revise an already-built
bundle in place by PATCHing its recorded Kind Robots entities. Built revisions preserve
the deterministic Facet seed and technical world slug, supersede the old six art requests,
and enqueue six fresh requests against the same entity IDs.

Request files are JSON objects ending in ``-request.json`` with:

{
  "proposal_path": "projects/dream-cycle/backlog/2026-08-27-old.md",
  "digest_role": "Tomorrow steering",
  "send_digest": true,
  "proposal": { ... canonical six-asset proposal ... }
}

Successful requests are renamed to ``-applied.json`` as durable receipts.
"""
from __future__ import annotations

import argparse
import datetime
import html
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import author_dream_proposal as author  # noqa: E402
import build_dream_proposal as proposals  # noqa: E402
import build_dream_records as records  # noqa: E402
from dream_art_prompts import (  # noqa: E402
    character_prompt,
    location_prompt,
    reward_prompt,
    scenario_prompt,
    world_prompt,
)

ROOT = Path(__file__).resolve().parents[1]
BACKLOG = ROOT / "projects" / "dream-cycle" / "backlog"
EMAIL_PATH = ROOT / "creative-reset-email.json"
REVISION_STAMP = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _data_block(text: str, name: str) -> dict[str, Any] | None:
    match = re.search(rf"<!--\s*{re.escape(name)}\s*\n(.*?)\n-->", text, re.DOTALL)
    if not match:
        return None
    try:
        value = json.loads(match.group(1))
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def _frontmatter_value(text: str, key: str) -> str:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*['\"]?([^'\"\n]+)['\"]?\s*$", text)
    return match.group(1).strip() if match else ""


def _creative_validation(
    proposal: dict[str, Any],
    day: str,
    *,
    premise_history: list[str] | None = None,
    name_history: dict[str, list[str]] | None = None,
) -> list[str]:
    complaints = proposals.validate_proposal(proposal)
    premise_history = (
        author.recent_premise_history(day) if premise_history is None else premise_history
    )
    name_history = author.recent_name_history(day) if name_history is None else name_history
    complaints.extend(
        author.story_diversity_complaints(
            proposal,
            premise_history,
            proposal.get("seed_facets") if isinstance(proposal, dict) else None,
        )
    )
    characters = proposal.get("characters") if isinstance(proposal, dict) else None
    if isinstance(characters, list) and characters and isinstance(characters[0], dict):
        complaints.extend(
            author.name_diversity_complaints(
                str(characters[0].get("name") or ""),
                name_history.get("characters", []),
            )
        )
    return complaints


def lacks_canonical_seed(proposal: dict[str, Any]) -> bool:
    """True for a pre-v2 bundle whose seed block cannot be preserved because it never existed.

    The four 2026-07 bundles left over from the retired eight-stage experiment have no
    `seed_facets` at all. "Preserve the seed exactly" is unsatisfiable for them, so a
    legacy reseed draws the plan their own date would deterministically produce today
    (`build_dream_proposal.facet_seed_plan`) rather than inventing one.
    """
    return any(
        error.startswith("seed_facets")
        for error in proposals.validate_proposal(dict(proposal or {}))
    )


def validate_revision(
    old_proposal: dict[str, Any],
    new_proposal: dict[str, Any],
    day: str,
    *,
    built: bool,
    legacy_reseed: bool = False,
    premise_history: list[str] | None = None,
    name_history: dict[str, list[str]] | None = None,
) -> None:
    if new_proposal.get("seed_facets") != old_proposal.get("seed_facets"):
        if not (legacy_reseed and lacks_canonical_seed(old_proposal)):
            raise ValueError("revision must preserve seed_facets exactly")
        if lacks_canonical_seed(new_proposal):
            raise ValueError("a legacy reseed must supply a valid version-2 seed block")
    if built and new_proposal.get("slug") != old_proposal.get("slug"):
        raise ValueError("a built revision must preserve the technical world slug")
    complaints = _creative_validation(
        new_proposal,
        day,
        premise_history=premise_history,
        name_history=name_history,
    )
    if complaints:
        raise ValueError("creative revision failed validation:\n- " + "\n- ".join(complaints))


def _patch(endpoint: str, entity_id: int, body: dict[str, Any]) -> None:
    status, response = records.http_json(
        "PATCH", f"{records.KR_BASE_URL}{endpoint}/{entity_id}", body
    )
    if status not in (200, 201):
        raise RuntimeError(
            f"PATCH {endpoint}/{entity_id} failed with {status}: {str(response)[:300]}"
        )
    print(f"  patched {endpoint}/{entity_id}")


def _row_is_live(endpoint: str, entity_id: int) -> bool:
    status, _ = records.http_json("GET", f"{records.KR_BASE_URL}{endpoint}/{entity_id}")
    return status == 200


def _retire(endpoint: str, entity_id: int) -> bool:
    """Take a superseded legacy row out of circulation without deleting it."""
    status, _ = records.http_json(
        "PATCH",
        f"{records.KR_BASE_URL}{endpoint}/{entity_id}",
        {"isActive": False, "isPublic": False},
    )
    if status in (200, 201):
        print(f"  retired {endpoint}/{entity_id}")
        return True
    print(f"  WARNING: could not retire {endpoint}/{entity_id} (status {status})")
    return False


def _first_live(rows: list[dict[str, Any]], endpoint: str) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    """(row to remaster, rows superseded). Skips rows whose record is already gone."""
    chosen: dict[str, Any] | None = None
    rest: list[dict[str, Any]] = []
    for row in rows:
        try:
            entity_id = _record_id(row)
        except (TypeError, ValueError):
            continue
        if chosen is None and _row_is_live(endpoint, entity_id):
            chosen = row
            continue
        rest.append(row)
    return chosen, rest


def _record_id(value: Any) -> int:
    if isinstance(value, dict):
        value = value.get("id")
    parsed = int(value)
    if parsed <= 0:
        raise ValueError(f"invalid built entity id: {value!r}")
    return parsed


def _quoted(value: str) -> str:
    return "'" + str(value).replace("'", "''") + "'"


def _art_entry(
    *,
    world_slug: str,
    element_slug: str,
    label: str,
    prompt: str,
    entity_type: str,
    entity_id: int,
    revision_stamp: str,
) -> tuple[dict[str, Any], str]:
    request_id = (
        f"dream-cycle-revision-{world_slug}-{revision_stamp.lower()}-{element_slug}"
    )
    image_path = (
        f"public/images/dreams/{world_slug}/revisions/{revision_stamp.lower()}/"
        f"{element_slug}-card.webp"
    )
    public_path = "/" + image_path.removeprefix("public/")
    yaml_text = (
        f"- id: {request_id}\n"
        "  source: dream-cycle\n"
        "  status: pending\n"
        "  target_repo: silasfelinus/kind_robots\n"
        f"  image_path: {image_path}\n"
        f"  source_url: {public_path}\n"
        f"  page_url: {records.PAGE_URL}\n"
        "  variant: card\n"
        f"  size: {records.CARD_SIZE}\n"
        f"  label: {_quoted(label)}\n"
        f"  prompt: {_quoted(' '.join(prompt.split()))}\n"
        f"  entity_type: {entity_type}\n"
        f"  entity_id: {entity_id}\n"
        "  entity_field: imagePath\n"
    )
    evidence = {
        "request_id": request_id,
        "image_path": image_path,
        "public_path": public_path,
        "attached": False,
        "element": element_slug,
        "entity_type": entity_type,
        "entity_id": entity_id,
        "entity_field": "imagePath",
        "target_endpoint": f"/api/{entity_type}s" if entity_type != "dream" else "/api/dreams",
        "target_id": entity_id,
    }
    return evidence, yaml_text


def _patch_built_bundle(
    old_proposal: dict[str, Any],
    new_proposal: dict[str, Any],
    built_data: dict[str, Any],
    *,
    revision_stamp: str,
    legacy: bool = False,
) -> dict[str, Any]:
    if not records.KR_API_TOKEN:
        raise RuntimeError("KR_API_TOKEN is required to revise a built Daily Dream")

    built_records = built_data.get("records") or {}
    world_row = built_records.get("world") or {}
    location_rows = built_records.get("locations") or []
    character_rows = built_records.get("characters") or []
    reward_rows = built_records.get("rewards") or []
    scenario_rows = built_records.get("scenarios") or []
    canonical = (
        world_row
        and len(location_rows) == 1
        and len(character_rows) == 1
        and len(reward_rows) == 2
        and len(scenario_rows) == 1
    )
    if not canonical and not legacy:
        raise ValueError("built-data does not describe the canonical six-asset bundle")

    superseded: list[dict[str, Any]] = []
    if not canonical:
        # A pre-v2 staged bundle carries a second vibe Dream, extra locations, extra
        # characters, and a second Scenario. Remaster the canonical six; retire the rest
        # rather than leaving two contradictory locations under one remastered world.
        location_row, extra_locations = _first_live(location_rows, "/api/dreams")
        character_row, extra_characters = _first_live(character_rows, "/api/characters")
        scenario_row, extra_scenarios = _first_live(scenario_rows, "/api/scenarios")
        if not (world_row and location_row and character_row and scenario_row):
            raise ValueError(
                "legacy bundle has no live row for one of world/location/character/scenario"
            )
        if len(reward_rows) != 2:
            raise ValueError("legacy bundle does not carry exactly one ITEM and one SKILL Reward")
        location_rows = [location_row]
        character_rows = [character_row]
        scenario_rows = [scenario_row]
        for rows, endpoint in (
            (extra_locations, "/api/dreams"),
            (extra_characters, "/api/characters"),
            (extra_scenarios, "/api/scenarios"),
        ):
            for row in rows:
                superseded.append({"endpoint": endpoint, "row": row})
        legacy_vibe = built_records.get("vibe")
        if isinstance(legacy_vibe, dict) and legacy_vibe.get("id") != world_row.get("id"):
            superseded.append({"endpoint": "/api/dreams", "row": legacy_vibe})
        # Canonicalize the ledger itself, so this bundle is an ordinary six-asset bundle
        # from here on and never needs the legacy path again.
        built_records["locations"] = location_rows
        built_records["characters"] = character_rows
        built_records["scenarios"] = scenario_rows
        built_records.pop("vibe", None)

    title = str(new_proposal["title"])
    vibe = new_proposal["vibe"]
    vibe_line = str(vibe["line"])
    loc = new_proposal["locations"][0]
    ch = new_proposal["characters"][0]
    item = next(row for row in new_proposal["rewards"] if row["reward_type"] == "ITEM")
    skill = next(row for row in new_proposal["rewards"] if row["reward_type"] == "SKILL")
    sc = new_proposal["scenarios"][0]

    world_id = _record_id(world_row)
    location_id = _record_id(location_rows[0])
    character_id = _record_id(character_rows[0])
    reward_by_type = {
        str(row.get("reward_type") or "").upper(): _record_id(row) for row in reward_rows
    }
    item_id = reward_by_type["ITEM"]
    skill_id = reward_by_type["SKILL"]
    scenario_id = _record_id(scenario_rows[0])

    world_art = world_prompt(title, new_proposal["idea"], vibe_line, vibe["art_direction"])
    location_art = location_prompt(
        loc["title"], loc["art_direction"], loc["known_for"], loc["best_scene"], title, vibe_line
    )
    character_art = character_prompt(
        ch["name"], ch["look"], ch["role_drive"], ch["carries"], title, vibe_line
    )
    item_art = reward_prompt(
        item["name"], "ITEM", item["look"], item["grants"], item["rarity"], title, vibe_line
    )
    skill_art = reward_prompt(
        skill["name"], "SKILL", skill["look"], skill["grants"], skill["rarity"], title, vibe_line
    )
    scenario_art = scenario_prompt(
        sc["title"], sc["setup"], loc["title"], title, vibe_line
    )

    _patch(
        "/api/dreams",
        world_id,
        {
            "title": title,
            "description": new_proposal["idea"],
            "flavorText": vibe_line,
            "artPrompt": world_art,
        },
    )
    location_description = (
        f"Known for {loc['known_for']} Local rule: {loc['local_rule']} "
        f"Best scene: {loc['best_scene']}"
    )
    _patch(
        "/api/dreams",
        location_id,
        {
            "title": loc["title"],
            "description": location_description,
            "flavorText": loc["local_rule"],
            "artPrompt": location_art,
        },
    )
    _patch(
        "/api/characters",
        character_id,
        {
            "name": ch["name"],
            "drive": ch["role_drive"],
            "quirks": ch["complication"],
            "backstory": f"Carries {ch['carries']}. {ch['complication']}",
            "artPrompt": character_art,
            "genre": vibe["title"],
        },
    )
    for reward, reward_id, reward_art in (
        (item, item_id, item_art),
        (skill, skill_id, skill_art),
    ):
        _patch(
            "/api/rewards",
            reward_id,
            {
                "name": reward["name"],
                "description": reward["grants"],
                "flavorText": reward["catch"],
                "effect": reward["grants"],
                "rarity": reward["rarity"],
                "rewardType": reward["reward_type"],
                "artPrompt": reward_art,
            },
        )
    _patch(
        "/api/scenarios",
        scenario_id,
        {
            "title": sc["title"],
            "description": sc["setup"],
            "intros": sc["setup"],
            "locations": loc["title"],
            "genres": vibe["title"],
            "artPrompt": scenario_art,
        },
    )

    sheets = built_data.get("sheets") or {}
    old_slug = str(old_proposal.get("slug") or "")
    old_loc_slug = records.slugify(old_proposal["locations"][0]["title"])
    world_sheet = sheets.get(old_slug)
    location_sheet = sheets.get(old_loc_slug)
    if world_sheet:
        _patch(
            "/api/sheets",
            _record_id(world_sheet),
            {
                "title": title,
                "hook": vibe["title"],
                "pitch": new_proposal["idea"],
                "highlight1Label": "Promise",
                "highlight1Value": vibe_line,
                "highlight2Label": "Builds Into",
                "highlight2Value": "one location, one character, two rewards, one scenario",
                "highlight3Label": "Status",
                "highlight3Value": "creatively revised after human feedback",
            },
        )
    if location_sheet:
        _patch(
            "/api/sheets",
            _record_id(location_sheet),
            {
                "title": loc["title"],
                "subtitle": "Location",
                "hook": loc["art_direction"],
                "highlight1Label": "Known For",
                "highlight1Value": loc["known_for"],
                "highlight2Label": "Local Rule",
                "highlight2Value": loc["local_rule"],
                "highlight3Label": "Best Scene",
                "highlight3Value": loc["best_scene"],
            },
        )

    if superseded:
        retired: list[dict[str, Any]] = []
        for entry in superseded:
            row = entry["row"]
            try:
                entity_id = _record_id(row)
            except (TypeError, ValueError):
                continue
            ok = _retire(entry["endpoint"], entity_id)
            retired.append(
                {
                    "endpoint": entry["endpoint"],
                    "id": entity_id,
                    "label": row.get("title") or row.get("name"),
                    "retired": ok,
                    "reason": "superseded by the legacy canonicalization remaster",
                }
            )
        built_data.setdefault("retired_legacy_rows", []).extend(retired)
        # Narrator Bots are a different subsystem and stay for the separately scoped
        # cleanup PIPELINE.md describes; they are only recorded here.
        narrator = (built_data.get("records") or {}).get("narrator")
        if isinstance(narrator, dict):
            built_data.setdefault("legacy_narrator_left_in_place", narrator)

    world_slug = str(old_proposal["slug"])
    art_specs = [
        (records.slugify(title), title, world_art, "dream", world_id),
        (records.slugify(loc["title"]), loc["title"], location_art, "dream", location_id),
        (records.slugify(ch["name"]), ch["name"], character_art, "character", character_id),
        (records.slugify(item["name"]), item["name"], item_art, "reward", item_id),
        (records.slugify(skill["name"]), skill["name"], skill_art, "reward", skill_id),
        (records.slugify(sc["title"]) + "-scenario", sc["title"], scenario_art, "scenario", scenario_id),
    ]
    fresh_art: list[dict[str, Any]] = []
    yaml_entries: list[str] = []
    used: set[str] = set()
    for element_slug, label, prompt, entity_type, entity_id in art_specs:
        base = element_slug
        suffix = 2
        while element_slug in used:
            element_slug = f"{base}-{suffix}"
            suffix += 1
        used.add(element_slug)
        evidence, yaml_text = _art_entry(
            world_slug=world_slug,
            element_slug=element_slug,
            label=label,
            prompt=prompt,
            entity_type=entity_type,
            entity_id=entity_id,
            revision_stamp=revision_stamp,
        )
        fresh_art.append(evidence)
        yaml_entries.append(yaml_text)
    records.append_art_requests(yaml_entries, dry_run=False)

    old_art = list(built_data.get("art") or [])
    if old_art:
        built_data.setdefault("superseded_art", []).extend(old_art)
    built_data["art"] = fresh_art
    built_data.setdefault("revisions", []).append(
        {
            "revised_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "reason": "creative reset after human feedback: escape repeated ledger/filing motif",
            "title": title,
            "art_request_ids": [row["request_id"] for row in fresh_art],
        }
    )
    world_row["title"] = title
    location_rows[0]["title"] = loc["title"]
    character_rows[0]["name"] = ch["name"]
    for row in reward_rows:
        rtype = str(row.get("reward_type") or "").upper()
        row["name"] = item["name"] if rtype == "ITEM" else skill["name"]
    scenario_rows[0]["title"] = sc["title"]
    return built_data


def _render_source(
    proposal: dict[str, Any],
    day: str,
    *,
    built_data: dict[str, Any] | None,
) -> str:
    rendered = proposals.render_markdown(proposal, day)
    if not built_data:
        return rendered
    rendered = re.sub(r"(?m)^status:\s*outline\s*$", "status: built", rendered, count=1)
    built_at = str(built_data.get("built_at") or "")[:10] or day
    log = (
        "## Build log\n"
        f"- {datetime.datetime.now(datetime.timezone.utc).date().isoformat()} | revised | "
        "creative reset after human feedback; existing live rows patched in place and replacement art queued\n"
        f"- {built_at} | records | existing canonical six-row bundle retained and revised in place\n"
        f"- {day} | proposed | deterministic Facet-seeded six-asset bundle\n"
    )
    rendered = re.sub(
        r"## Build log\n.*?(?=\n<!-- proposal-data)",
        log.rstrip(),
        rendered,
        count=1,
        flags=re.DOTALL,
    )
    rendered = rendered.rstrip() + (
        "\n\n<!-- built-data\n"
        + json.dumps(built_data, ensure_ascii=False, sort_keys=True)
        + "\n-->\n"
    )
    return rendered


def apply_request(path: Path) -> dict[str, Any]:
    request = json.loads(path.read_text(encoding="utf-8"))
    proposal_path = ROOT / str(request["proposal_path"])
    if not proposal_path.exists():
        raise FileNotFoundError(f"proposal not found: {proposal_path}")
    old_text = proposal_path.read_text(encoding="utf-8")
    old_proposal = _data_block(old_text, "proposal-data")
    if not old_proposal:
        raise ValueError(f"{proposal_path}: missing proposal-data")
    built_data = _data_block(old_text, "built-data")
    built = built_data is not None or _frontmatter_value(old_text, "status") == "built"
    day = _frontmatter_value(old_text, "proposal_date") or _frontmatter_value(old_text, "created")
    if not day:
        raise ValueError(f"{proposal_path}: missing proposal date")

    legacy_reseed = bool(request.get("legacy_reseed"))
    new_proposal = proposals.normalize(dict(request["proposal"]), set())
    validate_revision(
        old_proposal, new_proposal, day, built=built, legacy_reseed=legacy_reseed
    )

    if built:
        if not built_data:
            raise ValueError("built proposal is missing built-data")
        built_data = _patch_built_bundle(
            old_proposal,
            new_proposal,
            built_data,
            revision_stamp=REVISION_STAMP,
            legacy=legacy_reseed,
        )

    rendered = _render_source(new_proposal, day, built_data=built_data)
    target = proposal_path
    if not built:
        target = BACKLOG / f"{day}-{new_proposal['slug']}.md"
    target.write_text(rendered, encoding="utf-8")
    if target != proposal_path:
        proposal_path.unlink()
        print(f"  replaced {proposal_path.name} -> {target.name}")
    else:
        print(f"  revised {target.name}")

    receipt = dict(request)
    receipt["status"] = "applied"
    receipt["applied_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    receipt["result_path"] = str(target.relative_to(ROOT))
    receipt_path = path.with_name(path.name.replace("-request.json", "-applied.json"))
    receipt_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    path.unlink()
    return {
        "day": day,
        "role": str(request.get("digest_role") or "Revised Daily Dream"),
        "proposal": new_proposal,
        "built": built,
        "send_digest": bool(request.get("send_digest", False)),
    }


def _plain_section(result: dict[str, Any]) -> str:
    p = result["proposal"]
    loc = p["locations"][0]
    ch = p["characters"][0]
    item = next(row for row in p["rewards"] if row["reward_type"] == "ITEM")
    skill = next(row for row in p["rewards"] if row["reward_type"] == "SKILL")
    sc = p["scenarios"][0]
    art_note = (
        "Six replacement art renders are queued against the existing live entities."
        if result["built"]
        else "This steering proposal will use the new per-world visual-style lane when built."
    )
    return "\n".join(
        [
            f"{result['role']}: {p['title']}",
            p["idea"],
            f"Dream vibe: {p['vibe']['title']} — {p['vibe']['line']}",
            f"Location: {loc['title']} — {loc['known_for']}",
            f"Character: {ch['name']} — {ch['role_drive']}",
            f"Reward item: {item['name']} — {item['grants']}",
            f"Reward skill: {skill['name']} — {skill['grants']}",
            f"Scenario: {sc['title']} — {sc['setup']}",
            f"Art: {art_note}",
        ]
    )


def _html_section(result: dict[str, Any]) -> str:
    p = result["proposal"]
    loc = p["locations"][0]
    ch = p["characters"][0]
    item = next(row for row in p["rewards"] if row["reward_type"] == "ITEM")
    skill = next(row for row in p["rewards"] if row["reward_type"] == "SKILL")
    sc = p["scenarios"][0]
    art_note = (
        "Six replacement art renders are queued against the existing live entities."
        if result["built"]
        else "This steering proposal will use the new per-world visual-style lane when built."
    )
    esc = html.escape
    rows = [
        ("Dream vibe", f"{p['vibe']['title']} — {p['vibe']['line']}"),
        ("Location", f"{loc['title']} — {loc['known_for']}"),
        ("Character", f"{ch['name']} — {ch['role_drive']}"),
        ("Reward item", f"{item['name']} — {item['grants']}"),
        ("Reward skill", f"{skill['name']} — {skill['grants']}"),
        ("Scenario", f"{sc['title']} — {sc['setup']}"),
        ("Art", art_note),
    ]
    details = "".join(
        f"<p style='margin:8px 0'><strong>{esc(label)}:</strong> {esc(value)}</p>"
        for label, value in rows
    )
    return (
        "<section style='margin:28px 0;padding:22px;border:1px solid #d7d7df;"
        "border-radius:18px;background:#fff'>"
        f"<div style='font-size:13px;font-weight:700;letter-spacing:.06em;text-transform:uppercase'>"
        f"{esc(result['role'])}</div>"
        f"<h2 style='margin:8px 0 10px'>{esc(p['title'])}</h2>"
        f"<p style='font-size:16px;line-height:1.55'>{esc(p['idea'])}</p>"
        f"{details}</section>"
    )


def write_reset_email(results: list[dict[str, Any]]) -> None:
    if not any(result["send_digest"] for result in results):
        return
    day = datetime.datetime.now(datetime.timezone.utc).astimezone(
        datetime.timezone(datetime.timedelta(hours=-7))
    ).date().isoformat()
    subject = f"Conductor Dream Digest {day} — Creative Reset"
    intro = (
        "The stale records-and-ledgers groove from the earlier digest has been replaced. "
        "This correction intentionally omits The Filing Office at the End of History and "
        "does not reuse its bureaucracy/recordkeeping story machinery."
    )
    text = (
        f"Conductor — Daily Dream Digest Creative Reset ({day})\n\n{intro}\n\n"
        + "\n\n".join(_plain_section(result) for result in results)
        + "\n\nThe deterministic Facet seeds were preserved; the story engines and visual direction changed."
    )
    html_content = (
        "<div style='font-family:system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif;"
        "max-width:760px;margin:0 auto;padding:24px;background:#f6f6fa;color:#17171c'>"
        "<h1 style='margin:0 0 12px'>Daily Dream Creative Reset</h1>"
        f"<p style='font-size:16px;line-height:1.55'>{html.escape(intro)}</p>"
        + "".join(_html_section(result) for result in results)
        + "<p style='font-size:14px;line-height:1.5'>The deterministic Facet seeds were preserved; "
        "the story engines and visual direction changed.</p></div>"
    )
    EMAIL_PATH.write_text(
        json.dumps(
            {"subject": subject, "textContent": text, "htmlContent": html_content},
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote {EMAIL_PATH}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("requests", nargs="+", help="revision request JSON files")
    args = parser.parse_args(argv)
    results: list[dict[str, Any]] = []
    try:
        for value in args.requests:
            results.append(apply_request(Path(value)))
        write_reset_email(results)
    except (OSError, ValueError, RuntimeError, KeyError, TypeError) as error:
        print(f"Daily Dream revision failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
