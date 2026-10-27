"""No-network contracts for safe resubmission of Prom of Doom's 144 outcome plates."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import submit_prom_personal_outcomes as submit  # noqa: E402
import enqueue_art_requests as enq  # noqa: E402
from repair_negation_art_prompts import violations  # noqa: E402


class PromArtSubmitTests(unittest.TestCase):
    def test_all_144_cells_are_unique_and_safe(self):
        ledger = submit.parse_ledger()
        self.assertEqual(len(ledger["subjects"]), 144)
        self.assertEqual(
            sorted(set(x["asset"].split("/")[-1] for x in ledger["subjects"])),
            ["hero", "student", "villain"],
        )
        self.assertEqual(len(set(x["seed"] for x in ledger["subjects"])), 144)
        self.assertEqual(len(set(x["asset"] for x in ledger["subjects"])), 144)
        for subject in ledger["subjects"]:
            prompt = enq.compose_prompt(ledger["lanes"][0], subject)
            self.assertTrue(prompt.strip(), subject["key"])
            self.assertFalse(violations(prompt), subject["key"])

    def test_recovers_previous_artjob_before_posting(self):
        ledger = submit.parse_ledger()
        first = ledger["subjects"][0]
        prompt = enq.compose_prompt(ledger["lanes"][0], first)
        existing = [{"id": 41623, "projectSlug": "comet-city-academy", "payload": {"promptString": prompt}}]
        self.assertEqual(submit.recover_submitted(ledger, existing), 1)
        self.assertEqual(first["jobs"]["krea2"], 41623)
        self.assertEqual(submit.recover_submitted(ledger, existing), 0)

    def test_rejects_incomplete_remote_pages(self):
        def missing(method, url):
            self.assertEqual(method, "GET")
            return 200, {"success": True, "data": {"jobs": [], "pagination": {"totalCount": 1, "hasNextPage": False}}}
        with self.assertRaisesRegex(RuntimeError, "Incomplete ArtJob pages"):
            submit.fetch_existing_jobs(missing)

    def test_rejects_failed_auth_and_wrong_project(self):
        with self.assertRaisesRegex(RuntimeError, "HTTP 401"):
            submit.fetch_existing_jobs(lambda method, url: (401, {"success": False}))
        with self.assertRaisesRegex(RuntimeError, "unrelated project"):
            submit.fetch_existing_jobs(lambda method, url: (200, {"success": True, "data": {
                "jobs": [{"id": 8, "projectSlug": "other"}],
                "pagination": {"totalCount": 1, "hasNextPage": False},
            }}))

    def test_different_prompt_never_reuses_an_unrelated_job(self):
        ledger = submit.parse_ledger()
        unrelated = [{"id": 42, "projectSlug": "comet-city-academy", "payload": {"promptString": "Different image"}}]
        self.assertEqual(submit.recover_submitted(ledger, unrelated), 0)
        self.assertFalse(any(subject.get("jobs") for subject in ledger["subjects"]))


if __name__ == "__main__":
    unittest.main()
