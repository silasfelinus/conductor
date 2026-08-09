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
    pipeline.DESIGN_BRIEF,
    pipeline.SEED_CONTRACT,
    pipeline.IDEA_TEMPLATE,
    pipeline.SHIPPED,
    pipeline.API_SURFACE,
    pipeline.OUTLINE_CHECKER,
    pipeline.ROADMAP,
    pipeline.BUILDER,
    pipeline.CLAUDE,
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
    """A real granted capability, not a mention of one.

    This fixture used to append "# KR_API_TOKEN" — a comment, chosen to keep the
    file valid YAML. That passed for the wrong reason once the digest workflow
    grew a comment explaining why it deliberately has no such token: the guard
    flagged the explanation. The capability is what matters, so grant one.
    """
    root = _copy_contract(tmp_path)
    digest = root / pipeline.DIGEST
    digest.write_text(
        digest.read_text(encoding="utf-8")
        + "\n        env:\n          KR_API_TOKEN: ${{ secrets.KR_API_TOKEN }}\n",
        encoding="utf-8",
    )

    errors = pipeline.check_pipeline(root)

    assert any("Daily Digest must be read-only" in error for error in errors)


def test_documenting_an_absent_capability_is_not_granting_it(tmp_path):
    """A comment grants nothing, so it must not read as a violation.

    The digest workflow says, in prose, that it deliberately receives no
    KR_API_TOKEN and why. That sentence is the opposite of the thing being
    guarded against, and a substring search cannot tell them apart.
    """
    root = _copy_contract(tmp_path)
    digest = root / pipeline.DIGEST
    digest.write_text(
        digest.read_text(encoding="utf-8")
        + "\n      # No KR_API_TOKEN here: the digest stays read-only.\n",
        encoding="utf-8",
    )

    errors = pipeline.check_pipeline(root)

    assert not any("Daily Digest must be read-only" in error for error in errors)


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
def test_stale_project_brief_is_rejected(tmp_path):
    root = _copy_contract(tmp_path)
    brief = root / pipeline.DESIGN_BRIEF
    brief.write_text(brief.read_text(encoding="utf-8") + "\nThe 8-stage manual path returns.\n", encoding="utf-8")
    assert any("DESIGN-BRIEF.md" in error for error in pipeline.check_pipeline(root))


def test_builder_cannot_accept_removed_page_or_narrator_path(tmp_path):
    root = _copy_contract(tmp_path)
    builder = root / pipeline.BUILDER
    builder.write_text(
        builder.read_text(encoding="utf-8")
        .replace("PAGE_URL = KR_BASE_URL", 'PAGE_URL = f"{KR_BASE_URL}/daily-dream"')
        + '\n# 5. Narrator\nPOST = "/api/bots"\n',
        encoding="utf-8",
    )
    errors = pipeline.check_pipeline(root)
    assert any("builder" in error.lower() for error in errors)


def test_roadmap_cannot_reactivate_staged_dream_instructions(tmp_path):
    root = _copy_contract(tmp_path)
    roadmap = root / pipeline.ROADMAP
    roadmap.write_text(
        roadmap.read_text(encoding="utf-8").replace(
            "CURRENT CONTRACT:", "advance it exactly ONE stage. CURRENT CONTRACT:"
        ),
        encoding="utf-8",
    )
    assert any("roadmap t-006" in error for error in pipeline.check_pipeline(root))
