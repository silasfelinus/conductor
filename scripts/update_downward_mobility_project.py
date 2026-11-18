#!/usr/bin/env python3
"""One-shot owner-approved presentation rename via Kind Robots' Project API.

The Project row and public visibility are Kind Robots data, not Conductor
projection fields. This does not alter the stable conductorSlug, URLs, user
progress, artwork, payment or deployment controls.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

BASE = "https://kindrobots.org"
SLUG = "shifting-desks"
TITLE = "Downward Mobility"


def pick_project(rows: list[dict]) -> dict:
    matches = [row for row in rows if row.get("conductorSlug") == SLUG]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one Project with conductorSlug={SLUG}; found {len(matches)}")
    project = matches[0]
    if not isinstance(project.get("id"), int) or project["id"] <= 0:
        raise ValueError("project ID is missing or invalid")
    if project.get("isMature") is True:
        raise ValueError("unexpected mature project: public visibility is not approved")
    if project.get("title") not in ("Shifting Desks", "The Elevator Only Goes Down", TITLE):
        raise ValueError("unexpected existing Project title; refusing to overwrite another owner decision")
    return project


def patch_fields(project: dict) -> dict:
    changes: dict[str, str | bool] = {}
    if project.get("title") != TITLE:
        changes["title"] = TITLE
    if project.get("isPublic") is not True:
        changes["isPublic"] = True
    if project.get("isActive") is not True:
        changes["isActive"] = True
    return changes


def api_request(path: str, token: str, *, patch: dict | None = None) -> dict:
    request = urllib.request.Request(
        BASE + path,
        data=json.dumps(patch).encode("utf-8") if patch is not None else None,
        method="PATCH" if patch is not None else "GET",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            **({"Content-Type": "application/json"} if patch is not None else {}),
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            data = json.load(response)
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"Project API returned HTTP {error.code}") from None
    if not isinstance(data, dict) or data.get("success") is not True:
        raise RuntimeError("Project API returned an unsuccessful response")
    return data


def main() -> int:
    token = os.environ.get("KR_API_TOKEN", "").strip()
    if not token:
        print("KR_API_TOKEN unavailable; Project display title not changed", file=sys.stderr)
        return 1
    payload = api_request("/api/projects?search=shifting-desks&includeInactive=true&take=250", token)
    project = pick_project(payload.get("data", []))
    changes = patch_fields(project)
    if not changes:
        print("Downward Mobility Project already has the approved title and public visibility")
        return 0
    result = api_request(f"/api/projects/{project['id']}", token, patch=changes)
    updated = result.get("data")
    if not isinstance(updated, dict) or updated.get("id") != project["id"]:
        raise RuntimeError("Project API did not confirm the updated Project ID")
    if updated.get("title") != TITLE or updated.get("isPublic") is not True:
        raise RuntimeError("Project API did not confirm title and public visibility")
    print("Downward Mobility Project display title and public visibility confirmed")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1) from None
