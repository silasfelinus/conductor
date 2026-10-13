"""Scheduled semantic intent reviews must be real, opt-in, and fail closed."""
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


def test_missing_token_is_explicitly_waiting_for_opt_in(tmp_path):
    directory = tmp_path / "projects/conductor"
    directory.mkdir(parents=True)
    result = review.execute(tmp_path, date(2026, 10, 10), "")
    assert result["status"] == "awaiting-provider"
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
            return b'{"content":[{"type":"text","text":"too short"}]}'
    monkeypatch.setattr(review.urllib.request, "urlopen", lambda req, timeout: Response())
    with pytest.raises(ValueError, match="Incomplete"):
        review.model_review("mock context", "fake")


def _complete_review_text():
    return ("## Verified\n" + "\n".join(review.LEADS)
            + "\nCONTROL.md and projects/kind-pinball/roadmap.yaml\n"
            + "The tested implementation matches the documented portfolio direction. " * 12
            + "\n## Corrected\nNone.\n## Still questionable\nLive QA outstanding."
            + "\n## Next review\nIn three days.")


def test_model_retries_non_json_and_accepts_verified_response(monkeypatch):
    from io import BytesIO

    calls = []
    good = {"content": [{"type": "text", "text": _complete_review_text()}]}

    def urlopen(_request, timeout):
        calls.append(timeout)
        if len(calls) == 1:
            return BytesIO(b"")
        return BytesIO(__import__("json").dumps(good).encode())

    monkeypatch.setattr(review.urllib.request, "urlopen", urlopen)
    sleep = mock.Mock()
    monkeypatch.setattr(review.time, "sleep", sleep)
    assert "## Verified" in review.model_review("source context", "fake")
    assert calls == [120, 120]
    sleep.assert_called_once_with(2)


def test_model_retries_transient_http_error(monkeypatch):
    from io import BytesIO
    from urllib.error import HTTPError

    calls = []
    good = {"content": [{"type": "text", "text": _complete_review_text()}]}

    def urlopen(request, timeout):
        calls.append(timeout)
        if len(calls) == 1:
            raise HTTPError(review.API, 429, "Too Many Requests", {}, None)
        return BytesIO(__import__("json").dumps(good).encode())

    monkeypatch.setattr(review.urllib.request, "urlopen", urlopen)
    monkeypatch.setattr(review.time, "sleep", lambda _delay: None)
    assert "## Next review" in review.model_review("source context", "fake")
    assert len(calls) == 2


def test_model_does_not_retry_permanent_http_error(monkeypatch):
    from urllib.error import HTTPError

    calls = []
    def urlopen(request, timeout):
        calls.append(True)
        raise HTTPError(review.API, 403, "Forbidden", {}, None)

    monkeypatch.setattr(review.urllib.request, "urlopen", urlopen)
    monkeypatch.setattr(review.time, "sleep", lambda _delay: pytest.fail("should not sleep"))
    with pytest.raises(HTTPError) as exc:
        review.model_review("source context", "fake")
    assert exc.value.code == 403
    assert len(calls) == 1


def test_model_stops_after_three_invalid_responses(monkeypatch):
    from io import BytesIO

    calls = []
    def urlopen(request, timeout):
        calls.append(True)
        return BytesIO(b"not json")

    monkeypatch.setattr(review.urllib.request, "urlopen", urlopen)
    monkeypatch.setattr(review.time, "sleep", lambda _delay: None)
    with pytest.raises(__import__("json").JSONDecodeError):
        review.model_review("source context", "fake")
    assert len(calls) == 3


def test_anthropic_request_uses_messages_api_without_bearer_header(monkeypatch):
    from io import BytesIO
    import json

    observed = {}
    def urlopen(request, timeout):
        observed["url"] = request.full_url
        observed["headers"] = dict(request.header_items())
        observed["payload"] = json.loads(request.data)
        return BytesIO(json.dumps({
            "content": [{"type": "text", "text": _complete_review_text()}]
        }).encode())

    monkeypatch.setattr(review.urllib.request, "urlopen", urlopen)
    assert review.model_review("context", "fake-api-key").startswith("## Verified")
    assert observed["url"] == "https://api.anthropic.com/v1/messages"
    assert observed["payload"]["system"] == review.SYSTEM
    assert observed["payload"]["messages"] == [{"role": "user", "content": "context"}]
    assert observed["headers"]["X-api-key"] == "fake-api-key"
    assert not any(k.lower() == "authorization" for k in observed["headers"])


def test_missing_provider_does_not_collect_or_create_report(tmp_path, monkeypatch):
    directory = tmp_path / "projects/conductor"
    directory.mkdir(parents=True)
    monkeypatch.setattr(review, "gather", lambda _root: pytest.fail("no paid inference"))
    result = review.execute(tmp_path, date(2026, 10, 13), "")
    assert result["status"] == "awaiting-provider"
    assert not list(directory.iterdir())
