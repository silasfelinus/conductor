"""Tests for scripts/check_daily_commitment_staleness.py. No network, no real roadmaps."""

import sys
import textwrap
from datetime import datetime, timezone

import scripts.check_daily_commitment_staleness as staleness

NOW = datetime(2026, 9, 23, 12, 0, 0, tzinfo=timezone.utc)  # 2026-09-23 05:00 Pacific


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
    return staleness.scan(
        projects_dir=tmp_path / "projects",
        overrides_path=tmp_path / "project-overrides.yaml",
        now=NOW,
        **kwargs,
    )


def test_checked_today_is_clean(tmp_path):
    write_roadmap(
        tmp_path,
        "alpha",
        """\
        tasks:
          - id: t-001
            daily_commitment: true
            recurring: true
            status: ready
            daily_last_checked: '2026-09-23'
        """,
    )
    write_overrides(tmp_path, [("alpha", "active")])

    findings = _scan(tmp_path)

    assert findings == []


def test_non_daily_commitment_task_is_ignored(tmp_path):
    write_roadmap(
        tmp_path,
        "alpha",
        """\
        tasks:
          - id: t-001
            recurring: true
            status: ready
        """,
    )
    write_overrides(tmp_path, [("alpha", "active")])

    findings = _scan(tmp_path)

    assert findings == []


def test_stale_check_flagged_past_threshold(tmp_path):
    write_roadmap(
        tmp_path,
        "alpha",
        """\
        tasks:
          - id: t-007
            title: Ship one new screensaver
            daily_commitment: true
            recurring: true
            status: ready
            daily_last_checked: '2026-09-21'
        """,
    )
    write_overrides(tmp_path, [("alpha", "active")])

    findings = _scan(tmp_path)

    assert len(findings) == 1
    entry = findings[0]
    assert entry["project"] == "alpha"
    assert entry["task_id"] == "t-007"
    issue = entry["issues"][0]
    assert issue["type"] == "stale-check"
    assert issue["days_since"] == 2
    assert issue["last_checked"] == "2026-09-21"


def test_one_day_stale_is_within_default_threshold(tmp_path):
    write_roadmap(
        tmp_path,
        "alpha",
        """\
        tasks:
          - id: t-007
            daily_commitment: true
            recurring: true
            status: ready
            daily_last_checked: '2026-09-22'
        """,
    )
    write_overrides(tmp_path, [("alpha", "active")])

    findings = _scan(tmp_path)

    assert findings == []


def test_missing_daily_last_checked_is_flagged(tmp_path):
    write_roadmap(
        tmp_path,
        "alpha",
        """\
        tasks:
          - id: t-007
            daily_commitment: true
            recurring: true
            status: ready
        """,
    )
    write_overrides(tmp_path, [("alpha", "active")])

    findings = _scan(tmp_path)

    assert len(findings) == 1
    issue = findings[0]["issues"][0]
    assert issue["type"] == "stale-check"
    assert issue["last_checked"] is None


def test_stalled_claim_is_flagged(tmp_path):
    write_roadmap(
        tmp_path,
        "alpha",
        """\
        tasks:
          - id: t-007
            daily_commitment: true
            recurring: true
            status: claimed
            daily_last_checked: '2026-09-23'
            claimed_at: '2026-09-23T08:00:00Z'
        """,
    )
    write_overrides(tmp_path, [("alpha", "active")])

    findings = _scan(tmp_path)

    assert len(findings) == 1
    issue = findings[0]["issues"][0]
    assert issue["type"] == "stalled-claim"
    assert issue["minutes_since"] == 240
    assert issue["ttl_minutes"] == staleness.CLAIM_TTL_MINUTES


def test_fresh_claim_is_not_a_stalled_claim(tmp_path):
    write_roadmap(
        tmp_path,
        "alpha",
        """\
        tasks:
          - id: t-007
            daily_commitment: true
            recurring: true
            status: claimed
            daily_last_checked: '2026-09-23'
            claimed_at: '2026-09-23T11:30:00Z'
        """,
    )
    write_overrides(tmp_path, [("alpha", "active")])

    findings = _scan(tmp_path)

    assert findings == []


