"""VACE overwrite mixing stays deterministic, including legacy full-strength jobs."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parents[1] / "ops/home-server"
SPEC = importlib.util.spec_from_file_location(
    "coat_dance_vace_worker", HERE / "coat_dance_vace_worker.py"
)
worker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(worker)


class OverwriteStrengthTests(unittest.TestCase):
    def test_percentages_and_legacy_default(self):
        self.assertEqual(worker.overwrite_strength({"renderRecipe": {}}), 100)
        for value in (0, 25, 50, 100):
            self.assertEqual(worker.overwrite_strength(
                {"renderRecipe": {"overwriteStrength": value}}
            ), value)
        for value in (-1, 101, 42.5, "50", None, True):
            with self.assertRaises(ValueError):
                worker.overwrite_strength(
                    {"renderRecipe": {"overwriteStrength": value}}
                )

    def test_blend_retains_source_audio_and_frame_count(self):
        for strength in (0, 35, 75, 100):
            commands = []
            with patch.object(worker, "run", side_effect=commands.append):
                worker.assemble(
                    HERE, Path("source.mp4"),
                    {"startSec": 1.5, "durationSec": 1.0},
                    [Path("styled.mp4")], 16, "720p", strength,
                )
            self.assertEqual(len(commands), 1)
            args = commands[0]
            filters = args[args.index("-filter_complex") + 1]
            if strength < 100:
                self.assertIn("blend=all_expr=", filters)
                self.assertIn(f"B*{strength / 100:.2f}", filters)
                self.assertIn("[1:v]fps=16,scale=720:480", filters)
                self.assertIn("[mixed]", args)
            else:
                self.assertNotIn("blend=", filters)
                self.assertIn("[joined]", args)
            self.assertIn("1:a:0?", args)
            self.assertEqual(args[args.index("-frames:v") + 1], "16")


if __name__ == "__main__":
    unittest.main()
