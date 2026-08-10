#!/usr/bin/env python3
"""Retry-stable public entrypoint for the shared ArtJob queue consumer.

The implementation remains in ``consume_art_queue_core``. Generic project-art and
art-request entries without an explicit seed receive a deterministic seed derived
from their stable request identity. Re-running the same pending entry therefore
rebuilds the same ArtJob payload instead of silently submitting a differently
seeded duplicate after a local polling timeout.

The specialized coloring-book consumer intentionally explores fresh seeds and
carries its own timed-out-job recovery path, so its concept entries retain the
core implementation's randomized behavior.
"""

from __future__ import annotations

import hashlib
import json
import sys
from typing import Any

try:
    from scripts import consume_art_queue_core as _core
except ImportError:
    import consume_art_queue_core as _core

_core_entry_to_job = _core.entry_to_job
DAILY_DREAM_PRIORITY = 200
DAILY_DREAM_ENTITY_TYPES = {"dream", "character", "reward", "scenario", "bot"}


def retry_seed_identity(entry: dict[str, Any]) -> dict[str, str]:
    return {
        "id": str(entry.get("id") or ""),
        "image_path": str(entry.get("image_path") or ""),
        "project": str(entry.get("project") or ""),
        "prompt": " ".join(str(entry.get("prompt") or "").split()),
        "engine": _core.normalize_engine(entry.get("engine")),
    }


def stable_retry_seed(entry: dict[str, Any]) -> int:
    encoded = json.dumps(
        retry_seed_identity(entry),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return int.from_bytes(hashlib.sha256(encoded).digest()[:8], "big") % (_core.SEED_MAX + 1)


def uses_specialized_attempt_recovery(entry: dict[str, Any]) -> bool:
    # `semantic_attempts` is the pre-2026-08 spelling, still present on queue
    # entries written before the vision gate was removed. Accept either so an
    # un-migrated entry keeps its fresh-seed exploration policy instead of
    # silently falling back to a stable synthetic seed.
    return (
        bool(entry.get("set"))
        and bool(entry.get("concept_id"))
        and ("render_attempts" in entry or "semantic_attempts" in entry)
    )


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
    normalized = dict(entry)
    engine = _core.normalize_engine(normalized.get("engine"))
    seed = normalized.get("seed")
    seed_is_unset = not isinstance(seed, int) or isinstance(seed, bool) or seed < 0
    synthetic_seed = (
        engine in _core.COMFY_WORKFLOW_ENGINES
        and seed_is_unset
        and not uses_specialized_attempt_recovery(normalized)
    )

    if synthetic_seed:
        normalized["seed"] = stable_retry_seed(normalized)

    job = _core_entry_to_job(normalized)
    if _is_daily_dream(normalized):
        _enrich_daily_dream_job(normalized, job)
    else:
        _enrich_generic_destination(normalized, job)
    if synthetic_seed:
        payload = job.get("payload")
        if isinstance(payload, dict):
            payload.pop("seed", None)
    return job


_core.retry_seed_identity = retry_seed_identity
_core.stable_retry_seed = stable_retry_seed
_core.uses_specialized_attempt_recovery = uses_specialized_attempt_recovery
_core.entry_to_job = entry_to_job
_core.DAILY_DREAM_PRIORITY = DAILY_DREAM_PRIORITY
_core.DAILY_DREAM_ENTITY_TYPES = DAILY_DREAM_ENTITY_TYPES
sys.modules[__name__] = _core


if __name__ == "__main__":
    sys.exit(_core.main())
