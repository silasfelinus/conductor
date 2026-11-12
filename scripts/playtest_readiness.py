"""Evidence-based handoff policy for games entering the playtest lifecycle.

A playtest project has shipped its finite authored content and verification work.
Only explicitly recurring iterative polish and genuine human gates may remain.
The human's verdict is NOT implied by declaring the project playtest.
"""
from __future__ import annotations


def playtest_readiness_errors(tasks: list[dict]) -> list[str]:
    if not tasks:
        return ["roadmap has no tasks"]

    errors = []
    outstanding = [
        str(task.get("id", "<unknown>"))
        for task in tasks
        if isinstance(task, dict)
        and not task.get("recurring")
        and not task.get("gate_human")
        and task.get("status") not in ("done", "cancelled")
    ]
    if outstanding:
        errors.append("agent-owned tasks still open: " + ", ".join(outstanding[:12]))

    final_gates = [
        task for task in tasks
        if isinstance(task, dict)
        and task.get("gate_human") is True
        and task.get("gate_reason") in ("subjective-acceptance", "creative-approval")
        and task.get("status") == "needs-human"
        and not task.get("approved_by_human")
    ]
    if not final_gates:
        errors.append(
            "requires an unapproved subjective-acceptance/creative-approval "
            "task with gate_human: true and status: needs-human"
        )
    return errors
