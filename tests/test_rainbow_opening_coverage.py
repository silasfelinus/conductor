"""Regression tests for Rainbow opening shot coverage preflight."""

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import yaml

from scripts import export_rainbow_opening as opening


def ledger_for(round_name, shots):
    return {
        "round": round_name,
        "subjects": [
            {"key": key, "source_image_id": index + 1}
            for index, (key, _) in enumerate(shots)
        ],
    }


class OpeningCoverageTests(unittest.TestCase):
    def test_valid_doodle_and_legacy_cuts(self):
        for round_name, shots in (
            (opening.DOODLE_ROUND, opening.DOODLE_SHOTS),
            ("legacy-opening", opening.SHOTS),
        ):
            with self.subTest(round=round_name):
                opening.validate_shot_coverage(ledger_for(round_name, shots))

    def test_missing_shot_rejected_in_both_rounds(self):
        for round_name, shots in (
            (opening.DOODLE_ROUND, opening.DOODLE_SHOTS),
            ("legacy-opening", opening.SHOTS),
        ):
            with self.subTest(round=round_name):
                ledger = ledger_for(round_name, shots)
                ledger["subjects"].pop()
                with self.assertRaisesRegex(ValueError, "expected exactly one opening shot"):
                    opening.validate_shot_coverage(ledger)

    def test_duplicate_key_rejected(self):
        ledger = ledger_for(opening.DOODLE_ROUND, opening.DOODLE_SHOTS)
        ledger["subjects"].append(dict(ledger["subjects"][0]))
        with self.assertRaisesRegex(ValueError, "expected exactly one opening shot"):
            opening.validate_shot_coverage(ledger)

    def test_invalid_source_ids_rejected(self):
        for bad in (0, -1, "123", None, True, 1.5):
            with self.subTest(source_id=bad):
                ledger = ledger_for(opening.DOODLE_ROUND, opening.DOODLE_SHOTS)
                ledger["subjects"][0]["source_image_id"] = bad
                with self.assertRaisesRegex(ValueError, "approved source ArtImage ID"):
                    opening.validate_shot_coverage(ledger)

    def test_missing_subject_list_rejected(self):
        with self.assertRaisesRegex(ValueError, "subjects list"):
            opening.validate_shot_coverage({"round": opening.DOODLE_ROUND})

    def test_cli_coverage_failure_has_distinct_prefix(self):
        ledger = ledger_for("legacy-opening", opening.SHOTS)
        ledger["subjects"].pop()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "opening.yaml"
            path.write_text(yaml.safe_dump(ledger))
            errors = io.StringIO()
            with contextlib.redirect_stderr(errors):
                result = opening.main(["--ledger", str(path), "--check-queue-budget"])
        self.assertEqual(result, opening.EXIT_ERROR)
        self.assertIn("opening shot coverage:", errors.getvalue())
        self.assertNotIn("opening WAN queue budget:", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
