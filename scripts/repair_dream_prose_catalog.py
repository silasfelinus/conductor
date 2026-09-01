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

# A reward's index is not fixed by the schema (only "exactly one ITEM and one
# SKILL" is), so reward paths address the row by type and resolve to an index at
# access time. Keys must match the labels dream_prose_quality.complaints() emits,
# because _complaint_fields() maps complaint -> field through this table.
ITEM = {"reward_type": "ITEM"}
SKILL = {"reward_type": "SKILL"}

FIELD_PATHS = {
    "idea": ("idea",),
    "vibe.line": ("vibe", "line"),
    "locations[0].known_for": ("locations", 0, "known_for"),
    "locations[0].local_rule": ("locations", 0, "local_rule"),
    "locations[0].best_scene": ("locations", 0, "best_scene"),
    "characters[0].role_drive": ("characters", 0, "role_drive"),
    "characters[0].carries": ("characters", 0, "carries"),
    "characters[0].complication": ("characters", 0, "complication"),
    "rewards[item].grants": ("rewards", ITEM, "grants"),
    "rewards[item].best_used_when": ("rewards", ITEM, "best_used_when"),
    "rewards[item].catch": ("rewards", ITEM, "catch"),
    "rewards[skill].grants": ("rewards", SKILL, "grants"),
    "rewards[skill].best_used_when": ("rewards", SKILL, "best_used_when"),
    "rewards[skill].catch": ("rewards", SKILL, "catch"),
    "scenarios[0].setup": ("scenarios", 0, "setup"),
}
RESPONSE_KEYS = {
    "idea": "idea",
    "vibe.line": "vibe_line",
    "locations[0].known_for": "known_for",
    "locations[0].local_rule": "local_rule",
    "locations[0].best_scene": "best_scene",
    "characters[0].role_drive": "character_role_drive",
    "characters[0].carries": "character_carries",
    "characters[0].complication": "character_complication",
    "rewards[item].grants": "item_grants",
    "rewards[item].best_used_when": "item_best_used_when",
    "rewards[item].catch": "item_catch",
    "rewards[skill].grants": "skill_grants",
    "rewards[skill].best_used_when": "skill_best_used_when",
    "rewards[skill].catch": "skill_catch",
    "scenarios[0].setup": "scenario_setup",
}


def _resolve_key(container: Any, key: Any) -> Any:
    """Resolve a reward-type selector to a concrete list index."""
    if not isinstance(key, dict):
        return key
    wanted = str(key["reward_type"]).upper()
    for index, row in enumerate(container):
        if isinstance(row, dict) and str(row.get("reward_type") or "").upper() == wanted:
            return index
    raise KeyError(f"no reward with reward_type={wanted}")


def _get(value: Any, path: tuple[Any, ...]) -> Any:
    current = value
    for key in path:
        current = current[_resolve_key(current, key)]
    return current


def _set(value: Any, path: tuple[Any, ...], new_value: Any) -> None:
    current = value
    for key in path[:-1]:
        current = current[_resolve_key(current, key)]
    current[_resolve_key(current, path[-1])] = new_value


def _complaint_fields(proposal: dict[str, Any]) -> list[str]:
    fields: list[str] = []
    for complaint in prose.complaints(proposal):
        label = complaint.split(" ", 1)[0]
        if label in FIELD_PATHS and label not in fields:
            fields.append(label)
    return fields


def _load_built_catalog(backlog: Path | None = None) -> list[dict[str, Any]]:
    # Resolved at call time, never frozen as a default: a default argument binds
    # BACKLOG at import, so redirecting the module attribute silently had no
    # effect and a test once wrote to the real catalog through this path.
    backlog = BACKLOG if backlog is None else backlog
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


