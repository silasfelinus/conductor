#!/usr/bin/env python3
"""art_queue_health.py — record why the art queue failed, so an agent fixes it.

WHY THIS EXISTS

Auto Art Generate's consume steps are `continue-on-error`, so the job is green
whether it rendered everything or nothing. On 2026-10-07 it went 0/24 on project
art and 0/4 on requests -- every one an HTTP 422 from kind_robots' prompt
contract -- and twelve projects sat at `status: pending` for days behind a green
check. select_role.py could not see it either: it deliberately does not watch
auto-art-generate.yml, whose conclusion is mostly benign `cancelled` noise.

So the workflow tees each art step's output to a log, and `record` turns the
`FAILED ...` lines into ops/art-queue-health.yaml, committed with the run's
other results. `check` (session_sweep.py) and select_role.py's `art-medic` role
read that file, so the next Conductor session picks the failures up as work.

    python scripts/art_queue_health.py record \\
        --log project-art=/tmp/consume.log --log requests=/tmp/requests.log \\
        --log kr-failed-jobs=/tmp/repair.log
    python scripts/art_queue_health.py check          # exit 1 = art-medic work
    python scripts/art_queue_health.py check --json

A source whose log is missing or empty (its step was skipped because the render
box or the API was down) keeps its previous entries rather than reading as
"all clear". The file only changes when the set of failures changes: each entry
carries the date it was first seen, never a per-run timestamp, so a stable
failure does not commit on every run.

Exit codes (check): 0 nothing actionable, 1 actionable failures listed.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
HEALTH_FILE = ROOT / "ops" / "art-queue-health.yaml"
SOURCES = ("project-art", "requests", "kr-failed-jobs")
DEFAULT_PERSIST_DAYS = 2
DETAIL_LIMIT = 240

# Never heal on their own: a rejected prompt is rejected every run, an ArtImage
# with no data 404s every run, and a FAILED ArtJob the repair step has no known
# repair for stays FAILED. Anything else (a timeout, a transient HTTP error)
# only becomes work once it has persisted DEFAULT_PERSIST_DAYS.
ALWAYS_ACTIONABLE = {"contract-rejected", "adopt-failed", "kr-job-failed"}

HEADER = """\
# art-queue-health.yaml -- written by scripts/art_queue_health.py record at the
# end of every Auto Art Generate run. Do not hand-edit: fix the cause (see
# docs/agents/roles/art-medic.md) and the next run drops the entry.
"""

FAILED_ADOPT = re.compile(r"^\s*FAILED to adopt (\S+): (.*)$")
FAILED = re.compile(r"^\s*FAILED (\S+): (.*)$")
UNHANDLED_HEADER = re.compile(r"^\s*Unhandled FAILED ArtJobs \(\d+\):")
UNHANDLED_JOB = re.compile(r"^\s*ArtJob (\d+): (engine=.*)$")
RULE = re.compile(r"\[([a-z0-9][a-z0-9-]*)\]")


def _detail(text: str) -> str:
    text = " ".join(text.split())
    return text if len(text) <= DETAIL_LIMIT else text[: DETAIL_LIMIT - 1] + "…"


def _classify(error: str) -> str:
    if "prompt contract" in error:
        return "contract-rejected"
    if "timed out" in error:
        return "timeout"
    return "error"


def parse_log(text: str, source: str) -> list[dict]:
    """Failures named in one art step's output, in order of appearance."""
    failures: list[dict] = []
    in_unhandled = False
    last: dict | None = None
    for line in text.splitlines():
        if UNHANDLED_HEADER.match(line):
            in_unhandled, last = True, None
            continue
        job = UNHANDLED_JOB.match(line) if in_unhandled else None
        if job:
            last = {"target": f"ArtJob {job.group(1)}", "kind": "kr-job-failed", "detail": job.group(2)}
            failures.append(last)
            continue
        in_unhandled = in_unhandled and line.startswith((" ", "\t"))
        match = FAILED_ADOPT.match(line)
        if match:
            last = {"target": match.group(1), "kind": "adopt-failed", "detail": match.group(2)}
            failures.append(last)
            continue
        match = FAILED.match(line)
        if match:
            error = match.group(2)
            last = {"target": match.group(1), "kind": _classify(error), "detail": error}
            failures.append(last)
            continue
        # A contract rejection names its rule(s) on the following indented line.
        if last is not None and line.startswith((" ", "\t")) and RULE.search(line):
            last["detail"] = f"{last['detail']} {line.strip()}"
            continue
        last = None

    for failure in failures:
        rules = sorted(set(RULE.findall(failure["detail"])))
        if rules and failure["kind"] in ("contract-rejected", "kr-job-failed"):
            failure["rules"] = rules
        failure["detail"] = _detail(failure["detail"])
        failure["source"] = source
    return failures


def _key(entry: dict) -> tuple[str, str, str]:
    return (entry.get("source", ""), entry.get("target", ""), entry.get("kind", ""))


