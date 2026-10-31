"""Hoshimori e08 nightmare gallery authoring contract: 30 local + two cross-realm faces.

This verifies only authored briefs. It does not imply queued ArtJobs, delivered
ArtImages, visual acceptance, or in-game collectible unlocks.
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

MANIFEST = ROOT / "projects/memory-dungeon/art/HOSHIMORI-E08-GALLERY-BRIEFS.yaml"
WARM_MANIFEST = ROOT / "projects/memory-dungeon/art/HOSHIMORI-E07-GALLERY-BRIEFS.yaml"
DEST = "public/images/memory-dungeon/hoshimori/e08/gallery/"
CATEGORIES = {"character": 10, "location": 10, "event": 10, "collaboration": 2}

# Exact title snapshot from kind_robots/utils/memoryDungeon/hoshimoriNight.ts.
# Only these first sixteen e08 sites are source-backed; later tiles are not
# silently credited as implemented by an illustration brief.
NIGHT_SITES = {
    "1,1": "Cedar Footbridge / The Wall That Listens",
    "2,1": "Singing Terraces / The Breathless Choir",
    "3,1": "Persimmon Steps / The Coat With No Body",
    "4,1": "Orchard of Floating Lanterns / The Hanging Eyes",
    "1,2": "Lantern Stall / The Mask Exchange",
    "2,2": "Pip’s Ledger House / The Census of Rescued Names",
    "3,2": "Shrine of the Third Light / The Door That Prays",
    "4,2": "Bakery Back Door / The Nurikabe Toll",
    "1,3": "Returning Slippers / The March of Empty Feet",
    "2,3": "Night-Crew Lane / The Names Beneath Ash",
    "3,3": "Guest Registry / The Redacted Parade",
    "4,3": "The Red Oven / The Furnace of Names",
    "1,4": "Hillside Shelter / The Photograph Behind Glass",
    "2,4": "The Paper Theatre / Actors Who Cannot Exit",
    "3,4": "Oathboat / The Ferry That Returns Itself",
    "4,4": "Southern Council / The Last Shut Door",
}


class HoshimoriNightGalleryBriefTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
        cls.faces = cls.manifest["faces"]
        cls.warm_faces = yaml.safe_load(WARM_MANIFEST.read_text(encoding="utf-8"))["faces"]

    def test_budget_and_authoring_only_gate(self):
        self.assertEqual(self.manifest["version"], 1)
        self.assertEqual(self.manifest["world"], "e08")
        self.assertEqual(self.manifest["project"], "memory-dungeon")
        self.assertEqual(self.manifest["stage"], "briefs_only")
        self.assertIs(self.manifest["auto_submit"], False)
        self.assertEqual(self.manifest["expected_local"], 30)
        self.assertEqual(self.manifest["expected_collaboration"], 2)
        self.assertEqual(len(self.faces), 32)
        self.assertEqual(dict(Counter(f["category"] for f in self.faces)), CATEGORIES)

    def test_unique_numbered_ids_and_unsubmitted_media_destinations(self):
        ids, paths, prompts = set(), set(), set()
        warm_ids = {f["id"] for f in self.warm_faces}
        warm_paths = {f["image_path"] for f in self.warm_faces}
        for index, face in enumerate(self.faces, 1):
            number = f"{index:02d}"
            identifier = face["id"]
            self.assertRegex(identifier, rf"^hoshimori-e08-{number}-[a-z0-9-]+$")
            slug = identifier.split(f"e08-{number}-", 1)[1]
            self.assertEqual(face["image_path"], f"{DEST}{number}-{slug}.webp")
            self.assertNotIn(identifier, ids | warm_ids)
            self.assertNotIn(face["image_path"], paths | warm_paths)
            self.assertNotIn(face["prompt"], prompts)
            ids.add(identifier)
            paths.add(face["image_path"])
            prompts.add(face["prompt"])
            self.assertEqual(face["status"], "brief_only")
            for forbidden in ("last_art_job_id", "art_image_id", "delivered", "source_url"):
                self.assertNotIn(forbidden, face)

    def test_every_brief_is_anchored_to_actual_night_site_and_safe_prompt(self):
        seen_sites = set()
        for face in self.faces:
            with self.subTest(face=face["id"]):
                self.assertIn(face["site_key"], NIGHT_SITES)
                self.assertEqual(face["source_title"], NIGHT_SITES[face["site_key"]])
                seen_sites.add(face["site_key"])
                self.assertGreaterEqual(len(face["story_hook"]), 50)
                self.assertGreaterEqual(len(face["prompt"]), 180)
                validate_prompt(face["prompt"], face["id"])
                self.assertNotRegex(
                    face["prompt"],
                    re.compile(r"\b(?:placeholder|svg|emoji|Junji\s+Ito|Ghibli)\b", re.I),
                )
        self.assertEqual(seen_sites, set(NIGHT_SITES))
        self.assertNotIn("6,7", seen_sites)  # Reserved photo, not yet an authored site.

    def test_face_order_and_distinct_cross_realm_pairings(self):
        self.assertEqual([f["category"] for f in self.faces[:10]], ["character"] * 10)
        self.assertEqual([f["category"] for f in self.faces[10:20]], ["location"] * 10)
        self.assertEqual([f["category"] for f in self.faces[20:30]], ["event"] * 10)
        self.assertEqual([f["category"] for f in self.faces[30:]], ["collaboration"] * 2)
        self.assertTrue(all("cross_realm" not in f for f in self.faces[:30]))
        self.assertEqual([f["cross_realm"] for f in self.faces[30:]], ["e06", "e04"])
        self.assertIn("Vesper", self.faces[30]["prompt"])
        self.assertIn("Scylla", self.faces[30]["prompt"])
        self.assertIn("Pip", self.faces[31]["prompt"])
        self.assertIn("Morrow", self.faces[31]["prompt"])

    def test_nightmare_is_not_warm_gallery_relabeling(self):
        warm_prompts = {f["prompt"] for f in self.warm_faces}
        self.assertTrue(all(f["prompt"] not in warm_prompts for f in self.faces))
        combined = " ".join(f["prompt"] for f in self.faces)
        for required in ("Vesper", "Scylla", "Pip", "Oren", "nurikabe", "procession"):
            self.assertIn(required.casefold(), combined.casefold())


if __name__ == "__main__":
    unittest.main()
