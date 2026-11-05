#!/usr/bin/env python3
"""Process connector-safe Coloring Book Studio events."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

sys.path.insert(0, str(Path(__file__).parent))
import coloring_render_settings  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
EVENT_DIR = ROOT / "color-art-events"
QUARANTINE_DIR = EVENT_DIR / "quarantine"
ATTEMPT_STATE_PATH = EVENT_DIR / "attempt-state.yaml"
# How many consecutive failures a single queued event may accrue before it is
# pulled out of the live queue instead of retrying forever. Mirrors
# render_retry.py's COLOR_ART_MAX_RENDER_ATTEMPTS pattern, but counts across
# separate scheduled runs of this script rather than within one.
MAX_EVENT_ATTEMPTS = int(os.environ.get("COLOR_ART_EVENT_MAX_ATTEMPTS", "3"))
# Consumer exit status for "nothing failed; renders are still in flight on the
# art server" (consume_coloring_book_studio_request.EXIT_WAITING). The event is
# preserved for the next run without counting an attempt toward quarantine.
EXIT_WAITING = 75
# Operations that submit ArtJobs and may block for minutes. Everything else
# (accept/finalize/adopt) is a fast local ledger update and runs first, so a
# studio curation click is never stuck behind somebody else's slow render.
GENERATION_OPERATIONS = ("generate-color-proposals", "generate-bw", "generate-cover")
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
    "bw_source",
    "color_source",
    "render_settings",
    "timeout",
    "force",
    "requested_by",
    "task",
    "note",
}
IMAGE_SUFFIXES = {".webp", ".png", ".jpg", ".jpeg"}
ACCEPT_OPERATIONS = ("accept-color", "accept-bw", "accept-cover")
# Where a generate-bw request draws its line art from. "color" (the default and
# the only behavior before 2026-11-04) converts the accepted color master;
# "version" converts one named color or B&W file from the page's history
# (source_path); "prompt" renders fresh line art from the page's text prompt.
BW_SOURCES = ("color", "version", "prompt")
# generate-color-proposals: "prompt" (default) renders from the page prompt;
# "version" colors the B&W (or re-colors the color) file named by source_path.
COLOR_SOURCES = ("prompt", "version")
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
    render_settings: dict[str, Any] | None = None
    bw_source: str | None = None
    color_source: str | None = None

    @property
    def is_cover(self) -> bool:
        return self.operation in COVER_OPERATIONS

    @property
    def is_generation(self) -> bool:
        return self.operation in GENERATION_OPERATIONS

    @property
    def targets(self) -> frozenset[str]:
        """Pages (or the cover) this event changes; same-target events stay ordered."""
        if self.is_cover:
            return frozenset({f"{self.book}/cover"})
        return frozenset(f"{self.book}/{pid}" for pid in self.proposal_ids)

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
            if self.render_settings is not None:
                command.extend(
                    ("--render-settings", json.dumps(self.render_settings, sort_keys=True))
                )
            if self.color_source:
                command.extend(("--color-source", self.color_source))
            if self.source_path:
                command.extend(("--source-path", self.source_path))
        elif self.source_path and self.operation in ACCEPT_OPERATIONS:
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
            if self.bw_source:
                command.extend(("--bw-source", self.bw_source))
            if self.source_path:
                command.extend(("--source-path", self.source_path))
        if self.force:
            command.append("--force")
        if live:
            command.append("--live")
        return command


def _integer(value: Any, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{field} must be an integer")
    return value


def _source_path(
    value: Any,
    *,
    book: str,
    operation: str,
    bw_source: str | None = None,
    color_source: str | None = None,
) -> str | None:
    if value is None or value == "":
        return None
    if not isinstance(value, str):
        raise ValueError("source_path must be a string")
    if operation not in ACCEPT_OPERATIONS and not (
        (operation == "generate-bw" and bw_source == "version")
        or (operation == "generate-color-proposals" and color_source == "version")
    ):
        raise ValueError(
            "source_path is supported only for accept-color, accept-bw, accept-cover, "
            "generate-bw with bw_source: version, and generate-color-proposals with "
            "color_source: version"
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
    bw_source = data.get("bw_source")
    if bw_source is not None:
        if operation_text != "generate-bw":
            raise ValueError("bw_source is supported only for generate-bw")
        if bw_source not in BW_SOURCES:
            raise ValueError(f"bw_source must be one of: {', '.join(BW_SOURCES)}")
    color_source = data.get("color_source")
    if color_source is not None:
        if operation_text != "generate-color-proposals":
            raise ValueError("color_source is supported only for generate-color-proposals")
        if color_source not in COLOR_SOURCES:
            raise ValueError(f"color_source must be one of: {', '.join(COLOR_SOURCES)}")
    source_path = _source_path(
        data.get("source_path"),
        book=book_text,
        operation=operation_text,
        bw_source=bw_source,
        color_source=color_source,
    )
    if bw_source == "version" and not source_path:
        raise ValueError("bw_source: version requires a source_path")
    if color_source == "version" and not source_path:
        raise ValueError("color_source: version requires a source_path")
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
    if source_path and force and operation_text in ACCEPT_OPERATIONS:
        raise ValueError("source_path adoption cannot be combined with force")

    render_settings = None
    if data.get("render_settings") is not None:
        if operation_text != "generate-color-proposals":
            raise ValueError("render_settings is supported only for generate-color-proposals")
        render_settings = coloring_render_settings.normalize(data["render_settings"])

    return ColorArtEvent(
        path=path,
        operation=operation_text,
        book=book_text,
        proposal_ids=tuple(proposal_ids),
        source_path=source_path,
        timeout=timeout,
        force=force,
        render_settings=render_settings,
        bw_source=bw_source,
        color_source=color_source,
    )


def queued_events() -> list[Path]:
    if not EVENT_DIR.exists():
        return []
    return sorted(
        path
        for path in EVENT_DIR.glob("*.yaml")
        if path.is_file() and path != ATTEMPT_STATE_PATH
    )


def load_attempt_state() -> dict[str, int]:
    """Consecutive-failure count per queued event filename, keyed by name.

    Persisted as a sidecar file alongside the events themselves so a count
    survives between separate scheduled runs of this script (each run is a
    fresh process/checkout).
    """

    if not ATTEMPT_STATE_PATH.exists():
        return {}
    data = yaml.safe_load(ATTEMPT_STATE_PATH.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        return {}
    return {
        str(name): int(count)
        for name, count in data.items()
        if isinstance(count, int) and not isinstance(count, bool) and count > 0
    }


def save_attempt_state(state: dict[str, int]) -> None:
    if not state:
        if ATTEMPT_STATE_PATH.exists():
            ATTEMPT_STATE_PATH.unlink()
        return
    EVENT_DIR.mkdir(parents=True, exist_ok=True)
    ATTEMPT_STATE_PATH.write_text(
        yaml.safe_dump(dict(sorted(state.items())), sort_keys=True),
        encoding="utf-8",
    )


def quarantine_event(event: ColorArtEvent, *, attempts: int) -> Path:
    QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)
    destination = QUARANTINE_DIR / event.path.name
    event.path.replace(destination)
    print(
        f"::warning::Quarantined {event.path.name} after {attempts} consecutive "
        f"failures -- moved to {destination.relative_to(ROOT)} for manual review "
        "instead of retrying forever."
    )
    return destination


def process_event(
    event: ColorArtEvent, *, live: bool, attempt_state: dict[str, int]
) -> int:
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

    # No operation here needs a model credential any more. Renders are gated
    # only by the free structural check in art_quality.py; whether a render is
    # any *good* is decided by a human in the ArtJob trainer panel.
    result = subprocess.run(command, cwd=ROOT, check=False)
    if result.returncode == 0:
        attempt_state.pop(event.path.name, None)
        event.path.unlink()
        print(f"Consumed {event.path.relative_to(ROOT)}")
        return 0
    if result.returncode == EXIT_WAITING:
        # Renders are still in flight -- not a failure, so no attempt is
        # counted and the event is never quarantined for merely waiting.
        print(
            f"Renders still in flight; preserving {event.path.relative_to(ROOT)} "
            "for the next run (no attempt counted)."
        )
        return EXIT_WAITING

    attempts = attempt_state.get(event.path.name, 0) + 1
    if attempts >= MAX_EVENT_ATTEMPTS:
        attempt_state.pop(event.path.name, None)
        quarantine_event(event, attempts=attempts)
        # Quarantining is the resolution, not another failure to retry: return
        # 0 so the scheduled workflow stops reporting this event as an
        # unaddressed error on every future tick.
        return 0

    attempt_state[event.path.name] = attempts
    print(
        f"Consumer exited {result.returncode}; preserving "
        f"{event.path.relative_to(ROOT)} for retry "
        f"({attempts}/{MAX_EVENT_ATTEMPTS} attempts).",
        file=sys.stderr,
    )
    return result.returncode


def blocking_events(
    event: ColorArtEvent, events: list[ColorArtEvent]
) -> list[ColorArtEvent]:
    """Earlier, still-queued events that change the same page or cover.

    A page's actions apply in the order they were requested; unrelated pages
    never wait on each other.
    """

    blockers: list[ColorArtEvent] = []
    for other in events:
        if other.path == event.path:
            break
        if other.path.exists() and other.targets & event.targets:
            blockers.append(other)
    return blockers


def schedule(events: list[ColorArtEvent]) -> list[ColorArtEvent]:
    """Fast curation actions first, then generation, each in queue order."""

    return sorted(events, key=lambda event: event.is_generation)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true")
    parser.add_argument(
        "--max-events",
        type=int,
        default=1,
        help="most events to attempt this run",
    )
    parser.add_argument(
        "--time-budget",
        type=int,
        default=0,
        help="seconds after which no further event is started (0 = no limit)",
    )
    args = parser.parse_args()

    if args.max_events < 1:
        parser.error("--max-events must be at least 1")
    if args.time_budget < 0:
        parser.error("--time-budget must not be negative")

    paths = queued_events()
    if not paths:
        print("No queued coloring-art events.")
        return 0

    # Load every queued event, not only the first --max-events: ordering is
    # decided per page across the whole queue. A malformed event is reported
    # and skipped; it must not stall every valid request behind it.
    events: list[ColorArtEvent] = []
    exit_status = 0
    for path in paths:
        try:
            events.append(load_event(path))
        except (OSError, ValueError, yaml.YAMLError) as error:
            print(
                f"Invalid event {path.relative_to(ROOT)}: {error}",
                file=sys.stderr,
            )
            exit_status = 1

    attempt_state = load_attempt_state()
    started = time.monotonic()
    attempted = 0
    tried: set[Path] = set()
    try:
        # Repeat until a pass makes no progress, so an acceptance queued behind
        # a generation for the same page still lands this run once that
        # generation is consumed.
        progress = True
        while progress:
            progress = False
            for event in schedule(events):
                if event.path in tried or not event.path.exists():
                    continue
                blockers = blocking_events(event, events)
                if blockers:
                    continue
                if attempted >= args.max_events:
                    break
                if args.time_budget and time.monotonic() - started >= args.time_budget:
                    print(
                        f"Time budget of {args.time_budget}s spent; leaving the "
                        "rest for the next run."
                    )
                    progress = False
                    break
                tried.add(event.path)
                attempted += 1
                status = process_event(event, live=args.live, attempt_state=attempt_state)
                if not event.path.exists():
                    progress = True
                if status not in (0, EXIT_WAITING):
                    exit_status = status
    finally:
        save_attempt_state(attempt_state)
    for event in events:
        if event.path.exists() and event.path not in tried:
            blockers = blocking_events(event, events)
            if blockers:
                print(
                    f"Deferred {event.path.name}: waits behind "
                    + ", ".join(other.path.name for other in blockers)
                )
    remaining = [event for event in events if event.path.exists()]
    print(
        f"Attempted {attempted} event(s); {len(events) - len(remaining)} consumed, "
        f"{len(remaining)} still queued."
    )
    return exit_status


if __name__ == "__main__":
    raise SystemExit(main())
