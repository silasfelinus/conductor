#!/usr/bin/env python3
"""Retry-safe front end for the bounded Daily Dream identity collision repair.

The first production attempt proved two useful facts:
- Fault Line Follies completed its fresh six-row live rebuild before the later
  bundle failed, so a retry must adopt that exact uncommitted live bundle.
- The Deep Shift has one older, unclaimed PITCH row with the same technical
  identity but stale prose, so the canonical builder correctly refused to
  adopt it under its normal exact-content conflict rule.

This wrapper keeps the normal builder strict everywhere else. For this one
approved recovery request only, it extends PITCH conflict recovery to adopt a
single *unprotected* row matching title + slug + dreamType + designer, refreshes
its user-facing prose to the request's current proposal during adoption, then
hands control back to rebuild_dream_identity_collision.py. Exact rows created by
an earlier failed attempt continue to use the normal exact adoption path.
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

ROOT = Path(__file__).resolve().parents[1]
REPAIR_DIR = ROOT / "projects" / "dream-cycle" / "record-repairs"


def _rows(response: Any) -> list[dict[str, Any]]:
    if not isinstance(response, dict):
        return []
    value = response.get("data")
    if isinstance(value, dict):
        value = value.get("rows") or value.get("items") or value.get("dream") or value.get("dreams")
    if isinstance(value, dict):
        value = [value]
    return [row for row in value if isinstance(row, dict)] if isinstance(value, list) else []


def _protected_ids(request: dict[str, Any]) -> set[tuple[str, int]]:
    protected: set[tuple[str, int]] = set()
    for row in request.get("protected_owners") or []:
        if not isinstance(row, dict):
            continue
        endpoint = str(row.get("endpoint") or "")
        try:
            record_id = int(row.get("id") or 0)
        except (TypeError, ValueError):
            continue
        if endpoint and record_id > 0:
            protected.add((endpoint, record_id))
    return protected


def make_recovery_matcher(
    original_matcher,
    protected: set[tuple[str, int]],
):
    """Return the narrow conflict matcher used only by this retry wrapper."""

    def recovery_matcher(endpoint: str, identity: dict[str, Any]):
        exact = original_matcher(endpoint, identity)
        if exact is not None:
            return exact

        # Never relax identity for locations, characters, rewards, scenarios, or
        # ordinary builds. The production failure was one stale, unclaimed PITCH.
        if endpoint != "/api/dreams" or str(identity.get("dreamType") or "").upper() != "PITCH":
            return None

        title = str(identity.get("title") or "").strip()
        slug = str(identity.get("slug") or "").strip()
        designer = str(identity.get("designer") or "").strip()
        if not title or not slug or not designer:
            return None

        query = urllib.parse.urlencode(
            {
                "search": title,
                "mine": "true",
                "includeInactive": "true",
                "includeMature": "true",
                "take": "200",
            }
        )
        status, response = records.http_json(
            "GET", f"{records.KR_BASE_URL}/api/dreams?{query}"
        )
        if status != 200:
            return None

        candidates = [
            row
            for row in _rows(response)
            if str(row.get("title") or "") == title
            and str(row.get("slug") or "") == slug
            and str(row.get("dreamType") or "").upper() == "PITCH"
            and str(row.get("designer") or "") == designer
            and isinstance(row.get("id"), int)
            and (endpoint, int(row["id"])) not in protected
        ]
        if len(candidates) != 1:
            return None

        row = candidates[0]
        record_id = int(row["id"])
        # Bring the stale orphan forward to the *current* authored proposal before
        # returning it as adoptable. Do not touch identity fields or imagePath here;
        # the canonical recovery lane attaches the approved existing render later.
        payload = {
            key: identity[key]
            for key in ("title", "description", "flavorText", "artPrompt")
            if key in identity
        }
        patch_status, patch_response = records.http_json(
            "PATCH", f"{records.KR_BASE_URL}/api/dreams/{record_id}", payload
        )
        if patch_status not in (200, 201):
            raise RuntimeError(
                f"could not refresh recoverable PITCH /api/dreams/{record_id} "
                f"({patch_status}): {str(patch_response)[:300]}"
            )
        updated = dict(row)
        updated.update(payload)
        print(
            f"  recovery-adopted stale unclaimed PITCH: {title} "
            f"(ID {record_id}); refreshed current prose"
        )
        return updated

    return recovery_matcher


def run(request_path: Path) -> dict[str, Any]:
    request = json.loads(request_path.read_text(encoding="utf-8"))
    if not isinstance(request, dict):
        raise ValueError("identity rebuild request must be a JSON object")
    # Reuse the base lane's full approval/scope validation before altering the
    # matcher. This keeps the relaxation impossible to invoke with a broad request.
    repair.validate_request(request)

    original_matcher = records._matching_existing
    records._matching_existing = make_recovery_matcher(
        original_matcher, _protected_ids(request)
    )
    try:
        return repair.run(request_path)
    finally:
        records._matching_existing = original_matcher


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
        print(f"identity rebuild retry failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
