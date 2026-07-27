#!/usr/bin/env python3
"""
consume_animation_pitches.py — drain dated pitch artifacts into PITCHES.yaml.

Gap: connector-only Workers (GitHub tools, no local shell/Python) cannot safely
rewrite the whole animation-manager PITCHES.yaml in one PR — a truncated read of a
large file risks a destructive overwrite. Their workaround (see conductor PR #1043,
"Flags for Reviewer") is to add a small dated additive file under
projects/animation-manager/pitches/<date>-<slug>.yaml instead of touching PITCHES.yaml
at all. Nothing ever consumed those files: PR #1043 said as much explicitly ("a later
consolidation pass can fold dated pitch artifacts into the canonical queue once the
repository exposes a safe append processor") and its kaizen suggestion asked for exactly
this script. Left alone, animation-manager/t-006's daily-pitch cadence looks satisfied
by the artifact's existence while PITCHES.yaml — the file check_animation_novelty.py and
t-007's "highest-priority unbuilt pitch" pick both actually read — never sees the entry.
Found orphaned 2026-07-25T07:10:34-07:00 (kintsugi-weather), never consolidated as of
2026-07-27.

Runs entirely local, read-only by default. Each artifact is:
  1. parsed and checked for the required pitch fields,
  2. skipped (and its stale file deleted) if its id is already present in PITCHES.yaml,
  3. assigned the next unused priority (authoritative renumbering — never trusts the
     artifact's own `priority`, so two artifacts queued out of order can't collide),
  4. appended to PITCHES.yaml as a targeted text insertion (not a full YAML re-dump,
     which would reformat every existing entry's folded-scalar style into noise).
The merged result is validated with check_animation_novelty.py --strict against a
temp copy before anything real is written, so a genuine novelty collision aborts the
whole run with nothing touched.

Usage:
  python scripts/consume_animation_pitches.py            # dry run, reports what would land
  python scripts/consume_animation_pitches.py --live      # consolidate + delete consumed artifacts
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
PITCH_DIR = ROOT / "projects" / "animation-manager" / "pitches"
PITCHES_FILE = ROOT / "projects" / "animation-manager" / "PITCHES.yaml"
NOVELTY_SCRIPT = ROOT / "scripts" / "check_animation_novelty.py"

REQUIRED_FIELDS = [
    "id",
    "title",
    "status",
    "priority",
    "surprise",
    "passive_loop",
    "optional_interaction",
    "technique",
    "reduced_motion",
    "performance_risk",
    "novelty",
    "acceptance",
]
FOLDED_FIELDS = [
    "surprise",
    "passive_loop",
    "optional_interaction",
    "technique",
    "reduced_motion",
    "performance_risk",
    "novelty",
]
WRAP_WIDTH = 88
FOLD_THRESHOLD = 90


class ConsumeError(Exception):
    pass


def artifact_files() -> list[Path]:
    if not PITCH_DIR.exists():
        return []
    return sorted(PITCH_DIR.glob("*.yaml"))


def load_pitch(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ConsumeError(f"{path.name}: expected a YAML mapping")
    missing = [f for f in REQUIRED_FIELDS if f not in data]
    if missing:
        raise ConsumeError(f"{path.name}: missing required field(s): {', '.join(missing)}")
    if not isinstance(data["acceptance"], list) or not data["acceptance"]:
        raise ConsumeError(f"{path.name}: 'acceptance' must be a non-empty list")
    return data


def existing_ids_and_max_priority(pitches_text: str) -> tuple[set[str], int]:
    data = yaml.safe_load(pitches_text) or {}
    pitches = data.get("pitches") or []
    ids = {p.get("id") for p in pitches if isinstance(p, dict) and p.get("id")}
    priorities = [p.get("priority") for p in pitches if isinstance(p, dict) and isinstance(p.get("priority"), int)]
    return ids, (max(priorities) if priorities else 0)


def format_field(name: str, value: Any, indent: str = "    ") -> str:
    text = str(value).strip()
    if name in FOLDED_FIELDS and len(text) > FOLD_THRESHOLD:
        wrapped = textwrap.wrap(text, width=WRAP_WIDTH)
        body = "\n".join(f"{indent}  {line}" for line in wrapped)
        return f"{indent}{name}: >\n{body}"
    return f"{indent}{name}: {text}"


def render_block(pitch: dict[str, Any], priority: int) -> str:
    lines = [
        f"  - id: {pitch['id']}",
        f"    title: {pitch['title']}",
        f"    status: {pitch.get('status') or 'pitched'}",
        f"    priority: {priority}",
    ]
    for field in FOLDED_FIELDS:
        lines.append(format_field(field, pitch[field]))
    lines.append("    acceptance:")
    for item in pitch["acceptance"]:
        lines.append(f"      - {str(item).strip()}")
    return "\n".join(lines)


def bump_updated(text: str) -> str:
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    return re.sub(r'^updated: ".*"', f'updated: "{now}"', text, count=1, flags=re.M)


def run_novelty_check(candidate_path: Path) -> tuple[bool, str]:
    result = subprocess.run(
        [sys.executable, str(NOVELTY_SCRIPT), "--pitches", str(candidate_path), "--strict"],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0, (result.stdout + result.stderr)


def consume(live: bool) -> int:
    artifacts = artifact_files()
    if not artifacts:
        print("No pending pitch artifacts to consolidate.")
        return 0

    pitches_text = PITCHES_FILE.read_text(encoding="utf-8")
    ids, max_priority = existing_ids_and_max_priority(pitches_text)

    blocks: list[str] = []
    to_delete: list[Path] = []
    skipped: list[Path] = []

    for path in artifacts:
        try:
            pitch = load_pitch(path)
        except ConsumeError as exc:
            print(f"SKIP (invalid): {exc}")
            continue

        if pitch["id"] in ids:
            print(f"SKIP (already consolidated): {path.name} -- id {pitch['id']!r} already in PITCHES.yaml")
            skipped.append(path)
            continue

        max_priority += 1
        ids.add(pitch["id"])
        blocks.append(render_block(pitch, max_priority))
        to_delete.append(path)
        print(f"STAGE: {path.name} -> priority {max_priority} ({pitch['id']})")

    if not blocks and not skipped:
        print("Nothing to do.")
        return 0

    if not blocks:
        if live:
            for path in skipped:
                path.unlink()
                print(f"REMOVED stale artifact: {path.name}")
        return 0

    new_text = pitches_text
    for block in blocks:
        new_text = new_text.rstrip("\n") + "\n\n" + block + "\n"
    new_text = bump_updated(new_text)

    # Sanity: must still parse as valid YAML with the expected shape.
    reparsed = yaml.safe_load(new_text)
    if not isinstance(reparsed, dict) or not isinstance(reparsed.get("pitches"), list):
        raise ConsumeError("merged PITCHES.yaml failed to parse back into the expected shape")

    with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False, encoding="utf-8") as tmp:
        tmp.write(new_text)
        tmp_path = Path(tmp.name)
    try:
        ok, output = run_novelty_check(tmp_path)
    finally:
        tmp_path.unlink(missing_ok=True)

    if not ok:
        print("ABORT: novelty check failed against the merged result -- nothing written.")
        print(output)
        return 1

    print(output)

    if not live:
        print(f"DRY RUN: would consolidate {len(blocks)} pitch(es) into {PITCHES_FILE}; rerun with --live to apply.")
        return 0

    PITCHES_FILE.write_text(new_text, encoding="utf-8")
    for path in to_delete + skipped:
        path.unlink()
        print(f"REMOVED consumed artifact: {path.name}")
    print(f"Consolidated {len(blocks)} pitch(es) into {PITCHES_FILE}.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="Apply changes (default: dry run)")
    args = parser.parse_args(argv)
    try:
        return consume(live=args.live)
    except ConsumeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
