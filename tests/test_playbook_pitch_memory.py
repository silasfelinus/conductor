"""Memory, genealogy and exact-three daily story-pitch contracts."""
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
import playbook_pitch_memory as memory
import build_digest_email_v2 as email


class EvolvingPitchMemoryTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.dockets = Path(self.temp.name)
        original = ROOT / "pitches/playbook-challenges/2026-10-26.yaml"
        self.root = yaml.safe_load(original.read_text(encoding="utf-8"))
        (self.dockets / "2026-10-26.yaml").write_text(
            yaml.safe_dump(self.root, sort_keys=False), encoding="utf-8",
        )
        self.patcher = patch.object(challenge, "DOCKETS", self.dockets)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def next_day(self):
        docket = copy.deepcopy(self.root)
        docket["date"] = "2026-10-27"
        expanded, fresh, fused = docket["pitches"]

        expanded["mode"] = "expand"
        expanded["parents"] = ["2026-10-26/the-bumbledown-atlas"]
        expanded["evolution"] = (
            "Deepens the atlas's reading-free visual syntax through cooperative "
            "friendship rules and introduces a new folded-map puzzle branch."
        )
        expanded["next_questions"] = [
            "Which companion can decipher a partially folded picture?",
            "When should the atlas change after a heartfelt apology?",
        ]

        fresh["mode"] = "new"
        fresh["slug"] = "the-barrowlight-sea"
        fresh["concept_id"] = fresh["slug"]
        fresh["title"] = "The Barrowlight Sea"
        fresh["parents"] = []

        fused["mode"] = "meld"
        fused["slug"] = "the-ghosts-of-circuit-heaven"
        fused["concept_id"] = fused["slug"]
        fused["title"] = "The Ghosts of Circuit Heaven"
        fused["parents"] = [
            "2026-10-26/afterbody-the-human-question",
            "2026-10-26/the-scales-of-forever",
        ]
        fused["evolution"] = (
            "A genuine fusion of afterlife testimony and copied-self jurisprudence "
            "where digital personhood changes the rules of both eternities."
        )
        return docket

    def test_first_day_and_three_lineage_modes_validate(self):
        self.assertEqual(challenge.validate("2026-10-26", self.root), [])
        docket = self.next_day()
        self.assertEqual(challenge.validate("2026-10-27", docket), [])
        (self.dockets / "2026-10-27.yaml").write_text(
            yaml.safe_dump(docket), encoding="utf-8",
        )
        payload = challenge.payload("2026-10-27")
        self.assertEqual(payload["status"], "ready")
        self.assertEqual([p["mode"] for p in payload["pitches"]], ["expand", "new", "meld"])
        rendered = email.playbook_challenge_section(payload)
        self.assertIn("Expanded concept", rendered)
        self.assertIn("Concept fusion", rendered)
        self.assertIn("2026-10-26/the-scales-of-forever", rendered)
        self.assertIn("What evolves", rendered)
        self.assertIn("Next design questions", rendered)

    def test_exactly_three_is_mandatory(self):
        docket = self.next_day()
        for count in (0, 1, 2, 4):
            with self.subTest(count=count):
                edited = copy.deepcopy(docket)
                edited["pitches"] = (docket["pitches"] * 2)[:count]
                errors = challenge.validate("2026-10-27", edited)
                self.assertTrue(any("exactly three" in e for e in errors))

    def test_single_lineage_keeps_stable_id_across_years(self):
        docket = self.next_day()
        (self.dockets / "2026-10-27.yaml").write_text(
            yaml.safe_dump(docket), encoding="utf-8",
        )
        index = memory.build_index(self.dockets, before="2026-10-28")
        self.assertEqual(
            index["concepts"]["the-bumbledown-atlas"]["versions"],
            ["2026-10-26/the-bumbledown-atlas", "2026-10-27/the-bumbledown-atlas"],
        )
        self.assertEqual(index["concepts"]["the-bumbledown-atlas"]["latest"]["mode"], "expand")
        self.assertEqual(
            index["versions"]["2026-10-27/the-ghosts-of-circuit-heaven"]["parents"],
            ["2026-10-26/afterbody-the-human-question", "2026-10-26/the-scales-of-forever"],
        )
        self.assertIn("LONG-RUN PITCH MEMORY", memory.memory_summary(index))

    def test_future_or_missing_ancestor_is_blocked(self):
        docket = self.next_day()
        docket["pitches"][0]["parents"] = ["2026-10-28/the-bumbledown-atlas"]
        self.assertTrue(any("future parent" in e for e in challenge.validate("2026-10-27", docket)))
        docket["pitches"][0]["parents"] = ["2026-10-27/the-bumbledown-atlas"]
        self.assertTrue(any("same-day" in e for e in challenge.validate("2026-10-27", docket)))

    def test_expansion_cannot_switch_identity(self):
        docket = self.next_day()
        docket["pitches"][0]["concept_id"] = "other-concept"
        errors = challenge.validate("2026-10-27", docket)
        self.assertTrue(any("parent's concept_id" in e for e in errors))

    def test_merger_needs_two_different_families(self):
        docket = self.next_day()
        docket["pitches"][2]["parents"] = [
            "2026-10-26/afterbody-the-human-question",
            "2026-10-26/afterbody-the-human-question",
        ]
        errors = challenge.validate("2026-10-27", docket)
        self.assertTrue(any("different earlier concept families" in e for e in errors))
        self.assertTrue(any("repeated parent" in e for e in errors))

    def test_previous_ideas_are_not_new_genres_and_daily_continuation_required(self):
        docket = self.next_day()
        docket["pitches"][1]["slug"] = "afterbody-the-human-question"
        docket["pitches"][1]["concept_id"] = "afterbody-the-human-question"
        errors = challenge.validate("2026-10-27", docket)
        self.assertTrue(any("historical identity" in e for e in errors))
        all_fresh = self.next_day()
        for idx, pitch in enumerate(all_fresh["pitches"]):
            pitch["mode"] = "new"
            pitch["parents"] = []
            pitch["slug"] = f"fresh-{idx}"
            pitch["concept_id"] = pitch["slug"]
            pitch["title"] = f"Fresh Game {idx}"
        self.assertTrue(any(
            "at least one evolution" in e
            for e in challenge.validate("2026-10-27", all_fresh)
        ))

    def test_rejected_ancestor_requires_conscious_reactivation(self):
        (self.dockets / "MEMORY.yaml").write_text(yaml.safe_dump({
            "concepts": {
                "afterbody-the-human-question": {
                    "status": "rejected", "guardrails": ["No repackaging without approval"],
                },
            },
        }), encoding="utf-8")
        docket = self.next_day()
        errors = challenge.validate("2026-10-27", docket)
        self.assertTrue(any("cannot merge a rejected concept" in e for e in errors))
        notes = memory.build_index(self.dockets)
        self.assertEqual(notes["concepts"]["afterbody-the-human-question"]["editorial"]["status"], "rejected")

    def test_full_history_does_not_forget_older_revisions(self):
        docket = self.next_day()
        (self.dockets / "2026-10-27.yaml").write_text(
            yaml.safe_dump(docket), encoding="utf-8",
        )
        old = copy.deepcopy(docket)
        old["date"] = "2026-11-25"
        # All 3 are expansions of already-established 10/27 families.
        for pitch in old["pitches"]:
            pitch["mode"] = "expand"
            pitch["parents"] = [f"2026-10-27/{pitch['slug']}"]
        self.assertEqual(challenge.validate("2026-11-25", old), [])
        index = memory.build_index(self.dockets, before="2026-11-25")
        self.assertIn("2026-10-26/the-bumbledown-atlas", index["versions"])


if __name__ == "__main__":
    unittest.main()
