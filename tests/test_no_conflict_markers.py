"""Guard: no tracked file on main may contain unresolved git merge-conflict markers.

2026-11-22: two art receipts (comet-city-academy AUTHORED-RECRUITS-EMOTIONS and
every-villain-tactics ONE-HIT-CREW-COMBAT-STATES) reached main with literal
conflict markers from a `[skip ci]` receipt-recovery commit, making them invalid
YAML. Fixed in PR #7839; this test makes the next occurrence fail CI.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Built from pieces so this file never matches itself.
_START = "<" * 7
_END = ">" * 7
MARKER = re.compile(rf"^(?:{_START}|{_END})(?: |$)", re.MULTILINE)
TEXT_SUFFIXES = {".yaml", ".yml", ".json", ".md", ".py", ".ts", ".js", ".toml", ".txt"}


def find_conflict_markers(paths: list[Path], root: Path = ROOT) -> list[str]:
    hits = []
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if MARKER.search(text):
            hits.append(str(path.relative_to(root)))
    return hits


def _tracked_text_files() -> list[Path]:
    out = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout
    return [ROOT / p for p in out.split("\0") if p and Path(p).suffix in TEXT_SUFFIXES]


def test_detector_flags_markers(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text(f"a: 1\n{_START} HEAD\nb: 2\n=======\nb: 3\n{_END} abc123\n")
    good = tmp_path / "good.md"
    good.write_text("Fine text mentioning <<<<<<<inline but not at line start.\n")
    assert find_conflict_markers([bad, good], root=tmp_path) == ["bad.yaml"]


def test_no_tracked_file_has_conflict_markers():
    hits = find_conflict_markers(_tracked_text_files())
    assert not hits, f"Unresolved merge-conflict markers committed in: {hits}"
