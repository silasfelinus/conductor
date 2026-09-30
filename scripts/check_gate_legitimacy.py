#!/usr/bin/env python3
"""Flag `needs-human` gates that are not actually waiting on a human.

WHY THIS EXISTS. Silas, 2026-09-30: *"can we get some sort of oversight so that
we aren't allowing things to hang when its not really a human gate issue?"*
The triage that prompted it found 51 open gates. A fair number of them were not
waiting on Silas at all:

- art-archive/t-033 went from soft gate, to "reclassified as ordinary engineering
  work", then back to a soft gate, asking whether archive jobs should use
  ComfyUI. Silas had already answered that in a standing directive ("any (all)
  gen tasks should be comfy").
- art-archive/t-041 was parked on "needs a Force Update first". Production had
  been running a build containing the fix for nine days.
- rainbow-butterflies/t-014 is a wait on t-009/t-010. It was filed as a gate
  anyway, so it counted as one more thing for Silas to clear.
- cthulhuquarium/t-065 sat as a HARD gate with `gate_human: false` and
  `stakes: reversible`, which means nothing in it needed a human at all.

`audit_human_gates.py` lists gates. It deliberately flags only strong
contradictions, because it must never nag Silas about a real privacy, money or
publishing decision. This script asks the opposite question: which gates
**agents** should take back? Every finding is agent work. None of them ask
Silas to do anything.

Findings (each one names the fix):

  NO_GATE_BASIS       A hard (non-soft) gate with no hard-gate marker at all.
                      That means no gate_human, reversible or unset stakes,
                      software kind, and no `gate_reason`. AGENTS.md "Hard vs
                      soft" gives such a task no grounds to stop.
                      Fix: return it to ready, or name the real reason in
                      `gate_reason`.
  APPROVED_PARKED     approved_by_human is already true but the task still sits
                      at needs-human. The decision is made; what remains is
                      execution. Fix: do it, or record the one step only
                      Silas can take as `gate_reason: physical-access` or
                      `gate_reason: secrets`.
  SHOULD_BE_WAITING   depends_on names a task that is not done. That is a
                      dependency wait, not a human gate. Fix: `status: waiting`,
                      so resolve_deps.py releases it automatically.
  DEPLOY_PREREQ_MET   (--live only) The note waits on a Kind Robots Force
                      Update/deploy, and the build now serving production
                      (/api/version) was committed after the task's last
                      update. Fix: re-run the blocked step now.
  UNREVIEWED          The gate has not been touched or re-checked in
                      --soft-days (soft) or --hard-days (hard) days. Fix: an
                      agent re-triages it: return it to ready, build the missing
                      agent path, or stamp `gate_rechecked: YYYY-MM-DD` with a
                      one-line reason in the note. Gates whose `gate_reason` is
                      a genuinely human-only category (money, publish, legal,
                      irreversible, secrets, security, physical-access,
                      subjective-acceptance, creative-approval) use the longer
                      --reasoned-days window. They are legitimately waiting on
                      Silas, and re-triaging them weekly would be noise.

Optional task fields this reads, none required:
  gate_reason:     one of GATE_REASONS below. It names why a human is needed.
  gate_rechecked:  YYYY-MM-DD of the last agent re-triage.

Exit 0 when clean, 1 when any finding exists. Advisory for the sweep, and the
trigger for `select_role.py`'s `gate-triage` role. Paused, retired and finished
projects are skipped, the same as audit_human_gates.py.

Usage:
  python scripts/check_gate_legitimacy.py
  python scripts/check_gate_legitimacy.py --live      # also check deploy state
  python scripts/check_gate_legitimacy.py --json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_human_gates import PROJECTS, scan  # noqa: E402

# Categories where waiting on Silas is the correct state. A gate carrying one
# of these gets the long re-check window instead of the weekly one.
GATE_REASONS = frozenset(
    {
        "money",                  # live payments, payouts, spend
        "publish",                # public posting, store submission, outreach
        "legal",                  # contracts, terms, licensing
        "irreversible",           # destructive or one-way production action
        "secrets",                # credentials only Silas can supply
        "security",               # security finding needing acknowledgement
        "physical-access",        # hands on Alexandria / Silas-PC / a console
        "subjective-acceptance",  # "does this look/feel right" visual or play verdict
        "creative-approval",      # content/proposal sign-off
    }
)

# An approved decision can still legitimately wait on Silas when the only remaining
# step needs his hands: a console, or a credential only he can supply.
HANDS_ONLY_REASONS = frozenset({"physical-access", "secrets"})

DEFAULT_SOFT_DAYS = 7
DEFAULT_HARD_DAYS = 14
DEFAULT_REASONED_DAYS = 30

DEPLOY_WAIT = re.compile(r"force update|not (?:yet )?deployed|merge != deploy|reach(?:es|ed)? production", re.I)
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")


def _as_date(value: Any) -> date | None:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    match = DATE_RE.search(str(value or ""))
    if not match:
        return None
    try:
        return date.fromisoformat(match.group(1))
    except ValueError:
        return None


def _as_datetime(value: Any) -> datetime | None:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    text = str(value or "").strip()
    if not text:
        return None
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        day = _as_date(text)
        return datetime(day.year, day.month, day.day, tzinfo=timezone.utc) if day else None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def _load_tasks(projects_dir: Path, slug: str) -> dict[str, dict[str, Any]]:
    data = yaml.safe_load((projects_dir / slug / "roadmap.yaml").read_text(encoding="utf-8")) or {}
    return {
        str(t.get("id")): t
        for t in data.get("tasks", []) or []
        if isinstance(t, dict) and t.get("id")
    }


def _kind(projects_dir: Path, slug: str) -> str:
    data = yaml.safe_load((projects_dir / slug / "roadmap.yaml").read_text(encoding="utf-8")) or {}
    return str(data.get("kind") or "software")


def _deps(task: dict[str, Any]) -> list[str]:
    raw = task.get("depends_on")
    if raw is None:
        return []
    return [str(d) for d in (raw if isinstance(raw, list) else [raw])]


def deployed_commit_time(
    base_url: str = "https://kindrobots.org",
    repo: str = "silasfelinus/kind_robots",
    token: str = "",
) -> datetime | None:
    """Commit time of the build production is serving, or None if unknown."""
    try:
        with urllib.request.urlopen(f"{base_url}/api/version", timeout=20) as resp:
            sha = (json.load(resp).get("data") or {}).get("commit")
        if not sha:
            return None
        req = urllib.request.Request(
            f"https://api.github.com/repos/{repo}/commits/{sha}",
            headers={"Accept": "application/vnd.github+json", "User-Agent": "conductor-gate-legitimacy"},
        )
        if token:
            req.add_header("Authorization", f"Bearer {token}")
        with urllib.request.urlopen(req, timeout=20) as resp:
            stamp = json.load(resp)["commit"]["committer"]["date"]
        return _as_datetime(stamp)
    except Exception as error:  # pragma: no cover - network-dependent
        print(f"[gate-legitimacy] deploy check unavailable: {error}", file=sys.stderr)
        return None


def classify(
    gate: dict[str, Any],
    task: dict[str, Any],
    tasks: dict[str, dict[str, Any]],
    kind: str,
    *,
    today: date,
    soft_days: int = DEFAULT_SOFT_DAYS,
    hard_days: int = DEFAULT_HARD_DAYS,
    reasoned_days: int = DEFAULT_REASONED_DAYS,
    deployed_at: datetime | None = None,
) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    soft = bool(task.get("soft_gate"))
    reason = str(task.get("gate_reason") or "").strip().lower()
    stakes = str(task.get("stakes") or "reversible").strip().lower()

    def add(code: str, detail: str) -> None:
        findings.append({"code": code, "detail": detail})

    if (
        not soft
        and not task.get("gate_human")
        and stakes not in {"outward-facing", "irreversible"}
        and kind not in {"content", "proposal"}
        and not task.get("security_flag")
        and reason not in GATE_REASONS
    ):
        add(
            "NO_GATE_BASIS",
            "hard gate with no gate_human, reversible stakes and no gate_reason. "
            "Return it to ready, or name the real reason.",
        )

    if task.get("approved_by_human") is True and reason not in HANDS_ONLY_REASONS:
        add(
            "APPROVED_PARKED",
            "approved_by_human is already true, so the decision is made. Execute it, "
            "or record the one hands-on step as gate_reason: physical-access or secrets.",
        )

    unmet = [d for d in _deps(task) if str((tasks.get(d) or {}).get("status")) != "done"]
    if unmet:
        add(
            "SHOULD_BE_WAITING",
            f"depends_on {', '.join(unmet)} is not done. Set status: waiting so "
            "resolve_deps.py releases it.",
        )

    updated = _as_datetime(task.get("updated"))
    if deployed_at and updated and deployed_at > updated and DEPLOY_WAIT.search(str(task.get("note") or "")):
        add(
            "DEPLOY_PREREQ_MET",
            f"the note waits on a deploy, and production has served a build committed "
            f"{deployed_at:%Y-%m-%d} since the last update ({updated:%Y-%m-%d}). Re-run the "
            "blocked step.",
        )

    touched = max(
        (d for d in (_as_date(task.get("updated")), _as_date(task.get("gate_rechecked"))) if d),
        default=None,
    )
    window = reasoned_days if reason in GATE_REASONS else (soft_days if soft else hard_days)
    age = (today - touched).days if touched else None
    if age is None or age >= window:
        since = f"{age} days" if age is not None else "ever (no updated/gate_rechecked date)"
        add(
            "UNREVIEWED",
            f"not re-triaged in {since} (window {window}d). Return it to ready, build "
            "the missing agent path, or stamp gate_rechecked with a reason.",
        )
    return findings


def check(
    projects_dir: Path = PROJECTS,
    *,
    today: date | None = None,
    soft_days: int = DEFAULT_SOFT_DAYS,
    hard_days: int = DEFAULT_HARD_DAYS,
    reasoned_days: int = DEFAULT_REASONED_DAYS,
    deployed_at: datetime | None = None,
) -> list[dict[str, Any]]:
    today = today or datetime.now(timezone.utc).date()
    results: list[dict[str, Any]] = []
    cache: dict[str, tuple[dict[str, dict[str, Any]], str]] = {}
    for gate in scan(projects_dir=projects_dir):
        slug = gate["project"]
        if slug not in cache:
            cache[slug] = (_load_tasks(projects_dir, slug), _kind(projects_dir, slug))
        tasks, kind = cache[slug]
        task = tasks.get(str(gate["task_id"]))
        if task is None:
            continue
        findings = classify(
            gate,
            task,
            tasks,
            kind,
            today=today,
            soft_days=soft_days,
            hard_days=hard_days,
            reasoned_days=reasoned_days,
            deployed_at=deployed_at,
        )
        if findings:
            results.append(
                {
                    "project": slug,
                    "task_id": gate["task_id"],
                    "title": gate["title"],
                    "soft_gate": gate["soft_gate"],
                    "gate_reason": task.get("gate_reason"),
                    "findings": findings,
                }
            )
    return results


def render(results: list[dict[str, Any]], total: int) -> str:
    if not results:
        return f"All {total} active gate(s) are legitimately waiting on a human and recently re-triaged."
    lines = [
        f"{len(results)} of {total} active gate(s) look like agent work, not a human gate:",
        "",
    ]
    for item in results:
        codes = ", ".join(f["code"] for f in item["findings"])
        lines.append(f"- {item['project']}/{item['task_id']} [{codes}] {item['title']}")
        for finding in item["findings"]:
            lines.append(f"    {finding['code']}: {finding['detail']}")
    lines += [
        "",
        "Every finding is agent work. Take the gate back (select_role.py role: gate-triage).",
        "Do not ask Silas to clear it. Stamping gate_rechecked is only honest after a real re-check.",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--live", action="store_true", help="check the deployed Kind Robots build (network)")
    parser.add_argument("--soft-days", type=int, default=DEFAULT_SOFT_DAYS)
    parser.add_argument("--hard-days", type=int, default=DEFAULT_HARD_DAYS)
    parser.add_argument("--reasoned-days", type=int, default=DEFAULT_REASONED_DAYS)
    args = parser.parse_args()

    deployed_at = None
    if args.live:
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or ""
        deployed_at = deployed_commit_time(token=token)

    total = len(scan())
    results = check(
        soft_days=args.soft_days,
        hard_days=args.hard_days,
        reasoned_days=args.reasoned_days,
        deployed_at=deployed_at,
    )
    if args.json:
        print(json.dumps({"total_gates": total, "flagged": results}, indent=2, default=str))
    else:
        print(render(results, total))
    sys.exit(1 if results else 0)


if __name__ == "__main__":
    main()
