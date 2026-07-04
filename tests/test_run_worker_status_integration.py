from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_WORKER = ROOT / "scripts" / "run_worker.py"


def _function_body(text: str, name: str, next_name: str) -> str:
    start = text.index(f"def {name}")
    end = text.index(f"def {next_name}", start)
    return text[start:end]


def test_claim_task_calls_lifecycle_helper():
    text = RUN_WORKER.read_text()
    body = _function_body(text, "claim_task", "set_task_status")

    assert "_run_worker_task_status" in body
    assert "claim" in body
    assert "write_roadmap" not in body


def test_set_task_status_calls_lifecycle_helper():
    text = RUN_WORKER.read_text()
    body = _function_body(text, "set_task_status", "_read")

    assert "_run_worker_task_status" in body
    assert "write_roadmap" not in body


def test_worker_script_has_no_full_roadmap_writer_function():
    text = RUN_WORKER.read_text()

    assert "def write_roadmap" not in text
