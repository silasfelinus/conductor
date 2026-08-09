from pathlib import Path

import scripts.art_request_staging_priority as staging


ROOT = Path(__file__).resolve().parents[1]
DAILY_DREAM_PRIORITY = 200


def test_daily_dream_staging_uses_reserved_priority():
    assert staging.submission_priority(
        {"source": "dream-cycle"},
        daily_dream_priority=DAILY_DREAM_PRIORITY,
    ) == DAILY_DREAM_PRIORITY
    assert DAILY_DREAM_PRIORITY > 100


def test_daily_dream_requests_jump_ahead_of_older_generic_staging():
    older_generic = {"id": "old-repair", "source": "kind-robots-missing-image"}
    older_explicit = {"id": "operator-urgent", "source": "manual", "priority": 50}
    dream_one = {"id": "dream-a", "source": "dream-cycle"}
    dream_two = {"id": "dream-b", "source": " Dream-Cycle "}
    newest_generic = {"id": "new-repair", "source": "kind-robots-missing-image"}
    entries = [older_generic, older_explicit, dream_one, dream_two, newest_generic]

    ordered = staging.prioritize_requests(
        entries,
        daily_dream_priority=DAILY_DREAM_PRIORITY,
    )
    assert [entry["id"] for entry in ordered] == [
        "dream-a",
        "dream-b",
        "operator-urgent",
        "old-repair",
        "new-repair",
    ]


def test_staging_order_is_fifo_inside_equal_priority():
    entries = [
        {"id": "first", "priority": 20},
        {"id": "second", "priority": 20},
        {"id": "third", "priority": 20},
    ]
    ordered = staging.prioritize_requests(
        entries,
        daily_dream_priority=DAILY_DREAM_PRIORITY,
    )
    assert [entry["id"] for entry in ordered] == ["first", "second", "third"]


def test_submitted_daily_dream_waits_for_relay_instead_of_reposting():
    entry = {
        "source": "dream-cycle",
        "last_art_job_id": 8123,
    }
    assert staging.should_consume_after_submission(entry, already_satisfied=False) is False
    assert staging.should_consume_after_submission(entry, already_satisfied=True) is True


def test_unsubmitted_daily_dream_and_generic_requests_still_consume():
    assert staging.should_consume_after_submission(
        {"source": "dream-cycle"}, already_satisfied=False
    ) is True
    assert staging.should_consume_after_submission(
        {"source": "kind-robots-missing-image", "last_art_job_id": 99},
        already_satisfied=False,
    ) is True


def test_auto_art_runs_request_lane_before_project_art_lane():
    workflow = (ROOT / ".github" / "workflows" / "auto-art-generate.yml").read_text(
        encoding="utf-8"
    )
    request_step = workflow.index("- name: Submit + wait + verify art requests")
    project_step = workflow.index("- name: Submit + wait + verify project-art results")
    assert request_step < project_step


def test_auto_art_retriggers_when_request_staging_logic_changes():
    workflow = (ROOT / ".github" / "workflows" / "auto-art-generate.yml").read_text(
        encoding="utf-8"
    )
    assert '      - "scripts/consume_art_requests_to_media.py"' in workflow
