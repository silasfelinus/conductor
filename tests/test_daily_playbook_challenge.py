"""Regression contracts for the Pacific-dated, proposal-only playbook challenge."""
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

    def test_complete_review_and_two_valid_original_pitches(self):
        self.assertEqual(challenge.validate("2026-10-26", self.docket, set()), [])
        self.assertEqual(len(self.docket["reviewed_playbooks"]), 8)
        self.assertEqual(len(self.docket["pitches"]), 2)

    def test_calculated_costs_count_unique_images_not_style_passes(self):
        museum, broadcast = self.docket["pitches"]
        self.assertEqual(challenge.compute_units(museum)["unique_people"], 22)
        self.assertEqual(challenge.compute_units(museum)["art_units"], 298)
        self.assertEqual(challenge.compute_units(museum)["text_units"], 200)
        self.assertEqual(challenge.compute_units(museum)["image_generation_passes"], 596)
        self.assertEqual(challenge.compute_units(museum)["text_authoring_passes"], 400)
        self.assertEqual(challenge.compute_units(museum)["total_planned_passes"], 996)
        self.assertEqual(challenge.compute_units(broadcast)["art_units"], 286)
        self.assertEqual(challenge.compute_units(broadcast)["text_units"], 186)
        self.assertEqual(challenge.compute_units(broadcast)["total_planned_passes"], 944)
        self.assertEqual(challenge.compute_units(broadcast)["art_breakdown"]["portraits"], 105)

    def test_stale_docket_is_not_recycled(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(challenge, "DOCKETS", Path(directory)):
                self.assertEqual(challenge.payload("2026-10-27")["status"], "missing")
                self.assertEqual(challenge.payload("2026-10-27")["pitches"], [])

    def test_rejects_repeat_and_shallow_hotspots(self):
        existing = copy.deepcopy(self.docket)
        existing["pitches"][0]["slug"] = "emperor-of-dust"
        self.assertTrue(any("existing" in e for e in challenge.validate("2026-10-26", existing)))
        existing["pitches"][0]["slug"] = "past-playbook"
        self.assertTrue(any("duplicate" in e for e in challenge.validate("2026-10-26", existing, {"past-playbook"})))
        existing["pitches"][0]["collisions"] = existing["pitches"][0]["collisions"][:1]
        self.assertTrue(any("at least three" in e for e in challenge.validate("2026-10-26", existing)))

    def test_rejects_imaginary_art_units(self):
        edited = copy.deepcopy(self.docket)
        edited["pitches"][0]["cast"]["portraits_per_person"] = 1
        self.assertTrue(any("portrait" in e for e in challenge.validate("2026-10-26", edited)))
        edited = copy.deepcopy(self.docket)
        edited["pitches"][0]["production"]["maps"] = "a dozen"
        self.assertTrue(any("production" in e for e in challenge.validate("2026-10-26", edited)))

    def test_valid_payload_and_email_section_render_full_brief(self):
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            (temp / "2026-10-26.yaml").write_text(self.path.read_text(encoding="utf-8"))
            with patch.object(challenge, "DOCKETS", temp):
                payload = challenge.payload("2026-10-26")
                self.assertEqual(payload["status"], "ready")
                rendered = email.playbook_challenge_section(payload)
                self.assertIn("Museum of Unfinished Tomorrows", rendered)
                self.assertIn("The Last Broadcast from Utopia", rendered)
                self.assertIn("298 unique finished images", rendered)
                self.assertIn("286 unique finished images", rendered)
                self.assertIn("Seed", rendered)
                self.assertIn("Opening characters", rendered)
                self.assertIn("No new project, ArtJob", rendered)

    def test_email_missing_docket_is_truthful(self):
        html = email.playbook_challenge_section({"date": "2026-10-27", "status": "missing", "pitches": []})
        self.assertIn("No new playbook pitch", html)
        self.assertNotIn("Museum of Unfinished Tomorrows", html)

    def test_escape_untrusted_pitch_text(self):
        entry = copy.deepcopy(self.docket["pitches"][0])
        entry["title"] = '<script>alert("x")</script>'
        rendered = email.playbook_challenge_section({
            "date": "2026-10-26", "status": "ready",
            "pitches": [{**entry, "units": challenge.compute_units(entry)}],
        })
        self.assertNotIn("<script>", rendered)
        self.assertIn("&lt;script&gt;", rendered)


if __name__ == "__main__":
    unittest.main()
