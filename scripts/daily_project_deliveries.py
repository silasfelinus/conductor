#!/usr/bin/env python3
"""Five evidenced daily additions to approved projects. Historical pitches stay intact."""
from __future__ import annotations
import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import yaml

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "projects/dream-cycle/daily-deliveries"
CUTOVER = "2026-10-13"
PR = re.compile(r"https://github\.com/[\w.-]+/[\w.-]+/pull/[1-9]\d*")
RUN = re.compile(r"https://github\.com/[\w.-]+/[\w.-]+/actions/runs/[1-9]\d*")
SHA = re.compile(r"[a-fA-F0-9]{40}")
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def today():
    return datetime.now(ZoneInfo("America/Los_Angeles")).date().isoformat()


def load(date):
    p = DIR / f"{date}.yaml"
    return yaml.safe_load(p.read_text(encoding="utf-8")) if p.exists() else None


def record_path(date, slug):
    return ROOT / "pitches" / f"{date}-{slug}.md"


def active_targets():
    p = ROOT / "project-overrides.yaml"
    if not p.exists():
        return {p.name for p in (ROOT / "projects").iterdir() if p.is_dir()}
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    entries = data.get("overrides", [])
    if isinstance(entries, dict):
        entries = [{"slug": k, **v} for k, v in entries.items()]
    return {e["slug"] for e in entries if isinstance(e, dict) and
            e.get("status") in ("active", "continuous") and e.get("slug")}


def validate(date, docket):
    if date < CUTOVER:
        return ["Delivery mode starts 2026-10-13 PT; historical pitches remain unchanged"]
    if not isinstance(docket, dict) or str(docket.get("date")) != date:
        return [f"{date}: missing docket or date mismatch"]
    entries = docket.get("entries")
    if not isinstance(entries, list) or len(entries) != 5:
        return [f"{date}: require exactly five real updates, never padded pitches"]
    errors, seen, active = [], set(), active_targets()
    for number, entry in enumerate(entries, 1):
        label = f"entry {number}"
        if not isinstance(entry, dict):
            errors.append(f"{label}: expected mapping")
            continue
        slug = str(entry.get("slug") or "")
        if not SLUG.fullmatch(slug) or slug in seen:
            errors.append(f"{label}: invalid or duplicate slug")
        seen.add(slug)
        if entry.get("target") not in active:
            errors.append(f"{label}: must target an existing active project")
        for field in ("title", "kind", "summary", "verification"):
            if len(str(entry.get(field) or "").strip()) < 5:
                errors.append(f"{label}: missing meaningful {field}")
        if len(str(entry.get("summary") or "").split()) < 8:
            errors.append(f"{label}: summary must describe a change, not an idea")
        if len(str(entry.get("verification") or "").split()) < 5:
            errors.append(f"{label}: verification must describe an actual check")
        if not PR.fullmatch(str(entry.get("pull_request") or "")):
            errors.append(f"{label}: missing real implementation PR URL")
        if not RUN.fullmatch(str(entry.get("checks_url") or "")):
            errors.append(f"{label}: missing actual GitHub Actions run URL")
        status = entry.get("status")
        if status not in ("shipped", "in-progress"):
            errors.append(f"{label}: status must be shipped or in-progress")
        if status == "shipped":
            if not SHA.fullmatch(str(entry.get("merge_sha") or "")) or entry.get("checks") != "passed":
                errors.append(f"{label}: shipped requires merge_sha and completed passing CI")
        if status == "in-progress" and len(str(entry.get("next_step") or "").split()) < 5:
            errors.append(f"{label}: in-progress needs a concrete next_step")
        art = entry.get("art")
        if not isinstance(art, dict) or art.get("status") not in (
            "delivered", "queued", "not-required", "blocked"
        ):
            errors.append(f"{label}: art.status must be delivered/queued/not-required/blocked")
        elif art["status"] == "delivered" and not str(art.get("url") or "").startswith("https://"):
            errors.append(f"{label}: delivered art requires a final asset URL")
        elif art["status"] == "queued" and not art.get("job_ids"):
            errors.append(f"{label}: queued art requires durable ArtJob IDs")
    return errors


