#!/usr/bin/env python3
"""Audit every Conductor roadmap and generate strategic maintenance reports.

The audit is intentionally conservative: it reports suspicious state and framework
problems but never rewrites roadmap task state. Humans and Worker/Reviewer agents
use the report to decide which repairs are safe.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from roadmap_deps import dependency_satisfied  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "projects"
VALID_STATUS = {
    "ready",
    "waiting",
    "blocked",
    "claimed",
    "review",
    "needs-human",
    "done",
    "challenged",
}
# The three enum values AGENTS.md/CLAUDE.md define for a task's `stakes:` field
# (PR handoff template, hard-gate list, status lifecycle). Anything else is almost
# always a different field's value (status, priority) that bled into `stakes` --
# see conductor/t-107.
VALID_STAKES = {"reversible", "outward-facing", "irreversible"}
ACTIVE_STATES = {"active"}
WORKABLE_STATES = {"active", "continuous"}
IN_PROGRESS = {"claimed", "review"}
TERMINAL = {"done"}
OPEN_STATES = VALID_STATUS - TERMINAL
STALE_DAYS = 3


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def find_duplicate_keys(text: str) -> list[tuple[str, int]]:
    """Return (key, line) for every key that appears more than once within
    the same YAML mapping. yaml.safe_load silently lets the last occurrence
    win, which has previously let a stale trailing owner/claimed_by/status
    trio override the real one (conductor/t-079)."""
    duplicates: list[tuple[str, int]] = []

    class _DupKeyLoader(yaml.SafeLoader):
        pass

    def construct_mapping(loader: yaml.SafeLoader, node: yaml.Node, deep: bool = False) -> dict[Any, Any]:
        mapping: dict[Any, Any] = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if key in mapping:
                duplicates.append((str(key), key_node.start_mark.line + 1))
            mapping[key] = loader.construct_object(value_node, deep=deep)
        return mapping

    _DupKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)
    try:
        yaml.load(text, Loader=_DupKeyLoader)
    except yaml.YAMLError:
        pass
    return duplicates


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [str(value).strip()] if str(value).strip() else []


def parse_time(value: Any) -> dt.datetime | None:
    if not value:
        return None
    text = str(value).strip().replace("Z", "+00:00")
    try:
        parsed = dt.datetime.fromisoformat(text)
    except ValueError:
        try:
            parsed = dt.datetime.strptime(text[:10], "%Y-%m-%d")
        except ValueError:
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def find_cycles(graph: dict[str, list[str]]) -> list[list[str]]:
    cycles: list[list[str]] = []
    stack: list[str] = []
    state: dict[str, int] = {}

    def visit(node: str) -> None:
        state[node] = 1
        stack.append(node)
        for dep in graph.get(node, []):
            if dep not in graph:
                continue
            if state.get(dep, 0) == 0:
                visit(dep)
            elif state.get(dep) == 1:
                start = stack.index(dep)
                cycle = stack[start:] + [dep]
                if cycle not in cycles:
                    cycles.append(cycle)
        stack.pop()
        state[node] = 2

    for node in graph:
        if state.get(node, 0) == 0:
            visit(node)
    return cycles


def issue(severity: str, code: str, project: str, message: str, task: str | None = None) -> dict[str, Any]:
    return {
        "severity": severity,
        "code": code,
        "project": project,
        "task": task,
        "message": message,
    }


def control_priority_band() -> list[str]:
    text = (ROOT / "CONTROL.md").read_text(encoding="utf-8")
    match = re.search(r"\*\*Priority order this week:\*\*(.*?)(?:\n\(|\n\n)", text, re.S)
    if not match:
        return []
    band = match.group(1).replace("\n", " ")
    return [part.strip().strip(". ") for part in band.split("→") if part.strip()]


def audit() -> dict[str, Any]:
    now = dt.datetime.now(dt.timezone.utc)
    overrides_data = load_yaml(ROOT / "project-overrides.yaml")
    priority_data = load_yaml(PROJECTS / "priority.yaml")
    priority = as_list(priority_data.get("order"))
    overrides = {
        str(entry.get("slug")): entry
        for entry in overrides_data.get("overrides", [])
        if isinstance(entry, dict) and entry.get("slug")
    }
    active = {slug for slug, entry in overrides.items() if entry.get("status") in ACTIVE_STATES}
    continuous = {slug for slug, entry in overrides.items() if entry.get("status") == "continuous"}
    workable = active | continuous

    findings: list[dict[str, Any]] = []
    projects: list[dict[str, Any]] = []
    roadmap_paths = sorted(PROJECTS.glob("*/roadmap.yaml"))
    roadmap_slugs = {path.parent.name for path in roadmap_paths if path.parent.name != "_template"}

    for slug in sorted(workable - set(priority)):
        findings.append(issue("error", "ACTIVE_MISSING_PRIORITY", slug, "Active project is absent from projects/priority.yaml."))
    for slug in priority:
        if slug not in roadmap_slugs:
            findings.append(issue("error", "PRIORITY_MISSING_ROADMAP", slug, "Priority entry has no projects/<slug>/roadmap.yaml."))
    duplicates = [slug for slug, count in collections.Counter(priority).items() if count > 1]
    for slug in duplicates:
        findings.append(issue("error", "DUPLICATE_PRIORITY", slug, "Project appears more than once in priority order."))

    control_band = control_priority_band()
    if control_band and priority[: len(control_band)] != control_band:
        findings.append(
            issue(
                "error",
                "CONTROL_PRIORITY_DRIFT",
                "_global",
                f"CONTROL.md priority band {control_band} does not match priority.yaml prefix {priority[:len(control_band)]}.",
            )
        )
    if priority and priority[-1] != "dream-cycle":
        findings.append(issue("error", "DREAM_CYCLE_NOT_LAST", "dream-cycle", "dream-cycle must remain the final priority entry."))

    for path in roadmap_paths:
        slug = path.parent.name
        if slug == "_template":
            continue
        data = load_yaml(path)
        for key, line in find_duplicate_keys(path.read_text(encoding="utf-8")):
            findings.append(
                issue(
                    "warning",
                    "DUPLICATE_YAML_KEY",
                    slug,
                    f"Duplicate key {key!r} at line {line} — YAML mapping semantics let the "
                    "last occurrence silently win; check for a stale trailing owner/claimed_by/"
                    "status value overriding the real one.",
                )
            )
        tasks = [task for task in data.get("tasks", []) if isinstance(task, dict)]
        task_by_id = {str(task.get("id")): task for task in tasks if task.get("id")}
        graph: dict[str, list[str]] = {}
        counts = collections.Counter(str(task.get("status", "missing")) for task in tasks)
        override = overrides.get(slug, {})
        override_status = override.get("status", "missing")
        kind = override.get("kind") or data.get("kind") or "unknown"

        if slug not in overrides:
            findings.append(issue("warning", "ROADMAP_MISSING_OVERRIDE", slug, "Roadmap has no project-overrides.yaml entry."))
        if slug not in priority and override_status in WORKABLE_STATES:
            findings.append(issue("error", "WORKABLE_ROADMAP_MISSING_PRIORITY", slug, "Active/continuous roadmap is not selectable because it is absent from priority.yaml."))
        if data.get("project") and str(data.get("project")) != slug:
            findings.append(issue("warning", "SLUG_MISMATCH", slug, f"roadmap project field is {data.get('project')!r}, not directory slug."))
        if not data.get("goal"):
            findings.append(issue("info", "MISSING_GOAL", slug, "Roadmap has no friendly goal/definition of done."))
        if not data.get("milestones"):
            findings.append(issue("info", "MISSING_MILESTONES", slug, "Roadmap has no milestone definitions."))

        ids = [str(task.get("id")) for task in tasks if task.get("id")]
        for task_id, count in collections.Counter(ids).items():
            if count > 1:
                findings.append(issue("error", "DUPLICATE_TASK_ID", slug, "Task id appears more than once.", task_id))

        for task in tasks:
            task_id = str(task.get("id", "<missing>"))
            status = str(task.get("status", "missing"))
            raw_deps = task.get("depends_on")
            deps = as_list(raw_deps)
            graph[task_id] = deps

            if not task.get("id"):
                findings.append(issue("error", "MISSING_TASK_ID", slug, "Task has no id."))
            if status not in VALID_STATUS:
                findings.append(issue("error", "INVALID_STATUS", slug, f"Unknown task status {status!r}.", task_id))
            raw_stakes = task.get("stakes")
            if raw_stakes is not None and str(raw_stakes) not in VALID_STAKES:
                findings.append(
                    issue(
                        "error",
                        "INVALID_STAKES_VALUE",
                        slug,
                        f"stakes value {raw_stakes!r} is not one of {sorted(VALID_STAKES)} -- "
                        "check for a status/priority value that landed in the wrong field.",
                        task_id,
                    )
                )
            if isinstance(raw_deps, str) and "," in raw_deps:
                findings.append(issue("error", "MALFORMED_DEPENDENCY_LIST", slug, f"depends_on is a comma-separated string: {raw_deps!r}; use a YAML list.", task_id))
            for dep in deps:
                if dep == task_id:
                    findings.append(issue("error", "SELF_DEPENDENCY", slug, "Task depends on itself.", task_id))
                elif dep not in task_by_id:
                    findings.append(issue("error", "MISSING_DEPENDENCY", slug, f"Dependency {dep!r} does not exist in this roadmap.", task_id))

            known_deps = [task_by_id[dep] for dep in deps if dep in task_by_id]
            all_done = bool(deps) and len(known_deps) == len(deps) and all(dependency_satisfied(dep) for dep in known_deps)
            unmet = [dep for dep in deps if dep not in task_by_id or not dependency_satisfied(task_by_id[dep])]
            if status == "waiting" and all_done:
                findings.append(issue("error", "WAITING_WITH_SATISFIED_DEPS", slug, "All dependencies are satisfied; resolver should promote this task to ready.", task_id))
            if status == "ready" and unmet:
                findings.append(issue("error", "READY_WITH_UNMET_DEPS", slug, f"Ready task has unmet dependencies: {', '.join(unmet)}.", task_id))
            if status == "done" and task.get("gate_human") and not task.get("approved_by_human"):
                findings.append(issue("error", "GATED_DONE_WITHOUT_APPROVAL", slug, "Human-gated task is done without approved_by_human: true.", task_id))
            if task.get("approved_by_human") and not task.get("gate_human"):
                findings.append(issue("info", "APPROVAL_WITHOUT_GATE", slug, "approved_by_human is set on a task that is not human-gated.", task_id))

            updated = parse_time(task.get("updated"))
            if status in IN_PROGRESS:
                if not updated:
                    findings.append(issue("warning", "IN_PROGRESS_WITHOUT_TIMESTAMP", slug, "Claimed/review task has no parseable updated timestamp.", task_id))
                elif (now - updated).days >= STALE_DAYS:
                    findings.append(issue("warning", "STALE_IN_PROGRESS", slug, f"Task has remained {status} for {(now - updated).days} days.", task_id))

            if status == "needs-human":
                hard_reasons = []
                if task.get("gate_human"):
                    hard_reasons.append("gate_human")
                if str(task.get("stakes", "")).lower() in {"needs-human", "outward-facing", "irreversible"}:
                    hard_reasons.append(str(task.get("stakes")))
                if kind in {"content", "proposal"}:
                    hard_reasons.append(kind)
                note = str(task.get("note", ""))
                if not hard_reasons and not task.get("soft_gate"):
                    findings.append(issue("warning", "SOFT_NEEDS_HUMAN", slug, "needs-human has no obvious hard-gate marker; consider returning it to ready, setting soft_gate: true, or documenting the actual gate.", task_id))
                if "FOR SILAS:" not in note:
                    findings.append(issue("info", "NEEDS_HUMAN_NOTE_FORMAT", slug, "needs-human note does not use the AGENTS.md FOR SILAS action format.", task_id))

            if status in OPEN_STATES and kind == "software" and task.get("gate_human") and str(task.get("stakes", "reversible")) == "reversible":
                note = str(task.get("note", "")).lower()
                if not any(word in note for word in ("publish", "deploy", "billing", "secret", "dns", "production", "security", "approve", "legal")):
                    findings.append(issue("warning", "POSSIBLY_UNNECESSARY_GATE", slug, "Reversible software task is human-gated without an obvious hard-gate reason in its note.", task_id))

            if status in OPEN_STATES and not task.get("title"):
                findings.append(issue("warning", "OPEN_TASK_MISSING_TITLE", slug, "Open task has no title.", task_id))
            if status in OPEN_STATES and not task.get("stakes"):
                findings.append(issue("info", "OPEN_TASK_MISSING_STAKES", slug, "Open task has no stakes classification.", task_id))

            ci = task.get("continuous_improvement")
            if isinstance(ci, dict):
                note_text = str(task.get("note", "")).lower()
                if any(phrase in note_text for phrase in ("next preferred lane", "rotate")):
                    ci_last_run = parse_time(ci.get("last_run"))
                    if updated and ci_last_run and updated > ci_last_run:
                        findings.append(
                            issue(
                                "warning",
                                "CONTINUOUS_IMPROVEMENT_NOTE_DRIFT",
                                slug,
                                "Task note mentions a lane rotation but continuous_improvement.last_run "
                                "predates the task's updated timestamp — the continuous_improvement block "
                                "(last_lane/next_lane/last_run/last_pr) may be stale relative to the note.",
                                task_id,
                            )
                        )

        for cycle in find_cycles(graph):
            findings.append(issue("error", "DEPENDENCY_CYCLE", slug, "Dependency cycle: " + " -> ".join(cycle)))

        open_count = sum(counts.get(state, 0) for state in OPEN_STATES)
        if override_status == "active" and tasks and open_count == 0:
            findings.append(issue("warning", "ACTIVE_PROJECT_NO_OPEN_TASKS", slug, "Active project has no open tasks; mark finished/paused or add an intentional recurring task."))
        if override_status not in WORKABLE_STATES and counts.get("ready", 0):
            findings.append(issue("info", "INACTIVE_PROJECT_HAS_READY_TASKS", slug, f"Inactive project retains {counts.get('ready', 0)} ready task(s); harmless but misleading in generated status."))
        if override_status == "active" and counts.get("done", 0) == len(tasks) and tasks:
            findings.append(issue("warning", "ACTIVE_PROJECT_ALL_DONE", slug, "All tasks are done but project override remains active."))

        projects.append(
            {
                "slug": slug,
                "kind": kind,
                "override_status": override_status,
                "priority_index": priority.index(slug) + 1 if slug in priority else None,
                "autonomous": bool(data.get("autonomous")),
                "task_count": len(tasks),
                "counts": dict(sorted(counts.items())),
                "open_count": open_count,
                "human_attention": counts.get("needs-human", 0),
                "ready": counts.get("ready", 0),
                "waiting": counts.get("waiting", 0),
                "claimed": counts.get("claimed", 0),
                "review": counts.get("review", 0),
                "done": counts.get("done", 0),
            }
        )

    severity_order = {"error": 0, "warning": 1, "info": 2}
    findings.sort(key=lambda item: (severity_order[item["severity"]], item["project"], item.get("task") or "", item["code"]))
    projects.sort(key=lambda item: (item["priority_index"] is None, item["priority_index"] or 9999, item["slug"]))

    return {
        "generated_at": now.isoformat(),
        "summary": {
            "roadmaps": len(projects),
            "active_projects": len(active),
            "continuous_projects": len(continuous),
            "tasks": sum(item["task_count"] for item in projects),
            "ready": sum(item["ready"] for item in projects),
            "waiting": sum(item["waiting"] for item in projects),
            "needs_human": sum(item["human_attention"] for item in projects),
            "in_progress": sum(item["claimed"] + item["review"] for item in projects),
            "done": sum(item["done"] for item in projects),
            "errors": sum(1 for item in findings if item["severity"] == "error"),
            "warnings": sum(1 for item in findings if item["severity"] == "warning"),
            "info": sum(1 for item in findings if item["severity"] == "info"),
        },
        "projects": projects,
        "findings": findings,
    }


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Roadmap Audit",
        "",
        f"Generated: `{report['generated_at']}`",
        "",
        "This is a conservative structural audit. It reports suspicious state; it does not automatically change task status or remove human gates.",
        "",
        "## Portfolio snapshot",
        "",
        f"- **{summary['roadmaps']}** roadmaps, **{summary['active_projects']}** active + **{summary['continuous_projects']}** continuous projects, **{summary['tasks']}** tasks",
        f"- **{summary['ready']} ready**, **{summary['waiting']} waiting**, **{summary['needs_human']} needs-human**, **{summary['in_progress']} claimed/review**, **{summary['done']} done**",
        f"- Findings: **{summary['errors']} errors**, **{summary['warnings']} warnings**, **{summary['info']} informational**",
        "",
        "## Project inventory",
        "",
        "| # | Project | State | Kind | Ready | Waiting | Human | In progress | Done / Total |",
        "|---:|---|---|---|---:|---:|---:|---:|---:|",
    ]
    for project in report["projects"]:
        index = project["priority_index"] if project["priority_index"] is not None else "—"
        in_progress = project["claimed"] + project["review"]
        lines.append(
            f"| {index} | `{project['slug']}` | {project['override_status']} | {project['kind']} | {project['ready']} | {project['waiting']} | {project['human_attention']} | {in_progress} | {project['done']} / {project['task_count']} |"
        )

    lines.extend(["", "## Findings by severity", ""])
    for severity in ("error", "warning", "info"):
        items = [item for item in report["findings"] if item["severity"] == severity]
        lines.append(f"### {severity.title()} ({len(items)})")
        lines.append("")
        if not items:
            lines.append("_None._")
        for item in items:
            location = f"`{item['project']}`"
            if item.get("task"):
                location += f" / `{item['task']}`"
            lines.append(f"- **{item['code']}** — {location}: {item['message']}")
        lines.append("")

    lines.extend(
        [
            "## Interpretation rules",
            "",
            "- **Errors** are deterministic framework or state defects and should normally be repaired promptly.",
            "- **Warnings** need judgment; they are candidates for roadmap cleanup, gate removal, or project-state changes.",
            "- **Informational** findings improve consistency but should not interrupt productive Worker execution.",
            "- A reported `POSSIBLY_UNNECESSARY_GATE` is not permission to bypass a real approval boundary. Confirm the task has no publishing, money, legal, production, secret, DNS, destructive, or security-sensitive consequence before removing the gate.",
            "",
            "## Regeneration",
            "",
            "```bash",
            "python scripts/audit_roadmaps.py",
            "```",
            "",
            "Use `--json <path>` and `--markdown <path>` to override output locations.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", default="ROADMAP-AUDIT.json")
    parser.add_argument("--markdown", default="ROADMAP-AUDIT.md")
    args = parser.parse_args()

    report = audit()
    json_path = ROOT / args.json
    markdown_path = ROOT / args.markdown
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(render_markdown(report), encoding="utf-8")
    print(
        f"Audited {report['summary']['roadmaps']} roadmaps: "
        f"{report['summary']['errors']} errors, "
        f"{report['summary']['warnings']} warnings, "
        f"{report['summary']['info']} info findings."
    )


if __name__ == "__main__":
    main()
