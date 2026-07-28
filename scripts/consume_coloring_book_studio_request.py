#!/usr/bin/env python3
"""Process one explicit Coloring Book Studio render request.

The regular coloring-book consumer deliberately works in book-order batches. The
studio needs a narrower contract: edit a canonical proposal, then request that
specific proposal without allowing an earlier pending slot to steal the run.
This wrapper reuses the existing enqueue, recovery, quality-gate, rejection, and
queue-writeback functions rather than creating a second rendering pipeline.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent))
import consume_art_queue as queue_consumer  # noqa: E402
import consume_coloring_book_color_art as coloring  # noqa: E402

ALLOWED_BOOKS = ("monster-recast", "hollywood-recast", "kind-robots")
BOOK_PREFIXES = {
    "monster-recast": ("mr-", "mr-group-"),
    "hollywood-recast": ("hwr-",),
    "kind-robots": ("kr-",),
}
REVISION_CLEAR_FIELDS = (
    "art_image_id",
    "completed_at",
    "last_rejected_art_image_id",
    "last_render_seed",
    "last_semantic_reasons",
    "last_semantic_score",
    "on_brief",
    "prompt_fingerprint",
    "render_engine",
    "render_seed",
    "rendered_path",
    "semantic_gate_error",
    "semantic_gate_error_at",
    "semantic_model",
    "semantic_score",
    "semantic_verdict",
    "subject_match",
)


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def archive_existing_candidate(source: dict[str, Any]) -> str | None:
    image_path = str(source.get("image_path") or "")
    if not image_path:
        return None

    current = coloring.ROOT / image_path
    if not current.exists():
        return None

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    archive_dir = current.parent / "revisions"
    archive_dir.mkdir(parents=True, exist_ok=True)
    archived = archive_dir / f"{current.stem}-{stamp}{current.suffix}"
    counter = 2
    while archived.exists():
        archived = archive_dir / f"{current.stem}-{stamp}-{counter}{current.suffix}"
        counter += 1
    current.replace(archived)
    return str(archived.relative_to(coloring.ROOT))


def queue_sources(queue: dict[str, Any], book_slug: str) -> dict[str, dict[str, Any]]:
    for book in queue.get("books") or []:
        if not isinstance(book, dict) or str(book.get("slug")) != book_slug:
            continue
        return {
            str(entry.get("id")): entry
            for entry in book.get("entries") or []
            if isinstance(entry, dict) and entry.get("id")
        }
    raise RuntimeError(f"Book not found in canonical color queue: {book_slug}")


def prepare_requested_entries(book_slug: str, proposal_ids: list[str], force: bool) -> None:
    queue = coloring.load_yaml(coloring.QUEUE_FILE)
    sources = queue_sources(queue, book_slug)
    missing = [proposal_id for proposal_id in proposal_ids if proposal_id not in sources]
    if missing:
        raise RuntimeError(f"Unknown proposal id(s) for {book_slug}: {', '.join(missing)}")

    changed = False
    blocked: list[str] = []

    for proposal_id in proposal_ids:
        source = sources[proposal_id]
        status = str(source.get("status") or "pending").strip().lower()
        if status == "pending":
            continue
        if not force:
            blocked.append(f"{proposal_id} ({status})")
            continue

        history = source.get("studio_revision_history")
        if not isinstance(history, list):
            history = []
        record: dict[str, Any] = {
            "requested_at": now_iso(),
            "previous_status": status,
            "art_image_id": source.get("art_image_id"),
            "rendered_path": source.get("rendered_path"),
            "semantic_score": source.get("semantic_score"),
            "prompt_fingerprint": source.get("prompt_fingerprint"),
        }
        archived_path = archive_existing_candidate(source)
        if archived_path:
            record["archived_path"] = archived_path
        history.append(record)
        source["studio_revision_history"] = history
        source["status"] = "pending"
        source["studio_revision_requested_at"] = now_iso()
        for field in REVISION_CLEAR_FIELDS:
            source.pop(field, None)
        changed = True

    if blocked:
        raise RuntimeError(
            "Proposal(s) are not pending; use --force to request a new revision: "
            + ", ".join(blocked)
        )
    if changed:
        coloring.write_queue(queue)


def selected_entries(book_slug: str, proposal_ids: list[str]) -> list[dict[str, Any]]:
    _queue, pending = coloring.build_entries(book_slug)
    by_id = {str(entry["concept_id"]): entry for entry in pending}
    missing = [proposal_id for proposal_id in proposal_ids if proposal_id not in by_id]
    if missing:
        raise RuntimeError(
            "Requested proposal(s) are not available as pending color jobs: " + ", ".join(missing)
        )
    return [by_id[proposal_id] for proposal_id in proposal_ids]


def run_entries(entries: list[dict[str, Any]], *, live: bool, timeout: int) -> int:
    mode = "LIVE" if live else "DRY RUN"
    print(f"{mode}: {len(entries)} proposal-targeted Coloring Book Studio request(s)")

    if not live:
        for entry in entries:
            job = coloring.stable_job_body(entry)
            print(
                f"  {entry['set']}/{entry['concept_id']} -> {entry['image_path']} "
                f"engine={entry.get('engine')} seed={job.get('resolvedSeed')}"
            )
        return 0

    if not queue_consumer.KR_API_TOKEN:
        print("KR_API_TOKEN is required for --live.", file=sys.stderr)
        return 1

    completed: list[dict[str, Any]] = []
    retryable_failures = 0

    for entry in entries:
        destination = coloring.target_path(entry)
        try:
            recovered: tuple[bool, dict[str, Any]] | None = None
            if destination.exists():
                print(
                    f"  validating existing candidate for {entry['set']}/{entry['concept_id']} "
                    f"at {destination.relative_to(coloring.ROOT)}"
                )
            elif (stuck_job_id := coloring.referenced_job_id(entry)) is not None:
                recovered = coloring.recover_timed_out_job(entry, stuck_job_id)
                if recovered is None:
                    print(
                        f"  job {stuck_job_id} for {entry['set']}/{entry['concept_id']} is still "
                        "queued/running; preserving the event without submitting a duplicate"
                    )
                    retryable_failures += 1
                    continue
                destination = coloring.target_path(entry)
                print(
                    f"  recovered completed ArtJob {stuck_job_id} for "
                    f"{entry['set']}/{entry['concept_id']}"
                )
            else:
                job_id, deduplicated = coloring.enqueue(entry)
                suffix = " (existing matching attempt)" if deduplicated else ""
                print(
                    f"  queued ArtJob {job_id}{suffix} for "
                    f"{entry['set']}/{entry['concept_id']} color - waiting..."
                )
                job = queue_consumer.wait_for_job(job_id, timeout)
                entry["art_image_id"] = int(job["artImageId"])
                image_b64 = queue_consumer.fetch_image_b64(job["artImageId"])
                destination = coloring.save_result(entry, image_b64)

            accepted, semantic = (
                recovered if recovered is not None else coloring.validate_candidate(entry, destination)
            )
            if not accepted:
                rejected = coloring.rejection_destination(destination, entry, "rejected")
                next_status = coloring.record_semantic_rejection(entry, semantic, rejected)
                if next_status == "pending":
                    retryable_failures += 1
                print(
                    f"  SEMANTIC-REJECT {entry['set']}/{entry['concept_id']}: "
                    f"{' ; '.join(semantic.get('reasons') or [])} -> "
                    f"{rejected.relative_to(coloring.ROOT)} ({next_status})",
                    file=sys.stderr,
                )
                continue

            entry["semantic_verdict"] = semantic.get("verdict")
            entry["semantic_score"] = semantic.get("score")
            entry["subject_match"] = semantic.get("subject_match") is True
            entry["on_brief"] = semantic.get("on_brief") is True
            entry["semantic_model"] = semantic.get("model")
            completed.append(entry)
            print(
                f"  DONE {entry['set']}/{entry['concept_id']} -> "
                f"{destination.relative_to(coloring.ROOT)} "
                f"(ArtImage {entry.get('art_image_id') or 'existing'}, semantic={semantic.get('score')})"
            )
        except Exception as error:  # noqa: BLE001
            retryable_failures += 1
            if destination.exists():
                try:
                    rejected = coloring.rejection_destination(destination, entry, "unverified")
                    print(
                        f"    unverified candidate moved to {rejected.relative_to(coloring.ROOT)}",
                        file=sys.stderr,
                    )
                except Exception:  # noqa: BLE001
                    pass
            coloring.record_semantic_gate_error(entry, error)
            print(f"  FAILED {entry['set']}/{entry['concept_id']}: {error}", file=sys.stderr)

    marked = coloring.mark_done(completed)
    print(f"Marked {marked} targeted color proposal(s) done.")
    return 1 if retryable_failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--book", choices=ALLOWED_BOOKS, required=True)
    parser.add_argument("--proposal-id", action="append", dest="proposal_ids", required=True)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    proposal_ids = list(dict.fromkeys(str(value).strip() for value in args.proposal_ids if str(value).strip()))
    if not proposal_ids:
        parser.error("at least one --proposal-id is required")
    if len(proposal_ids) > 18:
        parser.error("at most 18 proposal ids may be requested")
    prefixes = BOOK_PREFIXES[args.book]
    invalid = [proposal_id for proposal_id in proposal_ids if not proposal_id.startswith(prefixes)]
    if invalid:
        parser.error(f"proposal id(s) do not belong to {args.book}: {', '.join(invalid)}")
    if not 30 <= args.timeout <= 900:
        parser.error("--timeout must be between 30 and 900")

    try:
        prepare_requested_entries(args.book, proposal_ids, args.force)
        entries = selected_entries(args.book, proposal_ids)
        return run_entries(entries, live=args.live, timeout=args.timeout)
    except Exception as error:  # noqa: BLE001
        print(f"Studio request failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
