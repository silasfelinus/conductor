"""Shared Space Couch ledger status and image-provenance contracts.

ArtJob states mirror Kind Robots' ArtJobStatus enum in prisma/schema.prisma.
ACCEPTED and REJECTED are curator verdicts, not ArtJob states. In particular,
DONE proves only that a render exists, never that its image has been accepted.
"""

from __future__ import annotations

ART_JOB_STATUSES = frozenset({"PENDING", "RUNNING", "DONE", "FAILED", "CANCELLED"})
CURATOR_STATUSES = frozenset({"ACCEPTED", "REJECTED"})
LEDGER_LOOKUP_STATUSES = frozenset({"ERROR"})
ART_LEDGER_STATUSES = ART_JOB_STATUSES | CURATOR_STATUSES | LEDGER_LOOKUP_STATUSES

IMAGE_REQUIRED_STATUSES = frozenset({"DONE", "ACCEPTED"})
IMAGE_FORBIDDEN_STATUSES = frozenset(
    {"PENDING", "RUNNING", "FAILED", "CANCELLED", "ERROR"}
)


def positive_id(value: object) -> bool:
    """Exclude booleans, which Python otherwise considers integer IDs."""
    return type(value) is int and value > 0


def provenance_errors(subject: dict, lane: str) -> list[str]:
    """Validate one recorded art lane without confusing rendering with approval."""
    art = (subject.get("art") or {}).get(lane)
    if not isinstance(art, dict):
        return [f"{lane}: missing art record"]

    errors = []
    job_id = (subject.get("jobs") or {}).get(lane)
    if not positive_id(job_id):
        errors.append(f"{lane}: missing valid ArtJob ID")

    status = art.get("status")
    if status not in ART_LEDGER_STATUSES:
        errors.append(f"{lane}: unknown status {status!r}")

    image_id = art.get("art_image_id")
    if image_id is not None and not positive_id(image_id):
        errors.append(f"{lane}: invalid ArtImage ID")
    if status in IMAGE_REQUIRED_STATUSES and image_id is None:
        errors.append(f"{lane}: {status} requires an ArtImage ID")
    if status in IMAGE_FORBIDDEN_STATUSES and image_id is not None:
        errors.append(f"{lane}: {status} cannot claim an ArtImage")

    # Rejected paintings may retain the original ArtImage for visual evidence.
    return errors


def is_visually_accepted(subject: dict, lane: str) -> bool:
    """A DONE render is not an approved painting."""
    art = (subject.get("art") or {}).get(lane) or {}
    return art.get("status") == "ACCEPTED" and not provenance_errors(subject, lane)
