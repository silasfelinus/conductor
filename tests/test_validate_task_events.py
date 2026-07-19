import importlib.util
import tempfile
import unittest
from pathlib import Path

import yaml


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_task_events.py"
SPEC = importlib.util.spec_from_file_location("validate_task_events", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class ValidateTaskEventsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "projects" / "demo").mkdir(parents=True)
        (self.root / "task-events").mkdir()
        (self.root / "projects" / "demo" / "roadmap.yaml").write_text(
            yaml.safe_dump(
                {
                    "project": "demo",
                    "kind": "software",
                    "tasks": [{"id": "t-001", "title": "First", "status": "ready"}],
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        MODULE.ROOT = self.root
        MODULE.EVENT_DIR = self.root / "task-events"

    def tearDown(self):
        self.temp.cleanup()

    def write_raw(self, name, text):
        path = self.root / "task-events" / name
        path.write_text(text, encoding="utf-8")
        return path

    def write_event(self, name, content):
        return self.write_raw(name, yaml.safe_dump(content, sort_keys=False))

    def test_no_files_is_ok(self):
        self.assertEqual(MODULE.main(), 0)

    def test_example_yaml_is_ignored(self):
        self.write_raw("example.yaml", "not: even: valid: yaml: here:")
        self.assertEqual(MODULE.main(), 0)

    def test_well_formed_event_is_valid(self):
        event = self.write_event(
            "claim.yaml",
            {"version": 1, "project": "demo", "task": "t-001", "operation": "claim"},
        )
        self.assertIsNone(MODULE.validate(event))
        self.assertEqual(MODULE.main(), 0)

    def test_syntax_error_is_caught(self):
        # conductor/t-067: an unquoted colon inside a free-text note field is
        # exactly the shape that broke the shared process-task-events CI job.
        path = self.write_raw(
            "bad-note.yaml",
            "version: 1\nproject: demo\ntask: t-001\noperation: claim\n"
            "note: fixed the bug: it was a race condition\n",
        )
        error = MODULE.validate(path)
        self.assertIsNotNone(error)
        self.assertIn("invalid YAML syntax", error)
        self.assertEqual(MODULE.main(), 1)

    def test_non_mapping_document_is_rejected(self):
        path = self.write_raw("list.yaml", "- one\n- two\n")
        error = MODULE.validate(path)
        self.assertIn("expected a YAML mapping", error)

    def test_unknown_operation_is_rejected(self):
        event = self.write_event(
            "bad-op.yaml",
            {"version": 1, "project": "demo", "task": "t-001", "operation": "launch-rocket"},
        )
        error = MODULE.validate(event)
        self.assertIn("unsupported operation", error)

    def test_unknown_project_is_rejected(self):
        event = self.write_event(
            "bad-project.yaml",
            {"version": 1, "project": "does-not-exist", "task": "t-001", "operation": "claim"},
        )
        error = MODULE.validate(event)
        self.assertIn("unknown project roadmap", error)

    def test_learning_on_non_closed_operation_is_rejected(self):
        event = self.write_event(
            "bad-learning-op.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "claim",
                "learning": {"kind": "software", "stakes": "reversible", "lesson": "x"},
            },
        )
        error = MODULE.validate(event)
        self.assertIn("learning may only accompany done or blocked", error)

    def test_learning_missing_required_field_is_rejected(self):
        event = self.write_event(
            "bad-learning-fields.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "done",
                "learning": {"kind": "software", "stakes": "reversible"},
            },
        )
        error = MODULE.validate(event)
        self.assertIn("learning is missing required fields", error)

    def test_empty_note_is_rejected(self):
        event = self.write_event(
            "blank-note.yaml",
            {"version": 1, "project": "demo", "task": "t-001", "operation": "claim", "note": "   "},
        )
        error = MODULE.validate(event)
        self.assertIn("note must be a non-empty string", error)

    def test_one_bad_file_does_not_hide_a_second_bad_file(self):
        self.write_raw("aaa-bad.yaml", "note: fixed: it\n")
        self.write_event(
            "zzz-bad.yaml",
            {"version": 1, "project": "demo", "task": "t-001", "operation": "not-a-real-op"},
        )
        self.assertEqual(MODULE.main(), 1)


if __name__ == "__main__":
    unittest.main()
