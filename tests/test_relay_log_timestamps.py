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


# --- Startup must not block on ComfyUI, and must carry exactly one stamp -----

def test_warm_up_does_not_block_startup(monkeypatch):
    """Warming is an optimisation, never a precondition.

    The first version called fetch_comfy_object_info(force=True) inline in
    main(). The fetch may take _OBJECT_INFO_TIMEOUT x _OBJECT_INFO_ATTEMPTS
    plus backoff, so on a box whose ComfyUI was mid-render the relay sat for
    ~3 minutes before claiming its first job -- silently, because neither the
    warm-up line nor the "polling" line had been reached. Observed 2026-08-13.
    """
    import time as _time

    def slow_and_failing(*a, **k):
        _time.sleep(0.4)
        raise OSError("timed out")

    monkeypatch.setattr(relay, "http_json", slow_and_failing)
    monkeypatch.setattr(relay.time, "sleep", lambda _s: None)
    monkeypatch.setattr(relay, "log", lambda _m: None)
    relay._object_info_cache.update(at=0.0, data=None)

    started = _time.monotonic()
    thread = relay.warm_object_info_async()
    elapsed = _time.monotonic() - started

    assert elapsed < 0.2, f"warm-up blocked startup for {elapsed:.2f}s"
    assert thread.daemon, "a warm-up thread must never hold the process open"
    thread.join(timeout=5)


def test_main_warms_before_it_polls():
    source = (RELAY_DIR / "relay_agent.py").read_text(encoding="utf-8")
    main_body = source[source.index("def main("):]
    assert "fetch_comfy_object_info(force=True)" not in main_body.split("while True")[0], (
        "main() must not fetch object_info inline -- use warm_object_info_async"
    )
    assert main_body.index("warm_object_info_async()") < main_body.index(
        "polling {KR_BASE_URL}"
    )


LINE = re.compile(
    r"^(?P<iso>\S+) \[(?P<human>[A-Z][a-z]{2} \d{1,2} \d{1,2}:\d{2}[AP]M)\] "
    r"(?P<source>\S+) (?P<message>.*)$"
)


def test_log_line_leads_with_iso_then_a_readable_time(monkeypatch):
    """`cut -d' ' -f1` is still the ISO stamp; the bracket is for reading.

    pm2's duplicate prefix is disabled for these two apps
    (ecosystem.config.js, time:false) -- pm2's own stamp carries no offset,
    so it was strictly worse than ours."""
    for module, source_tag in ((relay, "relay"), (lora, "lora-import")):
        lines = []
        monkeypatch.setattr("builtins.print", lambda msg, **kw: lines.append(msg))
        module.log("hello world")
        match = LINE.match(lines[0])
        assert match, f"unexpected log shape: {lines[0]!r}"
        assert ISO_WITH_OFFSET.fullmatch(match["iso"])
        assert datetime.fromisoformat(match["iso"]).tzinfo is not None
        assert match["source"] == source_tag
        assert match["message"] == "hello world"
        # The two stamps must describe the same instant, not drift apart.
        parsed = datetime.fromisoformat(match["iso"])
        assert relay.human_time(parsed) == match["human"]


def test_human_time_handles_midnight_and_noon():
    """12-hour clocks are where hand-rolled formatting goes wrong."""
    from datetime import datetime as dt

    cases = {
        (0, 5): "12:05AM",
        (9, 30): "9:30AM",
        (11, 59): "11:59AM",
        (12, 0): "12:00PM",
        (15, 47): "3:47PM",
        (23, 59): "11:59PM",
    }
    for (hour, minute), expected in cases.items():
        got = relay.human_time(dt(2026, 8, 13, hour, minute))
        assert got == f"Aug 13 {expected}", f"{hour:02d}:{minute:02d} -> {got}"


def test_human_time_uses_no_platform_specific_directives():
    """%-I/%-d are glibc; Windows wants %#I/%#d. The relay runs on Windows, so
    the readable stamp is built by arithmetic, not strftime padding flags.

    Checks USE, not mention -- the docstring explaining this necessarily names
    the directives it forbids, and a naive substring scan flags itself."""
    # A no-pad directive as actually used: inside strftime("...") or an
    # f-string format spec such as {moment:%-I}.
    used = re.compile(r"""strftime\([^)]*%[-#]|:%[-#]""")
    for name in ("relay_agent.py", "lora_import_agent.py"):
        source = (RELAY_DIR / name).read_text(encoding="utf-8")
        hit = used.search(source)
        assert hit is None, f"{name} uses a platform-specific directive: {hit.group(0)!r}"


def _pm2_app_block(config, app):
    """The config text for one app: from its name to the start of the next."""
    start = config.index(f"name: '{app}'")
    nxt = config.find("name: '", start + 10)
    return config[start:] if nxt == -1 else config[start:nxt]


def test_pm2_does_not_double_stamp_the_self_stamping_agents():
    config = (RELAY_DIR / "ecosystem.config.js").read_text(encoding="utf-8")
    # Our agents already lead every line with an offset-qualified stamp.
    for app in ("kr-relay", "kr-download"):
        block = _pm2_app_block(config, app)
        assert "time: false" in block, f"{app} would carry two timestamps per line"
        assert "time: true" not in block
    # ComfyUI and sd-webui do not stamp themselves, so pm2 must.
    for app in ("comfyui", "sd-webui"):
        block = _pm2_app_block(config, app)
        assert "time: true" in block, f"{app} does not stamp itself and needs pm2's"
        assert "log_date_format" in block
