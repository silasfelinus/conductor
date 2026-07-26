"""
Tests for recheck_render_queue.py — the shared render-queue-backlog recheck
ledger tool (conductor/t-081). No real network calls: fetch_queue_stats is
monkeypatched or urlopen is monkeypatched at the urllib layer.
"""

import json
from pathlib import Path

import pytest

import scripts.recheck_render_queue as recheck


LEDGER_TEMPLATE = """# RENDER-BACKLOG.md

Some intro text.

## Log
"""


def make_ledger(tmp_path: Path) -> Path:
    ledger = tmp_path / "RENDER-BACKLOG.md"
    ledger.write_text(LEDGER_TEMPLATE, encoding="utf-8")
    return ledger


SAMPLE_DATA = {
    "windowHours": 24,
    "queueDepth": {"PENDING": 135, "RUNNING": 1, "DONE": 1546, "FAILED": 62},
    "windowThroughput": {"PENDING": 133, "RUNNING": 1, "DONE": 37, "FAILED": 43},
    "oldestPending": {"id": 2017, "ageSeconds": 191547, "engine": "COMFY"},
    "recentFailed": [
        {"error": "ComfyUI reported a workflow error"},
        {"error": "ComfyUI reported a workflow error"},
        {
            "error": (
                "ComfyUI POST /prompt failed at http://127.0.0.1:8188 "
                "(<urlopen error [WinError 10061] ... actively refused it>)."
            )
        },
    ],
}


def test_classify_growing():
    assert recheck.classify({"PENDING": 10}, {"DONE": 5, "PENDING": 20}) == "growing"


def test_classify_draining():
    assert recheck.classify({"PENDING": 10}, {"DONE": 50, "PENDING": 5}) == "draining"


def test_classify_healthy_when_no_pending():
    assert recheck.classify({"PENDING": 0}, {"DONE": 5, "PENDING": 0}) == "healthy"


def test_summarize_failures_groups_by_signature():
    summary = recheck.summarize_failures(SAMPLE_DATA["recentFailed"])
    assert "2/3 = generic workflow error" in summary
    assert "1/3 = connection-refused to ComfyUI" in summary


def test_summarize_failures_empty():
    assert recheck.summarize_failures([]) == "recentFailed: none"


def test_format_entry_growing():
    status_label, detail = recheck.format_entry(SAMPLE_DATA, "ai-art-academy/t-004")
    assert status_label == "growing"
    assert "PENDING=135" in detail
    assert "oldestPending: id=2017" in detail
    assert "~53.2h" in detail
    assert "generic workflow error" in detail


def test_format_entry_no_oldest_pending():
    data = {
        "windowHours": 24,
        "queueDepth": {"PENDING": 0},
        "windowThroughput": {"PENDING": 0, "DONE": 3},
        "oldestPending": None,
        "recentFailed": [],
    }
    status_label, detail = recheck.format_entry(data, None)
    assert status_label == "healthy"
    assert "oldestPending: none." in detail


def test_append_entry_writes_stamped_section(tmp_path):
    ledger = make_ledger(tmp_path)
    recheck.append_entry("conductor/t-081", "growing", "some detail", ledger_path=ledger)
    text = ledger.read_text(encoding="utf-8")
    assert "| conductor/t-081 | growing" in text
    assert "some detail" in text
    assert text.startswith("# RENDER-BACKLOG.md")


def test_append_entry_no_task(tmp_path):
    ledger = make_ledger(tmp_path)
    recheck.append_entry(None, "draining", "detail here", ledger_path=ledger)
    text = ledger.read_text(encoding="utf-8")
    assert "| draining\ndetail here" in text


def test_append_entry_is_additive_never_touches_prior_lines(tmp_path):
    ledger = make_ledger(tmp_path)
    recheck.append_entry("a/t-1", "growing", "x", ledger_path=ledger)
    first_snapshot = ledger.read_text(encoding="utf-8")
    recheck.append_entry("b/t-2", "draining", "y", ledger_path=ledger)
    second_snapshot = ledger.read_text(encoding="utf-8")
    assert second_snapshot.startswith(first_snapshot.rstrip("\n"))
    assert "a/t-1" in second_snapshot
    assert "b/t-2" in second_snapshot


