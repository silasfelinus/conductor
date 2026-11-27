#!/usr/bin/env python3
"""
build_status.py — Regenerate STATUS.md from projects/*/roadmap.yaml and pitches/*.md

Run from repo root: python scripts/build_status.py
"""

import os
import re
import yaml
from datetime import datetime, timezone
from pathlib import Path

try:
    from daily_gate import already_recorded_today
    from next_ready_task import task_is_unblocked
    from roadmap_claims import task_is_claimable
except ModuleNotFoundError:
    from scripts.daily_gate import already_recorded_today
    from scripts.next_ready_task import task_is_unblocked
    from scripts.roadmap_claims import task_is_claimable

try:
    from playtest_readiness import pending_agent_owned_task_ids
except ModuleNotFoundError:
    from scripts.playtest_readiness import pending_agent_owned_task_ids

try:
    from project_lifecycle import PROJECT_LIFECYCLE_STATUSES, lifecycle_status, load_project_overrides, ordered_workable_slugs
except ModuleNotFoundError:  # imported as scripts.build_status in pytest
    from scripts.project_lifecycle import PROJECT_LIFECYCLE_STATUSES, lifecycle_status, load_project_overrides, ordered_workable_slugs

REPO_ROOT = Path(__file__).parent.parent
PROJECTS_DIR = REPO_ROOT / "projects"
PITCHES_DIR = REPO_ROOT / "pitches"
STATUS_FILE = REPO_ROOT / "STATUS.md"
OVERRIDES_FILE = REPO_ROOT / "project-overrides.yaml"

STATUS_COLS = ["ready", "waiting", "claimed", "review", "done", "blocked", "needs-human"]


def load_roadmap(project_dir: Path) -> dict | None:
    roadmap = project_dir / "roadmap.yaml"
    if not roadmap.exists():
        return None
    with open(roadmap) as f:
        return yaml.safe_load(f)


def compute_progress(milestones: list[dict], tasks: list[dict] | None = None) -> float:
    tasks = tasks or []
    total_m = sum(m.get("weight", 10) for m in milestones)
    done_m = sum(
        m.get("weight", 10) * (1.0 if m.get("status") == "done" else 0.5 if m.get("status") == "in-progress" else 0.0)
        for m in milestones
    )
    if total_m and done_m > 0:
        progress = round(done_m / total_m * 100, 1)
    else:
        # Milestones may be stale; preserve the existing task-ratio fallback.
        counted = [t for t in tasks if t.get("status") != "cancelled"]
        done_t = sum(1 for t in counted if t.get("status") == "done")
        progress = round(done_t / len(counted) * 100, 1) if counted else 0.0

    # 100% is a finite-work handoff, not milestone arithmetic. Genuine release
    # approvals and deferred subjective verdicts are exempt, but unfinished
    # authored content, art, build and QA must hold the number below 100.
    finite = [
        task for task in tasks
        if not task.get("recurring") and not task.get("playtest_iteration")
    ]
    if finite:
        has_completed = any(task.get("status") == "done" for task in finite)
        if not has_completed or pending_agent_owned_task_ids(tasks):
            return min(progress, 99.0)
        return 100.0
    return progress


def count_tasks(tasks: list[dict]) -> dict[str, int]:
    counts = {s: 0 for s in STATUS_COLS}
    for t in tasks:
        s = t.get("status", "ready")
        if s in counts:
            counts[s] += 1
    return counts


def get_pitches_pending() -> list[tuple[str, str, str]]:
    """Returns (title, date, project_target) for pitches with status awaiting-silas."""
    results = []
    if not PITCHES_DIR.exists():
        return results
    for f in sorted(PITCHES_DIR.glob("*.md")):
        if f.name == "README.md":
            continue
        text = f.read_text()
        title = re.search(r"^#\s*Pitch:\s*(.+)$", text, re.MULTILINE)
        title = title.group(1).strip() if title else f.stem
        date_match = re.match(r"(\d{4}-\d{2}-\d{2})-", f.name)
        date = date_match.group(1) if date_match else "unknown"
        status_match = re.search(
            r"^(?:status:\s*|\*\*Status:\*\*\s*)(.+)$",
            text,
            re.MULTILINE | re.IGNORECASE,
        )
        status = (
            status_match.group(1).strip().lower()
            if status_match
            else "awaiting-silas"
        )
        target_match = re.search(r"^project-target:\s*(.+)$", text, re.MULTILINE)
        target = target_match.group(1).strip() if target_match else "—"
        if "awaiting" in status:
            results.append((title, date, target))
    return results


def pickup_rows(project_tasks: dict, overrides: dict, order: list[str], *, now: datetime) -> list[str]:
    """Small read-only index, never a claim or proof that a review is complete."""
    rows = []
    for slug in ordered_workable_slugs(order, overrides):
        tasks = project_tasks.get(slug, [])
        by_id = {str(task["id"]): task for task in tasks if task.get("id")}
        ready = [
            str(task["id"])
            for task in tasks
            if task.get("id")
            and task.get("status") == "ready"
            and task_is_claimable(task, tasks_by_id=by_id, now=now)
            and task_is_unblocked(task, by_id)
            and not already_recorded_today(task, now=now)
        ]
        review = [
            str(task["id"]) for task in tasks
            if task.get("id") and task.get("status") == "review"
        ]

        def short(ids: list[str], limit: int) -> str:
            if not ids:
                return "—"
            return ", ".join(ids[:limit]) + (
                f" (+{len(ids) - limit} more)" if len(ids) > limit else ""
            )

        if ready or review:
            rows.append(
                f"| {slug} | {lifecycle_status(overrides, slug)} "
                f"| {short(review, 6)} | {short(ready, 3)} |"
            )
    return rows


