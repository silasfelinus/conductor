"""PR validation must never evict queued Conductor task-event writers."""
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_task_event_processing_serializes_only_writers():
    doc = yaml.safe_load(
        (ROOT / ".github/workflows/process-task-events.yml").read_text(
            encoding="utf-8"
        )
    )
    assert "concurrency" not in doc, "workflow-level group allows PRs to starve writer"
    jobs = doc["jobs"]
    assert "concurrency" not in jobs["validate-pr"]
    assert jobs["process"]["concurrency"] == {
        "group": "conductor-task-events",
        "cancel-in-progress": False,
    }
