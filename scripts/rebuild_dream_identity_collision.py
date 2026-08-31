#!/usr/bin/env python3
"""Rebuild Daily Dream bundles whose recorded live IDs were proven stale.

This is a narrow recovery lane for an identity-collision incident.  It does not
invent or revise creative content and it never queues replacement art.  For each
approved bundle it:

1. verifies the current source is an unbuilt, collision-reset proposal;
2. loads the last trustworthy built-data snapshot only as art/history evidence;
3. verifies the live rows that won the collision still belong to their owners;
4. creates/adopts a fresh canonical six-row bundle through build_dream_records;
5. reattaches the already-rendered current art and reapplies the persisted Facets;
6. verifies the fresh live rows, writes new built-data, and leaves a receipt.

Usage:
  python scripts/rebuild_dream_identity_collision.py path/to/*-request.json

Environment:
  KR_API_TOKEN   required for live rebuilds
  KR_BASE_URL    defaults to https://kindrobots.org
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import apply_daily_dream_facets as facets  # noqa: E402
import audit_dream_record_identity as identity  # noqa: E402
import build_dream_records as records  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BACKLOG = ROOT / "projects" / "dream-cycle" / "backlog"
REPAIR_DIR = ROOT / "projects" / "dream-cycle" / "record-repairs"
UTC = datetime.timezone.utc

ROLE_ENDPOINTS = {
    "world": "/api/dreams",
    "location": "/api/dreams",
    "character": "/api/characters",
    "reward_item": "/api/rewards",
    "reward_skill": "/api/rewards",
    "scenario": "/api/scenarios",
}
ROLE_ENTITY_TYPES = {
    "world": "dream",
    "location": "dream",
    "character": "character",
    "reward_item": "reward",
    "reward_skill": "reward",
    "scenario": "scenario",
}
HISTORY_KEYS = ("prose_repairs", "revisions", "remasters", "superseded_art", "retired_legacy_rows")
IDENTITY_RESET_MARKER = "| identity-repair |"


def _now() -> str:
    return datetime.datetime.now(UTC).isoformat()


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def _git_show(ref: str, relative_path: str) -> str:
    if not re.fullmatch(r"[0-9a-fA-F]{7,40}", ref):
        raise ValueError("source_ref must be a commit SHA")
    result = subprocess.run(
        ["git", "show", f"{ref}:{relative_path}"],
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode:
        raise RuntimeError(f"git show {ref}:{relative_path} failed: {result.stderr.strip()}")
    return result.stdout


def _relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def _unwrap_record(response: Any) -> dict[str, Any] | None:
    if not isinstance(response, dict):
        return None
    data = response.get("data")
    if isinstance(data, dict):
        for key in ("dream", "character", "reward", "scenario", "sheet"):
            nested = data.get(key)
            if isinstance(nested, dict):
                return nested
        if "id" in data:
            return data
    return response if "id" in response else None


def _live_get(endpoint: str, record_id: int) -> dict[str, Any]:
    status, response = records.http_json("GET", f"{records.KR_BASE_URL}{endpoint}/{record_id}")
    row = _unwrap_record(response)
    if status != 200 or not row:
        raise RuntimeError(f"GET {endpoint}/{record_id} failed ({status}): {str(response)[:300]}")
    return row


def _expected_label(row: dict[str, Any]) -> str:
    return str(row.get("title") or row.get("name") or "").strip()


def verify_protected_owners(protected: list[dict[str, Any]]) -> list[dict[str, Any]]:
    verified: list[dict[str, Any]] = []
    for item in protected:
        endpoint = str(item.get("endpoint") or "")
        record_id = int(item.get("id") or 0)
        expected = str(item.get("title") or item.get("name") or "").strip()
        if endpoint not in {"/api/dreams", "/api/characters", "/api/rewards", "/api/scenarios"}:
            raise ValueError(f"invalid protected-owner endpoint: {endpoint!r}")
        if record_id <= 0 or not expected:
            raise ValueError("protected owner requires positive id and title/name")
        row = _live_get(endpoint, record_id)
        actual = _expected_label(row)
        if actual != expected:
            raise RuntimeError(
                f"protected owner drift: {endpoint}/{record_id} expected {expected!r}, got {actual!r}"
            )
        verified.append({"endpoint": endpoint, "id": record_id, "label": actual})
    return verified


def role_records(built: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows = built.get("records") if isinstance(built.get("records"), dict) else {}
    locations = rows.get("locations") if isinstance(rows.get("locations"), list) else []
    characters = rows.get("characters") if isinstance(rows.get("characters"), list) else []
    rewards = rows.get("rewards") if isinstance(rows.get("rewards"), list) else []
    scenarios = rows.get("scenarios") if isinstance(rows.get("scenarios"), list) else []
    item = next((row for row in rewards if str(row.get("reward_type") or "").upper() == "ITEM"), None)
    skill = next((row for row in rewards if str(row.get("reward_type") or "").upper() == "SKILL"), None)
    mapped = {
        "world": rows.get("world"),
        "location": locations[0] if len(locations) == 1 else None,
        "character": characters[0] if len(characters) == 1 else None,
        "reward_item": item,
        "reward_skill": skill,
        "scenario": scenarios[0] if len(scenarios) == 1 else None,
    }
    if any(not isinstance(value, dict) or int(value.get("id") or 0) <= 0 for value in mapped.values()):
        raise ValueError("built-data does not contain one complete canonical six-record bundle")
    return {role: value for role, value in mapped.items() if isinstance(value, dict)}


def art_by_role(historical_built: dict[str, Any]) -> dict[str, dict[str, Any]]:
    old_records = role_records(historical_built)
    arts = historical_built.get("art") if isinstance(historical_built.get("art"), list) else []
    mapped: dict[str, dict[str, Any]] = {}
    for role, row in old_records.items():
        old_id = int(row["id"])
        endpoint = ROLE_ENDPOINTS[role]
        matches = [
            art for art in arts
            if isinstance(art, dict)
            and int(art.get("target_id") or art.get("entity_id") or 0) == old_id
            and str(art.get("target_endpoint") or endpoint) == endpoint
        ]
        if len(matches) != 1:
            raise ValueError(f"historical built-data has {len(matches)} current art entries for {role}")
        public_path = str(matches[0].get("public_path") or "")
        if not public_path.startswith("/images/"):
            raise ValueError(f"historical {role} art has invalid public_path: {public_path!r}")
        mapped[role] = dict(matches[0])
    return mapped


def migrated_art(historical_built: dict[str, Any], new_built: dict[str, Any]) -> list[dict[str, Any]]:
    old_art = art_by_role(historical_built)
    fresh = role_records(new_built)
    output: list[dict[str, Any]] = []
    for role in ROLE_ENDPOINTS:
        entry = dict(old_art[role])
        fresh_id = int(fresh[role]["id"])
        entry.update(
            {
                "attached": True,
                "entity_type": ROLE_ENTITY_TYPES[role],
                "entity_id": fresh_id,
                "target_endpoint": ROLE_ENDPOINTS[role],
                "target_id": fresh_id,
                "identity_reused": True,
            }
        )
        output.append(entry)
    return output


def _validate_current_source(path: Path, text: str) -> tuple[dict[str, Any], dict[str, Any]]:
    fm = records._frontmatter(text)
    proposal = records._data_block(text, "proposal-data")
    if fm.get("status") != "outline" or not fm.get("proposal"):
        raise ValueError(f"{_relative(path)} must be a reset outline proposal")
    if records._data_block(text, "built-data") is not None:
        raise ValueError(f"{_relative(path)} unexpectedly has current built-data")
    if IDENTITY_RESET_MARKER not in text:
        raise ValueError(f"{_relative(path)} lacks the identity-repair reset marker")
    errors = records._canonical_proposal_errors(proposal)
    if errors:
        raise ValueError(f"{_relative(path)} proposal is not canonical: {'; '.join(errors)}")
    assert isinstance(proposal, dict)
    return fm, proposal


def _validate_history(current_proposal: dict[str, Any], historical_text: str) -> dict[str, Any]:
    historical_proposal = records._data_block(historical_text, "proposal-data")
    historical_built = records._data_block(historical_text, "built-data")
    if not isinstance(historical_built, dict):
        raise ValueError("historical source has no built-data")
    if historical_proposal != current_proposal:
        raise ValueError("historical source proposal does not match the current collision-reset proposal")
    art_by_role(historical_built)
    return historical_built


def _verify_art_exists(arts: dict[str, dict[str, Any]]) -> None:
    missing = [
        role for role, art in arts.items()
        if not records.head_ok(records.KR_MEDIA_ORIGIN + str(art["public_path"]))
    ]
    if missing:
        raise RuntimeError(f"existing art is not reachable for roles: {', '.join(missing)}")


def _patch(endpoint: str, record_id: int, payload: dict[str, Any]) -> None:
    status, response = records.http_json(
        "PATCH", f"{records.KR_BASE_URL}{endpoint}/{record_id}", payload
    )
    if status not in (200, 201):
        raise RuntimeError(
            f"PATCH {endpoint}/{record_id} failed ({status}): {str(response)[:300]}"
        )


def _attach_existing_art(historical_built: dict[str, Any], new_built: dict[str, Any]) -> None:
    old_art = art_by_role(historical_built)
    fresh = role_records(new_built)
    for role, endpoint in ROLE_ENDPOINTS.items():
        _patch(endpoint, int(fresh[role]["id"]), {"imagePath": old_art[role]["public_path"]})

    sheets = new_built.get("sheets") if isinstance(new_built.get("sheets"), dict) else {}
    world_key = next((key for key in sheets if key == new_built.get("world_slug")), None)
    # build_dream_records keys the world sheet by the technical bundle slug and the
    # location sheet by the location title slug.  Infer them from the two Dream roles
    # so this recovery remains compatible with same-title world/location handling.
    if len(sheets) != 2:
        raise ValueError(f"fresh bundle has {len(sheets)} sheets; expected exactly 2")
    world_element = str(old_art["world"].get("element") or "")
    location_element = str(old_art["location"].get("element") or "")
    world_sheet = sheets.get(world_element)
    location_sheet = sheets.get(location_element)
    if not world_sheet:
        # Historical remaster element names can differ from the technical slug.  The
        # world sheet is always the sheet whose key is the current proposal slug; the
        # caller stores it as identity_bundle_slug before reaching this helper.
        world_sheet = sheets.get(str(new_built.get("identity_bundle_slug") or ""))
    if not location_sheet:
        location_sheet = sheets.get(str(new_built.get("identity_location_slug") or ""))
    if not world_sheet or not location_sheet:
        raise ValueError(f"could not map fresh sheets to world/location: {sheets}")
    _patch("/api/sheets", int(world_sheet), {"imagePath": old_art["world"]["public_path"]})
    _patch("/api/sheets", int(location_sheet), {"imagePath": old_art["location"]["public_path"]})


def _apply_facets(proposal: dict[str, Any], built: dict[str, Any], token: str) -> None:
    targets = facets._record_targets(proposal, built)
    if len(targets) != 6:
        raise ValueError(f"fresh bundle exposes {len(targets)} Facet targets; expected 6")
    applied: list[dict[str, Any]] = []
    for target in targets:
        selection = facets._facet_selection(target["facets"])
        if not selection["facetIds"] and not selection["facetKeys"]:
            raise ValueError(f"{target['element']}: no resolvable Facets")
        result = facets._put(target["path"], selection, token)
        returned = result.get("data") if isinstance(result.get("data"), list) else []
        applied.append(
            {
                "element": target["element"],
                "model": target["model"],
                "record_id": target["record_id"],
                "facet_ids": [
                    row.get("id") for row in returned
                    if isinstance(row, dict) and isinstance(row.get("id"), int)
                ] or selection["facetIds"],
                "facet_keys": selection["facetKeys"],
            }
        )
    built["facet_assignments"] = {
        "status": "complete",
        "seed_version": proposal["seed_facets"].get("version"),
        "applied_at": _now(),
        "targets": applied,
        "errors": [],
    }


def expected_live_labels(proposal: dict[str, Any]) -> dict[str, str]:
    item = next(row for row in proposal["rewards"] if row["reward_type"] == "ITEM")
    skill = next(row for row in proposal["rewards"] if row["reward_type"] == "SKILL")
    return {
        "world": str(proposal["title"]),
        "location": str(proposal["locations"][0]["title"]),
        "character": str(proposal["characters"][0]["name"]),
        "reward_item": str(item["name"]),
        "reward_skill": str(skill["name"]),
        "scenario": str(proposal["scenarios"][0]["title"]),
    }


def verify_fresh_bundle(proposal: dict[str, Any], built: dict[str, Any]) -> list[dict[str, Any]]:
    fresh = role_records(built)
    labels = expected_live_labels(proposal)
    arts = art_by_role(built)
    verified: list[dict[str, Any]] = []
    for role, endpoint in ROLE_ENDPOINTS.items():
        record_id = int(fresh[role]["id"])
        row = _live_get(endpoint, record_id)
        actual = _expected_label(row)
        if actual != labels[role]:
            raise RuntimeError(
                f"fresh {role} {endpoint}/{record_id} expected {labels[role]!r}, got {actual!r}"
            )
        image_path = str(row.get("imagePath") or "")
        expected_path = str(arts[role]["public_path"])
        if image_path != expected_path:
            raise RuntimeError(
                f"fresh {role} {endpoint}/{record_id} image mismatch: {image_path!r} != {expected_path!r}"
            )
        verified.append(
            {"role": role, "endpoint": endpoint, "id": record_id, "label": actual, "imagePath": image_path}
        )
    return verified


def _write_built_source(path: Path, built: dict[str, Any]) -> None:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"^status:\s*.+$", "status: built", text, count=1, flags=re.MULTILINE)
    log = (
        "- 2026-08-30 | identity-rebuild | created/adopted 6 fresh canonical kind_robots rows "
        "after stale-ID collision; reused 6 existing remastered art assets; facets reapplied; "
        "no new ArtJobs"
    )
    text = re.sub(r"(^## Build log\s*\n)", rf"\1{log}\n", text, count=1, flags=re.MULTILINE)
    block = f"\n<!-- built-data\n{json.dumps(built, ensure_ascii=False, sort_keys=True)}\n-->\n"
    path.write_text(text.rstrip() + "\n" + block, encoding="utf-8")


def _preserve_history(historical_built: dict[str, Any], built: dict[str, Any]) -> None:
    for key in HISTORY_KEYS:
        value = historical_built.get(key)
        if value:
            built[key] = value


def rebuild_one(relative_path: str, source_ref: str, token: str) -> dict[str, Any]:
    path = (ROOT / relative_path).resolve()
    if path.parent != BACKLOG.resolve() or path.suffix != ".md":
        raise ValueError(f"repair path must be a direct dream-cycle backlog markdown file: {relative_path}")
    current_text = path.read_text(encoding="utf-8")
    fm, proposal = _validate_current_source(path, current_text)
    historical_text = _git_show(source_ref, relative_path)
    historical_built = _validate_history(proposal, historical_text)
    historical_art = art_by_role(historical_built)
    _verify_art_exists(historical_art)

    slug = str(fm.get("slug") or records.slugify(proposal["title"]))
    pdate = str(fm.get("proposal_date") or fm.get("created") or "")
    built, results, art_entries = records.build_records(proposal, slug, pdate, False)
    failures = [result for result in results if not result.get("ok")]
    if failures:
        deleted = records.rollback_created(results)
        raise RuntimeError(
            f"{relative_path}: canonical rebuild had {len(failures)} failed API calls; rolled back {deleted} rows"
        )
    if len(art_entries) != 6:
        deleted = records.rollback_created(results)
        raise RuntimeError(
            f"{relative_path}: canonical builder planned {len(art_entries)} art requests, expected 6; rolled back {deleted} rows"
        )

    built["identity_bundle_slug"] = slug
    built["identity_location_slug"] = records.slugify(proposal["locations"][0]["title"])
    try:
        _attach_existing_art(historical_built, built)
        built["art"] = migrated_art(historical_built, built)
        _apply_facets(proposal, built, token)
        _preserve_history(historical_built, built)
        old_records = role_records(historical_built)
        built["identity_rebuilds"] = [
            *(historical_built.get("identity_rebuilds") or []),
            {
                "rebuilt_at": _now(),
                "source_ref": source_ref,
                "reason": "repair stale live-record ownership after cross-bundle ID collision",
                "previous_claimed_ids": {role: int(row["id"]) for role, row in old_records.items()},
                "reused_existing_art": True,
                "new_art_jobs": 0,
            },
        ]
        verified = verify_fresh_bundle(proposal, built)
    except Exception:
        records.rollback_created(results)
        raise

    # Only after the live six-row bundle, existing art, facets, and labels all verify do
    # we make the source authoritative again.
    _write_built_source(path, built)
    return {
        "path": relative_path,
        "title": proposal["title"],
        "fresh_records": {row["role"]: row["id"] for row in verified},
        "art_paths": {role: art["public_path"] for role, art in historical_art.items()},
        "new_art_jobs": 0,
    }


def validate_request(request: dict[str, Any]) -> tuple[str, list[str], list[dict[str, Any]]]:
    if request.get("version") != 1:
        raise ValueError("request version must be 1")
    source_ref = str(request.get("source_ref") or "")
    if not re.fullmatch(r"[0-9a-fA-F]{40}", source_ref):
        raise ValueError("source_ref must be a full 40-character commit SHA")
    bundles = request.get("bundles")
    if not isinstance(bundles, list) or len(bundles) != 2 or not all(isinstance(v, str) for v in bundles):
        raise ValueError("request must contain exactly two backlog bundle paths")
    if len(set(bundles)) != len(bundles):
        raise ValueError("request contains duplicate bundle paths")
    protected = request.get("protected_owners")
    if not isinstance(protected, list) or len(protected) < 2 or not all(isinstance(v, dict) for v in protected):
        raise ValueError("request must include protected_owners")
    if not request.get("approved_by_user"):
        raise ValueError("request lacks explicit user approval evidence")
    return source_ref, list(bundles), list(protected)


def run(request_path: Path) -> dict[str, Any]:
    request = _read_json(request_path)
    source_ref, bundles, protected = validate_request(request)
    token = os.environ.get("KR_API_TOKEN", "").strip()
    if not token:
        raise RuntimeError("KR_API_TOKEN is required")

    before = verify_protected_owners(protected)
    results: list[dict[str, Any]] = []
    for relative_path in bundles:
        print(f"Rebuilding {relative_path} from clean source with art history at {source_ref[:12]}…")
        results.append(rebuild_one(relative_path, source_ref, token))

    after = verify_protected_owners(protected)
    if before != after:
        raise RuntimeError("protected owner rows changed during collision repair")

    collision_report = identity.summary()
    if collision_report.get("collision_count") != 0:
        raise RuntimeError(
            "record identity audit still reports collisions: "
            + json.dumps(collision_report, ensure_ascii=False)
        )

    receipt = {
        "version": 1,
        "status": "complete",
        "completed_at": _now(),
        "source_ref": source_ref,
        "approved_by_user": request.get("approved_by_user"),
        "protected_owners": after,
        "bundles": results,
        "collision_count_after": 0,
    }
    receipt_path = request_path.with_name(request_path.name.replace("-request.json", "-receipt.json"))
    receipt_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    request_path.unlink()
    print(json.dumps(receipt, indent=2, ensure_ascii=False))
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request", type=Path)
    args = parser.parse_args()
    request_path = args.request if args.request.is_absolute() else ROOT / args.request
    if request_path.parent.resolve() != REPAIR_DIR.resolve() or not request_path.name.endswith("-request.json"):
        raise SystemExit("request must be projects/dream-cycle/record-repairs/*-request.json")
    try:
        run(request_path)
    except Exception as error:  # noqa: BLE001 - one visible failure is better than a partial silent repair
        print(f"identity rebuild failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
