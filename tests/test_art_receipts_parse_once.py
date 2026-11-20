"""Regression: receipt sweeps must not parse opted-in YAML ledgers twice."""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import check_auto_art_receipts as receipts
import sweep_art_ledgers as sweep


class ReceiptParseOnceTests(unittest.TestCase):
    def test_audit_reuses_discovery_parse(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / "projects" / "comet-city-academy" / "art"
            folder.mkdir(parents=True)
            ledger = folder / "round.yaml"
            ledger.write_text(
                "auto_submit: true\\nlanes:\\n  - key: portrait\\n"
                "subjects:\\n  - key: captain\\n    jobs: {}\\n"
            )
            original = sweep.yaml.safe_load
            parses = []

            def counted(value):
                parses.append(value)
                return original(value)

            with patch.object(sweep.yaml, "safe_load", side_effect=counted):
                found = sweep.find_ledgers(root, with_data=True)
                self.assertEqual(len(found), 1)
                path, data = found[0]
                with patch.object(receipts, "last_commit_timestamp", return_value=1):
                    self.assertTrue(
                        receipts.missing_receipts(
                            path, now=100000, root=root, data=data
                        )
                    )
            self.assertEqual(len(parses), 1)

    def test_default_discovery_still_returns_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / "projects" / "demo" / "art"
            folder.mkdir(parents=True)
            path = folder / "round.yaml"
            path.write_text("auto_submit: true\\nlanes: []\\nsubjects: []\\n")
            self.assertEqual(sweep.find_ledgers(root), [path])


if __name__ == "__main__":
    unittest.main()
