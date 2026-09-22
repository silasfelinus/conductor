#!/usr/bin/env python3
"""
check_facet_prompt_subjects.py — Flag a live Facet whose artPrompt never names
anything drawable, so a bad cohort is caught from the reading end instead of
from the picture.

2026-09-20. The negation-repair pass reported a clean live audit -- 0 violations
across 4,442 prompts -- and the pictures it was producing were garbage. Silas,
looking at the Facet cards it had just rendered: "what the hell is with the
facets that have recently been generated? Octopus, ocelot, axolotl? The prompts
make no sense and the images reflect that", and on the alignment cards, "coming
up with plain images and text, which is a real no no".

Both cohorts passed every rule in server/utils/artPromptContract.ts, because
they contained no negation, no conditional and no jargon. That is ART-PROMPTS.md
rule 5 with the last word taken off: a green contract means the last bug is
gone, never that the prompt is good. What those 149 prompts actually were is the
Facet's DESCRIPTION pasted whole -- the card copy, which is written as a joke --
plus a generic taxonomy clause, and the Facet's own title nowhere in it. Facet
290 "Octopus" read "Three hearts, nine brains, infinite arms. Has been something
else so long they forgot which one they started as." and rendered a plush blob
with three hearts. Facet 235 "Transactional" rendered a wall of garbled text.

So this checks the one thing the contract structurally cannot: not whether a
prompt breaks a rule, but whether it says what to draw.

Three findings, in descending confidence:

  NO SUBJECT: the Facet's own title appears nowhere in its artPrompt AND the
  prompt is producer-generated (it carries one of the registered taxonomy
  clauses). A hand-authored prompt that names a concrete scene without
  repeating the title is CORRECT and is not flagged -- "A row of identical
  blank-eyed figures on a conveyor line" is exactly right for a Facet called
  "Batch-Made". The generated-clause test is what separates the two.

  APP WRAPPER: the prompt carries application context -- the product name, the
  builder it belongs to, or the catalog group as a label ("Kind Robots premium
  Builder illustration for Reward Types: Magic"). Krea paints those as the
  title text of the card it decides it is drawing.

  CARD COPY: the prompt begins with the Facet's description verbatim. On its
  own that is only a smell, so it is reported at a lower level than the two
  above and never alone decides the exit code.

Needs KR_API_TOKEN; exits 2 (unresolved, not clean) without it, matching
check_project_scaffold_drift.py and check_live_facet_coverage.py.

Usage:
  python scripts/check_facet_prompt_subjects.py
  python scripts/check_facet_prompt_subjects.py --json
  python scripts/check_facet_prompt_subjects.py --limit 20

Exit codes: 0 = clean, 1 = at least one NO SUBJECT or APP WRAPPER finding,
2 = unresolved (no token, or the catalog could not be read). Advisory: a
non-zero exit is a prompt to go look at the cards, not a gate.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

KR_BASE_URL = os.environ.get("KR_BASE_URL", "https://kindrobots.org").rstrip("/")
KR_API_TOKEN = os.environ.get("KR_API_TOKEN", "")
PAGE = 250

# Every clause the Facet art producer has appended to a generated prompt, in
# every shape that has reached the live catalog. Kept in step with
# GENERATED_PROMPT_TAILS in kind_robots/scripts/generate_facet_art_v4.ts --
# including the two entries that only exist because a repair pass truncated a
# registered tail, which is what de-registered 147 Facets in the first place.
GENERATED_CLAUSES = (
    "One unmistakable full creature, recognizable anatomy, distinctive personality, habitat cues.",
    "Show one unmistakable full creature with recognizable anatomy, personality, and habitat cues.",
    "Iconic scene, concrete focal subject, environment, action, strong atmosphere.",
    "Character-centered visual metaphor, clear emotion through pose, expression, costume, and environment.",
    "Use a character-centered visual metaphor with a clear emotional read.",
    "Unmistakable palette or material behavior through lighting, texture, and a strong central form.",
    "Polished sample of the visual treatment, coherent medium, linework, palette, lighting, and surface detail.",
    "Single distinctive figure in action, readable tools",
    "Premium collectible object or emblem, rarity expressed through materials and lighting, clean silhouette.",
    "Create a premium collectible emblem or object with a strong rarity read",
    "Single clear subject or emblem, immediately",
    "Use a single clear subject or emblem that makes the concept understandable at thumbnail size.",
    "The whole animal head to tail, its markings and proportions true to the species, alert in the habitat it lives in.",
    "The whole subject shown in full, its form and proportions true to what it is, in the place it belongs.",
    "A scene of this kind underway, everyone in it and the place around them painted together, the light and the weather carrying its mood.",
    "The place itself, wide and lived-in, its architecture and ground and sky and weather doing the work.",
    "One person seen from head to shoes, doing something only someone like this would do, in a place that belongs to them, the feeling carried in the face and the posture.",
    "A person at full height doing something only someone like this would do",
    "A person at full height in the middle of this work",
    "A single large form filling the frame, made of this, lit so the colour and the surface behave the way they really do.",
    # v7 (2026-09-21): "frame" -> "picture" in the two clauses that carried it.
    # Krea paints "frame" as a physical picture frame whichever sense is meant
    # (ArtJobs 30116/30117), so kind_robots' artPromptContract.ts now rejects it.
    # Both spellings stay registered here for the same reason GENERATED_PROMPT_TAILS
    # keeps its old entries: a clause this list does not know about is a cohort
    # whose prompts read as hand-authored and are never reported.
    "A single large form filling the picture, made of this, lit so the colour and the surface behave the way they really do.",
    "One clear subject alone in the picture, large and plainly lit.",
    "A finished picture made this way, the medium and the linework and the palette and the lighting all plainly visible in it.",
    "One person seen from head to shoes, their face turned toward the light, standing in the place where they do this.",
    "A single treasured object resting alone, its materials and the light around it telling you how rare it is.",
    "One clear subject alone in the frame, large and plainly lit.",
)

APP_WRAPPERS = (
    re.compile(r"\bIllustrate the Facet concept\b", re.I),
    re.compile(r"\bCreate (?:this as|a) [^.\n]{0,160}\bfor Kind Robots\b", re.I),
    re.compile(r"\bKind Robots\b[^.\n]{0,80}\billustration for\b", re.I),
    re.compile(r"\b(?:Bot|Reward|Dream|Facet|Rarity|Character)\s+Type[s]?\s+card\b", re.I),
)


def http_get(path: str) -> dict:
    request = urllib.request.Request(
        f"{KR_BASE_URL}{path}",
        headers={"Authorization": f"Bearer {KR_API_TOKEN}"},
    )
    with urllib.request.urlopen(request, timeout=90) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_facets() -> list[dict]:
    rows: dict[int, dict] = {}
    skip = 0
    while True:
        payload = http_get(f"/api/facets?take={PAGE}&skip={skip}&includeInactive=true")
        batch = payload.get("data") or []
        if isinstance(batch, dict):
            batch = batch.get("facets") or batch.get("items") or []
        if not batch:
            break
        fresh = 0
        for row in batch:
            if row.get("id") not in rows:
                rows[row["id"]] = row
                fresh += 1
        # /api/facets caps `take` and has historically ignored `skip` in some
        # shapes. A page that adds nothing new means the walk is over, however
        # the endpoint chose to answer -- otherwise this loops forever.
        if fresh == 0:
            break
        skip += PAGE
    return list(rows.values())


def normalize(value: str) -> str:
    """Curly quotes and dashes differ between the title and the pasted copy."""
    return (
        value.replace("’", "'")
        .replace("‘", "'")
        .replace("“", '"')
        .replace("”", '"')
        .replace("—", "-")
        .replace("–", "-")
        .lower()
    )


def inspect(row: dict) -> dict | None:
    prompt = (row.get("artPrompt") or "").strip()
    if not prompt:
        return None
    title = (row.get("title") or "").strip()
    description = (row.get("description") or "").strip()
    flat = normalize(prompt)

    wrapper = next((p.pattern for p in APP_WRAPPERS if p.search(prompt)), None)
    generated = any(clause in prompt for clause in GENERATED_CLAUSES)
    named = bool(title) and normalize(title) in flat
    copy_led = bool(description) and flat.startswith(normalize(description)[:60])

    if wrapper:
        finding = "app-wrapper"
    elif generated and not named:
        finding = "no-subject"
    elif copy_led and generated:
        finding = "card-copy"
    else:
        return None

    return {
        "id": row.get("id"),
        "title": title,
        "taxonomy": row.get("taxonomy"),
        "finding": finding,
        "prompt": prompt,
        "imagePath": row.get("imagePath"),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument(
        "--limit", type=int, default=10, help="examples printed per finding (default 10)"
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    if not KR_API_TOKEN:
        print(
            "KR_API_TOKEN is not set, so the live Facet catalog cannot be read. "
            "Unresolved, not clean.",
            file=sys.stderr,
        )
        return 2

    try:
        rows = fetch_facets()
    except (urllib.error.URLError, urllib.error.HTTPError, ValueError) as error:
        print(f"Could not read the Facet catalog: {error}", file=sys.stderr)
        return 2

    findings = [f for f in (inspect(row) for row in rows) if f]
    blocking = [f for f in findings if f["finding"] in ("no-subject", "app-wrapper")]

    if args.json:
        print(json.dumps({"checked": len(rows), "findings": findings}, indent=2))
        return 1 if blocking else 0

    print(f"Checked {len(rows)} Facets against their own artPrompt.")
    if not findings:
        print("Every prompt names something to draw.")
        return 0

    for kind, label in (
        ("no-subject", "NO SUBJECT — generated prompt, own title nowhere in it"),
        ("app-wrapper", "APP WRAPPER — application context Krea will paint as text"),
        ("card-copy", "CARD COPY — prompt opens with the description verbatim (smell only)"),
    ):
        group = [f for f in findings if f["finding"] == kind]
        if not group:
            continue
        print(f"\n{label}: {len(group)}")
        for item in group[: args.limit]:
            print(f"  facet/{item['id']} {item['taxonomy']} {item['title']!r}")
            print(f"      {item['prompt'][:150]}")
        if len(group) > args.limit:
            print(f"  ... and {len(group) - args.limit} more")

    if blocking:
        print(
            "\nAdvisory. Rewrite these to lead with the physical subject, then go look "
            "at the cards -- a clean contract is not a good prompt (ART-PROMPTS.md rule 5)."
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
