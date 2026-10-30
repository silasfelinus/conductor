"""Guard the versioned Space Couch captain/crew redraw against stale first-round art."""

from __future__ import annotations

import unittest
from pathlib import Path

import yaml

from scripts.enqueue_art_requests import compose_prompt
from scripts.repair_negation_art_prompts import violations


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "projects/game-of-captains/art/CAST-REDESIGN-ROUND-2.yaml"
CAPTAINS = {"fluke", "vale", "solace", "rex", "quill", "ro"}
CREW = {
    "pell", "vela", "tess", "rue", "mox", "jex", "sora", "kivo",
    "taal", "brin", "omi", "fen", "nyra", "gleam", "harrow", "edda",
}
EXPRESSIONS = {"primary", "defiant", "vulnerable"}


class SpaceCouchCastRedesignTests(unittest.TestCase):
    def test_every_identity_has_three_versioned_requests_and_traced_art(self):
        data = yaml.safe_load(LEDGER.read_text())
        self.assertEqual(data["project_slug"], "game-of-captains")
        self.assertIs(data["auto_submit"], True)
        self.assertIs(data["is_public"], False)
        self.assertEqual(len(data["subjects"]), 66)
        self.assertEqual(len(data["lanes"]), 1)
        self.assertEqual(data["lanes"][0]["engine"], "krea2")

        actual = set()
        keys, assets, seeds = set(), set(), set()
        for subject in data["subjects"]:
            key = subject["key"]
            parts = key.removeprefix("sc-cast-v2-").split("-")
            kind, *middle = parts
            expression = middle.pop()
            character = "-".join(middle)
            self.assertIn(expression, EXPRESSIONS)
            self.assertIn(character, CAPTAINS if kind == "captain" else CREW)
            actual.add((kind, character, expression))
            self.assertNotIn(key, keys)
            self.assertNotIn(subject["asset"], assets)
            self.assertNotIn(subject["seed"], seeds)
            keys.add(key)
            assets.add(subject["asset"])
            seeds.add(subject["seed"])
            expected = f"game-of-captains/portraits/v2/{kind}-{character}"
            if expression != "primary":
                expected += f"-{expression}"
            self.assertEqual(subject["asset"], expected)
            self.assertEqual(subject["lane"], "krea2")
            self.assertEqual(subject["size"], "1024x1024")
            # The private art sweep legitimately transitions requests to DONE.
            # Completed requests must have a submitted Job and an ArtImage.
            # Incomplete requests cannot claim an image just by listing a key.
            for lane, lane_art in subject.get("art", {}).items():
                if lane_art.get("status") == "DONE":
                    job_id = subject.get("jobs", {}).get(lane)
                    image_id = lane_art.get("art_image_id")
                    self.assertIsInstance(job_id, int)
                    self.assertGreater(job_id, 0)
                    self.assertIsInstance(image_id, int)
                    self.assertGreater(image_id, 0)
                else:
                    self.assertIsNone(lane_art.get("art_image_id"))

        expected = {
            (kind, identity, expression)
            for kind, names in (("captain", CAPTAINS), ("crew", CREW))
            for identity in names
            for expression in EXPRESSIONS
        }
        self.assertEqual(actual, expected)

    def test_literal_prompts_keep_couch_and_current_characters(self):
        data = yaml.safe_load(LEDGER.read_text())
        prompts = {}
        for subject in data["subjects"]:
            prompt = compose_prompt(data["lanes"][0], subject)
            prompts[subject["key"]] = prompt
            lower = prompt.lower()
            self.assertIn("scarlet", lower)
            self.assertIn("velvet couch", lower)
            self.assertIn("protective bubble", lower)
            self.assertIn("folding room", lower)
            self.assertIn("full-body", lower)
            self.assertEqual(list(violations(prompt)), [], subject["key"])

        self.assertIn("soldering gauntlet", prompts["sc-cast-v2-captain-vale-primary"])
        self.assertIn("janitor coveralls", prompts["sc-cast-v2-captain-solace-primary"])
        self.assertIn("sealed bodysuit", prompts["sc-cast-v2-captain-quill-primary"])
        self.assertIn("black velvet suit", prompts["sc-cast-v2-captain-ro-primary"])
        self.assertIn("silver android", prompts["sc-cast-v2-crew-mox-primary"])


if __name__ == "__main__":
    unittest.main()
