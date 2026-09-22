"""Shared assertion for daily-digest.yml's post-email failure-step contract.

test_daily_digest_resilience.py and test_daily_digest_schedule.py each independently
asserted that the block between the "Email via Brevo" step and the `creative-revision:`
job does not resurrect a Daily Dream sidecar failure into a failed digest run. Two
independent copies of the same policy assertion can silently drift apart if a future
change to daily-digest.yml only updates one file's copy — both passed at HEAD and only
conflicted once one side changed (conductor#4519, dream-cycle/t-031's kaizen origin).
Routing both tests through this one helper means the policy can only be changed in one
place, and a change that breaks the contract fails loudly in both files at once instead
of leaving one test silently asserting stale behavior.
"""

from pathlib import Path


def post_email_block(workflow_text: str) -> str:
    """The workflow text between the "Email via Brevo" step and the next job."""
    email_pos = workflow_text.index("      - name: Email via Brevo")
    creative_revision_pos = workflow_text.index("  creative-revision:", email_pos)
    return workflow_text[email_pos:creative_revision_pos]


def assert_no_post_email_failure_step(workflow_text: str) -> None:
    """The digest email delivery is never turned into a failed run after the fact.

    Daily Dream sidecar problems (author/build/verify) are recorded as warnings
    earlier in the workflow; nothing after "Email via Brevo" may re-check their
    outcomes and fail the job.
    """
    after_email = post_email_block(workflow_text)

    assert "Fail after digest if Daily Dream cycle failed" not in workflow_text
    assert "steps.daily_dream_author.outcome" not in after_email
    assert "steps.daily_dream_build.outcome" not in after_email
    assert 'exit "$failed"' not in after_email


def read_workflow(path: Path) -> str:
    return path.read_text(encoding="utf-8")
