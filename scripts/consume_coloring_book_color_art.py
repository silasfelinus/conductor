#!/usr/bin/env python3
"""Submit, validate, and retrieve canonical coloring-book COLOR ArtJobs.

A render is accepted only after both the local mechanical gate and the shared
vision-based semantic gate pass. Semantic failures are preserved under
rejected/semantic/, recorded in the queue, and retried with bounded explicit
lineage, a changed seed, and compact literal subject guidance.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import yaml

sys.path.insert(0, str(Path(__file__).parent))
import art_quality  # noqa: E402
import consume_art_queue as consumer  # noqa: E402
import semantic_art_quality  # noqa: E402

ROOT = consumer.ROOT
QUEUE_FILE = ROOT / "projects" / "coloring-book" / "color-art-jobs.yaml"

COLOR_SUFFIX = (
    " Render this as a finished full-color coloring-book design master, portrait 2:3: "
    "one coherent full-bleed scene, thick confident black contours, crisp bounded color, "
    "hard-edged value shapes, high organized detail, strong readable silhouette, clear "
    "hands and contact points, and enough closed shapes to support a later faithful line-art "
    "conversion. Fill the frame edge to edge. No border, no comic panels, no collage, no "
    "contact sheet, no readable text, no watermark, no signature, no brand marks, no soft "
    "airbrush haze, and no painterly blur."
)

LOGO_SUFFIX = (
    " Render this as a finished full-color coloring-book design master, portrait 2:3: "
    "one coherent full-bleed scene, thick confident black contours, crisp bounded color, "
    "hard-edged value shapes, high organized detail, and a strong iconic silhouette. A "
    "recognizable emblem or mascot variation is allowed because this is the designated "
    "Kind Robots logo page, but include no readable words, letters, watermark, signature, "
    "border, comic panels, collage, contact sheet, soft airbrush haze, or painterly blur."
)


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


def clean(value: Any) -> str:
    return " ".join(str(value or "").split())


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def prompt_fingerprint(prompt: str) -> str:
    return hashlib.sha256(clean(prompt).encode("utf-8")).hexdigest()


def find_source_prompt(source_ref: str) -> tuple[str, str]:
    path_text, sep, item_id = source_ref.partition("#")
    if not sep or not item_id:
        raise RuntimeError(f"Invalid source_ref: {source_ref}")
    path = ROOT / path_text
    doc = load_yaml(path)

    batch_entries = ((doc.get("batch") or {}).get("entries") or [])
    for entry in batch_entries:
        if isinstance(entry, dict) and str(entry.get("id")) == item_id:
            prompt = clean(entry.get("prompt"))
            if not prompt:
                raise RuntimeError(f"{source_ref}: source entry has no prompt")
            return clean(entry.get("label") or item_id), prompt

    proposals = doc.get("proposals") or []
    for proposal in proposals:
        if isinstance(proposal, dict) and str(proposal.get("id")) == item_id:
            prompt_obj = proposal.get("prompt") if isinstance(proposal.get("prompt"), dict) else {}
            prompt = clean(prompt_obj.get("text"))
            if not prompt:
                raise RuntimeError(f"{source_ref}: proposal has no direct prompt text")
            return clean(proposal.get("title") or item_id), prompt

    raise RuntimeError(f"{source_ref}: no matching entry")


def build_entries(book_filter: str | None = None) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    queue = load_yaml(QUEUE_FILE)
    defaults = queue.get("defaults") if isinstance(queue.get("defaults"), dict) else {}
    books = queue.get("books") or []
    entries: list[dict[str, Any]] = []

    for book in books:
        if not isinstance(book, dict):
            continue
        book_slug = str(book.get("slug") or "")
        if book_filter and book_slug != book_filter:
            continue

        for source in book.get("entries") or []:
            if not isinstance(source, dict):
                continue
            status = str(source.get("status") or "pending").strip().lower()
            if status != "pending":
                continue

            title = clean(source.get("title"))
            scene_prompt = clean(source.get("prompt"))
            if source.get("source_ref"):
                resolved_title, resolved_prompt = find_source_prompt(str(source["source_ref"]))
                title = title or resolved_title
                scene_prompt = scene_prompt or resolved_prompt
            if not scene_prompt:
                raise RuntimeError(f"{book_slug}/{source.get('id')}: missing color prompt")

            semantic_attempts = max(0, int(source.get("semantic_attempts") or 0))
            attempted_prompt = scene_prompt
            if semantic_attempts:
                attempted_prompt = semantic_art_quality.literal_retry_prompt(
                    scene_prompt,
                    title,
                    semantic_attempts,
                )

            suffix = LOGO_SUFFIX if source.get("allow_logo_emblem") else COLOR_SUFFIX
            full_prompt = clean(attempted_prompt + suffix)
            entry = {
                "id": f"coloring-book-{book_slug}-{source['id']}-color",
                "queue_id": str(source["id"]),
                "project": "coloring-book",
                "set": book_slug,
                "concept_id": str(source["id"]),
                "title": title,
                "variant": "color",
                "image_path": str(source["image_path"]),
                "scene_prompt": scene_prompt,
                "prompt": full_prompt,
                "prompt_fingerprint": prompt_fingerprint(full_prompt),
                "target_repo": defaults.get("target_repo", "silasfelinus/conductor"),
                "size": str(defaults.get("size", "1024x1536")),
                "engine": str(defaults.get("engine", "flux")),
                "flux_variant": str(defaults.get("flux_variant", "dev")),
                "steps": int(defaults.get("steps", 36)),
                "guidance": float(defaults.get("guidance", 3.5)),
                "seed": int(source.get("seed") or 0),
                "semantic_attempts": semantic_attempts,
                "source_ref": source.get("source_ref"),
                "reference_images": source.get("reference_images") or [],
            }
            entries.append(entry)

    entries.sort(key=lambda item: (book_order(queue, str(item["set"])), slot_for(queue, str(item["queue_id"]))))
    return queue, entries


def book_order(queue: dict[str, Any], slug: str) -> int:
    for book in queue.get("books") or []:
        if isinstance(book, dict) and str(book.get("slug")) == slug:
            return int(book.get("order") or 999)
    return 999


def slot_for(queue: dict[str, Any], queue_id: str) -> int:
    for book in queue.get("books") or []:
        if not isinstance(book, dict):
            continue
        for entry in book.get("entries") or []:
            if isinstance(entry, dict) and str(entry.get("id")) == queue_id:
                return int(entry.get("slot") or 999)
    return 999


def target_path(entry: dict[str, Any]) -> Path:
    return ROOT / str(entry["image_path"])


def save_result(entry: dict[str, Any], image_b64: str) -> Path:
    destination = target_path(entry)
    destination.parent.mkdir(parents=True, exist_ok=True)
    image_bytes = base64.b64decode(image_b64)

    if destination.suffix.lower() == ".webp":
        try:
            from PIL import Image
        except ImportError as error:
            raise RuntimeError("Pillow is required for WebP output.") from error
        image = Image.open(io.BytesIO(image_bytes))
        image.save(destination, "WEBP", quality=92, method=6)
        return destination

    destination.write_bytes(image_bytes)
    return destination


def find_queue_entry(
    queue: dict[str, Any],
    book_slug: str,
    queue_id: str,
) -> dict[str, Any]:
    for book in queue.get("books") or []:
        if not isinstance(book, dict) or str(book.get("slug")) != book_slug:
            continue
        for source in book.get("entries") or []:
            if isinstance(source, dict) and str(source.get("id")) == queue_id:
                return source
    raise RuntimeError(f"Queue entry not found: {book_slug}/{queue_id}")


def mutate_queue_entry(
    entry: dict[str, Any],
    mutate: Callable[[dict[str, Any]], None],
) -> None:
    queue = load_yaml(QUEUE_FILE)
    source = find_queue_entry(queue, str(entry["set"]), str(entry["queue_id"]))
    mutate(source)
    write_queue(queue)


def mark_done(completed: list[dict[str, Any]]) -> int:
    if not completed:
        return 0
    queue = load_yaml(QUEUE_FILE)
    changed = 0

    for done in completed:
        source = find_queue_entry(queue, str(done["set"]), str(done["queue_id"]))
        source["status"] = "done"
        source["rendered_path"] = str(done["image_path"])
        if done.get("art_image_id") is not None:
            source["art_image_id"] = int(done["art_image_id"])
        source["completed_at"] = now_iso()
        source["prompt_fingerprint"] = str(done["prompt_fingerprint"])
        source["semantic_verdict"] = done.get("semantic_verdict")
        source["semantic_score"] = done.get("semantic_score")
        source["subject_match"] = done.get("subject_match") is True
        source["on_brief"] = done.get("on_brief") is True
        source["semantic_model"] = done.get("semantic_model")
        source.pop("semantic_gate_error", None)
        changed += 1

    if changed:
        write_queue(queue)
    return changed


def rejection_destination(
    destination: Path,
    entry: dict[str, Any],
    category: str,
) -> Path:
    attempt = int(entry.get("semantic_attempts") or 0) + 1
    seed = int(entry.get("seed") or 0)
    filename = f"{destination.stem}-attempt-{attempt}-seed-{seed}{destination.suffix}"
    rejected = destination.parent / "rejected" / "semantic" / category / filename
    rejected.parent.mkdir(parents=True, exist_ok=True)
    if rejected.exists():
        rejected.unlink()
    destination.replace(rejected)
    return rejected


def record_semantic_rejection(
    entry: dict[str, Any],
    semantic: dict[str, Any],
    rejected: Path,
) -> str:
    next_attempt = int(entry.get("semantic_attempts") or 0) + 1
    max_attempts = max(1, semantic_art_quality.DEFAULT_MAX_ATTEMPTS)
    next_status = "pending" if next_attempt < max_attempts else "needs_review"

    def mutate(source: dict[str, Any]) -> None:
        current_seed = int(source.get("seed") or entry.get("seed") or 0)
        history = source.get("semantic_rejections")
        if not isinstance(history, list):
            history = []
        history.append(
            {
                "attempt": next_attempt,
                "seed": current_seed,
                "art_image_id": entry.get("art_image_id"),
                "prompt_fingerprint": entry.get("prompt_fingerprint"),
                "score": semantic.get("score"),
                "verdict": semantic.get("verdict"),
                "subject_match": semantic.get("subject_match") is True,
                "on_brief": semantic.get("on_brief") is True,
                "reasons": semantic.get("reasons") or [],
                "rejected_path": str(rejected.relative_to(ROOT)),
                "reviewed_at": now_iso(),
                "model": semantic.get("model"),
            }
        )
        source["semantic_rejections"] = history
        source["semantic_attempts"] = next_attempt
        source["last_rejected_art_image_id"] = entry.get("art_image_id")
        source["last_semantic_score"] = semantic.get("score")
        source["last_semantic_reasons"] = semantic.get("reasons") or []
        source["status"] = next_status
        source.pop("art_image_id", None)
        source.pop("completed_at", None)
        if next_status == "pending":
            source["previous_seed"] = current_seed
            source["seed"] = semantic_art_quality.next_retry_seed(current_seed, next_attempt)

    mutate_queue_entry(entry, mutate)
    return next_status


def record_semantic_gate_error(entry: dict[str, Any], error: Exception) -> None:
    def mutate(source: dict[str, Any]) -> None:
        source["semantic_gate_error"] = str(error)[:1000]
        source["semantic_gate_error_at"] = now_iso()
        source["status"] = "pending"

    mutate_queue_entry(entry, mutate)


def stable_job_body(entry: dict[str, Any]) -> dict[str, Any]:
    job = consumer.entry_to_job(entry)
    payload = job.get("payload") if isinstance(job.get("payload"), dict) else {}
    workflow = payload.get("workflow") if isinstance(payload.get("workflow"), dict) else {}
    text_node = workflow.get("59") if isinstance(workflow.get("59"), dict) else {}
    inputs = text_node.get("inputs") if isinstance(text_node.get("inputs"), dict) else {}
    if inputs:
        inputs["seed"] = (int(entry.get("seed") or 0) + 59_059) % 2_147_483_647

    payload["attempt"] = {
        "project": "coloring-book",
        "set": entry.get("set"),
        "conceptId": entry.get("concept_id"),
        "semanticAttempt": int(entry.get("semantic_attempts") or 0),
        "seed": int(entry.get("seed") or 0),
        "promptFingerprint": entry.get("prompt_fingerprint"),
        "sourceRef": entry.get("source_ref"),
    }
    key_material = {
        "set": entry.get("set"),
        "concept": entry.get("concept_id"),
        "semanticAttempt": int(entry.get("semantic_attempts") or 0),
        "seed": int(entry.get("seed") or 0),
        "promptFingerprint": entry.get("prompt_fingerprint"),
    }
    key_hash = hashlib.sha256(
        json.dumps(key_material, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    job["idempotencyKey"] = f"coloring-book:{entry['set']}:{entry['concept_id']}:{key_hash}"
    job["requireCompletionProof"] = False
    return job


def enqueue(entry: dict[str, Any]) -> tuple[int, bool]:
    status, response = consumer.http_json(
        "POST",
        f"{consumer.KR_BASE_URL}/api/art/queue",
        stable_job_body(entry),
    )
    if status not in (200, 201) or not response or not response.get("success"):
        message = response.get("message") if isinstance(response, dict) else response
        raise RuntimeError(f"enqueue failed: HTTP {status} {message}")
    data = response.get("data") or {}
    job = data.get("job") or {}
    return int(job["id"]), bool(data.get("deduplicated"))


def validate_candidate(entry: dict[str, Any], destination: Path) -> tuple[bool, dict[str, Any]]:
    ok, reasons, _info = art_quality.assess_file(destination, "color")
    if ok is False:
        return False, {
            "model": "mechanical",
            "score": 0,
            "verdict": "reject",
            "subject_match": False,
            "on_brief": False,
            "reasons": reasons,
        }
    if ok is None:
        raise RuntimeError(reasons[0] if reasons else "mechanical image gate unavailable")

    return semantic_art_quality.assess_semantic_file(
        destination,
        str(entry["scene_prompt"]),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--limit", type=int, default=0, help="0 uses queue batch_policy.worker_pass_size")
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--book", choices=("monster-recast", "hollywood-recast", "kind-robots"))
    args = parser.parse_args()

    queue, pending = build_entries(args.book)
    configured_limit = int(((queue.get("batch_policy") or {}).get("worker_pass_size")) or 18)
    limit = args.limit if args.limit > 0 else configured_limit
    todo = pending[:limit]

    if not todo:
        print("No pending coloring-book color ArtJobs.")
        return 0

    print(
        f"{'LIVE' if args.live else 'DRY RUN'}: {len(todo)} of {len(pending)} pending "
        f"color proposal ArtJob(s) via {consumer.KR_BASE_URL}; pass limit={limit}"
    )

    if not args.live:
        for entry in todo:
            job = stable_job_body(entry)
            refs = f" refs={len(entry.get('reference_images') or [])}" if entry.get("reference_images") else ""
            print(
                f"  {entry['set']}/{entry['concept_id']} -> {entry['image_path']} "
                f"[{job['payload']['width']}x{job['payload']['height']}] seed={entry['seed']} "
                f"semantic_attempt={entry['semantic_attempts']}{refs}"
            )
        return 0

    if not consumer.KR_API_TOKEN:
        print("KR_API_TOKEN is required for --live.", file=sys.stderr)
        return 1

    completed: list[dict[str, Any]] = []
    failures = 0

    for entry in todo:
        destination = target_path(entry)
        try:
            if destination.exists():
                print(
                    f"  validating existing candidate for {entry['set']}/{entry['concept_id']} "
                    f"at {destination.relative_to(ROOT)}"
                )
            else:
                job_id, deduplicated = enqueue(entry)
                suffix = " (existing matching attempt)" if deduplicated else ""
                print(
                    f"  queued ArtJob {job_id}{suffix} for "
                    f"{entry['set']}/{entry['concept_id']} color - waiting..."
                )
                job = consumer.wait_for_job(job_id, args.timeout)
                entry["art_image_id"] = int(job["artImageId"])
                image_b64 = consumer.fetch_image_b64(job["artImageId"])
                destination = save_result(entry, image_b64)

            accepted, semantic = validate_candidate(entry, destination)
            if not accepted:
                rejected = rejection_destination(destination, entry, "rejected")
                next_status = record_semantic_rejection(entry, semantic, rejected)
                failures += 1
                print(
                    f"  SEMANTIC-REJECT {entry['set']}/{entry['concept_id']}: "
                    f"{' ; '.join(semantic.get('reasons') or [])} -> "
                    f"{rejected.relative_to(ROOT)} ({next_status})",
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
                f"{destination.relative_to(ROOT)} "
                f"(ArtImage {entry.get('art_image_id') or 'existing'}, semantic={semantic.get('score')})"
            )
        except Exception as error:  # noqa: BLE001
            failures += 1
            if destination.exists():
                try:
                    rejected = rejection_destination(destination, entry, "unverified")
                    print(f"    unverified candidate moved to {rejected.relative_to(ROOT)}", file=sys.stderr)
                except Exception:  # noqa: BLE001
                    pass
            record_semantic_gate_error(entry, error)
            print(f"  FAILED {entry['set']}/{entry['concept_id']}: {error}", file=sys.stderr)

    marked = mark_done(completed)
    print(f"{len(todo) - failures}/{len(todo)} succeeded; {marked} queue entries marked done.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
