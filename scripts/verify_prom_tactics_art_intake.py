#!/usr/bin/env python3
"""Distinguish requested art from real accepted ArtJobs and finished ArtImages."""
from __future__ import annotations

import argparse
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
LEDGERS = {
    "Tactics one-hit telegraphs": (
        Path("projects/every-villain-tactics/art/ONE-HIT-CREW-TELEGRAPHS-2026-11-20.yaml"),
        12,
    ),
    "Prom October cast": (
        Path("projects/comet-city-academy/art/OCT-29-CAST-KREA2-ROUND-1.yaml"),
        24,
    ),
}


def verify(require_jobs: bool = False) -> bool:
    all_complete = True
    for label, (relative_path, expected) in LEDGERS.items():
        data = yaml.safe_load((ROOT / relative_path).read_text(encoding="utf-8"))
        assert data["project_slug"] in {"every-villain-tactics", "comet-city-academy"}
        assert data["is_public"] is False and data["auto_submit"] is True
        subjects = data["subjects"]
        assert len(subjects) == expected, (label, len(subjects), expected)
        assert len({s["key"] for s in subjects}) == expected
        assert len({s["asset"] for s in subjects}) == expected
        accepted = []
        rendered = []
        missing = []
        for row in subjects:
            job_id = (row.get("jobs") or {}).get("krea2")
            art = (row.get("art") or {}).get("krea2") or {}
            if isinstance(job_id, int) and job_id > 0:
                accepted.append((row["key"], job_id))
                if art.get("status") == "DONE" and isinstance(art.get("art_image_id"), int):
                    rendered.append(row["key"])
            else:
                missing.append(row["key"])
        print(
            f"{label}: REQUESTED={expected} ACCEPTED={len(accepted)} "
            f"DONE_WITH_ARTIMAGE={len(rendered)} MISSING_JOB_IDS={len(missing)}"
        )
        if accepted:
            print("  Accepted ArtJobs:", ", ".join(f"{key}={id}" for key, id in accepted))
        if missing:
            print("  Missing:", ", ".join(missing))
            all_complete = False
    return all_complete or not require_jobs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-jobs", action="store_true")
    args = parser.parse_args()
    try:
        return 0 if verify(args.require_jobs) else 1
    except (KeyError, TypeError, ValueError, AssertionError) as exc:
        print(f"Art intake contract failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
