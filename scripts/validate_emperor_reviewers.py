#!/usr/bin/env python3
"""Validate Emperor of Dust second-pass reviewer evidence records."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PLAYTEST = ROOT / "projects/emperor-of-dust/playtest"
DIMENSIONS = ("mood", "clarity", "uniqueness", "choices", "consequence")
REQUIRED = ("kind_robots_sha", "seed", "trace_path", "transcript_path")


def validate_record(record: object, source: Path) -> list[str]:
    errors: list[str] = []
    if not isinstance(record, dict):
        return [f"{source}: expected a YAML mapping"]
    acts = record.get("acts")
    if not isinstance(acts, dict):
        return [f"{source}: acts must be a mapping"]
    for act in range(1, 6):
        scores = acts.get(act, acts.get(str(act)))
        if not isinstance(scores, dict):
            errors.append(f"{source}: act {act} missing scores")
            continue
        has_score = any(scores.get(key) is not None for key in DIMENSIONS)
        if has_score:
            for field in REQUIRED:
                if record.get(field) is None or record.get(field) == "":
                    errors.append(f"{source}: scored act {act} missing {field}")
        for dimension in DIMENSIONS:
            value = scores.get(dimension)
            if value is None:
                continue
            if value == "N/A":
                continue
            if type(value) is not int or not 1 <= value <= 5:
                errors.append(
                    f"{source}: act {act} {dimension} must be 1-5 or N/A"
                )
        total = scores.get("total")
        if total is not None:
            if any(
                scores.get(dimension) is None
                or scores.get(dimension) == "N/A"
                for dimension in DIMENSIONS
            ):
                errors.append(
                    f"{source}: act {act} total requires five numeric scores"
                )
            elif type(total) is not int or total != sum(
                scores[dimension] for dimension in DIMENSIONS
                if type(scores[dimension]) is int
            ):
                errors.append(f"{source}: act {act} total is incorrect")
    return errors


def validate_directory(root: Path) -> list[str]:
    errors: list[str] = []
    for path in sorted(root.glob("*/reviewer*.yaml")) + sorted(
        root.glob("*/reviewer*.yml")
    ):
        try:
            record = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            errors.append(f"{path}: cannot read YAML: {exc}")
            continue
        errors.extend(validate_record(record, path))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=PLAYTEST)
    args = parser.parse_args()
    errors = validate_directory(args.root)
    for error in errors:
        print(error)
    if errors:
        return 1
    print("Emperor second-pass reviewer evidence: valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
