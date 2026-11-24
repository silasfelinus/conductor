"""The Rainbow asset coverage ledger joins shipped files to their provenance and to the code that uses them."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("coverage", ROOT / "scripts" / "build_rainbow_asset_coverage.py")
coverage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(coverage)


def test_shipped_files_are_traced_and_checked_against_the_code(tmp_path):
    kr = tmp_path / "kind_robots"
    art = kr / "public" / "rainbow-princess-art"
    (art / "alt").mkdir(parents=True)
    (art / "alt" / "x1-sky.webp").write_bytes(b"x" * 2048)
    (art / "lost").mkdir()
    (art / "lost" / "orphan.webp").write_bytes(b"y")
    code = kr / "utils" / "arcade" / "games"
    code.mkdir(parents=True)
    (code / "rainbowDetourPlanes.ts").write_text("const sky = `alt/x1-sky`\n")
    text, summary = coverage.build(kr)
    assert summary["files"] == 2
    assert summary["wired"] == 1, "only the file the code names is wired"
    sky = next(line for line in text.splitlines() if "alt/x1-sky.webp" in line)
    assert "GEN2-ROUND-2.yaml" in sky and "252085" in sky and "| yes |" in sky, sky
    orphan = next(line for line in text.splitlines() if "orphan.webp" in line)
    assert "legacy round" in orphan and "| NO |" in orphan
