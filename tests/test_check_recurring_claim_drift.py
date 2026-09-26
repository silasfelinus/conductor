"""Tests for scripts/check_recurring_claim_drift.py. No network, no real roadmaps."""

import sys
import textwrap

import scripts.check_recurring_claim_drift as drift


def write_roadmap(root, slug, content):
    project_dir = root / "projects" / slug
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "roadmap.yaml").write_text(textwrap.dedent(content), encoding="utf-8")


def write_overrides(root, entries):
    lines = ["overrides:"]
    for slug, status in entries:
        lines.extend([f"  - slug: {slug}", f"    status: {status}"])
    (root / "project-overrides.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _scan(tmp_path, **kwargs):
    return drift.scan(
        projects_dir=tmp_path / "projects",
        overrides_path=tmp_path / "project-overrides.yaml",
        **kwargs,
    )


def test_live_claim_is_clean(tmp_path):
    write_roadmap(
        tmp_path,
        "alpha",
        """\
        tasks:
          - id: t-001
            title: Some task
            status: claimed
            owner: worker
            claimed_by: worker-session-123
            claimed_at: '2026-09-25T23:00:00Z'
        """,
    )
    write_overrides(tmp_path, [("alpha", "active")])

    assert _scan(tmp_path) == []


def test_ready_status_is_ignored_even_with_null_claim_fields(tmp_path):
    write_roadmap(
        tmp_path,
        "alpha",
        """\
        tasks:
          - id: t-001
            title: Some task
            status: ready
            owner: null
            claimed_by: null
            claimed_at: null
        """,
    )
    write_overrides(tmp_path, [("alpha", "active")])

    assert _scan(tmp_path) == []


def test_stuck_claim_with_null_fields_is_flagged(tmp_path):
    write_roadmap(
        tmp_path,
        "alpha",
        """\
        tasks:
          - id: t-029
            title: Polish and upgrade front-end surface
            recurring: true
            status: claimed
            owner: null
            claimed_by: null
            claimed_at: null
            note: >-
              Cycle 101: no unblocked slice this cycle; re-arming to ready (recurring),
              releasing the claim.
        """,
    )
    write_overrides(tmp_path, [("alpha", "active")])

    findings = _scan(tmp_path)

    assert len(findings) == 1
    entry = findings[0]
    assert entry["project"] == "alpha"
    assert entry["task_id"] == "t-029"
    assert entry["recurring"] is True
    assert entry["note_mentions_rearm"] is True


def test_stuck_claim_missing_fields_entirely_is_flagged(tmp_path):
    write_roadmap(
        tmp_path,
        "alpha",
        """\
        tasks:
          - id: t-001
            title: Some task
            status: claimed
        """,
    )
    write_overrides(tmp_path, [("alpha", "active")])

    findings = _scan(tmp_path)

    assert len(findings) == 1
    assert findings[0]["note_mentions_rearm"] is False


def test_stuck_claim_with_only_claimed_by_set_is_not_flagged(tmp_path):
    # A partial write (claimed_by present, claimed_at absent, or vice versa) is
    # a different, narrower kind of inconsistency than the fully-null drift
    # this check targets -- only the "both null" combination is unambiguous.
    write_roadmap(
        tmp_path,
        "alpha",
        """\
        tasks:
          - id: t-001
            title: Some task
            status: claimed
            claimed_by: worker-session-123
            claimed_at: null
        """,
    )
    write_overrides(tmp_path, [("alpha", "active")])

    assert _scan(tmp_path) == []


def test_non_recurring_task_is_still_flagged(tmp_path):
    write_roadmap(
        tmp_path,
        "alpha",
        """\
        tasks:
          - id: t-050
            title: One-off task
            status: claimed
            claimed_by: null
            claimed_at: null
        """,
    )
    write_overrides(tmp_path, [("alpha", "active")])

    findings = _scan(tmp_path)

    assert len(findings) == 1
    assert findings[0]["recurring"] is False


def test_paused_project_excluded_by_default(tmp_path):
    write_roadmap(
        tmp_path,
        "alpha",
        """\
        tasks:
          - id: t-001
            title: Some task
            status: claimed
            claimed_by: null
            claimed_at: null
        """,
    )
    write_overrides(tmp_path, [("alpha", "paused")])

    assert _scan(tmp_path) == []
    assert len(_scan(tmp_path, include_inactive=True)) == 1


def test_render_clean_and_flagged():
    assert drift.render([]).startswith("No recurring-claim drift found")

    findings = [
        {
            "project": "alpha",
            "task_id": "t-029",
            "title": "Polish and upgrade front-end surface",
            "recurring": True,
            "note_mentions_rearm": True,
        }
    ]
    output = drift.render(findings)
    assert "alpha/t-029" in output
    assert "[recurring]" in output
    assert "status write did not land" in output


def test_main_exit_code_one_when_flagged(tmp_path, monkeypatch):
    write_roadmap(
        tmp_path,
        "alpha",
        """\
        tasks:
          - id: t-001
            title: Some task
            status: claimed
            claimed_by: null
            claimed_at: null
        """,
    )
    write_overrides(tmp_path, [("alpha", "active")])

    monkeypatch.setattr(drift, "PROJECTS_DIR", tmp_path / "projects")
    monkeypatch.setattr(drift, "OVERRIDES_PATH", tmp_path / "project-overrides.yaml")
    monkeypatch.setattr(sys, "argv", ["check_recurring_claim_drift.py"])

    try:
        drift.main()
    except SystemExit as exc:
        assert exc.code == 1
    else:
        raise AssertionError("main() should call sys.exit")


def test_main_exit_code_zero_when_clean(tmp_path, monkeypatch):
    write_roadmap(
        tmp_path,
        "alpha",
        """\
        tasks:
          - id: t-001
            title: Some task
            status: ready
        """,
    )
    write_overrides(tmp_path, [("alpha", "active")])

    monkeypatch.setattr(drift, "PROJECTS_DIR", tmp_path / "projects")
    monkeypatch.setattr(drift, "OVERRIDES_PATH", tmp_path / "project-overrides.yaml")
    monkeypatch.setattr(sys, "argv", ["check_recurring_claim_drift.py"])

    try:
        drift.main()
    except SystemExit as exc:
        assert exc.code == 0
    else:
        raise AssertionError("main() should call sys.exit")
