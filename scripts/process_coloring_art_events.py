#!/usr/bin/env python3
"""Process connector-safe Coloring Book Studio events."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
EVENT_DIR = ROOT / "color-art-events"
COLOR_CONSUMER = ROOT / "scripts" / "consume_coloring_book_studio_request.py"
PRODUCTION_CONSUMER = ROOT / "scripts" / "manage_coloring_book_production.py"
ADOPTION_CONSUMER = ROOT / "scripts" / "adopt_coloring_book_asset.py"
COVER_CONSUMER = ROOT / "scripts" / "manage_coloring_book_cover.py"
ALLOWED_BOOKS = ("monster-recast", "hollywood-recast", "kind-robots")
INTERIOR_OPERATIONS = (
    "generate-color-proposals",
    "accept-color",
    "generate-bw",
    "accept-bw",
    "finalize-pair",
)
COVER_OPERATIONS = ("generate-cover", "accept-cover", "finalize-cover")
ALLOWED_OPERATIONS = INTERIOR_OPERATIONS + COVER_OPERATIONS
BOOK_PATTERNS = {
    "monster-recast": re.compile(r"^(?:mr-\d{3}|mr-group-\d{3})$"),
    "hollywood-recast": re.compile(r"^hwr-\d{3}$"),
    "kind-robots": re.compile(r"^kr-\d{3}$"),
}
ALLOWED_KEYS = {
    "version",
    "operation",
    "book",
    "proposal_ids",
    "source_path",
    "timeout",
    "force",
    "requested_by",
    "task",
    "note",
}
IMAGE_SUFFIXES = {".webp", ".png", ".jpg", ".jpeg"}
MIN_TIMEOUT = 30
MAX_TIMEOUT = 900
MAX_PROPOSALS = 18


@dataclass(frozen=True)
class ColorArtEvent:
    path: Path
    operation: str
    book: str
    proposal_ids: tuple[str, ...]
    source_path: str | None
    timeout: int
    force: bool

    @property
    def is_cover(self) -> bool:
        return self.operation in COVER_OPERATIONS

    def command(self, *, live: bool) -> list[str]:
        if self.is_cover:
            command = [
                sys.executable,
                str(COVER_CONSUMER),
                "--operation",
                self.operation,
                "--book",
                self.book,
                "--timeout",
                str(self.timeout),
            ]
            if self.source_path:
                command.extend(("--source-path", self.source_path))
        elif self.operation == "generate-color-proposals":
            command = [
                sys.executable,
                str(COLOR_CONSUMER),
                "--book",
                self.book,
                "--timeout",
                str(self.timeout),
            ]
            for proposal_id in self.proposal_ids:
                command.extend(("--proposal-id", proposal_id))
        elif self.source_path:
            command = [
                sys.executable,
                str(ADOPTION_CONSUMER),
                "--operation",
                self.operation,
                "--book",
                self.book,
                "--proposal-id",
                self.proposal_ids[0],
                "--source-path",
                self.source_path,
            ]
        else:
            command = [
                sys.executable,
                str(PRODUCTION_CONSUMER),
                "--operation",
                self.operation,
                "--book",
                self.book,
                "--timeout",
                str(self.timeout),
            ]
            for proposal_id in self.proposal_ids:
                command.extend(("--proposal-id", proposal_id))
        if self.force:
            command.append("--force")
        if live:
            command.append("--live")
        return command


def _integer(value: Any, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{field} must be an integer")
    return value


def _source_path(value: Any, *, book: str, operation: str) -> str | None:
    if value is None or value == "":
        return None
    if not isinstance(value, str):
        raise ValueError("source_path must be a string")
    if operation not in ("accept-color", "accept-bw", "accept-cover"):
        raise ValueError(
            "source_path is supported only for accept-color, accept-bw, and accept-cover"
        )

    clean = value.strip().replace("\\", "/")
    prefix = f"projects/coloring-book/sets/{book}/"
    if clean.startswith(prefix):
        clean = clean[len(prefix) :]
    elif clean.startswith("projects/"):
        raise ValueError(f"source_path must belong to the {book} set")

    if (
        not clean
        or clean.startswith("/")
        or ":" in clean
        or ".." in Path(clean).parts
        or Path(clean).suffix.lower() not in IMAGE_SUFFIXES
    ):
        raise ValueError("source_path must be a safe image path inside the selected set")
    return clean


def _proposal_ids(data: dict[str, Any], book: str, operation: str) -> list[str]:
    raw_ids = data.get("proposal_ids")
    if operation in COVER_OPERATIONS:
        if raw_ids not in (None, []):
            raise ValueError("cover operations do not accept proposal_ids")
        return []

    if not isinstance(raw_ids, list) or not raw_ids:
        raise ValueError("proposal_ids must be a non-empty list")
    if len(raw_ids) > MAX_PROPOSALS:
        raise ValueError(f"proposal_ids may contain at most {MAX_PROPOSALS} items")

    proposal_ids: list[str] = []
    for value in raw_ids:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("proposal_ids must contain non-empty strings")
        proposal_id = value.strip()
        if not BOOK_PATTERNS[book].fullmatch(proposal_id):
            raise ValueError(f"proposal id {proposal_id!r} does not belong to {book}")
        if proposal_id not in proposal_ids:
            proposal_ids.append(proposal_id)
    return proposal_ids


def load_event(path: Path) -> ColorArtEvent:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError("event root must be a mapping")

    unknown = sorted(set(data) - ALLOWED_KEYS)
    if unknown:
        raise ValueError(f"unsupported event fields: {', '.join(unknown)}")
    if data.get("version") != 1:
        raise ValueError("version must be 1")

    operation = data.get("operation")
    if operation not in ALLOWED_OPERATIONS:
        raise ValueError(
            f"operation must be one of: {', '.join(ALLOWED_OPERATIONS)}"
        )

    book = data.get("book")
    if book not in ALLOWED_BOOKS:
        raise ValueError(f"book must be one of: {', '.join(ALLOWED_BOOKS)}")

    operation_text = str(operation)
    book_text = str(book)
    proposal_ids = _proposal_ids(data, book_text, operation_text)
    source_path = _source_path(
        data.get("source_path"),
        book=book_text,
        operation=operation_text,
    )
    if source_path and operation_text in INTERIOR_OPERATIONS and len(proposal_ids) != 1:
        raise ValueError("source_path requires exactly one proposal id")

    timeout = _integer(data.get("timeout", 600), "timeout")
    if not MIN_TIMEOUT <= timeout <= MAX_TIMEOUT:
        raise ValueError(f"timeout must be between {MIN_TIMEOUT} and {MAX_TIMEOUT}")

    force = data.get("force", False)
    if not isinstance(force, bool):
        raise ValueError("force must be a boolean")
    if force and operation_text not in (
        "generate-color-proposals",
        "generate-bw",
        "generate-cover",
    ):
        raise ValueError(
            "force is supported only for generate-color-proposals, generate-bw, and generate-cover"
        )
    if source_path and force:
        raise ValueError("source_path adoption cannot be combined with force")

    return ColorArtEvent(
        path=path,
        operation=operation_text,
        book=book_text,
        proposal_ids=tuple(proposal_ids),
        source_path=source_path,
        timeout=timeout,
        force=force,
    )


def queued_events() -> list[Path]:
    if not EVENT_DIR.exists():
        return []
    return sorted(path for path in EVENT_DIR.glob("*.yaml") if path.is_file())


def process_event(event: ColorArtEvent, *, live: bool) -> int:
    command = event.command(live=live)
    print(
        f"{'LIVE' if live else 'DRY RUN'} event {event.path.name}: "
        + " ".join(command)
    )

    if not live:
        return 0
    if event.operation in (
        "generate-color-proposals",
        "generate-bw",
        "generate-cover",
    ) and not os.environ.get("KR_API_TOKEN"):
        print(
            "KR_API_TOKEN is required for live coloring generation events.",
            file=sys.stderr,
        )
        return 1

    semantic_operations = {
        "generate-color-proposals",
        "generate-bw",
        "finalize-pair",
        "generate-cover",
        "accept-cover",
        "finalize-cover",
    }
    if event.operation in semantic_operations or (
        event.operation == "accept-bw" and event.source_path
    ):
        if not os.environ.get("ANTHROPIC_API_KEY"):
            print(
                "ANTHROPIC_API_KEY is required for semantic coloring review.",
                file=sys.stderr,
            )
            return 1

    result = subprocess.run(command, cwd=ROOT, check=False)
    if result.returncode == 0:
        event.path.unlink()
        print(f"Consumed {event.path.relative_to(ROOT)}")
    else:
        print(
            f"Consumer exited {result.returncode}; preserving "
            f"{event.path.relative_to(ROOT)} for retry.",
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
            print(
                f"Invalid event {path.relative_to(ROOT)}: {error}",
                file=sys.stderr,
            )
            return 1

    for event in events:
        status = process_event(event, live=args.live)
        if status != 0:
            return status
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
