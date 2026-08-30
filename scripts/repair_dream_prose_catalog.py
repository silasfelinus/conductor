#!/usr/bin/env python3
"""Audit and repair user-facing prose in already-built Daily Dream bundles.

This lane is intentionally narrower than a creative reset.  It changes only the prose
fields rendered directly on world/location/scenario cards, patches those fields onto the
existing Kind Robots rows and PitchSheets, and leaves titles, slugs, Facet seeds, entity
IDs, art prompts, and current art untouched.

A production request is a small JSON file, normally under
``projects/dream-cycle/prose-repairs/``::

    {
      "scope": "all-built",
      "reason": "catalog prose quality repair",
      "send_digest": false
    }

The script authors *all* repairs first and validates the complete batch before performing
any production PATCH.  This keeps a flaky model response from leaving a half-authored
catalog.
"""
from __future__ import annotations

import argparse
import copy
import datetime
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
import dream_prose_quality as prose  # noqa: E402
import apply_dream_revision as revision  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BACKLOG = ROOT / "projects" / "dream-cycle" / "backlog"

FIELD_PATHS = {
    "idea": ("idea",),
    "vibe.line": ("vibe", "line"),
    "locations[0].known_for": ("locations", 0, "known_for"),
    "locations[0].local_rule": ("locations", 0, "local_rule"),
    "locations[0].best_scene": ("locations", 0, "best_scene"),
    "scenarios[0].setup": ("scenarios", 0, "setup"),
}
RESPONSE_KEYS = {
    "idea": "idea",
    "vibe.line": "vibe_line",
    "locations[0].known_for": "known_for",
    "locations[0].local_rule": "local_rule",
    "locations[0].best_scene": "best_scene",
    "scenarios[0].setup": "scenario_setup",
}


def _get(value: Any, path: tuple[Any, ...]) -> Any:
    current = value
    for key in path:
        current = current[key]
    return current


def _set(value: Any, path: tuple[Any, ...], new_value: Any) -> None:
    current = value
    for key in path[:-1]:
        current = current[key]
    current[path[-1]] = new_value


def _complaint_fields(proposal: dict[str, Any]) -> list[str]:
    fields: list[str] = []
    for complaint in prose.complaints(proposal):
        label = complaint.split(" ", 1)[0]
        if label in FIELD_PATHS and label not in fields:
            fields.append(label)
    return fields


