#!/usr/bin/env python3
"""Queue the subject-first Western Cartoon re-render (Shifting Desks round 18).

Silas, 2026-11-02: "re-render western cartoon with subject-first prompts",
after "that is not a cockroach" on The Union Walkthrough. The first Western
Cartoon pass led every prompt with ~70 tokens of quality and style tags
(including "polished expressive character designs ... inviting character
warmth"), so Arthemy drew one centered antennaed woman or cat-person in an
arched doorway for most cards, whatever the card was about.

This rebuilds every STYLE-CATALOG subject's Western Cartoon row:
  * the body is the game's own art_prompt (kind_robots utils/shiftingDesks,
    falling back to the catalog), with the Classic-only style words removed
    so the subject is the first thing the model reads;
  * cards about the Roach Union lead with explicit insect tags;
  * a per-row negative bans the portrait template it fell into;
  * rows are force re-renders at the same image paths, so Kind Robots needs
    no path change. compose_checkpoint_prompt appends the lane style and the
    quality tags after the subject (SUBJECT_FIRST_LANES).

Writes the rows into projects/art-prompts.yaml requests and a ROUND-18.yaml
ledger for review. Re-running replaces this round's rows, never duplicates.

  python projects/shifting-desks/art/queue_western_cartoon_rerender.py          # dry run
  python projects/shifting-desks/art/queue_western_cartoon_rerender.py --write
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
ART = ROOT / "projects" / "shifting-desks" / "art"
QUEUE = ROOT / "projects" / "art-prompts.yaml"
KR_DATA = ROOT.parent / "kind_robots" / "utils" / "shiftingDesks"
MEDIA = "https://media.acrocatranch.com"
ROUND = "shifting-desks-18"
ID_PREFIX = "shifting-desks-style-v2-western-cartoon-subject-first-"
SEED_BASE = 72000

LEAD_IN = re.compile(
    r"^(?:an? )?mid-century (?:corporate )?safety-manual illustration(?: of)?\s*",
    re.IGNORECASE,
)
CLASSIC_PALETTE = re.compile(
    r"(?:limited )?palette of manila, carbon-paper blue, safety orange, "
    r"fluorescent-tube green and oxblood",
    re.IGNORECASE,
)
# Clauses that only describe the Classic edition's look.
CLASSIC_CLAUSE = re.compile(
    r"mid-century|safety-manual|screen-printed|gouache|halftone|palette\b|"
    r"\bcomposition\b|bare and unmarked|\bgrain\b",
    re.IGNORECASE,
)
ROACH = re.compile(r"\broach|cockroach", re.IGNORECASE)
ROACH_LEAD = "(cockroach:1.3), insect, glossy brown chitin shell, six jointed legs, long antennae"
# Danbooru names the failure itself: "insect girl" / "monster girl". Human
# faces stay allowed, since most roach cards also show a human worker.
ROACH_NEGATIVE = "insect girl, monster girl, humanoid insect, antennae on a human, mantis, robot"
BASE_NEGATIVE = (
    "low quality, blurry, bad anatomy, disfigured, writing, text, letters, words, "
    "watermark, logo, signature, nudity, nsfw, animal ears, kemonomimi, cat girl, "
    "fox girl, furry, centered character portrait, simple background, arched doorway, "
    "arched window, collage, multiple panels"
)


def kind_robots_prompts() -> dict[str, str]:
    prompts: dict[str, str] = {}

    def walk(node):
        if isinstance(node, dict):
            if node.get("id") and isinstance(node.get("art_prompt"), str):
                prompts.setdefault(node["id"], node["art_prompt"])
            epilogue = node.get("epilogue")
            if node.get("id") and isinstance(epilogue, dict) and epilogue.get("art_prompt"):
                prompts.setdefault(node["id"], epilogue["art_prompt"])
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    for path in sorted(KR_DATA.glob("*.json")):
        walk(json.loads(path.read_text()))
    return prompts


def subject_first(prompt: str) -> str:
    body = " ".join(prompt.split())
    body = CLASSIC_PALETTE.sub("", body)
    body = LEAD_IN.sub("", body)
    clauses = [c.strip() for c in body.split(",")]
    kept = [c for c in clauses if c and not CLASSIC_CLAUSE.search(c)]
    body = ", ".join(kept).strip(" ,.")
    return body[:1].lower() + body[1:] if body[:2].lower() in ("a ", "an") else body


def negative_for(body: str) -> str:
    parts = BASE_NEGATIVE.split(", ")
    if re.search(r"\barch", body, re.IGNORECASE):
        parts = [p for p in parts if not p.startswith("arched")]
    if re.search(r"\b(cat|fox|dog|rabbit|bunny|bear|animal)s?\b", body, re.IGNORECASE):
        parts = [p for p in parts if p != "furry"]
    if ROACH.search(body):
        parts.append(ROACH_NEGATIVE)
    return ", ".join(parts)


def build_rows() -> tuple[list[dict], list[dict]]:
    catalog = json.loads((ART / "STYLE-CATALOG.json").read_text())
    live = kind_robots_prompts()
    rows, ledger = [], []
    for index, subject in enumerate(catalog["subjects"], start=1):
        source = live.get(subject["id"]) or subject["prompt"]
        body = subject_first(source)
        if ROACH.search(body):
            body = f"{ROACH_LEAD}, {body}"
        relative = subject["classicImage"][len("/images/shifting-desks/"):]
        image_path = f"public/images/shifting-desks/styles/western-cartoon/{relative}"
        landscape = "horizontal" in source.lower()
        request_id = f"{ID_PREFIX}{subject['kind']}-{subject['id']}"
        row = {
            "id": request_id,
            "source": "shifting-desks",
            "status": "pending",
            "force": True,
            "target_repo": "silasfelinus/kind_robots",
            "project_slug": "shifting-desks",
            "project_target": "shifting-desks",
            "image_path": image_path,
            "source_url": f"{MEDIA}/{image_path[len('public/'):]}",
            "page_url": "https://kindrobots.org/play/shifting-desks",
            "variant": "image",
            "engine": "sdxl-checkpoint",
            "checkpoint_family": "western-cartoon",
            "size": "1152x864" if landscape else "832x1248",
            "seed": SEED_BASE + index,
            "priority": 10,
            "label": f"Shifting Desks Western Cartoon (subject first) - {subject['title']}",
            "prompt": body,
            "negative_prompt": negative_for(body),
        }
        rows.append(row)
        ledger.append({
            "key": f"{subject['kind']}-{subject['id']}",
            "kind": subject["kind"],
            "title": subject["title"],
            "request_id": request_id,
            "roach": bool(ROACH.search(body)),
            "target_path": f"kind_robots {image_path}",
            "media_url": row["source_url"],
            "prompt": body,
            "status": "requested",
            "verdict": None,
        })
    return rows, ledger


def write_queue(rows: list[dict]) -> int:
    text = QUEUE.read_text()
    data = yaml.safe_load(text)
    targets = {row["image_path"] for row in rows}
    stale = [
        e for e in data["requests"]
        if e.get("id", "").startswith(ID_PREFIX)
        or (e.get("image_path") in targets and e.get("status") == "pending")
    ]
    # Drop stale rows textually so the rest of the hand-kept file is untouched.
    lines = text.splitlines(keepends=True)
    starts = [i for i, line in enumerate(lines) if line.startswith("- id:")]
    drop_ids = {e["id"] for e in stale}
    keep: list[str] = []
    bounds = starts + [len(lines)]
    keep.extend(lines[: starts[0]] if starts else lines)
    for begin, end in zip(bounds, bounds[1:]):
        item_id = yaml.safe_load(lines[begin][2:])["id"]
        if item_id not in drop_ids:
            keep.extend(lines[begin:end])
    body = "".join(keep)
    if not body.endswith("\n"):
        body += "\n"
    body += yaml.safe_dump(rows, sort_keys=False, allow_unicode=True, width=10_000)
    QUEUE.write_text(body)
    return len(stale)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    if not KR_DATA.is_dir():
        print(f"missing {KR_DATA}; check out kind_robots beside conductor", file=sys.stderr)
        return 2
    rows, ledger = build_rows()
    roach = sum(1 for item in ledger if item["roach"])
    print(f"{len(rows)} Western Cartoon rows ({roach} Roach Union subjects)")
    if not args.write:
        for row in rows[:3]:
            print(f"- {row['id']}\n  {row['prompt'][:160]}")
        return 0
    removed = write_queue(rows)
    header = (
        f"# Shifting Desks art round 18 (2026-11-02 PT): subject-first Western Cartoon re-render.\n"
        f"# Built by queue_western_cartoon_rerender.py. Every row is a forced re-render at its\n"
        f"# existing styles/western-cartoon path. Review each render against its prompt, set\n"
        f"# verdict keep/redo, and only then lift kind_robots WITHDRAWN_RENDERS for the roach cards.\n"
    )
    ledger_doc = {
        "round": ROUND,
        "project_slug": "shifting-desks",
        "queue": "projects/art-prompts.yaml requests",
        "requested_at": "2026-11-02",
        "checkpoint": "Illustrious/arthemyWesternArt_v30.safetensors",
        "subjects": ledger,
    }
    (ART / "ROUND-18.yaml").write_text(
        header + yaml.safe_dump(ledger_doc, sort_keys=False, allow_unicode=True, width=110)
    )
    print(f"wrote {len(rows)} rows (replaced {removed}) and ROUND-18.yaml")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
