#!/usr/bin/env python3
"""Build SECURITY-REPORT.md from safe local checks and optional GitHub API data."""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from typing import Any

REPO = "silasfelinus/conductor"
GITHUB_API = "https://api.github.com"
DEFAULT_OUTPUT = pathlib.Path("SECURITY-REPORT.md")
EXCLUDED_DIRS = {".git", "node_modules", ".nuxt", ".output", "dist", "build"}
EXCLUDED_FILES = {"SECURITY-REPORT.md"}
TEXT_SUFFIXES = {".env", ".example", ".json", ".js", ".md", ".mjs", ".py", ".sh", ".ts", ".tsx", ".vue", ".yaml", ".yml"}
CREDENTIAL_MARKERS = ("api_key", "apikey", "password=", "private key", "token=")


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run_check(command: list[str]) -> tuple[bool, str]:
    try:
        completed = subprocess.run(command, check=False, capture_output=True, text=True, timeout=120)
    except FileNotFoundError as exc:
        return False, f"command unavailable: {exc.filename}"
    except subprocess.TimeoutExpired:
        return False, "timed out after 120 seconds"
    output = "\n".join(part.strip() for part in (completed.stdout, completed.stderr) if part.strip())
    return completed.returncode == 0, output or "no output"


def compile_python_scripts() -> tuple[bool, str]:
    scripts = sorted(pathlib.Path("scripts").glob("*.py"))
    if not scripts:
        return True, "no scripts/*.py files found"
    return run_check([sys.executable, "-m", "py_compile", *(str(path) for path in scripts)])


def run_authz_regression() -> tuple[bool, str]:
    test_file = pathlib.Path("tests/test_authz_regression.py")
    if not test_file.exists():
        return False, "tests/test_authz_regression.py is missing"
    return run_check([sys.executable, "-m", "pytest", str(test_file)])


def path_is_scannable(path: pathlib.Path) -> bool:
    if path.name in EXCLUDED_FILES:
        return False
    if any(part in EXCLUDED_DIRS for part in path.parts):
        return False
    return path.suffix in TEXT_SUFFIXES or path.name.endswith(".env.example")


def scan_credential_markers() -> list[str]:
    findings: list[str] = []
    for path in sorted(pathlib.Path(".").rglob("*")):
        if not path.is_file() or not path_is_scannable(path):
            continue
        try:
            for idx, line in enumerate(path.read_text(errors="ignore").splitlines(), start=1):
                lower = line.lower()
                if any(marker in lower for marker in CREDENTIAL_MARKERS) and "example" not in lower and "placeholder" not in lower:
                    findings.append(f"{path}:{idx}: credential-like marker requires review")
        except OSError:
            continue
    return findings


