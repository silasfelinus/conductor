#!/usr/bin/env python3
"""reconcile_unrecorded_art.py -- find art that rendered but was never recorded, and record it.

WHY THIS EXISTS. Silas, 2026-11-11 PT: "A lot of our art generated seems to fail to get recorded,
so we keep finding art that was requested and made but not linked ... it should be both corrected
and linked and be a part of the normal conductor agent task rotation to be responsible for that
sweep so it doesn't get lost because a thread agent was killed."

Every Conductor art submitter writes the returned ArtJob id into a file (a ledger cell's ``jobs:``,
a request's ``last_art_job_id``) and the id is only durable once that file reaches main. Measured
2026-11-11: of 2,000 DONE ArtJobs over two days, 382 were referenced nowhere in either repo --
Ruler Hooked's 211 art-prompts.yaml requests had rendered about 414 times while every row still
read ``pending`` with no job id (Auto Art Generate runs time out at 150 minutes, before "Commit
conductor results"), 50 Monstrique renders were submitted by a session that never recorded them,
and an Ironjaw round sat in a run that had not checkpointed yet.

Three passes, cheapest first. Each writes only with --apply:

  1. keyed    Every unrecorded ledger cell and pending request has a deterministic request key
              (scripts/art_request_key.py). ``POST /api/art/queue/lookup`` (kind_robots#5031)
              returns the job for each key, and the id is written back.
  2. backfill (--backfill-days N) Jobs submitted without a key (before #5031, or by another
              tool) are matched to a still-unrecorded cell/request by prompt text within the same
              project. Newest DONE wins; extra DONE renders of one target count as duplicates.
  3. strays   (--strays-days N) DONE jobs for a Conductor project whose ArtJob id and ArtImage id
              appear nowhere in this repo (or the kind_robots checkout) are recorded into
              ``projects/<slug>/art/RECOVERED-<date>.yaml`` -- a ledger the art-medic rotation
              triages (link it, mark it duplicate, or reject it). That is the "linked" half: the
              render becomes a reviewable ledger cell instead of an orphan on the admin page.

The run summary goes to ``ops/unrecorded-art.yaml`` (--report). select_role.py reads it and makes
``art-medic`` own whatever needs judgment; the session sweep reports it.

    python scripts/reconcile_unrecorded_art.py                       # keyed pass, dry run
    python scripts/reconcile_unrecorded_art.py --apply --report ops/unrecorded-art.yaml
    python scripts/reconcile_unrecorded_art.py --apply --backfill-days 3 --strays-days 2 \
        --report ops/unrecorded-art.yaml
    python scripts/reconcile_unrecorded_art.py --check               # offline: read the report

Env: KR_API_TOKEN, KR_BASE_URL. Exit: 0 nothing to do, 1 something recovered/recorded or needs
triage, 2 could not check (no token, Kind Robots unreachable).
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import consume_art_queue_core as core  # noqa: E402
import enqueue_art_requests as ledgers  # noqa: E402
from art_request_key import ledger_cell_key, request_key  # noqa: E402
from art_request_staging_priority import positive_job_id  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ART_PROMPTS = ROOT / "projects" / "art-prompts.yaml"
LEDGER_PATTERNS = ("projects/*/art/*.yaml", "projects/*/art/**/*.yaml")
DEFAULT_REPORT = ROOT / "ops" / "unrecorded-art.yaml"
LOOKUP_CHUNK = 400
PACIFIC = ZoneInfo("America/Los_Angeles")
RECOVERED_LANE = {
    "key": "recovered",
    "label": "Rendered by Kind Robots but recorded nowhere; adopted by reconcile_unrecorded_art.py",
    "engine": "recovered",
    "prompt": "prose",
}
# A recovered cell is untriaged until an agent sets one of these (see docs/agents/roles/art-medic.md).
TRIAGE_VALUES = ("linked", "adopted", "duplicate", "rejected")
REPORT_STALE_HOURS = 6
LOOKUP_UNAVAILABLE_GRACE_HOURS = 48


# --------------------------------------------------------------------------- targets


class Target:
    """One thing that should own an ArtJob id but has none on disk."""

    def __init__(self, kind, path, key, project, prompt, label, subject=None, lane=None, request=None):
        self.kind = kind  # "ledger" | "request"
        self.path = path
        self.key = key
        self.project = project
        self.prompt = prompt
        self.label = label
        self.subject = subject
        self.lane = lane
        self.request = request
        self.job = None  # {"jobId", "status", "artImageId", "via"}
        self.ambiguous = False


def norm(text: Any) -> str:
    return " ".join(str(text or "").split()).lower()


def ledger_paths(root: Path = ROOT) -> list[Path]:
    found = set()
    for pattern in LEDGER_PATTERNS:
        found.update(root.glob(pattern))
    return sorted(found)


def load_ledger_file(path: Path):
    try:
        header, data = ledgers.load_ledger(path)
    except (OSError, yaml.YAMLError):
        return None, None
    if not isinstance(data, dict) or not isinstance(data.get("lanes"), list) or not isinstance(data.get("subjects"), list):
        return None, None
    return header, data


def ledger_targets(root: Path = ROOT) -> tuple[list[Target], dict]:
    targets, loaded = [], {}
    for path in ledger_paths(root):
        header, data = load_ledger_file(path)
        if data is None:
            continue
        rel = path.relative_to(root).as_posix()
        project = data.get("project_slug") or rel.split("/")[1]
        loaded[path] = (header, data)
        for subject, lane in ledgers.iter_cells(data):
            if not isinstance(subject, dict) or not isinstance(lane, dict) or not lane.get("key"):
                continue
            if lane.get("key") == RECOVERED_LANE["key"] or ledgers.job_id_of(subject, lane["key"]):
                continue
            targets.append(
                Target(
                    "ledger", path, ledger_cell_key(rel, lane, subject), project,
                    ledgers.compose_prompt(lane, subject), f"{rel}#{subject.get('key')}@{lane['key']}",
                    subject=subject, lane=lane,
                )
            )
    return targets, loaded


def request_targets(path: Path = ART_PROMPTS) -> list[Target]:
    if not path.exists():
        return []
    data = yaml.safe_load(path.read_text()) or {}
    targets = []
    for entry in data.get("requests") or []:
        if not isinstance(entry, dict) or not entry.get("id") or not entry.get("prompt"):
            continue
        if str(entry.get("status") or "pending").strip().lower() != "pending":
            continue
        if positive_job_id(entry.get("last_art_job_id")) is not None:
            continue
        targets.append(
            Target(
                "request", path, request_key(entry), str(entry.get("project_slug") or entry.get("source") or ""),
                entry.get("prompt"), f"art-prompts.yaml#{entry['id']}", request=entry,
            )
        )
    return targets


# --------------------------------------------------------------------------- Kind Robots


def http(method, url, body=None, timeout=60, attempts=3):
    """core.http_json with retries for the relay's 502s and cut-off bodies."""
    last = (None, None)
    for attempt in range(attempts):
        try:
            last = core.http_json(method, url, body, timeout=timeout)
        except Exception as error:  # noqa: BLE001 - network faults are retried, then reported
            last = (None, {"message": f"{type(error).__name__}: {error}"})
        if last[0] and last[0] < 500 and isinstance(last[1], dict):
            return last
        time.sleep(2 * (attempt + 1))
    return last


