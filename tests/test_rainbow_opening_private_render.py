"""Private Rainbow opening cut: no partial previews or chroma-green false approval."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from scripts import export_rainbow_opening as opening
from scripts import inspect_rainbow_opening_preview as preview


class PrivateOpeningTests(unittest.TestCase):
    def test_timeline_has_eight_shots_and_exact_fifteen_seconds(self):
        timeline = preview.shot_timeline()
        self.assertEqual(len(timeline), 8)
        self.assertEqual(timeline[0]["start"], 0)
        self.assertAlmostEqual(
            timeline[-1]["start"] + timeline[-1]["duration"], 15, places=5,
        )

    def test_receipts_require_every_completed_render_and_art_image(self):
        ledger = {
            "round": opening.DOODLE_ROUND,
            "subjects": [
                {
                    "key": key,
                    "source_image_id": 262203 + index,
                    "jobs": {"wan-mp4": 70000 + index},
                    "art": {
                        "wan-mp4": {
                            "status": "DONE", "art_image_id": 270000 + index,
                        },
                    },
                }
                for index, (key, _) in enumerate(opening.DOODLE_SHOTS)
            ],
        }
        receipt = preview.validated_receipts(ledger)
        self.assertEqual(len(receipt), 8)
        self.assertEqual(receipt[2]["key"], "intro-dolphin-armada")
        self.assertEqual(receipt[2]["art_job_id"], 70002)
        for bad in ("RUNNING", "FAILED"):
            with self.subTest(state=bad):
                ledger["subjects"][2]["art"]["wan-mp4"]["status"] = bad
                with self.assertRaisesRegex(ValueError, "not DONE"):
                    preview.validated_receipts(ledger)
        ledger["subjects"][2]["art"]["wan-mp4"]["status"] = "DONE"
        ledger["subjects"][2]["art"]["wan-mp4"]["art_image_id"] = None
        with self.assertRaisesRegex(ValueError, "not DONE"):
            preview.validated_receipts(ledger)

    def test_chroma_green_detection(self):
        self.assertEqual(
            preview.chroma_green_fraction(Image.new("RGB", (80, 80), "#00ff00")),
            1.0,
        )
        self.assertEqual(
            preview.chroma_green_fraction(Image.new("RGB", (80, 80), "#ac42b2")),
            0.0,
        )
        gradient = Image.new("RGB", (160, 90), "#401359")
        for y in range(90):
            for x in range(160):
                if x < 32:
                    gradient.putpixel((x, y), (3, 243, 3))
        self.assertLess(preview.chroma_green_fraction(gradient), 0.4)

    def test_strict_preview_rejects_pending_wan_before_reading_track(self):
        with tempfile.TemporaryDirectory() as tmp:
            track = Path(tmp) / "sound.mp3"
            track.write_bytes(b"audio")
            sources = [
                (key, beats, 262212, None if index == 2 else 9000 + index)
                for index, (key, beats) in enumerate(opening.DOODLE_SHOTS)
            ]
            with patch.object(
                opening, "shot_sources", return_value=iter(sources),
            ), patch.object(opening, "download") as download:
                result = opening.main([
                    "--track", str(track), "--require-all-clips",
                    "--out", str(Path(tmp) / "opening.mp4"),
                ])
            self.assertEqual(result, opening.EXIT_RENDERING)
            download.assert_not_called()

    def test_strict_preview_rejects_unusable_wan_even_with_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            track = Path(tmp) / "sound.mp3"
            track.write_bytes(b"audio")
            source = [
                (key, beats, 262212, 9000 + index)
                for index, (key, beats) in enumerate(opening.DOODLE_SHOTS)
            ]

            def render(sources, last, accepted, rejected):
                last.append(Image.new("RGB", opening.SIZE, "pink"))
                accepted.extend(key for key, _, _, _ in sources[:-1])
                rejected.append(sources[-1][0])
                return iter(())

            def encode(frames, audio, mp4, seconds):
                mp4.write_bytes(b"mp4")
                mp4.with_suffix(".webm").write_bytes(b"webm")
                return round(seconds * opening.FPS)

            with patch.object(
                opening, "shot_sources", return_value=iter(source),
            ), patch.object(
                opening, "render", side_effect=render,
            ), patch.object(
                opening, "encode", side_effect=encode,
            ), patch.object(opening, "verify_encoded_media"):
                result = opening.main([
                    "--track", str(track), "--require-all-clips",
                    "--out", str(Path(tmp) / "opening.mp4"),
                ])
            self.assertEqual(result, opening.EXIT_RENDERING)
            self.assertFalse((Path(tmp) / "opening.mp4").exists())

    def test_stills_only_cannot_claim_strict_wan_completion(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = opening.main([
                "--out", str(Path(tmp) / "opening.mp4"),
                "--stills-only", "--require-all-clips",
            ])
            self.assertEqual(result, opening.EXIT_ERROR)


if __name__ == "__main__":
    unittest.main()
