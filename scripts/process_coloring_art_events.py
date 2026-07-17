#!/usr/bin/env python3
"""Process connector-safe coloring-book color-generation events.

Event files request one bounded batch from the canonical color ArtJob queue. Dry-run
is the default. A secret-bearing GitHub Actions runner invokes this script with
``--live`` and deletes an event only after its consumer exits successfully.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
EVENT_DIR = ROOT / "color-art-events"
CONSUMER = ROOT / "scripts" / "consume_coloring_book_color_art.py"
ALLOWED_BOOKS = ("monster-recast", "hollywood-recast", "kind-robots")
ALLOWED_KEYS = {
    "version",
    "operation",
    "book",
    "limit",
    "timeout",
    "requested_by",
    "task",
    "note",
}
MAX_LIMIT = 18
MIN_TIMEOUT = 30
MAX_TIMEOUT = 900


@dataclass(frozen=True)
class ColorArtEvent:
    path: Path
    book: str
    limit: int
    timeout: int

    def command(self, *, live: bool) -> list[str]:
        command = [
            sys.executable,
            str(CONSUMER),
            "--book",
            self.book,
            "--limit",
            str(self.limit),
            "--timeout",
            str(self.timeout),
        ]
        if live:
            command.append("--live")
        return command


def _positive_int(value: Any, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{field} must be an integer")
    return value


def load_event(path: Path) -> ColorArtEvent:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError("event root must be a mapping")

    unknown = sorted(set(data) - ALLOWED_KEYS)
    if unknown:
        raise ValueError(f"unsupported event fields: {', '.join(unknown)}")
    if data.get("version") != 1:
        raise ValueError("version must be 1")
    if data.get("operation") != "generate-color-proposals":
        raise ValueError("operation must be generate-color-proposals")

    book = data.get("book")
    if book not in ALLOWED_BOOKS:
        raise ValueError(f"book must be one of: {', '.join(ALLOWED_BOOKS)}")

    limit = _positive_int(data.get("limit", MAX_LIMIT), "limit")
    if not 1 <= limit <= MAX_LIMIT:
        raise ValueError(f"limit must be between 1 and {MAX_LIMIT}")

    timeout = _positive_int(data.get("timeout", 300), "timeout")
    if not MIN_TIMEOUT <= timeout <= MAX_TIMEOUT:
        raise ValueError(f"timeout must be between {MIN_TIMEOUT} and {MAX_TIMEOUT}")

    return ColorArtEvent(path=path, book=str(book), limit=limit, timeout=timeout)


def queued_events() -> list[Path]:
    if not EVENT_DIR.exists():
        return []
    return sorted(path for path in EVENT_DIR.glob("*.yaml") if path.is_file())


def process_event(event: ColorArtEvent, *, live: bool) -> int:
    command = event.command(live=live)
    print(f"{'LIVE' if live else 'DRY RUN'} event {event.path.name}: {' '.join(command)}")

    if not live:
        return 0
    if not os.environ.get("KR_API_TOKEN"):
        print("KR_API_TOKEN is required for live coloring-art events.", file=sys.stderr)
        return 1

    result = subprocess.run(command, cwd=ROOT, check=False)
    if result.returncode == 0:
        event.path.unlink()
        print(f"Consumed {event.path.relative_to(ROOT)}")
    else:
        print(
            f"Consumer exited {result.returncode}; preserving {event.path.relative_to(ROOT)} for retry.",
            file=sys.stderr,
        )
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--max-events", type=int, default=1)
    args = parser.parse_args()

    if args.max_events < 1:
        parser.error("--max-events must be at least 1")

    paths = queued_events()[: args.max_events]
    if not paths:
        print("No queued coloring-art events.")
        return 0

    events: list[ColorArtEvent] = []
    for path in paths:
        try:
            events.append(load_event(path))
        except (OSError, ValueError, yaml.YAMLError) as error:
            print(f"Invalid event {path.relative_to(ROOT)}: {error}", file=sys.stderr)
            return 1

    for event in events:
        status = process_event(event, live=args.live)
        if status != 0:
            return status
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
