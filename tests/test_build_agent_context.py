from datetime import datetime, timezone
import json

import yaml

from scripts.build_agent_context import control_ranges, generate, git_blob, role_hint, task_ranges

NOW = datetime(2026, 11, 26, 22, tzinfo=timezone.utc)


def test_ranges_preserve_exact_task_without_neighbor():
    text = ("project: demo\ntasks:\n  - id: t-001\n    title: First\n"
            "    note: |\n      nested - id: fake\n      more\n"
            "  - id: t-002\n    title: Second\n    status: ready\n")
    ranges = task_ranges(text)
    assert ranges == {"t-001": [3, 7], "t-002": [8, 10]}
    for tid, (start, end) in ranges.items():
        assert yaml.safe_load("\n".join(text.splitlines()[start-1:end]))[0]["id"] == tid
    assert task_ranges(text.rstrip()) == ranges
    # Root-level task sequence and another top-level field.
    assert task_ranges("tasks:\n- id: a\n  status: ready\nnotes: yes\n") == {"a": [2, 3]}


def test_control_ranges_match_scoped_sections():
    text = "# CONTROL\n## Global overview\nGlobal\n## Per-project direction\n### one (software)\nOne\n### two\nTwo\n## End\n"
    assert control_ranges(text) == ([2, 3], {"one": [5, 6], "two": [7, 8]})


def test_role_hint_is_advisory():
    assert role_hint({"status": "review", "lane": "art"}, "software") == "reviewer"
    assert role_hint({"daily_commitment": True}, "software") == "daily-creative"
    assert role_hint({"lane": "art"}, "software") == "art"
    assert role_hint({"lane": "qa"}, "software") == "qa"
    assert role_hint({}, "content") == "content"
    assert role_hint({"gate_human": True}, "software") == "developer"


def test_generation_uses_canonical_blob_and_filters_candidates(tmp_path):
    (tmp_path / "projects/demo").mkdir(parents=True)
    (tmp_path / "projects/paused").mkdir()
    (tmp_path / "CONTROL.md").write_text("## Global overview\nglobal\n## Per-project direction\n### demo\ndirection\n")
    (tmp_path / "projects/priority.yaml").write_text("order: [paused, demo]\n")
    (tmp_path / "project-overrides.yaml").write_text("overrides: [{slug: demo, status: active}, {slug: paused, status: paused}]\n")
    tasks = [
        {"id": "t-001", "status": "done"},
        {"id": "t-002", "status": "ready", "depends_on": ["t-001"], "note": "Long private task history"},
        {"id": "t-003", "status": "review", "title": "Review me"},
        {"id": "t-004", "status": "ready", "depends_on": "t-003"},
        {"id": "t-005", "status": "ready", "rest_until": "2026-11-27T01:00:00Z"},
        {"id": "t-006", "status": "ready", "remaining_scope_task": "t-003"},
        {"id": "t-007", "status": "claimed", "claimed_at": "2026-11-26T18:00:00Z"},
    ]
    path = tmp_path / "projects/demo/roadmap.yaml"
    path.write_text(yaml.safe_dump({"kind": "software", "tasks": tasks}, sort_keys=False))
    (tmp_path / "projects/paused/roadmap.yaml").write_text(path.read_text())
    assert generate(tmp_path, "a" * 40, NOW) == 1
    out = tmp_path / "ops/agent-context"
    packet = json.loads((out / "demo.json").read_text())
    assert packet["source_commit"] == "a" * 40 and packet["advisory"]
    assert packet["roadmap"]["blob"] == git_blob(path.read_bytes())
    assert packet["control"]["project_lines"] == [4, 5]
    assert packet["ready"] == ["t-002"] and packet["review"] == ["t-003"]
    assert "t-001" not in packet["tasks"] and "t-007" in packet["tasks"]
    assert "Long private task history" not in (out / "demo.json").read_text()
    assert not (out / "paused.json").exists()
    (out / "paused.json").write_text("{}")
    generate(tmp_path, "a" * 40, NOW)
    assert not (out / "paused.json").exists()
