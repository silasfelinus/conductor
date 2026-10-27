"""Offline guardrails for the 100 named Space Couch hires and 200 scoped Krea2 requests."""
from __future__ import annotations

import unittest
from pathlib import Path

from scripts import submit_space_couch_redshirts as submit
from scripts import enqueue_art_requests as enq


class RedshirtArtTests(unittest.TestCase):
    def test_exact_two_unique_jobs_per_hire(self):
        header, data = submit.parse_ledger()
        self.assertIn("Space Couch", header)
        self.assertFalse(data["auto_submit"], "Only the targeted submitter owns this ledger")
        self.assertEqual(len(data["subjects"]), 200)
        keys, assets, seeds = set(), set(), set()
        for row in data["subjects"]:
            self.assertNotIn(row["key"], keys)
            self.assertNotIn(row["asset"], assets)
            self.assertNotIn(row["seed"], seeds)
            keys.add(row["key"])
            assets.add(row["asset"])
            seeds.add(row["seed"])
            self.assertEqual(row["lane"], "krea2")
            self.assertTrue("game-of-captains/redshirts/" in row["asset"])
            prompt = enq.compose_prompt(data["lanes"][0], row)
            self.assertTrue("crimson" in prompt.lower())
            self.assertTrue("uniform" in prompt.lower())
            self.assertTrue("couch" in prompt.lower())
            self.assertGreater(len(prompt), 350)
        self.assertEqual(len(keys), 200)
        self.assertEqual(len(assets), 200)
        self.assertEqual(len(seeds), 200)

    def test_recover_job_id_from_exact_prompt(self):
        _, data = submit.parse_ledger()
        row = data["subjects"][0]
        prompt = enq.compose_prompt(data["lanes"][0], row)
        jobs = [{
            "id": 55601,
            "projectSlug": "game-of-captains",
            "payload": {"promptString": prompt},
        }]
        self.assertEqual(submit.reconcile(data, jobs), 1)
        self.assertEqual(row["jobs"]["krea2"], 55601)
        self.assertEqual(submit.reconcile(data, jobs), 0)
        self.assertFalse(data["subjects"][1].get("jobs"))

    def test_ignores_unrelated_prompt(self):
        _, data = submit.parse_ledger()
        self.assertEqual(submit.reconcile(data, [{
            "id": 55, "projectSlug": "game-of-captains",
            "payload": {"promptString": "An unrelated painting"}
        }]), 0)

    def test_refuses_incomplete_or_mis_scoped_remote_queue(self):
        with self.assertRaisesRegex(RuntimeError, "Partial ArtJob"):
            submit.fetch_existing_jobs(lambda method, url: (
                200, {"success": True, "data": {
                    "jobs": [], "pagination": {"totalCount": 3, "hasNextPage": False}
                }}
            ))
        with self.assertRaisesRegex(RuntimeError, "unrelated project"):
            submit.fetch_existing_jobs(lambda method, url: (
                200, {"success": True, "data": {
                    "jobs": [{"id": 1, "projectSlug": "other"}],
                    "pagination": {"totalCount": 1, "hasNextPage": False},
                }}
            ))
        with self.assertRaisesRegex(RuntimeError, "HTTP 401"):
            submit.fetch_existing_jobs(lambda method, url: (401, {"success": False}))

    def test_prompts_avoid_legacy_negation_contract(self):
        from scripts.repair_negation_art_prompts import violations
        _, data = submit.parse_ledger()
        for cell in data["subjects"]:
            prompt = enq.compose_prompt(data["lanes"][0], cell)
            self.assertEqual(list(violations(prompt)), [], cell["key"])


if __name__ == "__main__":
    unittest.main()
