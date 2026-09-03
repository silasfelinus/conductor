"""Tests for scripts/check_container_log_drift.py. No network, no real digest.

The staleness case is the one that matters most. A log-triage pipeline that
dies quietly is worse than not having one, because "nothing to report" and
"not running" are indistinguishable from the reading end -- which is the exact
failure check_engine_heartbeat.py was written for after healthcheck.ps1 stopped
running for ~37 hours and its log simply ended.
"""

import json
from datetime import datetime, timedelta, timezone

import scripts.check_container_log_drift as check

NOW = datetime(2026, 9, 3, 12, 0, 0, tzinfo=timezone.utc)


def make_digest(generated_at=None, new=(), spiking=(), quiet=(), failed=()):
    return {
        "version": 1,
        "generated_at": (generated_at or NOW).isoformat(),
        "host": "alexandria",
        "window": "24h",
        "scan": {
            "containers_total": 52,
            "containers_scanned": 51,
            "containers_failed": list(failed),
            "truncated": [],
            "high_cardinality": [],
            "lines_read": 91234,
            "lines_matched": 4120,
            "signatures_total": 87,
        },
        "new": list(new),
        "spiking": list(spiking),
        "quiet": list(quiet),
        "top": [],
    }


def signature(fingerprint="abc123abc123", container="plex", count=5, baseline=None):
    return {
        "fingerprint": fingerprint,
        "container": container,
        "severity": "error",
        "count": count,
        "baseline": baseline,
        "sample": "ERROR database is locked",
        "skeleton": "error database is locked",
    }


# --------------------------------------------------------------------------
# assess()
# --------------------------------------------------------------------------

def test_fresh_and_empty_is_clean():
    state, reason, findings = check.assess(make_digest(), NOW, 48.0)
    assert state == "clean"
    assert not findings
    assert "51 containers scanned" in reason


def test_new_signature_is_a_finding():
    state, reason, findings = check.assess(make_digest(new=[signature()]), NOW, 48.0)
    assert state == "findings"
    assert len(findings) == 1
    assert findings[0]["bucket"] == "new"


def test_spiking_signature_is_a_finding():
    digest = make_digest(spiking=[signature(count=4000, baseline=12.0)])
    state, reason, findings = check.assess(digest, NOW, 48.0)
    assert state == "findings"
    assert findings[0]["bucket"] == "spiking"


def test_quiet_alone_does_not_trip_the_check():
    # Worth surfacing in the text, but it is not a reason to fail a sweep.
    state, reason, findings = check.assess(make_digest(quiet=[signature()]), NOW, 48.0)
    assert state == "clean"
    assert "1 went quiet" not in reason or state == "clean"


def test_stale_digest_is_a_finding_even_with_nothing_new():
    old = NOW - timedelta(hours=72)
    state, reason, findings = check.assess(make_digest(generated_at=old), NOW, 48.0)
    assert state == "stale"
    assert "72.0h old" in reason
    assert "stopped running" in reason


def test_digest_just_inside_the_window_is_clean():
    recent = NOW - timedelta(hours=47)
    state, _, _ = check.assess(make_digest(generated_at=recent), NOW, 48.0)
    assert state == "clean"


def test_stale_beats_findings():
    # A stale digest's "findings" are days old; the staleness is the real news.
    old = NOW - timedelta(hours=99)
    state, _, findings = check.assess(make_digest(generated_at=old, new=[signature()]), NOW, 48.0)
    assert state == "stale"
    assert not findings


def test_missing_timestamp_is_unresolved():
    digest = make_digest()
    del digest["generated_at"]
    state, reason, _ = check.assess(digest, NOW, 48.0)
    assert state == "unresolved"


def test_unreadable_containers_are_mentioned_when_clean():
    digest = make_digest(failed=[{"container": "nolog", "error": "no log driver"}])
    state, reason, _ = check.assess(digest, NOW, 48.0)
    assert state == "clean"
    assert "1 unreadable" in reason


# --------------------------------------------------------------------------
# load_digest() and main()
# --------------------------------------------------------------------------

def test_absent_digest_loads_as_none(tmp_path):
    assert check.load_digest(str(tmp_path / "missing.json")) is None


def test_corrupt_digest_raises(tmp_path):
    path = tmp_path / "digest.json"
    path.write_text("not json at all", encoding="utf-8")
    try:
        check.load_digest(str(path))
    except RuntimeError as error:
        assert "unreadable" in str(error)
    else:
        raise AssertionError("corrupt digest should raise")


def test_main_exits_clean_when_not_configured(tmp_path, capsys):
    code = check.main(["--digest", str(tmp_path / "missing.json")])
    assert code == check.EXIT_CLEAN
    assert "not configured yet" in capsys.readouterr().out


def test_main_exits_findings_on_new_signatures(tmp_path):
    path = tmp_path / "digest.json"
    path.write_text(json.dumps(make_digest(new=[signature()])), encoding="utf-8")
    assert check.main(["--digest", str(path)]) == check.EXIT_FINDINGS


def test_main_exits_unresolved_on_corrupt_digest(tmp_path):
    path = tmp_path / "digest.json"
    path.write_text("{{{", encoding="utf-8")
    assert check.main(["--digest", str(path)]) == check.EXIT_UNRESOLVED


def test_main_json_mode_is_parseable(tmp_path, capsys):
    path = tmp_path / "digest.json"
    path.write_text(json.dumps(make_digest(new=[signature()])), encoding="utf-8")
    check.main(["--digest", str(path), "--json"])
    payload = json.loads(capsys.readouterr().out)
    assert payload["state"] == "findings"
    assert payload["host"] == "alexandria"


def test_render_does_not_crash_on_missing_fields():
    digest = make_digest(new=[{"bucket": "new"}])
    text = check.render("findings", "1 new", [{"bucket": "new"}], digest)
    assert "container log triage FINDINGS" in text
