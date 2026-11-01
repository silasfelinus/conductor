"""Adversarial provenance checks for Memory Dungeon's destination-bound gallery batch."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import sys
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from verify_memory_dungeon_hoshimori_bound_gallery import (  # noqa: E402
    LEDGER, source_faces, validate,
)


class HoshimoriBoundGalleryTests(unittest.TestCase):
    def setUp(self):
        self.data = yaml.safe_load(LEDGER.read_text(encoding="utf-8"))
        self.faces = source_faces()

    def test_exact_eight_source_backed_requests(self):
        report = validate(self.data, self.faces)
        self.assertEqual(report["authored"], 8)
        self.assertEqual(report["submitted"] + report["unsubmitted"], 8)
        self.assertEqual(report["bound_live"], None)
        self.assertNotEqual(report["delivered"], 8)

    def test_privacy_and_destination_are_in_actual_queue_payload(self):
        from consume_art_queue import entry_to_job
        for request in self.data["requests"]:
            job = entry_to_job(request)
            self.assertEqual(job["payload"]["save"], {"isPublic": False, "isMature": False})
            self.assertEqual(job["payload"]["conductorRequest"]["id"], request["id"])
            self.assertEqual(job["payload"]["imagePath"], request["image_path"])
            self.assertEqual(job["payload"]["targetRepo"], request["target_repo"])
            self.assertEqual(job["engine"], "COMFY")

    def test_forged_prompt_is_rejected(self):
        self.data["requests"][0]["prompt"] = "A different drawing."
        with self.assertRaisesRegex(ValueError, "source/visibility drift"):
            validate(self.data, self.faces)

    def test_cross_realm_destination_is_rejected(self):
        self.data["requests"][0]["image_path"] = self.data["requests"][4]["image_path"]
        with self.assertRaisesRegex(ValueError, "source/visibility drift"):
            validate(self.data, self.faces)

    def test_public_or_mature_override_is_rejected(self):
        self.data["requests"][0]["is_public"] = True
        with self.assertRaisesRegex(ValueError, "source/visibility drift"):
            validate(self.data, self.faces)
        self.data["requests"][0]["is_public"] = False
        self.data["requests"][0]["is_mature"] = True
        with self.assertRaisesRegex(ValueError, "source/visibility drift"):
            validate(self.data, self.faces)

    def test_duplicate_face_from_prior_round_is_rejected(self):
        self.data["requests"][0]["id"] = "hoshimori-e07-01-vesper-route-cartographer"
        with self.assertRaisesRegex(ValueError, "source/visibility drift"):
            validate(self.data, self.faces)

    def test_receipts_must_be_distinct_positive_integers(self):
        self.data["requests"][0]["last_art_job_id"] = 61234
        self.data["requests"][1]["last_art_job_id"] = 61234
        with self.assertRaisesRegex(ValueError, "duplicate durable"):
            validate(self.data, self.faces)
        self.data["requests"][1]["last_art_job_id"] = -1
        with self.assertRaisesRegex(ValueError, "invalid/duplicate"):
            validate(self.data, self.faces)

    def test_require_jobs_rejects_unsubmitted_requests(self):
        with self.assertRaisesRegex(ValueError, "unsubmitted"):
            validate(self.data, self.faces, require_jobs=True)

    def test_live_receipt_checks_real_binding_not_only_status(self):
        first = self.data["requests"][0]
        first["last_art_job_id"] = 61234
        from consume_art_queue import entry_to_job
        job = entry_to_job(first)
        live = {61234: {"id": 61234, "projectSlug": "memory-dungeon",
                        "engine": "COMFY", "status": "PENDING", "payload": job["payload"]}}
        self.assertEqual(validate(self.data, self.faces, live_jobs=live)["bound_live"], 1)
        live[61234]["payload"] = deepcopy(job["payload"])
        live[61234]["payload"]["conductorRequest"]["imagePath"] = "public/images/unrelated.webp"
        with self.assertRaisesRegex(ValueError, "live provenance mismatch"):
            validate(self.data, self.faces, live_jobs=live)

    def test_unreadable_live_receipt_is_not_delivery(self):
        self.data["requests"][0]["last_art_job_id"] = 61234
        with self.assertRaisesRegex(ValueError, "missing from live queue"):
            validate(self.data, self.faces, live_jobs={})

    def test_generic_privacy_flags_reject_string_bools(self):
        from consume_art_queue import entry_to_job
        request = deepcopy(self.data["requests"][0])
        request["is_public"] = "false"
        with self.assertRaisesRegex(ValueError, "must be a boolean"):
            entry_to_job(request)


if __name__ == "__main__":
    unittest.main()
