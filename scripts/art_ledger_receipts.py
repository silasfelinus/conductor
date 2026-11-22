"""Validate durable art receipts without confusing draft, queued and rendered states.

An auto_submit ledger evolves *after* it is authored: the art generation workflow
adds jobs and images while preserving prompt, seed and asset keys. Tests should
never assert that jobs/art fields are absent on a repository production ledger.
"""

from __future__ import annotations

from typing import Any


def receipt_problems(subject: dict[str, Any]) -> list[str]:
    """Return structural errors for one ledger subject, not subjective art QA."""
    problems: list[str] = []
    lane = subject.get("lane")
    jobs = subject.get("jobs")
    art = subject.get("art")

    if jobs is None and art is None:
        return []  # authored/requested only, not submitted

    if not isinstance(lane, str) or not lane:
        return ["missing lane for art receipt"]
    if not isinstance(jobs, dict) or set(jobs) != {lane}:
        return ["submitted receipt must have one matching ArtJob lane"]
    job_id = jobs.get(lane)
    if type(job_id) is not int or job_id <= 0:
        problems.append("ArtJob id must be a positive integer")
    if art is None:
        return problems  # accepted job, still awaiting status checkpoint
    if not isinstance(art, dict) or set(art) - {lane}:
        return problems + ["ArtImage status must use its ArtJob lane"]
    for status in art.values():
        if not isinstance(status, dict):
            problems.append("ArtImage status must be a mapping")
            continue
        state = status.get("status")
        if not isinstance(state, str) or not state:
            problems.append("ArtJob status must be recorded")
        image_id = status.get("art_image_id")
        if state == "DONE" and (type(image_id) is not int or image_id <= 0):
            problems.append("DONE requires a real ArtImage id")
        if image_id is not None and (type(image_id) is not int or image_id <= 0):
            problems.append("ArtImage id must be positive when present")
    return problems
