"""Evidence-based handoff policy for games entering the playtest lifecycle.

A playtest project has shipped its finite authored content and verification work.
Only explicitly recurring iterative polish and independent non-build approvals may remain.
A genuine subjective fun verdict or separate publication approval is not a finite
production task even when its legacy task is still marked waiting.
Human playtesting and a subjective verdict happen AFTER the roadmap is closed.
The handoff does not authorize publication, sharing, or wider promotion.
"""
from __future__ import annotations


def pending_agent_owned_task_ids(tasks: list[dict]) -> list[str]:
    return [
        str(task.get("id", "<unknown>"))
        for task in tasks
        if isinstance(task, dict)
        and not task.get("recurring")
        and not task.get("playtest_iteration")
        and task.get("status") not in ("done", "cancelled")
        and not (
            task.get("gate_human") is True
            and (
                task.get("gate_reason") in ("subjective-acceptance", "publish")
                or (
                    task.get("gate_reason") == "creative-approval"
                    and task.get("status") == "needs-human"
                )
            )
        )
    ]


def playtest_readiness_errors(tasks: list[dict]) -> list[str]:
    if not tasks:
        return ["roadmap has no tasks"]

    errors = []
    malformed = [index for index, task in enumerate(tasks, 1) if not isinstance(task, dict)]
    if malformed:
        errors.append("malformed roadmap tasks at positions: " + ", ".join(map(str, malformed[:12])))
    outstanding = pending_agent_owned_task_ids(tasks)
    if outstanding:
        errors.append("agent-owned tasks still open: " + ", ".join(outstanding[:12]))

    return errors
