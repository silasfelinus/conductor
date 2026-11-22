import io
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

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

    def test_manifest_clip_count_tracks_only_validated_video(self):
        """A DONE ledger entry with corrupt bytes must not inflate the shipped clip count."""
        accepted = []
        still = io.BytesIO()
        Image.new("RGB", (64, 36), "pink").save(still, "PNG")
        good = [Image.new("RGB", opening.SIZE, "cyan") for _ in range(12)]
        sources = [("valid", 1, 101, 201), ("corrupt", 1, 102, 202)]
        with (
            patch.object(opening, "safe_clip_download", side_effect=[good, None]),
            patch.object(opening, "download", return_value=still.getvalue()),
        ):
            frames = list(opening.render(sources, [], accepted))
        self.assertGreater(len(frames), 0)
        self.assertEqual(accepted, ["valid"])
        self.assertEqual(len(accepted), 1)

    def test_still_only_opening_has_no_accepted_clips(self):
        accepted = []
        still = io.BytesIO()
        Image.new("RGB", (64, 36), "pink").save(still, "PNG")
        with patch.object(opening, "download", return_value=still.getvalue()):
            frames = list(opening.render([("still", 1, 101, None)], [], accepted))
        self.assertGreater(len(frames), 0)
        self.assertEqual(accepted, [])

    def test_rejected_shot_keys_record_only_failed_done_clips(self):
        accepted, rejected = [], []
        still = io.BytesIO()
        Image.new("RGB", (64, 36), "pink").save(still, "PNG")
        good = [Image.new("RGB", opening.SIZE, "cyan") for _ in range(12)]
        sources = [
            ("good-shot", 1, 101, 201),
            ("bad-shot", 1, 102, 202),
            ("pending-shot", 1, 103, None),
        ]
        with (
            patch.object(opening, "safe_clip_download", side_effect=[good, None]),
            patch.object(opening, "download", return_value=still.getvalue()),
        ):
            frames = list(opening.render(sources, [], accepted, rejected))
        self.assertGreater(len(frames), 0)
        self.assertEqual(accepted, ["good-shot"])
        self.assertEqual(rejected, ["bad-shot"])

    def test_still_only_opening_has_no_rejected_shots(self):
        accepted, rejected = [], []
        still = io.BytesIO()
        Image.new("RGB", (64, 36), "pink").save(still, "PNG")
        with patch.object(opening, "download", return_value=still.getvalue()):
            frames = list(opening.render(
                [("pending-shot", 1, 101, None)], [], accepted, rejected
            ))
        self.assertGreater(len(frames), 0)
        self.assertEqual(accepted, [])
        self.assertEqual(rejected, [])

    def test_delivery_report_is_only_sidecar_and_cleans_legacy(self):
        sources = [
            ("accepted", 1, 101, 201),
            ("rejected", 1, 102, 202),
            ("pending", 1, 103, None),
        ]
        with tempfile.TemporaryDirectory() as work:
            target = Path(work) / "opening.mp4"
            legacy = target.with_name("opening-rejected-clips.json")
            legacy.write_text('{"obsolete": true}')
            report = opening.write_delivery_report(
                target, sources, ["accepted"], ["rejected"]
            )
            output = target.with_name("opening-delivery-report.json")
            self.assertFalse(legacy.exists())
            self.assertEqual(json.loads(output.read_text()), report)
            self.assertTrue(output.read_text().endswith("\n"))
            self.assertEqual(report["wan_requeue_shots"], ["rejected"])
            self.assertEqual(report["still_fallback_shots"], ["rejected", "pending"])
            self.assertEqual(
                [p.name for p in Path(work).glob("opening-*.json")],
                ["opening-delivery-report.json"],
            )

    def test_delivery_report_distinguishes_rejected_from_pending_stills(self):
        sources = [
            ("accepted", 1, 101, 201),
            ("rejected", 1, 102, 202),
            ("pending", 1, 103, None),
        ]
        report = opening.delivery_report(sources, ["accepted"], ["rejected"])
        self.assertEqual(report["shots"], 3)
        self.assertEqual(report["animated_shots"], 1)
        self.assertEqual(report["accepted_shots"], ["accepted"])
        self.assertEqual(report["rejected_shots"], ["rejected"])
        self.assertEqual(report["wan_requeue_shots"], ["rejected"])
        self.assertEqual(report["still_fallback_shots"], ["rejected", "pending"])

    def test_delivery_report_stills_only_does_not_request_wan_rerender(self):
        sources = [("still", 1, 101, None)]
        report = opening.delivery_report(sources, [], [])
        self.assertEqual(report["wan_requeue_shots"], [])
        self.assertEqual(report["still_fallback_shots"], ["still"])

    def test_rejects_long_wan_clip_before_rgb_decode(self):
        payload = b"0000ftyp" + b"video-payload"
        probe = subprocess.CompletedProcess(
            [], 0, stdout=json.dumps({"streams": [{"width": 1280, "height": 720,
                                                     "duration": "90.0", "nb_frames": "1440"}]}),
            stderr="",
        )
        with (
            patch.object(opening.subprocess, "run", return_value=probe),
            patch.object(opening, "clip_frames") as decode,
        ):
            self.assertIsNone(opening.validated_clip(payload, "long-shot"))
            decode.assert_not_called()

    def test_rejects_excessive_frame_count_before_decode(self):
        payload = b"0000ftyp" + b"video-payload"
        probe = subprocess.CompletedProcess(
            [], 0, stdout=json.dumps({"streams": [{"width": 1280, "height": 720,
                                                     "duration": "10.0", "nb_frames": "900"}]}),
            stderr="",
        )
        with (
            patch.object(opening.subprocess, "run", return_value=probe),
            patch.object(opening, "clip_frames") as decode,
        ):
            self.assertIsNone(opening.validated_clip(payload, "oversized-shot"))
            decode.assert_not_called()

    def test_accepts_bounded_clip(self):
        payload = b"0000ftyp" + b"video-payload"
        probe = subprocess.CompletedProcess(
            [], 0, stdout=json.dumps({"streams": [{"width": 1280, "height": 720,
                                                     "duration": "2.0", "nb_frames": "32"}]}),
            stderr="",
        )
        frames = [Image.new("RGB", opening.SIZE, "pink") for _ in range(12)]
        with (
            patch.object(opening.subprocess, "run", return_value=probe),
            patch.object(opening, "clip_frames", return_value=frames),
        ):
            self.assertEqual(opening.validated_clip(payload, "good-shot"), frames)

    def test_decode_command_has_hard_frame_ceiling(self):
        """Even inaccurate ffprobe metadata cannot trigger unbounded RGB output."""
        payload = b"0000ftyp" + b"video-payload"
        frame_bytes = opening.SIZE[0] * opening.SIZE[1] * 3
        fake = subprocess.CompletedProcess([], 0, stdout=b"\x00" * frame_bytes, stderr=b"")
        with patch.object(opening.subprocess, "run", return_value=fake) as run:
            frames = opening.clip_frames(payload)
        self.assertEqual(len(frames), 1)
        command = run.call_args.args[0]
        self.assertEqual(command[command.index("-frames:v") + 1], str(opening.MAX_CLIP_FRAMES))
        self.assertEqual(command[command.index("-t") + 1], str(opening.MAX_CLIP_SECONDS))

    def test_animated_image_frame_budget_rejects_before_decode(self):
        image = unittest.mock.MagicMock()
        image.n_frames = opening.MAX_CLIP_FRAMES + 1
        with patch.object(Image, "open", return_value=image):
            with self.assertRaisesRegex(ValueError, "excessive animated image frames"):
                opening.clip_frames(b"animated-image-payload")
        image.seek.assert_not_called()

    def test_rejects_clip_exceeding_decode_budget(self):
        payload = b"0000ftyp" + b"video-payload"
        probe = subprocess.CompletedProcess(
            [], 0, stdout=json.dumps({"streams": [{
                "width": 1280, "height": 720, "duration": "9.0", "nb_frames": "120"
            }]}), stderr="",
        )
        with (
            patch.object(opening.subprocess, "run", return_value=probe),
            patch.object(opening, "clip_frames") as decode,
        ):
            self.assertIsNone(opening.validated_clip(payload, "over-budget"))
            decode.assert_not_called()

    def test_delivery_validation_checks_both_formats_and_soundtrack(self):
        metadata = {
            "format": {"duration": "15.04"},
            "streams": [
                {"codec_type": "video", "width": 1280, "height": 720},
                {"codec_type": "audio"},
            ],
        }
        probe = subprocess.CompletedProcess([], 0, stdout=json.dumps(metadata), stderr="")
        with patch.object(opening.subprocess, "run", return_value=probe) as run:
            opening.verify_encoded_media(Path("opening.mp4"), 15.0, True)
        self.assertEqual(run.call_count, 2)
        self.assertTrue(run.call_args_list[0].args[0][-1].endswith(".mp4"))
        self.assertTrue(run.call_args_list[1].args[0][-1].endswith(".webm"))

    def test_delivery_validation_rejects_missing_audio_and_short_webm(self):
        good = {
            "format": {"duration": "15.0"},
            "streams": [
                {"codec_type": "video", "width": 1280, "height": 720},
                {"codec_type": "audio"},
            ],
        }
        no_audio = {
            "format": {"duration": "15.0"},
            "streams": [{"codec_type": "video", "width": 1280, "height": 720}],
        }
        short = {**good, "format": {"duration": "2.0"}}
        for broken in (no_audio, short):
            responses = [
                subprocess.CompletedProcess([], 0, stdout=json.dumps(good), stderr=""),
                subprocess.CompletedProcess([], 0, stdout=json.dumps(broken), stderr=""),
            ]
            with self.subTest(broken=broken), patch.object(
                opening.subprocess, "run", side_effect=responses
            ):
                with self.assertRaisesRegex(RuntimeError, "soundtrack missing|encoded duration"):
                    opening.verify_encoded_media(Path("opening.mp4"), 15.0, True)

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
