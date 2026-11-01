"""Adversarial provenance contracts for Hoshimori's fourth gallery batch."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import sys
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from consume_art_queue import entry_to_job  # noqa: E402
from verify_memory_dungeon_hoshimori_bound_gallery import (  # noqa: E402
    LEDGER, ROUND4_LEDGER, source_faces, validate,
)


class HoshimoriBoundGalleryRoundFourTests(unittest.TestCase):
    def setUp(self):
        self.data = yaml.safe_load(ROUND4_LEDGER.read_text(encoding="utf-8"))
        self.faces = source_faces(4)
        for request in self.data["requests"]:
            request.pop("last_art_job_id", None)

    def check(self, **kwargs):
        return validate(self.data, self.faces, round_number=4, **kwargs)

    def test_committed_receipts_are_valid_before_and_after_submission(self):
        committed = yaml.safe_load(ROUND4_LEDGER.read_text(encoding="utf-8"))
        report = validate(committed, self.faces, round_number=4)
        self.assertEqual(report["submitted"] + report["unsubmitted"], 8)

    def test_eight_unique_authored_location_faces(self):
        report = self.check()
        self.assertEqual(report["authored"], 8)
        self.assertEqual(report["submitted"] + report["unsubmitted"], 8)
        self.assertEqual({face["category"] for face in self.faces}, {"location"})
        self.assertEqual(len({row["image_path"] for row in self.data["requests"]}), 8)

    def test_all_jobs_are_private_and_destination_bound(self):
        for request in self.data["requests"]:
            job = entry_to_job(request)
            payload = job["payload"]
            self.assertEqual(job["engine"], "COMFY")
            self.assertEqual(payload["save"], {"isPublic": False, "isMature": False})
            self.assertEqual(payload["conductorRequest"]["id"], request["id"])
            self.assertEqual(payload["conductorRequest"]["imagePath"], request["image_path"])
            self.assertEqual(payload["conductorRequest"]["targetRepo"], request["target_repo"])

    def test_forged_prompt_and_destination_rejected(self):
        self.data["requests"][0]["prompt"] = "An unrelated placeholder."
        with self.assertRaisesRegex(ValueError, "source/visibility drift"):
            self.check()
        self.setUp()
        self.data["requests"][0]["image_path"] = "public/images/unrelated.webp"
        with self.assertRaisesRegex(ValueError, "source/visibility drift"):
            self.check()

    def test_public_mature_and_wrong_engine_rejected(self):
        for key, value in (("is_public", True), ("is_mature", True), ("engine", "a1111")):
            altered = deepcopy(self.data)
            altered["requests"][0][key] = value
            with self.assertRaisesRegex(ValueError, "source/visibility drift"):
                validate(altered, self.faces, round_number=4)

    def test_previous_bound_round_cannot_be_resubmitted(self):
        prior = yaml.safe_load(LEDGER.read_text(encoding="utf-8"))
        self.data["requests"][0]["id"] = prior["requests"][0]["id"]
        with self.assertRaisesRegex(ValueError, "source/visibility drift"):
            self.check()

    def test_previous_artjob_receipt_cannot_be_reused(self):
        prior = yaml.safe_load(LEDGER.read_text(encoding="utf-8"))
        prior_receipts = [row["last_art_job_id"] for row in prior["requests"]
                          if type(row.get("last_art_job_id")) is int]
        self.assertTrue(prior_receipts)
        self.data["requests"][0]["last_art_job_id"] = prior_receipts[0]
        with self.assertRaisesRegex(ValueError, "invalid/duplicate durable"):
            self.check()

    def test_missing_live_receipt_is_not_verified(self):
        self.data["requests"][0]["last_art_job_id"] = 61234
        with self.assertRaisesRegex(ValueError, "missing from live queue"):
            self.check(live_jobs={})
        self.assertEqual(self.check(live_jobs={}, allow_missing_live_jobs=True)["submitted"], 1)

    def test_live_binding_must_match_exact_target(self):
        first = self.data["requests"][0]
        first["last_art_job_id"] = 61234
        payload = entry_to_job(first)["payload"]
        job = {"id": 61234, "projectSlug": "memory-dungeon", "engine": "COMFY",
               "status": "PENDING", "payload": payload}
        self.assertEqual(self.check(live_jobs={61234: job})["bound_live"], 1)
        job["payload"] = deepcopy(payload)
        job["payload"]["conductorRequest"]["targetRepo"] = "someone/else"
        with self.assertRaisesRegex(ValueError, "live provenance mismatch"):
            self.check(live_jobs={61234: job})


if __name__ == "__main__":
    unittest.main()