def lookup_keys(keys: list[str], post=None) -> tuple[str, dict[str, dict]]:
    """('ok'|'unavailable'|'error', {requestKey: job})."""
    post = post or (lambda body: http("POST", f"{core.KR_BASE_URL}/api/art/queue/lookup", body))
    found: dict[str, dict] = {}
    for start in range(0, len(keys), LOOKUP_CHUNK):
        status, resp = post({"requestKeys": keys[start:start + LOOKUP_CHUNK]})
        message = str((resp or {}).get("message") or "") if isinstance(resp, dict) else ""
        # Before kind_robots#5031 deploys the path falls through to the site's HTML page.
        if status in (404, 405) or "JSONDecodeError" in message:
            return "unavailable", found
        if status != 200 or not isinstance(resp, dict) or not resp.get("success"):
            return "error", found
        for job in (resp.get("data") or {}).get("jobs") or []:
            found[job["requestKey"]] = job
    return "ok", found


def job_prompt(job: dict) -> str:
    payload = job.get("payload") or {}
    provenance = payload.get("provenance") or {}
    return provenance.get("normalizedPrompt") or payload.get("promptString") or payload.get("basePromptString") or ""


def parse_time(value) -> datetime | None:
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None


def page_jobs(query: str, since: datetime, max_pages: int, get=None, time_field="createdAt"):
    """Yield lean dicts for jobs newer than ``since`` from the (heavy) queue listing."""
    get = get or (lambda url: http("GET", url, timeout=120, attempts=4))
    for page in range(1, max_pages + 1):
        status, resp = get(f"{core.KR_BASE_URL}/api/art/queue?{query}&pageSize=20&page={page}")
        if status != 200 or not isinstance(resp, dict) or not resp.get("data"):
            raise RuntimeError(f"queue listing page {page} failed: HTTP {status}")
        jobs = resp["data"].get("jobs") or []
        for job in jobs:
            when = parse_time(job.get(time_field))
            if when and when < since:
                return
            payload = job.get("payload") or {}
            yield {
                "id": job.get("id"),
                "status": job.get("status"),
                "artImageId": job.get("artImageId"),
                "projectSlug": job.get("projectSlug"),
                "createdAt": job.get("createdAt"),
                "designer": (payload.get("save") or {}).get("designer"),
                "requestKey": payload.get("requestKey"),
                "prompt": job_prompt(job),
            }
        if not (resp["data"].get("pagination") or {}).get("hasNextPage"):
            return


