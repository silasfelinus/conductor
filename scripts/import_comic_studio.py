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

# The locked eight-angle cast (comic-creator t-015, CAST-PICKS.md): entity, slot prefix, and per angle the picked
# ArtImage id (negative = shown mirrored). Each pick becomes a `selected` attempt on a `cast-*` slot, so the
# studio's Cast board opens on the approved designs instead of the round-2/3 brainstorm. The ArtJob behind each
# image is looked up in the issue ledgers, so a pick never needs a hand-copied job id.
ANGLES = [
    "front",
    "front-three-quarter-left",
    "profile-left",
    "back-three-quarter-left",
    "back",
    "back-three-quarter-right",
    "profile-right",
    "front-three-quarter-right",
]
CAST = [
    ("zuzu", "zuzu", "Zuzu", [242395, 242397, 242193, 242113, 242117, 242120, -242193, 242399]),
    ("siblings", "sister", "The sister", [242128, 242130, 242132, 242135, 242137, 242138, 242140, 242143]),
    ("siblings", "toddler", "The toddler", [242144, 242146, 242148, 242150, 242153, 242154, 242156, 242158]),
    ("coyote", "coyote", "The coyote", [242531, 242209, -242404, -242216, 242214, -242537, 242404, 242220]),
    ("otter-house", "abbess", "The abbess", [242559, -242513, -242561, 242515, 242356, 242520, 242521, -242524]),
]
CAST_EXTRA = [
    ("coyote", "coyote-stump-fresh", "The coyote: fresh stump (chapter 1, after the croc)", 242550),
    ("coyote", "coyote-stump-bandaged", "The coyote: stump bandaged by Zuzu", 242588),
]
CAST_ENTITIES = [
    ("coyote", "character", "The one-eyed coyote", "Destitute drifter, sick and underfed, never skeletal. Eyepatch on his RIGHT eye, revolver on his RIGHT hip. The croc takes his right (gun) hand in chapter 1; Zuzu bandages the stump and they part with their backs turned. Returns later as an ally.", None),
    ("croc", "creature", "The crocodile", "Erupts from the watering hole in chapter 1. Shadow, swell and teeth; never lingers.", None),
]


def image_index() -> dict:
    """ArtImage id -> (ArtJob id, ledger subject) across every ledger in the issue folder."""
    index = {}
    for path in sorted(ISSUE_DIR.glob("*.yaml")):
        try:
            ledger = yaml.safe_load(path.read_text())
        except yaml.YAMLError:
            continue
        if not isinstance(ledger, dict):
            continue
        for subject in ledger.get("subjects") or []:
            for lane_key, art in (subject.get("art") or {}).items():
                job_id = (subject.get("jobs") or {}).get(lane_key)
                if isinstance(art, dict) and art.get("art_image_id") and job_id:
                    index[int(art["art_image_id"])] = (int(job_id), subject)
    return index


def cast(index: dict):
    slots, attempts, missing = [], [], []
    used = {}

    def add(entity, key, title, image, notes, order):
        found = index.get(abs(image)) if image else None
        if found and found[0] in used:
            # An attempt row is unique per ArtJob, so a mirrored reuse points at the slot that holds it.
            notes = f"{notes} Same render as {used[found[0]]}."
            found = (None, found[1])
        tags = (found[1].get("prompt_tags") if found else None) or None
        slots.append(
            {
                "key": key,
                "entityKey": entity,
                "kind": "subject",
                "title": title,
                "notes": notes,
                "aspect": "2:3",
                "promptTags": tags,
                "promptProse": None if tags else (found[1].get("prompt_prose") if found else None),
                "useSeriesStyle": True,
                "sortOrder": order,
            }
        )
        if found and found[0]:
            used[found[0]] = key
            attempts.append({"slotKey": key, "artJobId": found[0], "verdict": "selected"})
        elif image and not found:
            missing.append(f"{key}: ArtImage {abs(image)} not in any ledger")

    order = -100
    for entity, prefix, name, picks in CAST:
        for angle, image in zip(ANGLES, picks):
            note = f"Locked pick ArtImage {abs(image)}" + (", shown mirrored." if image < 0 else ".") if image else "Pick pending."
            add(entity, f"cast-{prefix}-{angle}", f"{name}: {angle.replace('-', ' ')}", image, note, order)
            order += 1
    for entity, key, title, image in CAST_EXTRA:
        add(entity, f"cast-{key}", title, image, f"Locked pick ArtImage {image}.", order)
        order += 1
    return slots, attempts, missing


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
    slots_c, attempts_c, missing = cast(image_index())
    for line in missing:
        print(f"  cast: {line}", file=sys.stderr)
    script = read_text(ISSUE_DIR / "ISSUE-01-SCRIPT.md")
    entities = ENTITIES + CAST_ENTITIES
    return {
        "series": {
            "slug": "zuzu-koala-assassin",
            "title": "Zuzu, Koala Assassin",
            "notes": read_text(ISSUE_DIR / "BOOK-ONE.md") or read_text(ISSUE_DIR / "BRAINSTORM-ROUND-3.md"),
            "styleProse": "gritty inked western comic, anthropomorphic animals, dark atmosphere, high contrast, heavy shadows, muted earthy palette, desaturated, weathered, harsh low sunlight",
            "styleTags": "gritty, dark atmosphere, grindhouse, high contrast, heavy shadows, muted earthy palette, desaturated, weathered, grimy",
            "negativeTags": "nsfw, nude, suggestive, cleavage, revealing clothes, gore, lowres, worst quality, bad anatomy, bad hands, extra limbs, deformed, watermark, signature, blurry, jpeg artifacts, chibi, human, text",
        },
        "entities": [
            {"key": key, "kind": kind, "name": name, "notes": notes, "secretUntil": secret, "sortOrder": index}
            for index, (key, kind, name, notes, secret) in enumerate(entities)
        ],
        "slots": slots_c + slots3 + slots2,
        "attempts": attempts_c + attempts3 + attempts2,
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
