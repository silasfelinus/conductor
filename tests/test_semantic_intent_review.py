"""The no-cost semantic workflow prepares evidence; only an agent may audit."""
from datetime import date, datetime, timezone
import json
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


def test_due_review_prepares_packet_and_never_authors_audit(tmp_path, monkeypatch):
    directory = tmp_path / "projects/conductor"
    directory.mkdir(parents=True)
    monkeypatch.setattr(review, "gather", lambda root: (
        "CONTROL.md\n" + "\n".join(review.LEADS) + "\n"
        + "projects/kind-pinball/roadmap.yaml\n" + "Evidence. " * 380
    ))
    result = review.prepare_brief(tmp_path, date(2026, 10, 13))
    assert result["status"] == "awaiting-agent"
    assert result["context_chars"] >= 3000
    packet = (tmp_path / "semantic-intent-brief.md").read_text()
    assert "NOT A COMPLETED AUDIT" in packet
    assert "roadmap-intent-auditor" in packet
    assert all(lead in packet for lead in review.LEADS)
    assert list(directory.glob("INTENT-AUDIT-*.md")) == []
    assert review.due(tmp_path, date(2026, 10, 13))


def test_current_report_skips_brief_without_collecting(tmp_path, monkeypatch):
    directory = tmp_path / "projects/conductor"
    directory.mkdir(parents=True)
    (directory / "INTENT-AUDIT-2026-10-12.md").write_text("manual audit")
    monkeypatch.setattr(review, "gather", lambda root: pytest.fail("should not gather"))
    result = review.prepare_brief(tmp_path, date(2026, 10, 13))
    assert result["status"] == "skipped"
    assert not (tmp_path / "semantic-intent-brief.md").exists()


def test_force_only_creates_packet_not_audit(tmp_path, monkeypatch):
    directory = tmp_path / "projects/conductor"
    directory.mkdir(parents=True)
    (directory / "INTENT-AUDIT-2026-10-13.md").write_text("existing audit")
    monkeypatch.setattr(review, "gather", lambda root: (
        "CONTROL.md " + " ".join(review.LEADS) + " X" * 1700))
    assert review.prepare_brief(tmp_path, date(2026, 10, 13), force=True)["status"] == "awaiting-agent"
    assert (directory / "INTENT-AUDIT-2026-10-13.md").read_text() == "existing audit"


def test_incomplete_source_context_fails_closed(tmp_path, monkeypatch):
    directory = tmp_path / "projects/conductor"
    directory.mkdir(parents=True)
    monkeypatch.setattr(review, "gather", lambda root: "too small")
    with pytest.raises(ValueError, match="Insufficient"):
        review.prepare_brief(tmp_path, date(2026, 10, 13))
    assert not (tmp_path / "semantic-intent-brief.md").exists()
    assert list(directory.iterdir()) == []


def test_no_paid_api_path_in_scheduled_workflow():
    workflow = (Path(__file__).resolve().parents[1] /
                ".github/workflows/semantic-intent-review.yml").read_text()
    script = Path(review.__file__).read_text()
    assert "ANTHROPIC_API_KEY" not in workflow
    assert "models.github.ai" not in workflow
    assert "api.anthropic.com" not in workflow
    assert "urlopen(" not in script
    assert "## Semantic intent review" in workflow


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
    monkeypatch.setattr(runs, "fetch_runs", lambda token, repo: [_run("completed", "success")])
    assert ensure.ensure({"intent_review": {"due": True}}, "fake", "org/repo",
                         datetime(2026, 10, 10, 16, tzinfo=timezone.utc)) == "already-attempted"
