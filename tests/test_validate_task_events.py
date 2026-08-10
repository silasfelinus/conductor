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
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "claim",
                "session": "sess-A",
            },
        )
        self.assertIsNone(MODULE.validate(event))
        self.assertEqual(MODULE.main(), 0)

    def test_claim_without_session_is_rejected(self):
        # conductor/#1036: a claim event MUST name its session so the processor
        # can distinguish two concurrent Worker claims from a single idempotent one.
        event = self.write_event(
            "sessionless-claim.yaml",
            {"version": 1, "project": "demo", "task": "t-001", "operation": "claim"},
        )
        error = MODULE.validate(event)
        self.assertIn("session", error)
        self.assertEqual(MODULE.main(), 1)

    def test_claim_with_blank_session_is_rejected(self):
        event = self.write_event(
            "blank-session.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "claim",
                "session": "   ",
            },
        )
        error = MODULE.validate(event)
        self.assertIn("session", error)

    def test_blank_session_on_non_claim_event_is_rejected(self):
        event = self.write_event(
            "blank-session-done.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "done",
                "session": "",
            },
        )
        error = MODULE.validate(event)
        self.assertIn("session", error)

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
            {
                "version": 1,
                "project": "does-not-exist",
                "task": "t-001",
                "operation": "claim",
                "session": "sess-A",
            },
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
                "session": "sess-A",
                "learning": {"kind": "software", "stakes": "reversible", "lesson": "x"},
            },
        )
        error = MODULE.validate(event)
        self.assertIn("learning may only accompany done or blocked", error)

    def test_learning_rejected_on_every_non_closed_operation(self):
        # conductor/t-101: the 2026-08-05 stuck-event incident (a queued `rearm`
        # for ai-art-academy/t-010 carrying a `learning:` field) was this exact
        # rejection, just on an operation the prior test above never exercised.
        # ALLOWED_OPERATIONS minus CLOSED_OPERATIONS ({done, blocked}) is
        # {claim, ready, review, needs-human, rearm} -- cover all five so a future
        # operation added to ALLOWED_OPERATIONS without a matching test here would
        # still be caught the moment someone tries `learning:` on it.
        non_closed = MODULE.ALLOWED_OPERATIONS - MODULE.CLOSED_OPERATIONS
        self.assertEqual(non_closed, {"claim", "ready", "review", "needs-human", "rearm"})
        for operation in sorted(non_closed):
            with self.subTest(operation=operation):
                event_body = {
                    "version": 1,
                    "project": "demo",
                    "task": "t-001",
                    "operation": operation,
                    "learning": {"kind": "software", "stakes": "reversible", "lesson": "x"},
                }
                if operation == "claim":
                    event_body["session"] = "sess-A"
                event = self.write_event(f"bad-learning-{operation}.yaml", event_body)
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

    def test_bare_string_learning_is_accepted(self):
        # conductor/t-097: matches process_task_events.py's prepare_learning()
        # coercion for the same shape -- the PR-time gate must not reject what the
        # processor will happily accept.
        event = self.write_event(
            "string-learning.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "done",
                "learning": "Small event files avoid whole-roadmap connector rewrites.",
            },
        )
        error = MODULE.validate(event)
        self.assertIsNone(error)

    def test_blank_string_learning_is_rejected(self):
        event = self.write_event(
            "blank-string-learning.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "done",
                "learning": "   ",
            },
        )
        error = MODULE.validate(event)
        self.assertIn("non-empty string", error)

    def test_empty_note_is_rejected(self):
        event = self.write_event(
            "blank-note.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "claim",
                "session": "sess-A",
                "note": "   ",
            },
        )
        error = MODULE.validate(event)
        self.assertIn("note must be a non-empty string", error)

    def test_verify_pr_well_formed_is_accepted(self):
        event = self.write_event(
            "verify-pr-ok.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "done",
                "verify_pr": "silasfelinus/kind_robots#1718",
            },
        )
        self.assertIsNone(MODULE.validate(event))

    def test_verify_pr_bad_format_is_rejected(self):
        event = self.write_event(
            "verify-pr-bad.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "done",
                "verify_pr": "not-a-pr-reference",
            },
        )
        error = MODULE.validate(event)
        self.assertIn("owner/repo#number", error)

    def test_one_bad_file_does_not_hide_a_second_bad_file(self):
        self.write_raw("aaa-bad.yaml", "note: fixed: it\n")
        self.write_event(
            "zzz-bad.yaml",
            {"version": 1, "project": "demo", "task": "t-001", "operation": "not-a-real-op"},
        )
        self.assertEqual(MODULE.main(), 1)


if __name__ == "__main__":
    unittest.main()
