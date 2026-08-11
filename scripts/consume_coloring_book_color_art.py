#!/usr/bin/env python3
"""Submit, validate, and retrieve canonical coloring-book COLOR ArtJobs.

A render is accepted once the local mechanical gate passes -- it is a real,
structurally valid image. Quality is NOT judged here: a landed render is parked
for human review in the ArtJob trainer panel. Structural failures (blank frame,
wrong aspect, unreadable file) are preserved under rejected/render/, recorded in
the queue, and re-rolled with a changed seed up to a bounded number of attempts.

WebP output requires Pillow. A fresh sandbox may not have it -- run
`source scripts/provision_kind_robots_deps.sh` first (it installs Pillow
alongside the kind_robots verification deps; see coloring-book/t-038) rather
than rediscovering "Pillow is required for WebP output" mid-batch.
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
import render_retry  # noqa: E402

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

            render_attempts = max(0, int(source.get("render_attempts") or 0))
            attempted_prompt = scene_prompt
            if render_attempts:
                attempted_prompt = render_retry.retry_prompt(
                    scene_prompt,
                    title,
                    render_attempts,
                    note=clean(source.get("reviewer_note")) or None,
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
                "render_attempts": render_attempts,
                "source_ref": source.get("source_ref"),
                "reference_images": source.get("reference_images") or [],
                "render_gate_error": source.get("render_gate_error"),
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
        source.pop("render_gate_error", None)
        source.pop("render_gate_error_at", None)
        changed += 1

    if changed:
        write_queue(queue)
    return changed


def rejection_destination(
    destination: Path,
    entry: dict[str, Any],
    category: str,
) -> Path:
    attempt = int(entry.get("render_attempts") or 0) + 1
    seed = entry.get("resolved_seed")
    if seed is None:
        seed = entry.get("seed") or 0
    filename = f"{destination.stem}-attempt-{attempt}-seed-{seed}{destination.suffix}"
    rejected = destination.parent / "rejected" / "render" / category / filename
    rejected.parent.mkdir(parents=True, exist_ok=True)
    if rejected.exists():
        rejected.unlink()
    destination.replace(rejected)
    return rejected


def record_render_rejection(
    entry: dict[str, Any],
    mechanical: dict[str, Any],
    rejected: Path,
) -> str:
    """Record a *structural* render failure and decide whether to re-roll.

    Only the mechanical gate can land here — a blank frame, a wrong aspect
    ratio, an unreadable file. These are objective defects with no judgement in
    them, so a bounded automatic re-render is appropriate. Anything that is a
    real image goes to a human instead and never reaches this function.
    """

    next_attempt = int(entry.get("render_attempts") or 0) + 1
    max_attempts = max(1, render_retry.MAX_RENDER_ATTEMPTS)
    next_status = "pending" if next_attempt < max_attempts else "needs_review"

    used_seed = entry.get("resolved_seed")

    def mutate(source: dict[str, Any]) -> None:
        seed_for_history = used_seed if used_seed is not None else source.get("seed")
        history = source.get("render_failures")
        if not isinstance(history, list):
            history = []
        history.append(
            {
                "attempt": next_attempt,
                "seed": seed_for_history,
                "engine": entry.get("engine"),
                "art_image_id": entry.get("art_image_id"),
                "prompt_fingerprint": entry.get("prompt_fingerprint"),
                "gate": "mechanical",
                "reasons": mechanical.get("reasons") or [],
                "rejected_path": str(rejected.relative_to(ROOT)),
                "checked_at": now_iso(),
            }
        )
        source["render_failures"] = history
        source["render_attempts"] = next_attempt
        source["last_rejected_art_image_id"] = entry.get("art_image_id")
        source["last_render_seed"] = seed_for_history
        source["last_render_reasons"] = mechanical.get("reasons") or []
        source["status"] = next_status
        source.pop("art_image_id", None)
        source.pop("completed_at", None)
        # A definitive structural verdict just landed (whether from a fresh
        # submission or a recovered job) -- any stale "job N ..." breadcrumb
        # from a prior timeout no longer describes this entry's state and must
        # not survive into the next pass. Leaving it would make
        # referenced_job_id() keep pointing the next pass at the same
        # already-rejected job forever: recover_timed_out_job() would keep
        # "recovering" (re-fetching) the identical rejected image and re-running
        # the gate on it, never submitting a fresh, differently-seeded attempt
        # (see t-022 2026-08-01: mr-001/005/006 were stuck re-judging the same
        # rejected image across multiple hourly runs).
        source.pop("render_gate_error", None)
        source.pop("render_gate_error_at", None)
        if next_status == "pending" and bool(source.get("lock_seed")):
            # Locked concept: keep the deterministic seed rotation so a
            # reproducible render can still explore a few variants on retry.
            base = int(source.get("seed") or seed_for_history or 0)
            source["previous_seed"] = base
            source["seed"] = render_retry.next_retry_seed(base, next_attempt)
        # Unlocked concepts leave `seed` unset so the next attempt randomizes.

    mutate_queue_entry(entry, mutate)
    return next_status


def record_render_gate_error(entry: dict[str, Any], error: Exception, job_id: int | None = None) -> None:
    def mutate(source: dict[str, Any]) -> None:
        message = str(error)[:1000]
        # A fresh submission's ArtJob completed and rendered (job_id is set) but
        # validate_candidate() then failed -- e.g. PIL missing on the runner.
        # Without a "job N" reference in the stored error, referenced_job_id()
        # can never find it and every future pass is forced into a genuine
        # duplicate resubmission for an image that already rendered. Stamp the id
        # in (only if the message doesn't already carry one, e.g. from recovery).
        if job_id is not None and JOB_ID_PATTERN.search(message) is None:
            message = f"job {job_id}: {message}"[:1000]
        source["render_gate_error"] = message
        source["render_gate_error_at"] = now_iso()
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
        "renderAttempt": int(entry.get("render_attempts") or 0),
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
        "renderAttempt": int(entry.get("render_attempts") or 0),
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


class RecoveryAbandoned(RuntimeError):
    """Raised by recover_timed_out_job() only when it has positively determined
    the referenced ArtJob will never produce a usable render (failed, cancelled,
    or belongs to a different concept) -- as opposed to any other failure while
    checking/fetching/verifying it, where the job may still be perfectly good.
    The caller uses this distinction to decide whether to keep the "job N"
    reference for a future recovery pass or give up and let the next pass
    submit a fresh ArtJob."""


def referenced_job_id(entry: dict[str, Any]) -> int | None:
    """A prior run's timeout error names the ArtJob it was waiting on. Extract
    it so a later run can check whether that job actually finished instead of
    submitting a fresh (differently-seeded) duplicate."""
    match = JOB_ID_PATTERN.search(str(entry.get("render_gate_error") or ""))
    return int(match.group(1)) if match else None


def recover_timed_out_job(entry: dict[str, Any], job_id: int) -> tuple[bool, dict[str, Any]] | None:
    """Check a job a prior run gave up on waiting for. Unlocked entries pick a
    fresh random seed on every enqueue() call, so blindly resubmitting after a
    timeout creates a duplicate ArtJob against the render backend rather than
    reusing the one already in flight -- this recovers the original instead.

    Returns None if the job is still queued/running (leave it for next cycle).
    Raises RecoveryAbandoned if the job failed/was cancelled, or if it belongs
    to a different concept than expected -- these are the only outcomes where
    giving up on job_id and letting the next pass submit fresh is correct.
    Any other exception (network error checking status, missing local
    dependency while saving/verifying the fetched image, etc.) means job_id's
    own fate is still unknown and must not be treated the same way -- see the
    caller in main().
    """
    status, response = consumer.http_json("GET", f"{consumer.KR_BASE_URL}/api/art/queue/{job_id}")
    if status != 200 or not response or not response.get("success"):
        return None
    job = response.get("data", {}).get("job") or {}
    if job.get("status") in ("PENDING", "RUNNING"):
        return None
    if job.get("status") != "DONE":
        raise RecoveryAbandoned(f"job {job_id} {job.get('status')}: {job.get('error')}")

    art_image_id = job.get("artImageId")
    if not art_image_id:
        raise RecoveryAbandoned(f"job {job_id} DONE with no artImageId")

    attempt = (job.get("payload") or {}).get("attempt") or {}
    if attempt.get("conceptId") and str(attempt["conceptId"]) != str(entry["concept_id"]):
        raise RecoveryAbandoned(
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
    """Structural check only — is this a usable image file at all?

    This gate answers objective questions (blank frame? wrong aspect? not line
    art when line art was asked for?) using PIL, for free, with no credential.
    It deliberately does NOT judge likeness, composition, camp, or whether the
    render is any good: that is the reviewer's call, made in the ArtJob trainer
    panel, and a render that passes here goes straight to a human however rough
    it looks.
    """

    ok, reasons, info = art_quality.assess_file(destination, "color")
    if ok is None:
        raise RuntimeError(reasons[0] if reasons else "mechanical image gate unavailable")
    return bool(ok), {
        "gate": "mechanical",
        "reasons": [str(reason) for reason in reasons],
        "stats": info,
    }


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
                f"seed={seed_label} render_attempt={entry['render_attempts']}{refs}"
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
        submitted_job_id: int | None = None
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
                submitted_job_id = job_id
                suffix = " (existing matching attempt)" if deduplicated else ""
                print(
                    f"  queued ArtJob {job_id}{suffix} for "
                    f"{entry['set']}/{entry['concept_id']} color - waiting..."
                )
                job = consumer.wait_for_job(job_id, args.timeout)
                entry["art_image_id"] = int(job["artImageId"])
                image_b64 = consumer.fetch_image_b64(job["artImageId"])
                destination = save_result(entry, image_b64)

            accepted, mechanical = recovered if recovered is not None else validate_candidate(entry, destination)
            if not accepted:
                rejected = rejection_destination(destination, entry, "rejected")
                next_status = record_render_rejection(entry, mechanical, rejected)
                failures += 1
                print(
                    f"  RENDER-REJECT {entry['set']}/{entry['concept_id']}: "
                    f"{' ; '.join(mechanical.get('reasons') or [])} -> "
                    f"{rejected.relative_to(ROOT)} ({next_status})",
                    file=sys.stderr,
                )
                continue

            completed.append(entry)
            print(
                f"  LANDED {entry['set']}/{entry['concept_id']} -> "
                f"{destination.relative_to(ROOT)} "
                f"(ArtImage {entry.get('art_image_id') or 'existing'}) - awaiting human review"
            )
        except RecoveryAbandoned as error:
            # recover_timed_out_job() positively determined job {stuck_job_id}
            # will never produce a usable render (failed/cancelled/wrong
            # concept) -- safe (and correct) to drop the reference so the next
            # pass submits fresh instead of retrying a dead job forever.
            failures += 1
            record_render_gate_error(entry, error, job_id=stuck_job_id)
            print(f"  FAILED {entry['set']}/{entry['concept_id']}: {error}", file=sys.stderr)
        except Exception as error:  # noqa: BLE001
            failures += 1
            if destination.exists():
                try:
                    rejected = rejection_destination(destination, entry, "unverified")
                    print(f"    unverified candidate moved to {rejected.relative_to(ROOT)}", file=sys.stderr)
                except Exception:  # noqa: BLE001
                    pass
            if stuck_job_id is not None:
                # Anything other than RecoveryAbandoned during a recovery
                # attempt (network error checking/fetching job {stuck_job_id},
                # a missing local dependency like Pillow while saving the
                # fetched image, ...) means
                # job {stuck_job_id}'s own fate is still unknown -- it may well
                # be a completed, valid render. Overwriting render_gate_error
                # here would destroy the "job N" text a future recovery pass
                # parses via referenced_job_id(), forcing that future pass into
                # a genuine duplicate ArtJob submission for a render that may
                # already exist (see ai-art-academy/t-010's fauvism incident
                # and this task's own 2026-07-29 duplicate-submission incident
                # for what happens when that reference is lost). Leave the
                # entry's recoverable reference untouched instead.
                print(
                    f"  RECOVERY UNVERIFIED {entry['set']}/{entry['concept_id']}: {error} -- "
                    f"job {stuck_job_id} reference left intact for a future pass, "
                    "no duplicate submitted",
                    file=sys.stderr,
                )
            else:
                record_render_gate_error(entry, error, job_id=submitted_job_id)
                print(f"  FAILED {entry['set']}/{entry['concept_id']}: {error}", file=sys.stderr)

    marked = mark_done(completed)
    print(f"{len(todo) - failures}/{len(todo)} succeeded; {marked} queue entries marked done.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
