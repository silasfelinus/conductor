#!/usr/bin/env python3
"""pitch_links.py -- signed one-click decision links for the digest's daily pitches.

Silas decides pitches from the digest email, and every pitch button opens ONE page: Kind
Robots' /api/conductor/pitch-inbox, which lists every undecided pitch with Approve, Approve
with changes, Pass and Decide later, and applies them all on a single save (a GET never
changes state, so mail scanners cannot decide anything). The button a pitch carries only
preselects that pitch's choice (``pick=<stem>:<choice>``, a UI default, not part of the
signature). Approved pitches get ``status: approved`` in pitches/<stem>.md; approve-with-changes
also appends a "Silas's modifications" section that ``daily_pitches.py --approved`` prints.

The inbox link is signed with HMAC-SHA256 over ``pitch-inbox|<exp>`` using the shared
PITCH_LINK_SECRET. The older per-pitch signature (``pitch-decision|<stem>|<vote>|<exp>``,
``decision_url``) is still verified by /api/conductor/pitch-decision so emails already in
inboxes keep working. The verifier is kind_robots server/utils/pitchDecisionLink.ts;
tests/test_pitch_links.py and kind_robots utils/scripts/verifyPitchDecision.test.ts assert
the same fixed vectors.

With no PITCH_LINK_SECRET the digest falls back to a plain link to the signed-in project
page (kindrobots.org/conductor), so the email still works while the secret is unset.
"""
from __future__ import annotations

import hashlib
import hmac
import os
import time
from urllib.parse import urlencode

DEFAULT_BASE_URL = "https://kindrobots.org"
TTL_SECONDS = 14 * 24 * 3600
VOTES = {"approve": "approved", "pass": "rejected"}  # legacy per-pitch links
CHOICES = {"approve": "approve", "changes": "approve-changes", "pass": "pass"}


def sign(secret: str, stem: str, vote: str, exp: int) -> str:
    message = f"pitch-decision|{stem}|{vote}|{exp}".encode()
    return hmac.new(secret.encode(), message, hashlib.sha256).hexdigest()


def decision_url(secret: str, stem: str, vote: str, exp: int, base_url: str = DEFAULT_BASE_URL) -> str:
    query = urlencode({"slug": stem, "vote": vote, "exp": exp, "sig": sign(secret, stem, vote, exp)})
    return f"{base_url.rstrip('/')}/api/conductor/pitch-decision?{query}"


def project_page_url(base_url: str | None = None) -> str:
    return f"{(base_url or os.environ.get('KR_BASE_URL') or DEFAULT_BASE_URL).rstrip('/')}/conductor"


def sign_inbox(secret: str, exp: int) -> str:
    return hmac.new(secret.encode(), f"pitch-inbox|{exp}".encode(), hashlib.sha256).hexdigest()


def inbox_url(secret: str, exp: int, base_url: str = DEFAULT_BASE_URL, picks: dict[str, str] | None = None) -> str:
    """The single inbox page; ``picks`` ({stem: choice}) only preselects radio buttons."""
    query = urlencode(
        [("exp", exp), ("sig", sign_inbox(secret, exp))] + [("pick", f"{stem}:{choice}") for stem, choice in (picks or {}).items()]
    )
    return f"{base_url.rstrip('/')}/api/conductor/pitch-inbox?{query}"


def _secret() -> str:
    return (os.environ.get("PITCH_LINK_SECRET") or "").strip()


def _base_and_expiry(now: float | None) -> tuple[str, int]:
    base = os.environ.get("KR_BASE_URL") or DEFAULT_BASE_URL
    return base, int((time.time() if now is None else now)) + TTL_SECONDS


def inbox_link(now: float | None = None) -> str | None:
    """The unpreselected inbox link, or None when no secret is set."""
    if not _secret():
        return None
    base, exp = _base_and_expiry(now)
    return inbox_url(_secret(), exp, base)


def links_for(stem: str, now: float | None = None) -> dict[str, str] | None:
    """{'approve', 'changes', 'pass'} inbox URLs preselecting that choice for a pitch stem."""
    if not _secret():
        return None
    base, exp = _base_and_expiry(now)
    return {label: inbox_url(_secret(), exp, base, {stem: choice}) for label, choice in CHOICES.items()}