def audit(backlog: Path | None = None) -> list[dict[str, Any]]:
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
        "character": (proposal.get("characters") or [{}])[0],
        "rewards": proposal.get("rewards") or [],
        "scenario": (proposal.get("scenarios") or [{}])[0],
    }
    return f"""Repair only the weak user-facing prose fields in this Daily Dream.

The story, names, world logic, and factual meaning are already approved. Do NOT invent a
new premise, rename anything, alter continuity, or add unrelated lore. Expand fragments
just enough that each field explains itself when shown alone on a card. Use complete,
properly capitalized sentences with terminal punctuation. Prefer one vivid substantial
sentence per field. Preserve the voice and concrete imagery already present.

Do NOT write a field as a grammatical continuation of its own name. The card already
prints a label, so `known_for` must not be phrased to follow "known for", `carries` must
not be phrased to follow "carries", and `best_used_when` must not be phrased to follow
"best used when" (nor restate it as "Use it when ..."). Each value has to stand on its
own as a sentence. Referring to other objects in this same bundle by name is fine.

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
    characters = built_records.get("characters") or []
    reward_rows = built_records.get("rewards") or []
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
        # Same shape build_dream_records writes for a fresh build: three complete
        # sentences joined as prose, no "Known for:"/"Local rule:" stems. The
        # labelled breakdown lives on the PitchSheet highlights below.
        description = " ".join(
            str(loc[key]).strip()
            for key in ("known_for", "local_rule", "best_scene")
            if str(loc.get(key) or "").strip()
        )
        revision._patch(
            "/api/dreams",
            _record_id(locations[0]),
            {"description": description, "flavorText": loc["local_rule"]},
        )

    character_fields = {
        "characters[0].role_drive",
        "characters[0].carries",
        "characters[0].complication",
    }
    if field_set & character_fields:
        if len(characters) != 1:
            raise ValueError("prose repair requires exactly one built character row")
        ch = new["characters"][0]
        revision._patch(
            "/api/characters",
            _record_id(characters[0]),
            {
                "drive": ch["role_drive"],
                "quirks": ch["complication"],
                "backstory": " ".join(
                    str(ch[key]).strip()
                    for key in ("carries", "complication")
                    if str(ch.get(key) or "").strip()
                ),
            },
        )

    # `best_used_when` is deliberately absent: build_dream_records never writes it
    # to a Reward row, so it is repaired in the source proposal only.
    for kind in ("ITEM", "SKILL"):
        label = kind.lower()
        if not field_set & {f"rewards[{label}].grants", f"rewards[{label}].catch",
                            f"rewards[{label}].best_used_when"}:
            continue
        row = next(
            (r for r in reward_rows
             if str(r.get("reward_type") or "").upper() == kind), None)
        reward = next(
            (r for r in new.get("rewards", [])
             if str(r.get("reward_type") or "").upper() == kind), None)
        if row is None or reward is None:
            raise ValueError(f"prose repair requires a built {kind} reward row")
        body: dict[str, Any] = {}
        if f"rewards[{label}].grants" in field_set:
            body["description"] = reward["grants"]
            body["effect"] = reward["grants"]
        if f"rewards[{label}].catch" in field_set:
            body["flavorText"] = str(reward["catch"])[:500]
        if body:
            revision._patch("/api/rewards", _record_id(row), body)

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


def typography_findings(backlog: Path | None = None) -> list[dict[str, Any]]:
    """Built bundles whose card copy needs the deterministic typography pass.

    `backlog` resolves at call time rather than as a default argument, so the
    module-level BACKLOG is not frozen at import and callers (and tests) can
    redirect it.
    """
    rows: list[dict[str, Any]] = []
    for bundle in _load_built_catalog(BACKLOG if backlog is None else backlog):
        proposal = bundle["proposal"]
        fields = [
            label for label in FIELD_PATHS
            if _get_or_none(proposal, label) is not None
            and proposals.normalize_typography(_get_or_none(proposal, label))
            != _get_or_none(proposal, label)
        ]
        if fields:
            rows.append({**bundle, "fields": fields})
    return rows


def _get_or_none(proposal: dict[str, Any], label: str) -> Any:
    try:
        return _get(proposal, FIELD_PATHS[label])
    except (KeyError, IndexError, TypeError):
        return None


def _apply_typography(request_path: Path, request: dict[str, Any]) -> list[dict[str, Any]]:
    """Deterministic, model-free presentational pass over built card copy.

    Kept separate from the authored repair because nothing here is a judgement
    call: no ANTHROPIC_API_KEY is needed, no wording changes, and the diff is
    reproducible. Only fields that actually change are patched live.
    """
    results: list[dict[str, Any]] = []
    reason = str(request.get("reason") or "card-copy typography normalisation")
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    for bundle in typography_findings():
        old = bundle["proposal"]
        new = copy.deepcopy(old)
        for label in bundle["fields"]:
            _set(new, FIELD_PATHS[label], proposals.normalize_typography(_get(old, FIELD_PATHS[label])))
        structural = proposals.validate_proposal(proposals.normalize(copy.deepcopy(new), set()))
        remaining = prose.complaints(new)
        if structural or remaining:
            raise RuntimeError(
                f"{bundle['path'].name}: typography pass would break the contract: "
                + "; ".join(structural + remaining)
            )
        built = bundle["built"]
        _patch_live(old, new, built, bundle["fields"])
        built.setdefault("prose_repairs", []).append(
            {"repaired_at": now, "reason": reason, "fields": list(bundle["fields"]),
             "art_unchanged": True, "deterministic": True}
        )
        bundle["path"].write_text(_render_source(new, bundle["day"], built), encoding="utf-8")
        results.append({
            "path": str(bundle["path"].relative_to(ROOT)),
            "day": bundle["day"],
            "title": new.get("title"),
            "fields": bundle["fields"],
            "before": {RESPONSE_KEYS[x]: _get(old, FIELD_PATHS[x]) for x in bundle["fields"]},
            "after": {RESPONSE_KEYS[x]: _get(new, FIELD_PATHS[x]) for x in bundle["fields"]},
        })
        print(f"normalised typography: {new.get('title')} ({', '.join(bundle['fields'])})")

    receipt = dict(request)
    receipt.update({"status": "applied", "applied_at": now,
                    "repaired_bundles": len(results), "results": results,
                    "remaining_typography": [r["day"] for r in typography_findings()]})
    receipt_path = request_path.with_name(request_path.name.replace("-request.json", "-applied.json"))
    receipt_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    request_path.unlink()
    if receipt["remaining_typography"]:
        raise RuntimeError("catalog still has typography findings after the pass")
    return results


def _apply_batch(request_path: Path, request: dict[str, Any]) -> list[dict[str, Any]]:
    if str(request.get("mode") or "") == "typography":
        return _apply_typography(request_path, request)
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
    #
    # Source is written here but production is NOT touched: the live PATCH is a
    # second phase (`--publish`), run only after the workflow has pushed this
    # source to main. Run 33450722225 did it the other way round -- patched 16
    # bundles' live rows, then had its evidence push rejected by GitHub three
    # times -- and left live ahead of source with the repaired `best_used_when`
    # values existing nowhere but a discarded runner working tree. Ordering the
    # durable write first makes that outcome impossible: a failed push now costs
    # a re-run, not a divergence.
    results: list[dict[str, Any]] = []
    reason = str(request.get("reason") or "catalog prose quality repair")
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    for bundle in authored:
        old = bundle["proposal"]
        new = bundle["candidate"]
        built = bundle["built"]
        built.setdefault("prose_repairs", []).append(
            {
                "repaired_at": now,
                "reason": reason,
                "fields": list(bundle["fields"]),
                "art_unchanged": True,
                "live_pending": True,
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
            "status": "source-written",
            "applied_at": now,
            "repaired_bundles": len(results),
            "results": results,
            "remaining_complaints": audit(),
            # Consumed by `--publish` after this source is pushed. Each entry is
            # re-resolved from the committed file, so publishing never depends on
            # runner state that a failed push would discard.
            "pending_live": [
                {"path": r["path"], "fields": r["fields"]} for r in results
            ],
        }
    )
    receipt_path = request_path.with_name(request_path.name.replace("-request.json", "-applied.json"))
    receipt_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    request_path.unlink()
    if receipt["remaining_complaints"]:
        raise RuntimeError("catalog still has prose-quality complaints after repair")
    return results


def publish_live(receipt_path: Path) -> int:
    """Phase two: patch live rows from source that is already committed.

    Split out from the authoring phase so production is only ever touched after
    the repaired source is durable. Re-runnable: a bundle whose `live_pending`
    marker is already cleared is skipped, so a partial run finishes cleanly.
    """
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    pending = receipt.get("pending_live") or []
    if not pending:
        print("No pending live patches in this receipt.")
        return 0
    published: list[str] = []
    for entry in pending:
        path = ROOT / entry["path"]
        text = path.read_text(encoding="utf-8")
        proposal = revision._data_block(text, "proposal-data")
        built = revision._data_block(text, "built-data")
        if not proposal or not built:
            raise RuntimeError(f"{path.name}: cannot publish without proposal and built data")
        repairs = [r for r in (built.get("prose_repairs") or []) if r.get("live_pending")]
        if not repairs:
            print(f"already published: {proposal.get('title')}")
            continue
        # Titles are never repaired, so the committed proposal serves as both
        # sides of the patch; only the repaired fields differ from live.
        _patch_live(proposal, proposal, built, entry["fields"])
        for record in repairs:
            record.pop("live_pending", None)
        day = (revision._frontmatter_value(text, "proposal_date")
               or revision._frontmatter_value(text, "created"))
        path.write_text(_render_source(proposal, day, built), encoding="utf-8")
        published.append(str(proposal.get("title")))
        print(f"published to live: {proposal.get('title')}")
    receipt["status"] = "applied"
    receipt["published_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    receipt["pending_live"] = []
    receipt_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"published {len(published)} bundle(s) to live")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("request", nargs="?", type=Path)
    parser.add_argument("--audit", action="store_true", help="print current built-catalog prose complaints")
    parser.add_argument("--strict", action="store_true", help="return nonzero when audit finds complaints")
    parser.add_argument("--publish", type=Path, metavar="RECEIPT",
                        help="phase two: patch live rows from an already-committed receipt")
    args = parser.parse_args(argv)

    if args.publish:
        try:
            return publish_live(args.publish)
        except (OSError, KeyError, TypeError, ValueError, RuntimeError, json.JSONDecodeError) as error:
            print(f"Daily Dream live publish failed: {error}", file=sys.stderr)
            return 1
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
