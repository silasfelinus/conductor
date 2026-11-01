"""Gutter Crown first reserve art manifest and stable slot coverage."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "projects/slime-city/art/GUTTER-CROWN-RESERVE-CARDS-ROUND-3.yaml"
RESERVES = {
    "splice-runner", "mutual-aid", "pogo-punk", "amp-tripwire",
    "union-millwright", "spare-pistons", "spark-diver", "firebreak-parade",
    "pipe-seer", "snitch-grate", "audit-fiend", "debt-holiday",
}

class GutterCrownArtContract(unittest.TestCase):
    def test_all_reserves_have_unique_queue_slots(self):
        data = yaml.safe_load(LEDGER.read_text(encoding="utf-8"))
        self.assertEqual(data["project_slug"], "slime-city")
        self.assertTrue(data["auto_submit"])
        self.assertFalse(data["is_public"])
        subjects = data["subjects"]
        self.assertEqual(len(subjects), 12)
        self.assertEqual({row["asset"].split("/")[-1] for row in subjects}, RESERVES)
        self.assertEqual(len({row["seed"] for row in subjects}), 12)
        self.assertEqual(len({row["key"] for row in subjects}), 12)
        prior = yaml.safe_load((ROOT / "projects/slime-city/art/BLACKOUT-STORY-ROUND-2.yaml").read_text(encoding="utf-8"))
        self.assertFalse({row["asset"] for row in subjects} & {row["asset"] for row in prior["subjects"]})
        self.assertTrue(all(row["lane"] == "krea2" and row["prompt_prose"].strip()
                            and row["entity"] == "card-art" for row in subjects))

if __name__ == "__main__":
    unittest.main()
