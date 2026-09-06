"""Heartbeats must keep posting even while the poll loop is blocked in process().

conductor/t-147 (ArtJob 21616, 2026-09-05): the relay's one concurrent slot
hung inside process(job) for ~30 minutes with no error and no other job
claimed. Reviewing the repo-side LoRA fix for that incident (kind_robots#2435)
surfaced a second, independent cause of misleading incident behaviour:
relay_agent.py only called send_heartbeats() from inside the poll loop, once
per pass, between jobs -- so a single long or wedged process(job) call (fully
synchronous: claim -> render -> upload -> complete) silently stopped
heartbeats for its entire duration. A watchdog reading heartbeat freshness
during that window could not distinguish "alive but busy" from "silent"; both
look identical with no heartbeat at all.

These tests lock the fix: heartbeats run on their own daemon thread, started
once in main(), independent of whatever the poll loop is doing.
"""

import sys
import threading
import time
from pathlib import Path

RELAY_DIR = Path(__file__).resolve().parents[1] / "ops" / "home-server"
if str(RELAY_DIR) not in sys.path:
    sys.path.insert(0, str(RELAY_DIR))

import relay_agent as relay  # noqa: E402


def test_heartbeat_thread_ticks_on_its_own_schedule(monkeypatch):
    """The thread must call send_heartbeats() repeatedly without any help
    from the poll loop -- nothing here ever calls relay.main()."""
    calls = threading.Event()
    count = []

    def fake_send():
        count.append(1)
        if len(count) >= 3:
            calls.set()

    monkeypatch.setattr(relay, "send_heartbeats", fake_send)
    monkeypatch.setattr(relay, "HEARTBEAT_SECONDS", 0.01)

    thread = relay.start_heartbeat_thread()
    try:
        assert thread is not None
        assert thread.daemon
        assert calls.wait(timeout=5), f"only {len(count)} heartbeat(s) sent"
    finally:
        # Daemon thread with no stop switch; the process exiting is what
        # normally reaps it. Nothing to join in a test -- just stop asserting.
        pass


def test_heartbeat_thread_keeps_ticking_while_something_else_blocks(monkeypatch):
    """The exact shape of t-147: a long synchronous call must not suppress
    heartbeats. Simulate process(job) blocking for longer than several
    heartbeat intervals and confirm ticks still land during that window."""
    tick_count = []
    tick_lock = threading.Lock()

    def fake_send():
        with tick_lock:
            tick_count.append(time.monotonic())

    monkeypatch.setattr(relay, "send_heartbeats", fake_send)
    monkeypatch.setattr(relay, "HEARTBEAT_SECONDS", 0.01)

    relay.start_heartbeat_thread()

    # Stand in for a wedged process(job): block the "main loop" for well
    # longer than several heartbeat intervals, on this same test thread.
    time.sleep(0.1)

    with tick_lock:
        ticks_during_block = len(tick_count)
    assert ticks_during_block >= 3, (
        f"expected several heartbeats during a 0.1s block at a 0.01s "
        f"interval, got {ticks_during_block}"
    )


def test_heartbeat_thread_disabled_when_interval_is_zero(monkeypatch):
    logged = []
    monkeypatch.setattr(relay, "log", lambda message: logged.append(str(message)))
    monkeypatch.setattr(relay, "HEARTBEAT_SECONDS", 0)

    thread = relay.start_heartbeat_thread()

    assert thread is None
    assert any("disabled" in line for line in logged)


def test_heartbeat_thread_survives_a_failing_send(monkeypatch):
    """post_heartbeat already swallows its own errors, but the loop itself
    must not die even if send_heartbeats somehow raises."""
    calls = threading.Event()
    attempts = []

    def flaky_send():
        attempts.append(1)
        if len(attempts) == 1:
            raise RuntimeError("boom")
        calls.set()

    monkeypatch.setattr(relay, "send_heartbeats", flaky_send)
    monkeypatch.setattr(relay, "HEARTBEAT_SECONDS", 0.01)

    relay.start_heartbeat_thread()
    assert calls.wait(timeout=5), "heartbeat loop died after one failure"


def test_main_starts_the_heartbeat_thread_independently_of_the_poll_loop():
    """Wiring check: main() must start the heartbeat thread itself rather
    than folding heartbeat cadence back into the poll loop -- a heartbeat
    call sitting inline in the while-loop is exactly the bug this replaces."""
    import inspect

    source = inspect.getsource(relay.main)
    assert "start_heartbeat_thread()" in source
    # The old inline cadence check must be gone, not just supplemented.
    assert "last_heartbeat" not in source
