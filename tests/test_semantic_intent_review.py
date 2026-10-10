"""GitHub semantic intent reviews must be real, fail closed and page only on failure."""
from datetime import date, datetime, timezone
from pathlib import Path
from unittest import mock

import pytest

from scripts import run_semantic_intent_review as review
from scripts import semantic_intent_actions as runs
from scripts import ensure_semantic_intent_review as ensure


def test_review_due_uses_merged_dated_reports(tmp_path):
    directory = tmp_path / "projects/conductor"
    directory.mkdir(parents=True)
    assert review.due(tmp_path, date(2026, 10, 10))
    (directory / "INTENT-AUDIT-2026-10-08.md").write_text("substantive review")
    assert not review.due(tmp_path, date(2026, 10, 10))
    assert review.due(tmp_path, date(2026, 10, 11))


def test_missing_token_never_fakes_report(tmp_path):
    directory = tmp_path / "projects/conductor"
    directory.mkdir(parents=True)
    with pytest.raises(ValueError, match="GITHUB_TOKEN"):
        review.execute(tmp_path, date(2026, 10, 10), "")
    assert list(directory.glob("INTENT-AUDIT-*.md")) == []


def test_incomplete_model_output_never_fakes_report(tmp_path, monkeypatch):
    directory = tmp_path / "projects/conductor"
    directory.mkdir(parents=True)
    monkeypatch.setattr(review, "gather", lambda root: "source")
    monkeypatch.setattr(review, "model_review", lambda context, token: (_ for _ in ()).throw(
        ValueError("Incomplete semantic-review response")
    ))
    with pytest.raises(ValueError, match="Incomplete"):
        review.execute(tmp_path, date(2026, 10, 10), "fake")
    assert list(directory.glob("INTENT-AUDIT-*.md")) == []


def test_actual_model_output_creates_one_dated_report(tmp_path, monkeypatch):
    directory = tmp_path / "projects/conductor"
    directory.mkdir(parents=True)
    monkeypatch.setattr(review, "gather", lambda root: "verified sources")
    text = "## Verified\n" + "\n".join(review.LEADS) + "\nCONTROL.md roadmap.yaml\n"
    text += ("Confirmed explicit project direction. " * 12)
    text += "\n## Corrected\nNone.\n## Still questionable\nManual QA required.\n## Next review\nThree days."
    monkeypatch.setattr(review, "model_review", lambda context, token: text)
    result = review.execute(tmp_path, date(2026, 10, 10), "fake")
    assert result["status"] == "completed"
    assert "## Still questionable" in (tmp_path / result["report"]).read_text()
    assert not review.due(tmp_path, date(2026, 10, 11))


def _run(status, conclusion, when="2026-10-10T15:00:00Z"):
    return {"status": status, "conclusion": conclusion, "created_at": when,
            "run_started_at": when, "html_url": "https://github.com/example/repo/actions/runs/1"}


def test_due_alone_is_never_failed_attempt():
    assert runs.failed_attempt([], date(2026, 10, 3)) is None
    assert runs.failed_attempt([_run("in_progress", None)], date(2026, 10, 3)) is None
    assert runs.failed_attempt([_run("completed", "success")], date(2026, 10, 3)) is None


def test_only_latest_actual_failure_triggers_email_marker():
    bad = _run("completed", "failure", "2026-10-10T15:00:00Z")
    assert runs.failed_attempt([bad], date(2026, 10, 3))["status"] == "failed"
    assert runs.failed_attempt([bad, _run("completed", "success", "2026-10-10T16:00:00Z")],
                               date(2026, 10, 3)) is None
    assert runs.failed_attempt([bad], date(2026, 10, 10)) is None


def test_dispatch_is_not_needed_when_review_is_current():
    assert ensure.ensure({"intent_review": {"due": False}}, "", "",
                         datetime(2026, 10, 10, tzinfo=timezone.utc)) == "current"


def test_recent_attempt_prevents_duplicate_dispatch(monkeypatch):
    monkeypatch.setattr(runs, "fetch_runs", lambda token, repo: [_run("completed", "failure")])
    assert ensure.ensure({"intent_review": {"due": True}}, "fake", "org/repo",
                         datetime(2026, 10, 10, 16, tzinfo=timezone.utc)) == "already-attempted"


def test_runner_requires_real_named_lead_evidence(monkeypatch):
    class Response:
        def __enter__(self):
            return self
        def __exit__(self, *unused):
            return False
        def read(self):
            return b'{"choices":[{"message":{"content":"too short"}}]}'
    monkeypatch.setattr(review.urllib.request, "urlopen", lambda req, timeout: Response())
    with pytest.raises(ValueError, match="Incomplete"):
        review.model_review("mock context", "fake")
