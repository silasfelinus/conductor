#!/usr/bin/env python3
"""
resync_vendored_scanner.py — automate vendored LoRA/model scanner re-syncs.

The single-file mode fetches a current kind_robots scanner original, writes it over the
home-server vendored copy, and appends a dated provenance note. The parity-report mode
consumes JSON emitted by check_vendored_scanner_parity.py --json and applies every drift
finding in one invocation.

It does not commit or push anything. Review the diff and run the parity checker afterward.

Usage:
  python scripts/resync_vendored_scanner.py --file scan_loras.py
  python scripts/resync_vendored_scanner.py --file scan_loras.py --reason "adds the XYZ field"
  python scripts/resync_vendored_scanner.py --from-parity-report parity.json
  python scripts/resync_vendored_scanner.py --from-parity-report parity.json --dry-run

Requires: GITHUB_TOKEN (or GH_TOKEN) env var — kind_robots is private.

Exit codes:
  0 = success
  2 = invalid input, unresolved parity findings, or a fetch failure
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.check_vendored_scanner_parity import (
    TRACKED_FILES,
    VENDOR_DIR,
    fetch_kind_robots_file,
    github_token,
)

PROVENANCE_PATH = ROOT / "ops" / "home-server" / "lora-catalog" / "PROVENANCE.md"


def resync(
    file_name: str,
    ref: str = "main",
    reason: str | None = None,
    token: str | None = None,
    vendor_dir: Path | None = None,
    provenance_path: Path | None = None,
    fetcher=None,
    dry_run: bool = False,
    today: str | None = None,
) -> dict[str, Any]:
    vendor_dir = vendor_dir or VENDOR_DIR
    provenance_path = provenance_path or PROVENANCE_PATH
    fetcher = fetcher or fetch_kind_robots_file
    token = token if token is not None else github_token()

    if file_name not in TRACKED_FILES:
        return {
            "ok": False,
            "error": f"unknown file {file_name!r}; tracked files are {sorted(TRACKED_FILES)}",
        }

    if not token:
        return {
            "ok": False,
            "error": "GITHUB_TOKEN/GH_TOKEN not set -- kind_robots is private, cannot fetch the original",
        }

    source_relative = TRACKED_FILES[file_name]
    original_bytes, error = fetcher(source_relative, ref, token)
    if error is not None:
        return {"ok": False, "error": error}

    vendored_path = vendor_dir / file_name
    current_bytes = vendored_path.read_bytes() if vendored_path.exists() else None
    if current_bytes == original_bytes:
        return {"ok": True, "changed": False, "file": file_name}

    note_date = today or dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    reason_text = f" for {reason}" if reason else ""
    note_line = f"\nRe-synced {note_date} (`{file_name}`){reason_text}. Source: kind_robots@{ref}.\n"

    if not dry_run:
        vendor_dir.mkdir(parents=True, exist_ok=True)
        vendored_path.write_bytes(original_bytes)
        with provenance_path.open("a", encoding="utf-8") as fh:
            fh.write(note_line)

    return {
        "ok": True,
        "changed": True,
        "file": file_name,
        "vendored_path": str(vendored_path),
        "provenance_path": str(provenance_path),
        "note": note_line.strip(),
        "dry_run": dry_run,
    }


def files_from_parity_report(report: dict[str, Any]) -> tuple[list[str] | None, str | None]:
    """Return the unique tracked drift files from checker --json output."""
    unresolved = report.get("unresolved")
    if not isinstance(unresolved, list):
        return None, "parity report is missing an unresolved list"
    if unresolved:
        names = ", ".join(str(item.get("file", "unknown")) for item in unresolved if isinstance(item, dict))
        return None, f"parity report contains unresolved checks: {names or 'unknown'}"

    findings = report.get("findings")
    if not isinstance(findings, list):
        return None, "parity report is missing a findings list"

    files: list[str] = []
    for finding in findings:
        if not isinstance(finding, dict) or not isinstance(finding.get("file"), str):
            return None, "parity report contains a finding without a file"
        file_name = finding["file"]
        if file_name not in TRACKED_FILES:
            return None, f"parity report names untracked file {file_name!r}"
        if file_name not in files:
            files.append(file_name)
    return files, None


def resync_from_parity_report(
    report: dict[str, Any],
    *,
    ref: str | None = None,
    reason: str | None = None,
    token: str | None = None,
    vendor_dir: Path | None = None,
    provenance_path: Path | None = None,
    fetcher=None,
    dry_run: bool = False,
    today: str | None = None,
) -> dict[str, Any]:
    files, error = files_from_parity_report(report)
    if error is not None:
        return {"ok": False, "error": error, "results": []}

    report_ref = report.get("ref", "main")
    effective_ref = ref or (report_ref if isinstance(report_ref, str) else "main")
    results: list[dict[str, Any]] = []
    for file_name in files or []:
        result = resync(
            file_name=file_name,
            ref=effective_ref,
            reason=reason or "parity report drift",
            token=token,
            vendor_dir=vendor_dir,
            provenance_path=provenance_path,
            fetcher=fetcher,
            dry_run=dry_run,
            today=today,
        )
        results.append(result)
        if not result["ok"]:
            return {"ok": False, "error": result["error"], "results": results}

    return {"ok": True, "ref": effective_ref, "results": results}


def load_parity_report(path: str) -> tuple[dict[str, Any] | None, str | None]:
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, f"could not read parity report {path!r}: {exc}"
    if not isinstance(payload, dict):
        return None, "parity report must contain a JSON object"
    return payload, None


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--file", choices=sorted(TRACKED_FILES), help="vendored file to re-sync")
    source.add_argument(
        "--from-parity-report",
        metavar="PATH",
        help="JSON output from check_vendored_scanner_parity.py --json",
    )
    parser.add_argument("--reason", default=None, help="short reason recorded in the PROVENANCE.md note")
    parser.add_argument("--ref", default=None, help="kind_robots ref (default: report ref, otherwise main)")
    parser.add_argument(
        "--dry-run", action="store_true", help="report what would change without writing anything"
    )
    args = parser.parse_args()

    if args.from_parity_report:
        report, error = load_parity_report(args.from_parity_report)
        if error is not None:
            print(f"ERROR: {error}")
            sys.exit(2)
        result = resync_from_parity_report(
            report,
            ref=args.ref,
            reason=args.reason,
            dry_run=args.dry_run,
        )
        if not result["ok"]:
            print(f"ERROR: {result['error']}")
            sys.exit(2)
        changed = [item["file"] for item in result["results"] if item.get("changed")]
        verb = "Would re-sync" if args.dry_run else "Re-synced"
        if changed:
            print(f"{verb} {', '.join(changed)} from kind_robots@{result['ref']}.")
        else:
            print(f"Parity report has no drift requiring a re-sync against kind_robots@{result['ref']}.")
        sys.exit(0)

    ref = args.ref or "main"
    result = resync(file_name=args.file, ref=ref, reason=args.reason, dry_run=args.dry_run)
    if not result["ok"]:
        print(f"ERROR: {result['error']}")
        sys.exit(2)
    if not result["changed"]:
        print(f"{args.file} already matches kind_robots@{ref} -- nothing to do.")
        sys.exit(0)
    verb = "Would re-sync" if args.dry_run else "Re-synced"
    print(f"{verb} {args.file} from kind_robots@{ref}.")
    if not args.dry_run:
        print(f"Updated {result['vendored_path']} and appended a note to {result['provenance_path']}.")
        print(f"Note: {result['note']}")
    sys.exit(0)


if __name__ == "__main__":
    main()
