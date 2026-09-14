import scripts.portfolio_oversight_email_gate as gate


def report(status, *, days_since=3, stale_days=3):
    return {
        "summary": {"status": status},
        "intent_review": {
            "days_since": days_since,
            "stale_days": stale_days,
        },
    }


def test_semantic_review_due_gets_agent_grace_before_email():
    assert gate.should_email(report("semantic-review-due", days_since=3)) is False


def test_semantic_review_escalates_after_grace_day():
    assert gate.should_email(report("semantic-review-due", days_since=4)) is True


def test_deterministic_action_and_unresolved_still_email_immediately():
    assert gate.should_email(report("action-needed")) is True
    assert gate.should_email(report("unresolved")) is True


def test_clean_report_does_not_email():
    assert gate.should_email(report("clean")) is False


def test_missing_intent_baseline_is_exceptional_and_escalates():
    assert gate.should_email(report("semantic-review-due", days_since=None)) is True
