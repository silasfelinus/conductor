#!/usr/bin/env python3
"""Validate the single-writer Daily Dream pipeline contract.

This repository-local check guards architecture without production credentials. The
morning daily-digest workflow owns the only executable creation sequence; Hourly
Conductor is health/reporting only.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HOURLY = Path(".github/workflows/hourly-conductor.yml")
DIGEST = Path(".github/workflows/daily-digest.yml")
SUMMARY = Path("scripts/build_conductor_summary.py")
REPORT_ONLY = Path("scripts/build_conductor_summary_report_only.py")
PIPELINE = Path("projects/dream-cycle/PIPELINE.md")
CREATION_SPEC = Path("projects/dream-cycle/specs/CREATION-SPEC.md")
DREAM_SPEC = Path("projects/dream-cycle/specs/dream.md")
BACKLOG_README = Path("projects/dream-cycle/backlog/README.md")
DESIGN_BRIEF = Path("projects/dream-cycle/DESIGN-BRIEF.md")
SEED_CONTRACT = Path("projects/dream-cycle/CREATIVE-SEED-CONTRACT.md")
IDEA_TEMPLATE = Path("projects/dream-cycle/backlog/_template.md")
SHIPPED = Path("projects/dream-cycle/SHIPPED.md")
API_SURFACE = Path("projects/dream-cycle/docs/api-surface.md")
OUTLINE_CHECKER = Path("scripts/check_dream_outlines.py")
ROADMAP = Path("projects/dream-cycle/roadmap.yaml")
BUILDER = Path("scripts/build_dream_records.py")
AUTHOR = Path("scripts/author_dream_proposal.py")
SUBMIT = Path("scripts/submit_daily_dream_art.py")
CLAUDE = Path("CLAUDE.md")

REQUIRED_FILES = (
    HOURLY,
    DIGEST,
    SUMMARY,
    REPORT_ONLY,
    PIPELINE,
    CREATION_SPEC,
    DREAM_SPEC,
    BACKLOG_README,
    DESIGN_BRIEF,
    SEED_CONTRACT,
    IDEA_TEMPLATE,
    SHIPPED,
    API_SURFACE,
    OUTLINE_CHECKER,
    ROADMAP,
    BUILDER,
    AUTHOR,
    SUBMIT,
    CLAUDE,
)


def _read(root: Path, path: Path, errors: list[str]) -> str:
    target = root / path
    if not target.exists():
        errors.append(f"missing pipeline file: {path}")
        return ""
    return target.read_text(encoding="utf-8")


def _in_order(text: str, needles: tuple[str, ...]) -> bool:
    cursor = -1
    for needle in needles:
        cursor = text.find(needle, cursor + 1)
        if cursor < 0:
            return False
    return True


def check_pipeline(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    content = {path: _read(root, path, errors) for path in REQUIRED_FILES}

    hourly = content[HOURLY]
    digest = content[DIGEST]
    summary = content[SUMMARY]
    report_only = content[REPORT_ONLY]
    pipeline = content[PIPELINE]
    creation_spec = content[CREATION_SPEC]
    dream_spec = content[DREAM_SPEC]
    backlog_readme = content[BACKLOG_README]
    design_brief = content[DESIGN_BRIEF]
    seed_contract = content[SEED_CONTRACT]
    idea_template = content[IDEA_TEMPLATE]
    shipped = content[SHIPPED]
    api_surface = content[API_SURFACE]
    outline_checker = content[OUTLINE_CHECKER]
    roadmap = content[ROADMAP]
    builder = content[BUILDER]
    submit = content[SUBMIT]
    claude = content[CLAUDE]

    if hourly.count("python scripts/build_conductor_summary_report_only.py") != 1:
        errors.append("Hourly Conductor must invoke the report-only summary entrypoint exactly once")
    for forbidden in ("build_dream_records.py", "apply_daily_dream_facets.py", "submit_daily_dream_art.py"):
        if forbidden in hourly:
            errors.append(f"Hourly Conductor must not perform Daily Dream creation work: {forbidden}")
    if "summary.build_dream_records.ensure_records = report_only_daily_dream" not in report_only:
        errors.append("report-only summary entrypoint must neutralize the legacy ensure_records side effect")

    digest_sequence = (
        "python scripts/author_dream_proposal.py",
        "python scripts/build_dream_records.py",
        "python scripts/apply_daily_dream_facets.py",
        "python scripts/submit_daily_dream_art.py",
        "Commit Daily Dream cycle evidence",
        "Verify Daily Dream cycle",
        "python scripts/build_digest.py",
        "python scripts/enrich_daily_dream_digest.py",
        "python scripts/annotate_daily_dream_art_queue.py",
        "python scripts/validate_digest.py",
        "python scripts/build_digest_email_v2.py",
        "Email via Brevo",
    )
    if not _in_order(digest, digest_sequence):
        errors.append(
            "Daily Digest must author, build, attach Facets, submit ArtJobs, persist evidence, verify, then render/send"
        )
    if digest.count("python scripts/author_dream_proposal.py") != 1:
        errors.append("Daily Digest must author exactly once, at the start of the cycle")
    if digest.count("python scripts/build_dream_records.py") != 1:
        errors.append("Daily Digest must invoke the sole object writer exactly once")
    if "KR_API_TOKEN" not in digest:
        errors.append("Daily Digest now owns object creation and must receive KR_API_TOKEN")

    # Build, Facet, and ArtJob steps may leave useful local evidence even when
    # their final status is failure. The workflow must commit that evidence before
    # it converts those outcomes into a failed cycle, or production rows/jobs can
    # become detached from the canonical ledger.
    evidence_guards = (
        "id: daily_dream_build\n        continue-on-error: true",
        "id: daily_dream_facets\n        if: ${{ steps.daily_dream_build.outcome == 'success' }}\n        continue-on-error: true",
        "id: daily_dream_art\n        if: ${{ steps.daily_dream_build.outcome == 'success' }}\n        continue-on-error: true",
        "- name: Commit Daily Dream cycle evidence\n        if: ${{ always() }}",
        'steps.daily_dream_build.outcome',
        'steps.daily_dream_facets.outcome',
        'steps.daily_dream_art.outcome',
    )
    for guard in evidence_guards:
        if guard not in digest:
            errors.append(f"Daily Digest is missing durable failure-evidence guard: {guard!r}")

    for workflow in sorted((root / ".github/workflows").glob("*.yml")):
        if workflow.name in {"daily-dream-contract.yml", "daily-digest.yml"}:
            continue
        text = workflow.read_text(encoding="utf-8")
        if "build_dream_records.py" in text or "submit_daily_dream_art.py" in text:
            errors.append(
                f"workflow {workflow.name} invokes Daily Dream creation/submission; only daily-digest.yml may"
            )

    if "sole object writer" not in pipeline.casefold():
        errors.append("PIPELINE.md must identify the sole object writer")
    if "author → build → facets → submit artjobs → commit → digest" not in pipeline.casefold():
        errors.append("PIPELINE.md must state the ordered morning cycle")
    if "scripts/build_dream_records.py" not in creation_spec:
        errors.append("CREATION-SPEC.md must name the canonical builder")
    if "sole object writer" not in dream_spec.casefold():
        errors.append("specs/dream.md must name the sole object writer")
    if "only files eligible to create daily-dream database objects" not in backlog_readme:
        errors.append("backlog README must distinguish proposals from idea inventory")
    if "source: dream-cycle" not in submit:
        errors.append("Daily Dream ArtJob submitter must be scoped to source: dream-cycle")
    if "last_art_job_id" not in submit:
        errors.append("Daily Dream ArtJob submitter must persist durable ArtJob ids")

    retired_phrases = (
        "parallel daily-dream fast lane",
        "fuller idle-loop path",
        "## The 8 stages",
    )
    for path, text in ((CREATION_SPEC, creation_spec), (DREAM_SPEC, dream_spec)):
        lowered = text.casefold()
        for phrase in retired_phrases:
            if phrase.casefold() in lowered:
                errors.append(f"{path} still documents retired parallel path: {phrase!r}")

    for endpoint in (
        "POST /api/dreams",
        "POST /api/characters",
        "POST /api/rewards",
        "POST /api/scenarios",
        "POST /api/dream-relations",
        "POST /api/sheets",
    ):
        if endpoint in dream_spec or endpoint in creation_spec:
            errors.append(f"active dream specs must not authorize direct object writes: {endpoint}")

    project_checks = (
        ("DESIGN-BRIEF.md", design_brief, ("exactly six assets", "sole daily dream object writer")),
        ("CREATIVE-SEED-CONTRACT.md", seed_contract, ("seed_facets", "build_dream_proposal.py --brief")),
        ("SHIPPED.md", shipped, ("built-data", "not a second ledger")),
        ("api-surface.md", api_surface, ("not part of the current dated daily dream contract",)),
    )
    for label, surface, required in project_checks:
        lowered = surface.casefold()
        for phrase in required:
            if phrase.casefold() not in lowered:
                errors.append(f"{label} is missing current contract phrase: {phrase!r}")

    stale_surfaces = {
        "DESIGN-BRIEF.md": (design_brief, ("the 8-stage", "2–4", "3–6", "optional narrator")),
        "idea template": (idea_template, ("status: building", "narrator: yes", "## characters")),
        "seed contract": (seed_contract, ("creative_seeds:", "every build must document all three")),
        "outline checker": (outline_checker, ("legacy/manual outlines follow", "characters-count", "narrator-missing")),
        "builder": (builder, ("# 5. narrator", 'page_url = f"{kr_base_url}/daily-dream"')),
        "CLAUDE.md": (claude, ("the active `building` creation (type + next", "next queued outline")),
    }
    for label, (surface, forbidden) in stale_surfaces.items():
        lowered = surface.casefold()
        for phrase in forbidden:
            if phrase.casefold() in lowered:
                errors.append(f"{label} still exposes retired Daily Dream contract: {phrase!r}")

    if "idea inventory" not in idea_template.casefold() or "proposal: false" not in idea_template:
        errors.append("legacy Dream template must be explicitly non-buildable idea inventory")
    if "def _canonical_proposal_errors" not in builder:
        errors.append("object builder must enforce the exact six-asset input contract")
    if "page_url = kr_base_url" not in builder.casefold():
        errors.append("object builder must not emit the removed /daily-dream page URL")

    t020_start = roadmap.find("  - id: t-020")
    t020_end = roadmap.find("  - id: t-021", t020_start)
    if t020_start < 0 or "status: done" not in roadmap[t020_start:t020_end]:
        errors.append("roadmap t-020 must be closed after correcting the removed page reference")
    t006_start = roadmap.find("  - id: t-006")
    t006_end = roadmap.find("  - id: t-007", t006_start)
    t006 = roadmap[t006_start:t006_end].casefold()
    if "advance it exactly one stage" in t006 or "stage 3" in t006:
        errors.append("roadmap t-006 still contains executable retired stage instructions")

    # The underlying summary module still contains its historical builder call for
    # compatibility; only the report-only entrypoint is executable from Hourly.
    if "build_dream_records.ensure_records" not in summary:
        errors.append("summary compatibility contract unexpectedly changed; update report-only wrapper/check together")

    return errors


def main() -> int:
    errors = check_pipeline()
    if errors:
        print("Daily Dream pipeline is unhealthy:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Daily Dream pipeline healthy: one ordered morning cycle, one object writer, "
        "and an hourly report-only sweep."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
