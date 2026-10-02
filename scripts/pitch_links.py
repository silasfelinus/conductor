#!/usr/bin/env python3
"""pitch_links.py -- signed one-click decision links for the digest's daily pitches.

Silas decides a pitch from the digest email: each pitch carries Approve and Pass buttons.
Each button is a link to Kind Robots' /api/conductor/pitch-decision, which shows a confirm
page (a GET never changes state, so mail scanners cannot decide anything) and, on confirm,
writes ``status:`` into pitches/<stem>.md through the same writer the project page uses.

The link is signed with HMAC-SHA256 over ``pitch-decision|<stem>|<vote>|<exp>`` using the
shared PITCH_LINK_SECRET, so it grants exactly one vote on one pitch until it expires. The
verifier is kind_robots server/utils/pitchDecisionLink.ts; tests/test_pitch_links.py and
kind_robots utils/scripts/verifyPitchDecision.test.ts assert the same fixed vector.

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
VOTES = {"approve": "approved", "pass": "rejected"}


def sign(secret: str, stem: str, vote: str, exp: int) -> str:
    message = f"pitch-decision|{stem}|{vote}|{exp}".encode()
    return hmac.new(secret.encode(), message, hashlib.sha256).hexdigest()


def decision_url(secret: str, stem: str, vote: str, exp: int, base_url: str = DEFAULT_BASE_URL) -> str:
    query = urlencode({"slug": stem, "vote": vote, "exp": exp, "sig": sign(secret, stem, vote, exp)})
    return f"{base_url.rstrip('/')}/api/conductor/pitch-decision?{query}"


def project_page_url(base_url: str | None = None) -> str:
    return f"{(base_url or os.environ.get('KR_BASE_URL') or DEFAULT_BASE_URL).rstrip('/')}/conductor"


def links_for(stem: str, now: float | None = None) -> dict[str, str] | None:
    """{'approve': url, 'pass': url} for a pitch file stem, or None when no secret is set."""
    secret = (os.environ.get("PITCH_LINK_SECRET") or "").strip()
    if not secret:
        return None
    base = os.environ.get("KR_BASE_URL") or DEFAULT_BASE_URL
    exp = int((time.time() if now is None else now)) + TTL_SECONDS
    return {label: decision_url(secret, stem, vote, exp, base) for label, vote in VOTES.items()}
