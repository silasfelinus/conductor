from datetime import datetime, timezone
from pathlib import Path

import scripts.build_status as build_status


def test_status_counts_real_lifecycle_states(tmp_path: Path, monkeypatch) -> None:
    projects = tmp_path / "projects"
    projects.mkdir()
    (tmp_path / "pitches").mkdir()
    (tmp_path / "project-overrides.yaml").write_text(
        "overrides:\n"
        "  - slug: finite\n    status: active\n"
        "  - slug: forever\n    status: continuous\n"
        "  - slug: shipped\n    status: finished\n",
        encoding="utf-8",
    )
    for slug in ("finite", "forever", "shipped"):
        path = projects / slug
        path.mkdir()
        (path / "roadmap.yaml").write_text(
            f"project: {slug}\nkind: software\ntasks:\n- id: t-001\n  status: {'done' if slug == 'shipped' else 'ready'}\n",
            encoding="utf-8",
        )
    monkeypatch.setattr(build_status, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(build_status, "PROJECTS_DIR", projects)
    monkeypatch.setattr(build_status, "PITCHES_DIR", tmp_path / "pitches")
    monkeypatch.setattr(build_status, "STATUS_FILE", tmp_path / "STATUS.md")
    monkeypatch.setattr(build_status, "OVERRIDES_FILE", tmp_path / "project-overrides.yaml")
    build_status.build_status()
    text = (tmp_path / "STATUS.md").read_text(encoding="utf-8")
    assert "| Active projects | 1 |" in text
    assert "| Continuous projects | 1 |" in text
    assert "| Finished projects | 1 |" in text
    assert "| forever | continuous | software |" in text
    assert "## Agent pickup hints" in text
    assert "| finite | active | — | t-001 |" in text


def test_status_splits_live_and_archival_gates_and_parses_markdown_pitch_status(
    tmp_path: Path, monkeypatch
) -> None:
    projects = tmp_path / "projects"
    pitches = tmp_path / "pitches"
    projects.mkdir()
    pitches.mkdir()
    (tmp_path / "project-overrides.yaml").write_text(
        "overrides:\n"
        "  - slug: live\n    status: active\n"
        "  - slug: forever\n    status: continuous\n"
        "  - slug: paused\n    status: paused\n"
        "  - slug: shipped\n    status: finished\n",
        encoding="utf-8",
    )
    for slug in ("live", "forever", "paused", "shipped"):
        path = projects / slug
        path.mkdir()
        (path / "roadmap.yaml").write_text(
            f"project: {slug}\nkind: software\ntasks:\n"
            "- id: t-001\n  status: needs-human\n",
            encoding="utf-8",
        )

    (pitches / "2026-08-11-approved.md").write_text(
        "# Retire old surface\n\n**Status:** approved by Silas in-session 2026-08-11\n",
        encoding="utf-8",
    )
    (pitches / "2026-09-29-pending.md").write_text(
        "# Pitch: Still pending\nstatus: awaiting-silas\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(build_status, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(build_status, "PROJECTS_DIR", projects)
    monkeypatch.setattr(build_status, "PITCHES_DIR", pitches)
    monkeypatch.setattr(build_status, "STATUS_FILE", tmp_path / "STATUS.md")
    monkeypatch.setattr(build_status, "OVERRIDES_FILE", tmp_path / "project-overrides.yaml")
    build_status.build_status()

    text = (tmp_path / "STATUS.md").read_text(encoding="utf-8")
    assert "| Needs human (all history) | 4 |" in text
    assert "| Needs human (workable projects) | 2 |" in text
    assert "| Needs human (archival projects) | 2 |" in text
    assert "| Pitches pending | 1 |" in text
    assert "Still pending" in text
    assert "Retire old surface" not in text


def test_pickup_hints_prioritize_reviews_and_filter_unclaimable_work() -> None:
    now = datetime(2026, 11, 26, 22, tzinfo=timezone.utc)
    overrides = {
        "ongoing": {"status": "continuous"},
        "finite": {"status": "active"},
        "paused": {"status": "paused"},
        "finished": {"status": "finished"},
    }
    tasks = {
        "ongoing": [{"id": "t-001", "status": "ready"}],
        "finite": [
            {"id": "t-001", "status": "review"},
            {"id": "t-002", "status": "ready", "depends_on": "t-001"},
            {"id": "t-003", "status": "ready", "rest_until": "2026-11-27T01:00:00Z"},
            {"id": "t-004", "status": "ready", "remaining_scope_task": "t-001"},
            {"id": "t-005", "status": "ready", "note": "Once per Pacific calendar day. Ran on 2026-11-26 Pacific."},
            {"id": "t-006", "status": "claimed", "claimed_at": "2026-11-26T18:00:00Z"},
            {"id": "t-007", "status": "done", "gate_human": True},
            {"id": "t-008", "status": "ready", "depends_on": "t-007"},
            *({"id": f"t-{i:03}", "status": "ready"} for i in range(9, 14)),
        ],
        "paused": [{"id": "t-001", "status": "review"}],
        "finished": [{"id": "t-001", "status": "ready"}],
    }
    assert build_status.pickup_rows(
        tasks, overrides, ["ongoing", "paused", "finite", "finished"], now=now
    ) == [
        "| finite | active | t-001 | t-009, t-010, t-011 (+2 more) |",
        "| ongoing | continuous | — | t-001 |",
    ]


def test_pickup_hints_bound_review_ids_without_hiding_count() -> None:
    rows = build_status.pickup_rows(
        {"live": [{"id": f"t-{i:03}", "status": "review"} for i in range(1, 9)]},
        {"live": {"status": "active"}},
        [],
        now=datetime(2026, 11, 26, tzinfo=timezone.utc),
    )
    assert rows == ["| live | active | t-001, t-002, t-003, t-004, t-005, t-006 (+2 more) | — |"]


def test_status_is_not_rewritten_when_only_the_stamp_would_change(tmp_path: Path, monkeypatch) -> None:
    projects = tmp_path / "projects"
    (projects / "demo").mkdir(parents=True)
    (tmp_path / "pitches").mkdir()
    (tmp_path / "project-overrides.yaml").write_text("overrides:\n  - slug: demo\n    status: active\n", encoding="utf-8")
    roadmap = projects / "demo" / "roadmap.yaml"
    roadmap.write_text("project: demo\nkind: software\ntasks:\n- id: t-001\n  status: ready\n", encoding="utf-8")
    status = tmp_path / "STATUS.md"
    for name, value in (("REPO_ROOT", tmp_path), ("PROJECTS_DIR", projects), ("PITCHES_DIR", tmp_path / "pitches"),
                        ("STATUS_FILE", status), ("OVERRIDES_FILE", tmp_path / "project-overrides.yaml")):
        monkeypatch.setattr(build_status, name, value)

    build_status.build_status()
    stale = status.read_text(encoding="utf-8").replace("<!-- Last generated: ", "<!-- Last generated: 1999-")
    status.write_text(stale, encoding="utf-8")
    build_status.build_status()
    assert status.read_text(encoding="utf-8") == stale

    roadmap.write_text("project: demo\nkind: software\ntasks:\n- id: t-001\n  status: done\n", encoding="utf-8")
    build_status.build_status()
    assert status.read_text(encoding="utf-8") != stale
