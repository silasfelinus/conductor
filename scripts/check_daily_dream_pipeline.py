#!/usr/bin/env python3
"""Validate the single-writer Daily Dream pipeline contract.

This is intentionally repository-local and network-free so it can run in CI and in
an agent health check. It guards architecture, not production credentials.
"""

from __future__ import annotations

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

REQUIRED_FILES = (
    HOURLY,
    DIGEST,
    SUMMARY,
    PIPELINE,
    CREATION_SPEC,
    DREAM_SPEC,
    BACKLOG_README,
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

    if summary.count("build_dream_records.ensure_records(") != 1:
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
        if forbidden in digest:
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
