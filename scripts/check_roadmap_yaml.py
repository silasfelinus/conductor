#!/usr/bin/env python3
"""Reject roadmaps that PyYAML accepts but a spec-compliant YAML parser rejects.

Why this exists
---------------
kind_robots renders the Projects board from these roadmaps
(`server/api/conductor/projects.get.ts` -> `server/utils/conductorRoadmap.ts`),
parsing them with the `yaml` npm package — a YAML 1.2 parser. PyYAML is more
permissive than the spec in one way that matters here: it accepts a quoted flow
scalar whose continuation lines sit at column 0, e.g.

    notes_from_silas: 'Auto-import LoRAs: drop a file into Lora/import
    <- this line is at column 0, so a 1.2 parser errors here
    and have it detected...
    '

The spec requires continuation lines of a flow scalar to be indented deeper than
the mapping key. A 1.2 parser raises "Missing closing 'quote"; PyYAML shrugs and
carries on. Every conductor-side tool uses PyYAML, so nothing noticed — but the
front end failed to parse the whole file and rendered the project as empty.

Found 2026-07-31: `lora-ingestion` and `art-generator-connect` were both in this
state, so both showed 0% and no tasks on the live board despite being 31.8% and
11.5% complete. Both are repaired; this check keeps a PyYAML round-trip from
silently reintroducing the shape (`yaml.safe_dump` emits it whenever the value
contains a colon-space and long lines).

Exit codes: 0 = every roadmap is spec-clean, 1 = at least one is not.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "projects"

# `key: '` or `key: "` where the scalar does not close on the same line.
OPENS_FLOW_SCALAR = re.compile(r'^([A-Za-z_][\w-]*): *(["\'])(.*)$')


def unterminated(quote: str, rest: str) -> bool:
    """True when `rest` leaves the quoted scalar open at end of line."""
    if quote == "'":
        # '' is an escaped quote inside a single-quoted scalar.
        return len(re.sub(r"''", "", rest).split("'")) % 2 == 1
    # Backslash-escaped quotes inside a double-quoted scalar.
    return len(re.sub(r"\\.", "", rest).split('"')) % 2 == 1


def check(path: Path) -> list[str]:
    problems: list[str] = []
    lines = path.read_text(encoding="utf-8").split("\n")
    index = 0
    while index < len(lines):
        match = OPENS_FLOW_SCALAR.match(lines[index])
        if not match:
            index += 1
            continue
        key, quote, rest = match.groups()
        if not unterminated(quote, rest):
            index += 1
            continue

        # Walk the continuation lines to the closing quote.
        start = index + 1
        index = start
        while index < len(lines):
            line = lines[index]
            if line.strip() and not line.startswith(" "):
                problems.append(
                    f"{path.relative_to(ROOT)}:{index + 1}: continuation of quoted "
                    f"scalar `{key}` is at column 0 — a YAML 1.2 parser stops here. "
                    f"Rewrite the value as a block scalar (`{key}: |`)."
                )
                break
            if unterminated(quote, line):
                index += 1
                continue
            break
        index += 1
    return problems


def main() -> int:
    problems: list[str] = []
    roadmaps = sorted(PROJECTS.glob("*/roadmap.yaml"))
    for path in roadmaps:
        if path.parent.name == "_template":
            continue
        problems.extend(check(path))

    if problems:
        print(f"{len(problems)} roadmap(s) are not spec-compliant YAML:\n")
        for problem in problems:
            print(f"  {problem}")
        print(
            "\nThese parse under PyYAML but not under the YAML 1.2 parser the "
            "kind_robots Projects board uses, so the affected projects render "
            "as empty on the site."
        )
        return 1

    print(f"checked {len(roadmaps)} roadmaps — all spec-compliant.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