def gh_get(path: str, api_token: str) -> Any | None:
    req = urllib.request.Request(
        f"{GITHUB_API}{path}",
        headers={
            "Authorization": "Bearer " + api_token,
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
        print(f"WARNING: GitHub API request failed for {path}: {exc}", file=sys.stderr)
        return None


def fetch_recent_security_runs(api_token: str) -> list[dict[str, Any]]:
    data = gh_get(f"/repos/{REPO}/actions/workflows/security-audit.yml/runs?per_page=5", api_token)
    if not isinstance(data, dict):
        return []
    runs = data.get("workflow_runs", [])
    return runs if isinstance(runs, list) else []


def fetch_open_security_prs(api_token: str) -> list[dict[str, Any]]:
    pulls = gh_get(f"/repos/{REPO}/pulls?state=open&base=main&per_page=100", api_token)
    if not isinstance(pulls, list):
        return []
    matches: list[dict[str, Any]] = []
    for pr in pulls:
        if not isinstance(pr, dict):
            continue
        haystack = f"{pr.get('title', '')} {pr.get('head', {}).get('ref', '')} {pr.get('body', '')}".lower()
        if any(term in haystack for term in ("security", "authz", "audit", "credential")):
            matches.append(pr)
    return matches


def status_label(ok: bool) -> str:
    return "PASS" if ok else "FAIL"


def first_line(text: str) -> str:
    return text.splitlines()[0][:160] if text else "no output"


def build_report(api_token: str) -> str:
    generated = now_iso()
    py_ok, py_output = compile_python_scripts()
    authz_ok, authz_output = run_authz_regression()
    credential_findings = scan_credential_markers()
    credential_ok = not credential_findings
    recent_runs = fetch_recent_security_runs(api_token) if api_token else []
    security_prs = fetch_open_security_prs(api_token) if api_token else []

    lines: list[str] = [
        "# SECURITY-REPORT.md — audit snapshot",
        "",
        f"Generated: {generated}",
        f"Repo: {REPO}",
        "",
    ]
    if not api_token:
        lines.append("> ⚠ GITHUB_TOKEN not set — GitHub Actions and open PR data omitted; local checks still ran.")
        lines.append("")

    lines.extend([
        "## Pass/fail summary",
        "",
        "| Check | Status | Detail |",
        "|---|---|---|",
        f"| Python syntax | {status_label(py_ok)} | {first_line(py_output)} |",
        f"| Authz regression fixture | {status_label(authz_ok)} | {first_line(authz_output)} |",
        f"| Credential-marker smoke scan | {status_label(credential_ok)} | {len(credential_findings)} warning(s) |",
        "",
        "## Latest Security Audit workflow runs",
        "",
    ])

    if not recent_runs:
        lines.append("_No workflow run data available in this environment._")
    else:
        lines.append("| Run | Status | Conclusion | Event | Updated |")
        lines.append("|---|---|---|---|---|")
        for run in recent_runs:
            url = run.get("html_url", "")
            run_id = run.get("id", "?")
            link = f"[#{run_id}]({url})" if url else f"#{run_id}"
            lines.append(f"| {link} | {run.get('status', '?')} | {run.get('conclusion', '?')} | {run.get('event', '?')} | {str(run.get('updated_at', ''))[:19]} |")
    lines.append("")

    lines.extend(["## Dependency vulnerabilities", ""])
    lines.append("No dependency advisory details are available locally. Check the latest Security Audit dependency-audit job when workflow data is present.")
    lines.append("")

    lines.extend(["## Failed authz boundaries", ""])
    if authz_ok:
        lines.append("_No fixture authz failures detected by tests/test_authz_regression.py._")
    else:
        lines.append("- Authz fixture regression failed. First line:")
        lines.append(f"  - `{first_line(authz_output)}`")
    lines.append("")

    lines.extend(["## Stale config / credential-marker warnings", ""])
    if credential_ok:
        lines.append("_No credential-like markers found by the local smoke scan._")
    else:
        for finding in credential_findings[:25]:
            lines.append(f"- {finding}")
        if len(credential_findings) > 25:
            lines.append(f"- ...and {len(credential_findings) - 25} more warning(s).")
    lines.append("")

    lines.extend(["## Open security-related PRs", ""])
    if not security_prs:
        lines.append("_No open PRs matched security/authz/audit keywords, or PR data was unavailable._")
    else:
        lines.append("| PR | Branch | Updated |")
        lines.append("|---|---|---|")
        for pr in security_prs:
            url = pr.get("html_url", "")
            num = pr.get("number", "?")
            title = str(pr.get("title", "untitled"))[:80]
            link = f"[#{num}]({url})" if url else f"#{num}"
            lines.append(f"| {link} {title} | `{pr.get('head', {}).get('ref', '?')}` | {str(pr.get('updated_at', ''))[:19]} |")
    lines.append("")

    lines.extend(["## Maintenance queue", ""])
    queue: list[str] = []
    if not py_ok:
        queue.append("Fix Python syntax failures before merging further automation changes.")
    if not authz_ok:
        queue.append("Inspect and fix the authz regression failure; keep this ahead of feature work.")
    if not credential_ok:
        queue.append("Review credential-marker warnings and replace any real material with placeholders.")
    if not api_token:
        queue.append("Run this report in GitHub Actions with GITHUB_TOKEN so workflow and PR sections populate.")
    if not queue:
        queue.append("No immediate maintenance item detected by this report run.")
    for item in queue:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("---")
    lines.append(f"_Auto-generated by `scripts/build_security_report.py` at {generated}_")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build SECURITY-REPORT.md")
    parser.add_argument("--dry-run", action="store_true", help="Print report; do not write file")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Output file path")
    args = parser.parse_args()

    report = build_report(os.environ.get("GITHUB_TOKEN", ""))
    if args.dry_run:
        print(report)
        return

    output = pathlib.Path(args.output)
    output.write_text(report)
    print(f"Written: {output}", file=sys.stderr)


if __name__ == "__main__":
    main()
