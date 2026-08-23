from datetime import datetime, timezone

import scripts.daily_gate as dg


def test_is_daily_gated_true_for_pacific_contract_note():
    note = "DAILY/PROGRESS-GATED CONTRACT (Silas, 2026-08-03): ... At most once per Pacific calendar day ..."
    assert dg.is_daily_gated(note) is True


def test_is_daily_gated_false_for_ordinary_note():
    assert dg.is_daily_gated("Just a normal recurring task note.") is False


def test_is_daily_gated_false_for_missing_or_non_string_note():
    assert dg.is_daily_gated(None) is False
    assert dg.is_daily_gated(123) is False


def test_dates_recorded_in_note_finds_verified_no_op_entries():
    note = (
        "Verified no-op on 2026-08-19 Pacific: the watched manuscript blob is unchanged.\n"
        "Verified no-op on 2026-08-20 Pacific: still unchanged."
    )
    assert dg.dates_recorded_in_note(note) == {"2026-08-19", "2026-08-20"}


def test_dates_recorded_in_note_ignores_dates_not_near_pacific():
    note = "Merged PR #1673 on 2026-08-04 for manuscript blob abc123. Unrelated date here."
    assert dg.dates_recorded_in_note(note) == set()


def test_dates_recorded_in_note_empty_for_non_string():
    assert dg.dates_recorded_in_note(None) == set()


def test_today_pacific_converts_from_utc_across_date_boundary():
    # 2026-08-24 02:00 UTC is still 2026-08-23 evening in Pacific (UTC-7 in August, PDT).
    now = datetime(2026, 8, 24, 2, 0, 0, tzinfo=timezone.utc)
    assert dg.today_pacific(now=now) == "2026-08-23"


def test_already_recorded_today_true_when_gated_and_dated_entry_matches():
    now = datetime(2026, 8, 23, 15, 0, 0, tzinfo=timezone.utc)  # 2026-08-23 08:00 PDT
    task = {
        "note": (
            "DAILY/PROGRESS-GATED CONTRACT: at most once per Pacific calendar day.\n"
            "Verified no-op on 2026-08-23 Pacific: unchanged."
        )
    }
    assert dg.already_recorded_today(task, now=now) is True


def test_already_recorded_today_false_when_gated_but_not_yet_touched_today():
    now = datetime(2026, 8, 23, 15, 0, 0, tzinfo=timezone.utc)
    task = {
        "note": (
            "DAILY/PROGRESS-GATED CONTRACT: at most once per Pacific calendar day.\n"
            "Verified no-op on 2026-08-22 Pacific: unchanged."
        )
    }
    assert dg.already_recorded_today(task, now=now) is False


def test_already_recorded_today_false_when_not_daily_gated_at_all():
    now = datetime(2026, 8, 23, 15, 0, 0, tzinfo=timezone.utc)
    task = {"note": "Ordinary recurring task, worked on 2026-08-23 Pacific for unrelated reasons."}
    assert dg.already_recorded_today(task, now=now) is False


def test_already_recorded_today_false_for_missing_note():
    assert dg.already_recorded_today({}) is False
