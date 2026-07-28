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

for _name in dir(_core):
    if not _name.startswith("__"):
        globals()[_name] = getattr(_core, _name)

_core_entry_to_job = _core.entry_to_job


def retry_seed_identity(entry: dict[str, Any]) -> dict[str, str]:
    return {
        "id": str(entry.get("id") or ""),
        "image_path": str(entry.get("image_path") or ""),
        "project": str(entry.get("project") or ""),
        "prompt": " ".join(str(entry.get("prompt") or "").split()),
        "engine": normalize_engine(entry.get("engine")),
    }


def stable_retry_seed(entry: dict[str, Any]) -> int:
    encoded = json.dumps(
        retry_seed_identity(entry),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return int.from_bytes(hashlib.sha256(encoded).digest()[:8], "big") % (SEED_MAX + 1)


def uses_specialized_attempt_recovery(entry: dict[str, Any]) -> bool:
    return (
        bool(entry.get("set"))
        and bool(entry.get("concept_id"))
        and "semantic_attempts" in entry
    )


def entry_to_job(entry: dict[str, Any]):
    normalized = dict(entry)
    engine = normalize_engine(normalized.get("engine"))
    seed = normalized.get("seed")
    seed_is_unset = not isinstance(seed, int) or isinstance(seed, bool) or seed < 0

    if (
        engine in COMFY_WORKFLOW_ENGINES
        and seed_is_unset
        and not uses_specialized_attempt_recovery(normalized)
    ):
        normalized["seed"] = stable_retry_seed(normalized)

    return _core_entry_to_job(normalized)


_core.entry_to_job = entry_to_job


if __name__ == "__main__":
    sys.exit(_core.main())
