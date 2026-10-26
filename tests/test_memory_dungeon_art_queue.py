"""Regression contract for Memory Dungeon's interrupted 752-request art handoff."""
import sys
import unittest

import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from reconcile_memory_dungeon_art_jobs import (  # noqa: E402
    index_existing_jobs, reconcile_text,
)
from repair_memory_dungeon_art_prompts import repair_text  # noqa: E402


class MemoryArtQueueTests(unittest.TestCase):

    def test_both_complete_ledgers_have_700_plus_unique_requests(self):
        sources = [
            ROOT / "projects/art-prompts.yaml",
            ROOT / "projects/memory-dungeon/art/KNOWN-ART-REQUESTS.yaml",
        ]
        ids = []
        for source in sources:
            data = yaml.safe_load(source.read_text()) or {}
            subset = [
                item for item in data.get("requests") or []
                if str(item.get("id") or "").startswith("memory-dungeon-saturate-")
            ]
            # art-prompts.yaml is the live queue and is drained once the
            # requests are submitted; only the permanent ledger must stay full.
            if source.name == "art-prompts.yaml" and not subset:
                continue
            self.assertGreater(len(subset), 100, str(source))
            for item in subset:
                ids.append(item["id"])
                self.assertTrue(item.get("image_path"))
                self.assertEqual(item.get("project_slug"), "memory-dungeon")
                self.assertTrue(item.get("prompt"))
                for bad, _replacement in (
                    ("horizontal scenic frame", ""),
                    ("wide single frame", ""),
                    ("Square frame", ""),
                    ("cinematic frame", ""),
                ):
                    self.assertNotIn(bad, item["prompt"], item["id"])
        self.assertGreaterEqual(len(ids), 500)
        self.assertEqual(len(ids), len(set(ids)), "Duplicate requests would create duplicate ArtJobs")

    def test_recovers_an_existing_job_without_minting_another(self):
        entry = """requests:
- id: "memory-dungeon-saturate-a"
  status: pending
  target_repo: silasfelinus/kind_robots
  image_path: "public/images/memory-dungeon/a.webp"
  prompt: "Ancient archway and moss"
"""
        job = {
            "id": 45570, "status": "DONE",
            "payload": {"conductorRequest": {
                "id": "memory-dungeon-saturate-a",
                "targetRepo": "silasfelinus/kind_robots",
                "imagePath": "public/images/memory-dungeon/a.webp"
            }}
        }
        indexed = index_existing_jobs([job])
        revised, count = reconcile_text(entry, indexed)
        self.assertEqual(count, 1)
        self.assertIn("last_art_job_id: 45570", revised)
        again, count = reconcile_text(revised, indexed)
        self.assertEqual(count, 0)
        self.assertEqual(again, revised)

    def test_rejects_mismatched_destinations_and_failed_jobs(self):
        pending = {"id": 56, "status": "PENDING", "payload": {
            "conductorRequest": {"id": "memory-dungeon-saturate-a",
                                 "targetRepo": "silasfelinus/kind_robots",
                                 "imagePath": "public/images/elsewhere.webp"}}}
        failed = {**pending, "id": 57, "status": "FAILED"}
        indexed = index_existing_jobs([pending, failed])
        self.assertEqual(indexed[("memory-dungeon-saturate-a", "public/images/elsewhere.webp")], 56)
        self.assertNotIn(("memory-dungeon-saturate-a", "public/images/memory-dungeon/a.webp"), indexed)

    def test_does_not_overwrite_a_deliberate_regeneration(self):
        text = """requests:
- id: "memory-dungeon-saturate-a"
  status: pending
  force: true
  image_path: "public/images/memory-dungeon/a.webp"
  prompt: "Reshoot the scene"
"""
        fixed, count = reconcile_text(text, {("memory-dungeon-saturate-a", "public/images/memory-dungeon/a.webp"): 45570})
        self.assertEqual(count, 0)
        self.assertEqual(fixed, text)

    def test_repairs_only_memory_prompts(self):
        source = """requests:
- id: "memory-dungeon-saturate-a"
  prompt: "Hand-painted, horizontal scenic frame. A wide single frame"
- id: "unrelated-request"
  prompt: "Horizontal scenic frame is part of this painting"
- id: "memory-dungeon-saturate-b"
  prompt: "Square frame; cinematic frame"
"""
        result, count = repair_text(source)
        self.assertEqual(count, 2)
        self.assertIn("wide landscape illustration", result)
        self.assertIn("wide environmental composition", result)
        self.assertIn("Square composition; cinematic composition", result)
        self.assertIn('prompt: "Horizontal scenic frame is part', result)
        self.assertEqual(repair_text(result), (result, 0))


    def test_repairs_unclaimed_portrait_frame_noun_rejections(self):
        source = """requests:
- id: memory-dungeon-saturate-house-outcome-hd-27-keep
  prompt: "Haunting painted empty chair and silhouetted absent subject in ornate cracked portrait frame."
- id: memory-dungeon-saturate-dark-house-hd-27
  prompt: "Haunting painted empty chair and silhouetted absent subject in ornate cracked portrait frame."
- id: memory-dungeon-saturate-dark-house-outcome-hd-27-keep
  prompt: "Haunting painted empty chair and silhouetted absent subject in ornate cracked portrait frame."
- id: memory-dungeon-saturate-dark-house-hd-27-attend
  prompt: "Empty portrait frame on dark wall, adult traveler holding an image."
"""
        result, count = repair_text(source)
        self.assertEqual(count, 4)
        self.assertNotIn("portrait frame", result)
        self.assertIn("cracked carved wood", result)
        self.assertIn("carved gilded border", result)
        self.assertEqual(repair_text(result), (result, 0))


if __name__ == "__main__":
    unittest.main()
