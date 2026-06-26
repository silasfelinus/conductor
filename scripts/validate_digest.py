#!/usr/bin/env python3
"""Validate the JSON shape produced by scripts/build_digest.py."""
import json
import sys
from pathlib import Path


def main() -> int:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "digest.json")
    with path.open(encoding="utf-8") as digest_file:
        digest = json.load(digest_file)

    required_keys = {
        "date",
        "commits_since",
        "merges_since",
        "projects",
        "all_needs_attention",
        "pitches_awaiting_vote",
    }
    list_keys = required_keys - {"date"}
    required_project_keys = {
        "name",
        "kind",
        "progress_pct",
        "milestones",
        "needs_attention",
        "in_flight",
        "waiting_count",
        "ready_count",
    }

    missing = sorted(required_keys - digest.keys())
    if missing:
        print("digest.json is missing required keys: " + ", ".join(missing), file=sys.stderr)
        return 1

    wrong_list_types = sorted(key for key in list_keys if not isinstance(digest[key], list))
    if wrong_list_types:
        print("digest.json fields must be lists: " + ", ".join(wrong_list_types), file=sys.stderr)
        return 1

    for index, project in enumerate(digest["projects"]):
        if not isinstance(project, dict):
            print(f"digest.json projects[{index}] must be an object", file=sys.stderr)
            return 1

        missing_project_keys = sorted(required_project_keys - project.keys())
        if missing_project_keys:
            print(
                f"digest.json projects[{index}] missing keys: " + ", ".join(missing_project_keys),
                file=sys.stderr,
            )
            return 1

        for key in ["milestones", "needs_attention", "in_flight"]:
            if not isinstance(project[key], list):
                print(f"digest.json projects[{index}].{key} must be a list", file=sys.stderr)
                return 1

    print(f"digest.json validated with {len(digest['projects'])} projects")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
