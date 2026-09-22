"""Workflow contract: Daily Dream failures may not swallow the digest email."""

from pathlib import Path

from tests.daily_digest_contract import assert_no_post_email_failure_step


WORKFLOW = (
    Path(__file__).resolve().parents[1] / ".github" / "workflows" / "daily-digest.yml"
)


def _step(text: str, name: str, next_name: str) -> str:
    start = text.index(f"      - name: {name}")
    end = text.index(f"      - name: {next_name}", start)
    return text[start:end]


def test_daily_dream_failures_are_recorded_without_blocking_digest_delivery():
    text = WORKFLOW.read_text(encoding="utf-8")

    author = _step(
        text,
        "Author today's next Daily Dream proposal",
        "Build the eligible Daily Dream proposal",
    )
    commit = _step(
        text,
        "Commit Daily Dream cycle evidence",
        "Verify Daily Dream cycle",
    )
    verify = _step(text, "Verify Daily Dream cycle", "Build digest JSON")

    assert "id: daily_dream_author" in author
    assert "continue-on-error: true" in author
    assert "id: daily_dream_commit" in commit
    assert "continue-on-error: true" in commit
    assert "::warning::" in verify
    assert "exit 1" not in verify


def test_daily_dream_sidecar_failure_is_not_restored_after_email_delivery():
    text = WORKFLOW.read_text(encoding="utf-8")
    assert_no_post_email_failure_step(text)
