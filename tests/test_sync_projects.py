import io
import urllib.error
from unittest.mock import patch

import scripts.sync_projects as sp


class FakeResponse:
    def __init__(self, data):
        self._data = data

    def read(self):
        return self._data

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def http_error(code, body):
    return urllib.error.HTTPError("http://x", code, "err", {}, io.BytesIO(body))


# ---------------------------------------------------------------------------
# kr_request retry classification
# ---------------------------------------------------------------------------

def test_retries_5xx_status_code():
    calls = {"n": 0}

    def fake_urlopen(req, timeout=15):
        calls["n"] += 1
        if calls["n"] == 1:
            raise http_error(503, b"")
        return FakeResponse(b'{"ok": true}')

    with patch("urllib.request.urlopen", side_effect=fake_urlopen), patch("time.sleep"):
        result = sp.kr_request("GET", "/x", "tok")
    assert result == {"ok": True}
    assert calls["n"] == 2


def test_retries_400_with_transient_body_marker():
    calls = {"n": 0}

    def fake_urlopen(req, timeout=15):
        calls["n"] += 1
        if calls["n"] == 1:
            body = b'{"message":"Cannot execute new commands: connection closed"}'
            raise http_error(400, body)
        return FakeResponse(b'{"ok": true}')

    with patch("urllib.request.urlopen", side_effect=fake_urlopen), patch("time.sleep"):
        result = sp.kr_request("GET", "/projects/animation-manager", "tok")
    assert result == {"ok": True}
    assert calls["n"] == 2


def test_does_not_retry_genuine_400():
    def fake_urlopen(req, timeout=15):
        raise http_error(400, b'{"message":"Validation failed: title required"}')

    with patch("urllib.request.urlopen", side_effect=fake_urlopen), patch("time.sleep") as sleep:
        try:
            sp.kr_request("POST", "/projects", "tok", {"title": ""})
            assert False, "expected HTTPError"
        except urllib.error.HTTPError as error:
            assert error.code == 400
            assert b"Validation failed" in error.read()
    sleep.assert_not_called()


def test_does_not_retry_401():
    def fake_urlopen(req, timeout=15):
        raise http_error(401, b'{"message":"unauthorized"}')

    with patch("urllib.request.urlopen", side_effect=fake_urlopen), patch("time.sleep") as sleep:
        try:
            sp.kr_request("GET", "/projects/foo", "tok")
            assert False, "expected HTTPError"
        except urllib.error.HTTPError as error:
            assert error.code == 401
    sleep.assert_not_called()


def test_body_still_readable_after_exhausting_retries():
    def fake_urlopen(req, timeout=15):
        body = b'{"message":"Cannot execute new commands: connection closed"}'
        raise http_error(400, body)

    with patch("urllib.request.urlopen", side_effect=fake_urlopen), patch("time.sleep"):
        try:
            sp.kr_request("GET", "/projects/animation-manager", "tok")
            assert False, "expected HTTPError"
        except urllib.error.HTTPError as error:
            assert error.code == 400
            assert b"connection closed" in error.read()
            assert b"connection closed" in error.read()


# ---------------------------------------------------------------------------
# Project lifecycle synchronization
# ---------------------------------------------------------------------------

def test_synced_overrides_keeps_every_recognized_lifecycle():
    overrides = [
        {"slug": "a", "status": "active"},
        {"slug": "b", "status": "paused"},
        {"slug": "c", "status": "finished"},
        {"slug": "d", "status": "retired"},
        {"slug": "e", "status": "unknown"},
        {"status": "active"},
    ]

    assert [entry["slug"] for entry in sp.synced_overrides(overrides)] == [
        "a",
        "b",
        "c",
        "d",
    ]


def test_build_project_payload_maps_status_priority_and_active_state():
    cases = [
        ("active", "ACTIVE", True),
        ("paused", "PAUSED", True),
        ("finished", "DONE", True),
        ("retired", "ARCHIVED", False),
    ]

    for conductor_status, expected_status, expected_active in cases:
        payload = sp.build_project_payload(
            "sample-project",
            {
                "status": conductor_status,
                "priority": "urgent",
                "liveUrl": "/sample",
            },
            {
                "project": "Sample Project",
                "goal": "Ship it.",
                "notes_from_silas": "Useful project description.",
            },
        )
        assert payload["status"] == expected_status
        assert payload["priority"] == "HIGH"
        assert payload["isActive"] is expected_active
        assert payload["liveUrl"] == "/sample"
        assert payload["goal"] == "Ship it."


def test_project_changed_fields_detects_archival_state():
    existing = {
        "status": "ACTIVE",
        "priority": "NORMAL",
        "isActive": True,
    }
    payload = {
        "status": "ARCHIVED",
        "priority": "NORMAL",
        "isActive": False,
        "lastSyncedAt": "ignored",
    }

    assert sp.project_changed_fields(existing, payload) == ["status", "isActive"]


def test_main_syncs_all_lifecycle_entries(monkeypatch, capsys):
    overrides = [
        {"slug": "active-one", "status": "active"},
        {"slug": "paused-one", "status": "paused"},
        {"slug": "done-one", "status": "finished"},
        {"slug": "retired-one", "status": "retired"},
        {"slug": "ignored-one", "status": "unknown"},
    ]
    synced = []

    monkeypatch.setenv("KR_API_TOKEN", "token")
    monkeypatch.setattr(sp, "load_overrides", lambda: overrides)
    monkeypatch.setattr(
        sp,
        "sync_project",
        lambda slug, override, token: synced.append((slug, override["status"], token)) or True,
    )

    sp.main()

    assert synced == [
        ("active-one", "active", "token"),
        ("paused-one", "paused", "token"),
        ("done-one", "finished", "token"),
        ("retired-one", "retired", "token"),
    ]
    output = capsys.readouterr().out
    assert "syncing 4 tracked projects" in output
    assert "active=1" in output
    assert "paused=1" in output
    assert "finished=1" in output
    assert "retired=1" in output
