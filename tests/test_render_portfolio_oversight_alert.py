from pathlib import Path

from scripts.render_portfolio_oversight_alert import alert_body, alert_subject


def report_fixture():
    return {
        "summary": {"status": "action-needed"},
        "openai_scheduled_agent": {
            "overdue": True,
            "last_activity": "2026-09-10T09:34:43+00:00",
            "hours_since": 59.08,
            "stale_hours": 6.0,
            "marker": "openai-scheduled-",
        },
        "project_parity": {"forward": [], "reverse": [], "unresolved": None},
        "roadmap_audit": {"summary": {"errors": 0, "warnings": 5}, "errors": []},
        "intent_review": {"due": False, "last_report": "INTENT-AUDIT-2026-09-10.md"},
    }


def test_heartbeat_alert_explains_exact_sensor_and_threshold():
    report = report_fixture()
    subject = alert_subject(report)
    body = alert_body(report, run_url="https://github.com/example/actions/runs/123")

    assert subject == "Conductor Oversight: scheduled agent heartbeat overdue"
    assert "Why this email was sent:" in body
    assert "last visible activity was 2026-09-10T09:34:43+00:00" in body
    assert "59.08h ago; threshold 6.0h" in body
    assert "5 roadmap warnings" in body
    assert "warnings alone do not trigger this alert" in body
    assert "https://github.com/example/actions/runs/123" in body


def test_alert_lists_every_triggering_problem_not_just_the_first():
    report = report_fixture()
    report["roadmap_audit"] = {
        "summary": {"errors": 1, "warnings": 0},
        "errors": [
            {
                "code": "CONTROL_PRIORITY_DRIFT",
                "project": "_global",
                "task": None,
                "message": "priority drift",
            }
        ],
    }
    report["project_parity"] = {
        "forward": [{"conductor_slug": "missing-roadmap"}],
        "reverse": [{"conductor_slug": "missing-row"}],
        "unresolved": None,
    }

    body = alert_body(report)

    assert "CONTROL_PRIORITY_DRIFT at _global: priority drift" in body
    assert "missing-roadmap is claimed in Kind Robots but has no roadmap" in body
    assert "missing-row has a Conductor roadmap but no matching Kind Robots row" in body


def test_oversight_workflow_emails_actionable_sensor_results_instead_of_failing_on_purpose():
    workflow = (
        Path(__file__).parents[1] / ".github" / "workflows" / "conductor-oversight.yml"
    ).read_text(encoding="utf-8")

    assert "Email explained oversight action" in workflow
    assert "render_portfolio_oversight_alert.py" in workflow
    assert "send_alert_brevo.py" in workflow
    assert 'exit "${{ steps.oversight.outputs.exit_code }}"' not in workflow
    assert "Surface oversight action" not in workflow
