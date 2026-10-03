#!/usr/bin/env python3
"""Seed the Kind Robots Comic Studio with the Zuzu brainstorm (comic-creator/t-013).

The studio's database is the source of truth once seeded; this script only posts
the Conductor ledgers to POST /api/comics/import, which is fill-only and safe to
re-run (existing rows and studio edits are never overwritten).

What it sends:
  series   notes = BRAINSTORM-ROUND-3.md (the current direction, which the
           adversarial editor holds every idea to); the v0 script becomes
           Issue 1's notes behind a superseded banner.
  entities Zuzu, the fennec siblings, Old Komodo, the three factions, thin
           reality, the buried human twist (marked secret), covers, plot seeds.
  slots    the 12 round-3 subjects (ART-ROUND-3.yaml) and the 50 round-2
           brainstorm prompts (COMFY-PROMPTS-BRAINSTORM.yaml).
  attempts every ArtJob from both rounds. Round-2 job ids are pinned in
           ART-ROUND-2-JOBS.yaml and carry expectRequestId, so the server
           checks each job's own request id before importing it.

Usage:
    python scripts/import_comic_studio.py            # dry run: print counts
    python scripts/import_comic_studio.py --live     # post to Kind Robots
Environment: KR_API_TOKEN (for --live), KR_BASE_URL.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

try:
    from scripts import consume_art_queue_core as core
except ImportError:  # pragma: no cover - direct script execution
    import consume_art_queue_core as core

ROOT = Path(__file__).resolve().parent.parent
ISSUE_DIR = ROOT / "projects" / "comic-creator" / "issues" / "zuzu-koala-assassin-01"
REQUEST_PREFIX = "zuzu-koala-assassin-01/"

SIZE_TO_ASPECT = {"1216x832": "3:2", "1344x768": "16:9", "832x1216": "2:3", "1024x1024": "1:1"}

ENTITIES = [
    ("zuzu", "character", "Zuzu", "Koala ronin, always serious: Clint Eastwood stillness, not a sensei. A samurai in a weird western, a fish out of water.", None),
    ("siblings", "character", "The fennec siblings", "Older sister (about ten) and toddler brother who only babbles. Sole survivors of the Hollow Bell massacre: poor, starving, beaten, scared, alone.", None),
    ("old-komodo", "creature", "Old Komodo", "Shock appearance from under the sand. Not really a villain, but he tries to eat the siblings before Zuzu intercedes with a staff.", None),
    ("storm-crows", "faction", "Storm Crows", "Raiders out of the storms. Undeveloped: a name and a first image.", None),
    ("hyena-tribe", "faction", "Hyena tribe", "Slavers in the first plot seed: the otter sisters plan to sell the children to them.", None),
    ("otter-house", "faction", "The otter house", "A convent of otter 'sisters' with a respectable face (and possibly a bordello/geisha house behind it). Zuzu leaves the kids there; they plan to sell them to the hyenas; he goes back.", None),
    ("thin-reality", "creature", "Thin reality", "The fabric of reality is weak. Monsters step through from elsewhere, Conan style (the dinosaur-like dragon of Red Nails). Never explained.", None),
    ("human-ruins", "twist", "There were humans", "Planet of the Apes reveal at an issue ending: a fallen statue and a half-buried PHARMACY sign, or the Great Wall in the dunes. The wasteland used to be prosperous.", "a chosen issue ending"),
    ("covers", "cover", "Covers", "Cover concepts, including Zuzu fighting the giant sand monster.", None),
    ("plot-seeds", "plot", "Plot seeds", "Cover-aimed plot ideas from round 2. Brainstorm, not canon.", None),
    ("species-tests", "other", "Sibling species tests", "Round 2 tried twenty species for the siblings. Silas chose fennec foxes.", None),
]

ROUND2_ENTITY = {"zuzu": "zuzu", "covers": "covers", "plots": "plot-seeds", "kids": "species-tests"}


def read_text(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def round3(ledger: dict):
    slots, attempts = [], []
    for index, subject in enumerate(ledger.get("subjects") or []):
        slots.append(
            {
                "key": subject["key"],
                "entityKey": subject.get("entity"),
                "kind": "subject",
                "title": subject["title"],
                "aspect": SIZE_TO_ASPECT.get(str(subject.get("size")), "1:1"),
                "promptProse": subject.get("prompt_prose"),
                "promptTags": subject.get("prompt_tags"),
                "negativePrompt": subject.get("negative"),
                "useSeriesStyle": False,
                "sortOrder": index,
            }
        )
        for lane_key, job_id in (subject.get("jobs") or {}).items():
            if job_id:
                attempts.append({"slotKey": subject["key"], "laneKey": lane_key, "artJobId": int(job_id)})
    return slots, attempts


def round2(prompts: list, job_by_prompt: dict):
    slots, attempts = [], []
    for index, prompt in enumerate(prompts):
        entity = ROUND2_ENTITY.get(prompt.get("group"), "plot-seeds")
        if prompt["id"] == "kid-08-fennec":
            entity = "siblings"
        if prompt["id"] == "cover-01-sand-monster":
            entity = "old-komodo"
        key = f"r2-{prompt['id']}"
        slots.append(
            {
                "key": key,
                "entityKey": entity,
                "kind": "cover" if prompt.get("group") == "covers" else "subject",
                "title": prompt.get("title") or prompt["id"],
                "notes": prompt.get("pitch"),
                "aspect": prompt.get("aspect") or "1:1",
                "promptProse": prompt.get("prompt"),
                "useSeriesStyle": False,
                "sortOrder": 100 + index,
            }
        )
        job_id = job_by_prompt.get(prompt["id"])
        if job_id:
            attempts.append(
                {
                    "slotKey": key,
                    "laneKey": "krea2",
                    "artJobId": int(job_id),
                    "expectRequestId": REQUEST_PREFIX + prompt["id"],
                    "verdict": "liked" if prompt["id"] == "kid-08-fennec" else "none",
                }
            )
    return slots, attempts


def build_payload() -> dict:
    ledger3 = yaml.safe_load((ISSUE_DIR / "ART-ROUND-3.yaml").read_text()) or {}
    prompts2 = (yaml.safe_load((ISSUE_DIR / "COMFY-PROMPTS-BRAINSTORM.yaml").read_text()) or {}).get("prompts") or []
    jobs2 = (yaml.safe_load((ISSUE_DIR / "ART-ROUND-2-JOBS.yaml").read_text()) or {}).get("jobs") or {}
    slots3, attempts3 = round3(ledger3)
    slots2, attempts2 = round2(prompts2, jobs2)
    script = read_text(ISSUE_DIR / "ISSUE-01-SCRIPT.md")
    return {
        "series": {
            "slug": "zuzu-koala-assassin",
            "title": "Zuzu, Koala Assassin",
            "notes": read_text(ISSUE_DIR / "BRAINSTORM-ROUND-3.md"),
            "styleProse": "gritty painted comic illustration, realistic anthropomorphic animals with true fur and weight, heavy ink shadows, dusty ochre and burnt umber palette, harsh low sunlight",
            "negativeTags": "nsfw, nude, suggestive, cleavage, revealing clothes, gore, lowres, worst quality, bad anatomy, bad hands, extra limbs, deformed, watermark, signature, blurry, jpeg artifacts, chibi, human, text",
        },
        "entities": [
            {"key": key, "kind": kind, "name": name, "notes": notes, "secretUntil": secret, "sortOrder": index}
            for index, (key, kind, name, notes, secret) in enumerate(ENTITIES)
        ],
        "slots": slots3 + slots2,
        "attempts": attempts3 + attempts2,
        "issueNotes": script,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args(argv)
    payload = build_payload()
    print(
        f"{len(payload['entities'])} entities, {len(payload['slots'])} slots, "
        f"{len(payload['attempts'])} attempts via {core.KR_BASE_URL}/api/comics/import"
    )
    if not args.live:
        return 0
    if not core.KR_API_TOKEN:
        print("KR_API_TOKEN is required for --live.", file=sys.stderr)
        return 1
    status, resp = core.http_json("POST", f"{core.KR_BASE_URL}/api/comics/import", payload, timeout=300)
    print(f"HTTP {status}: {(resp or {}).get('message') if isinstance(resp, dict) else resp}")
    data = (resp or {}).get("data") if isinstance(resp, dict) else None
    if isinstance(data, dict):
        for line in (data.get("errors") or [])[:30]:
            print(f"  error: {line}")
        print(json.dumps({"created": data.get("created"), "skipped": len(data.get("skipped") or [])}))
    return 0 if status in (200, 201, 207) else 1


if __name__ == "__main__":
    sys.exit(main())
