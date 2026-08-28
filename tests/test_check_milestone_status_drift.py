"""Tests for scripts/check_milestone_status_drift.py. No network, no real roadmaps."""

import textwrap

import scripts.check_milestone_status_drift as drift


def write_roadmap(root, slug, content):
    project_dir = root / "projects" / slug
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "roadmap.yaml").write_text(textwrap.dedent(content), encoding="utf-8")


def write_overrides(root, entries):
    lines = ["overrides:"]
    for slug, status in entries:
        lines.extend([f"  - slug: {slug}", f"    status: {status}"])
    (root / "project-overrides.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_not_started_with_done_work_is_flagged(tmp_path):
    write_roadmap(
        tmp_path,
        "cthulhuquarium",
        """\
        milestones:
          - id: m3
            title: "POLISH"
            status: not-started
        tasks:
          - id: t-001
            milestone: m3
            status: done
          - id: t-002
            milestone: m3
            status: ready
        """,
    )
    write_overrides(tmp_path, [("cthulhuquarium", "active")])

    result = drift.scan(
        projects_dir=tmp_path / "projects",
        overrides_path=tmp_path / "project-overrides.yaml",
    )

    assert len(result["findings"]) == 1
    finding = result["findings"][0]
    assert finding["project"] == "cthulhuquarium"
    assert finding["milestone"] == "m3"
    assert finding["shape"] == "not-started-with-done-work"
    assert finding["done_task_count"] == 1
    assert finding["total_task_count"] == 2


def test_done_with_open_non_recurring_work_is_flagged(tmp_path):
    write_roadmap(
        tmp_path,
        "alexa-integration",
        """\
        milestones:
          - id: m3
            title: "Rollout"
            status: done
        tasks:
          - id: t-001
            milestone: m3
            status: done
          - id: t-002
            milestone: m3
            status: needs-human
        """,
    )
    write_overrides(tmp_path, [("alexa-integration", "active")])

    result = drift.scan(
        projects_dir=tmp_path / "projects",
        overrides_path=tmp_path / "project-overrides.yaml",
    )

    assert len(result["findings"]) == 1
    finding = result["findings"][0]
    assert finding["shape"] == "done-with-open-work"
    assert finding["open_task_count"] == 1
    assert finding["total_task_count"] == 2


def test_recurring_tasks_dont_count_against_a_done_milestone(tmp_path):
    """Recurring tasks never reach done by design -- a milestone can legitimately
    be done while one keeps cycling under it."""
    write_roadmap(
        tmp_path,
        "animation-manager",
        """\
        milestones:
          - id: m1
            title: "Shipped"
            status: done
        tasks:
          - id: t-001
            milestone: m1
            status: done
          - id: t-002
            milestone: m1
            status: ready
            recurring: true
        """,
    )
    write_overrides(tmp_path, [("animation-manager", "active")])

    result = drift.scan(
        projects_dir=tmp_path / "projects",
        overrides_path=tmp_path / "project-overrides.yaml",
    )

    assert result["findings"] == []


def test_no_finding_when_milestone_status_matches_task_state(tmp_path):
    write_roadmap(
        tmp_path,
        "coat-dance",
        """\
        milestones:
          - id: m1
            title: "In flight"
            status: in-progress
        tasks:
          - id: t-001
            milestone: m1
            status: done
          - id: t-002
            milestone: m1
            status: ready
        """,
    )
    write_overrides(tmp_path, [("coat-dance", "active")])

    result = drift.scan(
        projects_dir=tmp_path / "projects",
        overrides_path=tmp_path / "project-overrides.yaml",
    )

    assert result["findings"] == []


def test_milestone_with_no_tasks_is_skipped(tmp_path):
    write_roadmap(
        tmp_path,
        "empty-project",
        """\
        milestones:
          - id: m1
            title: "Nothing yet"
            status: not-started
        tasks: []
        """,
    )
    write_overrides(tmp_path, [("empty-project", "active")])

    result = drift.scan(
        projects_dir=tmp_path / "projects",
        overrides_path=tmp_path / "project-overrides.yaml",
    )

    assert result["findings"] == []


def test_paused_project_excluded_by_default(tmp_path):
    write_roadmap(
        tmp_path,
        "paused-project",
        """\
        milestones:
          - id: m1
            title: "Stale"
            status: not-started
        tasks:
          - id: t-001
            milestone: m1
            status: done
        """,
    )
    write_overrides(tmp_path, [("paused-project", "paused")])

    result = drift.scan(
        projects_dir=tmp_path / "projects",
        overrides_path=tmp_path / "project-overrides.yaml",
    )
    assert result["findings"] == []

    result_inactive = drift.scan(
        projects_dir=tmp_path / "projects",
        overrides_path=tmp_path / "project-overrides.yaml",
        include_inactive=True,
    )
    assert len(result_inactive["findings"]) == 1


def test_render_reports_clean_when_no_findings():
    assert "No milestone status drift" in drift.render({"findings": []})


def test_render_names_project_milestone_and_detail():
    text = drift.render(
        {
            "findings": [
                {
                    "project": "cthulhuquarium",
                    "milestone": "m3",
                    "title": "POLISH",
                    "milestone_status": "not-started",
                    "shape": "not-started-with-done-work",
                    "done_task_count": 25,
                    "total_task_count": 31,
                    "detail": "milestone status is 'not-started' but 25/31 of its tasks are already done",
                }
            ]
        }
    )
    assert "cthulhuquarium/m3" in text
    assert "25/31" in text
