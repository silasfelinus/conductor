"""
Tests for check_hostbuf_failure.py — the hourly render-box hostbuf sentinel
(conductor/t-157). No real network calls: fetch_queue_stats is monkeypatched.

conductor/t-157: the "unverified" state used to be reported only via a
`::warning::` line in the workflow's own log, which nothing durable reads.
These tests assert the fix -- an unverified run also writes a dated entry to
RENDER-BACKLOG.md -- actually happens, not just that stdout mentions it.
"""

from pathlib import Path

import scripts.check_hostbuf_failure as sentinel


LEDGER_TEMPLATE = """# RENDER-BACKLOG.md

Some intro text.

## Log
"""


def make_ledger(tmp_path: Path) -> Path:
    ledger = tmp_path / "RENDER-BACKLOG.md"
    ledger.write_text(LEDGER_TEMPLATE, encoding="utf-8")
    return ledger


UNVERIFIED_DATA = {
    "latestHostbufFailureAt": "2026-09-10T00:00:00Z",
    "latestDoneAt": "2026-09-09T23:00:00Z",
    "recentFailed": [],
}

RECOVERED_DATA = {
    "latestHostbufFailureAt": "2026-09-10T00:00:00Z",
    "latestDoneAt": "2026-09-10T01:00:00Z",
    "recentFailed": [],
}

CLEAR_DATA = {"recentFailed": []}


def test_hostbuf_state_unverified():
    assert sentinel.hostbuf_state(UNVERIFIED_DATA) == "unverified"


def test_hostbuf_state_recovered():
    assert sentinel.hostbuf_state(RECOVERED_DATA) == "recovered"


def test_main_writes_ledger_entry_on_unverified_state(tmp_path, monkeypatch, capsys):
    ledger = make_ledger(tmp_path)
    monkeypatch.setattr(sentinel, "LEDGER_FILE", ledger)
    monkeypatch.setattr(
        sentinel, "fetch_queue_stats", lambda window_hours=2, timeout=20.0: UNVERIFIED_DATA
    )

    exit_code = sentinel.main([])
    assert exit_code == 0

    text = ledger.read_text(encoding="utf-8")
    assert "unverified" in text
    assert "UNVERIFIED render recovery" in text
    assert "2026-09-10T00:00:00Z" in text

    out = capsys.readouterr().out
    assert "::warning::UNVERIFIED render recovery" in out


def test_main_no_append_skips_ledger_write(tmp_path, monkeypatch):
    ledger = make_ledger(tmp_path)
    monkeypatch.setattr(sentinel, "LEDGER_FILE", ledger)
    monkeypatch.setattr(
        sentinel, "fetch_queue_stats", lambda window_hours=2, timeout=20.0: UNVERIFIED_DATA
    )

    exit_code = sentinel.main(["--no-append"])
    assert exit_code == 0
    assert ledger.read_text(encoding="utf-8") == LEDGER_TEMPLATE


def test_main_recovered_state_does_not_touch_ledger(tmp_path, monkeypatch):
    ledger = make_ledger(tmp_path)
    monkeypatch.setattr(sentinel, "LEDGER_FILE", ledger)
    monkeypatch.setattr(
        sentinel, "fetch_queue_stats", lambda window_hours=2, timeout=20.0: RECOVERED_DATA
    )

    exit_code = sentinel.main([])
    assert exit_code == 0
    assert ledger.read_text(encoding="utf-8") == LEDGER_TEMPLATE


def test_main_clear_state_does_not_touch_ledger(tmp_path, monkeypatch):
    ledger = make_ledger(tmp_path)
    monkeypatch.setattr(sentinel, "LEDGER_FILE", ledger)
    monkeypatch.setattr(
        sentinel, "fetch_queue_stats", lambda window_hours=2, timeout=20.0: CLEAR_DATA
    )

    exit_code = sentinel.main([])
    assert exit_code == 0
    assert ledger.read_text(encoding="utf-8") == LEDGER_TEMPLATE


def test_main_task_flag_is_recorded_in_ledger_entry(tmp_path, monkeypatch):
    ledger = make_ledger(tmp_path)
    monkeypatch.setattr(sentinel, "LEDGER_FILE", ledger)
    monkeypatch.setattr(
        sentinel, "fetch_queue_stats", lambda window_hours=2, timeout=20.0: UNVERIFIED_DATA
    )

    exit_code = sentinel.main(["--task", "kindrobots-unraid/t-021"])
    assert exit_code == 0
    text = ledger.read_text(encoding="utf-8")
    assert "| kindrobots-unraid/t-021 | unverified" in text


def test_main_fresh_failure_still_exits_2(monkeypatch):
    data = {
        "latestHostbufFailureAt": None,
        "latestDoneAt": None,
        "recentFailed": [
            {"error": "node 3 (CLIPTextEncode): hostbuf_file_reader_read failed"}
            for _ in range(5)
        ],
        "since": "2026-09-10T00:00:00Z",
    }
    monkeypatch.setattr(sentinel, "fetch_queue_stats", lambda window_hours=2, timeout=20.0: data)
    exit_code = sentinel.main([])
    assert exit_code == 2
