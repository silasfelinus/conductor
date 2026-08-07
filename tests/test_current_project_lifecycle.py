from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def test_current_repository_roadmaps_pass_lifecycle_validation() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_roadmaps.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