def merge(previous: list[dict], fresh: dict[str, list[dict]], today: str) -> list[dict]:
    """Replace each freshly logged source's entries; keep the rest; carry first_seen."""
    seen = {_key(entry): entry.get("first_seen", today) for entry in previous}
    merged = [entry for entry in previous if entry.get("source") not in fresh]
    for failures in fresh.values():
        unique: dict[tuple[str, str, str], dict] = {}
        for failure in failures:
            unique[_key(failure)] = failure
        for key, failure in unique.items():
            entry = {
                "source": failure["source"],
                "target": failure["target"],
                "kind": failure["kind"],
            }
            if failure.get("rules"):
                entry["rules"] = failure["rules"]
            entry["detail"] = failure["detail"]
            entry["first_seen"] = seen.get(key, today)
            merged.append(entry)
    return sorted(merged, key=lambda e: (SOURCES.index(e["source"]) if e["source"] in SOURCES else 99, e["target"], e["kind"]))


def load(path: Path | None = None) -> list[dict]:
    path = path or HEALTH_FILE
    if not path.exists():
        return []
    data = yaml.safe_load(path.read_text()) or {}
    failures = data.get("failures") if isinstance(data, dict) else None
    return [entry for entry in failures or [] if isinstance(entry, dict)]


def dump(failures: list[dict]) -> str:
    return HEADER + yaml.safe_dump({"failures": failures}, sort_keys=False, allow_unicode=True, width=100)


def actionable(failures: list[dict], today: date, persist_days: int = DEFAULT_PERSIST_DAYS) -> list[dict]:
    flagged = []
    for entry in failures:
        if entry.get("kind") in ALWAYS_ACTIONABLE:
            flagged.append(entry)
            continue
        try:
            first = date.fromisoformat(str(entry.get("first_seen")))
        except ValueError:
            continue
        if (today - first).days >= persist_days:
            flagged.append(entry)
    return flagged


def _today() -> date:
    return datetime.now(timezone.utc).date()


def cmd_record(args: argparse.Namespace) -> int:
    fresh: dict[str, list[dict]] = {}
    for spec in args.log:
        source, _, raw_path = spec.partition("=")
        if source not in SOURCES or not raw_path:
            print(f"art_queue_health: bad --log {spec!r} (want one of {SOURCES}=PATH)", file=sys.stderr)
            return 2
        path = Path(raw_path)
        text = path.read_text(errors="replace") if path.exists() else ""
        if not text.strip():
            print(f"art_queue_health: {source}: no log (step skipped?) -- keeping its previous entries")
            continue
        fresh[source] = parse_log(text, source)
        print(f"art_queue_health: {source}: {len(fresh[source])} failure line(s)")

    out = Path(args.out)
    previous = load(out)
    merged = merge(previous, fresh, args.today or _today().isoformat())
    rendered = dump(merged)
    if out.exists() and out.read_text() == rendered:
        print(f"art_queue_health: {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out} unchanged")
        return 0
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(rendered)
    print(f"art_queue_health: wrote {len(merged)} failure(s)")
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    failures = load(Path(args.out))
    today = date.fromisoformat(args.today) if args.today else _today()
    flagged = actionable(failures, today, args.persist_days)
    if args.json:
        print(json.dumps({"failures": len(failures), "actionable": flagged}, indent=2))
        return 1 if flagged else 0
    if not flagged:
        print(f"art_queue_health: clean ({len(failures)} recorded failure(s), none actionable yet)")
        return 0
    by_kind: dict[str, int] = {}
    for entry in flagged:
        by_kind[entry["kind"]] = by_kind.get(entry["kind"], 0) + 1
    summary = ", ".join(f"{count} {kind}" for kind, count in sorted(by_kind.items()))
    print(f"art_queue_health: {len(flagged)} actionable art failure(s): {summary} -- role art-medic")
    for entry in flagged[:15]:
        rules = f" [{', '.join(entry['rules'])}]" if entry.get("rules") else ""
        print(f"  {entry['kind']}{rules}  {entry['source']}  {entry['target']}  (since {entry.get('first_seen')})")
    if len(flagged) > 15:
        print(f"  ... +{len(flagged) - 15} more in {HEALTH_FILE.relative_to(ROOT)}")
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", default=str(HEALTH_FILE), help="health file (default: %(default)s)")
    parser.add_argument("--today", help="override today's date (YYYY-MM-DD), for tests")
    sub = parser.add_subparsers(dest="command", required=True)
    record = sub.add_parser("record", help="parse art step logs into the health file")
    record.add_argument("--log", action="append", default=[], help="SOURCE=PATH, repeatable")
    check = sub.add_parser("check", help="exit 1 when there is art-medic work")
    check.add_argument("--persist-days", type=int, default=DEFAULT_PERSIST_DAYS)
    check.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    return cmd_record(args) if args.command == "record" else cmd_check(args)


if __name__ == "__main__":
    sys.exit(main())