# --------------------------------------------------------------------------- passes

STATUS_RANK = {"DONE": 3, "RUNNING": 2, "PENDING": 2, "FAILED": 1, "CANCELLED": 0}


def match_by_prompt(targets: list[Target], jobs: list[dict]) -> tuple[int, int]:
    """Attach the best keyless job to each target. Returns (matched, duplicate DONE renders)."""
    by_prompt: dict[str, list[Target]] = {}
    for target in targets:
        if target.job is None and norm(target.prompt):
            by_prompt.setdefault(norm(target.prompt), []).append(target)
    candidates: dict[int, list[dict]] = {}
    for job in jobs:
        text = norm(job.get("prompt"))
        if not text:
            continue
        hits = [t for prompt, group in by_prompt.items() if prompt in text for t in group]
        if len(hits) > 1:
            # A shorter prompt can sit inside a longer one; the exact match wins.
            hits = [t for t in hits if norm(t.prompt) == text] or hits
        if not hits:
            continue
        if len(hits) > 1:  # one prompt, several cells (A/B lanes): this job cannot say which
            for target in hits:
                target.ambiguous = True
            continue
        candidates.setdefault(id(hits[0]), []).append(job)
    matched = duplicates = 0
    for target in targets:
        jobs_for = candidates.get(id(target))
        if not jobs_for:
            continue
        target.ambiguous = False  # an unambiguous job of its own settles it
        jobs_for.sort(key=lambda j: (STATUS_RANK.get(str(j.get("status")), 0), j.get("id") or 0), reverse=True)
        best = jobs_for[0]
        target.job = {"jobId": best["id"], "status": best.get("status"), "artImageId": best.get("artImageId"), "via": "prompt"}
        duplicates += sum(1 for j in jobs_for[1:] if j.get("status") == "DONE")
        matched += 1
    return matched, duplicates


