import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import scripts.review_claim as rvc


def minutes_ago(minutes: float, *, now: datetime) -> str:
    return (now - timedelta(minutes=minutes)).strftime("%Y-%m-%dT%H:%M:%SZ")


def test_format_marker_round_trips_through_parse_marker():
    now = datetime(2026, 7, 28, 23, 30, 0, tzinfo=timezone.utc)
    body = rvc.format_marker("reviewer/session-abc", now=now)
    parsed = rvc.parse_marker(body)
    assert parsed is not None
    session, posted_at = parsed
    assert session == "reviewer/session-abc"
    assert posted_at == now


def test_parse_marker_rejects_unrelated_comment():
    assert rvc.parse_marker("Looks good, merging.") is None


def test_parse_marker_rejects_malformed_marker():
    assert rvc.parse_marker("REVIEWING: someone") is None
    assert rvc.parse_marker("REVIEWING: someone at not-a-timestamp") is None


def test_marker_is_fresh_within_ttl():
    now = datetime.now(timezone.utc)
    posted_at = now - timedelta(minutes=5)
    assert rvc.marker_is_fresh(posted_at, now=now) is True


def test_marker_is_fresh_exactly_at_ttl_boundary():
    now = datetime.now(timezone.utc)
    posted_at = now - timedelta(minutes=rvc.REVIEW_CLAIM_TTL_MINUTES)
    assert rvc.marker_is_fresh(posted_at, now=now) is True


def test_marker_is_stale_past_ttl():
    now = datetime.now(timezone.utc)
    posted_at = now - timedelta(minutes=rvc.REVIEW_CLAIM_TTL_MINUTES + 1)
    assert rvc.marker_is_fresh(posted_at, now=now) is False


def test_marker_from_the_future_is_not_fresh():
    # A clock-skewed or malformed future timestamp must not count as an active claim.
    now = datetime.now(timezone.utc)
    posted_at = now + timedelta(minutes=5)
    assert rvc.marker_is_fresh(posted_at, now=now) is False


def test_find_active_claim_returns_none_for_no_markers():
    comments = [{"body": "LGTM", "created_at": "2026-07-28T23:00:00Z"}]
    assert rvc.find_active_claim(comments) is None


def test_find_active_claim_returns_fresh_marker():
    now = datetime.now(timezone.utc)
    comments = [
        {"body": "unrelated comment", "created_at": minutes_ago(30, now=now)},
        {"body": rvc.format_marker("reviewer/other-session", now=now - timedelta(minutes=3)), "created_at": ""},
    ]
    claim = rvc.find_active_claim(comments, now=now)
    assert claim is not None
    assert claim["session"] == "reviewer/other-session"


def test_find_active_claim_ignores_stale_marker():
    now = datetime.now(timezone.utc)
    stale_marker = rvc.format_marker("reviewer/old-session", now=now - timedelta(minutes=rvc.REVIEW_CLAIM_TTL_MINUTES + 1))
    comments = [{"body": stale_marker, "created_at": ""}]
    assert rvc.find_active_claim(comments, now=now) is None


def test_find_active_claim_excludes_own_session():
    # A session re-checking a PR it already claimed should not see its own marker
    # as a collision.
    now = datetime.now(timezone.utc)
    own_marker = rvc.format_marker("reviewer/me", now=now - timedelta(minutes=2))
    comments = [{"body": own_marker, "created_at": ""}]
    assert rvc.find_active_claim(comments, now=now, exclude_session="reviewer/me") is None
    assert rvc.find_active_claim(comments, now=now) is not None


def test_find_active_claim_returns_freshest_of_multiple_markers():
    now = datetime.now(timezone.utc)
    older = rvc.format_marker("reviewer/first", now=now - timedelta(minutes=10))
    newer = rvc.format_marker("reviewer/second", now=now - timedelta(minutes=1))
    comments = [{"body": older, "created_at": ""}, {"body": newer, "created_at": ""}]
    claim = rvc.find_active_claim(comments, now=now)
    assert claim["session"] == "reviewer/second"


def test_find_active_claim_ignores_malformed_body_types():
    comments = [{"body": None}, {"created_at": "2026-07-28T23:00:00Z"}, {}]
    assert rvc.find_active_claim(comments) is None


def run(cmd: list[str], *, input: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, input=input, check=False)


def test_cli_format_prints_marker():
    result = run([sys.executable, "scripts/review_claim.py", "format", "reviewer/cli-session"])
    assert result.returncode == 0
    parsed = rvc.parse_marker(result.stdout.strip())
    assert parsed is not None
    assert parsed[0] == "reviewer/cli-session"


def test_cli_check_reports_no_claim_via_exit_code_and_null(tmp_path: Path):
    comments_file = tmp_path / "comments.json"
    comments_file.write_text(json.dumps([{"body": "LGTM", "created_at": "2026-07-28T23:00:00Z"}]))
    result = run([sys.executable, "scripts/review_claim.py", "check", str(comments_file)])
    assert result.returncode == 0
    assert result.stdout.strip() == "null"


def test_cli_check_reports_active_claim_via_exit_code_and_json(tmp_path: Path):
    now = datetime.now(timezone.utc)
    marker = rvc.format_marker("reviewer/found-me", now=now - timedelta(minutes=1))
    comments_file = tmp_path / "comments.json"
    comments_file.write_text(json.dumps([{"body": marker, "created_at": ""}]))
    result = run([sys.executable, "scripts/review_claim.py", "check", str(comments_file)])
    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert payload["session"] == "reviewer/found-me"


def test_cli_check_reads_from_stdin():
    comments = json.dumps([{"body": "LGTM", "created_at": ""}])
    result = run([sys.executable, "scripts/review_claim.py", "check", "-"], input=comments)
    assert result.returncode == 0
    assert result.stdout.strip() == "null"
