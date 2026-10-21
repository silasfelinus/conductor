"""MPEG program streams must become complete, readable motion guides for ComfyUI."""
import importlib.util
from pathlib import Path
import shutil
import subprocess

import pytest


WORKER_PATH = (
    Path(__file__).resolve().parents[1]
    / "ops"
    / "home-server"
    / "coat_dance_vace_worker.py"
)
SPEC = importlib.util.spec_from_file_location("coat_dance_mpeg_worker", WORKER_PATH)
worker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(worker)


@pytest.mark.skipif(
    not (shutil.which("ffmpeg") and shutil.which("ffprobe")),
    reason="requires ffmpeg and ffprobe",
)
def test_mpeg_program_stream_stages_as_decodable_mp4_and_repairs_partial_copy(tmp_path):
    # The relay currently writes its MPEG download to source.mp4; ffmpeg must
    # recognize the MPEG program stream by its contents, not the extension.
    source = tmp_path / "source.mp4"
    subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-f", "lavfi", "-i", "testsrc=size=720x480:rate=16:duration=2",
            "-c:v", "mpeg2video", "-f", "mpeg", str(source),
        ],
        check=True, timeout=45,
    )
    assert source.read_bytes()[:4] == b"\\x00\\x00\\x01\\xba"

    guide = tmp_path / "motion_control_000.mp4"
    worker.extract_window(source, 0, guide)
    worker.verify_motion_input(guide)

    comfy_input = tmp_path / "comfy_input"
    comfy_input.mkdir()
    staged = comfy_input / "coatdance_test_000.mp4"
    worker.stage_motion_input(guide, staged)
    worker.verify_motion_input(staged)
    assert staged.read_bytes() == guide.read_bytes()

    # An interrupted old copy must not be mistaken for a finished clip.
    staged.write_bytes(guide.read_bytes()[:256])
    with pytest.raises(ValueError, match="complete, decodable"):
        worker.verify_motion_input(staged)
    worker.stage_motion_input(guide, staged)
    worker.verify_motion_input(staged)
    assert staged.read_bytes() == guide.read_bytes()
    assert not list(comfy_input.glob("*.tmp.mp4"))


def test_comfy_decoder_error_reports_node_and_exception(monkeypatch, tmp_path):
    def fake_send_json(_base, path, _payload=None):
        if path == "/prompt":
            return {"prompt_id": "mpeg-test"}
        return {
            "mpeg-test": {
                "status": {
                    "status_str": "error",
                    "messages": [
                        ["execution_error", {
                            "node_type": "GetVideoComponents",
                            "exception_type": "InvalidDataError",
                            "exception_message": "Invalid data when processing input",
                        }],
                    ],
                },
            },
        }

    monkeypatch.setattr(worker, "send_json", fake_send_json)
    with pytest.raises(
        RuntimeError,
        match="GetVideoComponents: InvalidDataError: Invalid data",
    ):
        worker.execute_comfy("http://127.0.0.1:8188", {}, tmp_path / "result.mp4")
