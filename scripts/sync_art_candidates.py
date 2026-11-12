#!/usr/bin/env python3
"""sync_art_candidates.py -- every render Conductor knows about becomes a candidate for its art slot.

WHY THIS EXISTS. Silas, 2026-11-11 PT: "In most cases, we should support having multiple art
sources for art. They should be manageable from a back end, so that the admin interfaces can
choose a better choice. If the art is actually duplicated (same seed), they can be deleted."
Kind Robots keeps those candidates in ArtSlot/ArtCandidate (kind_robots#5048, /admin/art-slots).
This script fills it from Conductor and clears true duplicates:

  1. ledgers  Every ledger cell with a DONE render and an ArtImage id. The slot is the
              subject's `asset:` (namespaced to its project), so redo rounds of one card, and
              every A/B lane of it, land in one slot. Ledgers whose content has not changed
              since the last sync (ops/art-candidates-sync.yaml) are skipped.
  2. harvest  (--harvest-days N) DONE ArtJobs per project, matched by prompt to any ledger cell
              or art-prompts.yaml request, recorded or not. This is what turns re-renders that
              were never recorded (Ruler Hooked rendered ~690 extra copies on 2026-11-10/11 PT)
              into choices instead of orphans. A request's recorded job is chosen if its slot
              has no choice yet.
  3. dedupe   (--dedupe) Asks Kind Robots which candidates in the touched projects are the same
              picture (same prompt, seed, checkpoint, sampler, steps, cfg), protects every
              ArtImage id this repo or the kind_robots checkout references (a game manifest
              may wire any copy), and moves the rest to the Recycle Bin (restorable).

    python scripts/sync_art_candidates.py                         # dry run: counts only
    python scripts/sync_art_candidates.py --apply                 # ledger pass
    python scripts/sync_art_candidates.py --apply --harvest-days 2 --dedupe --kind-robots ../kind_robots

Env: KR_API_TOKEN, KR_BASE_URL. Exit 0 ok, 2 could not reach Kind Robots / endpoint not deployed.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import consume_art_queue_core as core  # noqa: E402
import reconcile_unrecorded_art as rec  # noqa: E402
from art_request_key import _clean  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "ops" / "art-candidates-sync.yaml"
BATCH = 400
PREFIX_CHARS = rec.PREFIX_CHARS


# --------------------------------------------------------------------------- slot keys


def project_slot(project: str, path: str) -> str:
    """``<project>/<path>``, unless the path already starts with the project."""
    project = _clean(project or "unknown")
    path = _clean(str(path).strip("/"))
    if path.startswith(f"{project}/"):
        return path[:300]
    return f"{project}/{path}"[:300]


def ledger_slot(project: str, ledger_rel: str, subject: dict, lane: dict) -> str:
    if subject.get("asset"):
        return project_slot(project, subject["asset"])
    stem = Path(ledger_rel).stem
    return project_slot(project, f"ledger/{stem}/{subject.get('key')}@{lane.get('key')}")


def request_slot(entry: dict) -> str:
    project = str(entry.get("project_slug") or entry.get("source") or "requests")
    path = str(entry.get("image_path") or entry.get("id"))
    for prefix in ("public/images/", "projects/"):
        if path.startswith(prefix):
            path = path[len(prefix):]
    path = path.rsplit(".", 1)[0] if "." in Path(path).name else path
    return project_slot(project, path)


# --------------------------------------------------------------------------- collection


def ledger_candidates(root: Path = ROOT, synced: dict | None = None):
    """(candidates, {ledger_rel: content_hash}) for ledgers whose content changed since ``synced``."""
    synced = synced or {}
    out, hashes = [], {}
    for path in rec.ledger_paths(root):
        rel = path.relative_to(root).as_posix()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()[:16]
        hashes[rel] = digest
        if synced.get(rel) == digest:
            continue
        _, data = rec.load_ledger_file(path)
        if data is None:
            continue
        project = data.get("project_slug") or rel.split("/")[1]
        for subject, lane in rec.ledgers.iter_cells(data):
            if not isinstance(subject, dict) or not isinstance(lane, dict) or lane.get("key") == rec.RECOVERED_LANE["key"]:
                continue
            art = ((subject.get("art") or {}).get(lane["key"]) or {})
            image_id = art.get("art_image_id")
            if str(art.get("status") or "").upper() != "DONE" or not image_id:
                continue
            out.append({
                "slotKey": ledger_slot(project, rel, subject, lane),
                "projectSlug": project,
                "label": str(subject.get("title") or subject.get("key") or "")[:300] or None,
                "artImageId": int(image_id),
                "artJobId": rec.positive_job_id((subject.get("jobs") or {}).get(lane["key"])),
                "source": "conductor-ledger",
                "sourceRef": f"{rel}#{subject.get('key')}@{lane['key']}"[:300],
            })
    return out, hashes


def prompt_targets(root: Path = ROOT, prompts_path: Path = rec.ART_PROMPTS) -> dict[str, list[dict]]:
    """Every prompt Conductor asked for, by project: [{prompt, slotKey, label, source, sourceRef, chosenJob}]."""
    by_project: dict[str, list[dict]] = {}
    for path in rec.ledger_paths(root):
        rel = path.relative_to(root).as_posix()
        _, data = rec.load_ledger_file(path)
        if data is None:
            continue
        project = data.get("project_slug") or rel.split("/")[1]
        for subject, lane in rec.ledgers.iter_cells(data):
            if not isinstance(subject, dict) or not isinstance(lane, dict) or lane.get("key") == rec.RECOVERED_LANE["key"]:
                continue
            by_project.setdefault(project, []).append({
                "prompt": rec.norm(rec.ledgers.compose_prompt(lane, subject)),
                "slotKey": ledger_slot(project, rel, subject, lane),
                "label": str(subject.get("title") or subject.get("key") or "")[:300] or None,
                "source": "conductor-ledger",
                "sourceRef": f"{rel}#{subject.get('key')}@{lane['key']}"[:300],
                "chosenJob": None,
            })
    if prompts_path.exists():
        data = yaml.safe_load(prompts_path.read_text()) or {}
        for entry in data.get("requests") or []:
            if not isinstance(entry, dict) or not entry.get("prompt"):
                continue
            project = str(entry.get("project_slug") or entry.get("source") or "requests")
            by_project.setdefault(project, []).append({
                "prompt": rec.norm(entry["prompt"]),
                "slotKey": request_slot(entry),
                "label": str(entry.get("label") or entry.get("id") or "")[:300] or None,
                "source": "conductor-request",
                "sourceRef": f"art-prompts.yaml#{entry.get('id')}"[:300],
                "chosenJob": rec.positive_job_id(entry.get("last_art_job_id")),
            })
    return by_project


def match_jobs(targets: list[dict], jobs: list[dict]) -> list[dict]:
    """Candidates for every DONE job whose prompt is exactly one slot's prompt (or contains it)."""
    index: dict[str, list[dict]] = {}
    for target in targets:
        if len(target["prompt"]) >= PREFIX_CHARS:
            index.setdefault(target["prompt"][:PREFIX_CHARS], []).append(target)
    out = []
    for job in jobs:
        if job.get("status") != "DONE" or not job.get("artImageId"):
            continue
        text = rec.norm(job.get("prompt"))
        bucket = index.get(text[:PREFIX_CHARS], [])
        hits = [t for t in bucket if t["prompt"] == text] or [t for t in bucket if t["prompt"] in text]
        slots = {t["slotKey"] for t in hits}
        if len(slots) != 1:
            continue  # unmatched, or one prompt shared by different slots: cannot say which
        target = hits[0]
        out.append({
            "slotKey": target["slotKey"],
            "projectSlug": job.get("projectSlug"),
            "label": target["label"],
            "artImageId": int(job["artImageId"]),
            "artJobId": int(job["id"]),
            "source": target["source"],
            "sourceRef": target["sourceRef"],
            "selectIfEmpty": bool(target["chosenJob"] and int(target["chosenJob"]) == int(job["id"])),
        })
    return out