def test_both_issues_can_fire_on_the_same_task(tmp_path):
    write_roadmap(
        tmp_path,
        "alpha",
        """\
        tasks:
          - id: t-007
            daily_commitment: true
            recurring: true
            status: claimed
            daily_last_checked: '2026-09-20'
            claimed_at: '2026-09-23T08:00:00Z'
        """,
    )
    write_overrides(tmp_path, [("alpha", "active")])

    findings = _scan(tmp_path)

    assert len(findings) == 1
    types = {issue["type"] for issue in findings[0]["issues"]}
    assert types == {"stale-check", "stalled-claim"}


def test_paused_project_excluded_by_default(tmp_path):
    write_roadmap(
        tmp_path,
        "alpha",
        """\
        tasks:
          - id: t-007
            daily_commitment: true
            recurring: true
            status: ready
            daily_last_checked: '2026-09-10'
        """,
    )
    write_overrides(tmp_path, [("alpha", "paused")])

    findings = _scan(tmp_path)
    assert findings == []

    findings_all = _scan(tmp_path, include_inactive=True)
    assert len(findings_all) == 1


def test_custom_stale_days_threshold(tmp_path):
    write_roadmap(
        tmp_path,
        "alpha",
        """\
        tasks:
          - id: t-007
            daily_commitment: true
            recurring: true
            status: ready
            daily_last_checked: '2026-09-21'
        """,
    )
    write_overrides(tmp_path, [("alpha", "active")])

    # 2 days stale, default threshold (2) flags it...
    assert len(_scan(tmp_path)) == 1
    # ...but a looser threshold does not.
    assert _scan(tmp_path, stale_days=3) == []


def test_render_clean_and_flagged():
    assert staleness.render([]).startswith("No daily_commitment task staleness found")

    findings = [
        {
            "project": "alpha",
            "task_id": "t-007",
            "title": "Ship one new screensaver",
            "status": "ready",
            "issues": [
                {"type": "stale-check", "days_since": 3, "last_checked": "2026-09-20"}
            ],
        }
    ]
    output = staleness.render(findings)
    assert "alpha/t-007" in output
    assert "STALE CHECK" in output


def test_main_exit_code_one_when_flagged(tmp_path, monkeypatch):
    write_roadmap(
        tmp_path,
        "alpha",
        """\
        tasks:
          - id: t-007
            daily_commitment: true
            recurring: true
            status: ready
            daily_last_checked: '2020-01-01'
        """,
    )
    write_overrides(tmp_path, [("alpha", "active")])

    monkeypatch.setattr(staleness, "PROJECTS_DIR", tmp_path / "projects")
    monkeypatch.setattr(staleness, "OVERRIDES_PATH", tmp_path / "project-overrides.yaml")
    monkeypatch.setattr(sys, "argv", ["check_daily_commitment_staleness.py"])

    try:
        staleness.main()
    except SystemExit as exc:
        assert exc.code == 1
    else:
        raise AssertionError("main() should call sys.exit")


def test_main_exit_code_zero_when_clean(tmp_path, monkeypatch):
    # daily_last_checked must be computed relative to the real wall clock, not
    # hardcoded: main() calls scan() with no `now` override, so it always reads
    # real current time. A fixed past date drifts into "stale" as days pass --
    # this test failed for real on 2026-09-25 for exactly that reason with a
    # '2026-09-23' literal here.
    today = staleness.today_pacific().isoformat()
    write_roadmap(
        tmp_path,
        "alpha",
        f"""\
        tasks:
          - id: t-007
            daily_commitment: true
            recurring: true
            status: ready
            daily_last_checked: '{today}'
        """,
    )
    write_overrides(tmp_path, [("alpha", "active")])

    monkeypatch.setattr(staleness, "PROJECTS_DIR", tmp_path / "projects")
    monkeypatch.setattr(staleness, "OVERRIDES_PATH", tmp_path / "project-overrides.yaml")
    monkeypatch.setattr(sys, "argv", ["check_daily_commitment_staleness.py"])

    try:
        staleness.main()
    except SystemExit as exc:
        assert exc.code == 0
    else:
        raise AssertionError("main() should call sys.exit")
