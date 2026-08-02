from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_daily_dream_pipeline as pipeline  # noqa: E402


CONTRACT_PATHS = (
    pipeline.HOURLY,
    pipeline.DIGEST,
    pipeline.SUMMARY,
    pipeline.PIPELINE,
    pipeline.CREATION_SPEC,
    pipeline.DREAM_SPEC,
    pipeline.BACKLOG_README,
)


def _copy_contract(tmp_path: Path) -> Path:
    for relative in CONTRACT_PATHS:
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, target)

    workflows = tmp_path / ".github/workflows"
    for source in (ROOT / ".github/workflows").glob("*.yml"):
        target = workflows / source.name
        if not target.exists():
            shutil.copy2(source, target)

    scripts = tmp_path / "scripts"
    for source in (ROOT / "scripts").glob("*.py"):
        target = scripts / source.name
        if not target.exists():
            shutil.copy2(source, target)
    return tmp_path


def test_repository_has_one_daily_dream_object_writer():
    assert pipeline.check_pipeline(ROOT) == []


def test_digest_cannot_gain_object_writing_credentials(tmp_path):
    root = _copy_contract(tmp_path)
    digest = root / pipeline.DIGEST
    digest.write_text(
        digest.read_text(encoding="utf-8") + "\n# KR_API_TOKEN\n",
        encoding="utf-8",
    )

    errors = pipeline.check_pipeline(root)

    assert any("Daily Digest must be read-only" in error for error in errors)


def test_second_builder_caller_is_rejected(tmp_path):
    root = _copy_contract(tmp_path)
    (root / "scripts/alternate_daily_dream.py").write_text(
        "import build_dream_records\n"
        "build_dream_records.ensure_records()\n",
        encoding="utf-8",
    )

    errors = pipeline.check_pipeline(root)

    assert any("second daily-dream object-builder caller" in error for error in errors)


def test_direct_rest_playbook_is_rejected(tmp_path):
    root = _copy_contract(tmp_path)
    dream_spec = root / pipeline.DREAM_SPEC
    dream_spec.write_text(
        dream_spec.read_text(encoding="utf-8")
        + "\nLegacy instruction: POST /api/characters by hand.\n",
        encoding="utf-8",
    )

    errors = pipeline.check_pipeline(root)

    assert any("must not authorize direct object writes" in error for error in errors)
