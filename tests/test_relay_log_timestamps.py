"""Timestamps on every operational log line, and a build stamp at startup.

Why this file exists (Silas, 2026-08-13): "It isn't the first time (or tenth)
we've been unable to identify when problems occurred or if we're looking at
stale problems."

Two distinct failures, both real this session:

1. A log line with no timezone cannot be lined up against an ArtJob's
   `updatedAt`, which is UTC. `[relay 2026-08-13 10:56:11]` is either 17:56 or
   18:56 UTC depending on DST, and the difference decides whether a failure is
   the one you are chasing.
2. Nothing said which build was running. A LoRA resolver that had been merged,
   tested, and pulled was diagnosed as a stale deployment; the real cause was a
   second submission path that never called it. `KR_RELAY_COMMIT` existed for
   exactly this and was always empty, because it needed a human to export it.
"""

import re
import sys
from datetime import datetime
from pathlib import Path

RELAY_DIR = Path(__file__).resolve().parents[1] / "ops" / "home-server"
if str(RELAY_DIR) not in sys.path:
    sys.path.insert(0, str(RELAY_DIR))

import lora_import_agent as lora  # noqa: E402
import relay_agent as relay  # noqa: E402

# ISO 8601 with a REQUIRED offset: ...T10:56:11-07:00 or ...T17:56:11+00:00.
ISO_WITH_OFFSET = re.compile(
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:[+-]\d{2}:\d{2}|Z)"
)


def test_relay_log_line_carries_an_offset_qualified_timestamp(monkeypatch):
    lines = []
    monkeypatch.setattr("builtins.print", lambda msg, **kwargs: lines.append(msg))
    relay.log("polling")
    assert len(lines) == 1
    stamp = ISO_WITH_OFFSET.search(lines[0])
    assert stamp, f"no offset-qualified timestamp in {lines[0]!r}"
    # Parseable, not merely regex-shaped -- an unparseable stamp is no better
    # than none when correlating against the queue.
    parsed = datetime.fromisoformat(stamp.group(0).replace("Z", "+00:00"))
    assert parsed.tzinfo is not None
    assert "polling" in lines[0]


def test_lora_import_log_uses_the_same_format(monkeypatch):
    # Both streams interleave in one pm2 log, so they must be comparable.
    lines = []
    monkeypatch.setattr("builtins.print", lambda msg, **kwargs: lines.append(msg))
    lora.log("importing")
    assert ISO_WITH_OFFSET.search(lines[0]), lines[0]
    assert "importing" in lines[0]


def test_naive_local_timestamps_are_gone_from_both_agents():
    # The exact pattern that caused the ambiguity: strftime with no %z.
    for name in ("relay_agent.py", "lora_import_agent.py"):
        source = (RELAY_DIR / name).read_text(encoding="utf-8")
        assert 'strftime("%Y-%m-%d %H:%M:%S")' not in source, (
            f"{name} still logs a naive local timestamp"
        )


def test_build_is_detected_without_an_env_var():
    build = relay.detect_relay_build()
    assert build["source"] in {"git", "mtime", "unknown"}
    if build["source"] == "git":
        assert build["commit"], "git detection must yield a commit"
        assert datetime.fromisoformat(build["committed_at"]).tzinfo is not None
    elif build["source"] == "mtime":
        assert datetime.fromisoformat(build["committed_at"]).tzinfo is not None


def test_build_detection_never_raises_when_git_is_unavailable(monkeypatch):
    def boom(*args, **kwargs):
        raise OSError("git not found")

    monkeypatch.setattr(relay.subprocess, "run", boom)
    build = relay.detect_relay_build()
    # Falls back to mtime rather than crashing the relay at import time.
    assert build["source"] in {"mtime", "unknown"}


def test_startup_logs_which_build_is_running(monkeypatch):
    logged = []
    monkeypatch.setattr(relay, "log", logged.append)
    monkeypatch.setattr(
        relay,
        "RELAY_BUILD",
        {"commit": "abc1234", "committed_at": "2026-08-13T11:38:40-07:00", "source": "git"},
    )
    monkeypatch.setattr(relay, "RELAY_COMMIT", "abc1234")
    relay.log_build_identity()
    assert len(logged) == 1
    assert "abc1234" in logged[0]
    assert "2026-08-13T11:38:40-07:00" in logged[0]


def test_relay_commit_reaches_the_api_without_an_env_var():
    # relayCommit is sent on every heartbeat; it was always None because
    # KR_RELAY_COMMIT was never exported. It must now be populated by detection.
    assert relay.RELAY_COMMIT, "RELAY_COMMIT must fall back to the detected build"