def reference_numbers(paths: list[Path]) -> set[int]:
    """Every 4-7 digit number in the tracked (and untracked) text of each repo: job and image ids."""
    numbers: set[int] = set()
    for repo in paths:
        if not (repo / ".git").exists():
            continue
        result = subprocess.run(
            ["git", "-C", str(repo), "grep", "-I", "-o", "-h", "-w", "--untracked", "-E", "[0-9]{4,7}", "--", "."],
            capture_output=True, check=False,
        )
        for line in result.stdout.splitlines():
            try:
                numbers.add(int(line))
            except ValueError:
                continue
    return numbers


# Kind Robots admin pages that queue art and keep the job ids in their own database rows, where
# neither repo's text can see them. A job listed by one of these is recorded, not a stray
# (2026-11-12: all 53 "unrecorded" Monstress renders were Monstrique series-bible portraits).
STUDIO_GALLERIES = ("/api/monstrique/bible",)


def studio_gallery_numbers(get=None) -> set[int]:
    """Job and ArtImage ids that Kind Robots studio pages already record. Best effort: an
    unreachable page contributes nothing (its renders then surface as strays for triage)."""
    get = get or (lambda url: http("GET", url))
    numbers: set[int] = set()
    for path in STUDIO_GALLERIES:
        status, data = get(f"{core.KR_BASE_URL}{path}")
        if status != 200 or not isinstance(data, dict):
            print(f"  studio gallery {path}: unavailable ({status})", file=sys.stderr)
            continue
        payload = data.get("data") if isinstance(data.get("data"), dict) else data
        for character in payload.get("characters") or []:
            for item in (character or {}).get("gallery") or []:
                for field in ("jobId", "artImageId"):
                    value = positive_job_id(item.get(field))
                    if value:
                        numbers.add(value)
    return numbers


PREFIX_CHARS = 32


def known_prompts(root: Path = ROOT, prompts_path: Path = ART_PROMPTS) -> dict[str, list[str]]:
    """Every prompt Conductor has asked for -- each ledger cell and each request, any status --
    indexed by its first PREFIX_CHARS normalized characters."""
    index: dict[str, list[str]] = {}

    def add(text):
        text = norm(text)
        if len(text) >= PREFIX_CHARS:
            index.setdefault(text[:PREFIX_CHARS], []).append(text)

    for path in ledger_paths(root):
        _, data = load_ledger_file(path)
        if data is None:
            continue
        for subject, lane in ledgers.iter_cells(data):
            if isinstance(subject, dict) and isinstance(lane, dict) and lane.get("key") != RECOVERED_LANE["key"]:
                add(ledgers.compose_prompt(lane, subject))
    if prompts_path.exists():
        data = yaml.safe_load(prompts_path.read_text()) or {}
        for section in ("requests", "images"):
            for entry in data.get(section) or []:
                if isinstance(entry, dict):
                    add(entry.get("prompt"))
    return index


def is_known(text: str, index: dict[str, list[str]]) -> bool:
    text = norm(text)
    return any(text.startswith(prompt) or prompt in text for prompt in index.get(text[:PREFIX_CHARS], ()))


def find_strays(jobs: list[dict], refs: set[int], projects: set[str], claimed: set[int], min_age: datetime,
                known: dict[str, list[str]] | None = None) -> tuple[list[dict], int]:
    """(strays, extra renders of known work). A DONE render whose prompt is one Conductor asked for
    is an extra copy of recorded work -- counted, not adopted -- and only the rest are strays."""
    strays, extra = [], 0
    for job in jobs:
        if job.get("status") != "DONE" or job.get("projectSlug") not in projects:
            continue
        if job["id"] in claimed or job["id"] in refs or (job.get("artImageId") or 0) in refs:
            continue
        created = parse_time(job.get("createdAt"))
        if created and created > min_age:
            continue  # a run that is still going may be about to commit it
        if known and is_known(job.get("prompt"), known):
            extra += 1
            continue
        strays.append(job)
    return strays, extra


# --------------------------------------------------------------------------- writing


