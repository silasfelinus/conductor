"""House atlas production request and receipt integrity regressions."""
import sys
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_memory_dungeon_house_atlases import EXPECTED, LEDGER, validate  # noqa: E402


class HouseAtlasArtTests(unittest.TestCase):
    def test_two_distinct_authored_krea2_requests(self):
        data = yaml.safe_load(LEDGER.read_text())
        receipts = validate(data)
        self.assertEqual(set(receipts), set(EXPECTED))
        self.assertTrue(all(job is None or job > 0 for job in receipts.values()))

    def test_rejects_wrong_destination_and_duplicate(self):
        data = yaml.safe_load(LEDGER.read_text())
        data["requests"][0]["image_path"] = "public/images/memory-dungeon/other.webp"
        with self.assertRaisesRegex(ValueError, "destination"):
            validate(data)
        data = yaml.safe_load(LEDGER.read_text())
        data["requests"][1]["id"] = data["requests"][0]["id"]
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            validate(data)

    def test_only_durable_positive_ids_satisfy_submission_gate(self):
        data = yaml.safe_load(LEDGER.read_text())
        data["requests"][0].pop("last_art_job_id", None)
        with self.assertRaisesRegex(ValueError, "Unsubmitted"):
            validate(data, require_jobs=True)
        data["requests"][0]["last_art_job_id"] = 46501
        data["requests"][1]["last_art_job_id"] = 46502
        self.assertEqual(len(validate(data, require_jobs=True)), 2)
        data["requests"][1]["last_art_job_id"] = "not-an-id"
        with self.assertRaisesRegex(ValueError, "Invalid"):
            validate(data, require_jobs=True)


if __name__ == "__main__":
    unittest.main()
