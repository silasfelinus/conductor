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
    pipeline.REPORT_ONLY,
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
    pipeline.AUTHOR,
    pipeline.SUBMIT,
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


def test_repository_has_one_ordered_daily_dream_writer():
    assert pipeline.check_pipeline(ROOT) == []


def test_digest_must_keep_object_writing_credentials(tmp_path):
    root = _copy_contract(tmp_path)
    digest = root / pipeline.DIGEST
    digest.write_text(
        digest.read_text(encoding="utf-8").replace("KR_API_TOKEN", "REMOVED_TOKEN"),
        encoding="utf-8",
    )

    errors = pipeline.check_pipeline(root)

    assert any("must receive KR_API_TOKEN" in error for error in errors)


def test_digest_cannot_author_twice(tmp_path):
    root = _copy_contract(tmp_path)
    digest = root / pipeline.DIGEST
    digest.write_text(
        digest.read_text(encoding="utf-8")
        + "\n      - name: Wrong second author\n        run: python scripts/author_dream_proposal.py\n",
        encoding="utf-8",
    )

    errors = pipeline.check_pipeline(root)

    assert any("author exactly once" in error for error in errors)


def test_hourly_cannot_regain_builder_side_effect(tmp_path):
    root = _copy_contract(tmp_path)
    hourly = root / pipeline.HOURLY
    hourly.write_text(
        hourly.read_text(encoding="utf-8")
        + "\n      - name: Wrong builder\n        run: python scripts/build_dream_records.py\n",
        encoding="utf-8",
    )

    errors = pipeline.check_pipeline(root)

    assert any("Hourly Conductor must not perform Daily Dream creation work" in error for error in errors)


def test_second_workflow_builder_caller_is_rejected(tmp_path):
    root = _copy_contract(tmp_path)
    rogue = root / ".github/workflows/rogue-dream.yml"
    rogue.write_text(
        "name: rogue\non: workflow_dispatch\njobs:\n  rogue:\n    runs-on: ubuntu-latest\n    steps:\n"
        "      - run: python scripts/build_dream_records.py\n",
        encoding="utf-8",
    )

    errors = pipeline.check_pipeline(root)

    assert any("only daily-digest.yml may" in error for error in errors)


def test_digest_order_cannot_submit_art_before_build(tmp_path):
    root = _copy_contract(tmp_path)
    digest = root / pipeline.DIGEST
    text = digest.read_text(encoding="utf-8")
    build = "python scripts/build_dream_records.py"
    submit = "python scripts/submit_daily_dream_art.py"
    text = text.replace(build, "__BUILD__").replace(submit, build).replace("__BUILD__", submit)
    digest.write_text(text, encoding="utf-8")

    errors = pipeline.check_pipeline(root)

    assert any("author, build, attach Facets, submit ArtJobs" in error for error in errors)


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
    brief.write_text(
        brief.read_text(encoding="utf-8") + "\nThe 8-stage manual path returns.\n",
        encoding="utf-8",
    )
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
