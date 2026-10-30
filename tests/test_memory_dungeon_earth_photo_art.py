"""Contract checks for Memory Dungeon's four currently playable Earth photographs."""
from pathlib import Path
import copy
import shlex
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_memory_dungeon_earth_photos import inspect, LEDGER  # noqa: E402


class EarthPhotoArtTests(unittest.TestCase):
    def test_four_playable_photo_destinations_have_authored_production_prompts(self):
        self.assertEqual(inspect(), [])

    def test_receipt_gate_requires_four_unique_positive_artjob_ids(self):
        data = yaml.safe_load(LEDGER.read_text())
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "requests.yaml"
            path.write_text(yaml.safe_dump(data))
            self.assertEqual(len([e for e in inspect(path, require_jobs=True) if "no durable" in e]), 4)
            for index, row in enumerate(data["requests"]):
                row["last_art_job_id"] = 61000 + index
            path.write_text(yaml.safe_dump(data))
            self.assertEqual(inspect(path, require_jobs=True), [])
            data["requests"][3]["last_art_job_id"] = 61000
            path.write_text(yaml.safe_dump(data))
            self.assertTrue(any("reused ArtJob" in e for e in inspect(path, require_jobs=True)))

    def test_wrong_media_path_or_duplicate_photo_is_rejected(self):
        data = yaml.safe_load(LEDGER.read_text())
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "requests.yaml"
            broken = copy.deepcopy(data)
            broken["requests"][0]["image_path"] = "public/images/memory-dungeon/elsewhere.webp"
            path.write_text(yaml.safe_dump(broken))
            self.assertTrue(any("wrong media destination" in e for e in inspect(path)))
            broken = copy.deepcopy(data)
            broken["requests"][1]["source_photo_id"] = "earth-01"
            path.write_text(yaml.safe_dump(broken))
            errors = inspect(path)
            self.assertTrue(any("duplicate photograph" in e for e in errors))
            self.assertTrue(any("Missing earth-02" in e for e in errors))

    def test_workflow_submits_and_checkpoints_earth_photo_receipts(self):
        workflow = yaml.safe_load((ROOT / ".github/workflows/auto-art-generate.yml").read_text())
        steps = workflow["jobs"]["generate"]["steps"]
        submit = [step for step in steps if step.get("name") == "Submit Memory Dungeon Earth Chronicle ArtJobs"]
        self.assertEqual(len(submit), 1)
        command = " ".join(line.strip().rstrip("\\").strip() for line in submit[0]["run"].splitlines())
        self.assertEqual(shlex.split(command), [
            "python", "scripts/consume_art_requests_to_media.py", "--live", "--submit-only",
            "--limit", "0", "--queue-file", "projects/memory-dungeon/art/EARTH-PHOTO-REQUESTS.yaml",
            "--id-prefix", "memory-dungeon-saturate-earth-photo-",
        ])
        checkpoint = next(step for step in steps if step.get("name") == "Checkpoint Memory Dungeon ArtJob IDs before rendering")
        self.assertIn("projects/memory-dungeon/art/EARTH-PHOTO-REQUESTS.yaml", checkpoint["run"])
        audit = next(step for step in steps if step.get("name") == "Verify four Earth Chronicle ArtJob receipts")
        self.assertIn("audit_memory_dungeon_earth_photos.py --require-jobs", audit["run"])


if __name__ == "__main__":
    unittest.main()