def _without_stamp(text: str) -> str:
    # The "Last generated" line alone must not create a commit on main.
    return "\n".join(l for l in text.splitlines() if not l.startswith("<!-- Last generated:"))


def build_status():
    generated_at = datetime.now(timezone.utc)
    now = generated_at.strftime("%Y-%m-%dT%H:%M:%SZ")

    project_rows = []
    project_tasks = {}
    global_counts = {s: 0 for s in STATUS_COLS}
    workable_needs_human = 0
    archival_needs_human = 0
    overrides = load_project_overrides(OVERRIDES_FILE)
    lifecycle_counts = {status: 0 for status in PROJECT_LIFECYCLE_STATUSES}

    for project_dir in sorted(PROJECTS_DIR.iterdir()):
        if not project_dir.is_dir() or project_dir.name.startswith("_"):
            continue
        roadmap = load_roadmap(project_dir)
        if not roadmap:
            continue

        lifecycle = lifecycle_status(overrides, project_dir.name)
        lifecycle_counts[lifecycle] += 1
        milestones = roadmap.get("milestones") or []
        tasks = roadmap.get("tasks") or []
        project_tasks[project_dir.name] = [task for task in tasks if isinstance(task, dict)]
        kind = roadmap.get("kind", "software")
        progress = compute_progress(milestones, tasks)
        counts = count_tasks(tasks)

        for k, v in counts.items():
            global_counts[k] += v

        if lifecycle in {"active", "playtest", "continuous"}:
            workable_needs_human += counts["needs-human"]
        else:
            archival_needs_human += counts["needs-human"]

        project_rows.append(
            f"| {project_dir.name} | {lifecycle} | {kind} | {progress}% "
            f"| {counts['ready']} | {counts['done']} | {counts['blocked']} |"
        )

    priority_path = PROJECTS_DIR / "priority.yaml"
    priority_data = yaml.safe_load(priority_path.read_text(encoding="utf-8")) if priority_path.exists() else {}
    order = (priority_data or {}).get("order", [])
    pickup = pickup_rows(project_tasks, overrides, order, now=generated_at)

    pitches = get_pitches_pending()
    pitch_rows = [f"| {t} | {d} | {p} |" for t, d, p in pitches]

    lines = [
        "# STATUS.md — Auto-generated project snapshot",
        f"<!-- Generated by scripts/build_status.py — DO NOT EDIT BY HAND -->",
        f"<!-- Last generated: {now} -->",
        "",
        "> This file is regenerated each cycle. Edit `CONTROL.md` to steer; edit `projects/*/roadmap.yaml` to update task state.",
        "",
        "## Global",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Active projects | {lifecycle_counts['active']} |",
        f"| Playtest projects | {lifecycle_counts['playtest']} |",
        f"| Continuous projects | {lifecycle_counts['continuous']} |",
        f"| Paused projects | {lifecycle_counts['paused']} |",
        f"| Finished projects | {lifecycle_counts['finished']} |",
        f"| Retired projects | {lifecycle_counts['retired']} |",
        f"| Total tasks | {sum(global_counts.values())} |",
        f"| Ready | {global_counts['ready']} |",
        f"| In progress (claimed/review) | {global_counts['claimed'] + global_counts['review']} |",
        f"| Needs human (all history) | {global_counts['needs-human']} |",
        f"| Needs human (workable projects) | {workable_needs_human} |",
        f"| Needs human (archival projects) | {archival_needs_human} |",
        f"| Blocked | {global_counts['blocked']} |",
        f"| Pitches pending | {len(pitches)} |",
        "",
        "## Agent pickup hints",
        "",
        "> Advisory snapshot, ordered by lifecycle and priority. Review IDs first; "
        "verify PRs, live task state, CONTROL.md and ownership before acting. "
        "Ready hints exclude blocked, resting and already-run daily tasks. "
        "Expired claims are handled by Process task events. Missing rows are not proof of no work.",
        "> Connector agents: fetch `ops/agent-context/<project>.json` for exact canonical task and CONTROL ranges, source commit, and advisory role hints.",
        "",
        "| Project | Lifecycle | Review IDs | Ready candidates (up to 3) |",
        "|---|---|---|---|",
        *(pickup if pickup else ["| (none) | — | — | — |"]),
        "",
        "## Projects",
        "",
        "| Project | Lifecycle | Kind | Progress | Ready | Done | Blocked |",
        "|---|---|---|---|---|---|---|",
        *project_rows,
        "",
        "## Pitches awaiting vote",
        "",
        "| Pitch | Date | Target |",
        "|---|---|---|",
        *(pitch_rows if pitch_rows else ["| (none) | — | — |"]),
    ]

    text = "\n".join(lines) + "\n"
    if STATUS_FILE.is_file() and _without_stamp(STATUS_FILE.read_text()) == _without_stamp(text):
        print("STATUS.md unchanged apart from its generation stamp; not rewritten")
        return
    STATUS_FILE.write_text(text)
    print(f"STATUS.md written ({len(project_rows)} projects, {len(pitches)} pitches)")


if __name__ == "__main__":
    build_status()
