import scripts.portfolio_oversight_email_gate as gate


def report(status, *, days_since=3, stale_days=3):
    return {
        "summary": {"status": status},
        "intent_review": {
            "days_since": days_since,
            "stale_days": stale_days,
        },
    }


def test_semantic_review_due_never_emails_without_failed_attempt():
    for days in (3, 4, 10, 100):
        assert gate.should_email(report("semantic-review-due", days_since=days)) is False


def test_semantic_review_emails_only_after_explicit_failed_attempt():
    overdue = report("semantic-review-due", days_since=4)
    overdue["intent_review"]["failed_attempt"] = {
        "status": "failed",
        "attempted_at": "2026-10-10T15:00:00+00:00",
        "reason": "GitHub read timed out after two attempts",
    }
    assert gate.should_email(overdue) is True
    overdue["intent_review"]["failed_attempt"]["status"] = "running"
    assert gate.should_email(overdue) is False


def test_deterministic_action_and_unresolved_still_email_immediately():
    assert gate.should_email(report("action-needed")) is True
    assert gate.should_email(report("unresolved")) is True


def test_early_semantic_review_assignment_never_emails():
    upcoming = report("semantic-review-upcoming", days_since=2)
    upcoming["intent_review"]["upcoming"] = True
    assert gate.should_email(upcoming) is False


def test_clean_report_does_not_email():
    assert gate.should_email(report("clean")) is False


def test_missing_intent_baseline_dispatches_work_but_does_not_page():
    assert gate.should_email(report("semantic-review-due", days_since=None)) is False


def test_repeated_identical_incident_is_suppressed_within_day():
    from datetime import datetime, timezone, timedelta
    now = datetime(2026, 10, 9, 18, tzinfo=timezone.utc)
    incident = report("unresolved")
    previous = {"signature": gate.incident_signature(incident), "sent_at": (now - timedelta(hours=6)).isoformat()}
    assert gate.should_notify(incident, previous, now) is False
    assert gate.should_notify(incident, previous, now + timedelta(hours=25)) is True


def test_changed_incident_alerts_immediately():
    from datetime import datetime, timezone
    now = datetime(2026, 10, 9, 18, tzinfo=timezone.utc)
    earlier = report("unresolved")
    changed = report("unresolved")
    changed["summary"]["project_unresolved"] = "HTTP 401"
    previous = {"signature": gate.incident_signature(earlier), "sent_at": now.isoformat()}
    assert gate.should_notify(changed, previous, now) is True


def test_generated_timestamps_do_not_change_incident_signature():
    first = report("unresolved")
    second = report("unresolved")
    first["generated_at"] = "2026-10-08"
    second["generated_at"] = "2026-10-09"
    assert gate.incident_signature(first) == gate.incident_signature(second)


def test_failed_review_attempt_changes_incident_signature():
    pending = report("semantic-review-due", days_since=7)
    failed = report("semantic-review-due", days_since=7)
    failed["intent_review"]["failed_attempt"] = {
        "status": "failed", "attempted_at": "2026-10-10T15:00:00Z", "reason": "agent error",
    }
    assert gate.incident_signature(pending) != gate.incident_signature(failed)
