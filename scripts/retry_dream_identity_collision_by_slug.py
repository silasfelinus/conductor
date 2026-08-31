#!/usr/bin/env python3
"""Retry the bounded Daily Dream identity repair using Dream.slug as the final key.

Kind Robots enforces Dream.slug as globally unique, but the Dream browse endpoint's
`search` parameter does not search slugs. Earlier recovery attempts therefore saw a
409 for `kelp-ink-transfer` yet could not rediscover the older row when its title no
longer matched `The Deep Shift`.

This wrapper preserves every guard in retry_dream_identity_collision.py. It only adds
one last PITCH-only fallback: page through the visible PITCH index, find exactly one
unprotected row whose slug and designer match the canonical identity, refresh only
its current user-facing prose, and hand that row back to the strict builder.
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


def _slug_candidates(slug: str, designer: str, protected: set[tuple[str, int]]) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    skip = 0
    page_size = 200
    while True:
        query = urllib.parse.urlencode(
            {
                "dreamType": "PITCH",
                "includeInactive": "true",
                "includeMature": "true",
                "take": str(page_size),
                "skip": str(skip),
            }
        )
        status, response = records.http_json("GET", f"{records.KR_BASE_URL}/api/dreams?{query}")
        if status != 200:
            raise RuntimeError(f"could not scan Dream PITCH index for slug {slug!r} ({status})")
        page = _rows(response)
        found.extend(
            row
            for row in page
            if str(row.get("slug") or "") == slug
            and str(row.get("dreamType") or "").upper() == "PITCH"
            and str(row.get("designer") or "") == designer
            and isinstance(row.get("id"), int)
            and ("/api/dreams", int(row["id"])) not in protected
        )
        if len(page) < page_size:
            break
        skip += page_size
        if skip >= 2000:
            raise RuntimeError("Dream PITCH slug scan exceeded 2000 rows")
    return found


def make_slug_recovery_matcher(base_matcher, protected: set[tuple[str, int]]):
    def matcher(endpoint: str, identity: dict[str, Any]):
        existing = base_matcher(endpoint, identity)
        if existing is not None:
            return existing

        if endpoint != "/api/dreams" or str(identity.get("dreamType") or "").upper() != "PITCH":
            return None
        slug = str(identity.get("slug") or "").strip()
        designer = str(identity.get("designer") or "").strip()
        title = str(identity.get("title") or "").strip()
        if not slug or not designer or not title:
            return None

        candidates = _slug_candidates(slug, designer, protected)
        if len(candidates) != 1:
            if len(candidates) > 1:
                raise RuntimeError(f"ambiguous unprotected PITCH slug recovery for {slug!r}: {len(candidates)} rows")
            return None

        row = candidates[0]
        record_id = int(row["id"])
        payload = {
            key: identity[key]
            for key in ("title", "description", "flavorText", "artPrompt")
            if key in identity
        }
        status, response = records.http_json(
            "PATCH", f"{records.KR_BASE_URL}/api/dreams/{record_id}", payload
        )
        if status not in (200, 201):
            raise RuntimeError(
                f"could not refresh recoverable slug-owned PITCH /api/dreams/{record_id} "
                f"({status}): {str(response)[:300]}"
            )
        updated = dict(row)
        updated.update(payload)
        print(
            f"  recovery-adopted unique slug owner: {slug} -> /api/dreams/{record_id}; "
            "refreshed current prose"
        )
        return updated

    return matcher


def run(request_path: Path) -> dict[str, Any]:
    request = json.loads(request_path.read_text(encoding="utf-8"))
    if not isinstance(request, dict):
        raise ValueError("identity rebuild request must be a JSON object")
    repair.validate_request(request)
    protected = retry._protected_ids(request)

    original_factory = retry.make_recovery_matcher

    def patched_factory(original_matcher, protected_ids, retry_adoptions=None):
        base = original_factory(original_matcher, protected_ids, retry_adoptions)
        return make_slug_recovery_matcher(base, protected_ids)

    retry.make_recovery_matcher = patched_factory
    try:
        return retry.run(request_path)
    finally:
        retry.make_recovery_matcher = original_factory


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
