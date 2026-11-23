#!/usr/bin/env python3
"""Read-only per-ArtImage summary of checkpointed private game-art media proof.

The YAML ledger preserves source media receipts; an Actions log adds the
authenticated gameplay URL and anonymous/privacy outcome. A missing runtime
check stays UNKNOWN, not verified. This script never fetches media, enqueues a
job, changes a ledger, or prints a private URL or bearer credential.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml


TOKEN = re.compile(r"([a-z_]+)=([A-Za-z0-9._/-]+)")
GAME_EVENT = re.compile(r"\b(GAME_PATH_OK|GAME_PATH_FAILED|VERIFIED|FAILED)\s")
PRIVATE_EVENT = re.compile(r"\bPRIVATE_POLICY_(VERIFIED|FAILED)(?:=([0-9]+))?\s+ledger=([A-Za-z0-9._-]+)")
SAFE_REASON = re.compile(r"^[A-Za-z]+(?:Error|Exception)$")
STATUS = ("verified", "failed", "unknown")


def checkpointed_receipts(ledgers):
    """Keep stable ArtImage/ArtJob identities and source-checkpoint status."""
    rows = {}
    for ledger in ledgers:
        document = yaml.safe_load(Path(ledger).read_text(encoding="utf-8")) or {}
        privacy = document.get("is_public") is False
        for subject in document.get("subjects") or []:
            key = subject.get("key")
            lane = subject.get("lane")
            if not isinstance(key, str) or not isinstance(lane, str):
                continue
            job = (subject.get("jobs") or {}).get(lane)
            art = (subject.get("art") or {}).get(lane) or {}
            image = art.get("art_image_id")
            if type(job) is not int or type(image) is not int:
                continue
            if job <= 0 or image <= 0 or art.get("status") not in ("DONE", "ACCEPTED"):
                continue
            proof = (subject.get("media_proof") or {}).get(lane) or {}
            proof_matches = (
                proof.get("art_job_id") == job
                and proof.get("art_image_id") == image
            )
            source = (
                "verified" if proof_matches and proof.get("status") == "VERIFIED"
                else "failed" if proof_matches and proof.get("status") == "FAILED"
                else "unknown"
            )
            if image in rows:
                raise ValueError("An ArtImage ID is reused by multiple art receipts")
            rows[image] = {
                "key": key,
                "job_id": job,
                "image_id": image,
                "ledger": Path(ledger).name,
                "private_requested": privacy,
                "source": source,
                "runtime": "unknown",
                "private": "unknown",
                "reason": "",
            }
    return rows


def apply_log(rows, log_text):
    """Join only exact whitelisted keys/ArtImages from the current Actions log."""
    by_key = {(row["key"], row["image_id"]): row for row in rows.values()}
    private_groups = {}
    for line in log_text.splitlines():
        match = GAME_EVENT.search(line)
        if match:
            kind = match.group(1)
            attrs = dict(TOKEN.findall(line[match.start():]))
            try:
                image = int(attrs.get("image", "-1"))
            except ValueError:
                continue
            row = by_key.get((attrs.get("key"), image))
            if row is None:
                continue
            if kind in ("VERIFIED", "FAILED"):
                row["source"] = "verified" if kind == "VERIFIED" else "failed"
            elif kind == "GAME_PATH_OK":
                if attrs.get("job") != str(row["job_id"]):
                    continue
                row["runtime"] = "verified"
                if row["private_requested"]:
                    row["private"] = (
                        "verified" if attrs.get("anonymous") == "PRIVATE_DENIED"
                        else "failed"
                    )
            else:
                row["runtime"] = "failed"
                raw_reason = attrs.get("reason", "")
                row["reason"] = (
                    raw_reason if SAFE_REASON.fullmatch(raw_reason)
                    else "RuntimeCheckFailed"
                )
        private_event = PRIVATE_EVENT.search(line)
        if private_event:
            _, count, ledger = private_event.groups()
            if private_event.group(1) == "VERIFIED" and count:
                private_groups[ledger] = int(count)
            elif private_event.group(1) == "FAILED":
                private_groups[ledger] = -1
    for ledger, count in private_groups.items():
        group = [row for row in rows.values() if row["ledger"] == ledger]
        if count == len(group) and group and all(
            row["runtime"] == "verified" and row["private_requested"]
            for row in group
        ):
            for row in group:
                row["private"] = "verified"
        elif count == -1:
            for row in group:
                if row["private"] != "failed":
                    row["private"] = "unknown"
    return rows


def summarize(rows):
    ordered = sorted(rows.values(), key=lambda row: (row["ledger"], row["key"]))
    counts = {
        phase: {status: sum(row[phase] == status for row in ordered) for status in STATUS}
        for phase in ("source", "runtime", "private")
    }
    return {"total": len(ordered), "counts": counts, "rows": ordered}


def formatted_report(report, *, all_rows=False):
    counts = report["counts"]
    lines = [
        "PROM_TACTICS_ART_IMAGES=" + str(report["total"]),
        *(
            f"{phase.upper()}_{status.upper()}={counts[phase][status]}"
            for phase in ("source", "runtime", "private")
            for status in STATUS
        ),
    ]
    for row in report["rows"]:
        if not all_rows and all(row[field] == "verified" for field in ("source", "runtime", "private")):
            continue
        if not all_rows and all(row[field] in ("verified", "unknown") for field in ("source", "runtime", "private")):
            continue
        lines.append(
            f"ART_IMAGE_PROOF image={row['image_id']} job={row['job_id']} "
            f"key={row['key']} source={row['source']} runtime={row['runtime']} "
            f"private={row['private']} reason={row['reason'] or 'none'}"
        )
    return "\n".join(lines)


def markdown_report(report):
    counts = report["counts"]
    lines = [
        "## Prom and Tactics private ArtImage delivery proof",
        "",
        f"**{report['total']}** recorded DONE/ACCEPTED ArtImages; "
        f"**{counts['source']['verified']}** source-verified, "
        f"**{counts['runtime']['verified']}** authenticated game-path verified, "
        f"**{counts['private']['verified']}** private-access verified.",
        "",
        "UNKNOWN means the current workflow did not complete that check, not that art was approved or delivered.",
        "",
        "| ArtImage | Key | Source | Game URL | Privacy | Failure type |",
        "| ---: | --- | --- | --- | --- | --- |",
    ]
    failing = [
        row for row in report["rows"]
        if any(row[field] == "failed" for field in ("source", "runtime", "private"))
    ]
    for row in failing:
        lines.append(
            f"| {row['image_id']} | {row['key']} | {row['source']} | "
            f"{row['runtime']} | {row['private']} | {row['reason'] or '-'} |"
        )
    if not failing:
        lines.append("| - | No explicit failures recorded | - | - | - | - |")
    lines.extend(["", "Recorded receipts do not certify composition review, character canon or gameplay attachment."])
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, action="append", required=True)
    parser.add_argument("--log", type=Path, action="append", default=[])
    parser.add_argument("--summary", type=Path)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args(argv)
    rows = checkpointed_receipts(args.ledger)
    for path in args.log:
        if path.is_file():
            apply_log(rows, path.read_text(encoding="utf-8", errors="replace"))
    report = summarize(rows)
    print(formatted_report(report))
    if args.summary:
        with args.summary.open("a", encoding="utf-8") as output:
            output.write(markdown_report(report))
    if args.json:
        args.json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
