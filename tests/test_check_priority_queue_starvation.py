"""Tests for scripts/check_priority_queue_starvation.py. No network, no real roadmaps."""

import sys
import textwrap
from datetime import datetime, timezone

import scripts.check_priority_queue_starvation as starve


def write_roadmap(root, slug, content):
    project_dir = root / "projects" / slug
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "roadmap.yaml").write_text(textwrap.dedent(content), encoding="utf-8")


def write_priority(root, order):
    lines = ["order:"] + [f"  - {slug}" for slug in order]
    (root / "projects" / "priority.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_overrides(root, entries):
    lines = ["overrides:"]
    for slug, status in entries:
        lines.extend([f"  - slug: {slug}", f"    status: {status}"])
    (root / "project-overrides.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")


NOW = datetime(2026, 9, 12, 12, 0, 0, tzinfo=timezone.utc)


def _scan(tmp_path):
    return starve.scan(
        projects_dir=tmp_path / "projects",
        priority_path=tmp_path / "projects" / "priority.yaml",
        overrides_path=tmp_path / "project-overrides.yaml",
        now=NOW,
    )


def test_landing_at_rank_one_is_clean(tmp_path):
    write_roadmap(
        tmp_path,
        "alpha",
        """\
        tasks:
          - id: t-001
            status: ready
        """,
    )
    write_priority(tmp_path, ["alpha"])
    write_overrides(tmp_path, [("alpha", "active")])

    result = _scan(tmp_path)

    assert result["landing"] == {"project": "alpha", "rank": 1}
    assert result["skipped"] == []
    assert starve.render(result, threshold=3).startswith("Priority queue holds")


def test_needs_human_project_is_skipped_and_named(tmp_path):
    write_roadmap(
        tmp_path,
        "alpha",
        """\
        tasks:
          - id: t-001
            title: "GATE: go live with real billing"
            status: needs-human
        """,
    )
    write_roadmap(
        tmp_path,
        "beta",
        """\
        tasks:
          - id: t-001
            status: ready
        """,
    )
    write_priority(tmp_path, ["alpha", "beta"])
    write_overrides(tmp_path, [("alpha", "active"), ("beta", "active")])

    result = _scan(tmp_path)

    assert result["landing"] == {"project": "beta", "rank": 2}
    assert len(result["skipped"]) == 1
    skip = result["skipped"][0]
    assert skip["project"] == "alpha"
    assert skip["reason"] == "gated-at-needs-human"
    assert skip["evidence"] == [{"task_id": "t-001", "title": "GATE: go live with real billing"}]


def test_all_waiting_blocked_project_is_flagged(tmp_path):
    write_roadmap(
        tmp_path,
        "alpha",
        """\
        tasks:
          - id: t-001
            status: waiting
            depends_on: t-000
          - id: t-000
            status: ready
        """,
    )
    write_roadmap(
        tmp_path,
        "beta",
        """\
        tasks:
          - id: t-001
            status: ready
        """,
    )
    write_priority(tmp_path, ["alpha", "beta"])
    write_overrides(tmp_path, [("alpha", "active"), ("beta", "active")])

    result = _scan(tmp_path)

    # alpha actually HAS a claimable task (t-000 is ready), so it should land there,
    # not be skipped -- this proves the scan doesn't misclassify a project that has
    # a genuinely ready task alongside an unrelated waiting one.
    assert result["landing"] == {"project": "alpha", "rank": 1}


def test_all_waiting_blocked_with_no_ready_sibling(tmp_path):
    write_roadmap(
        tmp_path,
        "alpha",
        """\
        tasks:
          - id: t-001
            status: waiting
            depends_on: t-000
          - id: t-000
            status: claimed
            claimed_at: '2026-09-12T11:50:00Z'
        """,
    )
    write_roadmap(
        tmp_path,
        "beta",
        """\
        tasks:
          - id: t-001
            status: ready
        """,
    )
    write_priority(tmp_path, ["alpha", "beta"])
    write_overrides(tmp_path, [("alpha", "active"), ("beta", "active")])

    result = _scan(tmp_path)

    assert result["landing"] == {"project": "beta", "rank": 2}
    skip = result["skipped"][0]
    assert skip["project"] == "alpha"
    # t-001 is genuinely waiting on an unmet dependency, which outranks "all
    # claimed" in the classifier's precedence (a structural dependency block is
    # more informative than "someone's in-progress on something else here") --
    # needs-human would outrank both if present.
    assert skip["reason"] == "all-waiting-blocked"


def test_all_claimed_project_is_flagged(tmp_path):
    write_roadmap(
        tmp_path,
        "alpha",
        """\
        tasks:
          - id: t-001
            status: claimed
            claimed_at: '2026-09-12T11:55:00Z'
        """,
    )
    write_roadmap(
        tmp_path,
        "beta",
        """\
        tasks:
          - id: t-001
            status: ready
        """,
    )
    write_priority(tmp_path, ["alpha", "beta"])
    write_overrides(tmp_path, [("alpha", "active"), ("beta", "active")])

    result = _scan(tmp_path)

    assert result["landing"] == {"project": "beta", "rank": 2}
    skip = result["skipped"][0]
    assert skip["reason"] == "all-claimed"


def test_stale_claim_is_claimable_not_starved(tmp_path):
    write_roadmap(
        tmp_path,
        "alpha",
        """\
        tasks:
          - id: t-001
            status: claimed
            claimed_at: '2026-09-12T09:00:00Z'
        """,
    )
    write_priority(tmp_path, ["alpha"])
    write_overrides(tmp_path, [("alpha", "active")])

    result = _scan(tmp_path)

    # claimed_at is 3 hours before NOW, past the 90-minute TTL -- this is an
    # abandoned claim and should be pickable again, same as next_ready_task.py.
    assert result["landing"] == {"project": "alpha", "rank": 1}


def test_all_done_project_is_flagged(tmp_path):
    write_roadmap(
        tmp_path,
        "alpha",
        """\
        tasks:
          - id: t-001
            status: done
        """,
    )
    write_roadmap(
        tmp_path,
        "beta",
        """\
        tasks:
          - id: t-001
            status: ready
        """,
    )
    write_priority(tmp_path, ["alpha", "beta"])
    write_overrides(tmp_path, [("alpha", "active"), ("beta", "active")])

    result = _scan(tmp_path)

    assert result["landing"] == {"project": "beta", "rank": 2}
    skip = result["skipped"][0]
    assert skip["reason"] == "all-done"
    assert skip["evidence"] == []


def test_paused_project_does_not_count_toward_rank(tmp_path):
    write_roadmap(
        tmp_path,
        "alpha",
        """\
        tasks:
          - id: t-001
            status: needs-human
        """,
    )
    write_roadmap(
        tmp_path,
        "beta",
        """\
        tasks:
          - id: t-001
            status: ready
        """,
    )
    write_priority(tmp_path, ["alpha", "beta"])
    write_overrides(tmp_path, [("alpha", "paused"), ("beta", "active")])

    result = _scan(tmp_path)

    # alpha is paused, so ordered_workable_slugs excludes it entirely -- beta
    # lands at rank 1, not rank 2.
    assert result["landing"] == {"project": "beta", "rank": 1}
    assert result["skipped"] == []


def test_no_claimable_work_anywhere_reports_no_landing(tmp_path):
    write_roadmap(
        tmp_path,
        "alpha",
        """\
        tasks:
          - id: t-001
            status: needs-human
        """,
    )
    write_priority(tmp_path, ["alpha"])
    write_overrides(tmp_path, [("alpha", "active")])

    result = _scan(tmp_path)

    assert result["landing"] is None
    assert len(result["skipped"]) == 1
    output = starve.render(result, threshold=3)
    assert "NO project" in output


def test_threshold_keeps_shallow_fallthrough_quiet():
    result = {
        "order_depth": 2,
        "skipped": [{"project": "alpha", "rank": 1, "reason": "all-done", "evidence": []}],
        "landing": {"project": "beta", "rank": 2},
    }
    output = starve.render(result, threshold=3)
    assert output.startswith("Priority queue holds")


def test_threshold_flags_deep_fallthrough():
    result = {
        "order_depth": 5,
        "skipped": [
            {"project": p, "rank": i + 1, "reason": "all-done", "evidence": []}
            for i, p in enumerate(["a", "b", "c", "d"])
        ],
        "landing": {"project": "e", "rank": 5},
    }
    output = starve.render(result, threshold=3)
    assert "starvation" in output.lower()
    assert "rank 5" in output


def test_main_exit_code_zero_within_threshold(tmp_path, monkeypatch):
    write_roadmap(tmp_path, "alpha", "tasks:\n  - id: t-001\n    status: ready\n")
    write_priority(tmp_path, ["alpha"])
    write_overrides(tmp_path, [("alpha", "active")])

    monkeypatch.setattr(starve, "PROJECTS_DIR", tmp_path / "projects")
    monkeypatch.setattr(starve, "PRIORITY_FILE", tmp_path / "projects" / "priority.yaml")
    monkeypatch.setattr(starve, "OVERRIDES_FILE", tmp_path / "project-overrides.yaml")
    monkeypatch.setattr(sys, "argv", ["check_priority_queue_starvation.py"])

    try:
        starve.main()
    except SystemExit as exc:
        assert exc.code == 0
    else:
        raise AssertionError("main() should call sys.exit")
