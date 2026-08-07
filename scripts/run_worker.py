#!/usr/bin/env python3
"""
run_worker.py — deterministic Conductor worker healthcheck.

This script intentionally does not call OpenAI, Claude, or any other model API.
Real task execution is session-driven from ChatGPT/OpenAI or Claude using their
GitHub connectors/tools. GitHub Actions only verifies the queue plumbing that
those sessions rely on.

What this checks:
- kind_robots Todo visibility via KR_API_TOKEN, when configured
- dependency-resolution dry run
- highest-priority ready roadmap task
- daily digest JSON generation and validation

Usage:
  python scripts/run_worker.py [--dry-run] [--since "24 hours ago"] [--sync-projects]

Env:
  KR_API_TOKEN  optional; enables kind_robots todo checks and Project sync
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    sys.exit('PyYAML not installed — run: pip install pyyaml')

sys.path.insert(0, str(Path(__file__).resolve().parent))
from roadmap_claims import remaining_scope_delegate_open  # noqa: E402
from project_lifecycle import (  # noqa: E402
    WORKABLE_PROJECT_STATUSES,
    lifecycle_status,
    load_project_overrides,
    ordered_workable_slugs,
)

PRIORITY_FILE = Path('projects/priority.yaml')
OVERRIDES_FILE = Path('project-overrides.yaml')
PROJECTS_DIR = Path('projects')


def run(command: list[str], *, capture: bool = False, check: bool = True) -> subprocess.CompletedProcess[str]:
    printable = ' '.join(command)
    print(f'[worker-check] $ {printable}', file=sys.stderr)
    return subprocess.run(command, text=True, capture_output=capture, check=check)


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open() as handle:
        return yaml.safe_load(handle) or {}


def load_priority() -> list[str]:
    data = load_yaml(PRIORITY_FILE)
    order = data.get('order', [])
    return [str(item) for item in order if item]


def load_overrides() -> dict[str, dict[str, Any]]:
    return load_project_overrides(OVERRIDES_FILE)


def load_roadmaps() -> list[dict[str, Any]]:
    overrides = load_overrides()
    roadmaps: list[dict[str, Any]] = []

    for path in sorted(PROJECTS_DIR.glob('*/roadmap.yaml')):
        if path.parent.name == '_template':
            continue

        roadmap = load_yaml(path)
        slug = roadmap.get('project') or path.parent.name
        override = overrides.get(str(slug), {})

        lifecycle = lifecycle_status(overrides, str(slug))
        if lifecycle not in WORKABLE_PROJECT_STATUSES:
            continue

        roadmap['_lifecycle'] = lifecycle
        roadmap['_path'] = str(path)
        roadmap['_project'] = str(slug)
        roadmaps.append(roadmap)

    return roadmaps


def find_ready_task(priority_order: list[str], roadmaps: list[dict[str, Any]]) -> dict[str, Any] | None:
    by_project = {roadmap.get('_project'): roadmap for roadmap in roadmaps}
    overrides = {str(slug): {'status': roadmap.get('_lifecycle', 'active')} for slug, roadmap in by_project.items()}
    for slug in ordered_workable_slugs(priority_order, overrides):
        roadmap = by_project[slug]
        tasks = roadmap.get('tasks', [])
        tasks_by_id = {
            str(task.get('id')): task for task in tasks if isinstance(task, dict) and task.get('id')
        }
        for task in tasks:
            if task.get('status') != 'ready':
                continue
            if remaining_scope_delegate_open(task, tasks_by_id):
                continue
            return {
                'project': roadmap.get('_project'),
                'task_id': task.get('id'),
                'title': task.get('title'),
                'roadmap_path': roadmap.get('_path'),
            }

    return None


def build_queue_summary() -> dict[str, Any]:
    roadmaps = load_roadmaps()
    ready_task = find_ready_task(load_priority(), roadmaps)

    return {
        'active_project_count': sum(1 for roadmap in roadmaps if roadmap.get('_lifecycle') == 'active'),
        'continuous_project_count': sum(1 for roadmap in roadmaps if roadmap.get('_lifecycle') == 'continuous'),
        'ready_task': ready_task,
        'projects_with_ready_tasks': [
            roadmap.get('_project')
            for roadmap in roadmaps
            if any(task.get('status') == 'ready' for task in roadmap.get('tasks', []))
        ],
        'projects_needing_human': [
            roadmap.get('_project')
            for roadmap in roadmaps
            if any(task.get('status') == 'needs-human' for task in roadmap.get('tasks', []))
        ],
    }


def check_todos() -> None:
    run([sys.executable, 'scripts/fetch_todos.py'], check=True)


def check_dependency_resolution() -> None:
    run([sys.executable, 'scripts/resolve_deps.py', '--dry-run'], check=True)


def check_digest(since: str) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        digest_path = Path(tmp) / 'digest.json'
        digest = run(
            [sys.executable, 'scripts/build_digest.py', '--since', since],
            capture=True,
            check=True,
        )
        digest_path.write_text(digest.stdout)
        run([sys.executable, 'scripts/validate_digest.py', str(digest_path)], check=True)
        print('[worker-check] digest JSON builds and validates', file=sys.stderr)


def sync_projects() -> None:
    if not os.environ.get('KR_API_TOKEN', '').strip():
        print('[worker-check] KR_API_TOKEN not set; skipping Project sync', file=sys.stderr)
        return

    run([sys.executable, 'scripts/sync_projects.py'], check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--since', default='24 hours ago')
    parser.add_argument(
        '--sync-projects',
        '--sync-dreams',  # legacy alias from the pre-split Dream sync
        dest='sync_projects',
        action='store_true',
        help='Also run scripts/sync_projects.py. Requires KR_API_TOKEN.',
    )
    args = parser.parse_args()

    print('[worker-check] model API calls are disabled by design', file=sys.stderr)
    check_todos()
    check_dependency_resolution()
    check_digest(args.since)

    if args.sync_projects and not args.dry_run:
        sync_projects()
    elif args.sync_projects:
        print('[worker-check] --dry-run set; skipping Project sync write', file=sys.stderr)

    summary = build_queue_summary()
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
