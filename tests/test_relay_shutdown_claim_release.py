"""A relay restart must hand its in-flight job back, not abandon it.

2026-08-13, Silas: "I'm confused that I have three artjobs currently running,
when I think only the flux one is actually processing ... possibly jobs that
started during a reboot and never cleared?"

Exactly that. Measured at the time:

    8276  claimed  4.8 min ago  <- genuinely rendering
    6781  claimed 23.7 min ago  <- orphaned by the 16:10:54 restart
    6777  claimed 28.1 min ago  <- orphaned by the 16:03:48 restart

Nothing reaps them. claim.post.ts only FAILs a stale RUNNING job once
attempts >= MAX_ATTEMPTS; below that it is merely re-claimable after
STALE_CLAIM_MINUTES. Correct, but it means abandoned work is counted as
"running" until the queue comes back around to it.

The relay had no SIGTERM handling at all -- only a KeyboardInterrupt catch,
which pm2's SIGTERM never triggers, because Python's default SIGTERM
disposition kills the process outright with no exception raised.
"""

import signal
import sys
from pathlib import Path

RELAY_DIR = Path(__file__).resolve().parents[1] / "ops" / "home-server"
if str(RELAY_DIR) not in sys.path:
    sys.path.insert(0, str(RELAY_DIR))

import relay_agent as relay  # noqa: E402


def test_release_requeues_the_in_flight_job(monkeypatch):
    calls = []

    def fake_post(method, url, body=None, bearer=None, timeout=None):
        calls.append((method, url, body))
        return 200, {"success": True}

    monkeypatch.setattr(relay, "http_json", fake_post)
    monkeypatch.setattr(relay, "log", lambda _m: None)
    monkeypatch.setattr(relay, "_in_flight_job_id", 6781)

    relay.release_in_flight_claim("signal 15")

    assert len(calls) == 1
    method, url, body = calls[0]
    assert method == "POST"
    assert url.endswith("/api/art/queue/6781/requeue")
    # The attempt was counted at claim time. Resetting it on every abandonment
    # would let a job that crashes the relay loop forever.
    assert body == {"resetAttempts": False}


def test_release_is_a_no_op_when_nothing_is_claimed(monkeypatch):
    calls = []
    monkeypatch.setattr(relay, "http_json", lambda *a, **k: calls.append(a))
    monkeypatch.setattr(relay, "_in_flight_job_id", None)
    relay.release_in_flight_claim("signal 15")
    assert calls == []


def test_release_never_raises_on_shutdown(monkeypatch):
    """A failed release must not stop the process from exiting."""
    def boom(*a, **k):
        raise OSError("network gone")

    monkeypatch.setattr(relay, "http_json", boom)
    monkeypatch.setattr(relay, "log", lambda _m: None)
    monkeypatch.setattr(relay, "_in_flight_job_id", 6781)
    relay.release_in_flight_claim("signal 15")  # must not raise

    # A non-200 is also survivable.
    monkeypatch.setattr(relay, "http_json", lambda *a, **k: (500, None))
    relay.release_in_flight_claim("signal 15")


def test_sigterm_is_handled_not_left_at_the_default(monkeypatch):
    """pm2 sends SIGTERM. Python's default disposition kills the process with
    no exception, so the existing KeyboardInterrupt catch never fires."""
    installed = {}
    monkeypatch.setattr(
        relay.signal, "signal", lambda sig, handler: installed.__setitem__(sig, handler)
    )
    relay.install_shutdown_handler()
    assert signal.SIGTERM in installed
    assert signal.SIGINT in installed
    assert installed[signal.SIGTERM] is not signal.SIG_DFL


def test_the_handler_releases_then_exits(monkeypatch):
    released = []
    monkeypatch.setattr(relay, "release_in_flight_claim", released.append)

    installed = {}
    monkeypatch.setattr(
        relay.signal, "signal", lambda sig, handler: installed.__setitem__(sig, handler)
    )
    relay.install_shutdown_handler()

    try:
        installed[signal.SIGTERM](signal.SIGTERM, None)
    except SystemExit as exit_code:
        assert exit_code.code == 0
    else:
        raise AssertionError("the handler must exit the process")
    assert released, "the claim must be released before exiting"


def test_main_installs_the_handler_before_polling():
    source = (RELAY_DIR / "relay_agent.py").read_text(encoding="utf-8")
    main_body = source[source.index("def main("):]
    assert main_body.index("install_shutdown_handler()") < main_body.index(
        "polling {KR_BASE_URL}"
    ), "a job claimed before the handler is installed would still leak"


def test_pm2_allows_time_for_the_release():
    """pm2's default kill_timeout is 1600ms -- tight for an HTTPS round trip."""
    config = (RELAY_DIR / "ecosystem.config.js").read_text(encoding="utf-8")
    for app in ("kr-relay", "kr-download"):
        start = config.index(f"name: '{app}'")
        nxt = config.find("name: '", start + 10)
        block = config[start:] if nxt == -1 else config[start:nxt]
        assert "kill_timeout" in block, f"{app} would be SIGKILLed mid-release"
