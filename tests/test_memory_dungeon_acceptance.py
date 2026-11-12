from scripts.check_memory_dungeon_acceptance import unresolved_done_tasks


def task(note: str, status: str = "done", task_id: str = "t-001") -> dict:
    return {"id": task_id, "status": status, "note": note}


def test_latest_remaining_requires_later_evidence() -> None:
    assert unresolved_done_tasks({"tasks": [task("2026-11-11 remaining: missing gallery")]}) == ["t-001"]
    assert unresolved_done_tasks({"tasks": [task("remaining met: old proof\nremaining: new gap")]}) == ["t-001"]


def test_later_remaining_met_clears_only_latest_gap() -> None:
    assert unresolved_done_tasks({"tasks": [task("remaining: gap\nremaining met: verified gallery URLs")]}) == []
    assert unresolved_done_tasks({"tasks": [task("remaining: first\nremaining met: first\nremaining: second")]}) == ["t-001"]


def test_ready_claimed_and_legacy_done_are_ignored() -> None:
    assert unresolved_done_tasks({"tasks": [
        task("remaining: open", "ready"),
        task("remaining: open", "claimed"),
        task("historical completion with no acceptance ledger"),
    ]}) == []


def test_quoted_remaining_in_completed_audit_is_not_a_live_gap() -> None:
    assert unresolved_done_tasks({"tasks": [task('Append a dated "remaining:" line to other tasks.')]}) == []
    assert unresolved_done_tasks({"tasks": [task("2026-11-11 PT remaining: artwork\n2026-11-12 PT remaining met: URLs checked")]}) == []
