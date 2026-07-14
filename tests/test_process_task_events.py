import importlib.util
import sys
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

    def test_claim_event_leaves_unrelated_roadmap_bytes_untouched(self):
        # Regression for conductor/challenge-center t-020: a one-task claim used to
        # reserialize the whole file via yaml.safe_dump (escaped Unicode, reformatted
        # quote/block styles, hundreds of unrelated changed lines).
        before = (self.root / "projects" / "demo" / "roadmap.yaml").read_text(encoding="utf-8")
        event = self.write_event(
            "claim.yaml",
            {"version": 1, "project": "demo", "task": "t-001", "operation": "claim"},
        )

        MODULE.process(event, dry_run=False)

        after = (self.root / "projects" / "demo" / "roadmap.yaml").read_text(encoding="utf-8")

        def tail_from_t002(text):
            lines = text.splitlines()
            start = next(i for i, line in enumerate(lines) if line.strip() == "- id: t-002")
            return lines[start:]

        # t-001 gained lines (new owner/updated fields), but t-002/t-003 -- entirely
        # unrelated tasks -- must be byte-identical regardless of where they now sit.
        self.assertEqual(tail_from_t002(after), tail_from_t002(before))

    def test_note_unicode_survives_process_unescaped(self):
        event = self.write_event(
            "claim.yaml",
            {"version": 1, "project": "demo", "task": "t-001", "operation": "claim"},
        )
        MODULE.process(event, dry_run=False)
        done_event = self.write_event(
            "done.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "done",
                "note": "Closed — verified the → path end to end.",
            },
        )

        MODULE.process(done_event, dry_run=False)

        text = (self.root / "projects" / "demo" / "roadmap.yaml").read_text(encoding="utf-8")
        self.assertIn("—", text)
        self.assertIn("→", text)
        self.assertNotIn("\\u2014", text)
        self.assertNotIn("\\u2192", text)

    def test_multiline_note_is_appended_as_literal_block_not_flattened(self):
        claim = self.write_event(
            "claim.yaml",
            {"version": 1, "project": "demo", "task": "t-001", "operation": "claim"},
        )
        MODULE.process(claim, dry_run=False)
        done_event = self.write_event(
            "done.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "done",
                "note": "Paragraph one.\n\nParagraph two.",
            },
        )

        MODULE.process(done_event, dry_run=False)

        task = self.roadmap()["tasks"][0]
        self.assertEqual(task["note"], "Paragraph one.\n\nParagraph two.")
        text = (self.root / "projects" / "demo" / "roadmap.yaml").read_text(encoding="utf-8")
        self.assertIn("note: |-", text)

    def test_invalid_learning_payload_leaves_roadmap_and_event_untouched(self):
        # Atomicity: a bad `learning` block must not leave an already-applied,
        # now-unrepeatable status transition stranded with its event undeleted.
        before = (self.root / "projects" / "demo" / "roadmap.yaml").read_text(encoding="utf-8")
        roadmap = self.roadmap()
        roadmap["tasks"][0]["status"] = "review"
        (self.root / "projects" / "demo" / "roadmap.yaml").write_text(
            yaml.safe_dump(roadmap, sort_keys=False), encoding="utf-8"
        )
        before = (self.root / "projects" / "demo" / "roadmap.yaml").read_text(encoding="utf-8")

        event = self.write_event(
            "bad-learning.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "done",
                # Missing required "lesson" field.
                "learning": {"kind": "software", "stakes": "reversible"},
            },
        )

        with self.assertRaisesRegex(ValueError, "missing required fields"):
            MODULE.process(event, dry_run=False)

        after = (self.root / "projects" / "demo" / "roadmap.yaml").read_text(encoding="utf-8")
        self.assertEqual(before, after)
        self.assertTrue(event.exists())
        ledger = yaml.safe_load((self.root / "LEARNING.yaml").read_text(encoding="utf-8"))
        self.assertEqual(ledger["records"], [])

    def test_repeat_claim_same_owner_is_a_true_noop_zero_diff(self):
        first = self.write_event(
            "claim.yaml",
            {"version": 1, "project": "demo", "task": "t-001", "operation": "claim"},
        )
        MODULE.process(first, dry_run=False)
        after_first = (self.root / "projects" / "demo" / "roadmap.yaml").read_text(encoding="utf-8")

        second = self.write_event(
            "claim-again.yaml",
            {"version": 1, "project": "demo", "task": "t-001", "operation": "claim", "owner": "worker"},
        )
        MODULE.process(second, dry_run=False)

        after_second = (self.root / "projects" / "demo" / "roadmap.yaml").read_text(encoding="utf-8")
        self.assertEqual(after_first, after_second)
        self.assertFalse(second.exists())

    def test_main_applies_valid_events_even_when_an_earlier_one_fails(self):
        # "bad-claim" sorts before "good-claim" alphabetically, reproducing the
        # queue-head-of-line-blocking bug: a single unresolvable event must not
        # prevent later, valid events in the same batch from being applied.
        bad = self.write_event(
            "bad-claim.yaml",
            {"version": 1, "project": "demo", "task": "t-002", "operation": "claim"},
        )
        good = self.write_event(
            "good-claim.yaml",
            {"version": 1, "project": "demo", "task": "t-001", "operation": "claim"},
        )

        original_resolver = MODULE.run_resolver
        original_argv = sys.argv
        MODULE.run_resolver = lambda dry_run: None
        sys.argv = ["process_task_events.py"]
        try:
            exit_code = MODULE.main()
        finally:
            MODULE.run_resolver = original_resolver
            sys.argv = original_argv

        self.assertEqual(exit_code, 1)
        self.assertTrue(bad.exists(), "unresolvable event stays for diagnosis")
        self.assertFalse(good.exists(), "valid event must still be consumed")
        task = self.roadmap()["tasks"][0]
        self.assertEqual(task["status"], "claimed")
        self.assertEqual(task["owner"], "worker")


if __name__ == "__main__":
    unittest.main()