def record_text(date, row):
    art = row["art"]
    evidence = [
        f"PR: {row['pull_request']}",
        f"Checks: {row['checks_url']}",
        f"Verified: {row['verification']}",
        f"Art: {art['status']}",
    ]
    for key, label in (("merge_sha", "Merge"), ("preview_url", "Playable preview")):
        if row.get(key):
            evidence.append(f"{label}: {row[key]}")
    if art.get("url"):
        evidence.append(f"Art URL: {art['url']}")
    if art.get("job_ids"):
        evidence.append(f"ArtJob IDs: {art['job_ids']}")
    if row.get("next_step"):
        evidence.append(f"Next step: {row['next_step']}")
    return (f"# Pitch: {row['title']}\n"
            f"date: {date}\n"
            f"project-target: {row['target']}\n"
            f"expansion-kind: {row['kind']}\n"
            f"delivery-status: {row['status']}\n"
            "status: awaiting-silas\n\n"
            "## Delivered change\n" + row["summary"].strip() + "\n\n"
            "## Evidence\n" + "\n".join(evidence) + "\n\n"
            "## Review after the work\n"
            "Approve = keep, approve with changes = revise, pass = request a scoped, "
            "CI-verified rollback. Rejections never directly delete production data.\n")


def materialize(date, docket):
    written = []
    for row in docket["entries"]:
        path = record_path(date, row["slug"])
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(record_text(date, row), encoding="utf-8")
            written.append(str(path.relative_to(ROOT)))
    return written


def decision(path):
    if not path.exists():
        return "pending"
    match = re.search(r"^status:\s*(\S+)", path.read_text(encoding="utf-8"), re.MULTILINE)
    result = match.group(1) if match else "awaiting-silas"
    return "pending" if result == "awaiting-silas" else result


def payload(date):
    docket = load(date)
    if validate(date, docket):
        return {"date": date, "entries": [], "missing": True}
    entries = []
    for row in docket["entries"]:
        entry = dict(row)
        entry["stem"] = f"{date}-{row['slug']}"
        entry["decision"] = decision(record_path(date, row["slug"]))
        entries.append(entry)
    return {"date": date, "entries": entries, "missing": False}


def feedback():
    work = []
    for path in sorted(DIR.glob("????-??-??.yaml")):
        docket = load(path.stem)
        if validate(path.stem, docket):
            continue
        for row in docket["entries"]:
            review = record_path(path.stem, row["slug"])
            if not review.exists():
                continue
            raw = review.read_text(encoding="utf-8")
            state = decision(review)
            notes = raw.split("## Silas's modifications", 1)
            if state == "rejected":
                work.append(f"{review.relative_to(ROOT)}: REJECTED {row['pull_request']}; "
                            "file a narrowly scoped tested rollback PR; preserve unrelated work")
            elif state == "approved" and len(notes) > 1 and notes[1].strip():
                work.append(f"{review.relative_to(ROOT)}: MODIFY {row['target']}: {notes[1].strip()}")
    return work


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=today())
    actions = parser.add_mutually_exclusive_group(required=True)
    for name in ("brief", "check", "materialize", "payload", "feedback"):
        actions.add_argument("--" + name, action="store_true")
    args = parser.parse_args()
    if args.brief:
        print(f"Write projects/dream-cycle/daily-deliveries/{args.date}.yaml with date and five entries.")
        print("Implement before recording: claim work; open PRs, verify actual CI; merge safe reversible "
              "changes when green. Each entry: slug, title, target, kind, summary (>=8 words), "
              "status (shipped|in-progress), pull_request, checks_url, verification, art: {status, "
              "url/job_ids}, and preview_url where available. Shipped: merge_sha, checks: passed. "
              "In-progress: next_step. Prefer five shipped; never mislabel progress as finished.")
        print("Then --materialize and --check; deliver using the existing signed review inbox. "
              "Use --feedback to pick up user modification and rollback requests.")
        return 0
    if args.feedback:
        print("\n".join(feedback()) or "No delivery feedback requiring agent work.")
        return 0
    if args.payload:
        print(json.dumps(payload(args.date)))
        return 0
    docket = load(args.date)
    errors = validate(args.date, docket)
    if not errors and args.check:
        errors = [f"{row['slug']} missing review record (run --materialize)"
                  for row in docket["entries"] if not record_path(args.date, row["slug"]).exists()]
    if errors:
        print("\n".join(errors))
        return 1
    if args.materialize:
        print("Materialized: " + ", ".join(materialize(args.date, docket)))
    else:
        print(f"{args.date}: five evidenced deliveries and review records are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
