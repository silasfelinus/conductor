#!/usr/bin/env python3
"""Archive explicitly tombstoned Kind Robots Project rows.

This is deliberately not "archive anything missing from Conductor". A Kind Robots
project can legitimately exist before its Conductor scaffold lands, so absence is not
deletion intent. Only rows named in project-tombstones.yaml are eligible, and both the
numeric Project id and conductorSlug/slug must match before any write occurs.

DELETE /api/projects/:id is Kind Robots' reversible project deletion: it sets
isActive=false and status=ARCHIVED while preserving the row for audit/history.
"""

from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_API_BASE = "https://kindrobots.org"
DEFAULT_TOMBSTONES = ROOT / "project-tombstones.yaml"


def load_tombstones(path: Path = DEFAULT_TOMBSTONES) -> list[dict[str, Any]]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if data.get("version") != 1:
        raise RuntimeError("project tombstones must use version: 1")
    projects = data.get("projects")
    if not isinstance(projects, list):
        raise RuntimeError("project tombstones must contain a projects list")

    seen_ids: set[int] = set()
    seen_slugs: set[str] = set()
    normalized: list[dict[str, Any]] = []
    for entry in projects:
        if not isinstance(entry, dict):
            raise RuntimeError("each project tombstone must be a mapping")
        project_id = entry.get("id")
        slug = str(entry.get("slug") or "").strip()
        if not isinstance(project_id, int) or project_id <= 0 or not slug:
            raise RuntimeError("each project tombstone requires a positive integer id and slug")
        if project_id in seen_ids or slug in seen_slugs:
            raise RuntimeError(f"duplicate project tombstone: id={project_id}, slug={slug}")
        seen_ids.add(project_id)
        seen_slugs.add(slug)
        normalized.append({"id": project_id, "slug": slug, "reason": entry.get("reason")})
    return normalized


def request_json(
    url: str,
    token: str,
    *,
    method: str = "GET",
) -> dict[str, Any]:
    req = urllib.request.Request(
        url,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "conductor-project-tombstone-reconciler/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Kind Robots API failed: HTTP {error.code}: {body}") from error


def fetch_projects(api_base: str, token: str) -> list[dict[str, Any]]:
    projects: list[dict[str, Any]] = []
    take = 250
    skip = 0
    while True:
        body = request_json(
            f"{api_base.rstrip('/')}/api/projects?includeInactive=true&take={take}&skip={skip}",
            token,
        )
        page = body.get("data", []) or []
        if not isinstance(page, list):
            raise RuntimeError("Kind Robots projects response did not contain a data list")
        projects.extend(page)
        if len(page) < take:
            return projects
        skip += take


def plan_actions(
    tombstones: list[dict[str, Any]],
    projects: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    by_id = {project.get("id"): project for project in projects}
    actions: list[dict[str, Any]] = []
    for tombstone in tombstones:
        project = by_id.get(tombstone["id"])
        if project is None:
            raise RuntimeError(
                f"tombstoned Project #{tombstone['id']} ({tombstone['slug']}) was not found"
            )

        expected = tombstone["slug"]
        actual_slug = str(project.get("slug") or "").strip()
        conductor_slug = str(project.get("conductorSlug") or "").strip()
        if actual_slug != expected or conductor_slug != expected:
            raise RuntimeError(
                f"refusing to archive Project #{tombstone['id']}: expected slug and "
                f"conductorSlug {expected!r}, got slug={actual_slug!r}, "
                f"conductorSlug={conductor_slug!r}"
            )

        archived = project.get("isActive") is False or project.get("status") == "ARCHIVED"
        actions.append(
            {
                "id": tombstone["id"],
                "slug": expected,
                "archive": not archived,
            }
        )
    return actions


def reconcile(
    api_base: str,
    token: str,
    tombstones: list[dict[str, Any]],
    *,
    check: bool = False,
) -> list[dict[str, Any]]:
    projects = fetch_projects(api_base, token)
    actions = plan_actions(tombstones, projects)

    if not check:
        for action in actions:
            if not action["archive"]:
                continue
            result = request_json(
                f"{api_base.rstrip('/')}/api/projects/{action['id']}",
                token,
                method="DELETE",
            )
            if not result.get("success"):
                raise RuntimeError(
                    f"Kind Robots refused to archive Project #{action['id']}: {result}"
                )

        refreshed = fetch_projects(api_base, token)
        verified = plan_actions(tombstones, refreshed)
        not_archived = [action for action in verified if action["archive"]]
        if not_archived:
            raise RuntimeError(f"project tombstone verification failed: {not_archived}")
    return actions


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="validate exact targets without writing")
    parser.add_argument("--tombstones", type=Path, default=DEFAULT_TOMBSTONES)
    parser.add_argument(
        "--api-base",
        default=os.environ.get("KR_API_BASE", DEFAULT_API_BASE),
    )
    args = parser.parse_args()

    token = os.environ.get("KR_API_TOKEN", "").strip()
    if not token:
        raise RuntimeError("KR_API_TOKEN is required for project tombstone reconciliation")

    tombstones = load_tombstones(args.tombstones)
    actions = reconcile(args.api_base, token, tombstones, check=args.check)
    print(
        json.dumps(
            {
                "mode": "check" if args.check else "archive",
                "projects": actions,
                "archiveCount": sum(1 for action in actions if action["archive"]),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