def apply_ledger(target: Target) -> None:
    lane_key = target.lane["key"]
    target.subject.setdefault("jobs", {})[lane_key] = int(target.job["jobId"])
    art = target.subject.setdefault("art", {})
    art[lane_key] = {"status": target.job.get("status"), "art_image_id": target.job.get("artImageId")}


def apply_requests(targets: list[Target], path: Path = ART_PROMPTS) -> int:
    import consume_art_requests as requests_lane  # noqa: PLC0415 - heavy import only when writing

    text = path.read_text()
    changed = 0
    for target in targets:
        text, did = requests_lane.set_request_field(text, target.request["id"], "last_art_job_id", int(target.job["jobId"]))
        changed += bool(did)
    if changed:
        path.write_text(text)
    return changed


def recovered_ledger_path(project: str, today: str, root: Path = ROOT) -> Path:
    return root / "projects" / project / "art" / f"RECOVERED-{today}.yaml"


RECOVERED_HEADER = """# Renders Kind Robots finished for this project that nothing in Conductor or kind_robots recorded:
# no ledger cell, request or manifest names their ArtJob or ArtImage id. Written by
# scripts/reconcile_unrecorded_art.py (Silas, 2026-11-11 PT: "art that was requested and made but
# not linked"). Not auto_submit: nothing here is ever re-rendered.
#
# art-medic triage (docs/agents/roles/art-medic.md "Unrecorded art"): give every subject a
# `triage:` of linked (wired into the game/site; say where in `linked_to:`), adopted (moved into
# the ledger cell it belongs to), duplicate (`duplicate_of:` the kept job), or rejected (off-brief;
# adult renders are marked mature, never deleted).
"""


def write_strays(strays: list[dict], today: str, root: Path = ROOT) -> list[Path]:
    written = []
    by_project: dict[str, list[dict]] = {}
    for job in strays:
        by_project.setdefault(job["projectSlug"], []).append(job)
    for project, jobs in sorted(by_project.items()):
        path = recovered_ledger_path(project, today, root)
        if path.exists():
            header, data = ledgers.load_ledger(path)
        else:
            header, data = RECOVERED_HEADER, None
        data = data or {
            "round": f"{project}-recovered-{today}",
            "project_slug": project,
            "designer": "Recovered unrecorded renders",
            "auto_submit": False,
            "lanes": [dict(RECOVERED_LANE)],
            "subjects": [],
        }
        have = {int(j) for s in data["subjects"] for j in (s.get("jobs") or {}).values() if j}
        for job in sorted(jobs, key=lambda j: j["id"]):
            if job["id"] in have:
                continue
            data["subjects"].append({
                "key": f"recovered-{job['id']}",
                "lane": "recovered",
                "title": job.get("designer") or "unrecorded render",
                "prompt_prose": " ".join(str(job.get("prompt") or "").split()),
                "jobs": {"recovered": job["id"]},
                "art": {"recovered": {"status": "DONE", "art_image_id": job.get("artImageId")}},
                "created_at": job.get("createdAt"),
            })
        path.parent.mkdir(parents=True, exist_ok=True)
        ledgers.save_ledger(path, header, data)
        written.append(path)
    return written


def untriaged_recovered(root: Path = ROOT) -> list[dict]:
    """RECOVERED ledgers with subjects nobody has triaged yet."""
    rows = []
    for path in sorted(root.glob("projects/*/art/RECOVERED-*.yaml")):
        _, data = load_ledger_file(path)
        if data is None:
            continue
        open_count = sum(1 for s in data["subjects"] if str(s.get("triage") or "").lower() not in TRIAGE_VALUES)
        if open_count:
            rows.append({"ledger": path.relative_to(root).as_posix(), "untriaged": open_count, "subjects": len(data["subjects"])})
    return rows


# --------------------------------------------------------------------------- report / check


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def load_report(path: Path = DEFAULT_REPORT) -> dict:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text()) or {}


