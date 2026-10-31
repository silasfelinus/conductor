"""Regression checks for the first real Hoshimori collectible-gallery ArtJob batch."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import sys
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from verify_memory_dungeon_hoshimori_gallery_pilot import (  # noqa: E402
    ART, LEDGER, ROUND2_LEDGER, ROUND2_SELECTED, SELECTED,
    load_and_validate, validate,
)


class HoshimoriGalleryPilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = yaml.safe_load(LEDGER.read_text(encoding="utf-8"))
        cls.sources = {
            world: yaml.safe_load((ART / f"HOSHIMORI-{world.upper()}-GALLERY-BRIEFS.yaml").read_text(encoding="utf-8"))
            for world in SELECTED
        }

    def test_exact_eight_authored_pilot_faces(self):
        result = load_and_validate()
        self.assertEqual(result["faces"], 8)
        self.assertEqual(result["submitted"] + result["unsubmitted"], 8)
        self.assertEqual([row["world"] for row in self.data["subjects"]], ["e07"] * 4 + ["e08"] * 4)

    def test_gallery_faces_do_not_reuse_style_proof_destinations(self):
        pilot_assets = [row["asset"] for row in self.data["subjects"]]
        self.assertEqual(len(set(pilot_assets)), 8)
        for world, filename in (("e07", "HOSHIMORI-WARM-STYLE-PROOFS.yaml"),
                                ("e08", "HOSHIMORI-HORROR-STYLE-PROOFS.yaml")):
            style = yaml.safe_load((ART / filename).read_text(encoding="utf-8"))
            paths = {row["image_path"].removeprefix("public/").removesuffix(".webp")
                     for row in style["requests"]}
            self.assertFalse(set(pilot_assets) & paths)
        self.assertTrue(all("/gallery/" in path for path in pilot_assets))

    def test_tampered_prompt_cannot_be_submitted_as_authored(self):
        altered = deepcopy(self.data)
        altered["subjects"][0]["prompt_prose"] = "An unrelated image."
        with self.assertRaisesRegex(ValueError, "source drift"):
            validate(altered, self.sources)

    def test_tampered_image_destination_is_rejected(self):
        altered = deepcopy(self.data)
        altered["subjects"][4]["asset"] = "images/memory-dungeon/hoshimori/e07/gallery/wrong"
        with self.assertRaisesRegex(ValueError, "source drift"):
            validate(altered, self.sources)

    def test_duplicate_artjob_receipts_are_rejected(self):
        altered = deepcopy(self.data)
        altered["subjects"][0]["jobs"] = {"krea2": 70001}
        altered["subjects"][1]["jobs"] = {"krea2": 70001}
        with self.assertRaisesRegex(ValueError, "duplicate ArtJob"):
            validate(altered, self.sources)

    def test_status_without_job_cannot_masquerade_as_delivery(self):
        altered = deepcopy(self.data)
        altered["subjects"][0].pop("jobs", None)
        altered["subjects"][0]["art"] = {"krea2": {"status": "DONE", "art_image_id": 42}}
        with self.assertRaisesRegex(ValueError, "without ArtJob"):
            validate(altered, self.sources)

    def test_require_jobs_refuses_unsubmitted_faces(self):
        altered = deepcopy(self.data)
        altered["subjects"][0].pop("jobs", None)
        with self.assertRaisesRegex(ValueError, "unsubmitted gallery face"):
            validate(altered, self.sources, require_jobs=True)

    def test_submitted_pending_is_not_delivered(self):
        altered = deepcopy(self.data)
        altered["subjects"][0]["jobs"] = {"krea2": 70001}
        altered["subjects"][0]["art"] = {"krea2": {"status": "PENDING", "art_image_id": None}}
        result = validate(altered, self.sources)
        self.assertGreaterEqual(result["submitted"], 1)

    def test_reject_artimage_before_done(self):
        altered = deepcopy(self.data)
        altered["subjects"][0]["jobs"] = {"krea2": 70001}
        altered["subjects"][0]["art"] = {"krea2": {"status": "PENDING", "art_image_id": 5}}
        with self.assertRaisesRegex(ValueError, "before DONE"):
            validate(altered, self.sources)

    def test_queue_visibility_and_priority_are_fixed(self):
        altered = deepcopy(self.data)
        altered["priority"] = 1000
        with self.assertRaisesRegex(ValueError, "settings changed"):
            validate(altered, self.sources)
        altered = deepcopy(self.data)
        altered["is_public"] = True
        with self.assertRaisesRegex(ValueError, "settings changed"):
            validate(altered, self.sources)


    def test_second_round_is_eight_source_backed_distinct_faces(self):
        round2 = yaml.safe_load(ROUND2_LEDGER.read_text(encoding="utf-8"))
        report = load_and_validate(round_number=2)
        self.assertEqual(report["faces"], 8)
        self.assertEqual(report["submitted"] + report["unsubmitted"], 8)
        self.assertEqual(
            [row["world"] for row in round2["subjects"]], ["e07"] * 4 + ["e08"] * 4
        )
        self.assertEqual(
            {row["face_id"] for row in self.data["subjects"]}
            & {row["face_id"] for row in round2["subjects"]}, set()
        )
        self.assertEqual(
            {row["asset"] for row in self.data["subjects"]}
            & {row["asset"] for row in round2["subjects"]}, set()
        )

    def test_second_round_rejects_forged_source_prompt_and_destination(self):
        round2 = yaml.safe_load(ROUND2_LEDGER.read_text(encoding="utf-8"))
        altered = deepcopy(round2)
        altered["subjects"][0]["prompt_prose"] = "A generic moth portrait."
        with self.assertRaisesRegex(ValueError, "source drift"):
            validate(altered, self.sources, selected=ROUND2_SELECTED)
        altered = deepcopy(round2)
        altered["subjects"][4]["asset"] = self.data["subjects"][4]["asset"]
        with self.assertRaisesRegex(ValueError, "source drift"):
            validate(altered, self.sources, selected=ROUND2_SELECTED)

    def test_second_round_requires_real_receipts_before_claiming_submission(self):
        round2 = yaml.safe_load(ROUND2_LEDGER.read_text(encoding="utf-8"))
        round2["subjects"][0].pop("jobs", None)
        round2["subjects"][0].pop("art", None)
        with self.assertRaisesRegex(ValueError, "unsubmitted gallery face"):
            validate(round2, self.sources, selected=ROUND2_SELECTED, require_jobs=True)

    def test_second_round_rejects_artimage_without_a_job(self):
        round2 = yaml.safe_load(ROUND2_LEDGER.read_text(encoding="utf-8"))
        round2["subjects"][0].pop("jobs", None)
        round2["subjects"][0]["art"] = {
            "krea2": {"status": "DONE", "art_image_id": 98989}
        }
        with self.assertRaisesRegex(ValueError, "without ArtJob"):
            validate(round2, self.sources, selected=ROUND2_SELECTED)



if __name__ == "__main__":
    unittest.main()
