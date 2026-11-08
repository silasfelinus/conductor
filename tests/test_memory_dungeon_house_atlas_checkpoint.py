"""Regression checks for durable House atlas receipts and delivery evidence.

The live audit owns HTTP verification. These checks ensure its committed
checkpoint cannot silently contradict the immutable two-atlas request ledger.
"""
import json
import unittest
from copy import deepcopy
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "projects/memory-dungeon/art"
ORIGINAL = "memory-dungeon-saturate-house-atlas-original-6x6"
MIRRORED = "memory-dungeon-saturate-house-atlas-mirrored-6x6"


def verify_checkpoint(ledger, report):
    requests = ledger["requests"]
    rows = report["results"]
    expected = {row["id"]: row for row in requests}
    if set(expected) != {ORIGINAL, MIRRORED} or len(requests) != 2:
        raise ValueError("Exactly the original and mirrored requests are required")
    if len(rows) != 2 or {row["id"] for row in rows} != set(expected):
        raise ValueError("Checkpoint must cover both distinct atlas requests")
    if report["total"] != 2:
        raise ValueError("Checkpoint total must equal two")
    delivered = 0
    image_ids = set()
    for row in rows:
        source = expected[row["id"]]
        if row["jobId"] != source["last_art_job_id"] or not isinstance(row["jobId"], int) or row["jobId"] <= 0:
            raise ValueError("ArtJob receipt differs from ledger")
        if row["imagePath"] != source["image_path"]:
            raise ValueError("ArtImage destination differs from ledger")
        if row["status"] == "delivered":
            image_id = row.get("artImageId")
            if not isinstance(image_id, int) or image_id <= 0 or image_id in image_ids:
                raise ValueError("Delivered atlas lacks a distinct positive ArtImage ID")
            image_ids.add(image_id)
            delivered += 1
    if report["delivered"] != delivered or report["counts"].get("delivered", 0) != delivered:
        raise ValueError("Checkpoint delivery count contradicts rows")
    if report["pendingReview"] < 0 or report["pendingReview"] > 2 - delivered:
        raise ValueError("Invalid pending review count")
    return delivered


class HouseAtlasCheckpointTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = yaml.safe_load((ART / "HOUSE-ATLAS-REQUESTS.yaml").read_text())
        cls.report = json.loads((ART / "HOUSE-ATLAS-STATUS.json").read_text())

    def test_committed_checkpoint_matches_two_production_receipts(self):
        self.assertEqual(verify_checkpoint(self.ledger, self.report), 2)

    def test_rejects_forged_artjob_receipt(self):
        report = deepcopy(self.report)
        report["results"][0]["jobId"] += 1
        with self.assertRaisesRegex(ValueError, "ArtJob"):
            verify_checkpoint(self.ledger, report)

    def test_rejects_wrong_media_destination(self):
        report = deepcopy(self.report)
        report["results"][1]["imagePath"] = report["results"][0]["imagePath"]
        with self.assertRaisesRegex(ValueError, "destination"):
            verify_checkpoint(self.ledger, report)

    def test_rejects_duplicate_artimage(self):
        report = deepcopy(self.report)
        report["results"][1]["artImageId"] = report["results"][0]["artImageId"]
        with self.assertRaisesRegex(ValueError, "ArtImage"):
            verify_checkpoint(self.ledger, report)

    def test_rejects_false_delivery_total(self):
        report = deepcopy(self.report)
        report["delivered"] = 1
        with self.assertRaisesRegex(ValueError, "count"):
            verify_checkpoint(self.ledger, report)

    def test_rejects_missing_mirrored_atlas(self):
        report = deepcopy(self.report)
        report["results"].pop()
        with self.assertRaisesRegex(ValueError, "both distinct"):
            verify_checkpoint(self.ledger, report)


if __name__ == "__main__":
    unittest.main()