def _load_built_catalog(backlog: Path = BACKLOG) -> list[dict[str, Any]]:
    bundles: list[dict[str, Any]] = []
    for path in sorted(backlog.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        proposal = revision._data_block(text, "proposal-data")
        built = revision._data_block(text, "built-data")
        if not proposal or not built:
            continue
        day = revision._frontmatter_value(text, "proposal_date") or revision._frontmatter_value(
            text, "created"
        )
        bundles.append({"path": path, "text": text, "proposal": proposal, "built": built, "day": day})
    return bundles


def audit(backlog: Path = BACKLOG) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for bundle in _load_built_catalog(backlog):
        proposal = bundle["proposal"]
        complaints = prose.complaints(proposal)
        if not complaints:
            continue
        rows.append(
            {
                "path": str(bundle["path"].relative_to(ROOT)) if bundle["path"].is_relative_to(ROOT) else str(bundle["path"]),
                "day": bundle["day"],
                "title": proposal.get("title"),
                "fields": _complaint_fields(proposal),
                "complaints": complaints,
                "current": {
                    RESPONSE_KEYS[label]: _get(proposal, FIELD_PATHS[label])
                    for label in _complaint_fields(proposal)
                },
            }
        )
    return rows


def _prompt(proposal: dict[str, Any], fields: list[str], complaints: list[str]) -> str:
    requested = {RESPONSE_KEYS[label]: _get(proposal, FIELD_PATHS[label]) for label in fields}
    context = {
        "title": proposal.get("title"),
        "idea": proposal.get("idea"),
        "vibe": proposal.get("vibe"),
        "location": (proposal.get("locations") or [{}])[0],
        "scenario": (proposal.get("scenarios") or [{}])[0],
    }
    return f"""Repair only the weak user-facing prose fields in this Daily Dream.

The story, names, world logic, and factual meaning are already approved. Do NOT invent a
new premise, rename anything, alter continuity, or add unrelated lore. Expand fragments
just enough that each field explains itself when shown alone on a card. Use complete,
properly capitalized sentences with terminal punctuation. Prefer one vivid substantial
sentence per field. Preserve the voice and concrete imagery already present.

Fields that failed the current quality contract:
{json.dumps(complaints, ensure_ascii=False, indent=2)}

Full local context:
{json.dumps(context, ensure_ascii=False, indent=2)}

Rewrite exactly these keys and no others:
{json.dumps(requested, ensure_ascii=False, indent=2)}

Return one JSON object containing exactly these keys: {', '.join(requested)}.
"""


def _author_patch(proposal: dict[str, Any], fields: list[str], api_key: str) -> tuple[dict[str, str], dict[str, Any]]:
    expected = {RESPONSE_KEYS[label] for label in fields}
    complaints = prose.complaints(proposal)
    last_error = ""
    for attempt in range(1, 3):
        try:
            raw = author.call_claude(
                _prompt(proposal, fields, complaints),
                "You are a precise fiction editor. Return JSON only.",
                api_key,
            )
            patch = author.parse_json_object(raw)
            if set(patch) != expected:
                raise ValueError(f"expected keys {sorted(expected)}, got {sorted(patch)}")
            if not all(isinstance(value, str) and value.strip() for value in patch.values()):
                raise ValueError("every repaired field must be a non-empty string")
            candidate = copy.deepcopy(proposal)
            for label in fields:
                _set(candidate, FIELD_PATHS[label], patch[RESPONSE_KEYS[label]].strip())
            structural = proposals.validate_proposal(proposals.normalize(copy.deepcopy(candidate), set()))
            remaining = prose.complaints(candidate)
            if structural or remaining:
                raise ValueError("; ".join(structural + remaining))
            return {key: str(value).strip() for key, value in patch.items()}, candidate
        except (RuntimeError, ValueError, json.JSONDecodeError) as error:
            last_error = str(error)
            if attempt == 2:
                break
    raise RuntimeError(f"could not author a valid prose repair after 2 attempts: {last_error}")


def _record_id(row: Any) -> int:
    return revision._record_id(row)


def _patch_live(old: dict[str, Any], new: dict[str, Any], built: dict[str, Any], fields: list[str]) -> None:
    if not records.KR_API_TOKEN:
        raise RuntimeError("KR_API_TOKEN is required to repair built Daily Dream prose")
    built_records = built.get("records") or {}
    world = built_records.get("world") or {}
    locations = built_records.get("locations") or []
    scenarios = built_records.get("scenarios") or []
    if not world or len(locations) != 1 or len(scenarios) != 1:
        raise ValueError("prose repair requires a canonical built world/location/scenario ledger")

    field_set = set(fields)
    if field_set & {"idea", "vibe.line"}:
        body: dict[str, Any] = {}
        if "idea" in field_set:
            body["description"] = new["idea"]
        if "vibe.line" in field_set:
            body["flavorText"] = new["vibe"]["line"]
        revision._patch("/api/dreams", _record_id(world), body)

    location_fields = {
        "locations[0].known_for",
        "locations[0].local_rule",
        "locations[0].best_scene",
    }
    if field_set & location_fields:
        loc = new["locations"][0]
        description = (
            f"Known for: {loc['known_for']} Local rule: {loc['local_rule']} "
            f"Best scene: {loc['best_scene']}"
        )
        revision._patch(
            "/api/dreams",
            _record_id(locations[0]),
            {"description": description, "flavorText": loc["local_rule"]},
        )

    if "scenarios[0].setup" in field_set:
        setup = new["scenarios"][0]["setup"]
        revision._patch(
            "/api/scenarios",
            _record_id(scenarios[0]),
            {"description": setup, "intros": setup},
        )

    sheets = built.get("sheets") or {}
    world_sheet = sheets.get(str(old.get("slug") or ""))
    old_loc_slug = records.slugify(old["locations"][0]["title"])
    location_sheet = sheets.get(old_loc_slug)
    if world_sheet and field_set & {"idea", "vibe.line"}:
        body = {}
        if "idea" in field_set:
            body["pitch"] = new["idea"]
        if "vibe.line" in field_set:
            body["highlight1Value"] = new["vibe"]["line"]
        revision._patch("/api/sheets", _record_id(world_sheet), body)
    if location_sheet and field_set & location_fields:
        loc = new["locations"][0]
        revision._patch(
            "/api/sheets",
            _record_id(location_sheet),
            {
                "highlight1Value": loc["known_for"],
                "highlight2Value": loc["local_rule"],
                "highlight3Value": loc["best_scene"],
            },
        )


def _render_source(proposal: dict[str, Any], day: str, built: dict[str, Any]) -> str:
    rendered = proposals.render_markdown(proposal, day)
    rendered = re.sub(r"(?m)^status:\s*outline\s*$", "status: built", rendered, count=1)
    built_at = str(built.get("built_at") or "")[:10] or day
    today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    log = (
        "## Build log\n"
        f"- {today} | prose-repair | user-facing prose repaired in source and live rows; art and entity identity unchanged\n"
        f"- {built_at} | records | existing canonical six-row bundle retained in place\n"
        f"- {day} | proposed | deterministic Facet-seeded six-asset bundle\n"
    )
    rendered = re.sub(
        r"## Build log\n.*?(?=\n<!-- proposal-data)",
        log.rstrip(),
        rendered,
        count=1,
        flags=re.DOTALL,
    )
    return rendered.rstrip() + "\n\n<!-- built-data\n" + json.dumps(
        built, ensure_ascii=False, sort_keys=True
    ) + "\n-->\n"


def _apply_batch(request_path: Path, request: dict[str, Any]) -> list[dict[str, Any]]:
    if request.get("scope") != "all-built":
        raise ValueError("only scope='all-built' is supported")
    api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is required to author prose repairs")

    bundles = _load_built_catalog()
    authored: list[dict[str, Any]] = []
    for bundle in bundles:
        proposal = bundle["proposal"]
        fields = _complaint_fields(proposal)
        if not fields:
            continue
        patch, candidate = _author_patch(proposal, fields, api_key)
        authored.append({**bundle, "fields": fields, "patch": patch, "candidate": candidate})
        print(f"authored prose repair: {proposal.get('title')} ({', '.join(fields)})")

    # All model work and validation happens above.  No production mutation occurs before
    # the complete batch has a valid candidate.
    results: list[dict[str, Any]] = []
    reason = str(request.get("reason") or "catalog prose quality repair")
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    for bundle in authored:
        old = bundle["proposal"]
        new = bundle["candidate"]
        built = bundle["built"]
        _patch_live(old, new, built, bundle["fields"])
        built.setdefault("prose_repairs", []).append(
            {
                "repaired_at": now,
                "reason": reason,
                "fields": list(bundle["fields"]),
                "art_unchanged": True,
            }
        )
        bundle["path"].write_text(_render_source(new, bundle["day"], built), encoding="utf-8")
        results.append(
            {
                "path": str(bundle["path"].relative_to(ROOT)),
                "day": bundle["day"],
                "title": new.get("title"),
                "fields": bundle["fields"],
                "before": {RESPONSE_KEYS[label]: _get(old, FIELD_PATHS[label]) for label in bundle["fields"]},
                "after": bundle["patch"],
            }
        )
        print(f"applied prose repair: {new.get('title')}")

    receipt = dict(request)
    receipt.update(
        {
            "status": "applied",
            "applied_at": now,
            "repaired_bundles": len(results),
            "results": results,
            "remaining_complaints": audit(),
        }
    )
    receipt_path = request_path.with_name(request_path.name.replace("-request.json", "-applied.json"))
    receipt_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    request_path.unlink()
    if receipt["remaining_complaints"]:
        raise RuntimeError("catalog still has prose-quality complaints after repair")
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("request", nargs="?", type=Path)
    parser.add_argument("--audit", action="store_true", help="print current built-catalog prose complaints")
    parser.add_argument("--strict", action="store_true", help="return nonzero when audit finds complaints")
    args = parser.parse_args(argv)

    if args.audit:
        rows = audit()
        print(json.dumps({"flagged": len(rows), "bundles": rows}, indent=2, ensure_ascii=False))
        return 1 if args.strict and rows else 0
    if args.request is None:
        parser.error("request path is required unless --audit is used")
    try:
        request = json.loads(args.request.read_text(encoding="utf-8"))
        results = _apply_batch(args.request, request)
        print(f"repaired {len(results)} built Daily Dream bundle(s)")
        return 0
    except (OSError, KeyError, TypeError, ValueError, RuntimeError, json.JSONDecodeError) as error:
        print(f"Daily Dream prose repair failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
