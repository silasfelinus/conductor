#!/usr/bin/env python3
"""Validate and summarize coloring-book proposal ledgers.

Incomplete books are normal and do not fail --check. Structural drift does.
Use --strict-finals only when verifying a book is ready for packaging.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SETS_DIR = ROOT / "projects" / "coloring-book" / "sets"
CATALOG_PATH = SETS_DIR / "catalog.yaml"
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


def proposal_state(proposal: dict[str, Any]) -> str:
    accepted = pair(proposal.get("accepted"))
    final = pair(proposal.get("final"))
    final_color = populated(final.get("color"))
    final_bw = populated(final.get("bw"))
    accepted_color = populated(accepted.get("color"))
    accepted_bw = populated(accepted.get("bw"))
    prompt = pair(proposal.get("prompt"))
    has_prompt = populated(prompt.get("text")) or populated(prompt.get("ref"))
    has_inspiration = bool(proposal.get("inspirations"))

    if final_color and final_bw:
        return "final-pair"
    if final_color:
        return "final-color"
    if final_bw:
        return "final-bw"
    if accepted_color and accepted_bw:
        return "accepted-pair"
    if accepted_color:
        return "accepted-color"
    if accepted_bw:
        return "accepted-bw"
    if has_inspiration:
        return "exploring"
    if has_prompt:
        return "prompted"
    return "open"


def next_action(proposal: dict[str, Any]) -> str | None:
    prompt = pair(proposal.get("prompt"))
    accepted = pair(proposal.get("accepted"))
    final = pair(proposal.get("final"))
    if not (populated(prompt.get("text")) or populated(prompt.get("ref"))):
        return "write proposed art prompt"
    if not populated(accepted.get("color")):
        return "attach or create accepted color working master"
    if not populated(accepted.get("bw")):
        return "attach or create accepted BW working master"
    if not populated(final.get("color")):
        return "revise and confirm final color draft"
    if not populated(final.get("bw")):
        return "revise and confirm final BW draft"
    return None


def needs_verification_entries(proposal: dict[str, Any]) -> list[dict[str, Any]]:
    inspirations = proposal.get("inspirations")
    if not isinstance(inspirations, list):
        return []
    return [
        inspiration
        for inspiration in inspirations
        if isinstance(inspiration, dict) and inspiration.get("needs_visual_verification")
    ]


def validate_book(
    entry: dict[str, Any],
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

        action = next_action(proposal)
        if action and first_next is None:
            first_next = (int(proposal.get("slot") or index), str(proposal.get("id") or index), action)

        proposal_id = str(proposal.get("id") or index)
        for inspiration in needs_verification_entries(proposal):
            needs_verification.append((slug, proposal_id, str(inspiration.get("path") or "?")))

    if inventory.get("requires_directory_reconciliation"):
        first_next = (0, "inventory", "reconcile discovered files into proposal records")
    return errors, counts, first_next, needs_verification


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail only on structural ledger errors.")
    parser.add_argument("--strict-finals", action="store_true", help="Also fail unless every book has 36 final pairs.")
    args = parser.parse_args()

    catalog = load_yaml(CATALOG_PATH)
    entries = catalog.get("production_order")
    if not isinstance(entries, list):
        print("ERROR: catalog production_order must be a list")
        return 1

    all_errors: list[str] = []
    all_complete = True
    all_needs_verification: list[tuple[str, str, str]] = []
    for entry in entries:
        if not isinstance(entry, dict):
            all_errors.append(f"catalog entry is not a mapping: {entry!r}")
            continue
        errors, counts, next_item, needs_verification = validate_book(entry)
        all_errors.extend(errors)
        all_needs_verification.extend(needs_verification)
        title = entry.get("title") or entry.get("slug")
        print(f"{entry.get('order')}. {title} ({entry.get('slug')})")
        if counts:
            print(
                "   "
                f"prompts {counts['prompted']}/36 | "
                f"accepted pairs {counts['accepted_pairs']}/36 | "
                f"final pairs {counts['final_pairs']}/36"
            )
            print(
                "   "
                f"accepted color/BW {counts['accepted_color']}/{counts['accepted_bw']} | "
                f"final color/BW {counts['final_color']}/{counts['final_bw']} | "
                f"with inspiration {counts['with_inspiration']}"
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

    print("Ledger structure: OK")
    if args.strict_finals and not all_complete:
        print("Final-pair gate: INCOMPLETE")
        return 2
    if args.strict_finals:
        print("Final-pair gate: COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
