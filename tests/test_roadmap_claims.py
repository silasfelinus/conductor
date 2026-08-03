from datetime import datetime, timedelta, timezone

import scripts.roadmap_claims as rc


def minutes_ago(minutes: float, *, now: datetime) -> str:
    return (now - timedelta(minutes=minutes)).strftime("%Y-%m-%dT%H:%M:%SZ")


def test_ready_task_is_claimable():
    assert rc.task_is_claimable({"status": "ready"}) is True


def test_terminal_statuses_are_not_claimable():
    for status in ("done", "review", "needs-human", "blocked", "waiting", "challenged"):
        assert rc.task_is_claimable({"status": status}) is False


def test_fresh_claim_is_not_claimable():
    now = datetime.now(timezone.utc)
    task = {"status": "claimed", "claimed_at": minutes_ago(5, now=now)}
    assert rc.task_is_claimable(task, now=now) is False


def test_claim_exactly_at_ttl_boundary_is_not_stale():
    now = datetime.now(timezone.utc)
    task = {"status": "claimed", "claimed_at": minutes_ago(rc.CLAIM_TTL_MINUTES - 1, now=now)}
    assert rc.task_is_claimable(task, now=now) is False


def test_stale_claim_past_ttl_is_claimable_again():
    now = datetime.now(timezone.utc)
    task = {"status": "claimed", "claimed_at": minutes_ago(rc.CLAIM_TTL_MINUTES + 1, now=now)}
    assert rc.task_is_claimable(task, now=now) is True


def test_claim_with_missing_claimed_at_is_treated_as_stale():
    # A hand-edited or pre-mechanism `status: claimed` task carries no fresh signal --
    # it must not be able to lock a task forever.
    assert rc.task_is_claimable({"status": "claimed"}) is True


def test_claim_with_unparseable_claimed_at_is_treated_as_stale():
    assert rc.task_is_claimable({"status": "claimed", "claimed_at": "not-a-timestamp"}) is True


def test_parse_timestamp_accepts_quoted_and_zulu_forms():
    now = rc.parse_timestamp("'2026-07-14T15:00:00Z'")
    assert now is not None
    assert now.year == 2026 and now.month == 7 and now.day == 14


def test_remaining_scope_delegate_open_when_delegate_not_done():
    task = {"status": "ready", "remaining_scope_task": "t-058"}
    tasks_by_id = {"t-058": {"status": "ready"}}
    assert rc.remaining_scope_delegate_open(task, tasks_by_id) is True


def test_remaining_scope_delegate_closed_when_delegate_done():
    task = {"status": "ready", "remaining_scope_task": "t-058"}
    tasks_by_id = {"t-058": {"status": "done"}}
    assert rc.remaining_scope_delegate_open(task, tasks_by_id) is False


def test_remaining_scope_delegate_open_false_with_no_field():
    assert rc.remaining_scope_delegate_open({"status": "ready"}, {}) is False


def test_remaining_scope_delegate_open_false_for_unknown_delegate():
    task = {"status": "ready", "remaining_scope_task": "t-999"}
    assert rc.remaining_scope_delegate_open(task, {}) is False


def test_task_is_claimable_blocked_by_open_delegate():
    task = {"status": "ready", "remaining_scope_task": "t-058"}
    tasks_by_id = {"t-058": {"status": "ready"}}
    assert rc.task_is_claimable(task, tasks_by_id=tasks_by_id) is False


def test_task_is_claimable_allowed_once_delegate_done():
    task = {"status": "ready", "remaining_scope_task": "t-058"}
    tasks_by_id = {"t-058": {"status": "done"}}
    assert rc.task_is_claimable(task, tasks_by_id=tasks_by_id) is True


def test_task_is_claimable_ignores_delegate_field_without_tasks_by_id():
    # Backward compatible: a caller not yet updated to pass tasks_by_id keeps old behavior.
    task = {"status": "ready", "remaining_scope_task": "t-058"}
    assert rc.task_is_claimable(task) is True
