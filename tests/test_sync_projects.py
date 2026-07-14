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
    # kind_robots occasionally wraps a raw DB-driver connection drop in an
    # HTTP 400 instead of a 5xx — status-code-only retry logic misses this.
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
        except urllib.error.HTTPError as e:
            assert e.code == 400
            assert b"Validation failed" in e.read()
    sleep.assert_not_called()


def test_does_not_retry_401():
    def fake_urlopen(req, timeout=15):
        raise http_error(401, b'{"message":"unauthorized"}')

    with patch("urllib.request.urlopen", side_effect=fake_urlopen), patch("time.sleep") as sleep:
        try:
            sp.kr_request("GET", "/projects/foo", "tok")
            assert False, "expected HTTPError"
        except urllib.error.HTTPError as e:
            assert e.code == 401
    sleep.assert_not_called()


def test_body_still_readable_after_exhausting_retries():
    def fake_urlopen(req, timeout=15):
        body = b'{"message":"Cannot execute new commands: connection closed"}'
        raise http_error(400, body)

    with patch("urllib.request.urlopen", side_effect=fake_urlopen), patch("time.sleep"):
        try:
            sp.kr_request("GET", "/projects/animation-manager", "tok")
            assert False, "expected HTTPError"
        except urllib.error.HTTPError as e:
            assert e.code == 400
            # Body must be readable more than once — sync_project() reads it
            # for its ERROR log line after kr_request re-raises.
            assert b"connection closed" in e.read()
            assert b"connection closed" in e.read()