# --------------------------------------------------------------------------- Kind Robots


def post(path: str, body: dict, timeout=120):
    return rec.http("POST", f"{core.KR_BASE_URL}{path}", body, timeout=timeout)


def unavailable(status, resp) -> bool:
    message = str((resp or {}).get("message") or "") if isinstance(resp, dict) else ""
    return status in (404, 405) or "JSONDecodeError" in message


def register(candidates: list[dict], send=post) -> tuple[str, int]:
    """('ok'|'unavailable'|'error', new candidates)."""
    created = 0
    for start in range(0, len(candidates), BATCH):
        status, resp = send("/api/art/slots/candidates", {"candidates": candidates[start:start + BATCH]})
        if unavailable(status, resp):
            return "unavailable", created
        if status != 200 or not isinstance(resp, dict) or not resp.get("success"):
            print(f"  register batch {start // BATCH}: HTTP {status} {(resp or {}).get('message') if isinstance(resp, dict) else resp}",
                  file=sys.stderr)
            return "error", created
        created += sum(1 for r in (resp.get("data") or {}).get("results") or [] if r.get("status") == "created")
    return "ok", created


def dedupe(projects: list[str], refs: set[int], apply: bool, send=post) -> tuple[int, int]:
    """(planned, removed) across ``projects``; referenced ids are protected."""
    planned = removed = 0
    for project in projects:
        status, resp = send("/api/art/slots/dedupe", {"projectSlug": project, "apply": False})
        if status != 200 or not isinstance(resp, dict) or not resp.get("success"):
            continue
        ids = {i for slot in resp["data"]["slots"] for g in slot["groups"] for i in [g["keepArtImageId"], *g["removeArtImageIds"]]}
        protect = sorted(ids & refs)
        remove = {i for slot in resp["data"]["slots"] for g in slot["groups"] for i in g["removeArtImageIds"]} - set(protect)
        planned += len(remove)
        if apply and remove:
            status, resp = send("/api/art/slots/dedupe", {"projectSlug": project, "apply": True, "protectArtImageIds": protect})
            if status == 200 and isinstance(resp, dict) and resp.get("success"):
                removed += int(resp["data"].get("removed") or 0)
                print(f"  {project}: {resp['data'].get('removed')} duplicate render(s) to the Recycle Bin")
        elif remove:
            print(f"  {project}: {len(remove)} duplicate render(s) would go to the Recycle Bin")
    return planned, removed


