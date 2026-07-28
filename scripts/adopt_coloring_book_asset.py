#!/usr/bin/env python3
"""Adopt an exact existing set asset as a reviewed coloring-book master.

This is the compatibility path for legacy and manually curated images that predate
the durable ArtJob queue. It never invents ArtJob provenance or copies the image.
The selected file must already live inside the named coloring-book set.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import manage_coloring_book_production as production  # noqa: E402

ALLOWED_OPERATIONS = ("accept-color", "accept-bw")
IMAGE_SUFFIXES = {".webp", ".png", ".jpg", ".jpeg"}


def safe_source(book_slug: str, source_path: str) -> tuple[str, Path]:
    clean = str(source_path or "").strip().replace("\\", "/")
    prefix = f"projects/coloring-book/sets/{book_slug}/"
    if clean.startswith(prefix):
        clean = clean[len(prefix) :]
    elif clean.startswith("projects/"):
        raise RuntimeError(f"Source path is outside the {book_slug} set")

    if (
        not clean
        or clean.startswith("/")
        or ":" in clean
        or ".." in Path(clean).parts
        or Path(clean).suffix.lower() not in IMAGE_SUFFIXES
    ):
        raise RuntimeError(f"Unsafe or unsupported set asset path: {source_path!r}")

    root = production.set_dir(book_slug).resolve()
    absolute = (root / clean).resolve()
    if root not in absolute.parents:
        raise RuntimeError(f"Source path escapes the {book_slug} set")
    if not absolute.is_file():
        raise RuntimeError(f"Selected set asset does not exist: {absolute}")
    return clean, absolute


def adopt_color(book_slug: str, proposal_id: str, source_path: str) -> None:
    relative, absolute = safe_source(book_slug, source_path)
    production.mechanical_check(absolute, "color")

    queue = production.load_yaml(production.QUEUE_FILE)
    ledger = production.load_yaml(production.ledger_path(book_slug))
    queue_entry = production.find_queue_entry(queue, book_slug, proposal_id)
    proposal = production.find_proposal(ledger, proposal_id)
    accepted = production.ensure_pair(proposal, "accepted")

    accepted["color"] = relative
    queue_entry["status"] = "approved"
    queue_entry["approved_at"] = production.now_iso()
    queue_entry["rendered_path"] = (
        f"projects/coloring-book/sets/{book_slug}/{relative}"
    )
    queue_entry["adopted_color_path"] = relative
    queue_entry["adopted_color_at"] = production.now_iso()
    if queue_entry.get("render_seed") is not None:
        queue_entry["lock_seed"] = True
        queue_entry["seed"] = queue_entry["render_seed"]
    else:
        queue_entry["lock_seed"] = False

    production.replace_ledger_pair_value(
        book_slug,
        proposal_id,
        "accepted",
        "color",
        relative,
    )
    production.write_yaml(production.QUEUE_FILE, queue)


def adopt_bw(book_slug: str, proposal_id: str, source_path: str) -> bool:
    relative, absolute = safe_source(book_slug, source_path)
    production.mechanical_check(absolute, "bw")

    queue = production.load_yaml(production.QUEUE_FILE)
    ledger = production.load_yaml(production.ledger_path(book_slug))
    queue_entry = production.find_queue_entry(queue, book_slug, proposal_id)
    proposal = production.find_proposal(ledger, proposal_id)
    accepted = production.ensure_pair(proposal, "accepted")
    color_relative = str(accepted.get("color") or "")
    if not color_relative:
        raise RuntimeError(
            f"{proposal_id} needs an accepted color master before an existing B&W asset can be adopted"
        )

    color = production.absolute_set_path(book_slug, color_relative)
    if not color.is_file():
        raise RuntimeError(f"Accepted color master does not exist: {color}")
    production.mechanical_check(color, "color")
    pair_ok, semantic = production.pair_vision(color, absolute)

    queue_entry["bw_rendered_path"] = relative
    queue_entry["bw_semantic_model"] = semantic.get("model")
    queue_entry["bw_semantic_score"] = semantic.get("score")
    queue_entry["bw_semantic_verdict"] = semantic.get("verdict")
    queue_entry["bw_semantic_reasons"] = semantic.get("reasons")
    queue_entry["bw_completed_at"] = production.now_iso()
    queue_entry["adopted_bw_path"] = relative
    queue_entry["adopted_bw_at"] = production.now_iso()

    if not pair_ok:
        queue_entry["bw_status"] = "needs_review"
        queue_entry["pair_status"] = "needs_review"
        queue_entry["pair_semantic_score"] = semantic.get("score")
        queue_entry["pair_semantic_reasons"] = semantic.get("reasons")
        production.write_yaml(production.QUEUE_FILE, queue)
        print(
            f"  ADOPTION-REVIEW {book_slug}/{proposal_id}: "
            + "; ".join(semantic.get("reasons") or [])
        )
        return False

    accepted["bw"] = relative
    queue_entry["bw_status"] = "approved"
    queue_entry["bw_approved_at"] = production.now_iso()
    queue_entry.pop("pair_status", None)
    queue_entry.pop("pair_semantic_reasons", None)
    production.replace_ledger_pair_value(
        book_slug,
        proposal_id,
        "accepted",
        "bw",
        relative,
    )
    production.write_yaml(production.QUEUE_FILE, queue)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--operation", choices=ALLOWED_OPERATIONS, required=True)
    parser.add_argument("--book", choices=production.BOOKS, required=True)
    parser.add_argument("--proposal-id", required=True)
    parser.add_argument("--source-path", required=True)
    args = parser.parse_args()

    print(
        f"{'LIVE' if args.live else 'DRY RUN'}: {args.operation} "
        f"{args.book}/{args.proposal_id} from {args.source_path}"
    )
    if not args.live:
        safe_source(args.book, args.source_path)
        return 0

    if args.operation == "accept-color":
        adopt_color(args.book, args.proposal_id, args.source_path)
        print(f"  ADOPTED color {args.book}/{args.proposal_id}")
        return 0

    adopted = adopt_bw(args.book, args.proposal_id, args.source_path)
    if adopted:
        print(f"  ADOPTED B&W {args.book}/{args.proposal_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
