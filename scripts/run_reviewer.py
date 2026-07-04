#!/usr/bin/env python3
"""
run_reviewer.py — deterministic Conductor reviewer healthcheck.

This script intentionally does not call Claude, OpenAI, or any other model API.
Real PR review happens from Claude/OpenAI sessions using GitHub connectors/tools.
GitHub Actions only reports whether there are worker branches that may need a
session-side review.

Usage:
  python scripts/run_reviewer.py [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent


def git(*args: str, check: bool = False) -> str:
    result = subprocess.run(
        ['git', *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    if check and result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f'git {" ".join(args)} failed')

    return result.stdout.strip()


def refresh_remotes() -> None:
    git('fetch', 'origin', '+refs/heads/*:refs/remotes/origin/*', '--prune')


def remote_worker_branches() -> list[dict[str, Any]]:
    raw = git('branch', '-r', '--no-merged', 'origin/main')
    branches: list[dict[str, Any]] = []

    for line in raw.splitlines():
        ref = line.strip()
        if not ref.startswith('origin/worker/'):
            continue

        branches.append(
            {
                'branch': ref.removeprefix('origin/'),
                'last_commit': git('log', '-1', '--pretty=format:%h %s', ref),
                'author': git('log', '-1', '--pretty=format:%an', ref),
                'age': git('log', '-1', '--pretty=format:%ar', ref),
            }
        )

    return branches


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    print('[reviewer-check] model API calls are disabled by design', file=sys.stderr)
    print('[reviewer-check] use a Claude/OpenAI session for actual PR review', file=sys.stderr)

    try:
        refresh_remotes()
    except Exception as error:
        print(f'[reviewer-check] remote refresh warning: {error}', file=sys.stderr)

    branches = remote_worker_branches()
    summary = {
        'reviewer_mode': 'session-driven',
        'dry_run': args.dry_run,
        'model_api_calls': False,
        'candidate_worker_branch_count': len(branches),
        'candidate_worker_branches': branches,
    }

    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
