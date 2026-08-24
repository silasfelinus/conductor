#!/usr/bin/env python3
"""
check_project_scaffold_drift.py — Verify the Kind-Robots-to-Conductor project
handoff actually happened, instead of trusting a closed scaffold Todo.

Background (conductor/t-125, filed 2026-08-24 while scaffolding cthulhuquarium,
the first project Silas started from the Kind Robots side rather than from
`intake.py`): the sync between the two repos is one-way by design --
sync_kind_robots_projection.py pushes Conductor roadmaps into Kind Robots and
never reads back -- so the ONLY path a Kind-Robots-authored project has into
Conductor is the scaffold Todo that `createProjectWithScaffoldTodo` writes
(server/api/projects/index.post.ts), picked up by fetch_todos.py at the start
of a Worker cycle. Nothing previously verified that handoff actually
completed: Todo #1320, "Scaffold conductor project for cthuluquarium", was
marked DONE while `projects/cthulhuquarium/` did not exist in this repo and
never had. A closed todo was indistinguishable from a completed scaffold, so a
dropped project could go silently missing.

Two-directional check, read-only:

  FORWARD (the bug this task reports, the strong finding): every Kind Robots
  Project with a `conductorSlug` set claims a matching Conductor roadmap. If
  `projects/<conductorSlug>/roadmap.yaml` does not exist here, the scaffold
  never actually landed -- flag it.

  REVERSE (weaker, informational): every active Conductor project directory
  should eventually get a matching Kind Robots Project row -- the projection
  sync's own upsert (`server/api/conductor/sync.post.ts`) creates one for
  every roadmap slug it pushes, or 409s if the slug is already claimed by a
  different Project. A Conductor project with no matching KR row at all is
  worth surfacing (a stuck 409 collision would leave exactly this shape), but
  it is not the reported bug and is reported separately from the forward
  findings.

Excludes paused, retired, and finished projects by default according to
project-overrides.yaml, matching check_pr_merged_drift.py and
audit_human_gates.py. Use --include-inactive for an intentional archive sweep.

Requires: KR_API_TOKEN env var (a valid kind_robots JWT for Silas's account) to
reach GET https://kindrobots.org/api/projects. Without it, the check cannot
run at all -- this is reported as unresolved, not as a clean pass.

Usage:
  python scripts/check_project_scaffold_drift.py
  python scripts/check_project_scaffold_drift.py --json
  python scripts/check_project_scaffold_drift.py --include-inactive

Exit codes: 0 = clean, 1 = forward drift found (a claimed scaffold is
missing), 2 = unresolved (token missing or API unreachable), 3 = only reverse
orphans found (weaker signal, no confirmed missing scaffold).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROJECTS_DIR = ROOT / "projects"
OVERRIDES_PATH = ROOT / "project-overrides.yaml"
API_URL = "https://kindrobots.org/api/projects"
ACTIVE_STATUS = "active"


def load_yaml(path: Path) -> dict[str, Any]:
    import yaml

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def load_project_statuses(path: Path | None = None) -> dict[str, str]:
    path = path or OVERRIDES_PATH
    if not path.exists():
        return {}
    data = load_yaml(path)
    statuses: dict[str, str] = {}
    for entry in data.get("overrides", []) or []:
        if not isinstance(entry, dict):
            continue
        slug = str(entry.get("slug") or "").strip()
        if not slug:
            continue
        statuses[slug] = str(entry.get("status") or ACTIVE_STATUS).strip().lower()
    return statuses


def local_project_slugs(projects_dir: Path | None = None) -> set[str]:
    projects_dir = projects_dir or PROJECTS_DIR
    return {
        path.parent.name
        for path in projects_dir.glob("*/roadmap.yaml")
        if path.parent.name != "_template"
    }


def fetch_kind_robots_projects(token: str) -> list[dict[str, Any]]:
    """GET every Kind Robots Project (active and inactive) with pagination."""
    projects: list[dict[str, Any]] = []
    take = 250
    skip = 0
    while True:
        url = f"{API_URL}?includeInactive=true&take={take}&skip={skip}"
        req = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = json.loads(resp.read())
        page = body.get("data", []) or []
        projects.extend(page)
        if len(page) < take:
            break
        skip += take
    return projects


def scan(
    kr_projects: list[dict[str, Any]],
    projects_dir: Path | None = None,
    overrides_path: Path | None = None,
    include_inactive: bool = False,
) -> dict[str, list[dict[str, Any]]]:
    project_statuses = load_project_statuses(overrides_path)
    local_slugs = local_project_slugs(projects_dir)

    forward: list[dict[str, Any]] = []
    claimed_slugs: set[str] = set()
    for project in kr_projects:
        conductor_slug = (project.get("conductorSlug") or "").strip()
        if not conductor_slug:
            continue
        claimed_slugs.add(conductor_slug)
        lifecycle = project_statuses.get(conductor_slug, ACTIVE_STATUS)
        if not include_inactive and lifecycle != ACTIVE_STATUS and conductor_slug in project_statuses:
            continue
        if conductor_slug not in local_slugs:
            forward.append(
                {
                    "conductor_slug": conductor_slug,
                    "kr_project_id": project.get("id"),
                    "kr_title": project.get("title"),
                    "kr_slug": project.get("slug"),
                }
            )

    reverse: list[dict[str, Any]] = []
    for slug in sorted(local_slugs):
        lifecycle = project_statuses.get(slug, ACTIVE_STATUS)
        if not include_inactive and lifecycle != ACTIVE_STATUS:
            continue
        if slug not in claimed_slugs:
            reverse.append({"conductor_slug": slug, "project_status": lifecycle})

    return {"forward": forward, "reverse": reverse}


def render(result: dict[str, list[dict[str, Any]]]) -> str:
    forward = result["forward"]
    reverse = result["reverse"]
    if not forward and not reverse:
        return "No project-scaffold drift found — every conductorSlug has a matching roadmap, every Conductor project has a matching Kind Robots row."

    lines: list[str] = []
    if forward:
        lines.append(
            f"FORWARD drift ({len(forward)}): Kind Robots Project claims a Conductor "
            "scaffold that does not exist here."
        )
        for f in forward:
            lines.append(
                f"  - conductorSlug={f['conductor_slug']!r} (KR Project #{f['kr_project_id']} "
                f"{f['kr_title']!r}, slug={f['kr_slug']!r}) -- "
                f"projects/{f['conductor_slug']}/roadmap.yaml is MISSING"
            )
        lines.append(
            "    A closed scaffold Todo does not mean the scaffold landed. Run "
            "intake.py for these slugs (or otherwise create the roadmap) before "
            "trusting this project's Conductor state."
        )
    if reverse:
        if lines:
            lines.append("")
        lines.append(
            f"REVERSE orphans ({len(reverse)}, informational): Conductor project has no "
            "matching Kind Robots Project row (conductorSlug never set)."
        )
        for r in reverse:
            lines.append(f"  - projects/{r['conductor_slug']}/ [{r['project_status']}]")
        lines.append(
            "    Could be a pending first sync, or a stuck 409 slug collision in "
            "sync_kind_robots_projection.py. Not the reported bug on its own -- verify "
            "before treating as drift."
        )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument(
        "--include-inactive",
        action="store_true",
        help="also check paused, retired, and finished projects",
    )
    args = parser.parse_args()

    token = os.environ.get("KR_API_TOKEN", "").strip()
    if not token:
        print("⚠  KR_API_TOKEN not set — cannot reach the Kind Robots API. This is not a clean audit.", file=sys.stderr)
        if args.json:
            print(json.dumps({"forward": [], "reverse": [], "unresolved": "KR_API_TOKEN not set"}, indent=2))
        sys.exit(2)

    try:
        kr_projects = fetch_kind_robots_projects(token)
    except urllib.error.HTTPError as e:
        print(f"⚠  kind_robots API returned {e.code} — cannot verify scaffold drift.", file=sys.stderr)
        if args.json:
            print(json.dumps({"forward": [], "reverse": [], "unresolved": f"HTTP {e.code}"}, indent=2))
        sys.exit(2)
    except Exception as e:  # noqa: BLE001 — any network failure is unresolved, not clean
        print(f"⚠  Could not reach kind_robots API: {e}", file=sys.stderr)
        if args.json:
            print(json.dumps({"forward": [], "reverse": [], "unresolved": str(e)}, indent=2))
        sys.exit(2)

    result = scan(kr_projects, include_inactive=args.include_inactive)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(render(result))

    if result["forward"]:
        sys.exit(1)
    if result["reverse"]:
        sys.exit(3)
    sys.exit(0)


if __name__ == "__main__":
    main()
