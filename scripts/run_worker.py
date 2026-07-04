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
  python scripts/run_worker.py [--dry-run] [--since "24 hours ago"] [--sync-dreams]

Env:
  KR_API_TOKEN  optional; enables kind_robots todo checks and Dream sync
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


def load_active_overrides() -> dict[str, dict[str, Any]]:
    data = load_yaml(OVERRIDES_FILE)
    overrides: dict[str, dict[str, Any]] = {}
    for entry in data.get('overrides', []):
        slug = entry.get('slug')
        if slug:
            overrides[str(slug)] = entry
    return overrides


def load_roadmaps() -> list[dict[str, Any]]:
    overrides = load_active_overrides()
    roadmaps: list[dict[str, Any]] = []

    for path in sorted(PROJECTS_DIR.glob('*/roadmap.yaml')):
        if path.parent.name == '_template':
            continue

        roadmap = load_yaml(path)
        slug = roadmap.get('project') or path.parent.name
        override = overrides.get(str(slug), {})

        if override.get('status', 'active') != 'active':
            continue

        roadmap['_path'] = str(path)
        roadmap['_project'] = str(slug)
        roadmaps.append(roadmap)

    return roadmaps


def find_ready_task(priority_order: list[str], roadmaps: list[dict[str, Any]]) -> dict[str, Any] | None:
    by_project = {roadmap.get('_project'): roadmap for roadmap in roadmaps}
    ordered = [by_project[slug] for slug in priority_order if slug in by_project]
    remaining = [roadmap for roadmap in roadmaps if roadmap.get('_project') not in priority_order]

    for roadmap in ordered + remaining:
        for task in roadmap.get('tasks', []):
            if task.get('status') == 'ready':
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
        'active_project_count': len(roadmaps),
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


def sync_dreams() -> None:
    if not os.environ.get('KR_API_TOKEN', '').strip():
        print('[worker-check] KR_API_TOKEN not set; skipping Dream sync', file=sys.stderr)
        return

    run([sys.executable, 'scripts/sync_projects_to_dreams.py'], check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--since', default='24 hours ago')
    parser.add_argument(
        '--sync-dreams',
        action='store_true',
        help='Also run scripts/sync_projects_to_dreams.py. Requires KR_API_TOKEN.',
    )
    args = parser.parse_args()

    print('[worker-check] model API calls are disabled by design', file=sys.stderr)
    check_todos()
    check_dependency_resolution()
    check_digest(args.since)

    if args.sync_dreams and not args.dry_run:
        sync_dreams()
    elif args.sync_dreams:
        print('[worker-check] --dry-run set; skipping Dream sync write', file=sys.stderr)

    summary = build_queue_summary()
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
