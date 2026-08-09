import contextlib
import importlib.util
import io
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
                            "claimed_by": "sess-stale",
                            "claimed_at": "2026-07-01T00:00:00Z",
                        },
                        {
                            "id": "t-004",
                            "title": "Recurring with a lane counter",
                            "status": "review",
                            "owner": "worker",
                            "recurring": True,
                            "continuous_improvement": {
                                "last_lane": 2,
                                "next_lane": 3,
                                "last_run": "2026-08-01T00:00:00Z",
                                "last_pr": "silasfelinus/conductor#1",
                            },
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
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "claim",
                "session": "sess-A",
            },
        )

        result = MODULE.process(event, dry_run=False)

        task = self.roadmap()["tasks"][0]
        self.assertEqual(result, "demo/t-001: claim")
        self.assertEqual(task["status"], "claimed")
        self.assertEqual(task["owner"], "worker")
        self.assertEqual(task["claimed_by"], "sess-A")
        self.assertIn("claimed_at", task)
        self.assertFalse(event.exists())

    def test_claim_requires_session_field(self):
        # conductor/#1036: a claim with no session can't be told apart from a rival
        # concurrent claim, so the processor refuses it (surfaced for diagnosis).
        event = self.write_event(
            "sessionless-claim.yaml",
            {"version": 1, "project": "demo", "task": "t-001", "operation": "claim"},
        )

        with self.assertRaisesRegex(ValueError, "session"):
            MODULE.process(event, dry_run=False)

        self.assertTrue(event.exists())
        self.assertEqual(self.roadmap()["tasks"][0]["status"], "ready")

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

    def test_learning_lesson_with_colon_space_round_trips(self):
        """conductor/t-063: a lesson containing an embedded ': ' (e.g. a
        parenthetical like '(confirmed here: 9 minutes later)') must come back
        out of write_learning_record's yaml.safe_dump quoted/escaped so the
        committed file stays valid YAML -- LEARNING.yaml line 3164 broke
        test_committed_ledger_schema_conformance on every PR because that exact
        pattern was hand-appended as an unquoted plain scalar instead of going
        through this writer."""
        roadmap = self.roadmap()
        roadmap["tasks"][0]["status"] = "review"
        (self.root / "projects" / "demo" / "roadmap.yaml").write_text(
            yaml.safe_dump(roadmap, sort_keys=False), encoding="utf-8"
        )
        tricky_lesson = (
            "Compare against the branch's latest run of ANY status (confirmed "
            "here: 9 minutes later), not just the latest completed one."
        )
        payload = {
            "version": 1,
            "project": "demo",
            "task": "t-001",
            "operation": "done",
            "learning": {
                "kind": "software",
                "stakes": "reversible",
                "lesson": tricky_lesson,
            },
        }

        MODULE.process(self.write_event("done-colon.yaml", payload), dry_run=False)

        ledger_text = (self.root / "LEARNING.yaml").read_text(encoding="utf-8")
        ledger = yaml.safe_load(ledger_text)  # raises yaml.scanner.ScannerError if malformed
        self.assertEqual(ledger["records"][0]["lesson"], tricky_lesson)

    def test_bare_string_learning_is_coerced_not_rejected(self):
        # conductor/t-097: task-events/README.md's documented workflow is a direct
        # push to main, so validate_task_events.py's PR-time gate never runs for the
        # normal case -- a bare string `learning:` (the exact "learning: >-" folded
        # scalar shape hit at least 5 times in a week: interface-vision/t-065, t-073,
        # t-061, t-034) used to hard-fail the whole processor run instead of landing.
        roadmap = self.roadmap()
        roadmap["tasks"][0]["status"] = "review"
        roadmap["tasks"][0]["stakes"] = "reversible"
        (self.root / "projects" / "demo" / "roadmap.yaml").write_text(
            yaml.safe_dump(roadmap, sort_keys=False), encoding="utf-8"
        )
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

        result = MODULE.process(event, dry_run=False)

        self.assertEqual(result, "demo/t-001: done")
        self.assertFalse(event.exists())
        task = self.roadmap()["tasks"][0]
        self.assertEqual(task["status"], "done")
        ledger = yaml.safe_load((self.root / "LEARNING.yaml").read_text(encoding="utf-8"))
        record = ledger["records"][0]
        self.assertEqual(
            record["lesson"], "Small event files avoid whole-roadmap connector rewrites."
        )
        # Inferred from the demo roadmap's project-level kind and the task's own
        # stakes field, set above.
        self.assertEqual(record["kind"], "software")
        self.assertEqual(record["stakes"], "reversible")

    def test_bare_string_learning_with_invalid_kind_stakes_falls_back(self):
        # kindrobots-unraid/t-006 (2026-08-09): a project-level roadmap `kind` outside
        # the three learning-ledger kinds (e.g. "infrastructure") and a task `stakes`
        # outside the three valid values (e.g. "high", conflated with `priority: high`)
        # both used to fall through to `None`, which passes prepare_learning's own
        # required-fields check but violates
        # test_backfill_learning.test_committed_ledger_schema_conformance's "kind/stakes
        # are always a valid enum value" invariant -- redding the Python test suite on
        # `main`. Mirror backfill_learning.py's own precedent
        # (test_invalid_kind_stakes_fall_back): default to "software"/"reversible"
        # instead of null.
        roadmap = self.roadmap()
        roadmap["kind"] = "infrastructure"
        roadmap["tasks"][0]["status"] = "review"
        roadmap["tasks"][0]["stakes"] = "high"
        (self.root / "projects" / "demo" / "roadmap.yaml").write_text(
            yaml.safe_dump(roadmap, sort_keys=False), encoding="utf-8"
        )
        event = self.write_event(
            "string-learning-invalid.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "done",
                "learning": "Package for Unraid without baking secrets into the image.",
            },
        )

        result = MODULE.process(event, dry_run=False)

        self.assertEqual(result, "demo/t-001: done")
        ledger = yaml.safe_load((self.root / "LEARNING.yaml").read_text(encoding="utf-8"))
        record = ledger["records"][0]
        self.assertEqual(record["kind"], "software")
        self.assertEqual(record["stakes"], "reversible")

    def test_blank_string_learning_is_rejected(self):
        roadmap = self.roadmap()
        roadmap["tasks"][0]["status"] = "review"
        (self.root / "projects" / "demo" / "roadmap.yaml").write_text(
            yaml.safe_dump(roadmap, sort_keys=False), encoding="utf-8"
        )
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

        with self.assertRaisesRegex(ValueError, "non-empty string"):
            MODULE.process(event, dry_run=False)

        self.assertTrue(event.exists())

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

    def test_rearm_clears_claimed_by_and_claimed_at(self):
        # ai-art-academy/t-046: a rearm event previously left claimed_by/claimed_at
        # stale from the prior claim all the way through the next full cycle,
        # unlike every other rearm-to-ready convention in this codebase.
        event = self.write_event(
            "rearm-claim-fields.yaml",
            {"version": 1, "project": "demo", "task": "t-003", "operation": "rearm"},
        )

        MODULE.process(event, dry_run=False)

        task = self.roadmap()["tasks"][2]
        self.assertEqual(task["status"], "ready")
        self.assertNotIn("claimed_by", task)
        self.assertNotIn("claimed_at", task)

    def test_rearm_with_continuous_improvement_fields_bumps_counter(self):
        # conductor/t-103: a rearm event that names the lane just completed and its
        # merged PR should advance the nested continuous_improvement mapping the
        # same way scripts/bump_continuous_improvement.py's manual CLI does.
        event = self.write_event(
            "rearm-ci.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-004",
                "operation": "rearm",
                "continuous_improvement_lane": 4,
                "continuous_improvement_pr": "silasfelinus/conductor#1834",
            },
        )

        MODULE.process(event, dry_run=False)

        task = self.roadmap()["tasks"][3]
        self.assertEqual(task["status"], "ready")
        mapping = task["continuous_improvement"]
        self.assertEqual(mapping["last_lane"], 4)
        self.assertEqual(mapping["next_lane"], 1)
        self.assertEqual(mapping["last_pr"], "silasfelinus/conductor#1834")
        self.assertNotEqual(mapping["last_run"], "2026-08-01T00:00:00Z")

    def test_continuous_improvement_lane_without_pr_is_rejected(self):
        event = self.write_event(
            "ci-lane-only.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-004",
                "operation": "rearm",
                "continuous_improvement_lane": 4,
            },
        )

        with self.assertRaisesRegex(ValueError, "supplied together"):
            MODULE.process(event, dry_run=False)

        self.assertTrue(event.exists())
        task = self.roadmap()["tasks"][3]
        self.assertEqual(task["continuous_improvement"]["last_lane"], 2)

    def test_continuous_improvement_pr_without_lane_is_rejected(self):
        event = self.write_event(
            "ci-pr-only.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-004",
                "operation": "rearm",
                "continuous_improvement_pr": "silasfelinus/conductor#1834",
            },
        )

        with self.assertRaisesRegex(ValueError, "supplied together"):
            MODULE.process(event, dry_run=False)

        self.assertTrue(event.exists())

    def test_continuous_improvement_lane_out_of_range_is_rejected(self):
        event = self.write_event(
            "ci-lane-bad.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-004",
                "operation": "rearm",
                "continuous_improvement_lane": 5,
                "continuous_improvement_pr": "silasfelinus/conductor#1834",
            },
        )

        with self.assertRaisesRegex(ValueError, "1-4"):
            MODULE.process(event, dry_run=False)

        self.assertTrue(event.exists())

    def test_continuous_improvement_pr_bad_format_is_rejected(self):
        event = self.write_event(
            "ci-pr-bad.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-004",
                "operation": "rearm",
                "continuous_improvement_lane": 4,
                "continuous_improvement_pr": "not-a-pr-reference",
            },
        )

        with self.assertRaisesRegex(ValueError, "owner/repo#number"):
            MODULE.process(event, dry_run=False)

        self.assertTrue(event.exists())

    def test_continuous_improvement_fields_require_existing_mapping(self):
        # t-003 has recurring: True but no continuous_improvement mapping -- a task
        # that has never adopted the convention should fail loudly, not silently
        # invent a mapping with no history behind it.
        event = self.write_event(
            "ci-no-mapping.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-003",
                "operation": "rearm",
                "continuous_improvement_lane": 1,
                "continuous_improvement_pr": "silasfelinus/conductor#1834",
            },
        )

        with self.assertRaisesRegex(Exception, "continuous_improvement"):
            MODULE.process(event, dry_run=False)

        self.assertTrue(event.exists())

    def test_event_without_continuous_improvement_fields_leaves_mapping_untouched(self):
        event = self.write_event(
            "rearm-no-ci.yaml",
            {"version": 1, "project": "demo", "task": "t-004", "operation": "rearm"},
        )

        MODULE.process(event, dry_run=False)

        task = self.roadmap()["tasks"][3]
        self.assertEqual(task["status"], "ready")
        self.assertEqual(task["continuous_improvement"]["last_lane"], 2)
        self.assertEqual(task["continuous_improvement"]["last_pr"], "silasfelinus/conductor#1")

    def test_claim_rejects_non_ready_without_force(self):
        event = self.write_event(
            "bad-claim.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-002",
                "operation": "claim",
                "session": "sess-A",
            },
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
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "claim",
                "session": "sess-A",
            },
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
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "claim",
                "session": "sess-A",
            },
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
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "claim",
                "session": "sess-A",
            },
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

    def test_repeat_claim_same_session_is_a_true_noop_zero_diff(self):
        first = self.write_event(
            "claim.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "claim",
                "session": "sess-A",
            },
        )
        MODULE.process(first, dry_run=False)
        after_first = (self.root / "projects" / "demo" / "roadmap.yaml").read_text(encoding="utf-8")

        second = self.write_event(
            "claim-again.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "claim",
                "owner": "worker",
                "session": "sess-A",
            },
        )
        result = MODULE.process(second, dry_run=False)

        after_second = (self.root / "projects" / "demo" / "roadmap.yaml").read_text(encoding="utf-8")
        self.assertEqual(result, "demo/t-001: claim")
        self.assertEqual(after_first, after_second)
        self.assertFalse(second.exists())

    def test_different_session_claim_collides_and_is_consumed_without_mutation(self):
        # conductor/#1036: the crux. A second session claiming a task the first
        # session already holds must NOT collapse into an owner-level no-op --
        # that would let two rival Worker sessions both believe they own it. The
        # losing claim is consumed as ALREADY_CLAIMED with zero roadmap mutation.
        first = self.write_event(
            "claim.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "claim",
                "session": "sess-A",
            },
        )
        MODULE.process(first, dry_run=False)
        after_first = (self.root / "projects" / "demo" / "roadmap.yaml").read_text(encoding="utf-8")

        second = self.write_event(
            "rival-claim.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "claim",
                "session": "sess-B",
            },
        )
        result = MODULE.process(second, dry_run=False)

        after_second = (self.root / "projects" / "demo" / "roadmap.yaml").read_text(encoding="utf-8")
        self.assertIn("ALREADY_CLAIMED", result)
        # Winner (sess-A) still owns it; the losing claim changed nothing.
        self.assertEqual(after_first, after_second)
        self.assertEqual(self.roadmap()["tasks"][0]["claimed_by"], "sess-A")
        # Losing event is consumed (not a poison event), so the shared queue stays clean.
        self.assertFalse(second.exists())

    def test_collision_dry_run_leaves_losing_event_in_place(self):
        first = self.write_event(
            "claim.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "claim",
                "session": "sess-A",
            },
        )
        MODULE.process(first, dry_run=False)

        second = self.write_event(
            "rival-claim.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "claim",
                "session": "sess-B",
            },
        )
        result = MODULE.process(second, dry_run=True)

        self.assertIn("ALREADY_CLAIMED", result)
        self.assertTrue(second.exists())

    def test_later_done_from_non_owning_session_is_rejected_as_collision(self):
        # "later review/done event ownership checks": a session that lost the claim
        # must not be able to flip the winner's task to done just by queueing a
        # session-tagged done event.
        claim = self.write_event(
            "claim.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "claim",
                "session": "sess-A",
            },
        )
        MODULE.process(claim, dry_run=False)
        before = (self.root / "projects" / "demo" / "roadmap.yaml").read_text(encoding="utf-8")

        intruder_done = self.write_event(
            "done.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "done",
                "session": "sess-B",
            },
        )
        result = MODULE.process(intruder_done, dry_run=False)

        after = (self.root / "projects" / "demo" / "roadmap.yaml").read_text(encoding="utf-8")
        self.assertIn("ALREADY_CLAIMED", result)
        self.assertEqual(before, after)
        self.assertEqual(self.roadmap()["tasks"][0]["status"], "claimed")
        self.assertFalse(intruder_done.exists())

    def test_later_done_from_owning_session_applies(self):
        claim = self.write_event(
            "claim.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "claim",
                "session": "sess-A",
            },
        )
        MODULE.process(claim, dry_run=False)

        owner_done = self.write_event(
            "done.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "done",
                "session": "sess-A",
            },
        )
        result = MODULE.process(owner_done, dry_run=False)

        self.assertNotIn("ALREADY_CLAIMED", result)
        self.assertEqual(self.roadmap()["tasks"][0]["status"], "done")

    def test_sessionless_done_still_applies_backward_compatible(self):
        # Legacy path: a done event with no session skips the ownership check and
        # applies as before, so existing sessionless workflows keep working.
        claim = self.write_event(
            "claim.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "claim",
                "session": "sess-A",
            },
        )
        MODULE.process(claim, dry_run=False)

        legacy_done = self.write_event(
            "done.yaml",
            {"version": 1, "project": "demo", "task": "t-001", "operation": "done"},
        )
        MODULE.process(legacy_done, dry_run=False)

        self.assertEqual(self.roadmap()["tasks"][0]["status"], "done")

    def test_stale_event_is_skipped_and_does_not_revert_newer_claim(self):
        # conductor/t-067: a queued "review" event generated at 07:20 sat unapplied
        # for an hour behind a malformed sibling file. In the meantime the same
        # (recurring) task cycled through another claim at 08:18. Applying the old
        # event once it finally parsed must not silently revert that newer claim.
        roadmap = self.roadmap()
        roadmap["tasks"][0]["status"] = "claimed"
        roadmap["tasks"][0]["owner"] = "worker"
        roadmap["tasks"][0]["claimed_by"] = "claude-newer-session"
        roadmap["tasks"][0]["claimed_at"] = "2026-07-19T08:18:20Z"
        roadmap["tasks"][0]["updated"] = "2026-07-19T08:18:20Z"
        (self.root / "projects" / "demo" / "roadmap.yaml").write_text(
            yaml.safe_dump(roadmap, sort_keys=False), encoding="utf-8"
        )
        before = (self.root / "projects" / "demo" / "roadmap.yaml").read_text(encoding="utf-8")

        stale_event = self.write_event(
            "stale-review.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "review",
                "updated": "2026-07-19T07:20:00Z",
                "note": "Roadmap-accuracy lane: stale by the time it applied.",
            },
        )

        result = MODULE.process(stale_event, dry_run=False)

        after = (self.root / "projects" / "demo" / "roadmap.yaml").read_text(encoding="utf-8")
        self.assertIn("STALE", result)
        self.assertEqual(before, after)
        self.assertFalse(stale_event.exists())

    def test_stale_event_with_learning_payload_warns_on_stderr(self):
        # conductor/t-086: a stale event carrying a note/learning payload used to
        # vanish with no trace beyond the terse STALE skip line. A session should
        # not have to catch this by chance via a well-timed git fetch.
        roadmap = self.roadmap()
        roadmap["tasks"][0]["status"] = "claimed"
        roadmap["tasks"][0]["claimed_at"] = "2026-07-19T08:18:20Z"
        roadmap["tasks"][0]["updated"] = "2026-07-19T08:18:20Z"
        (self.root / "projects" / "demo" / "roadmap.yaml").write_text(
            yaml.safe_dump(roadmap, sort_keys=False), encoding="utf-8"
        )

        stale_event = self.write_event(
            "stale-review-with-note.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "review",
                "updated": "2026-07-19T07:20:00Z",
                "note": "Would have been lost silently.",
            },
        )

        captured = io.StringIO()
        with contextlib.redirect_stderr(captured):
            result = MODULE.process(stale_event, dry_run=False)

        self.assertIn("STALE", result)
        stderr_output = captured.getvalue()
        self.assertIn("WARNING", stderr_output)
        self.assertIn("demo/t-001", stderr_output)
        self.assertFalse(stale_event.exists())

    def test_stale_event_without_learning_payload_is_silent_on_stderr(self):
        roadmap = self.roadmap()
        roadmap["tasks"][0]["status"] = "claimed"
        roadmap["tasks"][0]["claimed_at"] = "2026-07-19T08:18:20Z"
        roadmap["tasks"][0]["updated"] = "2026-07-19T08:18:20Z"
        (self.root / "projects" / "demo" / "roadmap.yaml").write_text(
            yaml.safe_dump(roadmap, sort_keys=False), encoding="utf-8"
        )

        stale_event = self.write_event(
            "stale-review-no-note.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "review",
                "updated": "2026-07-19T07:20:00Z",
            },
        )

        captured = io.StringIO()
        with contextlib.redirect_stderr(captured):
            result = MODULE.process(stale_event, dry_run=False)

        self.assertIn("STALE", result)
        self.assertEqual(captured.getvalue(), "")

    def test_stale_event_dry_run_leaves_event_file_in_place(self):
        roadmap = self.roadmap()
        roadmap["tasks"][0]["status"] = "claimed"
        roadmap["tasks"][0]["claimed_at"] = "2026-07-19T08:18:20Z"
        (self.root / "projects" / "demo" / "roadmap.yaml").write_text(
            yaml.safe_dump(roadmap, sort_keys=False), encoding="utf-8"
        )

        stale_event = self.write_event(
            "stale-review.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "review",
                "updated": "2026-07-19T07:20:00Z",
            },
        )

        result = MODULE.process(stale_event, dry_run=True)

        self.assertIn("STALE", result)
        self.assertTrue(stale_event.exists())

    def test_event_without_updated_timestamp_is_never_flagged_stale(self):
        # No reference timestamp on the event means there's nothing to compare
        # against -- fall through to normal processing rather than guessing.
        roadmap = self.roadmap()
        roadmap["tasks"][0]["status"] = "claimed"
        roadmap["tasks"][0]["owner"] = "worker"
        roadmap["tasks"][0]["claimed_at"] = "2026-07-19T08:18:20Z"
        (self.root / "projects" / "demo" / "roadmap.yaml").write_text(
            yaml.safe_dump(roadmap, sort_keys=False), encoding="utf-8"
        )

        event = self.write_event(
            "no-timestamp-done.yaml",
            {"version": 1, "project": "demo", "task": "t-001", "operation": "done"},
        )

        result = MODULE.process(event, dry_run=False)

        self.assertNotIn("STALE", result)
        task = self.roadmap()["tasks"][0]
        self.assertEqual(task["status"], "done")

    def test_event_newer_than_task_state_applies_normally(self):
        # The ordinary flow: a session claims a task, then later queues a "done"
        # event with a fresher timestamp than the claim. Not stale.
        roadmap = self.roadmap()
        roadmap["tasks"][0]["status"] = "claimed"
        roadmap["tasks"][0]["owner"] = "worker"
        roadmap["tasks"][0]["claimed_at"] = "2026-07-19T07:00:00Z"
        roadmap["tasks"][0]["updated"] = "2026-07-19T07:00:00Z"
        (self.root / "projects" / "demo" / "roadmap.yaml").write_text(
            yaml.safe_dump(roadmap, sort_keys=False), encoding="utf-8"
        )

        event = self.write_event(
            "later-done.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "done",
                "updated": "2026-07-19T07:20:00Z",
            },
        )

        result = MODULE.process(event, dry_run=False)

        self.assertNotIn("STALE", result)
        task = self.roadmap()["tasks"][0]
        self.assertEqual(task["status"], "done")

    def test_main_applies_valid_events_even_when_an_earlier_one_fails(self):
        # "bad-claim" sorts before "good-claim" alphabetically, reproducing the
        # queue-head-of-line-blocking bug: a single unresolvable event must not
        # prevent later, valid events in the same batch from being applied.
        bad = self.write_event(
            "bad-claim.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-002",
                "operation": "claim",
                "session": "sess-A",
            },
        )
        good = self.write_event(
            "good-claim.yaml",
            {
                "version": 1,
                "project": "demo",
                "task": "t-001",
                "operation": "claim",
                "session": "sess-A",
            },
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
