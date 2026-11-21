"""Keep the fast art-intake lane independent of expensive rendering work."""
from pathlib import Path
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
FLOW = ROOT / ".github/workflows/prom-tactics-art-intake.yml"


class PromTacticsArtIntakeTests(unittest.TestCase):
    def test_workflow_submits_and_checkpoints_durable_receipts(self):
        doc = yaml.safe_load(FLOW.read_text(encoding="utf-8"))
        events = doc.get("on", doc.get(True, {}))
        self.assertIn("schedule", events)
        self.assertEqual(events["schedule"][0]["cron"], "17 * * * *")
        self.assertFalse(doc["concurrency"]["cancel-in-progress"])
        job = doc["jobs"]["submit-approved-private-art"]
        self.assertLessEqual(job["timeout-minutes"], 25)
        steps = job["steps"]
        names = [step.get("name", "") for step in steps]
        tactics = "Submit missing Tactics telegraphs and checkpoint ArtJob IDs"
        prom = "Submit missing October Prom art and checkpoint ArtJob IDs"
        proof = "Require durable ArtJob IDs for all 36 cells"
        self.assertLess(names.index(tactics), names.index(prom))
        self.assertLess(names.index(prom), names.index(proof))
        command = "\n".join(step.get("run", "") for step in steps)
        self.assertIn("enqueue_art_requests.py", command)
        self.assertIn("checkpoint_art_state.sh", command)
        self.assertIn("--require-jobs", command)
        self.assertNotIn("consume_art_requests_to_media.py", command)
        self.assertIn("${{ secrets.KR_API_TOKEN }}", job["env"]["KR_API_TOKEN"])

    def test_manifests_have_36_unique_unpublished_requests(self):
        from scripts.verify_prom_tactics_art_intake import LEDGERS, verify

        self.assertEqual(sum(count for _, count in LEDGERS.values()), 36)
        self.assertTrue(verify(require_jobs=False))


if __name__ == "__main__":
    unittest.main()
