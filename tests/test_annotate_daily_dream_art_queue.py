import json
from pathlib import Path

import scripts.annotate_daily_dream_art_queue as annotate


def asset(request_id="dream-cycle-example-world", status="queued", image_url=""):
    return {
        "key": "vibe",
        "title": "Example",
        "request_id": request_id,
        "art_status": status,
        "image_url": image_url,
    }


def test_pending_request_without_artjob_is_not_called_queued():
    result = annotate.annotate_asset(
        asset(),
        {"dream-cycle-example-world": {"id": "dream-cycle-example-world", "status": "pending"}},
    )
    assert result["art_status"] == "awaiting ArtJob"
    assert "art_job_id" not in result


def test_submitted_request_is_called_queued_and_carries_job_id():
    result = annotate.annotate_asset(
        asset(),
        {
            "dream-cycle-example-world": {
                "id": "dream-cycle-example-world",
                "status": "pending",
                "last_art_job_id": 8123,
            }
        },
    )
    assert result["art_status"] == "queued"
    assert result["art_job_id"] == 8123


def test_done_request_without_visible_image_reports_attachment_gap():
    result = annotate.annotate_asset(
        asset(),
        {"dream-cycle-example-world": {"id": "dream-cycle-example-world", "status": "done"}},
    )
    assert result["art_status"] == "rendered, awaiting attachment"


def test_ready_image_wins_over_stale_request_metadata():
    ready = asset(status="ready", image_url="https://example.test/image.webp")
    result = annotate.annotate_asset(ready, {})
    assert result == ready


def test_missing_staging_row_does_not_pretend_an_artjob_exists():
    result = annotate.annotate_asset(asset(), {})
    assert result["art_status"] == "queue metadata missing"


def test_unbuilt_proposal_stays_awaiting_build():
    unbuilt = asset(request_id="", status="awaiting build")
    result = annotate.annotate_asset(unbuilt, {})
    assert result["art_status"] == "awaiting build"


def test_cli_rewrites_digest_in_place(tmp_path):
    queue = tmp_path / "art-prompts.yaml"
    queue.write_text(
        "requests:\n"
        "- id: dream-cycle-vinehorn-world\n"
        "  status: pending\n"
        "  prompt: vines\n"
        "  image_path: world.webp\n",
        encoding="utf-8",
    )
    digest = tmp_path / "digest.json"
    digest.write_text(
        json.dumps(
            {
                "tomorrow_proposal": {
                    "assets": [asset(request_id="", status="awaiting build")]
                },
                "yesterday_output": {
                    "assets": [asset(request_id="dream-cycle-vinehorn-world")]
                },
            }
        ),
        encoding="utf-8",
    )

    assert annotate.main([str(digest), "--queue", str(queue)]) == 0
    result = json.loads(digest.read_text(encoding="utf-8"))
    assert result["tomorrow_proposal"]["assets"][0]["art_status"] == "awaiting build"
    assert result["yesterday_output"]["assets"][0]["art_status"] == "awaiting ArtJob"
