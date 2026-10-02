#!/usr/bin/env python3
"""Run every CLAUDE.md startup reconciliation check in one call, compactly.

Token essentialization (2026-09-30). CLAUDE.md's startup sweep used to name
fourteen scripts, each run as its own tool call with its full output pasted
into the session's context -- 20KB+ of mostly "all clear" text before a
session had done any work, repeated by every hourly Conductor Agent Routine
run. This runs them concurrently, prints ONE line per check, and shows output
only for checks that need a look (non-zero exit), capped per check. Rerun the
individual script for the full output, or read docs/sweep-checks.md for what
a check means and how to fix what it flags.

Exit status: 0 when every check exited 0, 1 when any flagged (1/3), 2 when
any was unresolved (exit 2, timeout, or crash) and none flagged. Advisory --
same as the checks themselves, never a gate.

Usage:
  python scripts/session_sweep.py                  # all checks
  python scripts/session_sweep.py --max-lines 60   # show more of each flagged check
  python scripts/session_sweep.py --only audit_human_gates,check_pr_merged_drift
  python scripts/session_sweep.py --skip-network   # offline: skip checks that need tokens/API
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (name, argv after `python`, needs network/token, always_show)
# always_show: output is itself part of the startup report (the gate list, the
# Tzaddik docket), so it is shown even on exit 0 -- still capped by --max-lines.
CHECKS: list[tuple[str, list[str], bool, bool]] = [
    ("check_pr_merged_drift", ["scripts/check_pr_merged_drift.py"], True, False),
    ("audit_human_gates", ["scripts/audit_human_gates.py"], False, True),
    ("check_gate_legitimacy", ["scripts/check_gate_legitimacy.py", "--live"], True, False),
    ("check_project_scaffold_drift", ["scripts/check_project_scaffold_drift.py"], True, False),
    ("check_live_facet_coverage", ["scripts/check_live_facet_coverage.py"], True, False),
    ("check_milestone_status_drift", ["scripts/check_milestone_status_drift.py"], False, False),
    ("check_container_log_drift", ["scripts/check_container_log_drift.py"], False, False),
    ("check_roadmap_note_size", ["scripts/check_roadmap_note_size.py"], False, False),
    ("check_facet_prompt_subjects", ["scripts/check_facet_prompt_subjects.py"], True, False),
    ("check_priority_queue_starvation", ["scripts/check_priority_queue_starvation.py"], False, False),
    ("check_vendored_scanner_parity", ["scripts/check_vendored_scanner_parity.py"], True, False),
    ("check_daily_commitment_staleness", ["scripts/check_daily_commitment_staleness.py"], False, False),
    ("check_recurring_claim_drift", ["scripts/check_recurring_claim_drift.py"], False, False),
    ("check_recurring_churn", ["scripts/check_recurring_churn.py"], False, False),
    ("issue_bridge", ["scripts/sync_github_issues.py", "--check"], True, False),
    ("dream_docket", ["scripts/build_dream_proposal.py", "--check", "--fetch"], True, True),
    ("tzaddik_review", ["scripts/tzaddik_review.py", "--check"], False, True),
]

# Always report the projection headroom line (CLAUDE.md: report it every session).
HEADROOM = ("projection_headroom", ["scripts/check_roadmap_note_size.py", "--payload-only"], False, True)


def run(check, timeout: float) -> dict:
    name, argv, _, always_show = check
    started = time.monotonic()
    try:
        proc = subprocess.run(
            [sys.executable, *argv],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        code = proc.returncode
        out = (proc.stdout + ("\n" + proc.stderr if proc.stderr.strip() and code != 0 else "")).strip()
    except subprocess.TimeoutExpired:
        code, out = None, f"timed out after {timeout:.0f}s -- rerun `python {' '.join(argv)}` directly"
    return {
        "name": name,
        "argv": argv,
        "code": code,
        "out": out,
        "always_show": always_show,
        "secs": time.monotonic() - started,
    }


def first_line(text: str) -> str:
    for line in text.splitlines():
        if line.strip():
            return line.strip()[:160]
    return "(no output)"


def label(code) -> str:
    if code == 0:
        return "ok"
    if code in (1, 3):
        return f"FLAG({code})"
    if code is None:
        return "TIMEOUT"
    return f"UNRESOLVED({code})"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--max-lines", type=int, default=12, help="lines of output shown per flagged check")
    parser.add_argument("--timeout", type=float, default=90.0, help="per-check timeout in seconds")
    parser.add_argument("--only", default="", help="comma-separated check names to run")
    parser.add_argument("--skip-network", action="store_true", help="skip checks that need a token/API")
    args = parser.parse_args()

    checks = [HEADROOM, *CHECKS]
    if args.only:
        wanted = {n.strip() for n in args.only.split(",") if n.strip()}
        checks = [c for c in checks if c[0] in wanted]
    if args.skip_network:
        checks = [c for c in checks if not c[2]]

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda c: run(c, args.timeout), checks))

    print("=== SESSION SWEEP (details: docs/sweep-checks.md) ===")
    for r in results:
        print(f"{label(r['code']):<14} {r['name']:<34} {first_line(r['out'])}")

    for r in results:
        if r["code"] == 0 and not r["always_show"]:
            continue
        if r["name"] == "projection_headroom":
            continue  # its one line is already in the table
        lines = r["out"].splitlines()
        # Line 1 is already in the table; show the rest.
        body = lines[1:] if lines else []
        if not body:
            continue
        print(f"\n--- {r['name']} [{label(r['code'])}] ---")
        print("\n".join(body[: args.max_lines]))
        if len(body) > args.max_lines:
            print(f"... {len(body) - args.max_lines} more lines: python {' '.join(r['argv'])}")

    codes = [r["code"] for r in results]
    if any(c in (1, 3) for c in codes):
        return 1
    if any(c not in (0, 1, 3) for c in codes):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
