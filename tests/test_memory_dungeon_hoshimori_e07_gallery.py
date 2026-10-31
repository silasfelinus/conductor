"""Hoshimori e07 gallery brief contract: 30 local faces plus two cross-realm pairs.

This is an authoring gate, not an ArtJob/media delivery or in-game unlock test.
"""
from collections import Counter
from pathlib import Path
import re
import sys
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from memory_dungeon_hoshimori_prompt_contract import validate_prompt  # noqa: E402

MANIFEST = ROOT / "projects/memory-dungeon/art/HOSHIMORI-E07-GALLERY-BRIEFS.yaml"
DEST = "public/images/memory-dungeon/hoshimori/e07/gallery/"
PROTECTED = {
    "1,1": "Vesper’s Childhood Footbridge",
    "4,1": "The Orchard of Unfinished Maps",
    "2,2": "Pip’s Ledger House",
    "4,3": "The Red Oven",
    "4,4": "The Road Vesper Sold",
    "3,8": "The Paper Shadow Theatre",
    "8,8": "The South Watch Assembly",
    "2,3": "The Night-Crew Photograph",
    "7,5": "The Difficult Call",
}
CATEGORIES = {"character": 10, "location": 10, "event": 10, "collaboration": 2}


class HoshimoriGalleryBriefTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
        cls.faces = cls.manifest["faces"]

    def test_exact_gallery_budget_and_stage(self):
        self.assertEqual(self.manifest["version"], 1)
        self.assertEqual(self.manifest["world"], "e07")
        self.assertEqual(self.manifest["project"], "memory-dungeon")
        self.assertEqual(self.manifest["stage"], "briefs_only")
        self.assertIs(self.manifest["auto_submit"], False)
        self.assertEqual(self.manifest["expected_local"], 30)
        self.assertEqual(self.manifest["expected_collaboration"], 2)
        self.assertEqual(len(self.faces), 32)
        self.assertEqual(dict(Counter(face["category"] for face in self.faces)), CATEGORIES)

    def test_unique_ordered_ids_and_private_destinations(self):
        seen_ids, seen_paths, seen_prompts = set(), set(), set()
        for index, face in enumerate(self.faces, 1):
            number = f"{index:02d}"
            identifier = face["id"]
            self.assertRegex(identifier, rf"^hoshimori-e07-{number}-[a-z0-9-]+$")
            slug = identifier.split(f"e07-{number}-", 1)[1]
            self.assertEqual(face["image_path"], f"{DEST}{number}-{slug}.webp")
            self.assertNotIn(identifier, seen_ids)
            self.assertNotIn(face["image_path"], seen_paths)
            self.assertNotIn(face["prompt"], seen_prompts)
            seen_ids.add(identifier)
            seen_paths.add(face["image_path"])
            seen_prompts.add(face["prompt"])
            self.assertEqual(face["status"], "brief_only")
            for forbidden in ("last_art_job_id", "art_image_id", "delivered", "source_url"):
                self.assertNotIn(forbidden, face)

    def test_every_face_has_valid_canon_site_and_krea2_safe_scene(self):
        for face in self.faces:
            with self.subTest(face=face["id"]):
                self.assertRegex(face["site_key"], r"^[1-8],[1-8]$")
                if face["site_key"] in PROTECTED:
                    self.assertEqual(face["source_title"], PROTECTED[face["site_key"]])
                self.assertGreaterEqual(len(face["source_title"]), 9)
                self.assertGreaterEqual(len(face["story_hook"]), 50)
                self.assertGreaterEqual(len(face["prompt"]), 180)
                validate_prompt(face["prompt"], face["id"])
                self.assertNotRegex(face["prompt"], re.compile(r"\b(?:placeholder|svg|emoji)\b", re.I))

    def test_cross_realm_pairs_are_distinct_and_last(self):
        local = self.faces[:30]
        pairs = self.faces[30:]
        self.assertTrue(all(face["category"] != "collaboration" for face in local))
        self.assertEqual([face["category"] for face in pairs], ["collaboration", "collaboration"])
        self.assertEqual([face["cross_realm"] for face in pairs], ["e05", "e03"])
        self.assertTrue(all("cross_realm" not in face for face in local))
        self.assertIn("Scylla", pairs[0]["prompt"])
        self.assertIn("Morrow", pairs[1]["prompt"])
        self.assertIn("Vesper", pairs[0]["prompt"])
        self.assertIn("Pip", pairs[1]["prompt"])


if __name__ == "__main__":
    unittest.main()
