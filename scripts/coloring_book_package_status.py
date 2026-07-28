#!/usr/bin/env python3
"""Build canonical source-asset and print-package readiness for Coloring Book titles."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG_FILE = ROOT / "projects" / "coloring-book" / "print-package.yaml"
STATUS_FILE = ROOT / "projects" / "coloring-book" / "print-readiness.yaml"
LAYOUT_FIELDS = (
    "trim_width_inches",
    "trim_height_inches",
    "bleed_inches",
    "binding",
    "paper",
    "interior_color_mode",
    "cover_color_mode",
    "printer_template",
    "page_count_includes_blanks",
    "inside_cover_printing",
    "barcode_area_reserved",
)
EXPORT_FIELDS = ("interior_pdf", "cover_wrap_pdf", "source_archive")


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise RuntimeError(f"Expected YAML mapping: {path}")
    return data


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=110),
        encoding="utf-8",
    )


def relative_file(value: Any) -> tuple[str | None, bool]:
    clean = str(value or "").strip().replace("\\", "/")
    if (
        not clean
        or clean.startswith("/")
        or ":" in clean
        or ".." in Path(clean).parts
    ):
        return None, False
    path = ROOT / clean if clean.startswith("projects/") else None
    return clean, bool(path and path.is_file())


def set_asset(book_slug: str, value: Any) -> tuple[str | None, bool]:
    clean = str(value or "").strip().replace("\\", "/")
    if not clean:
        return None, False
    prefix = f"projects/coloring-book/sets/{book_slug}/"
    repo_path = clean if clean.startswith("projects/") else prefix + clean.removeprefix("./")
    if (
        not repo_path.startswith(prefix)
        or repo_path.startswith("/")
        or ":" in repo_path
        or ".." in Path(repo_path).parts
    ):
        return clean, False
    return clean, (ROOT / repo_path).is_file()


def find_cover(cover_queue: dict[str, Any], book_slug: str) -> dict[str, Any]:
    for cover in cover_queue.get("covers") or []:
        if isinstance(cover, dict) and str(cover.get("book_slug")) == book_slug:
            return cover
    return {}


def proposal_rows(ledger: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [row for row in ledger.get("proposals") or [] if isinstance(row, dict)]
    return sorted(rows, key=lambda row: int(row.get("slot") or 999))


def layout_status(layout: dict[str, Any]) -> tuple[bool, list[str]]:
    missing = [field for field in LAYOUT_FIELDS if layout.get(field) is None or layout.get(field) == ""]
    return not missing, missing


def export_status(exports: dict[str, Any]) -> tuple[bool, list[str], dict[str, bool]]:
    missing: list[str] = []
    existence: dict[str, bool] = {}
    for field in EXPORT_FIELDS:
        value = exports.get(field)
        path, exists = relative_file(value)
        existence[field] = exists
        if not path or not exists:
            missing.append(field)
    return not missing, missing, existence


def build_book_status(
    config: dict[str, Any],
    requirements: dict[str, Any],
    cover_queue: dict[str, Any],
) -> dict[str, Any]:
    slug = str(config.get("slug") or "")
    ledger_path = ROOT / str(config.get("ledger_path") or "")
    ledger = load_yaml(ledger_path)
    expected_slots = int(requirements.get("interior_slots") or 36)
    rows = proposal_rows(ledger)

    slot_counts: dict[int, int] = {}
    interiors: list[dict[str, Any]] = []
    missing_prompts: list[str] = []
    missing_final_color: list[str] = []
    missing_final_bw: list[str] = []
    missing_color_files: list[str] = []
    missing_bw_files: list[str] = []

    for row in rows:
        slot = int(row.get("slot") or 0)
        slot_counts[slot] = slot_counts.get(slot, 0) + 1
        proposal_id = str(row.get("id") or f"slot-{slot}")
        prompt = row.get("prompt") if isinstance(row.get("prompt"), dict) else {}
        prompt_text = str(prompt.get("text") or "").strip()
        prompt_ref = str(prompt.get("ref") or "").strip()
        if not prompt_text and not prompt_ref:
            missing_prompts.append(proposal_id)

        final = row.get("final") if isinstance(row.get("final"), dict) else {}
        color_path, color_exists = set_asset(slug, final.get("color"))
        bw_path, bw_exists = set_asset(slug, final.get("bw"))
        if not color_path:
            missing_final_color.append(proposal_id)
        elif not color_exists:
            missing_color_files.append(proposal_id)
        if not bw_path:
            missing_final_bw.append(proposal_id)
        elif not bw_exists:
            missing_bw_files.append(proposal_id)

        interiors.append(
            {
                "slot": slot,
                "id": proposal_id,
                "title": str(row.get("title") or proposal_id),
                "final_color": color_path,
                "final_color_exists": color_exists,
                "final_bw": bw_path,
                "final_bw_exists": bw_exists,
            }
        )

    expected = set(range(1, expected_slots + 1))
    actual = set(slot_counts)
    missing_slots = sorted(expected - actual)
    extra_slots = sorted(actual - expected)
    duplicate_slots = sorted(slot for slot, count in slot_counts.items() if count > 1)

    cover = find_cover(cover_queue, slug)
    cover_path, cover_exists = set_asset(slug, cover.get("final_path"))
    cover_final = bool(cover_path and cover_exists and str(cover.get("status")) == "final")

    source_issues = {
        "missing_slots": missing_slots,
        "extra_slots": extra_slots,
        "duplicate_slots": duplicate_slots,
        "missing_prompts": missing_prompts,
        "missing_final_color": missing_final_color,
        "missing_final_bw": missing_final_bw,
        "missing_color_files": missing_color_files,
        "missing_bw_files": missing_bw_files,
        "cover_not_final": not cover_final,
        "cover_final_path": cover_path,
        "cover_final_exists": cover_exists,
    }
    source_ready = not any(
        (
            missing_slots,
            extra_slots,
            duplicate_slots,
            missing_prompts,
            missing_final_color,
            missing_final_bw,
            missing_color_files,
            missing_bw_files,
        )
    ) and cover_final

    layout = config.get("layout") if isinstance(config.get("layout"), dict) else {}
    exports = config.get("exports") if isinstance(config.get("exports"), dict) else {}
    layout_ready, missing_layout = layout_status(layout)
    exports_ready, missing_exports, export_exists = export_status(exports)
    package_ready = source_ready and layout_ready and exports_ready

    if package_ready:
        status = "package-ready"
        next_action = "Review and publish the validated print package."
    elif source_ready and not layout_ready:
        status = "layout-needed"
        next_action = "Choose the printer and complete trim, bleed, binding, color, and template fields."
    elif source_ready:
        status = "exports-needed"
        next_action = "Generate the ordered interior PDF, cover-wrap PDF, and source archive."
    else:
        status = "source-production"
        next_action = "Finish and finalize missing interior pairs and cover source art."

    manifest_path = ROOT / str(exports.get("ordered_interior_manifest") or "")
    if str(exports.get("ordered_interior_manifest") or ""):
        write_yaml(
            manifest_path,
            {
                "schema_version": 1,
                "book": slug,
                "title": str(config.get("title") or slug),
                "print_interior_variant": requirements.get("print_interior_variant") or "bw",
                "source_ready": source_ready,
                "cover_source": cover_path,
                "interiors": interiors,
            },
        )

    return {
        "order": int(config.get("order") or 999),
        "slug": slug,
        "title": str(config.get("title") or slug),
        "status": status,
        "next_action": next_action,
        "source_ready": source_ready,
        "layout_ready": layout_ready,
        "exports_ready": exports_ready,
        "package_ready": package_ready,
        "interior_count": len(interiors),
        "expected_interior_count": expected_slots,
        "final_pair_count": sum(
            1
            for row in interiors
            if row["final_color"]
            and row["final_color_exists"]
            and row["final_bw"]
            and row["final_bw_exists"]
        ),
        "cover_status": str(cover.get("status") or "missing"),
        "source_issues": source_issues,
        "missing_layout_fields": missing_layout,
        "missing_export_fields": missing_exports,
        "export_exists": export_exists,
        "ordered_interior_manifest": str(exports.get("ordered_interior_manifest") or "") or None,
    }


def build_status(config_path: Path = CONFIG_FILE) -> dict[str, Any]:
    config = load_yaml(config_path)
    requirements = config.get("requirements") if isinstance(config.get("requirements"), dict) else {}
    books = [book for book in config.get("books") or [] if isinstance(book, dict)]
    cover_queue_path = ROOT / str(books[0].get("cover_queue_path") or "") if books else None
    cover_queue = load_yaml(cover_queue_path) if cover_queue_path else {"covers": []}
    statuses = [build_book_status(book, requirements, cover_queue) for book in books]
    statuses.sort(key=lambda item: int(item["order"]))
    return {
        "schema_version": 1,
        "project": str(config.get("project") or "coloring-book"),
        "requirements": requirements,
        "books": statuses,
        "all_source_ready": bool(statuses) and all(book["source_ready"] for book in statuses),
        "all_package_ready": bool(statuses) and all(book["package_ready"] for book in statuses),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=CONFIG_FILE)
    parser.add_argument("--output", type=Path, default=STATUS_FILE)
    parser.add_argument("--check", action="store_true", help="Fail only when a book claims package-ready but required files are missing.")
    args = parser.parse_args()

    status = build_status(args.config)
    write_yaml(args.output, status)
    for book in status["books"]:
        print(
            f"{book['slug']}: {book['status']} "
            f"({book['final_pair_count']}/{book['expected_interior_count']} final pairs; "
            f"cover={book['cover_status']})"
        )
    if args.check:
        invalid_ready = [
            book["slug"]
            for book in status["books"]
            if book["status"] == "package-ready" and not book["package_ready"]
        ]
        if invalid_ready:
            print(f"Invalid package-ready claims: {', '.join(invalid_ready)}")
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
