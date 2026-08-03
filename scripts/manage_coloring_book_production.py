#!/usr/bin/env python3
"""Apply explicit Coloring Book Studio production actions.

Color generation remains in consume_coloring_book_studio_request.py. This module
handles the human-gated production decisions around those renders:

- accept-color: promote the reviewed color candidate into the proposal ledger
- generate-bw: derive and validate a faithful line-art candidate from accepted color
- accept-bw: promote the reviewed line-art candidate into the proposal ledger
- finalize-pair: confirm the accepted color/BW files as the print-ready pair
"""

from __future__ import annotations

import argparse
import base64
import datetime
import io
import json
import os
import re
import shutil
import sys
import urllib.request
from pathlib import Path
from typing import Any

import yaml

sys.path.insert(0, str(Path(__file__).parent))
import art_quality  # noqa: E402
import consume_art_queue as queue_consumer  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
COLORING_ROOT = ROOT / "projects" / "coloring-book"
SETS_DIR = COLORING_ROOT / "sets"
QUEUE_FILE = COLORING_ROOT / "color-art-jobs.yaml"
BOOKS = ("monster-recast", "hollywood-recast", "kind-robots")
OPERATIONS = ("accept-color", "generate-bw", "accept-bw", "finalize-pair")
PAIR_MIN_SCORE = int(os.environ.get("BW_PAIR_MIN_SEMANTIC_SCORE", "80"))

BW_PROMPT = (
    "Convert the supplied accepted color master into a faithful black-and-white "
    "coloring-book page. Preserve the exact composition, subject identities, body "
    "types, pose, framing, perspective, contact points, expressions, props, and major "
    "background details. Use clean confident black outlines on a pure white background, "
    "with smooth closed contours and empty white regions ready to color. Remove every "
    "color, gray tone, gradient, shadow fill, halftone, and painterly texture. Do not "
    "redesign, simplify away important details, add text, add a border, or change the scene."
)

def now_iso() -> str:
    return (
        datetime.datetime.now(datetime.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def stamp() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise RuntimeError(f"Expected YAML mapping: {path}")
    return data


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=110),
        encoding="utf-8",
    )


def ledger_path(book_slug: str) -> Path:
    return SETS_DIR / book_slug / "proposals.yaml"


def set_dir(book_slug: str) -> Path:
    return SETS_DIR / book_slug


def find_queue_entry(queue: dict[str, Any], book_slug: str, proposal_id: str) -> dict[str, Any]:
    for book in queue.get("books") or []:
        if not isinstance(book, dict) or str(book.get("slug")) != book_slug:
            continue
        for entry in book.get("entries") or []:
            if isinstance(entry, dict) and str(entry.get("id")) == proposal_id:
                return entry
    raise RuntimeError(f"Queue entry not found: {book_slug}/{proposal_id}")


def find_proposal(ledger: dict[str, Any], proposal_id: str) -> dict[str, Any]:
    for proposal in ledger.get("proposals") or []:
        if isinstance(proposal, dict) and str(proposal.get("id")) == proposal_id:
            return proposal
    raise RuntimeError(f"Proposal not found: {proposal_id}")


def relative_to_set(book_slug: str, value: str) -> str:
    clean = str(value or "").strip().replace("\\", "/")
    prefix = f"projects/coloring-book/sets/{book_slug}/"
    if clean.startswith(prefix):
        return clean[len(prefix) :]
    return clean.removeprefix("./")


def absolute_set_path(book_slug: str, value: str) -> Path:
    clean = relative_to_set(book_slug, value)
    if not clean or clean.startswith("/") or ".." in Path(clean).parts:
        raise RuntimeError(f"Unsafe or empty set-relative path: {value!r}")
    return set_dir(book_slug) / clean


def yaml_scalar(value: str | None) -> str:
    return "null" if not value else json.dumps(value)


