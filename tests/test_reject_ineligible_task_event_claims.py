import importlib.util
import tempfile
import unittest
from pathlib import Path

import yaml


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "reject_ineligible_task_event_claims.py"
SPEC = importlib.util.spec_from_file_location("reject_ineligible_task_event_claims", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class DependencyClaimGuardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "projects" / "demo").mkdir(parents=True)
        (self.root / "task-events").mkdir()
        MODULE.ROOT = self.root
        MODULE.EVENT_DIR = self.root / "task-events"

    def tearDown(self):
        self.temp.cleanup()

    def write_roadmap(self, parent):
        roadmap = {
            "project": "demo",
            "kind": "software",
            "tasks": [
                {"id": "t-parent", "title": "Parent", **parent},
                {
                    "id": "t-child",
                    "title": "Child",
                    "status": "ready",
                    "depends_on": "t-parent",
                },
            ],
        }
        path = self.root / "projects" / "demo" / "roadmap.yaml"
        path.write_text(yaml.safe_dump(roadmap, sort_keys=False), encoding="utf-8")
        return path

    def write_claim(self):
        path = self.root / "task-events" / "claim.yaml"
        path.write_text(
            yaml.safe_dump(
                {
                    "version": 1,
                    "project": "demo",
                    "task": "t-child",
                    "operation": "claim",
                    "owner": "worker",
                    "session": "openai-scheduled-test-child-a1b2",
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        return path

    def test_unfinished_dependency_consumes_claim_without_roadmap_mutation(self):
        roadmap_path = self.write_roadmap({"status": "ready"})
        before = roadmap_path.read_text(encoding="utf-8")
        event = self.write_claim()

        result = MODULE.process_event(event)

        self.assertIn("DEPENDENCY_BLOCKED", result)
        self.assertIn("status='ready'", result)
        self.assertFalse(event.exists())
        self.assertEqual(roadmap_path.read_text(encoding="utf-8"), before)

    def test_claim_is_left_for_processor_once_dependency_is_done(self):
        self.write_roadmap({"status": "done"})
        event = self.write_claim()

        result = MODULE.process_event(event)

        self.assertIsNone(result)
        self.assertTrue(event.exists())

    def test_done_human_gated_dependency_still_requires_approval(self):
        roadmap_path = self.write_roadmap(
            {"status": "done", "gate_human": True, "approved_by_human": False}
        )
        before = roadmap_path.read_text(encoding="utf-8")
        event = self.write_claim()

        result = MODULE.process_event(event)

        self.assertIn("human approval missing", result)
        self.assertFalse(event.exists())
        self.assertEqual(roadmap_path.read_text(encoding="utf-8"), before)


if __name__ == "__main__":
    unittest.main()
