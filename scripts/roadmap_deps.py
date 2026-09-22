#!/usr/bin/env python3
"""
roadmap_deps.py — shared dependency-satisfaction rule for roadmap tasks.

resolve_deps.py, next_ready_task.py, and audit_roadmaps.py each need the identical
"is this task done enough to unblock a dependent task" check. Kept in one module so
the rule can't drift between them, mirroring how roadmap_claims.py already
centralizes claim-staleness logic. See conductor/t-043.

A task satisfies a dependency when:
  status == done  AND  (gate_human is falsy  OR  approved_by_human is true)
"""

from __future__ import annotations

import re
from typing import Any


def dependency_satisfied(task: dict[str, Any] | None) -> bool:
    """True when `task` (a dependency) is done enough to unblock a dependent task."""
    if not task or task.get("status") != "done":
        return False
    if task.get("gate_human"):
        return bool(task.get("approved_by_human"))
    return True


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def zero_diff_close_hint(
    task: dict[str, Any], tasks_by_id: dict[str, dict[str, Any]]
) -> dict[str, Any] | None:
    """Advisory-only: does a `done` dependency of `task` already look like it
    satisfied `task`'s own acceptance criteria while closing its own scope?

    Kaizen from butterfly-gallery/t-031 (conductor/t-190): t-031 was a pure
    audit task sitting on `depends_on: t-033`. When t-033 landed, its own
    closing note named t-031's id up front and built to its acceptance
    criteria directly -- t-031 closed with zero code diff once a session
    actually read t-033's note. A `done` dependency whose `note:` mentions
    this task's own id (as a whole word) is worth flagging as "likely a
    zero-diff close" so the next session doesn't have to rediscover this by
    hand.

    Returns a dict describing the first matching dependency, or None. Never
    used for task selection, ordering, or auto-closing -- purely an
    informational hint for whichever session picks the task up.
    """
    task_id = task.get("id")
    if not task_id:
        return None
    id_pattern = re.compile(rf"\b{re.escape(str(task_id))}\b")

    for dep_id in _as_list(task.get("depends_on")):
        dep = tasks_by_id.get(str(dep_id))
        if not dep or dep.get("status") != "done":
            continue
        note = dep.get("note")
        if not isinstance(note, str) or not id_pattern.search(note):
            continue
        return {
            "dependency_task_id": dep.get("id"),
            "reason": (
                f"dependency {dep.get('id')} is done and its note mentions "
                f"{task_id} -- worth checking before implementing from scratch"
            ),
        }
    return None