def actionable(report: dict, root: Path = ROOT, now: datetime | None = None) -> list[str]:
    """What an art-medic agent must do, from the committed report plus the RECOVERED ledgers."""
    now = now or now_utc()
    items = []
    for row in untriaged_recovered(root):
        items.append(f"triage {row['untriaged']} unrecorded render(s) in {row['ledger']}")
    generated = parse_time(report.get("generated_at")) if report else None
    if report and generated and now - generated > timedelta(hours=REPORT_STALE_HOURS):
        items.append(
            f"ops/unrecorded-art.yaml is {int((now - generated).total_seconds() // 3600)}h old: "
            "the Reconcile Unrecorded Art workflow has stopped running"
        )
    since = parse_time(report.get("lookup_unavailable_since")) if report else None
    if since and now - since > timedelta(hours=LOOKUP_UNAVAILABLE_GRACE_HOURS):
        items.append("POST /api/art/queue/lookup has been unavailable for over 48h (kind_robots#5031 not deployed?)")
    if report.get("ambiguous"):
        items.append(f"{report['ambiguous']} unrecorded cell(s) share one prompt across lanes; record their job ids by hand")
    return items


def check(report_path: Path, root: Path = ROOT) -> int:
    report = load_report(report_path)
    items = actionable(report, root)
    if not report:
        print("unrecorded art: no report yet (ops/unrecorded-art.yaml); the reconcile workflow has not run")
        return 2
    summary = (
        f"unrecorded art: last run {report.get('generated_at')}, lookup {report.get('lookup')}, "
        f"recovered {report.get('recovered_total', 0)} id(s), strays recorded {report.get('strays_recorded', 0)}, "
        f"duplicates seen {report.get('duplicate_renders', 0)}"
    )
    print(summary)
    for item in items:
        print(f"  - {item}")
    return 1 if items else 0


# --------------------------------------------------------------------------- main


