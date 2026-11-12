"""Read-only staging queue analysis cannot accidentally double-submit rerenders."""
from __future__ import annotations

import importlib.util
from pathlib import Path

import yaml

SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "projects/shifting-desks/art/check_request_queue.py"
)
SPEC = importlib.util.spec_from_file_location("shifting_desks_queue", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)

TARGET = "kind_robots public/images/shifting-desks/cards/wellness/sample.webp"


def seed(tmp_path, newer_status="requested", rows=None):
    folder = tmp_path / "art"
    folder.mkdir()
    for number in (13, 14, 15, 17):
        subjects = []
        if number in (13, 15):
            subjects = [{
                "key": "same-slot",
                "target_path": TARGET,
                "request_id": f"shifting-desks-r{number}-sample",
                "status": "delivered" if number == 13 else newer_status,
            }]
        (folder / f"ROUND-{number}.yaml").write_text(
            yaml.safe_dump({"subjects": subjects}), encoding="utf-8"
        )
    queue_path = tmp_path / "art-prompts.yaml"
    queue_path.write_text(
        yaml.safe_dump({"requests": rows or []}), encoding="utf-8"
    )
    return folder, queue_path


def test_latest_requested_row_overrides_older_delivered_art(tmp_path):
    folder, queue = seed(tmp_path, rows=[
        {"id": "shifting-desks-r13-sample", "status": "done"},
        {
            "id": "shifting-desks-r15-sample",
            "status": "pending",
            "image_path": TARGET.replace("kind_robots ", ""),
            "force": True,
            "priority": 35,
        },
    ])
    result = module.outstanding(folder, queue)
    assert result["outstanding"] == 1
    assert result["queued"] == 1
    assert result["missing_from_queue"] == 0
    row = result["requests"][0]
    assert row["round"] == 15
    assert row["queue_status"] == "pending"
    assert row["queue_force"] is True
    assert row["queue_path_matches"] is True


def test_missing_and_duplicate_requests_reported_without_mutation(tmp_path):
    folder, queue = seed(tmp_path)
    result = module.outstanding(folder, queue)
    assert result["outstanding"] == result["missing_from_queue"] == 1
    assert result["queued"] == 0
    before = queue.read_bytes()
    queue.write_text(yaml.safe_dump({"requests": [
        {"id": "shifting-desks-r15-sample", "status": "pending", "last_art_job_id": 123},
        {"id": "shifting-desks-r15-sample", "status": "pending", "last_art_job_id": 124},
    ]}), encoding="utf-8")
    second = module.outstanding(folder, queue)
    assert second["queued"] == 1
    assert second["duplicates"] == ["shifting-desks-r15-sample"]
    assert second["requests"][0]["queue_job_id"] == 124
    assert before != queue.read_bytes()


def test_delivered_latest_round_has_no_outstanding_job(tmp_path):
    folder, queue = seed(tmp_path, newer_status="delivered")
    result = module.outstanding(folder, queue)
    assert result["outstanding"] == 0
    assert result["requests"] == []
