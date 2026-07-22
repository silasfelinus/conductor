import os
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import semantic_art_quality


class ColoringBookSemanticGateTests(unittest.TestCase):
    def verdict(self, **overrides):
        value = {
            "subject_match": True,
            "on_brief": True,
            "line_art_valid": True,
            "camp_reads": True,
            "horror_reads": True,
            "anatomy_ok": True,
            "matches_approved_bar": True,
            "score": 88,
            "verdict": "promote",
            "reasons": [],
        }
        value.update(overrides)
        return value

    def test_missing_vision_key_fails_closed(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "ANTHROPIC_API_KEY"):
                semantic_art_quality.assess_semantic_file(
                    Path("candidate.webp"),
                    "A vampire family portrait",
                )

    def test_matching_subject_and_brief_pass(self):
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}, clear=False):
            with patch.object(
                semantic_art_quality.curate_art,
                "call_vision",
                return_value=self.verdict(),
            ):
                accepted, verdict = semantic_art_quality.assess_semantic_file(
                    Path("candidate.webp"),
                    "A vampire family portrait",
                )

        self.assertTrue(accepted)
        self.assertTrue(verdict["subject_match"])
        self.assertTrue(verdict["on_brief"])
        self.assertEqual(verdict["score"], 88)

    def test_colorful_cosmic_poster_cannot_pass_subject_gate(self):
        cosmic_failure = self.verdict(
            subject_match=False,
            on_brief=False,
            score=82,
            verdict="reject",
            reasons=[
                "Cosmic triangular architecture replaces the requested vampire family"
            ],
        )

        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}, clear=False):
            with patch.object(
                semantic_art_quality.curate_art,
                "call_vision",
                return_value=cosmic_failure,
            ):
                accepted, verdict = semantic_art_quality.assess_semantic_file(
                    Path("mr-009.webp"),
                    "Draculina and her three husbands in a velvet crypt lounge",
                )

        self.assertFalse(accepted)
        self.assertFalse(verdict["subject_match"])
        self.assertFalse(verdict["on_brief"])
        self.assertIn(
            "requested subjects or scene are absent",
            verdict["reasons"],
        )

    def test_score_floor_is_required_even_when_subject_matches(self):
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}, clear=False):
            with patch.object(
                semantic_art_quality.curate_art,
                "call_vision",
                return_value=self.verdict(score=61, verdict="revise"),
            ):
                accepted, verdict = semantic_art_quality.assess_semantic_file(
                    Path("candidate.webp"),
                    "A vampire family portrait",
                    min_score=75,
                )

        self.assertFalse(accepted)
        self.assertIn("below minimum 75", " ".join(verdict["reasons"]))

    def test_retry_seed_changes_deterministically(self):
        first = semantic_art_quality.next_retry_seed(840009, 1)
        second = semantic_art_quality.next_retry_seed(840009, 2)
        self.assertNotEqual(first, 840009)
        self.assertNotEqual(first, second)
        self.assertEqual(first, semantic_art_quality.next_retry_seed(840009, 1))

    def test_literal_retry_prompt_keeps_original_subject_first(self):
        original = "Draculina and her three husbands gather in a velvet crypt lounge."
        retry = semantic_art_quality.literal_retry_prompt(
            original,
            "Draculina and Her Three Husbands",
            1,
        )
        self.assertTrue(retry.startswith(original))
        self.assertIn("every named person", retry)
        self.assertIn("abstract architecture", retry)
        self.assertIn("immediately countable", retry)


if __name__ == "__main__":
    unittest.main()
