#!/usr/bin/env python3
"""Compatibility wrapper for the superseded Monster-Recast-only ArtJob consumer.

The canonical queue is now projects/coloring-book/color-art-jobs.yaml and the
canonical consumer handles 18 COLOR proposals per pass across all three books.
This wrapper keeps old manual invocations working while restricting them to
Monster Recast.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import consume_coloring_book_color_art as color_consumer  # noqa: E402


if __name__ == "__main__":
    if "--book" not in sys.argv:
        sys.argv.extend(["--book", "monster-recast"])
    raise SystemExit(color_consumer.main())
