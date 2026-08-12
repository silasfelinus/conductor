import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "process_task_events.py"
SPEC = importlib.util.spec_from_file_location("process_task_events", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


def test_ready_clears_claim_and_stale_implementation_metadata():
    task = {
        "status": "review",
        "owner": "worker",
        "claimed_by": "sess-old",
        "claimed_at": "2026-08-09T12:00:00Z",
        "implementation_pr": "silasfelinus/kind_robots#1665",
    }
    ops = MODULE.compute_transition_ops(
        task,
        {"updated": "2026-08-09T13:00:00Z"},
        "ready",
    )

    assert ("unset", "owner", None) in ops
    assert ("unset", "claimed_by", None) in ops
    assert ("unset", "claimed_at", None) in ops
    assert ("unset", "implementation_pr", None) in ops


def test_ready_accepts_explicit_replacement_implementation_pr():
    task = {
        "status": "review",
        "owner": "worker",
        "claimed_by": "sess-old",
        "claimed_at": "2026-08-09T12:00:00Z",
        "implementation_pr": "silasfelinus/kind_robots#1665",
    }
    ops = MODULE.compute_transition_ops(
        task,
        {
            "updated": "2026-08-09T13:00:00Z",
            "implementation_pr": "silasfelinus/kind_robots#1667",
        },
        "ready",
    )

    assert ("set", "implementation_pr", "silasfelinus/kind_robots#1667") in ops
    assert ("unset", "implementation_pr", None) not in ops


def test_ready_rejects_malformed_implementation_pr():
    task = {"status": "review", "owner": "worker"}

    try:
        MODULE.compute_transition_ops(
            task,
            {"implementation_pr": "PR 1667"},
            "ready",
        )
    except ValueError as error:
        assert "implementation_pr" in str(error)
    else:
        raise AssertionError("malformed implementation_pr must be rejected")


def test_recurring_ready_preserves_implementation_pr_without_replacement():
    task = {
        "status": "review",
        "owner": "worker",
        "recurring": True,
        "implementation_pr": "silasfelinus/kind_robots#1665",
    }
    ops = MODULE.compute_transition_ops(task, {}, "ready")

    assert ("unset", "implementation_pr", None) not in ops
