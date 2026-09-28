import json
import os
import subprocess
import sys
from pathlib import Path

import scripts.annotate_daily_dream_art_queue as annotate

ROOT = Path(__file__).resolve().parents[1]


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


def test_live_done_artjob_overrides_pending_staging_metadata():
    result = annotate.annotate_asset(
        asset(),
        {
            "dream-cycle-example-world": {
                "id": "dream-cycle-example-world",
                "status": "pending",
                "last_art_job_id": 8123,
            }
        },
        fetch_job=lambda job_id: {
            "id": job_id,
            "status": "DONE",
            "artImageId": 9123,
        },
    )
    assert result["art_status"] == "rendered, awaiting public image"
    assert result["art_job_id"] == 8123
    assert result["art_image_id"] == 9123


def test_live_running_artjob_is_not_flattened_to_generic_queued():
    result = annotate.annotate_asset(
        asset(),
        {
            "dream-cycle-example-world": {
                "id": "dream-cycle-example-world",
                "status": "pending",
                "last_art_job_id": 8123,
            }
        },
        fetch_job=lambda _job_id: {"status": "RUNNING"},
    )
    assert result["art_status"] == "rendering"


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


def test_cli_rewrites_current_and_previous_outputs_in_place(tmp_path, monkeypatch):
    # conductor/t-198: main() wires _live_job_fetcher() with no CLI override, and
    # that fetcher checks os.environ["KR_API_TOKEN"] to decide whether to make a
    # real network call. Whether that check even gets a chance to fire also
    # depends on `import consume_art_requests` succeeding, which is only true
    # once some *other* test file's `sys.path.insert(0, .../scripts)` has run in
    # the same process -- true in full-suite collection order, false running
    # this file alone. In an environment where KR_API_TOKEN is genuinely set
    # (this sandbox always has it), that combination makes this assertion
    # depend on a real Kind Robots API response for job 8123, deterministically
    # in full-suite runs, never in isolation. Clearing it here makes the test
    # hermetic regardless of both the ambient token and collection order.
    monkeypatch.delenv("KR_API_TOKEN", raising=False)
    queue = tmp_path / "art-prompts.yaml"
    queue.write_text(
        "requests:\n"
        "- id: dream-cycle-current-world\n"
        "  status: pending\n"
        "  last_art_job_id: 8123\n"
        "  prompt: current\n"
        "  image_path: current.webp\n"
        "- id: dream-cycle-previous-world\n"
        "  status: pending\n"
        "  prompt: previous\n"
        "  image_path: previous.webp\n",
        encoding="utf-8",
    )
    digest = tmp_path / "digest.json"
    digest.write_text(
        json.dumps(
            {
                "current_dream_output": {
                    "assets": [asset(request_id="dream-cycle-current-world")]
                },
                "previous_dream_output": {
                    "assets": [asset(request_id="dream-cycle-previous-world")]
                },
                "next_dream_proposal": {
                    "assets": [asset(request_id="", status="awaiting build")]
                },
            }
        ),
        encoding="utf-8",
    )

    assert annotate.main([str(digest), "--queue", str(queue)]) == 0
    result = json.loads(digest.read_text(encoding="utf-8"))
    current = result["current_dream_output"]["assets"][0]
    previous = result["previous_dream_output"]["assets"][0]
    assert current["art_status"] == "queued"
    assert current["art_job_id"] == 8123
    assert previous["art_status"] == "awaiting ArtJob"
    assert result["next_dream_proposal"]["assets"][0]["art_status"] == "awaiting build"


def test_live_job_fetcher_resolves_with_only_repo_root_on_sys_path():
    # conductor/t-199: _live_job_fetcher() used to do a bare `import
    # consume_art_requests`, which only succeeds when scripts/ itself (not just
    # the repo root) is already on sys.path -- true in a full pytest run because
    # other test files each insert scripts/ at collection time, false in a fresh
    # interpreter that only has the repo root on sys.path (the guarantee pytest
    # and `python3 scripts/foo.py` both actually provide). Run in a subprocess
    # with PYTHONPATH unset and cwd=ROOT so sys.path starts with only the repo
    # root, confirming the fixed dual-path import still resolves the real
    # fetcher rather than silently degrading to None.
    script = (
        "from scripts.annotate_daily_dream_art_queue import _live_job_fetcher\n"
        "from scripts import consume_art_requests as expected\n"
        "fetcher = _live_job_fetcher()\n"
        "assert fetcher is not None, 'expected a real fetcher, got None'\n"
        "assert fetcher is expected.fetch_job, 'resolved the wrong fetch_job'\n"
        "print('OK')\n"
    )
    env = {"PATH": os.environ.get("PATH", ""), "KR_API_TOKEN": "fake-token-for-test"}
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=str(ROOT),
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "OK"
