#!/usr/bin/env python3
"""
validate_roadmaps.py — confirm every projects/*/roadmap.yaml still parses as a
mapping with a `tasks` list. Used by the process-task-events workflow after a
surgical text edit, and safe to run standalone.

Usage: python scripts/validate_roadmaps.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    for path in sorted((ROOT / "projects").glob("*/roadmap.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or not isinstance(data.get("tasks", []), list):
            print(f"invalid roadmap: {path}", file=sys.stderr)
            return 1
    print("Roadmaps valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
