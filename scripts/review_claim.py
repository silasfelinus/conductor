#!/usr/bin/env python3
"""
review_claim.py — shared rules for lightweight, best-effort PR review-claim markers.

Fixes the rotation-collision gap from conductor/t-092 (see root TALKBACK.md,
2026-07-28 "four-way rotation collision"): `claim_task.py` already prevents two
sessions from both *implementing* the same roadmap task, but there was no
equivalent for *reviewing* -- nothing stopped N concurrent sessions from all
picking up the same open, green PR and racing to review/merge/close it out.
That collision produced real duplicate work (three redundant conductor PRs
opened for the same close-outs) even though git's non-fast-forward rejection
still prevented any actual data loss.

This module is deliberately transport-agnostic: it does not call the GitHub
API itself. Different sessions reach GitHub through different channels (this
sandbox's `mcp__github__*` tools, another session's `gh` CLI, or a direct
REST call) and direct `api.github.com` calls 403 from at least one known
sandbox shape (see scripts/select_role.py's docstring) -- so the network
call is left to the caller, using whatever transport that session already
has working. What's shared here is the marker format, the freshness rule,
and the pure decision logic, so every session applies the identical
convention regardless of how it fetches/posts comments.

Protocol (see AGENTS.md "Review-claim markers" for the full write-up):
    1. Before starting a review pass on an open PR, fetch its issue/PR
       comments (any transport) and call find_active_claim(comments).
    2. If it returns a claim from a DIFFERENT session, skip this PR --
       another session is already reviewing it. Move on to the next item.
    3. Otherwise, post a comment with format_marker(my_session) *before*
       starting the substantive review, then proceed.
    4. Advisory only -- a missed check is wasted duplicate work, not a
       safety violation. Git's own conflict rejection remains the real
       backstop against data loss, same as every other rotation-collision
       case in AGENTS.md.

Usage (helper for step 3 / manual testing of step 2):
    python scripts/review_claim.py format <session-id>
    python scripts/review_claim.py check <comments.json> [--ttl-minutes 20] [--exclude-session <id>]

`check` reads a JSON array of {"body": str, "created_at": ISO8601 str} objects
(the shape GitHub's REST/MCP comment listings already return) from a file or
stdin ("-") and prints the active claim (if any) as JSON, or "null".
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from roadmap_claims import parse_timestamp  # noqa: E402

# How long a review-claim marker stays active before a later session may treat
# the PR as unclaimed again. Short on purpose -- unlike roadmap task claims
# (which can span a whole implementation cycle), a review pass is a single
# short burst of activity within one session.
REVIEW_CLAIM_TTL_MINUTES = 20

MARKER_PREFIX = "REVIEWING:"
# "REVIEWING: <session> at <ISO8601>" -- session is any non-whitespace token,
# same collision-resistant id shape claim_task.py already asks sessions to use.
MARKER_RE = re.compile(r"^REVIEWING:\s*(\S+)\s+at\s+(\S+)\s*$", re.MULTILINE)


def format_marker(session: str, *, now: datetime | None = None) -> str:
    """The exact comment body a session should post before reviewing a PR."""
    now = now or datetime.now(timezone.utc)
    stamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"{MARKER_PREFIX} {session} at {stamp}"


def parse_marker(body: str) -> tuple[str, datetime] | None:
    """Extract (session, posted_at) from a comment body, or None if it isn't a marker."""
    if not isinstance(body, str):
        return None
    match = MARKER_RE.search(body.strip())
    if not match:
        return None
    session, stamp = match.group(1), match.group(2)
    posted_at = parse_timestamp(stamp)
    if posted_at is None:
        return None
    return session, posted_at


def marker_is_fresh(posted_at: datetime, *, now: datetime | None = None, ttl_minutes: int = REVIEW_CLAIM_TTL_MINUTES) -> bool:
    now = now or datetime.now(timezone.utc)
    age_minutes = (now - posted_at).total_seconds() / 60.0
    return 0 <= age_minutes <= ttl_minutes


def find_active_claim(
    comments: list[dict[str, Any]],
    *,
    now: datetime | None = None,
    ttl_minutes: int = REVIEW_CLAIM_TTL_MINUTES,
    exclude_session: str | None = None,
) -> dict[str, Any] | None:
    """Return the freshest still-active review-claim marker, or None.

    `comments` is a list of {"body": ..., "created_at": ...} dicts (extra keys
    ignored, so raw GitHub API/MCP comment objects can be passed directly).
    Markers from `exclude_session` (a session checking its own prior marker)
    are ignored -- pass this session's own id to avoid a false "already
    claimed by someone else" against a marker it posted itself.
    """
    now = now or datetime.now(timezone.utc)
    best: dict[str, Any] | None = None
    for comment in comments:
        parsed = parse_marker(comment.get("body", ""))
        if parsed is None:
            continue
        session, posted_at = parsed
        if exclude_session is not None and session == exclude_session:
            continue
        if not marker_is_fresh(posted_at, now=now, ttl_minutes=ttl_minutes):
            continue
        if best is None or posted_at > best["posted_at"]:
            best = {"session": session, "posted_at": posted_at, "comment": comment}
    return best


def _claim_to_json(claim: dict[str, Any] | None) -> str:
    if claim is None:
        return "null"
    return json.dumps(
        {"session": claim["session"], "posted_at": claim["posted_at"].isoformat()},
        indent=2,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    fmt = sub.add_parser("format", help="Print the marker comment body to post")
    fmt.add_argument("session", help="This session's collision-resistant id")

    chk = sub.add_parser("check", help="Evaluate a fetched comment list for an active claim")
    chk.add_argument("comments_file", help="Path to a JSON comment array, or - for stdin")
    chk.add_argument("--ttl-minutes", type=int, default=REVIEW_CLAIM_TTL_MINUTES)
    chk.add_argument("--exclude-session", default=None)

    args = parser.parse_args()

    if args.command == "format":
        print(format_marker(args.session))
        return 0

    if args.command == "check":
        raw = sys.stdin.read() if args.comments_file == "-" else Path(args.comments_file).read_text()
        comments = json.loads(raw)
        claim = find_active_claim(comments, ttl_minutes=args.ttl_minutes, exclude_session=args.exclude_session)
        print(_claim_to_json(claim))
        return 1 if claim is not None else 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
