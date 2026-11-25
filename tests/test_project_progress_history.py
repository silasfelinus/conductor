from datetime import datetime
from pathlib import Path
import subprocess
import sys
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from project_progress_history import history, task_counts
from build_digest_email_v2_impl import project_progress_history_section


def test_counts_exclude_recurring_and_cancelled():
    assert task_counts({"tasks": [
        {"status": "done"}, {"status": "review"},
        {"status": "done", "recurring": True}, {"status": "cancelled"},
    ]}) == {"done": 1, "total": 2}


def test_missing_history_is_not_zero(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.email", "test@example.org"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.name", "Test"], check=True)
    path = tmp_path / "projects" / "game" / "roadmap.yaml"
    path.parent.mkdir(parents=True)
    path.write_text("tasks:\n  - status: done\n  - status: ready\n")
    subprocess.run(["git", "-C", str(tmp_path), "add", "."], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "commit", "-qm", "test"], check=True)
    result = history(tmp_path, days=1, now=datetime.now(ZoneInfo("America/Los_Angeles")))
    assert result["series"]["game"] == [None, {"done": 1, "total": 2}]


def test_email_uses_actual_points_and_archive_link():
    html = project_progress_history_section({
        "status": "ready", "dates": ["2026-11-18", "2026-11-25"],
        "series": {"game": [{"done": 2, "total": 4}, {"done": 3, "total": 4}]},
        "masters": {"game": "https://github.com/example/repo/issues/1"},
    })
    assert "50%" in html and "75%" in html and "+1" in html
    assert "/admin/dead-air" in html
    assert "unavailable" in project_progress_history_section(None)
