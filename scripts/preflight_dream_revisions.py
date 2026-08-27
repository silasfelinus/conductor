#!/usr/bin/env python3
"""Preflight a set of Daily Dream revision requests without mutating source or production."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import apply_dream_revision as revision  # noqa: E402
import build_dream_proposal as proposals  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    paths = [Path(value) for value in (argv if argv is not None else sys.argv[1:])]
    if not paths:
        print("No Daily Dream revision requests supplied.", file=sys.stderr)
        return 2
    try:
        for path in paths:
            request = json.loads(path.read_text(encoding="utf-8"))
            proposal_path = ROOT / str(request["proposal_path"])
            old_text = proposal_path.read_text(encoding="utf-8")
            old = revision._data_block(old_text, "proposal-data")
            if old is None:
                raise ValueError(f"{proposal_path}: missing proposal-data")
            built = revision._data_block(old_text, "built-data") is not None or (
                revision._frontmatter_value(old_text, "status").casefold() == "built"
            )
            day = revision._frontmatter_value(old_text, "proposal_date") or revision._frontmatter_value(
                old_text, "created"
            )
            candidate = proposals.normalize(dict(request["proposal"]), set())
            revision.validate_revision(old, candidate, day, built=built)
            print(f"{path}: revision preflight passed")
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f"Daily Dream revision preflight failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
