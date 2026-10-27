"""Twenty distinct physically co-located Serendipity casino concept art requests."""
from __future__ import annotations

import unittest

from scripts.submit_space_couch_casinos import (
    EXPECTED, parse_ledger, reconcile, normalized,
)
from scripts.enqueue_art_requests import compose_prompt


class CasinoArtManifestTests(unittest.TestCase):
    def test_exact_twenty_original_venues(self):
        _, data = parse_ledger()
        self.assertEqual(len(data["subjects"]), EXPECTED)
        subjects = data["subjects"]
        ids = [s["key"].removeprefix("space-couch-serendipity-").removesuffix("-environment") for s in subjects]
        self.assertEqual(len(set(ids)), EXPECTED)
        self.assertIn("mesa", ids)
        self.assertIn("arcade", ids)
        self.assertTrue(all(s["asset"] == f"game-of-captains/venues/{id}" for id, s in zip(ids, subjects)))
        self.assertTrue(all(s["size"] == "1344x768" for s in subjects))
        self.assertTrue(all(s.get("jobs", {}) == {} or s.get("jobs", {}).get("krea2") for s in subjects))
        prompts = [compose_prompt(data["lanes"][0], item) for item in subjects]
        self.assertEqual(len(set(map(normalized, prompts))), EXPECTED)
        for prompt in prompts:
            self.assertIn("casino towers", prompt.lower())
            self.assertIn("bar is physically nested within the casino", prompt.lower())
            self.assertIn("living cobalt blue alien", prompt.lower())
            self.assertIn("scarlet velvet couch", prompt.lower())
        self.assertTrue(any("tex-mex" in prompt.lower() for prompt in prompts))
        self.assertTrue(any("arcade sports bar" in prompt.lower() for prompt in prompts))

    def test_reconcile_exact_prompt_and_never_repost(self):
        _, data = parse_ledger()
        first, second = data["subjects"][:2]
        sample = compose_prompt(data["lanes"][0], first)
        matches = [{"id": 95123, "projectSlug": "game-of-captains", "payload": {"promptString": sample}}]
        self.assertEqual(reconcile(data, matches), 1)
        self.assertEqual(first["jobs"]["krea2"], 95123)
        self.assertEqual(second["jobs"], {})
        self.assertEqual(reconcile(data, matches), 0)

    def test_reject_duplicate_remote_without_valid_artjob(self):
        _, data = parse_ledger()
        sample = compose_prompt(data["lanes"][0], data["subjects"][0])
        with self.assertRaises(RuntimeError):
            reconcile(data, [{"id": None, "payload": {"promptString": sample}}])


if __name__ == "__main__":
    unittest.main()
