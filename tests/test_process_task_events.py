import importlib.util
import tempfile
import unittest
from pathlib import Path

import yaml


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "process_task_events.py"
SPEC = importlib.util.spec_from_file_location("process_task_events", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class TaskEventProcessorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "projects" / "demo").mkdir(parents=True)
        (self.root / "task-events").mkdir()
        (self.root / "scripts").mkdir()
        (self.root / "projects" / "demo" / "roadmap.yaml").write_text(
            yaml.safe_dump(
                {
                    "project": "demo",
                    "kind": "software",
                    "tasks": [
                        {"id": "t-001", "title": "First", "status": "ready"},
                        {
                            "id": "t-002",
                            "title": "Second",
                            "status": "waiting",
                            "depends_on": "t-001",
                        },
                        {
                            "id": "t-003",
                            "title": "Recurring",
                            "status": "claimed",
                            "owner": "worker",
                            "recurring": True,
                        },
                    ],
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        (self.root / "LEARNING.yaml").write_text("records: []\n", encoding="utf-8")
        MODULE.ROOT = self.root
        MODULE.EVENT_DIR = self.root / "task-events"

    def tearDown(self):
        self.temp.cleanup()

    def write_event(self, name, content):
        path = self.root / "task-events" / name
        path.write_text(yaml.safe_dump(content, sort_keys=False), encoding="utf-8")
        return path

    def roadmap(self):
        return yaml.safe_load(
            (self.root / "projects" / "demo" / "roadmap.yaml").read_text(encoding="utf-8")
        )

    def test_claim_consumes_event_and_sets_owner(self):
        event = self.write_event(
            "claim.yaml",
            {"version": 1, "project": "demo", "task": "t-001", "operation": "claim"},
        )

        result = MODULE.process(event, dry_run=False)

        task = self.roadmap()["tasks"][0]
        self.assertEqual(result, "demo/t-001: claim")
        self.assertEqual(task["status"], "claimed")
        self.assertEqual(task["owner"], "worker")
        self.assertFalse(event.exists())

    def test_done_appends_learning_once(self):
        roadmap = self.roadmap()
        roadmap["tasks"][0]["status"] = "review"
        (self.root / "projects" / "demo" / "roadmap.yaml").write_text(
            yaml.safe_dump(roadmap, sort_keys=False), encoding="utf-8"
        )
        payload = {
            "version": 1,
            "project": "demo",
            "task": "t-001",
            "operation": "done",
            "learning": {
                "kind": "software",
                "stakes": "reversible",
                "lesson": "Small event files avoid whole-roadmap connector rewrites.",
            },
        }

        MODULE.process(self.write_event("done.yaml", payload), dry_run=False)
        MODULE.process(self.write_event("done-again.yaml", payload), dry_run=False)

        task = self.roadmap()["tasks"][0]
        ledger = yaml.safe_load((self.root / "LEARNING.yaml").read_text(encoding="utf-8"))
        self.assertEqual(task["status"], "done")
        self.assertNotIn("owner", task)
        self.assertEqual(len(ledger["records"]), 1)

    def test_rearm_requires_recurring_task(self):
        event = self.write_event(
            "bad-rearm.yaml",
            {"version": 1, "project": "demo", "task": "t-001", "operation": "rearm"},
        )

        with self.assertRaisesRegex(ValueError, "recurring"):
            MODULE.process(event, dry_run=False)

        self.assertTrue(event.exists())

    def test_rearm_clears_owner(self):
        event = self.write_event(
            "rearm.yaml",
            {"version": 1, "project": "demo", "task": "t-003", "operation": "rearm"},
        )

        MODULE.process(event, dry_run=False)

        task = self.roadmap()["tasks"][2]
        self.assertEqual(task["status"], "ready")
        self.assertNotIn("owner", task)

    def test_claim_rejects_non_ready_without_force(self):
        event = self.write_event(
            "bad-claim.yaml",
            {"version": 1, "project": "demo", "task": "t-002", "operation": "claim"},
        )

        with self.assertRaisesRegex(ValueError, "requires status ready"):
            MODULE.process(event, dry_run=False)

        self.assertTrue(event.exists())


if __name__ == "__main__":
    unittest.main()
