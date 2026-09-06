from datetime import date, datetime, timezone

import scripts.build_portfolio_oversight as oversight


def test_intent_review_due_when_never_run(tmp_path):
    result = oversight.intent_review_status(directory=tmp_path, stale_days=3, today=date(2026, 8, 28))
    assert result["due"] is True
    assert result["last_report"] is None


def test_intent_review_uses_newest_dated_report(tmp_path):
    (tmp_path / "INTENT-AUDIT-2026-08-20.md").write_text("old", encoding="utf-8")
    (tmp_path / "INTENT-AUDIT-2026-08-27.md").write_text("new", encoding="utf-8")
    (tmp_path / "INTENT-AUDIT-not-a-date.md").write_text("ignore", encoding="utf-8")

    result = oversight.intent_review_status(directory=tmp_path, stale_days=3, today=date(2026, 8, 28))

    assert result["due"] is False
    assert result["last_report"] == "INTENT-AUDIT-2026-08-27.md"
    assert result["days_since"] == 1


def test_intent_review_becomes_due_at_threshold(tmp_path):
    (tmp_path / "INTENT-AUDIT-2026-08-25.md").write_text("x", encoding="utf-8")
    result = oversight.intent_review_status(directory=tmp_path, stale_days=3, today=date(2026, 8, 28))
    assert result["due"] is True
    assert result["days_since"] == 3


def test_scheduled_agent_heartbeat_fresh_and_overdue():
    now = datetime(2026, 8, 29, 3, 30, tzinfo=timezone.utc)

    fresh = oversight.scheduled_agent_status(
        stale_hours=6,
        now=now,
        log_output="2026-08-29T02:30:00+00:00",
    )
    overdue = oversight.scheduled_agent_status(
        stale_hours=6,
        now=now,
        log_output="2026-08-28T20:00:00+00:00",
    )

    assert fresh["overdue"] is False
    assert fresh["hours_since"] == 1.0
    assert fresh["marker"] == "openai-scheduled-"
    assert overdue["overdue"] is True
    assert overdue["hours_since"] == 7.5


def test_missing_scheduled_agent_heartbeat_is_overdue_and_provider_specific():
    result = oversight.scheduled_agent_status(
        stale_hours=6,
        now=datetime(2026, 8, 29, 3, 30, tzinfo=timezone.utc),
        log_output="",
    )
    assert result["overdue"] is True
    assert result["last_activity"] is None
    assert "Claude activity does not satisfy" in result["note"]


def test_classify_deterministic_drift_beats_semantic_due_and_unresolved():
    result = oversight.classify_report(
        roadmap_report={"summary": {"errors": 2, "warnings": 4}},
        project_scan={"forward": [], "reverse": []},
        project_unresolved="api unavailable",
        heartbeat={"overdue": False},
        intent={"due": True},
    )
    assert result["status"] == "action-needed"
    assert result["roadmap_errors"] == 2


def test_classify_reverse_orphan_is_actionable():
    result = oversight.classify_report(
        roadmap_report={"summary": {"errors": 0, "warnings": 0}},
        project_scan={"forward": [], "reverse": [{"conductor_slug": "example"}]},
        project_unresolved=None,
        heartbeat={"overdue": False},
        intent={"due": False},
    )
    assert result["status"] == "action-needed"
    assert result["project_reverse_orphans"] == 1


def test_classify_unresolved_parity_is_not_clean():
    result = oversight.classify_report(
        roadmap_report={"summary": {"errors": 0, "warnings": 0}},
        project_scan=None,
        project_unresolved="KR_API_TOKEN not set",
        heartbeat={"overdue": False},
        intent={"due": False},
    )
    assert result["status"] == "unresolved"


def test_classify_warnings_alone_are_clean():
    result = oversight.classify_report(
        roadmap_report={"summary": {"errors": 0, "warnings": 9}},
        project_scan={"forward": [], "reverse": []},
        project_unresolved=None,
        heartbeat={"overdue": False},
        intent={"due": False},
    )
    assert result["status"] == "clean"
    assert result["roadmap_errors"] == 0
    assert result["roadmap_warnings"] == 9


def test_classify_semantic_review_due_after_mechanical_checks_are_clean():
    result = oversight.classify_report(
        roadmap_report={"summary": {"errors": 0, "warnings": 7}},
        project_scan={"forward": [], "reverse": []},
        project_unresolved=None,
        heartbeat={"overdue": False},
        intent={"due": True},
    )
    assert result["status"] == "semantic-review-due"


def test_render_markdown_surfaces_role_signals():
    report = {
        "generated_at": "2026-08-29T03:30:00+00:00",
        "summary": {"status": "action-needed"},
        "openai_scheduled_agent": {
            "last_activity": "2026-08-29T02:30:00+00:00",
            "hours_since": 1.0,
            "stale_hours": 6,
            "overdue": False,
            "marker": "openai-scheduled-",
            "note": "OpenAI heartbeat only",
        },
        "intent_review": {
            "last_report": None,
            "days_since": None,
            "stale_days": 3,
            "due": True,
        },
        "project_parity": {
            "forward": [{"conductor_slug": "foo", "kr_project_id": 1, "kr_title": "Foo"}],
            "reverse": [],
            "unresolved": None,
        },
        "roadmap_audit": {
            "summary": {"errors": 1, "warnings": 2},
            "errors": [
                {
                    "severity": "error",
                    "code": "CONTROL_PRIORITY_DRIFT",
                    "project": "_global",
                    "task": None,
                    "message": "priority drift",
                }
            ],
            "warnings": [{"severity": "warning"}],
        },
    }

    text = oversight.render_markdown(report)

    assert "OpenAI scheduled-agent heartbeat" in text
    assert "CONTROL_PRIORITY_DRIFT" in text
    assert "Forward drift" in text
    assert "INTENT-AUDIT" in text
    assert "OVERSIGHT-AGENT.md" in text
