#!/usr/bin/env python3
"""check_container_log_drift.py — surface Alexandria's container-log triage in the sweep.

The reading half of `ops/home-server/container_log_triage.py`, which runs daily
on Alexandria as an Unraid User Script and writes a small digest. This script
reads that digest and reports it like every other check_* in this repo, so the
findings land in the session-start sweep and the daily digest instead of in a
file nobody opens.

WHY THIS ALSO WATCHES THE CLOCK
    A watchdog cannot report its own absence -- the most expensive lesson in
    this repo. check_engine_heartbeat.py exists because healthcheck.ps1 stopped
    running at 2026-09-01 02:26:07 and simply never said so; its log just ends,
    ~37 hours before Silas noticed. A log-triage pipeline that dies silently is
    worse than none, because "no findings" and "not running" look identical
    from here.

    So a digest older than --stale-hours is a FINDING, not a pass. That is the
    difference between this and a plain report reader.

Exit codes follow the check_* convention:
    0  clean        -- digest is fresh and has nothing new, or the pipeline is
                       not set up yet (see below)
    1  findings     -- new/spiking signatures, or the digest has gone stale
    2  unresolved   -- the digest exists but cannot be read or parsed

A MISSING digest is exit 0, deliberately. Until Silas has the User Script
scheduled on Alexandria there is nothing to report, and a check that fails
loudly every session before its data source exists is how a sweep becomes
wallpaper -- the exact failure CLAUDE.md documents for the stale-project scan.
Once a digest has ever been seen, staleness takes over as the alarm.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_UNRESOLVED = 2

DEFAULT_DIGEST = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "ops", "home-server", "CONTAINER-LOG-DIGEST.json",
)
DEFAULT_STALE_HOURS = 48.0
MAX_SHOWN = 12


def load_digest(source, timeout=20.0):
    """Read the digest from a local path or an https URL. None if absent."""
    if source.startswith("http://") or source.startswith("https://"):
        request = urllib.request.Request(source, headers={"Accept": "application/json"})
        token = os.environ.get("CONTAINER_LOG_DIGEST_TOKEN", "").strip()
        if token:
            request.add_header("Authorization", "Bearer {}".format(token))
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8", "replace"))
        except urllib.error.HTTPError as error:
            if error.code == 404:
                return None
            raise RuntimeError("digest fetch failed: HTTP {}".format(error.code))
        except (urllib.error.URLError, OSError) as error:
            raise RuntimeError("digest fetch failed: {}".format(error))
        except ValueError as error:
            raise RuntimeError("digest is not valid JSON: {}".format(error))

    if not os.path.exists(source):
        return None
    try:
        with open(source, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (ValueError, OSError) as error:
        raise RuntimeError("digest at {} is unreadable: {}".format(source, error))


def parse_generated_at(digest):
    raw = (digest or {}).get("generated_at")
    if not isinstance(raw, str):
        return None
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def assess(digest, now, stale_hours):
    """Return (state, reason, findings) without printing anything."""
    generated = parse_generated_at(digest)
    if generated is None:
        return "unresolved", "digest has no readable generated_at timestamp", []

    age_hours = (now - generated).total_seconds() / 3600.0
    scan = digest.get("scan") or {}
    new = digest.get("new") or []
    spiking = digest.get("spiking") or []
    quiet = digest.get("quiet") or []

    if age_hours > stale_hours:
        return (
            "stale",
            "digest is {:.1f}h old (limit {:.0f}h) — the User Script on {} has "
            "probably stopped running".format(age_hours, stale_hours, digest.get("host", "the host")),
            [],
        )

    findings = (
        [dict(item, bucket="new") for item in new]
        + [dict(item, bucket="spiking") for item in spiking]
    )
    if findings:
        return (
            "findings",
            "{} new, {} spiking, {} went quiet across {} containers".format(
                len(new), len(spiking), len(quiet), scan.get("containers_scanned", "?")
            ),
            findings,
        )

    unreadable = scan.get("containers_failed") or []
    detail = "{} containers scanned, {} signatures known and steady".format(
        scan.get("containers_scanned", "?"), scan.get("signatures_total", "?")
    )
    if unreadable:
        detail += ", {} unreadable".format(len(unreadable))
    return "clean", detail, []


def render(state, reason, findings, digest):
    lines = []
    if state == "clean":
        lines.append("container log triage OK: {}".format(reason))
    elif state == "stale":
        lines.append("container log triage STALE: {}".format(reason))
    else:
        lines.append("container log triage FINDINGS: {}".format(reason))

    for item in findings[:MAX_SHOWN]:
        if item["bucket"] == "spiking":
            detail = "{}x vs {:.0f}/day baseline".format(item.get("count", 0), item.get("baseline") or 0)
        else:
            detail = "{}x".format(item.get("count", 0))
        lines.append(
            "  [{}] {} · {} · {} · {}".format(
                item.get("fingerprint", "?"), item.get("container", "?"),
                item.get("severity", "?"), item["bucket"], detail,
            )
        )
        sample = (item.get("sample") or "").strip()
        if sample:
            lines.append("      {}".format(sample))

    if len(findings) > MAX_SHOWN:
        lines.append("  ... and {} more (see the full digest)".format(len(findings) - MAX_SHOWN))

    quiet = (digest or {}).get("quiet") or []
    if quiet and state != "stale":
        lines.append(
            "  went quiet ({}): {} — either fixed, or the job that logged it "
            "stopped running".format(
                len(quiet), ", ".join(item.get("container", "?") for item in quiet[:5])
            )
        )
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--digest",
        default=os.environ.get("CONTAINER_LOG_DIGEST", DEFAULT_DIGEST),
        help="path or https URL of digest.json (default: the committed copy)",
    )
    parser.add_argument("--stale-hours", type=float, default=DEFAULT_STALE_HOURS)
    parser.add_argument("--json", action="store_true", help="emit the verdict as JSON")
    args = parser.parse_args(argv)

    now = datetime.now(timezone.utc)

    try:
        digest = load_digest(args.digest)
    except RuntimeError as error:
        if args.json:
            print(json.dumps({"state": "unresolved", "reason": str(error)}))
        else:
            print("container log triage UNRESOLVED: {}".format(error), file=sys.stderr)
        return EXIT_UNRESOLVED

    if digest is None:
        message = (
            "container log triage not configured yet: no digest at {}. "
            "Set up ops/home-server/container_log_triage.py as an Unraid User "
            "Script and publish its digest.json.".format(args.digest)
        )
        if args.json:
            print(json.dumps({"state": "not-configured", "reason": message}))
        else:
            print(message)
        return EXIT_CLEAN

    state, reason, findings = assess(digest, now, args.stale_hours)

    if args.json:
        print(json.dumps({
            "state": state,
            "reason": reason,
            "findings": findings[:MAX_SHOWN],
            "generated_at": digest.get("generated_at"),
            "host": digest.get("host"),
        }, indent=2, sort_keys=True))
    else:
        text = render(state, reason, findings, digest)
        print(text, file=sys.stderr if state in ("findings", "stale") else sys.stdout)

    if state == "unresolved":
        return EXIT_UNRESOLVED
    if state in ("findings", "stale"):
        return EXIT_FINDINGS
    return EXIT_CLEAN


if __name__ == "__main__":
    sys.exit(main())
