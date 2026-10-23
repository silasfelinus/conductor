#!/usr/bin/env python3
"""check_relay_version_drift.py -- is every live kr-relay running main's relay code?

The relay runs from a conductor checkout on the render box and only picks up a
merged fix after someone runs `git pull && pm2 restart kr-relay` there. Nothing
said when that had not happened. On 2026-10-23 Coat Dance ArtJob 42356 failed
in ComfyUI's PyAV loader with the defect conductor#6444 had fixed two days
earlier, because Silas-PC was still on the old worker; the only evidence was
the old wording of the error message.

kr-relay now reports agentVersion `conductor-relay-<fingerprint>@<commit>`,
where the fingerprint hashes the relay modules it loaded at startup
(ops/home-server/relay_fingerprint.py). This check computes the same hash from
this checkout (main, in a session) and compares it with every relay Kind Robots
has seen recently (GET /api/art/queue/relay-status).

Exit 0: every recent relay matches, or no relay has been seen recently (an
offline relay is check_engine_heartbeat's finding, not this one's).
Exit 1: a relay is stale (different fingerprint, or a pre-fingerprint build).
        The fix is on the box: `git pull && pm2 restart kr-relay`.
Exit 2: unresolved -- no KR_API_TOKEN, or relay-status unreachable.

Env: KR_BASE_URL, KR_API_TOKEN.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "ops" / "home-server"))

import relay_fingerprint  # noqa: E402

DEFAULT_RECENT_MINUTES = 30
FIX = "git pull && pm2 restart kr-relay"


def fetch_agents():
    """Relay agents from relay-status, or raise RuntimeError."""
    if not os.environ.get("KR_API_TOKEN", "").strip():
        raise RuntimeError("KR_API_TOKEN not set")
    sys.path.insert(0, str(ROOT / "scripts"))
    import consume_art_queue as consumer

    status, response = consumer.http_json(
        "GET", f"{consumer.KR_BASE_URL}/api/art/queue/relay-status", timeout=30
    )
    if status != 200 or not isinstance(response, dict) or not response.get("success"):
        raise RuntimeError(f"relay-status returned HTTP {status}")
    return (response.get("data") or {}).get("agents") or []


def parse_seen(value):
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None


def assess(agents, expected, now, recent_minutes=DEFAULT_RECENT_MINUTES):
    """(exit code, lines) for the relay agents against main's fingerprint."""
    cutoff = now - timedelta(minutes=recent_minutes)
    recent = [a for a in agents if (parse_seen(a.get("lastSeenAt")) or cutoff) > cutoff]
    if not recent:
        return 0, [f"check_relay_version_drift: no relay seen in {recent_minutes} min (main {expected})"]
    stale = []
    for agent in recent:
        version = agent.get("agentVersion") or ""
        if relay_fingerprint.parse_fingerprint(version) != expected:
            stale.append(agent)
    if not stale:
        names = ", ".join(str(a.get("agentId")) for a in recent)
        return 0, [f"check_relay_version_drift: {len(recent)} relay(s) on main's code {expected} ({names})"]
    lines = [
        f"check_relay_version_drift: {len(stale)} stale relay(s); main's relay code is {expected}"
    ]
    for agent in stale:
        version = agent.get("agentVersion") or "(none)"
        found = relay_fingerprint.parse_fingerprint(version)
        why = f"runs {found}" if found else "pre-fingerprint build"
        lines.append(f"  {agent.get('agentId')}: {why} [{version}] -- on the box: {FIX}")
    return 1, lines


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--recent-minutes", type=float, default=DEFAULT_RECENT_MINUTES)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    expected = relay_fingerprint.code_fingerprint()
    try:
        agents = fetch_agents()
    except Exception as error:  # noqa: BLE001 - any failure is "unresolved"
        print(f"check_relay_version_drift: unresolved -- {error}")
        return 2
    code, lines = assess(agents, expected, datetime.now(timezone.utc), args.recent_minutes)
    if args.json:
        print(json.dumps({"code": code, "expected": expected, "lines": lines, "agents": agents}))
    else:
        print("\n".join(lines))
    return code


if __name__ == "__main__":
    sys.exit(main())
