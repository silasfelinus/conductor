#!/usr/bin/env python3
"""Validate the single-writer Daily Dream pipeline contract.

This is intentionally repository-local and network-free so it can run in CI and in
an agent health check. It guards architecture, not production credentials.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HOURLY = Path(".github/workflows/hourly-conductor.yml")
DIGEST = Path(".github/workflows/daily-digest.yml")
SUMMARY = Path("scripts/build_conductor_summary.py")
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
CLAUDE = Path("CLAUDE.md")

REQUIRED_FILES = (
    HOURLY,
    DIGEST,
    SUMMARY,
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


def _without_yaml_comments(text: str) -> str:
    """Workflow YAML with `#` comment lines dropped.

    The forbidden-capability scan below is a substring search, so a comment
    EXPLAINING that a capability is deliberately absent used to trip it — the
    daily-digest step that authors the dream documents "no KR_API_TOKEN, and
    here is why", and that sentence read as the capability itself. Same class of
    false positive as a test failing on its own explanation. Only full-line
    comments are stripped: a `#` inside a quoted run-step string is not a
    comment and dropping it could hide a real capability.
    """
    return "\n".join(
        line for line in text.splitlines() if not line.lstrip().startswith("#")
    )


def _builder_call_count(source: str) -> int:
    """Count executable build_dream_records.ensure_records() calls, not prose."""
    tree = ast.parse(source)
    count = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if (
            isinstance(func, ast.Attribute)
            and func.attr == "ensure_records"
            and isinstance(func.value, ast.Name)
            and func.value.id == "build_dream_records"
        ):
            count += 1
    return count


def check_pipeline(root: Path = ROOT) -> list[str]:
    """Return human-readable contract violations, or an empty list when healthy."""
    errors: list[str] = []
    content = {path: _read(root, path, errors) for path in REQUIRED_FILES}

    hourly = content[HOURLY]
    digest = content[DIGEST]
    summary = content[SUMMARY]
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
    claude = content[CLAUDE]

    try:
        builder_calls = _builder_call_count(summary)
    except SyntaxError as error:
        errors.append(f"could not parse build_conductor_summary.py: {error}")
    else:
        if builder_calls != 1:
            errors.append(
                "build_conductor_summary.py must call "
                "build_dream_records.ensure_records() exactly once"
            )

    if hourly.count("python scripts/build_conductor_summary.py") != 1:
        errors.append(
            "Hourly Conductor must invoke build_conductor_summary.py exactly once"
        )

    hourly_sequence = (
        "python scripts/build_conductor_summary.py",
        "python scripts/apply_daily_dream_facets.py",
        "git add CONDUCTOR-REPORT.md projects/dream-cycle/backlog/ projects/art-prompts.yaml",
        "Verify daily-dream creation result",
    )
    if not _in_order(hourly, hourly_sequence):
        errors.append(
            "Hourly Conductor must build, attach Facets, commit evidence, then verify"
        )

    for forbidden in (
        "KR_API_TOKEN",
        "build_dream_records",
        "apply_daily_dream_facets",
    ):
        if forbidden in _without_yaml_comments(digest):
            errors.append(
                f"Daily Digest must be read-only; found forbidden capability {forbidden!r}"
            )

    digest_sequence = (
        "python scripts/build_digest.py",
        "python scripts/enrich_daily_dream_digest.py",
        "python scripts/validate_digest.py",
        "python scripts/build_digest_email_v2.py",
    )
    if not _in_order(digest, digest_sequence):
        errors.append(
            "Daily Digest must build, enrich, validate, and render in that order"
        )

    for workflow in sorted((root / ".github/workflows").glob("*.yml")):
        if workflow.name == "daily-dream-contract.yml":
            continue
        text = workflow.read_text(encoding="utf-8")
        if "build_dream_records.py" in text or "ensure_records(" in text:
            errors.append(
                f"workflow {workflow.name} directly invokes the object builder; "
                "only Hourly Conductor may reach it through build_conductor_summary.py"
            )

    allowed_callers = {
        "build_conductor_summary.py",
        "build_dream_records.py",
        "check_daily_dream_pipeline.py",
    }
    for script in sorted((root / "scripts").glob("*.py")):
        if script.name in allowed_callers:
            continue
        text = script.read_text(encoding="utf-8")
        if "build_dream_records.ensure_records(" in text or "build_dream_records.run_build(" in text:
            errors.append(
                f"script {script.name} is a second daily-dream object-builder caller"
            )

    if "sole object writer" not in pipeline.casefold():
        errors.append("PIPELINE.md must identify the sole object writer")
    if "digest workflow receives no `kr_api_token`" not in pipeline.casefold():
        errors.append("PIPELINE.md must state that digest reporting is read-only")
    if "scripts/build_dream_records.py" not in creation_spec:
        errors.append("CREATION-SPEC.md must name the canonical builder")
    if "sole object writer" not in dream_spec.casefold():
        errors.append("specs/dream.md must name the sole object writer")
    if "only files eligible to create daily-dream database objects" not in backlog_readme:
        errors.append("backlog README must distinguish proposals from idea inventory")

    retired_phrases = (
        "parallel daily-dream fast lane",
        "fuller idle-loop path",
        "## The 8 stages",
    )
    for path, text in (
        (CREATION_SPEC, creation_spec),
        (DREAM_SPEC, dream_spec),
    ):
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
            errors.append(
                f"active dream specs must not authorize direct object writes: {endpoint}"
            )

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

    return errors

def main() -> int:
    errors = check_pipeline()
    if errors:
        print("Daily Dream pipeline is unhealthy:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Daily Dream pipeline healthy: one proposal path, one object writer, "
        "read-only digest reporting."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
