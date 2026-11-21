"""CI contract: the real opening exporter rejects over-budget queue ledgers."""

import copy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
LEDGER = (
    ROOT
    / "projects/rainbow-bullet-hell-space-princess/art"
    / "OPENING-CLIPS-2-DOODLE.yaml"
)
EXPORTER = ROOT / "scripts/export_rainbow_opening.py"


def preflight(ledger):
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "opening.yaml"
        path.write_text(yaml.safe_dump(ledger))
        return subprocess.run(
            [
                sys.executable,
                str(EXPORTER),
                "--ledger",
                str(path),
                "--check-queue-budget",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )


class OpeningBudgetCI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.approved = yaml.safe_load(LEDGER.read_text())

    def test_approved_opening_is_queueable(self):
        result = preflight(self.approved)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("opening WAN queue budget: OK", result.stdout)

    def test_ten_second_shot_is_rejected_before_artjob(self):
        ledger = copy.deepcopy(self.approved)
        shot = next(
            subject
            for subject in ledger["subjects"]
            if subject["lane"] == "wan-mp4"
        )
        shot["duration"] = 10
        result = preflight(ledger)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(shot["key"], result.stderr)
        self.assertIn("do not enqueue", result.stderr)

    def test_excessive_fps_is_rejected_before_artjob(self):
        ledger = copy.deepcopy(self.approved)
        lane = next(
            lane for lane in ledger["lanes"] if lane["key"] == "wan-mp4"
        )
        lane["fps"] = 120
        result = preflight(ledger)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("opening clip budget", result.stderr)


if __name__ == "__main__":
    unittest.main()
