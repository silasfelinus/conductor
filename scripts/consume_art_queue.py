#!/usr/bin/env python3
"""Public entrypoint for the shared ArtJob queue consumer.

The implementation remains in ``consume_art_queue_core``. An entry that does not
name its own seed gets a fresh random one, every submission, on every lane --
``_core.resolve_seed`` picks it. An explicit non-negative seed is still
authoritative, so a caller that wants to reproduce a specific render says so.

This used to be a deterministic seed derived from the entry's request identity
(SHA-256 over id/image_path/project/prompt/engine), so re-running the same
pending entry rebuilt a byte-identical payload. That was for deduplication:
ArtJob.attemptFingerprint is a hash of the whole payload including the baked
workflow seed (kind_robots server/utils/artJobProvenance.ts), so a stable seed
made the enqueue endpoint's dedupe fire on a repeat submission.

Silas, 2026-08-30: *"we do not want that infrastructure choice to set
deterministic seeds. I see no reason to do it that way. If we resubmit the same
prompt, we should always get a random seed."* The cost of the old behavior was
that resubmitting a prompt could only ever reproduce the same picture -- there
was no way to re-roll a render you did not like without editing the prompt,
which is backwards for an art pipeline. Deduplication does not depend on this
anyway: consume_art_requests.has_unresolved_submission (conductor/t-133, with
t-136's release condition) blocks a re-submission while the row's existing
ArtJob is still in flight, and it keys on the recorded job id rather than on
payload bytes, so it is unaffected by the seed.
"""

from __future__ import annotations

import sys
from typing import Any

try:
    from scripts import consume_art_queue_core as _core
except ImportError:
    import consume_art_queue_core as _core

_core_entry_to_job = _core.entry_to_job
DAILY_DREAM_PRIORITY = 200
DAILY_DREAM_ENTITY_TYPES = {"dream", "character", "reward", "scenario", "bot"}


def _is_daily_dream(entry: dict[str, Any]) -> bool:
    return str(entry.get("source") or "").strip().lower() == "dream-cycle"


def _positive_int(value: Any) -> int | None:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None
    return parsed if parsed > 0 else None


def _enrich_generic_destination(entry: dict[str, Any], job: dict[str, Any]) -> None:
    """Keep an explicit Conductor destination on ordinary durable ArtJobs.

    Missing-image, dashboard-tab, tutorial, and other generic queue entries already
    carry ``target_repo``/``image_path``. The core renderer historically dropped
    those fields while converting the YAML entry to an ArtJob, so the relay could
    render an ArtImage but had no final media destination to deliver it to.
    """
    payload = job.get("payload")
    if not isinstance(payload, dict):
        return

    request_id = str(entry.get("id") or "").strip()
    target_repo = str(entry.get("target_repo") or "").strip()
    image_path = str(entry.get("image_path") or "").strip()
    source_url = str(entry.get("source_url") or "").strip()
    page_url = str(entry.get("page_url") or "").strip()
    label = str(entry.get("label") or "").strip()

    if not target_repo:
        return

    if request_id:
        job["idempotencyKey"] = request_id
    project_slug = str(entry.get("project_slug") or "").strip()
    if project_slug and not job.get("projectSlug"):
        job["projectSlug"] = project_slug

    payload["targetRepo"] = target_repo
    if image_path:
        payload["imagePath"] = image_path
    if source_url:
        payload["sourceUrl"] = source_url
    if page_url:
        payload["pageUrl"] = page_url
    payload["conductorRequest"] = {
        "id": request_id or None,
        "source": str(entry.get("source") or "").strip() or None,
        "label": label or None,
        "targetRepo": target_repo,
        "imagePath": image_path or None,
        "sourceUrl": source_url or None,
        "pageUrl": page_url or None,
    }


def _enrich_daily_dream_job(entry: dict[str, Any], job: dict[str, Any]) -> None:
    """Preserve canonical Daily Dream destination, provenance, and attach target.

    ``build_dream_records.py`` writes the stable destination plus entity
    type/id/field on each request. Keeping those fields inside the durable
    ArtJob means:
      * the relay and Kind Robots file resolver can honor the declared path,
      * Kind Robots can attach the completed ArtImage in the same transaction
        that marks the job DONE, and
      * the stable request id can suppress duplicate enqueues after a timeout.
    """
    payload = job.get("payload")
    if not isinstance(payload, dict):
        return

    request_id = str(entry.get("id") or "").strip()
    target_repo = str(entry.get("target_repo") or "").strip()
    image_path = str(entry.get("image_path") or "").strip()
    source_url = str(entry.get("source_url") or "").strip()
    page_url = str(entry.get("page_url") or "").strip()
    label = str(entry.get("label") or "").strip()
    entity_type = str(entry.get("entity_type") or "").strip().lower()
    entity_id = _positive_int(entry.get("entity_id"))
    entity_field = str(entry.get("entity_field") or "imagePath").strip() or "imagePath"

    job["priority"] = DAILY_DREAM_PRIORITY
    job["projectSlug"] = "dream-cycle"
    if request_id:
        job["idempotencyKey"] = request_id

    payload["collection"] = "dream-cycle"
    if target_repo:
        payload["targetRepo"] = target_repo
    if image_path:
        payload["imagePath"] = image_path
    if source_url:
        payload["sourceUrl"] = source_url
    if page_url:
        payload["pageUrl"] = page_url
    payload["conductorRequest"] = {
        "id": request_id or None,
        "source": "dream-cycle",
        "label": label or None,
        "targetRepo": target_repo or None,
        "imagePath": image_path or None,
        "sourceUrl": source_url or None,
        "pageUrl": page_url or None,
    }

    if entity_type in DAILY_DREAM_ENTITY_TYPES and entity_id:
        payload["entityArt"] = {
            "entityType": entity_type,
            "entityId": entity_id,
            "field": entity_field,
            "preserveOriginal": True,
            "mode": "recreate",
        }


def entry_to_job(entry: dict[str, Any]):
    # No seed rewriting here. An entry that names a seed keeps it; one that does
    # not gets a fresh random seed from _core.resolve_seed, which is what every
    # lane now wants (see the module docstring).
    normalized = dict(entry)
    job = _core_entry_to_job(normalized)
    if _is_daily_dream(normalized):
        _enrich_daily_dream_job(normalized, job)
    else:
        _enrich_generic_destination(normalized, job)
    return job


_core.entry_to_job = entry_to_job
_core.DAILY_DREAM_PRIORITY = DAILY_DREAM_PRIORITY
_core.DAILY_DREAM_ENTITY_TYPES = DAILY_DREAM_ENTITY_TYPES
sys.modules[__name__] = _core


if __name__ == "__main__":
    sys.exit(_core.main())
