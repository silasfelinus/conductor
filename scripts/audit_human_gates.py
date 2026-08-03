#!/usr/bin/env python3
"""Audit active Conductor human gates for stale-state signals.

The report lists every `status: needs-human` task in active projects and flags
only strong contradictions or explicit resolved-language. It is read-only and
never treats a suggestion as permission to bypass a genuine human gate.

Paused, retired, and finished projects are excluded by default according to
project-overrides.yaml. Use --include-inactive for an intentional archive
sweep.

Usage:
  python scripts/audit_human_gates.py
  python scripts/audit_human_gates.py --json
  python scripts/audit_human_gates.py --include-inactive
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "projects"
OVERRIDES = ROOT / "project-overrides.yaml"
ACTIVE_STATUS = "active"

# These phrases describe completed state, not merely a future condition. Keep
# this deliberately narrow: a false negative is preferable to nagging Silas
# about a real privacy, publishing, billing, or local-infrastructure decision.
RESOLVED_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "nothing-left",
        re.compile(
            r"\b(?:there is |there's )?nothing (?:else )?left to "
            r"(?:approve|decide|confirm|do)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "safe-to-close",
        re.compile(
            r"\b(?:looks |appears )?safe to set (?:its |the )?"
            r"status(?::| to)?\s*done\b",
            re.IGNORECASE,
        ),
    ),
    (
        "recovery-met",
        re.compile(
            r"\brecovery (?:bar|criteria) "
            r"(?:is|are|was|were|has been|have been) (?:met|satisfied)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "already-complete",
        re.compile(
            r"\b(?:the )?(?:requested work|implementation|decision) "
            r"(?:is|was|has been) already (?:complete|completed|done|merged)\b",
            re.IGNORECASE,
        ),
    ),
)


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def load_project_statuses(path: Path) -> dict[str, str]:
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


def stale_reasons(task: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if task.get("approved_by_human") is True:
        reasons.append("approved-by-human-but-still-needs-human")

    text = f"{task.get('title', '')}\n{task.get('note', '')}"
    for reason, pattern in RESOLVED_PATTERNS:
        if pattern.search(text):
            reasons.append(reason)
    return reasons


def scan(
    projects_dir: Path = PROJECTS,
    overrides_path: Path | None = None,
    include_inactive: bool = False,
) -> list[dict[str, Any]]:
    lifecycle_path = overrides_path or projects_dir.parent / "project-overrides.yaml"
    project_statuses = load_project_statuses(lifecycle_path)
    gates: list[dict[str, Any]] = []

    for roadmap_path in sorted(projects_dir.glob("*/roadmap.yaml")):
        project_slug = roadmap_path.parent.name
        if project_slug == "_template":
            continue
        lifecycle = project_statuses.get(project_slug, ACTIVE_STATUS)
        if not include_inactive and lifecycle != ACTIVE_STATUS:
            continue

        roadmap = load_yaml(roadmap_path)
        for task in roadmap.get("tasks", []) or []:
            if not isinstance(task, dict) or task.get("status") != "needs-human":
                continue
            gates.append(
                {
                    "project": project_slug,
                    "project_status": lifecycle,
                    "task_id": task.get("id"),
                    "title": task.get("title"),
                    "soft_gate": bool(task.get("soft_gate")),
                    "gate_human": bool(task.get("gate_human")),
                    "stakes": task.get("stakes"),
                    "approved_by_human": task.get("approved_by_human"),
                    "updated": task.get("updated"),
                    "stale_reasons": stale_reasons(task),
                }
            )

    return sorted(
        gates,
        key=lambda gate: (
            gate["soft_gate"],
            gate["project"],
            str(gate["task_id"]),
        ),
    )


def render(gates: list[dict[str, Any]]) -> str:
    if not gates:
        return "No active-project human gates found."

    findings = [gate for gate in gates if gate["stale_reasons"]]
    lines = [
        f"Active human gates: {len(gates)}",
        f"Strong stale-state signals: {len(findings)}",
        "",
    ]
    for gate in gates:
        flavor = "soft" if gate["soft_gate"] else "hard"
        suffix = ""
        if gate["stale_reasons"]:
            suffix = f"  REVIEW: {', '.join(gate['stale_reasons'])}"
        lines.append(
            f"- {gate['project']}/{gate['task_id']} [{flavor}] "
            f"{gate['title']}{suffix}"
        )

    if findings:
        lines.extend(
            [
                "",
                "Review the flagged task notes and current evidence. This report does not "
                "authorize closing a genuine gate.",
            ]
        )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument(
        "--include-inactive",
        action="store_true",
        help="also scan paused, retired, and finished projects",
    )
    args = parser.parse_args()

    gates = scan(include_inactive=args.include_inactive)
    findings = [gate for gate in gates if gate["stale_reasons"]]
    if args.json:
        print(json.dumps({"gates": gates, "findings": findings}, indent=2))
    else:
        print(render(gates))

    # A finding means human review is needed, not that the task is safe to close.
    sys.exit(1 if findings else 0)


if __name__ == "__main__":
    main()
