#!/usr/bin/env python3
"""Generate, adopt, accept, and finalize Coloring Book cover source art."""

from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

import yaml

sys.path.insert(0, str(Path(__file__).parent))
import art_quality  # noqa: E402
import consume_art_queue as consumer  # noqa: E402
import semantic_art_quality  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
COLORING_ROOT = ROOT / "projects" / "coloring-book"
QUEUE_FILE = COLORING_ROOT / "cover-art-jobs.yaml"
SETS_DIR = COLORING_ROOT / "sets"
BOOKS = ("monster-recast", "hollywood-recast", "kind-robots")
OPERATIONS = ("generate-cover", "accept-cover", "finalize-cover")
IMAGE_SUFFIXES = {".webp", ".png", ".jpg", ".jpeg"}

COVER_SUFFIX = (
    " Render as premium portrait front-cover source art with bold clean black ink contours, "
    "crisp bounded flat and cel-shaded color, organized detail, strong silhouettes, one coherent "
    "full-bleed scene, and a quiet uncluttered title area across the upper fifth. The image itself "
    "contains no readable words. No border, comic panels, collage, contact sheet, watermark, "
    "signature, copied poster typography, painterly haze, photographic rendering, or soft blur."
)


def now_iso() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def stamp() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def clean(value: Any) -> str:
    return " ".join(str(value or "").split())


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise RuntimeError(f"Expected YAML mapping: {path}")
    return data


def write_queue(queue: dict[str, Any]) -> None:
    QUEUE_FILE.write_text(
        yaml.safe_dump(queue, sort_keys=False, allow_unicode=True, width=110),
        encoding="utf-8",
    )


def find_cover(queue: dict[str, Any], book_slug: str) -> dict[str, Any]:
    for cover in queue.get("covers") or []:
        if isinstance(cover, dict) and str(cover.get("book_slug")) == book_slug:
            return cover
    raise RuntimeError(f"Cover queue entry not found: {book_slug}")


def set_dir(book_slug: str) -> Path:
    return SETS_DIR / book_slug


def relative_to_set(book_slug: str, value: str) -> str:
    path = str(value or "").strip().replace("\\", "/")
    prefix = f"projects/coloring-book/sets/{book_slug}/"
    if path.startswith(prefix):
        return path[len(prefix) :]
    return path.removeprefix("./")


def absolute_set_path(book_slug: str, value: str) -> Path:
    relative = relative_to_set(book_slug, value)
    if (
        not relative
        or relative.startswith("/")
        or ":" in relative
        or ".." in Path(relative).parts
    ):
        raise RuntimeError(f"Unsafe set-relative path: {value!r}")
    root = set_dir(book_slug).resolve()
    path = (root / relative).resolve()
    if root not in path.parents:
        raise RuntimeError(f"Path escapes {book_slug} set: {value!r}")
    return path


def safe_source(book_slug: str, value: str) -> tuple[str, Path]:
    relative = relative_to_set(book_slug, value)
    if Path(relative).suffix.lower() not in IMAGE_SUFFIXES:
        raise RuntimeError("Cover source must be an image inside the selected set")
    path = absolute_set_path(book_slug, relative)
    if not path.is_file():
        raise RuntimeError(f"Cover source does not exist: {path}")
    return relative, path


def yaml_scalar(value: str | None) -> str:
    return "null" if not value else json.dumps(value)


def replace_ledger_cover_value(
    book_slug: str,
    section_name: str,
    value: str,
) -> None:
    path = set_dir(book_slug) / "proposals.yaml"
    content = path.read_text(encoding="utf-8")
    cover_match = re.search(r"^cover:\s*$", content, re.MULTILINE)
    proposals_match = re.search(r"^proposals:\s*$", content, re.MULTILINE)
    if not cover_match or not proposals_match or proposals_match.start() <= cover_match.start():
        raise RuntimeError(f"Canonical cover section not found: {path}")

    start = cover_match.start()
    end = proposals_match.start()
    block = content[start:end]
    serialized = yaml_scalar(value)
    inline = re.search(
        rf"^  {re.escape(section_name)}:\s*\{{color:\s*(.*?),\s*bw:\s*(.*?)\}}\s*$",
        block,
        re.MULTILINE,
    )
    if inline:
        replacement = f"  {section_name}: {{color: {serialized}, bw: {inline.group(2).strip()}}}"
        updated = block[: inline.start()] + replacement + block[inline.end() :]
    else:
        section = re.search(
            rf"^  {re.escape(section_name)}:\s*$([\s\S]*?)(?=^  [a-z_]+:|\Z)",
            block,
            re.MULTILINE,
        )
        if not section:
            raise RuntimeError(f"cover.{section_name} not found: {path}")
        section_text = section.group(0)
        color_line = re.search(r"^    color:\s*.*$", section_text, re.MULTILINE)
        if not color_line:
            raise RuntimeError(f"cover.{section_name}.color not found: {path}")
        updated_section = (
            section_text[: color_line.start()]
            + f"    color: {serialized}"
            + section_text[color_line.end() :]
        )
        updated = block[: section.start()] + updated_section + block[section.end() :]

    path.write_text(content[:start] + updated + content[end:], encoding="utf-8")


