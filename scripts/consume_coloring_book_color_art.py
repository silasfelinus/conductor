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
import re
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

# House style anchor. These books want INKED COMIC art — bold clean black ink
# linework with flat, cel-shaded comic color, in the tradition of European
# bande dessinee / vintage comic inking — NOT a painterly or photographic
# render. The color master is the same drawing the black-and-white coloring
# page will be traced from, so every form must be bounded by a confident,
# closed ink outline. This anchor is what keeps a creative model from drifting
# into soft airbrushed illustration (the failure mode of the old flux path).
INKED_STYLE = (
    "bold clean black ink linework, confident closed contours around every form, "
    "flat cel-shaded comic color, crisp bounded color fills, hard-edged shapes, "
    "high organized detail, strong readable silhouette, in the tradition of "
    "European bande dessinee and vintage comic inking"
)

COLOR_SUFFIX = (
    f" Render this as a finished inked-comic coloring-book design master, portrait 2:3: {INKED_STYLE}. "
    "One coherent full-bleed scene, clear hands and contact points, and enough closed shapes to "
    "support a later faithful line-art conversion. Fill the frame edge to edge. No border, no "
    "comic panels, no collage, no contact sheet, no readable text, no watermark, no signature, "
    "no brand marks, no soft airbrush haze, no painterly blur, no photographic rendering."
)

