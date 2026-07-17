#!/usr/bin/env python3
"""
recheck_egress_blocks.py — probe one or more hosts through the sandbox's egress
allowlist and append a stamped result to EGRESS-BLOCKERS.md.

Replaces the copy-pasted "RECHECKED <date>: still a fresh connect_rejected/403"
prose paragraphs that had independently accumulated across ai-art-academy/t-008,
t-013, digital-storefront's Stripe task, and art-generator-connect's Civitai/HF
task (see conductor/t-052) — one append-only ledger, one line per recheck,
greppable from any task instead of hand-written each time.

Usage:
    python scripts/recheck_egress_blocks.py metmuseum.org upload.wikimedia.org \\
        --task ai-art-academy/t-008
    python scripts/recheck_egress_blocks.py api.stripe.com --no-append   # dry run

A connection-level failure (refused, reset, timeout, DNS failure) is treated as
"blocked" — the signature of a sandbox egress-allowlist rejection. An HTTP
response carrying a `cf-mitigated` header (Cloudflare's bot-management signal,
e.g. `cf-mitigated: challenge`) is treated as "bot-challenged" — the connection
reached the remote site, but the remote site is interposing a JS/managed
challenge rather than serving the resource, which silently defeats a fetch just
like a genuine block would (see EGRESS-BLOCKERS.md's www.artic.edu IIIF entry,
ai-art-academy/t-013). Any other actual HTTP response, even an error one (403,
404, ...), is treated as "reachable", since the connection itself succeeded and
no challenge signal was present; that's an ordinary remote-site response, not
an egress block.

This script never changes a roadmap task's status — it only records what it
observed. The calling agent still applies normal Failure-triage rules.
"""

from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
LEDGER_FILE = REPO_ROOT / "EGRESS-BLOCKERS.md"
LOG_MARKER = "## Log"


def _cf_mitigated(headers) -> str | None:
    """Return the `cf-mitigated` header value if present, else None."""
    if headers is None:
        return None
    return headers.get("cf-mitigated")


def probe_host(host: str, timeout: float = 10.0) -> tuple[str, str]:
    """Return (status, detail) for a single host.

    status is one of "blocked", "bot-challenged", "reachable".
    """
    url = host if host.startswith(("http://", "https://")) else f"https://{host}"
    req = urllib.request.Request(
        url, method="HEAD", headers={"User-Agent": "conductor-egress-recheck/1.0"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            cf = _cf_mitigated(resp.headers)
            if cf:
                return "bot-challenged", f"bot-challenged (HTTP {resp.status}, cf-mitigated: {cf})"
            return "reachable", f"reachable (HTTP {resp.status})"
    except urllib.error.HTTPError as e:
        cf = _cf_mitigated(e.headers)
        if cf:
            return "bot-challenged", f"bot-challenged (HTTP {e.code}, cf-mitigated: {cf})"
        return "reachable", f"reachable (HTTP {e.code})"
    except Exception as e:  # noqa: BLE001 - log the failure shape verbatim
        return "blocked", f"blocked ({e.__class__.__name__}: {e})"


def append_entry(
    host: str,
    status: str,
    detail: str,
    task: str | None,
    ledger_path: Path = LEDGER_FILE,
) -> None:
    if not ledger_path.exists():
        raise SystemExit(f"{ledger_path} not found — was it removed?")

    text = ledger_path.read_text(encoding="utf-8")
    if LOG_MARKER not in text:
        raise SystemExit(f"{ledger_path} missing a '{LOG_MARKER}' section marker")

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    task_part = f" | {task}" if task else ""
    entry = f"\n## {ts} | {host} | {status}{task_part}\n{detail}\n"

    ledger_path.write_text(text.rstrip("\n") + "\n" + entry, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("hosts", nargs="+", help="Hostname(s) to probe, e.g. metmuseum.org")
    parser.add_argument(
        "--task", help="project/task-id this recheck relates to, e.g. ai-art-academy/t-008"
    )
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument(
        "--no-append",
        action="store_true",
        help="Print results without writing to EGRESS-BLOCKERS.md (dry run)",
    )
    args = parser.parse_args(argv)

    markers = {"blocked": "\U0001f6ab", "bot-challenged": "⚠️", "reachable": "✓"}
    for host in args.hosts:
        status, detail = probe_host(host, timeout=args.timeout)
        marker = markers.get(status, "?")
        print(f"{marker} {host}: {detail}")
        if not args.no_append:
            append_entry(host, status, detail, args.task, ledger_path=LEDGER_FILE)

    return 0


if __name__ == "__main__":
    sys.exit(main())
