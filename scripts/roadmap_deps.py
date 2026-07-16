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

from typing import Any


def dependency_satisfied(task: dict[str, Any] | None) -> bool:
    """True when `task` (a dependency) is done enough to unblock a dependent task."""
    if not task or task.get("status") != "done":
        return False
    if task.get("gate_human"):
        return bool(task.get("approved_by_human"))
    return True
