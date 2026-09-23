#!/usr/bin/env python3
"""
check_vendored_scanner_parity.py — Verify the home-server vendored LoRA/model
scanners are still byte-identical to their kind_robots app-source originals.

Kaizen from lora-ingestion/t-013 (Reviewer, 2026-09-22): the vendored copies in
ops/home-server/lora-catalog/ (scan_loras.py, scan_models.py,
import_catalog.py) had silently drifted from their kind_robots originals at
scripts/lora-catalog/ -- the vendored scan_loras.py was missing the Civitai
tag category classifier entirely, with nothing catching the gap until a
downstream symptom (garbled preview classification) surfaced it days later.

PROVENANCE.md (ops/home-server/lora-catalog/PROVENANCE.md) is explicit that
these are meant to be a "straight file copy" -- both scripts are pure Python
stdlib with no kind_robots imports, so there is no reason for the two copies
to differ at all. That makes the check simple and strict: fetch each
original from kind_robots' default branch via the GitHub Contents API and
compare it byte-for-byte against the local vendored copy. Any difference,
however small, is drift -- there is no "acceptable" partial sync for a file
that is supposed to be an exact copy.

Read-only: never edits or re-syncs either copy. Fixing drift means running
the `cp` commands PROVENANCE.md documents and committing the result -- this
script only detects and reports.

Requires: GITHUB_TOKEN (or GH_TOKEN) env var to read kind_robots' contents API
without public rate limits; kind_robots is a private repo, so a token is
required for this to return anything -- without one, the check cannot run and
exits 2 (unresolved, not clean), same convention as check_project_scaffold_drift.py
without KR_API_TOKEN.

Usage:
  python scripts/check_vendored_scanner_parity.py
  python scripts/check_vendored_scanner_parity.py --json
  python scripts/check_vendored_scanner_parity.py --ref <branch-or-sha>

Exit codes:
  0 = clean -- every vendored file matches its kind_robots original byte-for-byte
  1 = drift found -- at least one vendored file differs from its original
  2 = could not verify -- missing token, network failure, or a vendored/
      original file could not be read; a clean read here would be a false
      "all good"
"""
from __future__ import annotations

import argparse
import base64
import difflib
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VENDOR_DIR = ROOT / "ops" / "home-server" / "lora-catalog"

KIND_ROBOTS_REPO = "silasfelinus/kind_robots"
KIND_ROBOTS_SOURCE_DIR = "scripts/lora-catalog"
DEFAULT_REF = "main"

# Vendored filename -> path relative to KIND_ROBOTS_SOURCE_DIR in kind_robots.
# All three currently sit at the same basename in both repos (see
# PROVENANCE.md), but this stays a mapping rather than a bare list in case
# that ever changes.
TRACKED_FILES = {
    "scan_loras.py": "scan_loras.py",
    "scan_models.py": "scan_models.py",
    "import_catalog.py": "import_catalog.py",
}


def github_token() -> str | None:
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")


def fetch_kind_robots_file(relative_path: str, ref: str, token: str | None) -> tuple[bytes | None, str | None]:
    """(content_bytes, error). error is None on success."""
    path = f"{KIND_ROBOTS_SOURCE_DIR}/{relative_path}"
    url = (
        f"https://api.github.com/repos/{KIND_ROBOTS_REPO}/contents/{path}"
        f"?ref={urllib.parse.quote(ref)}"
    )
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "conductor-check-vendored-scanner-parity/1.0",
    }
    if token:
        headers["Authorization"] = f"token {token}"
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            body = json.loads(response.read())
    except urllib.error.HTTPError as exc:
        return None, f"HTTP {exc.code} fetching {path}"
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return None, f"network error fetching {path}: {exc}"

    encoding = body.get("encoding")
    content = body.get("content")
    if encoding != "base64" or content is None:
        return None, f"unexpected contents API response shape for {path}"
    try:
        return base64.b64decode(content), None
    except (ValueError, TypeError) as exc:
        return None, f"failed to decode base64 content for {path}: {exc}"


