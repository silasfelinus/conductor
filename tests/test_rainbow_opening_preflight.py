"""Offline regressions for fail-closed Rainbow opening clip delivery."""
import importlib.util
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/export_rainbow_opening.py"
spec = importlib.util.spec_from_file_location("rainbow_opening_preflight", SCRIPT)
opening = importlib.util.module_from_spec(spec)
spec.loader.exec_module(opening)

MP4 = b"\x00\x00\x00\x18ftypisom" + b"\x00" * 16
WEBM = b"\x1a\x45\xdf\xa3" + b"\x00" * 16


def test_rejects_unknown_container_without_decoding():
    with patch.object(opening, "clip_frames") as decode:
        assert opening.validated_clip(b"not a movie", "intro-cats-launch") is None
        decode.assert_not_called()


def test_rejects_corrupt_mp4_and_uses_still():
    with patch.object(opening.subprocess, "run", side_effect=OSError("ffprobe missing")):
        assert opening.validated_clip(MP4, "intro-vivi-comet") is None


def test_rejects_undersized_video_before_decode():
    from subprocess import CompletedProcess
    probe = CompletedProcess([], 0, stdout='{"streams":[{"width":320,"height":180}]}')
    with patch.object(opening.subprocess, "run", return_value=probe), patch.object(opening, "clip_frames") as decode:
        assert opening.validated_clip(MP4, "intro-azure-prism") is None
        decode.assert_not_called()


def test_mp4_and_webm_headers_reach_ffprobe():
    """Recognised containers must be probed, not rejected as unknown."""
    from subprocess import CompletedProcess
    probe = CompletedProcess([], 0, stdout='{"streams":[{"width":320,"height":180}]}')
    for payload in (MP4, WEBM):
        with patch.object(opening.subprocess, "run", return_value=probe) as run:
            assert opening.validated_clip(payload, "intro-cats-launch") is None
            run.assert_called_once()


def test_rejects_short_decoded_video():
    from subprocess import CompletedProcess
    probe = CompletedProcess([], 0, stdout='{"streams":[{"width":832,"height":480}]}')
    with patch.object(opening.subprocess, "run", return_value=probe), patch.object(opening, "clip_frames", return_value=[]):
        assert opening.validated_clip(MP4, "intro-solenne-halo") is None


def test_failed_download_falls_back_to_still():
    with patch.object(opening, "download", side_effect=OSError("404")):
        assert opening.safe_clip_download(12345, "intro-cats-launch") is None