LOGO_SUFFIX = (
    f" Render this as a finished inked-comic coloring-book design master, portrait 2:3: {INKED_STYLE}, "
    "and a strong iconic silhouette. A recognizable emblem or mascot variation is allowed because "
    "this is the designated Kind Robots logo page, but include no readable words, letters, watermark, "
    "signature, border, comic panels, collage, contact sheet, soft airbrush haze, painterly blur, "
    "or photographic rendering."
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

            # Seed policy: explore with a RANDOM seed every attempt (so repeated
            # submissions of the same concept actually differ) and record the
            # concrete seed each render used. Only reuse a stored seed when the
            # entry is explicitly `lock_seed: true` — the state you want once a
            # composition is accepted and must be reproduced to derive its BW
            # coloring page. A stored `seed:` on an unlocked entry is treated as
            # provenance (last render), NOT as an input, so it no longer forces
            # identical iterations.
            locked = bool(source.get("lock_seed"))
            stored_seed = source.get("seed")
            seed = int(stored_seed) if (locked and stored_seed is not None) else None

            engine = str(source.get("engine") or defaults.get("engine") or "krea2")
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
                "size": str(source.get("size") or defaults.get("size", "1024x1536")),
                "engine": engine,
                "flux_variant": str(source.get("flux_variant") or defaults.get("flux_variant", "dev")),
                "guidance": float(source.get("guidance") or defaults.get("guidance", 3.5)),
                "seed": seed,
                "lock_seed": locked,
                "semantic_attempts": semantic_attempts,
                "source_ref": source.get("source_ref"),
                "reference_images": source.get("reference_images") or [],
                "semantic_gate_error": source.get("semantic_gate_error"),
            }
            # Steps: only pin when defaults/source ask for it, otherwise let each
            # engine run at its native cadence (Krea2 8, Klein 4, Flux-dev 30/36).
            explicit_steps = source.get("steps", defaults.get("steps"))
            if explicit_steps is not None:
                entry["steps"] = int(explicit_steps)
            # Per-concept overrides so a batch can mix engines / styles freely.
            for opt in ("lora", "lora_strength", "json_prompt", "sampler", "cfg", "negative_prompt"):
                if source.get(opt) is not None:
                    entry[opt] = source[opt]
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
        # Record the concrete seed + engine this accepted render used so it can
        # be reproduced (set `lock_seed: true` + this seed) when deriving the BW
        # coloring page from the accepted color master.
        if done.get("resolved_seed") is not None:
            source["render_seed"] = done["resolved_seed"]
        source["render_engine"] = done.get("engine")
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
    seed = entry.get("resolved_seed")
    if seed is None:
        seed = entry.get("seed") or 0
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

    used_seed = entry.get("resolved_seed")

    def mutate(source: dict[str, Any]) -> None:
        seed_for_history = used_seed if used_seed is not None else source.get("seed")
        history = source.get("semantic_rejections")
        if not isinstance(history, list):
            history = []
        history.append(
            {
                "attempt": next_attempt,
                "seed": seed_for_history,
                "engine": entry.get("engine"),
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
        source["last_render_seed"] = seed_for_history
        source["last_semantic_score"] = semantic.get("score")
        source["last_semantic_reasons"] = semantic.get("reasons") or []
        source["status"] = next_status
        source.pop("art_image_id", None)
        source.pop("completed_at", None)
        if next_status == "pending" and bool(source.get("lock_seed")):
            # Locked concept: keep the deterministic seed rotation so a
            # reproducible render can still explore a few variants on retry.
            base = int(source.get("seed") or seed_for_history or 0)
            source["previous_seed"] = base
            source["seed"] = semantic_art_quality.next_retry_seed(base, next_attempt)
        # Unlocked concepts leave `seed` unset so the next attempt randomizes.

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

    # The concrete seed the render will use — random for an unlocked exploration
    # attempt, the pinned seed for a locked one. entry_to_job baked this exact
    # value into the workflow graph; stash it on the entry so the caller records
    # "the real seed used" on the queue after the render lands.
    resolved_seed = job.get("resolvedSeed")
    entry["resolved_seed"] = resolved_seed

    payload["attempt"] = {
        "project": "coloring-book",
        "set": entry.get("set"),
        "conceptId": entry.get("concept_id"),
        "semanticAttempt": int(entry.get("semantic_attempts") or 0),
        "seed": resolved_seed,
        "engine": entry.get("engine"),
        "promptFingerprint": entry.get("prompt_fingerprint"),
        "sourceRef": entry.get("source_ref"),
    }
    # Include the resolved seed in the idempotency key so each fresh (randomized)
    # attempt is a distinct render, while a retry of the *same* built job still
    # dedupes. A locked seed therefore dedupes across runs; a random one does not.
    key_material = {
        "set": entry.get("set"),
        "concept": entry.get("concept_id"),
        "semanticAttempt": int(entry.get("semantic_attempts") or 0),
        "seed": resolved_seed,
        "engine": entry.get("engine"),
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


JOB_ID_PATTERN = re.compile(r"\bjob\s+#?(\d+)\b", re.IGNORECASE)


def referenced_job_id(entry: dict[str, Any]) -> int | None:
    """A prior run's timeout error names the ArtJob it was waiting on. Extract
    it so a later run can check whether that job actually finished instead of
    submitting a fresh (differently-seeded) duplicate."""
    match = JOB_ID_PATTERN.search(str(entry.get("semantic_gate_error") or ""))
    return int(match.group(1)) if match else None


def recover_timed_out_job(entry: dict[str, Any], job_id: int) -> tuple[bool, dict[str, Any]] | None:
    """Check a job a prior run gave up on waiting for. Unlocked entries pick a
    fresh random seed on every enqueue() call, so blindly resubmitting after a
    timeout creates a duplicate ArtJob against the render backend rather than
    reusing the one already in flight -- this recovers the original instead.

    Returns None if the job is still queued/running (leave it for next cycle).
    Raises if the job failed/was cancelled, or if it belongs to a different
    concept than expected (caller records that as a fresh semantic_gate_error,
    same as any other failure).
    """
    status, response = consumer.http_json("GET", f"{consumer.KR_BASE_URL}/api/art/queue/{job_id}")
    if status != 200 or not response or not response.get("success"):
        return None
    job = response.get("data", {}).get("job") or {}
    if job.get("status") in ("PENDING", "RUNNING"):
        return None
    if job.get("status") != "DONE":
        raise RuntimeError(f"job {job_id} {job.get('status')}: {job.get('error')}")

    art_image_id = job.get("artImageId")
    if not art_image_id:
        raise RuntimeError(f"job {job_id} DONE with no artImageId")

    attempt = (job.get("payload") or {}).get("attempt") or {}
    if attempt.get("conceptId") and str(attempt["conceptId"]) != str(entry["concept_id"]):
        raise RuntimeError(
            f"job {job_id} belongs to concept {attempt.get('conceptId')!r}, "
            f"expected {entry['concept_id']!r}"
        )

    entry["art_image_id"] = int(art_image_id)
    if attempt.get("seed") is not None:
        entry["resolved_seed"] = attempt["seed"]

    image_b64 = consumer.fetch_image_b64(art_image_id)
    destination = save_result(entry, image_b64)
    return validate_candidate(entry, destination)


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
    parser.add_argument(
        "--ids",
        help=(
            "Comma-separated queue_id list. When set, bounds the pass to exactly these "
            "pending entries (queue order preserved, --limit ignored) instead of the next "
            "N pending entries -- use this to run a recovery pass against a specific "
            "recovery_batch (see scripts/coloring_queue_status.py) without also touching "
            "unrelated pending entries that would otherwise fall within a plain --limit."
        ),
    )
    args = parser.parse_args()

    queue, pending = build_entries(args.book)
    if args.ids:
        wanted = {piece.strip() for piece in args.ids.split(",") if piece.strip()}
        todo = [entry for entry in pending if entry["queue_id"] in wanted]
        missing = wanted - {entry["queue_id"] for entry in todo}
        if missing:
            print(f"WARNING: --ids not found in pending queue: {sorted(missing)}", file=sys.stderr)
        limit_label = f"ids={sorted(wanted)}"
    else:
        configured_limit = int(((queue.get("batch_policy") or {}).get("worker_pass_size")) or 18)
        limit = args.limit if args.limit > 0 else configured_limit
        todo = pending[:limit]
        limit_label = f"limit={limit}"

    if not todo:
        print("No pending coloring-book color ArtJobs.")
        return 0

    print(
        f"{'LIVE' if args.live else 'DRY RUN'}: {len(todo)} of {len(pending)} pending "
        f"color proposal ArtJob(s) via {consumer.KR_BASE_URL}; pass {limit_label}"
    )

    if not args.live:
        for entry in todo:
            job = stable_job_body(entry)
            refs = f" refs={len(entry.get('reference_images') or [])}" if entry.get("reference_images") else ""
            seed_label = job.get("resolvedSeed")
            seed_label = "random" if entry.get("seed") is None else seed_label
            print(
                f"  {entry['set']}/{entry['concept_id']} -> {entry['image_path']} "
                f"[{job['payload']['width']}x{job['payload']['height']}] engine={entry.get('engine')} "
                f"seed={seed_label} semantic_attempt={entry['semantic_attempts']}{refs}"
            )
        return 0

    if not consumer.KR_API_TOKEN:
        print("KR_API_TOKEN is required for --live.", file=sys.stderr)
        return 1

    completed: list[dict[str, Any]] = []
    failures = 0

    for entry in todo:
        destination = target_path(entry)
        stuck_job_id: int | None = None
        try:
            recovered: tuple[bool, dict[str, Any]] | None = None
            if destination.exists():
                print(
                    f"  validating existing candidate for {entry['set']}/{entry['concept_id']} "
                    f"at {destination.relative_to(ROOT)}"
                )
            elif (stuck_job_id := referenced_job_id(entry)) is not None:
                recovered = recover_timed_out_job(entry, stuck_job_id)
                if recovered is None:
                    print(
                        f"  job {stuck_job_id} for {entry['set']}/{entry['concept_id']} still "
                        "queued/running - leaving for next cycle, no duplicate submitted"
                    )
                    continue
                destination = target_path(entry)
                print(
                    f"  recovered completed ArtJob {stuck_job_id} for "
                    f"{entry['set']}/{entry['concept_id']} (no duplicate submitted)"
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

            accepted, semantic = recovered if recovered is not None else validate_candidate(entry, destination)
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
            if stuck_job_id is not None and "ANTHROPIC_API_KEY" in str(error):
                # Recovery already reconciled a completed ArtJob (no duplicate was
                # submitted) -- the only thing that failed is verification, because
                # this pass has no semantic-gate credential. Overwriting
                # semantic_gate_error here would destroy the "job N timed out"
                # text a future recovery pass parses via referenced_job_id(), and
                # that future pass would then have no choice but to submit a
                # genuine duplicate ArtJob for the same already-completed render.
                # Leave the entry's recoverable reference untouched instead.
                print(
                    f"  RECOVERY UNVERIFIED {entry['set']}/{entry['concept_id']}: {error} -- "
                    f"job {stuck_job_id} reference left intact for a future pass with "
                    "semantic-gate credentials, no duplicate submitted",
                    file=sys.stderr,
                )
            else:
                record_semantic_gate_error(entry, error)
                print(f"  FAILED {entry['set']}/{entry['concept_id']}: {error}", file=sys.stderr)

    marked = mark_done(completed)
    print(f"{len(todo) - failures}/{len(todo)} succeeded; {marked} queue entries marked done.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