def replace_ledger_pair_value(
    book_slug: str,
    proposal_id: str,
    section_name: str,
    variant: str,
    value: str,
) -> None:
    path = ledger_path(book_slug)
    content = path.read_text(encoding="utf-8")
    starts = list(re.finditer(r"^- slot:\s*\d+\s*$", content, re.MULTILINE))
    block_start = -1
    block_end = -1
    for index, match in enumerate(starts):
        start = match.start()
        end = starts[index + 1].start() if index + 1 < len(starts) else len(content)
        block = content[start:end]
        if re.search(
            rf"^  id:\s*[\"']?{re.escape(proposal_id)}[\"']?\s*$",
            block,
            re.MULTILINE,
        ):
            block_start = start
            block_end = end
            break
    if block_start < 0:
        raise RuntimeError(f"Proposal block not found in ledger: {proposal_id}")

    block = content[block_start:block_end]
    inline_pattern = re.compile(
        rf"^  {re.escape(section_name)}:\s*\{{color:\s*(.*?),\s*bw:\s*(.*?)\}}\s*$",
        re.MULTILINE,
    )
    inline = inline_pattern.search(block)
    serialized = yaml_scalar(value)
    if inline:
        color = inline.group(1).strip()
        bw = inline.group(2).strip()
        if variant == "color":
            color = serialized
        else:
            bw = serialized
        replacement = f"  {section_name}: {{color: {color}, bw: {bw}}}"
        updated_block = block[: inline.start()] + replacement + block[inline.end() :]
    else:
        section_pattern = re.compile(
            rf"^  {re.escape(section_name)}:\s*$([\s\S]*?)(?=^  [a-z_]+:|\Z)",
            re.MULTILINE,
        )
        section = section_pattern.search(block)
        if not section:
            raise RuntimeError(f"{section_name} section not found for {proposal_id}")
        section_text = section.group(0)
        value_pattern = re.compile(rf"^    {re.escape(variant)}:\s*.*$", re.MULTILINE)
        if not value_pattern.search(section_text):
            raise RuntimeError(f"{section_name}.{variant} not found for {proposal_id}")
        updated_section = value_pattern.sub(
            f"    {variant}: {serialized}",
            section_text,
            count=1,
        )
        updated_block = block[: section.start()] + updated_section + block[section.end() :]

    path.write_text(
        content[:block_start] + updated_block + content[block_end:],
        encoding="utf-8",
    )


def ensure_pair(proposal: dict[str, Any], key: str) -> dict[str, Any]:
    value = proposal.get(key)
    if not isinstance(value, dict):
        value = {"color": None, "bw": None}
        proposal[key] = value
    value.setdefault("color", None)
    value.setdefault("bw", None)
    return value


def mechanical_check(path: Path, variant: str) -> None:
    ok, reasons, _info = art_quality.assess_file(path, variant)
    if ok is None:
        raise RuntimeError(reasons[0] if reasons else "image quality gate unavailable")
    if not ok:
        raise RuntimeError("; ".join(reasons) or f"{variant} image failed quality gate")


def image_data_url(path: Path) -> str:
    suffix = path.suffix.lower()
    media = {
        ".webp": "image/webp",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
    }.get(suffix, "image/png")
    return f"data:{media};base64,{base64.b64encode(path.read_bytes()).decode()}"


