#!/usr/bin/env python3
"""Compatibility entrypoint for the Conductor projection sync.

This script previously PATCHed individual Kind Robots Project records with
Conductor-owned title, description, goal, route, channel, tab, URL, lifecycle,
and priority values. That made two repositories authoritative for presentation
state.

Legacy worker instructions and workflows may still invoke
``python scripts/sync_projects.py``. Keep that command safe by delegating to the
one-way, commit-stamped projection sender. The Kind Robots sync endpoint owns
normalization and updates only coordination fields on existing Project rows.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.sync_kind_robots_projection import main as projection_main


def main() -> int:
    return projection_main()


if __name__ == "__main__":
    raise SystemExit(main())