# --------------------------------------------------------------------------- main


def load_state(path: Path = STATE) -> dict:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text()) or {}


def save_state(state: dict, path: Path = STATE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "# Written by scripts/sync_art_candidates.py: ledger content hashes already registered as art\n"
        "# candidates in Kind Robots. Delete a line to re-send that ledger. Do not hand-edit otherwise.\n"
        + yaml.safe_dump(state, sort_keys=True, width=110)
    )


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--apply", action="store_true", help="send candidates (and remove duplicates with --dedupe)")
    parser.add_argument("--full", action="store_true", help="re-send every ledger, ignoring the sync state")
    parser.add_argument("--harvest-days", type=float, default=0, help="match DONE jobs this many days back to slots")
    parser.add_argument("--max-pages", type=int, default=60, help="queue listing pages (20 jobs) per project for harvest")
    parser.add_argument("--project", action="append", help="limit harvest/dedupe to these projects")
    parser.add_argument("--dedupe", action="store_true", help="clear true duplicates in the touched projects")
    parser.add_argument("--kind-robots", type=Path, default=None, help="kind_robots checkout whose ids are protected")
    args = parser.parse_args(argv)
    if args.kind_robots is None and (ROOT.parent / "kind_robots" / ".git").exists():
        args.kind_robots = ROOT.parent / "kind_robots"
    if not core.KR_API_TOKEN:
        print("KR_API_TOKEN is required.", file=sys.stderr)
        return 2

    state = load_state()
    synced = {} if args.full else (state.get("ledgers") or {})
    candidates, hashes = ledger_candidates(ROOT, synced)
    touched = {c["projectSlug"] for c in candidates}
    print(f"ledger pass: {len(candidates)} candidate(s) from {sum(1 for k in hashes if synced.get(k) != hashes[k])} changed ledger(s)")

    # Ledgers first and saved at once, then each harvested project as soon as it is matched:
    # a long harvest cut off by the job timeout keeps everything already sent.
    outcome, created = ("ok", 0)
    if args.apply:
        outcome, created = register(candidates)
        print(f"register ledgers: {outcome}, {created} new candidate(s) of {len(candidates)}")
        if outcome == "unavailable":
            print("Kind Robots has no /api/art/slots yet (kind_robots#5048 not deployed); nothing recorded.", file=sys.stderr)
            return 2
        if outcome == "ok":
            state["ledgers"] = {**(state.get("ledgers") or {}), **hashes}
            state["last_sync"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            save_state(state)

    if args.harvest_days:
        since = datetime.now(timezone.utc) - timedelta(days=args.harvest_days)
        targets = prompt_targets(ROOT)
        projects = sorted(p for p in targets if not args.project or p in args.project)
        harvested = harvest_created = 0
        for project in projects:
            try:
                jobs = list(rec.page_jobs(f"projectSlug={project}&status=DONE", since, args.max_pages, time_field="updatedAt"))
            except RuntimeError as error:
                print(f"  harvest {project}: {error}", file=sys.stderr)
                continue
            found = match_jobs(targets[project], jobs)
            if not found:
                continue
            touched.add(project)
            harvested += len(found)
            if args.apply:
                result, new = register(found)
                harvest_created += new
                print(f"  {project}: {len(found)} render(s) matched, {new} new candidate(s) ({result})")
                if result != "ok":
                    outcome = result
        print(f"harvest: {harvested} render(s) matched to slots across {len(projects)} project(s), {harvest_created} new")
        candidates_total = len(candidates) + harvested
    else:
        candidates_total = len(candidates)

    if not args.apply:
        print(f"dry run: {candidates_total} candidate(s) would be sent (--apply sends)")
        return 0

    if args.dedupe:
        projects = sorted(p for p in touched if p and (not args.project or p in args.project))
        refs = rec.reference_numbers([ROOT, *([args.kind_robots] if args.kind_robots else [])])
        planned, removed = dedupe(projects, refs, apply=True)
        print(f"dedupe: {removed} duplicate render(s) moved to the Recycle Bin ({planned} planned)")
    return 0 if outcome == "ok" else 2

if __name__ == "__main__":
    sys.exit(main())
