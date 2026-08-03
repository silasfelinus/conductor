"""Contracts for the coloring-book render gate.

The vision-based semantic gate this file used to cover is gone -- quality is a
human call made in the ArtJob trainer panel. What remains is the mechanical
gate (structural validity only) plus the deterministic re-roll bookkeeping that
handles a render coming back structurally broken.
"""

from __future__ import annotations

import unittest

from scripts import render_retry


class RenderRetryContract(unittest.TestCase):
    def test_retry_seed_changes_deterministically(self):
        first = render_retry.next_retry_seed(840009, 1)
        second = render_retry.next_retry_seed(840009, 2)
        self.assertNotEqual(first, second)
        self.assertNotEqual(first, 840009)
        # Same inputs must always produce the same seed so a re-run of a pass
        # reproduces the identical render rather than exploring a new variant.
        self.assertEqual(first, render_retry.next_retry_seed(840009, 1))

    def test_retry_seed_stays_in_valid_range(self):
        for attempt in range(1, 6):
            seed = render_retry.next_retry_seed(2_147_483_000, attempt)
            self.assertGreaterEqual(seed, 0)
            self.assertLess(seed, 2_147_483_647)

    def test_retry_prompt_keeps_original_subject_first(self):
        retry = render_retry.retry_prompt(
            "A towering stitched monster striding through a flooded street.",
            "Monument Monster",
            1,
        )
        self.assertTrue(retry.startswith("A towering stitched monster"))
        self.assertIn("Monument Monster", retry)
        self.assertIn("Re-render 1", retry)

    def test_retry_prompt_carries_a_reviewer_note(self):
        retry = render_retry.retry_prompt(
            "A towering stitched monster striding through a flooded street.",
            "Monument Monster",
            2,
            note="never a bride -- no gown, no veil",
        )
        self.assertIn("Reviewer note: never a bride", retry)

    def test_retry_prompt_without_a_note_mentions_no_reviewer(self):
        retry = render_retry.retry_prompt("A monster.", "Monster", 1)
        self.assertNotIn("Reviewer note", retry)


class NoVisionDependency(unittest.TestCase):
    """The render gate must never reach for a model credential again."""

    def test_render_retry_module_has_no_vision_surface(self):
        for banned in ("assess_semantic_file", "call_vision", "curate_art"):
            self.assertFalse(
                hasattr(render_retry, banned),
                f"{banned} must not come back -- art quality is a human call",
            )

    def test_consumer_validation_is_mechanical_only(self):
        from scripts import consume_coloring_book_color_art as consumer

        source = consumer.validate_candidate.__doc__ or ""
        self.assertIn("Structural check only", source)
        self.assertFalse(hasattr(consumer, "record_semantic_rejection"))
        self.assertTrue(hasattr(consumer, "record_render_rejection"))


if __name__ == "__main__":
    unittest.main()
