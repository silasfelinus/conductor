#!/usr/bin/env python3
"""Generate small, connector-readable source locators; never mutate task state."""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import yaml

try:
    from daily_gate import already_recorded_today
    from next_ready_task import task_is_unblocked
    from project_lifecycle import lifecycle_status, load_project_overrides, ordered_workable_slugs
    from project_triage import role_hint
    from roadmap_claims import task_is_claimable
    from show_control import GLOBAL_RE, PER_PROJECT_RE, BLOCK_RE
except ModuleNotFoundError:
    from scripts.daily_gate import already_recorded_today
    from scripts.next_ready_task import task_is_unblocked
    from scripts.project_lifecycle import lifecycle_status, load_project_overrides, ordered_workable_slugs
    from scripts.project_triage import role_hint
    from scripts.roadmap_claims import task_is_claimable
    from scripts.show_control import GLOBAL_RE, PER_PROJECT_RE, BLOCK_RE

ROOT = Path(__file__).resolve().parents[1]
TERMINAL = {"done", "cancelled", "superseded", "dropped", "closed", "wontfix", "skipped", "retired"}


def git_blob(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw, usedforsecurity=False).hexdigest()


def control_ranges(text: str) -> tuple[list[int] | None, dict[str, list[int]]]:
    lines = text.splitlines()
    start = next((i for i, line in enumerate(lines) if GLOBAL_RE.match(line)), None)
    end = next((i for i, line in enumerate(lines) if PER_PROJECT_RE.match(line)), len(lines))
    global_range = [start + 1, end] if start is not None and start < end else None
    blocks = {}
    slug, first = None, None
    for i in range(end + 1, len(lines)):
        match = BLOCK_RE.match(lines[i])
        if match or lines[i].startswith("## "):
            if slug is not None:
                blocks[slug] = [first + 1, i]
            slug, first = (match.group(1), i) if match else (None, None)
    if slug is not None:
        blocks[slug] = [first + 1, len(lines)]
    return global_range, blocks


def task_ranges(text: str) -> dict[str, list[int]]:
    """Use YAML node marks, not regexes that can mistake a nested id for a task."""
    root = yaml.compose(text, Loader=yaml.SafeLoader)
    if not isinstance(root, yaml.MappingNode):
        return {}
    pair = next((value for key, value in root.value if key.value == "tasks"), None)
    if not isinstance(pair, yaml.SequenceNode):
        return {}
    ranges = {}
    for node in pair.value:
        if not isinstance(node, yaml.MappingNode):
            continue
        task_id = next((v.value for k, v in node.value if k.value == "id" and isinstance(v, yaml.ScalarNode)), None)
        if task_id is None:
            continue
        first = node.start_mark.line + 1
        # Block mapping end is normally the next task/key or EOF on a new line.
        # EOF without a newline instead ends on the final value's own line.
        mark = node.end_mark
        last = mark.line + (1 if mark.column and (node.flow_style or mark.index == len(text)) else 0)
        ranges[task_id] = [first, max(first, last)]
    return ranges


def project_packet(root: Path, slug: str, lifecycle: str, source_commit: str,
                   control: dict, master_issue: str | None, now: datetime) -> dict:
    path = root / "projects" / slug / "roadmap.yaml"
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    roadmap = yaml.safe_load(text) or {}
    kind = roadmap.get("kind", "software")
    tasks = [t for t in roadmap.get("tasks", []) if isinstance(t, dict) and t.get("id")]
    by_id = {str(t["id"]): t for t in tasks}
    ranges = task_ranges(text)
    ready, review, entries = [], [], {}
    for task in tasks:
        tid = str(task["id"])
        status = task.get("status")
        if status in TERMINAL:
            continue
        if tid not in ranges:
            raise ValueError(f"{slug}/{tid}: missing canonical source range")
        entry = {"lines": ranges[tid], "status": status, "role_hint": role_hint(task, kind),
                 "title": str(task.get("title", ""))[:160]}
        # No note/history copy. All details and acceptance remain in the canonical range.
        for key in ("depends_on", "gate_human", "approved_by_human", "stakes", "remaining_scope_task",
                    "recurring", "daily_commitment", "implementation_pr", "source_issue"):
            if key in task:
                entry[key] = task[key]
        entries[tid] = entry
        if status == "review":
            review.append(tid)
        elif (status == "ready" and task_is_claimable(task, tasks_by_id=by_id, now=now)
              and task_is_unblocked(task, by_id) and not already_recorded_today(task, now=now)):
            ready.append(tid)
    return {
        "version": 1, "advisory": True, "source_commit": source_commit, "project": slug,
        "lifecycle": lifecycle, "kind": kind, "roadmap": {
            "path": str(path.relative_to(root)), "blob": git_blob(raw),
        },
        "control": control, "master_issue": master_issue,
        "review": review[:6], "review_count": len(review), "ready": ready[:3], "ready_count": len(ready),
        "tasks": entries,
    }


def write_packet(path: Path, packet: dict) -> bool:
    """Write a locator unless only its source_commit would change.

    Every field that names source content (roadmap/CONTROL blobs, line ranges,
    statuses) is part of the packet, so an otherwise-identical packet means the
    previously recorded commit still holds byte-identical sources and remains a
    valid ref. Rewriting it anyway touched every locator on every refresh.
    """
    if path.is_file():
        try:
            previous = json.loads(path.read_text(encoding="utf-8"))
        except ValueError:
            previous = None
        if isinstance(previous, dict) and previous.get("source_commit"):
            strip = lambda d: {k: v for k, v in d.items() if k != "source_commit"}
            if strip(previous) == strip(json.loads(json.dumps(packet, default=str))):
                return False
    path.write_text(json.dumps(packet, ensure_ascii=False, separators=(",", ":"), default=str) + "\n",
                    encoding="utf-8")
    return True


def generate(root: Path, source_commit: str, now: datetime) -> int:
    raw = (root / "CONTROL.md").read_bytes()
    global_range, blocks = control_ranges(raw.decode("utf-8"))
    control_blob = git_blob(raw)
    overrides = load_project_overrides(root / "project-overrides.yaml")
    priority = yaml.safe_load((root / "projects/priority.yaml").read_text(encoding="utf-8")) or {}
    issue_path = root / "docs/agents/master-issues.yaml"
    issues = (yaml.safe_load(issue_path.read_text(encoding="utf-8")) or {}).get("master_issues", {}) if issue_path.exists() else {}
    out = root / "ops/agent-context"
    out.mkdir(parents=True, exist_ok=True)
    expected = set()
    for slug in ordered_workable_slugs(priority.get("order", []), overrides):
        if not (root / "projects" / slug / "roadmap.yaml").is_file():
            continue
        packet = project_packet(root, slug, lifecycle_status(overrides, slug), source_commit,
                                {"path": "CONTROL.md", "blob": control_blob, "global_lines": global_range,
                                 "project_lines": blocks.get(slug)}, issues.get(slug), now)
        name = slug + ".json"
        expected.add(name)
        write_packet(out / name, packet)
    # This directory is exclusively generated, never a canonical record.
    for file in out.glob("*.json"):
        if file.name not in expected:
            file.unlink()
    return len(expected)


def main() -> None:
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    count = generate(ROOT, commit, datetime.now(timezone.utc))
    print(f"Generated {count} advisory project context locators")


if __name__ == "__main__":
    main()