def diff_snippet(original: bytes, vendored: bytes, label: str, max_lines: int = 12) -> str:
    try:
        original_lines = original.decode("utf-8").splitlines(keepends=True)
        vendored_lines = vendored.decode("utf-8").splitlines(keepends=True)
    except UnicodeDecodeError:
        return "  (binary difference, no text diff available)"
    diff = list(
        difflib.unified_diff(
            vendored_lines,
            original_lines,
            fromfile=f"vendored/{label}",
            tofile=f"kind_robots/{label}",
            n=1,
        )
    )
    if not diff:
        return "  (content differs but no line-level diff -- likely a line-ending difference)"
    shown = diff[:max_lines]
    text = "".join(shown)
    if len(diff) > max_lines:
        text += f"  ... ({len(diff) - max_lines} more diff line(s))\n"
    return text


def scan(
    ref: str = DEFAULT_REF,
    token: str | None = None,
    vendor_dir: Path | None = None,
    fetcher=None,
) -> dict[str, Any]:
    vendor_dir = vendor_dir or VENDOR_DIR
    fetcher = fetcher or fetch_kind_robots_file
    token = token if token is not None else github_token()
    findings: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []

    if not token:
        return {
            "findings": findings,
            "unresolved": [
                {
                    "file": name,
                    "detail": "GITHUB_TOKEN/GH_TOKEN not set -- kind_robots is private, cannot fetch originals",
                }
                for name in TRACKED_FILES
            ],
            "checked": [],
        }

    checked: list[str] = []
    for vendored_name, source_relative in TRACKED_FILES.items():
        vendored_path = vendor_dir / vendored_name
        if not vendored_path.exists():
            findings.append(
                {
                    "file": vendored_name,
                    "shape": "vendor-file-missing",
                    "detail": f"{vendored_path} does not exist locally",
                }
            )
            continue

        vendored_bytes = vendored_path.read_bytes()
        original_bytes, error = fetcher(source_relative, ref, token)
        if error is not None:
            unresolved.append({"file": vendored_name, "detail": error})
            continue

        checked.append(vendored_name)
        if vendored_bytes != original_bytes:
            findings.append(
                {
                    "file": vendored_name,
                    "shape": "content-drift",
                    "vendored_bytes": len(vendored_bytes),
                    "original_bytes": len(original_bytes),
                    "detail": (
                        f"ops/home-server/lora-catalog/{vendored_name} no longer matches "
                        f"kind_robots@{ref}:{KIND_ROBOTS_SOURCE_DIR}/{source_relative}"
                    ),
                    "diff": diff_snippet(original_bytes, vendored_bytes, vendored_name),
                }
            )

    return {"findings": findings, "unresolved": unresolved, "checked": checked}


def render(result: dict[str, Any], ref: str) -> str:
    findings = result["findings"]
    unresolved = result["unresolved"]
    lines = []

    if unresolved and not findings:
        lines.append(f"Could not verify vendored scanner parity against kind_robots@{ref}:")
        for item in unresolved:
            lines.append(f"  - {item['file']}: {item['detail']}")
        lines.append(
            "\nUnresolved, not clean -- set GITHUB_TOKEN/GH_TOKEN and re-run."
        )
        return "\n".join(lines)

    if not findings:
        checked = ", ".join(result["checked"]) or "(none)"
        suffix = ""
        if unresolved:
            suffix = "\n\nAlso could not verify: " + "; ".join(
                f"{u['file']} ({u['detail']})" for u in unresolved
            )
        return (
            f"No vendored scanner drift found -- {checked} in ops/home-server/lora-catalog/ "
            f"all match kind_robots@{ref}:{KIND_ROBOTS_SOURCE_DIR}/ byte-for-byte.{suffix}"
        )

    lines.append(f"Vendored scanner drift ({len(findings)}) against kind_robots@{ref}:")
    for f in findings:
        lines.append(f"  - {f['file']}: {f['detail']}")
        if f["shape"] == "content-drift":
            lines.append(f["diff"].rstrip("\n"))
    lines.append(
        "\nRe-sync per ops/home-server/lora-catalog/PROVENANCE.md: cp the kind_robots "
        "originals over the vendored copies, update the \"Re-synced\" note, and commit both."
    )
    if unresolved:
        lines.append(
            "\nAlso could not verify: " + "; ".join(f"{u['file']} ({u['detail']})" for u in unresolved)
        )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument(
        "--ref",
        default=DEFAULT_REF,
        help=f"kind_robots ref to compare against (default: {DEFAULT_REF})",
    )
    args = parser.parse_args()

    result = scan(ref=args.ref)

    if args.json:
        print(json.dumps({**result, "ref": args.ref}, indent=2))
    else:
        print(render(result, args.ref))

    if result["findings"]:
        sys.exit(1)
    if result["unresolved"]:
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
