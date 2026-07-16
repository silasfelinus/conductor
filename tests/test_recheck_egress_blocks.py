"""
Tests for recheck_egress_blocks.py — the shared egress-recheck ledger tool
(conductor/t-052). No real network calls: probe_host is monkeypatched.
"""

from pathlib import Path

import pytest

import scripts.recheck_egress_blocks as recheck


LEDGER_TEMPLATE = """# EGRESS-BLOCKERS.md

Some intro text.

## Log
"""


def make_ledger(tmp_path: Path) -> Path:
    ledger = tmp_path / "EGRESS-BLOCKERS.md"
    ledger.write_text(LEDGER_TEMPLATE, encoding="utf-8")
    return ledger


def test_append_entry_blocked(tmp_path):
    ledger = make_ledger(tmp_path)
    recheck.append_entry(
        "metmuseum.org",
        True,
        "blocked (ConnectionResetError: [Errno 104] Connection reset by peer)",
        "ai-art-academy/t-008",
        ledger_path=ledger,
    )
    text = ledger.read_text(encoding="utf-8")
    assert "| metmuseum.org | blocked | ai-art-academy/t-008" in text
    assert "ConnectionResetError" in text
    # Original header/intro untouched.
    assert text.startswith("# EGRESS-BLOCKERS.md")


def test_append_entry_reachable_no_task(tmp_path):
    ledger = make_ledger(tmp_path)
    recheck.append_entry(
        "api.stripe.com", False, "reachable (HTTP 200)", None, ledger_path=ledger
    )
    text = ledger.read_text(encoding="utf-8")
    assert "| api.stripe.com | reachable\n" in text
    assert "reachable (HTTP 200)" in text


def test_append_entry_is_additive_never_touches_prior_lines(tmp_path):
    ledger = make_ledger(tmp_path)
    recheck.append_entry("host-a.example", True, "blocked (x)", None, ledger_path=ledger)
    first_snapshot = ledger.read_text(encoding="utf-8")
    recheck.append_entry("host-b.example", False, "reachable (HTTP 200)", None, ledger_path=ledger)
    second_snapshot = ledger.read_text(encoding="utf-8")
    assert second_snapshot.startswith(first_snapshot.rstrip("\n"))
    assert "host-a.example" in second_snapshot
    assert "host-b.example" in second_snapshot


def test_append_entry_missing_file_raises(tmp_path):
    missing = tmp_path / "does-not-exist.md"
    with pytest.raises(SystemExit):
        recheck.append_entry("host.example", True, "blocked (x)", None, ledger_path=missing)


def test_append_entry_missing_log_marker_raises(tmp_path):
    ledger = tmp_path / "EGRESS-BLOCKERS.md"
    ledger.write_text("# EGRESS-BLOCKERS.md\n\nNo log section here.\n", encoding="utf-8")
    with pytest.raises(SystemExit):
        recheck.append_entry("host.example", True, "blocked (x)", None, ledger_path=ledger)


def test_probe_host_reachable(monkeypatch):
    class FakeResp:
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    monkeypatch.setattr(recheck.urllib.request, "urlopen", lambda req, timeout=None: FakeResp())
    blocked, detail = recheck.probe_host("example.com")
    assert blocked is False
    assert "200" in detail


def test_probe_host_reachable_on_http_error(monkeypatch):
    def raise_http_error(req, timeout=None):
        raise recheck.urllib.error.HTTPError(req.full_url, 403, "Forbidden", {}, None)

    monkeypatch.setattr(recheck.urllib.request, "urlopen", raise_http_error)
    blocked, detail = recheck.probe_host("example.com")
    assert blocked is False
    assert "403" in detail


def test_probe_host_blocked_on_connection_failure(monkeypatch):
    def raise_conn_error(req, timeout=None):
        raise ConnectionResetError("Connection reset by peer")

    monkeypatch.setattr(recheck.urllib.request, "urlopen", raise_conn_error)
    blocked, detail = recheck.probe_host("example.com")
    assert blocked is True
    assert "ConnectionResetError" in detail


def test_main_dry_run_does_not_write(tmp_path, monkeypatch, capsys):
    ledger = make_ledger(tmp_path)
    monkeypatch.setattr(recheck, "LEDGER_FILE", ledger)
    monkeypatch.setattr(recheck, "probe_host", lambda host, timeout=10.0: (True, "blocked (x)"))

    exit_code = recheck.main(["example.com", "--no-append"])
    assert exit_code == 0
    assert ledger.read_text(encoding="utf-8") == LEDGER_TEMPLATE
    out = capsys.readouterr().out
    assert out == "\U0001f6ab example.com: blocked (x)\n"


def test_main_appends_using_default_ledger_file(tmp_path, monkeypatch):
    ledger = make_ledger(tmp_path)
    monkeypatch.setattr(recheck, "LEDGER_FILE", ledger)
    monkeypatch.setattr(recheck, "probe_host", lambda host, timeout=10.0: (False, "reachable (HTTP 200)"))

    exit_code = recheck.main(["example.com", "--task", "conductor/t-052"])
    assert exit_code == 0
    text = ledger.read_text(encoding="utf-8")
    assert "| example.com | reachable | conductor/t-052" in text
