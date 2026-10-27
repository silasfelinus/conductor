"""Regression contracts for genre-first Pacific-day new-playbook pitches."""
from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import daily_playbook_challenge as challenge
import build_digest_email_v2 as email


class DailyPlaybookChallengeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = ROOT / "pitches/playbook-challenges/2026-10-26.yaml"
        cls.docket = yaml.safe_load(cls.path.read_text(encoding="utf-8"))

    def test_every_committed_dated_docket_validates_with_full_lineage(self):
        """Catch malformed new daily dockets before the digest reads them."""
        for path in sorted((ROOT / "pitches/playbook-challenges").glob("????-??-??.yaml")):
            with self.subTest(date=path.stem):
                docket = yaml.safe_load(path.read_text(encoding="utf-8"))
                self.assertEqual(challenge.validate(path.stem, docket), [])
                payload = challenge.payload(path.stem)
                self.assertEqual(payload["status"], "ready")
                self.assertEqual(len(payload["pitches"]), 3)
                for pitch in payload["pitches"]:
                    self.assertGreater(pitch["units"]["art_units"], 0)
                    self.assertGreater(pitch["units"]["text_units"], 0)

    def test_all_eight_playbooks_reviewed_and_three_missing_genres_pitched(self):
        self.assertEqual(challenge.validate("2026-10-26", self.docket, set()), [])
        self.assertEqual(len(self.docket["reviewed_playbooks"]), 8)
        self.assertEqual(len(self.docket["pitches"]), 3)
        for pitch in self.docket["pitches"]:
            self.assertGreaterEqual(len(pitch["signature_systems"]), 3)
            self.assertGreaterEqual(len(pitch["collisions"]), 3)
            self.assertTrue(pitch["genre_pillar"])
            self.assertTrue(pitch["world_scope"])
            self.assertTrue(pitch["emotional_promise"])
        self.assertEqual(
            {p["slug"] for p in self.docket["pitches"]},
            {
                "the-bumbledown-atlas", "afterbody-the-human-question",
                "the-scales-of-forever",
            },
        )

    def test_calculated_costs_count_portraits_art_text_and_model_passes(self):
        cases = [
            # unique cast, portraits, images, authored beats, planned passes
            (29, 145, 422, 268, 1380),
            (38, 228, 677, 378, 2110),
            (34, 170, 547, 332, 1758),
        ]
        for pitch, (people, portraits, art, text, passes) in zip(
            self.docket["pitches"], cases, strict=True,
        ):
            with self.subTest(pitch=pitch["slug"]):
                units = challenge.compute_units(pitch)
                self.assertEqual(units["unique_people"], people)
                self.assertEqual(units["art_breakdown"]["portraits"], portraits)
                self.assertEqual(units["art_units"], art)
                self.assertEqual(units["text_units"], text)
                self.assertEqual(units["image_generation_passes"], art * 2)
                self.assertEqual(units["text_authoring_passes"], text * 2)
                self.assertEqual(units["total_planned_passes"], passes)

    def test_children_budget_is_about_friendship_not_romance(self):
        kids = self.docket["pitches"][0]
        self.assertEqual(kids["production"]["romance_illustrations"], 0)
        self.assertEqual(kids["production"]["romance_scenes"], 0)
        self.assertGreaterEqual(kids["production"]["friendship_illustrations"], 30)
        self.assertGreaterEqual(kids["production"]["friendship_scenes"], 40)

    def test_stale_docket_is_not_recycled(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(challenge, "DOCKETS", Path(directory)):
                self.assertEqual(challenge.payload("2026-10-27")["status"], "missing")
                self.assertEqual(challenge.payload("2026-10-27")["pitches"], [])

    def test_rejects_repeat_slug_title_or_shallow_collisions(self):
        old = copy.deepcopy(self.docket)
        old["pitches"][0]["slug"] = "emperor-of-dust"
        self.assertTrue(any("existing" in e for e in challenge.validate("2026-10-26", old)))
        old["pitches"][0]["slug"] = "past-playbook"
        self.assertTrue(any("duplicate" in e for e in challenge.validate("2026-10-26", old, {"past-playbook"})))
        old["pitches"][0]["slug"] = "new-slug"
        self.assertTrue(any("duplicate concept title" in e for e in challenge.validate(
            "2026-10-26", old, {"title:the-bumbledown-atlas"},
        )))
        old["pitches"][0]["collisions"] = old["pitches"][0]["collisions"][:1]
        self.assertTrue(any("at least three" in e for e in challenge.validate("2026-10-26", old)))

    def test_genre_pillar_and_systems_are_required_not_only_novelty(self):
        old = copy.deepcopy(self.docket)
        old["pitches"][0]["genre_gap"] = "fun"
        old["pitches"][1]["signature_systems"] = ["A fancy menu"]
        errors = challenge.validate("2026-10-26", old)
        self.assertTrue(any("genre_gap" in e for e in errors))
        self.assertTrue(any("genre-defining systems" in e for e in errors))

    def test_rejects_non_numeric_or_incomplete_art_budget(self):
        old = copy.deepcopy(self.docket)
        old["pitches"][0]["cast"]["portraits_per_person"] = 1
        self.assertTrue(any("portrait" in e for e in challenge.validate("2026-10-26", old)))
        old = copy.deepcopy(self.docket)
        old["pitches"][0]["production"]["maps"] = "a dozen"
        self.assertTrue(any("production" in e for e in challenge.validate("2026-10-26", old)))
        old = copy.deepcopy(self.docket)
        del old["pitches"][0]["production"]["friendship_illustrations"]
        self.assertTrue(any("production" in e for e in challenge.validate("2026-10-26", old)))

    def test_valid_payload_and_email_render_genre_world_and_budgets(self):
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            (temp / "2026-10-26.yaml").write_text(self.path.read_text(encoding="utf-8"))
            with patch.object(challenge, "DOCKETS", temp):
                payload = challenge.payload("2026-10-26")
                self.assertEqual(payload["status"], "ready")
                html = email.playbook_challenge_section(payload)
                for title in ("The Bumbledown Atlas", "Afterbody: The Human Question", "The Scales of Forever"):
                    self.assertIn(title, html)
                for art in (422, 677, 547):
                    self.assertIn(f"{art} unique finished images", html)
                self.assertIn("Genre pillar", html)
                self.assertIn("Genre-defining systems", html)
                self.assertIn("Opening characters", html)
                self.assertIn("No new project, ArtJob", html)

    def test_email_missing_docket_is_truthful(self):
        html = email.playbook_challenge_section({"date": "2026-10-27", "status": "missing", "pitches": []})
        self.assertIn("No new playbook pitch", html)
        self.assertNotIn("The Bumbledown Atlas", html)

    def test_escape_untrusted_pitch_text(self):
        pitch = copy.deepcopy(self.docket["pitches"][0])
        pitch["genre_pillar"] = '<script>alert("x")</script>'
        html = email.playbook_challenge_section({
            "date": "2026-10-26", "status": "ready",
            "pitches": [{**pitch, "units": challenge.compute_units(pitch)}],
        })
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)


if __name__ == "__main__":
    unittest.main()
