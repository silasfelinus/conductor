#!/usr/bin/env python3
"""art_request_key.py -- the stable Kind Robots ``requestKey`` for one Conductor art request.

WHY THIS EXISTS. Silas, 2026-11-11 PT: "A lot of our art generated seems to fail to get recorded,
so we keep finding art that was requested and made but not linked." Every Conductor submitter
writes the returned ArtJob id into a file on disk (a ledger cell's ``jobs:``, a request's
``last_art_job_id``) and the id only becomes durable when that file is committed. A thread agent
killed mid-session, or an Auto Art Generate run cancelled at its 150-minute timeout before
"Commit conductor results", loses it. The render still happens, nothing records it, and the next
run submits the same work again: Ruler Hooked's 211 requests rendered about 414 times over
2026-11-10/11 PT, none of them recorded on main.

A request key names the request itself, so Kind Robots (kind_robots#5031) can:
  * return the existing job instead of rendering again when a key is resubmitted, and
  * answer ``POST /api/art/queue/lookup`` with the job for each key, which
    ``scripts/reconcile_unrecorded_art.py`` uses to write lost ids back.

The key is deterministic from what is committed, so a session that never got to commit can still
be recovered by anyone holding main. It ends in a short hash of the fields that decide the render,
so editing a cell's prompt (and clearing its job id) is a new request rather than a dedup hit.
"""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any

KEY_MAX_LENGTH = 300
# Must match REQUEST_KEY_PATTERN in kind_robots server/utils/artRequestKey.ts.
_ALLOWED = re.compile(r"[^A-Za-z0-9_.:/#@+=-]")

# Fields of a ledger subject / lane that decide what renders. Curation fields added after a
# render (art, review, rejected, notes ...) are deliberately excluded so the key never drifts.
_SUBJECT_RENDER_PREFIXES = ("prompt", "negative", "source_", "last_image", "reference_", "mask_")
_SUBJECT_RENDER_FIELDS = ("size", "seed", "denoise", "loras", "duration", "loop", "entity_art")
_LANE_RENDER_FIELDS = (
    "engine", "checkpoint", "prompt", "prefix", "suffix", "steps", "cfg", "sampler", "guidance",
    "denoise", "loras", "seed", "fps", "output_format",
)
# A request's render-deciding fields. `force` and `render_nonce` are included on purpose: a row
# re-staged with force: true (or a bumped nonce) is a new request even when its prompt is unchanged.
_REQUEST_RENDER_FIELDS = (
    "prompt", "negative_prompt", "engine", "model", "size", "seed", "steps", "image_path",
    "force", "render_nonce",
)


def _digest(data: Any) -> str:
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:12]


def _clean(part: Any) -> str:
    return _ALLOWED.sub("-", str(part))


def _finish(key: str) -> str:
    """Trim an over-long key from the middle so the readable head and the hash survive."""
    if len(key) <= KEY_MAX_LENGTH:
        return key
    head, _, tail = key.rpartition("=")
    suffix = f"-{_digest(head)}={tail}"
    return head[: KEY_MAX_LENGTH - len(suffix)] + suffix


def ledger_cell_key(ledger_relpath: str, lane: dict, subject: dict) -> str:
    """``conductor:ledger:<path>#<subject>@<lane>=<hash>`` for one (subject, lane) cell."""
    render = {
        "lane": {field: lane.get(field) for field in _LANE_RENDER_FIELDS if lane.get(field) is not None},
        "subject": {
            field: value
            for field, value in subject.items()
            if value is not None
            and (field in _SUBJECT_RENDER_FIELDS or field.startswith(_SUBJECT_RENDER_PREFIXES))
        },
    }
    key = (
        f"conductor:ledger:{_clean(ledger_relpath)}#{_clean(subject.get('key'))}"
        f"@{_clean(lane.get('key'))}={_digest(render)}"
    )
    return _finish(key)


def request_key(entry: dict) -> str | None:
    """``conductor:request:<id>=<hash>`` for a projects/art-prompts.yaml request, or None without an id."""
    request_id = entry.get("id")
    if not request_id:
        return None
    render = {field: entry.get(field) for field in _REQUEST_RENDER_FIELDS if entry.get(field) not in (None, False)}
    return _finish(f"conductor:request:{_clean(request_id)}={_digest(render)}")