def save_image(path: Path, image_b64: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = base64.b64decode(image_b64)
    if path.suffix.lower() == ".webp":
        try:
            from PIL import Image
        except ImportError as error:
            raise RuntimeError("Pillow is required for WebP cover output") from error
        with Image.open(io.BytesIO(raw)) as image:
            image.convert("RGB").save(path, "WEBP", quality=94, method=6)
        return
    path.write_bytes(raw)


def archive_candidate(path: Path) -> str | None:
    if not path.exists():
        return None
    target_dir = path.parent / "revisions"
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{path.stem}-{stamp()}{path.suffix}"
    index = 2
    while target.exists():
        target = target_dir / f"{path.stem}-{stamp()}-{index}{path.suffix}"
        index += 1
    shutil.move(str(path), str(target))
    return str(target.relative_to(ROOT))


def reject_candidate(path: Path, category: str) -> str:
    target_dir = path.parent / "rejected" / category
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{path.stem}-{stamp()}{path.suffix}"
    shutil.move(str(path), str(target))
    return str(target.relative_to(ROOT))


def mechanical(path: Path) -> tuple[bool, list[str], dict[str, Any]]:
    ok, reasons, info = art_quality.assess_file(path, "color")
    if ok is None:
        raise RuntimeError(reasons[0] if reasons else "cover quality gate unavailable")
    return bool(ok), [str(reason) for reason in reasons], info


def semantic(path: Path, prompt: str) -> tuple[bool, dict[str, Any]]:
    return semantic_art_quality.assess_semantic_file(path, prompt)


def job_status(job_id: int) -> dict[str, Any] | None:
    status, response = consumer.http_json("GET", f"{consumer.KR_BASE_URL}/api/art/queue/{job_id}")
    if status != 200 or not response or not response.get("success"):
        return None
    job = (response.get("data") or {}).get("job")
    return job if isinstance(job, dict) else None


def enqueue_cover(
    cover: dict[str, Any],
    defaults: dict[str, Any],
    revision: int,
) -> tuple[int, int | None]:
    prompt = clean(cover.get("prompt"))
    full_prompt = clean(prompt + COVER_SUFFIX)
    entry = {
        "id": f"coloring-book-cover-{cover['book_slug']}-r{revision}",
        "project": "coloring-book",
        "set": str(cover["book_slug"]),
        "kind": "cover-source",
        "variant": "color",
        "image_path": str(cover["image_path"]),
        "size": str(cover.get("size") or defaults.get("size") or "1024x1536"),
        "engine": str(cover.get("engine") or defaults.get("engine") or "krea2"),
        "steps": int(cover.get("steps") or defaults.get("steps") or 8),
        "guidance": float(cover.get("guidance") or defaults.get("guidance") or 3.5),
        "prompt": full_prompt,
        "negative_prompt": (
            "readable text, letters, title, logo, watermark, signature, border, collage, "
            "comic panels, contact sheet, actor likeness, copied poster, blurry, photographic"
        ),
    }
    job = consumer.entry_to_job(entry)
    seed = job.get("resolvedSeed")
    fingerprint = hashlib.sha256(
        json.dumps(
            {
                "book": cover["book_slug"],
                "revision": revision,
                "prompt": full_prompt,
                "seed": seed,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    job["idempotencyKey"] = f"coloring-book-cover:{cover['book_slug']}:{fingerprint}"
    status, response = consumer.http_json("POST", f"{consumer.KR_BASE_URL}/api/art/queue", job)
    if status not in (200, 201) or not response or not response.get("success"):
        message = response.get("message") if isinstance(response, dict) else response
        raise RuntimeError(f"cover enqueue failed: HTTP {status} {message}")
    queued = ((response.get("data") or {}).get("job") or {})
    return int(queued["id"]), int(seed) if isinstance(seed, int) else None


def recover_or_generate(
    queue: dict[str, Any],
    cover: dict[str, Any],
    defaults: dict[str, Any],
    timeout: int,
) -> tuple[int, Path]:
    target = ROOT / str(cover["image_path"])
    job_id = cover.get("job_id")
    if isinstance(job_id, int) and job_id > 0:
        job = job_status(job_id)
        if job and job.get("status") in ("PENDING", "RUNNING"):
            job = consumer.wait_for_job(job_id, timeout)
        if job and job.get("status") == "DONE":
            art_image_id = job.get("artImageId")
            if not art_image_id:
                raise RuntimeError(f"Cover ArtJob {job_id} completed without artImageId")
            if not target.exists():
                save_image(target, consumer.fetch_image_b64(int(art_image_id)))
            return int(art_image_id), target
        if job and job.get("status") in ("FAILED", "CANCELLED"):
            cover["status"] = "failed"
            cover["error"] = job.get("error")
            write_queue(queue)
            raise RuntimeError(f"Cover ArtJob {job_id} {job.get('status')}: {job.get('error')}")

    history = cover.get("revision_history")
    revision = len(history) if isinstance(history, list) else 0
    job_id, seed = enqueue_cover(cover, defaults, revision)
    cover["job_id"] = job_id
    cover["status"] = "running"
    cover["render_seed"] = seed
    cover["requested_at"] = now_iso()
    write_queue(queue)
    job = consumer.wait_for_job(job_id, timeout)
    art_image_id = job.get("artImageId")
    if not art_image_id:
        raise RuntimeError(f"Cover ArtJob {job_id} completed without artImageId")
    save_image(target, consumer.fetch_image_b64(int(art_image_id)))
    return int(art_image_id), target


def generate_cover(
    book_slug: str,
    *,
    timeout: int,
    force: bool,
) -> bool:
    queue = load_yaml(QUEUE_FILE)
    defaults = queue.get("defaults") if isinstance(queue.get("defaults"), dict) else {}
    cover = find_cover(queue, book_slug)
    prompt = clean(cover.get("prompt"))
    if len(prompt) < 40:
        raise RuntimeError(f"{book_slug} cover prompt is empty or too short")

    target = ROOT / str(cover["image_path"])
    if force:
        history = cover.get("revision_history")
        if not isinstance(history, list):
            history = []
        history.append(
            {
                "requested_at": now_iso(),
                "previous_status": cover.get("status"),
                "art_image_id": cover.get("art_image_id"),
                "rendered_path": cover.get("rendered_path"),
                "semantic_score": cover.get("semantic_score"),
                "archived_path": archive_candidate(target),
            }
        )
        cover["revision_history"] = history
        for key in (
            "art_image_id",
            "completed_at",
            "error",
            "job_id",
            "rejected_path",
            "render_engine",
            "rendered_path",
            "semantic_model",
            "semantic_reasons",
            "semantic_score",
            "semantic_verdict",
        ):
            cover[key] = None if key not in ("semantic_reasons",) else []
        cover["status"] = "pending"
        write_queue(queue)
    elif str(cover.get("status") or "pending") in ("done", "approved", "final", "needs_review"):
        raise RuntimeError(
            f"{book_slug} cover status is {cover.get('status')}; accept it or request a forced revision"
        )

    art_image_id, target = recover_or_generate(queue, cover, defaults, timeout)
    mechanical_ok, reasons, info = mechanical(target)
    if not mechanical_ok:
        rejected = reject_candidate(target, "mechanical")
        cover["status"] = "needs_review"
        cover["art_image_id"] = art_image_id
        cover["rejected_path"] = rejected
        cover["semantic_verdict"] = "mechanical-reject"
        cover["semantic_reasons"] = reasons
        cover["mechanical_info"] = info
        cover["completed_at"] = now_iso()
        write_queue(queue)
        print(f"  COVER-REVIEW {book_slug}: {'; '.join(reasons)} -> {rejected}")
        return False

    accepted, review = semantic(target, prompt)
    if not accepted:
        rejected = reject_candidate(target, "semantic")
        cover["status"] = "needs_review"
        cover["art_image_id"] = art_image_id
        cover["rejected_path"] = rejected
        cover["semantic_model"] = review.get("model")
        cover["semantic_score"] = review.get("score")
        cover["semantic_verdict"] = review.get("verdict")
        cover["semantic_reasons"] = review.get("reasons") or []
        cover["completed_at"] = now_iso()
        write_queue(queue)
        print(
            f"  COVER-REVIEW {book_slug}: "
            + "; ".join(review.get("reasons") or [])
            + f" -> {rejected}"
        )
        return False

    cover["status"] = "done"
    cover["art_image_id"] = art_image_id
    cover["rendered_path"] = str(target.relative_to(ROOT))
    cover["render_engine"] = str(cover.get("engine") or defaults.get("engine") or "krea2")
    cover["semantic_model"] = review.get("model")
    cover["semantic_score"] = review.get("score")
    cover["semantic_verdict"] = review.get("verdict")
    cover["semantic_reasons"] = review.get("reasons") or []
    cover["completed_at"] = now_iso()
    cover["error"] = None
    write_queue(queue)
    print(
        f"  COVER-DONE {book_slug} -> {target.relative_to(ROOT)} "
        f"(ArtImage {art_image_id}, semantic={review.get('score')})"
    )
    return True


def accept_cover(book_slug: str, source_path: str | None = None) -> bool:
    queue = load_yaml(QUEUE_FILE)
    cover = find_cover(queue, book_slug)
    selected = source_path or str(cover.get("rendered_path") or "")
    if not selected:
        raise RuntimeError(f"{book_slug} has no cover candidate to accept")
    relative, path = safe_source(book_slug, selected)
    ok, reasons, info = mechanical(path)
    if not ok:
        cover["status"] = "needs_review"
        cover["adoption_reasons"] = reasons
        cover["mechanical_info"] = info
        write_queue(queue)
        print(f"  COVER-REVIEW {book_slug}: {'; '.join(reasons)}")
        return False

    review_ok, review = semantic(path, clean(cover.get("prompt")))
    cover["semantic_model"] = review.get("model")
    cover["semantic_score"] = review.get("score")
    cover["semantic_verdict"] = review.get("verdict")
    cover["semantic_reasons"] = review.get("reasons") or []
    if not review_ok:
        cover["status"] = "needs_review"
        write_queue(queue)
        print(
            f"  COVER-REVIEW {book_slug}: "
            + "; ".join(review.get("reasons") or [])
        )
        return False

    cover["status"] = "approved"
    cover["accepted_path"] = relative
    cover["approved_at"] = now_iso()
    cover["rendered_path"] = f"projects/coloring-book/sets/{book_slug}/{relative}"
    cover["adopted_path"] = relative if source_path else None
    replace_ledger_cover_value(book_slug, "accepted", relative)
    write_queue(queue)
    print(f"  COVER-ACCEPTED {book_slug} -> {relative}")
    return True


def finalize_cover(book_slug: str) -> bool:
    queue = load_yaml(QUEUE_FILE)
    cover = find_cover(queue, book_slug)
    accepted = str(cover.get("accepted_path") or "")
    if not accepted:
        raise RuntimeError(f"{book_slug} needs an accepted cover first")
    relative, path = safe_source(book_slug, accepted)
    ok, reasons, info = mechanical(path)
    if not ok:
        cover["status"] = "needs_review"
        cover["mechanical_info"] = info
        cover["semantic_reasons"] = reasons
        write_queue(queue)
        return False
    review_ok, review = semantic(path, clean(cover.get("prompt")))
    cover["semantic_score"] = review.get("score")
    cover["semantic_verdict"] = review.get("verdict")
    cover["semantic_reasons"] = review.get("reasons") or []
    if not review_ok:
        cover["status"] = "needs_review"
        write_queue(queue)
        return False

    cover["status"] = "final"
    cover["final_path"] = relative
    cover["finalized_at"] = now_iso()
    replace_ledger_cover_value(book_slug, "final", relative)
    write_queue(queue)
    print(f"  COVER-FINAL {book_slug} -> {relative}")
    return True


def run_operation(
    operation: str,
    book_slug: str,
    *,
    timeout: int,
    force: bool,
    source_path: str | None,
    live: bool,
) -> int:
    print(
        f"{'LIVE' if live else 'DRY RUN'}: {operation} {book_slug}"
        + (f" from {source_path}" if source_path else "")
    )
    if not live:
        queue = load_yaml(QUEUE_FILE)
        find_cover(queue, book_slug)
        if source_path:
            safe_source(book_slug, source_path)
        return 0

    if operation == "generate-cover":
        generate_cover(book_slug, timeout=timeout, force=force)
    elif operation == "accept-cover":
        accept_cover(book_slug, source_path)
    else:
        finalize_cover(book_slug)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--operation", choices=OPERATIONS, required=True)
    parser.add_argument("--book", choices=BOOKS, required=True)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--source-path")
    args = parser.parse_args()

    if not 30 <= args.timeout <= 900:
        parser.error("--timeout must be between 30 and 900")
    if args.force and args.operation != "generate-cover":
        parser.error("--force is supported only for generate-cover")
    if args.source_path and args.operation != "accept-cover":
        parser.error("--source-path is supported only for accept-cover")
    if args.operation == "generate-cover" and args.live and not consumer.KR_API_TOKEN:
        parser.error("KR_API_TOKEN is required for live cover generation")

    return run_operation(
        args.operation,
        args.book,
        timeout=args.timeout,
        force=args.force,
        source_path=args.source_path,
        live=args.live,
    )


if __name__ == "__main__":
    raise SystemExit(main())
