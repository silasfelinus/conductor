#!/usr/bin/env python3
"""Retry the bounded Daily Dream identity repair using global Dream.slug identity.

Kind Robots enforces Dream.slug globally across every Dream type. The browse endpoint's
`search` parameter does not search slugs, and earlier recovery attempts proved the stale
`kelp-ink-transfer` owner is not visible inside the PITCH-only slice. This wrapper keeps
all prior safeguards but scans the full visible Dream index for exactly one unprotected
slug owner, converts that row to the current canonical PITCH identity in place, then
lets the strict rebuild lane finish the bundle. No row is deleted to free the slug.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_dream_records as records  # noqa: E402
import rebuild_dream_identity_collision as repair  # noqa: E402
import retry_dream_identity_collision as retry  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
REPAIR_DIR = ROOT / "projects" / "dream-cycle" / "record-repairs"


def _rows(response: Any) -> list[dict[str, Any]]:
    if not isinstance(response, dict):
        return []
    data = response.get("data")
    if isinstance(data, dict):
        data = data.get("rows") or data.get("items") or data.get("dreams") or data.get("dream")
    if isinstance(data, dict):
        data = [data]
    return [row for row in data if isinstance(row, dict)] if isinstance(data, list) else []


def _slug_candidates(slug: str, protected: set[tuple[str, int]]) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    skip = 0
    page_size = 200
    while True:
        query = urllib.parse.urlencode(
            {
                "includeInactive": "true",
                "includeMature": "true",
                "take": str(page_size),
                "skip": str(skip),
            }
        )
        status, response = records.http_json("GET", f"{records.KR_BASE_URL}/api/dreams?{query}")
        if status != 200:
            raise RuntimeError(f"could not scan Dream index for slug {slug!r} ({status})")
        page = _rows(response)
        found.extend(
            row
            for row in page
            if str(row.get("slug") or "") == slug
            and isinstance(row.get("id"), int)
            and ("/api/dreams", int(row["id"])) not in protected
        )
        if len(page) < page_size:
            break
        skip += page_size
        if skip >= 2000:
            raise RuntimeError("Dream slug scan exceeded 2000 rows")
    return found


def make_slug_recovery_matcher(base_matcher, protected: set[tuple[str, int]]):
    def matcher(endpoint: str, identity: dict[str, Any]):
        existing = base_matcher(endpoint, identity)
        if existing is not None:
            return existing

        # The create conflict being recovered is a canonical PITCH. The stale row
        # that owns its globally unique slug may itself be any historical Dream type.
        if endpoint != "/api/dreams" or str(identity.get("dreamType") or "").upper() != "PITCH":
            return None
        slug = str(identity.get("slug") or "").strip()
        title = str(identity.get("title") or "").strip()
        if not slug or not title:
            return None

        candidates = _slug_candidates(slug, protected)
        if len(candidates) != 1:
            if len(candidates) > 1:
                raise RuntimeError(f"ambiguous unprotected Dream slug recovery for {slug!r}: {len(candidates)} rows")
            return None

        row = candidates[0]
        record_id = int(row["id"])
        payload = {
            "title": title,
            "dreamType": "PITCH",
            "designer": str(identity.get("designer") or records.DESIGNER),
            "description": str(identity.get("description") or ""),
        }
        status, response = records.http_json(
            "PATCH", f"{records.KR_BASE_URL}/api/dreams/{record_id}", payload
        )
        if status not in (200, 201):
            raise RuntimeError(
                f"could not convert slug owner /api/dreams/{record_id} to canonical PITCH "
                f"({status}): {str(response)[:300]}"
            )
        updated = dict(row)
        updated.update(payload)
        print(
            f"  recovery-adopted global slug owner: {slug} -> /api/dreams/{record_id}; "
            f"converted {row.get('dreamType') or 'UNKNOWN'} to PITCH"
        )
        return updated

    return matcher


def _refresh_world_and_sheet(relative_path: str) -> dict[str, Any]:
    """Refresh full authored world + PitchSheet after an adopted historical Dream."""
    path = ROOT / relative_path
    text = path.read_text(encoding="utf-8")
    fm = records._frontmatter(text)
    proposal = records._data_block(text, "proposal-data")
    built = records._data_block(text, "built-data")
    if not isinstance(proposal, dict) or not isinstance(built, dict):
        raise RuntimeError(f"{relative_path}: rebuilt source lacks proposal/built data")
    slug = str(fm.get("slug") or records.slugify(proposal["title"]))
    pdate = str(fm.get("proposal_date") or fm.get("created") or "")
    world = repair.role_records(built)["world"]
    world_id = int(world["id"])
    vibe = proposal.get("vibe") or {}
    title = str(proposal["title"])
    idea = str(proposal.get("idea") or "")
    vibe_line = str(vibe.get("line") or "")
    art_prompt = records.world_prompt(title, idea, vibe_line, str(vibe.get("art_direction") or ""))
    world_payload = {
        "title": title,
        "slug": records.slugify(slug),
        "dreamType": "PITCH",
        "designer": records.DESIGNER,
        "creationSource": records.CREATION_SOURCE,
        "isPublic": True,
        "description": idea,
        "flavorText": vibe_line[:500] if vibe_line else None,
        "artPrompt": art_prompt,
        "icon": "kind-icon:moon",
    }
    status, response = records.http_json(
        "PATCH", f"{records.KR_BASE_URL}/api/dreams/{world_id}", world_payload
    )
    if status not in (200, 201):
        raise RuntimeError(f"failed full world refresh for {world_id} ({status}): {str(response)[:300]}")

    sheets = built.get("sheets") if isinstance(built.get("sheets"), dict) else {}
    sheet_id = int(sheets.get(slug) or built.get("sheets", {}).get(records.slugify(slug)) or 0)
    if sheet_id <= 0:
        raise RuntimeError(f"{relative_path}: could not resolve world PitchSheet for {slug}")
    sheet_payload = {
        "designer": records.DESIGNER,
        "isPublic": True,
        "title": title,
        "hook": str(vibe.get("title") or ""),
        "pitch": idea,
        "highlight1Label": "Promise",
        "highlight1Value": vibe_line,
        "highlight2Label": "Builds Into",
        "highlight2Value": "one location, one character, two rewards, one scenario",
        "highlight3Label": "Status",
        "highlight3Value": f"proposed {pdate}, built by dream-cycle",
        "extraData": json.dumps(
            {"dreamCycle": slug, "proposalDate": pdate, "elementType": "PITCH", "element": slug}
        ),
    }
    status, response = records.http_json(
        "PATCH", f"{records.KR_BASE_URL}/api/sheets/{sheet_id}", sheet_payload
    )
    if status not in (200, 201):
        raise RuntimeError(f"failed world PitchSheet refresh for {sheet_id} ({status}): {str(response)[:300]}")
    return {"path": relative_path, "world_id": world_id, "sheet_id": sheet_id}


def run(request_path: Path) -> dict[str, Any]:
    request = json.loads(request_path.read_text(encoding="utf-8"))
    if not isinstance(request, dict):
        raise ValueError("identity rebuild request must be a JSON object")
    _, bundles, _ = repair.validate_request(request)
    protected = retry._protected_ids(request)

    original_factory = retry.make_recovery_matcher

    def patched_factory(original_matcher, protected_ids, retry_adoptions=None):
        base = original_factory(original_matcher, protected_ids, retry_adoptions)
        return make_slug_recovery_matcher(base, protected_ids)

    retry.make_recovery_matcher = patched_factory
    try:
        receipt = retry.run(request_path)
    finally:
        retry.make_recovery_matcher = original_factory

    refreshed = [_refresh_world_and_sheet(path) for path in bundles]
    receipt["canonical_world_refresh"] = refreshed
    receipt_path = request_path.with_name(request_path.name.replace("-request.json", "-receipt.json"))
    receipt_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
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
    except Exception as error:  # noqa: BLE001
        print(f"identity rebuild slug retry failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