def save_image(path: Path, image_b64: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = base64.b64decode(image_b64)
    if path.suffix.lower() == ".webp":
        try:
            from PIL import Image
        except ImportError as error:
            raise RuntimeError("Pillow is required for WebP output") from error
        with Image.open(io.BytesIO(raw)) as image:
            image.convert("RGB").save(path, "WEBP", quality=94, method=6)
        return
    path.write_bytes(raw)


def archive_file(path: Path, category: str) -> str | None:
    if not path.exists():
        return None
    destination_dir = path.parent / "revisions" / category
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / f"{path.stem}-{stamp()}{path.suffix}"
    counter = 2
    while destination.exists():
        destination = destination_dir / f"{path.stem}-{stamp()}-{counter}{path.suffix}"
        counter += 1
    shutil.move(str(path), str(destination))
    return str(destination.relative_to(ROOT))


def reject_file(path: Path, category: str) -> str:
    destination_dir = path.parent / "rejected" / category
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / f"{path.stem}-{stamp()}{path.suffix}"
    shutil.move(str(path), str(destination))
    return str(destination.relative_to(ROOT))


def queue_job_status(job_id: int) -> dict[str, Any] | None:
    status, response = queue_consumer.http_json(
        "GET", f"{queue_consumer.KR_BASE_URL}/api/art/queue/{job_id}"
    )
    if status != 200 or not response or not response.get("success"):
        return None
    job = (response.get("data") or {}).get("job")
    return job if isinstance(job, dict) else None


def enqueue_bw_job(
    source: Path,
    timeout: int,
    queue_entry: dict[str, Any],
    queue: dict[str, Any],
) -> dict[str, Any]:
    existing_job_id = queue_entry.get("bw_job_id")
    if isinstance(existing_job_id, int) and existing_job_id > 0:
        job = queue_job_status(existing_job_id)
        if job and job.get("status") == "DONE":
            return job
        if job and job.get("status") in ("PENDING", "RUNNING"):
            return queue_consumer.wait_for_job(existing_job_id, timeout)
        if job and job.get("status") in ("FAILED", "CANCELLED"):
            queue_entry["bw_status"] = "failed"
            queue_entry["bw_error"] = job.get("error")
            write_yaml(QUEUE_FILE, queue)
            raise RuntimeError(
                f"BW ArtJob {existing_job_id} {job.get('status')}: {job.get('error')}"
            )

    body = {
        "engine": "kontext",
        "promptString": BW_PROMPT,
        "sourceImageBase64": image_data_url(source),
        "width": 1024,
        "height": 1536,
        "steps": 20,
        "guidance": 2.5,
        "denoise": 1,
        "projectSlug": "coloring-book",
        "priority": 1,
        "isPublic": False,
        "designer": "Coloring Book Studio",
    }
    status, response = queue_consumer.http_json(
        "POST", f"{queue_consumer.KR_BASE_URL}/api/art/enqueue", body
    )
    if status not in (200, 201) or not response or not response.get("success"):
        message = response.get("message") if isinstance(response, dict) else response
        raise RuntimeError(f"BW enqueue failed: HTTP {status} {message}")
    job_id = int((response.get("data") or {}).get("jobId"))
    queue_entry["bw_job_id"] = job_id
    queue_entry["bw_status"] = "running"
    queue_entry["bw_requested_at"] = now_iso()
    write_yaml(QUEUE_FILE, queue)
    return queue_consumer.wait_for_job(job_id, timeout)


def accept_color(
    book_slug: str,
    proposal_id: str,
    queue: dict[str, Any],
    ledger: dict[str, Any],
) -> None:
    queue_entry = find_queue_entry(queue, book_slug, proposal_id)
    proposal = find_proposal(ledger, proposal_id)
    accepted = ensure_pair(proposal, "accepted")
    rendered = relative_to_set(book_slug, str(queue_entry.get("rendered_path") or ""))
    if not rendered:
        raise RuntimeError(f"{proposal_id} has no rendered color candidate")
    path = absolute_set_path(book_slug, rendered)
    if not path.exists():
        raise RuntimeError(f"Color candidate does not exist: {path.relative_to(ROOT)}")
    mechanical_check(path, "color")

    accepted["color"] = rendered
    queue_entry["status"] = "approved"
    queue_entry["approved_at"] = now_iso()
    queue_entry["lock_seed"] = True
    if queue_entry.get("render_seed") is not None:
        queue_entry["seed"] = queue_entry["render_seed"]
    replace_ledger_pair_value(book_slug, proposal_id, "accepted", "color", rendered)
    write_yaml(QUEUE_FILE, queue)


def generate_bw(
    book_slug: str,
    proposal_id: str,
    queue: dict[str, Any],
    ledger: dict[str, Any],
    *,
    timeout: int,
    force: bool,
) -> None:
    queue_entry = find_queue_entry(queue, book_slug, proposal_id)
    proposal = find_proposal(ledger, proposal_id)
    accepted = ensure_pair(proposal, "accepted")
    source_rel = str(accepted.get("color") or "")
    if not source_rel:
        raise RuntimeError(f"{proposal_id} needs an accepted color master first")
    source = absolute_set_path(book_slug, source_rel)
    if not source.exists():
        raise RuntimeError(f"Accepted color master does not exist: {source.relative_to(ROOT)}")

    candidate_rel = f"generated/bw/{proposal_id}-bw.webp"
    candidate = absolute_set_path(book_slug, candidate_rel)
    existing_rel = relative_to_set(
        book_slug, str(queue_entry.get("bw_rendered_path") or candidate_rel)
    )
    existing = absolute_set_path(book_slug, existing_rel)
    bw_status = str(queue_entry.get("bw_status") or "pending").lower()

    if force:
        archived = archive_file(existing, "studio") if existing.exists() else None
        history = queue_entry.get("bw_revision_history")
        if not isinstance(history, list):
            history = []
        history.append(
            {
                "requested_at": now_iso(),
                "previous_status": bw_status,
                "art_image_id": queue_entry.get("bw_art_image_id"),
                "rendered_path": existing_rel if existing.exists() else None,
                "semantic_score": queue_entry.get("bw_semantic_score"),
                "archived_path": archived,
            }
        )
        queue_entry["bw_revision_history"] = history
        for field in (
            "bw_art_image_id",
            "bw_completed_at",
            "bw_error",
            "bw_job_id",
            "bw_mechanical_info",
            "bw_rejected_path",
            "bw_rendered_path",
            "bw_semantic_model",
            "bw_semantic_reasons",
            "bw_semantic_score",
            "bw_semantic_verdict",
        ):
            queue_entry.pop(field, None)
        queue_entry["bw_status"] = "pending"
        bw_status = "pending"
        candidate = absolute_set_path(book_slug, candidate_rel)
        write_yaml(QUEUE_FILE, queue)
    elif bw_status in ("done", "approved", "needs_review"):
        raise RuntimeError(
            f"{proposal_id} already has BW status {bw_status}; accept it or request a forced revision"
        )

    if candidate.exists():
        art_image_id = queue_entry.get("bw_art_image_id")
        if not art_image_id and isinstance(queue_entry.get("bw_job_id"), int):
            job = queue_job_status(int(queue_entry["bw_job_id"]))
            art_image_id = (job or {}).get("artImageId")
        if not art_image_id:
            raise RuntimeError(
                f"{proposal_id} has a landed BW candidate but no recoverable ArtImage id"
            )
    else:
        job = enqueue_bw_job(source, timeout, queue_entry, queue)
        art_image_id = job.get("artImageId")
        if not art_image_id:
            raise RuntimeError(f"BW ArtJob {job.get('id')} completed without artImageId")
        image_b64 = queue_consumer.fetch_image_b64(int(art_image_id))
        save_image(candidate, image_b64)
        queue_entry["bw_art_image_id"] = int(art_image_id)
        queue_entry["bw_rendered_path"] = candidate_rel
        write_yaml(QUEUE_FILE, queue)

    ok, reasons, info = art_quality.assess_file(candidate, "bw")
    if ok is None:
        raise RuntimeError(reasons[0] if reasons else "BW mechanical gate unavailable")
    if not ok:
        rejected = reject_file(candidate, "mechanical")
        queue_entry["bw_status"] = "needs_review"
        queue_entry["bw_art_image_id"] = int(art_image_id)
        queue_entry["bw_rejected_path"] = rejected
        queue_entry["bw_mechanical_info"] = info
        queue_entry["bw_render_reasons"] = reasons
        queue_entry["bw_completed_at"] = now_iso()
        write_yaml(QUEUE_FILE, queue)
        print(f"  BW-REJECT {book_slug}/{proposal_id}: {'; '.join(reasons)} -> {rejected}")
        return

    # Structurally sound line art. Whether it is a faithful counterpart to the
    # color master is a judgement call, so it lands as `done` (awaiting review)
    # and a human promotes it from the trainer panel.
    queue_entry["bw_status"] = "done"
    queue_entry["bw_art_image_id"] = int(art_image_id)
    queue_entry["bw_rendered_path"] = candidate_rel
    queue_entry["bw_mechanical_info"] = info
    queue_entry["bw_render_reasons"] = []
    queue_entry["bw_completed_at"] = now_iso()
    queue_entry.pop("bw_error", None)
    write_yaml(QUEUE_FILE, queue)
    print(
        f"  BW-LANDED {book_slug}/{proposal_id} -> {candidate.relative_to(ROOT)} "
        f"(ArtImage {art_image_id}) - awaiting human review"
    )


def accept_bw(
    book_slug: str,
    proposal_id: str,
    queue: dict[str, Any],
    ledger: dict[str, Any],
) -> None:
    queue_entry = find_queue_entry(queue, book_slug, proposal_id)
    proposal = find_proposal(ledger, proposal_id)
    accepted = ensure_pair(proposal, "accepted")
    rendered = relative_to_set(book_slug, str(queue_entry.get("bw_rendered_path") or ""))
    if not rendered:
        raise RuntimeError(f"{proposal_id} has no completed BW candidate")
    path = absolute_set_path(book_slug, rendered)
    if not path.exists():
        raise RuntimeError(f"BW candidate does not exist: {path.relative_to(ROOT)}")
    mechanical_check(path, "bw")

    accepted["bw"] = rendered
    queue_entry["bw_status"] = "approved"
    queue_entry["bw_approved_at"] = now_iso()
    replace_ledger_pair_value(book_slug, proposal_id, "accepted", "bw", rendered)
    write_yaml(QUEUE_FILE, queue)


def finalize_pair(
    book_slug: str,
    proposal_id: str,
    queue: dict[str, Any],
    ledger: dict[str, Any],
) -> None:
    queue_entry = find_queue_entry(queue, book_slug, proposal_id)
    proposal = find_proposal(ledger, proposal_id)
    accepted = ensure_pair(proposal, "accepted")
    final = ensure_pair(proposal, "final")
    color_rel = str(accepted.get("color") or "")
    bw_rel = str(accepted.get("bw") or "")
    if not color_rel or not bw_rel:
        raise RuntimeError(f"{proposal_id} needs accepted color and BW files before finalization")

    color = absolute_set_path(book_slug, color_rel)
    bw = absolute_set_path(book_slug, bw_rel)
    if not color.exists() or not bw.exists():
        raise RuntimeError(f"{proposal_id} accepted pair is missing from disk")
    mechanical_check(color, "color")
    mechanical_check(bw, "bw")
    final_color = relative_to_set(book_slug, color_rel)
    final_bw = relative_to_set(book_slug, bw_rel)
    final["color"] = final_color
    final["bw"] = final_bw
    queue_entry["pair_status"] = "final"
    queue_entry["pair_semantic_score"] = semantic.get("score")
    queue_entry["pair_finalized_at"] = now_iso()
    replace_ledger_pair_value(book_slug, proposal_id, "final", "color", final_color)
    replace_ledger_pair_value(book_slug, proposal_id, "final", "bw", final_bw)
    write_yaml(QUEUE_FILE, queue)


def run_operation(
    operation: str,
    book_slug: str,
    proposal_ids: list[str],
    *,
    timeout: int,
    force: bool,
    live: bool,
) -> int:
    mode = "LIVE" if live else "DRY RUN"
    print(f"{mode}: {operation} for {book_slug}: {', '.join(proposal_ids)}")
    if not live:
        return 0

    queue = load_yaml(QUEUE_FILE)
    ledger = load_yaml(ledger_path(book_slug))
    failures = 0
    for proposal_id in proposal_ids:
        try:
            if operation == "accept-color":
                accept_color(book_slug, proposal_id, queue, ledger)
            elif operation == "generate-bw":
                generate_bw(
                    book_slug,
                    proposal_id,
                    queue,
                    ledger,
                    timeout=timeout,
                    force=force,
                )
            elif operation == "accept-bw":
                accept_bw(book_slug, proposal_id, queue, ledger)
            else:
                finalize_pair(book_slug, proposal_id, queue, ledger)
            print(f"  DONE {operation} {book_slug}/{proposal_id}")
        except Exception as error:  # noqa: BLE001
            failures += 1
            print(f"  FAILED {operation} {book_slug}/{proposal_id}: {error}", file=sys.stderr)
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--operation", choices=OPERATIONS, required=True)
    parser.add_argument("--book", choices=BOOKS, required=True)
    parser.add_argument("--proposal-id", action="append", dest="proposal_ids", required=True)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    proposal_ids = list(
        dict.fromkeys(str(value).strip() for value in args.proposal_ids if str(value).strip())
    )
    if not proposal_ids:
        parser.error("at least one --proposal-id is required")
    if len(proposal_ids) > 18:
        parser.error("at most 18 proposal ids may be requested")
    if not 30 <= args.timeout <= 900:
        parser.error("--timeout must be between 30 and 900")
    if args.operation == "generate-bw" and args.live and not queue_consumer.KR_API_TOKEN:
        parser.error("KR_API_TOKEN is required for live BW generation")

    return run_operation(
        args.operation,
        args.book,
        proposal_ids,
        timeout=args.timeout,
        force=args.force,
        live=args.live,
    )


if __name__ == "__main__":
    raise SystemExit(main())
