import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "worker_task_status.py"


def write_roadmap(tmp_path: Path) -> None:
    roadmap = tmp_path / "projects" / "demo" / "roadmap.yaml"
    roadmap.parent.mkdir(parents=True)
    roadmap.write_text(
        "project: demo\n"
        "kind: software\n"
        "tasks:\n"
        "- id: t-001\n"
        "  title: Demo task\n"
        "  status: ready\n"
        "  owner: null\n"
        "  updated: '2026-01-01T00:00:00Z'\n"
        "  passes: 0\n"
        "  stakes: reversible\n"
        "  note: old note\n"
        "- id: t-002\n"
        "  title: Other task\n"
        "  status: ready\n"
        "  owner: null\n"
        "  passes: 0\n"
    )


def copy_scripts(tmp_path: Path) -> None:
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    for name in ("set_task_field.py", "worker_task_status.py"):
        (scripts / name).write_text((ROOT / "scripts" / name).read_text())


def run_helper(tmp_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(tmp_path / "scripts" / "worker_task_status.py"), *args],
        cwd=tmp_path,
        text=True,
        capture_output=True,
    )


def test_claim_sets_worker_lifecycle_fields(tmp_path):
    write_roadmap(tmp_path)
    copy_scripts(tmp_path)

    result = run_helper(tmp_path, "claim", "demo", "t-001")

    assert result.returncode == 0, result.stderr
    text = (tmp_path / "projects" / "demo" / "roadmap.yaml").read_text()
    assert "  status: claimed\n" in text
    assert "  owner: worker\n" in text
    assert "  updated: '2026-01-01T00:00:00Z'\n" not in text
    assert "- id: t-002\n  title: Other task\n  status: ready\n" in text


def test_done_can_replace_note_without_touching_other_task(tmp_path):
    write_roadmap(tmp_path)
    copy_scripts(tmp_path)

    result = run_helper(tmp_path, "done", "demo", "t-001", "--note", "Completed in PR #999.")

    assert result.returncode == 0, result.stderr
    text = (tmp_path / "projects" / "demo" / "roadmap.yaml").read_text()
    assert "  status: done\n" in text
    assert "  note: 'Completed in PR #999.'\n" in text
    assert "- id: t-002\n  title: Other task\n  status: ready\n" in text


def test_passes_updates_count(tmp_path):
    write_roadmap(tmp_path)
    copy_scripts(tmp_path)

    result = run_helper(tmp_path, "passes", "demo", "t-001", "2")

    assert result.returncode == 0, result.stderr
    text = (tmp_path / "projects" / "demo" / "roadmap.yaml").read_text()
    assert "  passes: 2\n" in text
