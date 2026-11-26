"""Startup stays small and the selector reuses its roadmap snapshot."""
import json
import os
from pathlib import Path
import subprocess
from unittest.mock import patch

from scripts import run_worker

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / ".claude/hooks/session-start.sh"


def test_directed_startup_is_small_and_keeps_secret_bootstrap(tmp_path):
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts/install_secret_hooks.py").write_text(
        "from pathlib import Path\nPath('installed').touch()\n"
    )
    (tmp_path / "TALKBACK.md").write_text("DO_NOT_LOAD_HISTORY\n" * 100)
    env = dict(os.environ, CLAUDE_CODE_REMOTE="true", CLAUDE_PROJECT_DIR=str(tmp_path))
    result = subprocess.run(
        ["bash", str(HOOK)], cwd=tmp_path, env=env, text=True,
        capture_output=True, check=True, timeout=15,
    )
    assert (tmp_path / "installed").exists()
    message = json.loads(result.stdout)["message"]
    assert len(message) < 800
    assert "DO_NOT_LOAD_HISTORY" not in message
    assert "explicit work" in message and "select_role.py once" in message


def test_nonremote_startup_is_noop(tmp_path):
    result = subprocess.run(
        ["bash", str(HOOK)], cwd=tmp_path,
        env=dict(os.environ, CLAUDE_CODE_REMOTE="false", CLAUDE_PROJECT_DIR=str(tmp_path)),
        text=True, capture_output=True, check=True, timeout=15,
    )
    assert result.stdout == ""


def test_queue_uses_provided_snapshot_without_another_read():
    with patch.object(run_worker, "load_roadmaps", side_effect=AssertionError("duplicate load")), \
         patch.object(run_worker, "load_priority", return_value=[]):
        assert run_worker.build_queue_summary([])["ready_task"] is None
