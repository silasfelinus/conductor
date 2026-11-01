#!/usr/bin/env python3
"""Preserve Shifting Desks art submission provenance before queue retirement.

The queue may discard completed requests, but the authored ROUND-N ledger must
retain their ArtJob identity. This is *submission* evidence only: delivery and
editorial acceptance still require reconcile_delivery.py's independent checks.
"""

from __future__ import annotations

import os
import re
import tempfile
from pathlib import Path

import yaml

ART_DIR = Path(__file__).resolve().parents[1] / "projects" / "shifting-desks" / "art"
ROUND_ID = re.compile(r"^shifting-desks-r([1-9][0-9]*)-")
SUBJECT = re.compile(r"(?ms)^- key:.*?(?=^- key:|\Z)")


def _job_id(value):
    if isinstance(value, bool):
        return None
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None
    return parsed if parsed > 0 else None


def _target(value):
    result = str(value or "").strip().replace("\\", "/").lstrip("/")
    if result.startswith("kind_robots "):
        result = result[len("kind_robots "):]
    return result


def is_round_request(request):
    return (
        isinstance(request, dict)
        and ROUND_ID.match(str(request.get("id") or "")) is not None
        and str(request.get("target_repo") or request.get("repo") or "") == "silasfelinus/kind_robots"
    )


def preserve_completed_submissions(requests, *, art_dir=ART_DIR, before_write=None):
    """Return ids that MUST remain in the queue until their evidence is safe.

    A completed queue request is removable only after its matching round ledger
    contains the submitted ArtJob id. Missing subjects, mismatched destinations,
    invalid ids and conflicts remain held with status=done (never re-enqueued).
    Writes are minimal, comment-preserving and atomic, with a stale-read guard.
    """
    candidates = {}
    blocked = set()
    for request in requests:
        if not is_round_request(request):
            continue
        request_id = str(request["id"])
        if str(request.get("status") or "pending").lower() != "done":
            continue
        round_number = int(ROUND_ID.match(request_id).group(1))
        candidates.setdefault(round_number, []).append(request)

    for round_number, entries in candidates.items():
        path = Path(art_dir) / f"ROUND-{round_number}.yaml"
        ids = {str(entry["id"]) for entry in entries}
        if not path.exists():
            blocked.update(ids)
            continue
        original = path.read_text(encoding="utf-8")
        ledger = yaml.safe_load(original)
        rows = {}
        for row in ledger.get("subjects") or []:
            if not isinstance(row, dict):
                continue
            key = str(row.get("request_id") or "")
            if key in rows:
                raise ValueError(f"{path.name}: duplicate round request {key}")
            rows[key] = row
        replacements = {}
        for entry in entries:
            request_id = str(entry["id"])
            row = rows.get(request_id)
            job_id = _job_id(entry.get("last_art_job_id"))
            source_path = _target(entry.get("image_path"))
            if (
                row is None
                or not job_id
                or not source_path
                or _target(row.get("target_path")) != source_path
            ):
                blocked.add(request_id)
                continue
            recorded = _job_id(row.get("art_job_id"))
            if recorded is not None and recorded != job_id:
                blocked.add(request_id)
                continue
            if recorded is None:
                replacements[request_id] = job_id

        if not replacements:
            continue

        matched = set()

        def patch(match):
            block = match.group(0)
            identity = re.search(r"(?m)^  request_id: (\S+)\s*$", block)
            request_id = identity.group(1) if identity else None
            if request_id not in replacements:
                return block
            matched.add(request_id)
            field = re.compile(r"(?m)^(  art_job_id: ).*$")
            if len(field.findall(block)) != 1:
                raise ValueError(f"{path.name}: missing/duplicate art_job_id for {request_id}")
            return field.sub(lambda m: m.group(1) + str(replacements[request_id]), block)

        changed = SUBJECT.sub(patch, original)
        if matched != set(replacements):
            raise ValueError(f"{path.name}: subject blocks changed during reconciliation")
        yaml.safe_load(changed)
        if before_write:
            before_write(path)
        if path.read_text(encoding="utf-8") != original:
            raise RuntimeError(f"{path.name}: changed concurrently; refusing to overwrite")
        temp_name = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=path.parent, prefix=".round-evidence-",
                suffix=".yaml", delete=False
            ) as stream:
                stream.write(changed)
                temp_name = stream.name
            os.replace(temp_name, path)
        finally:
            if temp_name and os.path.exists(temp_name):
                os.unlink(temp_name)
    return blocked
