#!/usr/bin/env python3
"""
select_role.py — decide Worker vs Reviewer vs idle on arrival (conductor/t-026).

Neither "Worker" nor "Reviewer" is a property of which trigger fired a session;
it's a property of what the repo actually needs right now. This script is the
single front door a session runs FIRST, before following AGENTS.md's per-role
steps — it answers "what does this repo need from me today?" so a session that
was scheduled as "the Reviewer" but finds no PR to review does not idle or
no-op: it picks up ready work instead, and vice versa.

Root cause this replaces (conductor/t-026): two independently-scheduled
platform triggers ("Worker" hourly, "Reviewer" on a schedule that drifted from
actual worker/* PR volume) meant a session's role was decided BEFORE it ever
looked at live state, so a Reviewer-labeled session could fire 48+ times in a
row with nothing to review. The trigger schedule itself is a platform-level
setting outside this repo (AGENTS.md already documents that) — this script is
the repo-side half of the fix: whichever trigger fires, the session's first
action is now state-driven self-assignment, not blind role adherence.

This intentionally does not call OpenAI, Claude, or any other model API — same
contract as run_worker.py/run_reviewer.py, which it composes rather than
duplicates. Real role-appropriate work still happens in the actual session,
following AGENTS.md's "Role assignment" section.

Decision order (first match wins):
  1. candidate_worker_branch_count > 0   -> role: reviewer
  2. ready_task exists                   -> role: worker
  3. neither                             -> role: idle (dream-cycle fallback,
                                             per CREATION-SPEC.md's own
                                             "nothing better to do" contract)

Usage:
  python scripts/select_role.py [--dry-run]

Env:
  KR_API_TOKEN  optional; forwarded to run_worker.py's queue summary
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Allow `python scripts/select_role.py` (sys.path[0] == scripts/) as well as
# `import scripts.select_role` / `python -m scripts.select_role` (repo root on
# sys.path) — both are used, by the CLI usage above and by tests respectively.
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import scripts.run_reviewer as run_reviewer
import scripts.run_worker as run_worker


def select_role() -> dict[str, object]:
    try:
        run_reviewer.refresh_remotes()
    except Exception as error:  # pragma: no cover - network-dependent
        print(f'[select-role] remote refresh warning: {error}', file=sys.stderr)

    branches = run_reviewer.remote_worker_branches()
    queue = run_worker.build_queue_summary()
    ready_task = queue.get('ready_task')

    if branches:
        role = 'reviewer'
        reason = f'{len(branches)} open worker/* branch(es) awaiting review'
    elif ready_task:
        role = 'worker'
        reason = f'ready task available: {ready_task.get("project")}/{ready_task.get("task_id")}'
    else:
        role = 'idle'
        reason = 'no worker/* branches to review and no ready task — dream-cycle fallback applies'

    return {
        'role': role,
        'reason': reason,
        'candidate_worker_branch_count': len(branches),
        'candidate_worker_branches': branches,
        'ready_task': ready_task,
        'projects_with_ready_tasks': queue.get('projects_with_ready_tasks', []),
        'projects_needing_human': queue.get('projects_needing_human', []),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true', help='accepted for interface parity; this script never writes')
    parser.parse_args()

    print('[select-role] model API calls are disabled by design', file=sys.stderr)
    print('[select-role] this only recommends a role; the session decides what to do with it', file=sys.stderr)

    result = select_role()
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