def run(args) -> int:
    targets, loaded = ledger_targets(ROOT)
    targets += request_targets(ART_PROMPTS)
    previous = load_report(args.report) if args.report else {}
    report: dict[str, Any] = {
        "generated_at": now_utc().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "unrecorded_targets": len(targets),
    }
    if not core.KR_API_TOKEN:
        print("KR_API_TOKEN is required; nothing checked.", file=sys.stderr)
        return 2

    # 1. keyed
    lookup_state, found = lookup_keys([t.key for t in targets if t.key])
    report["lookup"] = lookup_state
    if lookup_state == "ok":
        report["lookup_unavailable_since"] = None
    else:
        report["lookup_unavailable_since"] = previous.get("lookup_unavailable_since") or report["generated_at"]
    for target in targets:
        job = found.get(target.key)
        if job:
            target.job = {**job, "via": "key"}
    keyed = sum(1 for t in targets if t.job)

    # 2. backfill
    duplicates = 0
    claimed: set[int] = set()
    if args.backfill_days:
        since = now_utc() - timedelta(days=args.backfill_days)
        projects = sorted({t.project for t in targets if t.job is None and t.project})
        if args.project:
            projects = [p for p in projects if p in args.project]
        for project in projects:
            try:
                jobs = list(page_jobs(f"projectSlug={project}", since, args.max_pages))
            except RuntimeError as error:
                print(f"  backfill {project}: {error}", file=sys.stderr)
                continue
            _, dups = match_by_prompt([t for t in targets if t.project == project], jobs)
            duplicates += dups
    matched = [t for t in targets if t.job]
    claimed.update(int(t.job["jobId"]) for t in matched)
    report["ambiguous"] = sum(1 for t in targets if t.ambiguous and t.job is None)
    report["duplicate_renders"] = duplicates

    for target in matched:
        print(f"  {'RECORD' if args.apply else 'would record'} job {target.job['jobId']} "
              f"({target.job.get('status')}, via {target.job['via']}) -> {target.label}")

    # 3. strays
    strays: list[dict] = []
    if args.strays_days:
        since = now_utc() - timedelta(days=args.strays_days)
        try:
            recent = list(page_jobs("status=DONE", since, args.strays_max_pages, time_field="updatedAt"))
        except RuntimeError as error:
            print(f"  stray scan: {error}", file=sys.stderr)
            recent = []
        refs = reference_numbers([ROOT, *([args.kind_robots] if args.kind_robots else [])])
        refs |= studio_gallery_numbers()
        projects = {p.name for p in (ROOT / "projects").iterdir() if p.is_dir()}
        min_age = now_utc() - timedelta(hours=args.stray_min_age_hours)
        strays, extra = find_strays(recent, refs, projects, claimed, min_age, known_prompts(ROOT))
        duplicates += extra
        report["duplicate_renders"] = duplicates
        report["stray_scan"] = {
            "days": args.strays_days,
            "scanned_jobs": len(recent),
            "kind_robots_checked": bool(args.kind_robots and (args.kind_robots / ".git").exists()),
        }
        for job in strays:
            print(f"  stray job {job['id']} (ArtImage {job.get('artImageId')}) {job['projectSlug']}: "
                  f"{str(job.get('designer') or job.get('prompt') or '')[:90]}")

    if args.apply:
        touched = set()
        for target in matched:
            if target.kind == "ledger":
                apply_ledger(target)
                touched.add(target.path)
        for path in sorted(touched):
            header, data = loaded[path]
            ledgers.save_ledger(path, header, data)
        apply_requests([t for t in matched if t.kind == "request"])
        if strays:
            write_strays(strays, datetime.now(PACIFIC).date().isoformat())

    report["recovered_total"] = len(matched)
    report["recovered_by"] = {"key": keyed, "prompt": len(matched) - keyed}
    report["recovered"] = [
        {"target": t.label, "job_id": int(t.job["jobId"]), "status": t.job.get("status"),
         "art_image_id": t.job.get("artImageId"), "via": t.job["via"]}
        for t in matched[:200]
    ]
    report["strays_recorded"] = len(strays) if args.apply else 0
    report["strays_found"] = len(strays)
    report["untriaged_recovered"] = untriaged_recovered(ROOT)

    if args.report and args.apply:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(
            "# Written by scripts/reconcile_unrecorded_art.py (Reconcile Unrecorded Art workflow). Do not hand-edit.\n"
            + yaml.safe_dump(report, sort_keys=False, width=110, allow_unicode=True)
        )

    print(
        f"\nunrecorded targets {len(targets)}; lookup {lookup_state}; recorded {len(matched)} "
        f"(key {keyed}, prompt {len(matched) - keyed}); duplicate DONE renders {duplicates}; strays {len(strays)}"
        + ("" if args.apply else " (dry run: --apply writes)")
    )
    if lookup_state == "error" and not matched:
        return 2
    return 1 if matched or strays else 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--apply", action="store_true", help="write recovered ids, RECOVERED ledgers and the report")
    parser.add_argument("--report", type=Path, default=None, help="summary YAML to write (with --apply) or read (--check)")
    parser.add_argument("--backfill-days", type=float, default=0, help="prompt-match keyless jobs this many days back")
    parser.add_argument("--max-pages", type=int, default=15, help="listing pages (20 jobs each) per project for backfill")
    parser.add_argument("--project", action="append", help="limit backfill to this project slug (repeatable)")
    parser.add_argument("--strays-days", type=float, default=0, help="scan DONE jobs this many days back for strays")
    parser.add_argument("--strays-max-pages", type=int, default=200, help="listing pages for the stray scan")
    parser.add_argument("--stray-min-age-hours", type=float, default=3.0, help="ignore jobs newer than this")
    parser.add_argument("--kind-robots", type=Path, default=None, help="kind_robots checkout to search for ids too")
    parser.add_argument("--check", action="store_true", help="offline: summarize the report and what needs an agent")
    args = parser.parse_args(argv)
    if args.check:
        return check(args.report or DEFAULT_REPORT)
    if args.kind_robots is None and (ROOT.parent / "kind_robots" / ".git").exists():
        args.kind_robots = ROOT.parent / "kind_robots"
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
