import importlib.util
from pathlib import Path
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "process_task_events.py"
SPEC = importlib.util.spec_from_file_location("process_task_events_human_approval", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class HumanApprovalTaskEventTests(unittest.TestCase):
    def test_done_event_can_record_human_approval(self):
        ops = MODULE.compute_transition_ops(
            {
                "id": "t-001",
                "status": "needs-human",
                "gate_human": True,
                "approved_by_human": False,
            },
            {
                "operation": "done",
                "approved_by_human": True,
                "updated": "2026-08-03T02:30:00Z",
            },
            "done",
        )

        self.assertIn(("set", "status", "done"), ops)
        self.assertIn(("set", "approved_by_human", "true"), ops)
        self.assertIn(("unset", "soft_gate", None), ops)

    def test_ready_event_can_record_human_rejection(self):
        ops = MODULE.compute_transition_ops(
            {
                "id": "t-001",
                "status": "needs-human",
                "gate_human": True,
                "approved_by_human": True,
            },
            {
                "operation": "ready",
                "approved_by_human": False,
                "updated": "2026-08-03T02:31:00Z",
                "note": "Please revise the rollout plan.",
            },
            "ready",
        )

        self.assertIn(("set", "status", "ready"), ops)
        self.assertIn(("set", "approved_by_human", "false"), ops)
        self.assertIn(("set", "note", "Please revise the rollout plan."), ops)

    def test_event_without_approval_flag_does_not_change_approval(self):
        ops = MODULE.compute_transition_ops(
            {"id": "t-001", "status": "needs-human"},
            {
                "operation": "needs-human",
                "soft_gate": True,
                "updated": "2026-08-03T02:31:30Z",
                "note": "Human left a comment without deciding the gate.",
            },
            "needs-human",
        )

        self.assertFalse(
            any(field == "approved_by_human" for _, field, _ in ops),
            "comment-only events must not manufacture a human decision",
        )

    def test_approval_flag_must_be_boolean(self):
        with self.assertRaisesRegex(ValueError, "must be a boolean"):
            MODULE.compute_transition_ops(
                {"id": "t-001", "status": "needs-human"},
                {
                    "operation": "done",
                    "approved_by_human": "true",
                    "updated": "2026-08-03T02:32:00Z",
                },
                "done",
            )


if __name__ == "__main__":
    unittest.main()
