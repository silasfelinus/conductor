import io
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts import export_rainbow_opening as opening


class DoodleOpeningTests(unittest.TestCase):
    def test_doodle_shots_are_exactly_fifteen_seconds(self):
        beats = sum(beats for _, beats in opening.DOODLE_SHOTS)
        self.assertEqual(beats, 44)
        self.assertEqual(round(beats * 60 / opening.BPM, 3), 15.0)
        self.assertEqual(opening.LEDGER.name, "OPENING-CLIPS-2-DOODLE.yaml")

    def test_doodle_ledger_selects_mp4_lane(self):
        subjects = [
            {
                "key": key,
                "source_image_id": 262069 + index,
                "art": {"wan-mp4": {"status": "DONE", "art_image_id": 9000 + index}},
            }
            for index, (key, _) in enumerate(opening.DOODLE_SHOTS)
        ]
        ledger = {"round": opening.DOODLE_ROUND, "subjects": subjects}
        sources = list(opening.shot_sources(ledger, False))
        self.assertEqual(len(sources), 8)
        self.assertEqual([item[3] for item in sources], list(range(9000, 9008)))
        self.assertTrue(all(item[3] is None for item in opening.shot_sources(ledger, True)))

    def test_original_ledger_still_works(self):
        old = {
            "round": "opening-clips-1",
            "subjects": [
                {"key": key, "source_image_id": 100 + index, "art": {}}
                for index, (key, _) in enumerate(opening.SHOTS)
            ],
        }
        self.assertEqual(len(list(opening.shot_sources(old, False))), 9)

    def test_animated_image_fallback(self):
        output = io.BytesIO()
        Image.new("RGB", (32, 18), "pink").save(output, "WEBP")
        frames = opening.clip_frames(output.getvalue())
        self.assertEqual(len(frames), 1)
        self.assertEqual(frames[0].size, opening.SIZE)

    @unittest.skipUnless(shutil.which("ffmpeg"), "ffmpeg unavailable")
    def test_mp4_decoding_and_resizing(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "source.mp4"
            subprocess.run(
                [
                    "ffmpeg", "-v", "error", "-y", "-f", "lavfi",
                    "-i", "color=c=red:s=320x180:r=12:d=0.5",
                    "-c:v", "mpeg4", "-movflags", "+faststart",
                    str(destination),
                ],
                check=True,
                capture_output=True,
            )
            frames = opening.clip_frames(destination.read_bytes())
            self.assertGreaterEqual(len(frames), 4)
            self.assertEqual(frames[0].size, opening.SIZE)


if __name__ == "__main__":
    unittest.main()
