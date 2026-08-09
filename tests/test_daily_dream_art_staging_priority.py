from pathlib import Path

import scripts.consume_art_requests_to_media as media_consumer


ROOT = Path(__file__).resolve().parents[1]


def test_daily_dream_staging_uses_reserved_priority():
    assert media_consumer.submission_priority({"source": "dream-cycle"}) == (
        media_consumer.consumer.DAILY_DREAM_PRIORITY
    )
    assert media_consumer.submission_priority({"source": "dream-cycle"}) > 100


def test_daily_dream_requests_jump_ahead_of_older_generic_staging(monkeypatch):
    older_generic = {"id": "old-repair", "source": "kind-robots-missing-image"}
    older_explicit = {"id": "operator-urgent", "source": "manual", "priority": 50}
    dream_one = {"id": "dream-a", "source": "dream-cycle"}
    dream_two = {"id": "dream-b", "source": " Dream-Cycle "}
    newest_generic = {"id": "new-repair", "source": "kind-robots-missing-image"}
    entries = [older_generic, older_explicit, dream_one, dream_two, newest_generic]

    monkeypatch.setattr(media_consumer, "original_load_requests", lambda: entries)

    ordered = media_consumer.prioritized_load_requests()
    assert [entry["id"] for entry in ordered] == [
        "dream-a",
        "dream-b",
        "operator-urgent",
        "old-repair",
        "new-repair",
    ]


def test_staging_order_is_fifo_inside_equal_priority(monkeypatch):
    entries = [
        {"id": "first", "priority": 20},
        {"id": "second", "priority": 20},
        {"id": "third", "priority": 20},
    ]
    monkeypatch.setattr(media_consumer, "original_load_requests", lambda: entries)
    assert [entry["id"] for entry in media_consumer.prioritized_load_requests()] == [
        "first",
        "second",
        "third",
    ]


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
