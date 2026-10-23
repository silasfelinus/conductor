import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for path in (ROOT / "ops" / "home-server", ROOT / "scripts"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import check_relay_version_drift as drift
import relay_agent as relay
import relay_fingerprint

NOW = datetime(2026, 10, 23, 22, 0, tzinfo=timezone.utc)


def agent(version, minutes_ago=1, agent_id="Silas-PC"):
    seen = (NOW - timedelta(minutes=minutes_ago)).isoformat().replace("+00:00", "Z")
    return {"agentId": agent_id, "lastSeenAt": seen, "agentVersion": version}


def write_relay(root, body=b"x = 1\n"):
    for name in relay_fingerprint.RELAY_CODE_FILES:
        (root / name).write_bytes(body)


def test_fingerprint_ignores_crlf_checkouts(tmp_path):
    unix, windows = tmp_path / "unix", tmp_path / "windows"
    unix.mkdir()
    windows.mkdir()
    write_relay(unix, b"a = 1\nb = 2\n")
    write_relay(windows, b"a = 1\r\nb = 2\r\n")
    assert relay_fingerprint.code_fingerprint(unix) == relay_fingerprint.code_fingerprint(windows)


def test_fingerprint_changes_when_any_relay_module_changes(tmp_path):
    write_relay(tmp_path)
    before = relay_fingerprint.code_fingerprint(tmp_path)
    (tmp_path / "coat_dance_vace_worker.py").write_bytes(b"x = 2\n")
    assert relay_fingerprint.code_fingerprint(tmp_path) != before


def test_relay_reports_its_fingerprint_as_agent_version():
    expected = relay_fingerprint.code_fingerprint()
    assert relay_fingerprint.parse_fingerprint(relay.RELAY_VERSION) == expected


def test_matching_relay_is_clean():
    expected = relay_fingerprint.code_fingerprint()
    code, lines = drift.assess([agent(relay_fingerprint.relay_version("ad0277b"))], expected, NOW)
    assert code == 0
    assert expected in lines[0]


def test_pre_fingerprint_relay_is_stale():
    code, lines = drift.assess([agent("conductor-relay-completion-proof-v1")], "0123456789ab", NOW)
    assert code == 1
    assert "pre-fingerprint build" in lines[1]
    assert "pm2 restart kr-relay" in lines[1]


def test_relay_on_other_code_is_stale():
    code, lines = drift.assess([agent("conductor-relay-ffffffffffff@abc1234")], "0123456789ab", NOW)
    assert code == 1
    assert "runs ffffffffffff" in lines[1]


def test_relays_not_seen_recently_are_ignored():
    code, lines = drift.assess(
        [agent("conductor-relay-completion-proof-v1", minutes_ago=120)], "0123456789ab", NOW
    )
    assert code == 0
    assert "no relay seen" in lines[0]


def test_missing_token_is_unresolved(monkeypatch, capsys):
    monkeypatch.delenv("KR_API_TOKEN", raising=False)
    assert drift.main([]) == 2
    assert "unresolved" in capsys.readouterr().out
