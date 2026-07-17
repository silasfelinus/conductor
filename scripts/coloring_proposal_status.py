#!/usr/bin/env python3
"""Validate and summarize coloring-book proposal ledgers and the color ArtJob queue.

Incomplete books are normal and do not fail --check. Structural drift does.
Use --strict-finals only when verifying all three books are ready for packaging.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SETS_DIR = ROOT / "projects" / "coloring-book" / "sets"
CATALOG_PATH = SETS_DIR / "catalog.yaml"
COLOR_QUEUE_PATH = ROOT / "projects" / "coloring-book" / "color-art-jobs.yaml"
EXPECTED_SLOTS = list(range(1, 37))


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = yaml.safe_load(handle) or {}
    if not isinstance(value, dict):
        raise ValueError(f"{path}: root must be a mapping")
    return value


def pair(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def populated(value: Any) -> bool:
    return value not in (None, "", [], {})


def load_color_queue() -> tuple[list[str], dict[str, dict[str, Any]], dict[str, dict[str, int]]]:
    errors: list[str] = []
    by_id: dict[str, dict[str, Any]] = {}
    by_book: dict[str, dict[str, int]] = {}

    if not COLOR_QUEUE_PATH.exists():
        return [f"missing color queue {COLOR_QUEUE_PATH.relative_to(ROOT)}"], by_id, by_book

    queue = load_yaml(COLOR_QUEUE_PATH)
    batch_size = ((queue.get("batch_policy") or {}).get("worker_pass_size"))
    if batch_size != 18:
        errors.append(f"color queue worker_pass_size must be 18, found {batch_size!r}")

    books = queue.get("books")
    if not isinstance(books, list):
        return errors + ["color queue books must be a list"], by_id, by_book

    for book in books:
        if not isinstance(book, dict):
            errors.append(f"color queue book is not a mapping: {book!r}")
            continue
        slug = str(book.get("slug") or "")
        entries = book.get("entries")
        if not slug or not isinstance(entries, list):
            errors.append(f"color queue book missing slug or entries: {book!r}")
            continue
        counts = {"pending": 0, "done": 0, "approved": 0}
        if len(entries) != 36:
            errors.append(f"{slug}: color queue expected 36 entries, found {len(entries)}")
        slots = [entry.get("slot") for entry in entries if isinstance(entry, dict)]
        if sorted(slots) != EXPECTED_SLOTS:
            errors.append(f"{slug}: color queue slots must be exactly 1..36")

        for entry in entries:
            if not isinstance(entry, dict):
                errors.append(f"{slug}: color queue entry is not a mapping")
                continue
            item_id = str(entry.get("id") or "")
            status = str(entry.get("status") or "pending").lower()
            if not item_id:
                errors.append(f"{slug}: color queue entry missing id")
                continue
            if item_id in by_id:
                errors.append(f"duplicate color queue id: {item_id}")
            by_id[item_id] = entry
            if status not in counts:
                errors.append(f"{slug}/{item_id}: invalid color queue status {status!r}")
            else:
                counts[status] += 1
            if not entry.get("image_path"):
                errors.append(f"{slug}/{item_id}: missing image_path")
            if not entry.get("prompt") and not entry.get("source_ref"):
                errors.append(f"{slug}/{item_id}: needs prompt or source_ref")
        by_book[slug] = counts

    if len(by_id) != 108:
        errors.append(f"color queue expected 108 unique entries, found {len(by_id)}")
    return errors, by_id, by_book



def needs_verification_entries(proposal: dict[str, Any]) -> list[dict[str, Any]]:
    inspirations = proposal.get("inspirations")
    if not isinstance(inspirations, list):
        return []
    return [
        inspiration
        for inspiration in inspirations
        if isinstance(inspiration, dict) and inspiration.get("needs_visual_verification")
    ]


def next_action(proposal: dict[str, Any], job: dict[str, Any] | None) -> str | None:
    prompt = pair(proposal.get("prompt"))
    accepted = pair(proposal.get("accepted"))
    final = pair(proposal.get("final"))

    if not (populated(prompt.get("text")) or populated(prompt.get("ref"))):
        return "write proposed COLOR art prompt"

    if not populated(accepted.get("color")):
        status = str((job or {}).get("status") or "").lower()
        if status == "pending":
            return "submit color proposal ArtJob"
        if status == "done":
            return "review rendered color proposal; accept or revise"
        if status == "approved":
            return "sync approved color master into ledger"
        return "queue color proposal ArtJob"

    if not populated(accepted.get("bw")):
        return "derive faithful BW counterpart from accepted color master"
    if not populated(final.get("color")):
        return "revise and confirm final color draft"
    if not populated(final.get("bw")):
        return "revise and confirm final BW draft"
    return None


def validate_book(
    entry: dict[str, Any],
    jobs: dict[str, dict[str, Any]],
) -> tuple[list[str], dict[str, int], tuple[int, str, str] | None, list[tuple[str, str, str]]]:
    errors: list[str] = []
    slug = str(entry.get("slug") or "")
    ledger_rel = entry.get("ledger")
    if not slug or not isinstance(ledger_rel, str):
        return [f"catalog entry missing slug or ledger: {entry!r}"], {}, None, []

    path = SETS_DIR / ledger_rel
    if not path.exists():
        return [f"{slug}: missing ledger {path.relative_to(ROOT)}"], {}, None, []

    doc = load_yaml(path)
    book = doc.get("book") if isinstance(doc.get("book"), dict) else {}
    proposals = doc.get("proposals")
    if not isinstance(proposals, list):
        return [f"{slug}: proposals must be a list"], {}, None, []
    inventory = doc.get("inventory_snapshot") if isinstance(doc.get("inventory_snapshot"), dict) else {}

    if book.get("slug") != slug:
        errors.append(f"{slug}: ledger book.slug is {book.get('slug')!r}")
    if book.get("target_proposals") != 36:
        errors.append(f"{slug}: target_proposals must be 36")
    if len(proposals) != 36:
        errors.append(f"{slug}: expected 36 proposals, found {len(proposals)}")

    slots = [p.get("slot") for p in proposals if isinstance(p, dict)]
    if sorted(slots) != EXPECTED_SLOTS:
        errors.append(f"{slug}: slots must be exactly 1..36")
    ids = [p.get("id") for p in proposals if isinstance(p, dict)]
    if any(not isinstance(pid, str) or not pid for pid in ids):
        errors.append(f"{slug}: every proposal needs a non-empty string id")
    if len(ids) != len(set(ids)):
        errors.append(f"{slug}: proposal ids must be unique")

    counts = {
        "prompted": 0,
        "with_inspiration": 0,
        "accepted_color": 0,
        "accepted_bw": 0,
        "accepted_pairs": 0,
        "final_color": 0,
        "final_bw": 0,
        "final_pairs": 0,
        "jobs_pending": 0,
        "jobs_done": 0,
        "jobs_approved": 0,
    }
    first_next: tuple[int, str, str] | None = None
    needs_verification: list[tuple[str, str, str]] = []
    required = {"slot", "id", "title", "prompt", "inspirations", "accepted", "final", "notes"}

    for index, proposal in enumerate(proposals, start=1):
        if not isinstance(proposal, dict):
            errors.append(f"{slug}: proposal index {index} is not a mapping")
            continue
        missing = sorted(required - set(proposal))
        if missing:
            errors.append(f"{slug}/{proposal.get('id', index)}: missing fields {missing}")
        prompt = pair(proposal.get("prompt"))
        accepted = pair(proposal.get("accepted"))
        final = pair(proposal.get("final"))
        if not {"text", "ref"} <= set(prompt):
            errors.append(f"{slug}/{proposal.get('id')}: prompt needs text and ref keys")
        if not {"color", "bw"} <= set(accepted):
            errors.append(f"{slug}/{proposal.get('id')}: accepted needs color and bw keys")
        if not {"color", "bw"} <= set(final):
            errors.append(f"{slug}/{proposal.get('id')}: final needs color and bw keys")
        if not isinstance(proposal.get("inspirations"), list):
            errors.append(f"{slug}/{proposal.get('id')}: inspirations must be a list")
        if not isinstance(proposal.get("notes"), list):
            errors.append(f"{slug}/{proposal.get('id')}: notes must be a list")

        pid = str(proposal.get("id") or "")
        job = jobs.get(pid)
        if job is None:
            errors.append(f"{slug}/{pid}: missing color queue entry")
        else:
            job_status = str(job.get("status") or "pending").lower()
            key = f"jobs_{job_status}"
            if key in counts:
                counts[key] += 1

        has_prompt = populated(prompt.get("text")) or populated(prompt.get("ref"))
        ac = populated(accepted.get("color"))
        ab = populated(accepted.get("bw"))
        fc = populated(final.get("color"))
        fb = populated(final.get("bw"))
        counts["prompted"] += int(has_prompt)
        counts["with_inspiration"] += int(bool(proposal.get("inspirations")))
        counts["accepted_color"] += int(ac)
        counts["accepted_bw"] += int(ab)
        counts["accepted_pairs"] += int(ac and ab)
        counts["final_color"] += int(fc)
        counts["final_bw"] += int(fb)
        counts["final_pairs"] += int(fc and fb)

        action = next_action(proposal, job)
        if action and first_next is None:
            first_next = (int(proposal.get("slot") or index), pid or str(index), action)

        for inspiration in needs_verification_entries(proposal):
            needs_verification.append((slug, pid or str(index), str(inspiration.get("path") or "?")))

    if inventory.get("requires_directory_reconciliation"):
        first_next = (0, "inventory", "reconcile discovered files into proposal records")
    return errors, counts, first_next, needs_verification


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail only on structural errors.")
    parser.add_argument("--strict-finals", action="store_true", help="Also fail unless every book has 36 final pairs.")
    args = parser.parse_args()

    queue_errors, jobs, queue_counts = load_color_queue()
    catalog = load_yaml(CATALOG_PATH)
    entries = catalog.get("production_order")
    if not isinstance(entries, list):
        print("ERROR: catalog production_order must be a list")
        return 1

    all_errors: list[str] = list(queue_errors)
    all_complete = True
    all_needs_verification: list[tuple[str, str, str]] = []
    for entry in entries:
        if not isinstance(entry, dict):
            all_errors.append(f"catalog entry is not a mapping: {entry!r}")
            continue
        errors, counts, next_item, needs_verification = validate_book(entry, jobs)
        all_errors.extend(errors)
        all_needs_verification.extend(needs_verification)
        title = entry.get("title") or entry.get("slug")
        slug = str(entry.get("slug") or "")
        print(f"{entry.get('order')}. {title} ({slug})")
        if counts:
            print(
                "   "
                f"prompts {counts['prompted']}/36 | "
                f"color jobs pending/done/approved "
                f"{counts['jobs_pending']}/{counts['jobs_done']}/{counts['jobs_approved']}"
            )
            print(
                "   "
                f"accepted color/BW {counts['accepted_color']}/{counts['accepted_bw']} | "
                f"final color/BW {counts['final_color']}/{counts['final_bw']} | "
                f"final pairs {counts['final_pairs']}/36"
            )
            if next_item:
                slot, pid, action = next_item
                if slot == 0:
                    print(f"   next: {pid} — {action}")
                else:
                    print(f"   next: slot {slot:02d} {pid} — {action}")
            else:
                print("   next: package and release-gate review")
            all_complete = all_complete and counts["final_pairs"] == 36
        print()

    if all_needs_verification:
        print("NEEDS VISUAL VERIFICATION (elimination-only inspiration matches):")
        for slug, proposal_id, inspiration_path in all_needs_verification:
            print(f"- {slug}/{proposal_id}: {inspiration_path}")
        print()

    if all_errors:
        print("STRUCTURAL ERRORS:")
        for error in all_errors:
            print(f"- {error}")
        return 1

    total_pending = sum(counts.get("pending", 0) for counts in queue_counts.values())
    print(f"Color queue: {total_pending} pending; worker pass size 18")
    print("Ledger and queue structure: OK")
    if args.strict_finals and not all_complete:
        print("Final-pair gate: INCOMPLETE")
        return 2
    if args.strict_finals:
        print("Final-pair gate: COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
