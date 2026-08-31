#!/usr/bin/env python3
"""Retry-safe front end for the bounded Daily Dream identity collision repair.

Production attempts established two recovery facts that are stronger than a
collection search:
- Daily Dream Identity Rebuild run 33343607764 created a complete fresh live
  Fault Line Follies bundle. The workflow failed later, before committing its
  source ledger, so those six rows must be adopted by their recorded IDs.
- The Deep Shift has one older, unclaimed PITCH row with the same technical
  identity but stale prose, so the canonical builder correctly refuses normal
  exact-content adoption until that row is refreshed.

This wrapper keeps normal builder behavior strict. For this one approved repair:
1. ordinary exact adoption is always attempted first;
2. rows explicitly recorded in the request as prior-attempt creations may be
   adopted by endpoint + ID + exact label after a direct live GET;
3. only a PITCH conflict may otherwise relax to one unprotected row matching
   title + slug + dreamType + designer, and that row's current prose is refreshed
   before adoption.

No matching rule is relaxed globally and protected owner rows are never eligible.
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


def _retry_adoptions(request: dict[str, Any]) -> list[dict[str, Any]]:
    source_run = int(request.get("retry_after_run") or 0)
    rows = request.get("retry_adoptions") or []
    if not rows:
        return []
    if source_run <= 0:
        raise ValueError("retry_adoptions require retry_after_run evidence")
    if not isinstance(rows, list) or not all(isinstance(row, dict) for row in rows):
        raise ValueError("retry_adoptions must be a list of objects")
    normalized: list[dict[str, Any]] = []
    seen: set[tuple[str, int]] = set()
    for row in rows:
        endpoint = str(row.get("endpoint") or "")
        record_id = int(row.get("id") or 0)
        label = str(row.get("title") or row.get("name") or "").strip()
        if endpoint not in {"/api/dreams", "/api/characters", "/api/rewards", "/api/scenarios"}:
            raise ValueError(f"invalid retry adoption endpoint: {endpoint!r}")
        if record_id <= 0 or not label:
            raise ValueError("retry adoption requires positive id and title/name")
        key = (endpoint, record_id)
        if key in seen:
            raise ValueError(f"duplicate retry adoption: {endpoint}/{record_id}")
        seen.add(key)
        normalized.append({"endpoint": endpoint, "id": record_id, "label": label, "source_run": source_run})
    return normalized


def _unwrap(response: Any) -> dict[str, Any] | None:
    if not isinstance(response, dict):
        return None
    data = response.get("data")
    if isinstance(data, dict):
        for key in ("dream", "character", "reward", "scenario"):
            nested = data.get(key)
            if isinstance(nested, dict):
                return nested
        if "id" in data:
            return data
    return response if "id" in response else None


def _label(row: dict[str, Any]) -> str:
    return str(row.get("title") or row.get("name") or "").strip()


def make_recovery_matcher(
    original_matcher,
    protected: set[tuple[str, int]],
    retry_adoptions: list[dict[str, Any]] | None = None,
):
    """Return the narrow conflict matcher used only by this retry wrapper."""
    retry_adoptions = retry_adoptions or []

    def recovery_matcher(endpoint: str, identity: dict[str, Any]):
        exact = original_matcher(endpoint, identity)
        if exact is not None:
            return exact

        wanted_label = str(identity.get("title") or identity.get("name") or "").strip()
        recorded = [
            row for row in retry_adoptions
            if row["endpoint"] == endpoint and row["label"] == wanted_label
        ]
        if len(recorded) > 1:
            raise RuntimeError(f"ambiguous recorded retry adoption for {endpoint} {wanted_label!r}")
        if recorded:
            evidence = recorded[0]
            key = (endpoint, int(evidence["id"]))
            if key in protected:
                raise RuntimeError(f"recorded retry adoption overlaps protected owner: {endpoint}/{evidence['id']}")
            status, response = records.http_json(
                "GET", f"{records.KR_BASE_URL}{endpoint}/{evidence['id']}"
            )
            row = _unwrap(response)
            if status != 200 or row is None:
                raise RuntimeError(
                    f"recorded retry row missing: {endpoint}/{evidence['id']} ({status})"
                )
            if _label(row) != wanted_label:
                raise RuntimeError(
                    f"recorded retry row drift: {endpoint}/{evidence['id']} expected "
                    f"{wanted_label!r}, got {_label(row)!r}"
                )
            print(
                f"  recovery-adopted prior-attempt row: {wanted_label} "
                f"({endpoint}/{evidence['id']}, run {evidence['source_run']})"
            )
            return row

        # Outside explicit prior-attempt evidence, never relax identity for locations,
        # characters, rewards, scenarios, or ordinary builds. The remaining known
        # recovery case is one stale, unclaimed PITCH for The Deep Shift.
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
    repair.validate_request(request)
    protected = _protected_ids(request)
    adoptions = _retry_adoptions(request)
    if any((row["endpoint"], row["id"]) in protected for row in adoptions):
        raise ValueError("retry_adoptions overlap protected owners")

    original_matcher = records._matching_existing
    records._matching_existing = make_recovery_matcher(
        original_matcher, protected, adoptions
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