def test_append_entry_missing_file_raises(tmp_path):
    missing = tmp_path / "does-not-exist.md"
    with pytest.raises(SystemExit):
        recheck.append_entry(None, "growing", "x", ledger_path=missing)


def test_append_entry_missing_log_marker_raises(tmp_path):
    ledger = tmp_path / "RENDER-BACKLOG.md"
    ledger.write_text("# RENDER-BACKLOG.md\n\nNo log section here.\n", encoding="utf-8")
    with pytest.raises(SystemExit):
        recheck.append_entry(None, "growing", "x", ledger_path=ledger)


def test_fetch_queue_stats_requires_token(monkeypatch):
    monkeypatch.setattr(recheck, "KR_API_TOKEN", "")
    with pytest.raises(RuntimeError, match="KR_API_TOKEN"):
        recheck.fetch_queue_stats()


def test_fetch_queue_stats_returns_data(monkeypatch):
    monkeypatch.setattr(recheck, "KR_API_TOKEN", "fake-token")

    class FakeResp:
        def read(self):
            return json.dumps({"success": True, "data": SAMPLE_DATA}).encode()

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    monkeypatch.setattr(recheck.urllib.request, "urlopen", lambda req, timeout=None: FakeResp())
    data = recheck.fetch_queue_stats()
    assert data == SAMPLE_DATA


def test_fetch_queue_stats_raises_on_unsuccessful_payload(monkeypatch):
    monkeypatch.setattr(recheck, "KR_API_TOKEN", "fake-token")

    class FakeResp:
        def read(self):
            return json.dumps({"success": False, "message": "nope"}).encode()

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    monkeypatch.setattr(recheck.urllib.request, "urlopen", lambda req, timeout=None: FakeResp())
    with pytest.raises(RuntimeError, match="unsuccessful payload"):
        recheck.fetch_queue_stats()


def test_fetch_queue_stats_raises_on_http_error(monkeypatch):
    monkeypatch.setattr(recheck, "KR_API_TOKEN", "fake-token")

    def raise_http_error(req, timeout=None):
        raise recheck.urllib.error.HTTPError(req.full_url, 403, "Forbidden", {}, None)

    monkeypatch.setattr(recheck.urllib.request, "urlopen", raise_http_error)
    with pytest.raises(RuntimeError, match="HTTP 403"):
        recheck.fetch_queue_stats()


def test_main_dry_run_does_not_write(tmp_path, monkeypatch, capsys):
    ledger = make_ledger(tmp_path)
    monkeypatch.setattr(recheck, "LEDGER_FILE", ledger)
    monkeypatch.setattr(recheck, "fetch_queue_stats", lambda window_hours=24, timeout=20.0: SAMPLE_DATA)

    exit_code = recheck.main(["--no-append"])
    assert exit_code == 0
    assert ledger.read_text(encoding="utf-8") == LEDGER_TEMPLATE


def test_main_appends_using_default_ledger_file(tmp_path, monkeypatch):
    ledger = make_ledger(tmp_path)
    monkeypatch.setattr(recheck, "LEDGER_FILE", ledger)
    monkeypatch.setattr(recheck, "fetch_queue_stats", lambda window_hours=24, timeout=20.0: SAMPLE_DATA)

    exit_code = recheck.main(["--task", "conductor/t-081"])
    assert exit_code == 0
    text = ledger.read_text(encoding="utf-8")
    assert "| conductor/t-081 | growing" in text


def test_main_prints_error_and_returns_1_on_failure(tmp_path, monkeypatch, capsys):
    ledger = make_ledger(tmp_path)
    monkeypatch.setattr(recheck, "LEDGER_FILE", ledger)

    def raise_error(window_hours=24, timeout=20.0):
        raise RuntimeError("KR_API_TOKEN is required to query the render queue.")

    monkeypatch.setattr(recheck, "fetch_queue_stats", raise_error)

    exit_code = recheck.main([])
    assert exit_code == 1
    err = capsys.readouterr().err
    assert "KR_API_TOKEN" in err
    assert ledger.read_text(encoding="utf-8") == LEDGER_TEMPLATE
