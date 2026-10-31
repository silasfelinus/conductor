"""Adversarial safety checks for the four-job Hoshimori priority pilot."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from memory_dungeon_hoshimori_priority_pilot import (  # noqa: E402
    TARGET_PRIORITY, apply_changes, pilot_receipts, plan_changes,
)

RECEIPTS = pilot_receipts()


def jobs():
    return [
        {
            "id": job_id, "status": "PENDING", "priority": 0, "attempts": 0,
            "engine": "COMFY", "projectSlug": "memory-dungeon",
            "payload": {"conductorRequest": {
                "id": request_id, "imagePath": path,
                "targetRepo": "silasfelinus/kind_robots",
            }},
        }
        for job_id, (request_id, path) in sorted(RECEIPTS.items())
    ]


class HoshimoriPriorityPilotTests(unittest.TestCase):
    def test_exact_four_receipts_come_from_existing_ledgers(self):
        self.assertEqual(len(RECEIPTS), 4)
        self.assertEqual(set(RECEIPTS), {52108, 52109, 52234, 52235})
        self.assertEqual(TARGET_PRIORITY, 1)

    def test_only_four_pending_zero_priority_jobs_are_planned(self):
        planned, skipped = plan_changes(RECEIPTS, jobs())
        self.assertEqual(planned, sorted(RECEIPTS))
        self.assertEqual(skipped, {})

    def test_running_and_done_are_not_reprioritized(self):
        live = jobs()
        live[0]["status"] = "RUNNING"
        live[1]["status"] = "DONE"
        planned, skipped = plan_changes(RECEIPTS, live)
        self.assertEqual(planned, sorted(RECEIPTS)[2:])
        self.assertEqual(skipped[live[0]["id"]], "RUNNING")
        self.assertEqual(skipped[live[1]["id"]], "DONE")

    def test_idempotent_priority_and_higher_priority_are_preserved(self):
        live = jobs()
        live[0]["priority"] = 1
        live[1]["priority"] = 100
        planned, skipped = plan_changes(RECEIPTS, live)
        self.assertEqual(planned, sorted(RECEIPTS)[2:])
        self.assertEqual(len(skipped), 2)

    def test_missing_job_refuses_entire_batch(self):
        with self.assertRaisesRegex(ValueError, "missing live"):
            plan_changes(RECEIPTS, jobs()[1:])

    def test_duplicate_live_id_refuses_batch(self):
        live = jobs()
        live.append(deepcopy(live[0]))
        with self.assertRaisesRegex(ValueError, "duplicate live"):
            plan_changes(RECEIPTS, live)

    def test_forged_request_or_destination_refuses_batch(self):
        for field in ("id", "imagePath", "targetRepo"):
            with self.subTest(field=field):
                live = jobs()
                live[0]["payload"]["conductorRequest"][field] = "forged"
                with self.assertRaisesRegex(ValueError, "mismatched"):
                    plan_changes(RECEIPTS, live)

    def test_wrong_engine_or_project_refuses_batch(self):
        for field, value in (("engine", "A1111"), ("projectSlug", "other-game")):
            with self.subTest(field=field):
                live = jobs()
                live[0][field] = value
                with self.assertRaisesRegex(ValueError, "wrong project or engine"):
                    plan_changes(RECEIPTS, live)

    def test_exhausted_or_untrusted_attempts_refuse_batch(self):
        for value in (3, -1, None, "0", True):
            with self.subTest(attempts=value):
                live = jobs()
                live[0]["attempts"] = value
                with self.assertRaisesRegex(ValueError, "attempt budget"):
                    plan_changes(RECEIPTS, live)

    def test_failed_cancelled_or_unknown_state_refuses_batch(self):
        for status in ("FAILED", "CANCELLED", "RETRY", None):
            with self.subTest(status=status):
                live = jobs()
                live[0]["status"] = status
                with self.assertRaisesRegex(ValueError, "unsafe status"):
                    plan_changes(RECEIPTS, live)

    def test_negative_or_malformed_priority_refuses_batch(self):
        for priority in (-1, None, "0", True):
            with self.subTest(priority=priority):
                live = jobs()
                live[0]["priority"] = priority
                with self.assertRaisesRegex(ValueError, "priority"):
                    plan_changes(RECEIPTS, live)

    def test_successful_response_verifies_same_provenance_and_priority(self):
        row = jobs()[0]
        job_id = row["id"]
        def post(method, url, body):
            self.assertEqual(method, "POST")
            self.assertTrue(url.endswith(f"/api/art/queue/{job_id}/priority"))
            self.assertEqual(body, {"priority": 1})
            return 200, {"success": True, "data": {"job": {**row, "priority": 1}}}
        self.assertEqual(apply_changes(RECEIPTS, [job_id], post), [job_id])

    def test_mismatched_success_response_never_claims_applied(self):
        row = jobs()[0]
        for mutation in ({"id": 99}, {"priority": 0}, {"payload": {}}):
            with self.subTest(mutation=mutation):
                def post(method, url, body):
                    return 200, {"success": True, "data": {"job": {**row, **mutation}}}
                with self.assertRaisesRegex(RuntimeError, "response"):
                    apply_changes(RECEIPTS, [row["id"]], post)

    def test_conflict_or_http_error_is_not_treated_as_success(self):
        job_id = jobs()[0]["id"]
        for status in (409, 401, 500):
            with self.subTest(status=status):
                with self.assertRaises(RuntimeError):
                    apply_changes(RECEIPTS, [job_id], lambda *args: (status, {"success": False}))


if __name__ == "__main__":
    unittest.main()
