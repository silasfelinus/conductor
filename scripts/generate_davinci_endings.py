#!/usr/bin/env python3

import argparse
import json
import re
from pathlib import Path

DIMENSIONS = [
    {
        "key": "legacy",
        "pass_label": "Remembered",
        "fail_label": "Forgotten",
        "pass_noun": "Legacy",
        "fail_noun": "Echo",
        "positive": "ancestral light, monuments of memory, heirlooms, records, continuity",
        "negative": "erased footprints, weathered ruins, vanishing records, forgotten rooms",
    },
    {
        "key": "wealth",
        "pass_label": "Prosperous",
        "fail_label": "Wanting",
        "pass_noun": "Fortune",
        "fail_noun": "Hunger",
        "positive": "golden practical abundance, secure workshop, generous resources",
        "negative": "empty ledger, patched tools, fragile shelter, scarcity atmosphere",
    },
    {
        "key": "love",
        "pass_label": "Beloved",
        "fail_label": "Alone",
        "pass_noun": "Heart",
        "fail_noun": "Distance",
        "positive": "warm companions, chosen family, affectionate gestures, soft light",
        "negative": "empty chairs, distant silhouettes, cold rooms, unspoken letters",
    },
    {
        "key": "wisdom",
        "pass_label": "Wise",
        "fail_label": "Foolish",
        "pass_noun": "Lantern",
        "fail_noun": "Mirror",
        "positive": "luminous library, reflective eyes, symbolic compass, patient mentor",
        "negative": "broken compass, scattered notes, looping corridor, misleading mirror",
    },
    {
        "key": "health",
        "pass_label": "Vital",
        "fail_label": "Diminished",
        "pass_noun": "Breath",
        "fail_noun": "Fever",
        "positive": "living garden, steady breath, resilient body, sunrise restoration",
        "negative": "wilted garden, cracked mask, exhausted posture, dim clinical light",
    },
    {
        "key": "freedom",
        "pass_label": "Free",
        "fail_label": "Bound",
        "pass_noun": "Horizon",
        "fail_noun": "Chain",
        "positive": "open road, unlocked gate, wind, horizon, self-directed motion",
        "negative": "locked gate, strings, contract chains, narrow hallway, caged light",
    },
    {
        "key": "fame",
        "pass_label": "Renowned",
        "fail_label": "Obscure",
        "pass_noun": "Crown",
        "fail_noun": "Mask",
        "positive": "stage glow, public mural, constellation audience, mythic silhouette",
        "negative": "small private room, unnoticed masterpiece, dim street, hidden face",
    },
    {
        "key": "creation",
        "pass_label": "Creator",
        "fail_label": "Barren",
        "pass_noun": "World",
        "fail_noun": "Canvas",
        "positive": "blooming studio, finished artifact, living machine, painted universe",
        "negative": "blank canvas, unfinished sculpture, silent tools, abandoned blueprint",
    },
    {
        "key": "community",
        "pass_label": "Rooted",
        "fail_label": "Exiled",
        "pass_noun": "Village",
        "fail_noun": "Road",
        "positive": "welcoming village, shared table, cooperative workshop, braided paths",
        "negative": "closed circle, empty town square, distant windows, solitary road",
    },
    {
        "key": "mystery",
        "pass_label": "Awakened",
        "fail_label": "Mundane",
        "pass_noun": "Door",
        "fail_noun": "Candle",
        "positive": "dream portal, impossible stars, symbolic animal, glowing threshold",
        "negative": "sealed door, dull sky, extinguished candle, sleeping oracle",
    },
]

TITLE_PATTERNS = [
    "The {primary_noun} of {secondary_noun}",
    "The {primary_label} {secondary_noun}",
    "The Last {primary_noun}",
    "The {primary_noun} Behind the {secondary_noun}",
    "The House of {primary_noun}",
    "The {primary_label} Life",
    "The {primary_noun} at the End of the Road",
    "The {secondary_label} {primary_noun}",
]


def slugify(value: str) -> str:
    return re.sub(r"(^-|-$)", "", re.sub(r"[^a-z0-9]+", "-", value.lower()))


def bit_count(outcome_key: str) -> int:
    return outcome_key.count("1")


def victory_type(outcome_key: str) -> str:
    passed = bit_count(outcome_key)
    values = {dimension["key"]: outcome_key[index] == "1" for index, dimension in enumerate(DIMENSIONS)}

    if values["mystery"] and values["creation"] and values["freedom"] and not (values["fame"] and values["wealth"]):
        return "SECRET"
    if passed >= 8 and (values["love"] or values["wisdom"] or values["creation"]):
        return "VICTORY"
    if passed <= 2:
        return "FAILURE"
    return "MIXED"


def ending_for_key(outcome_key: str) -> dict:
    passed = [DIMENSIONS[index] for index, bit in enumerate(outcome_key) if bit == "1"]
    failed = [DIMENSIONS[index] for index, bit in enumerate(outcome_key) if bit == "0"]
    positive_pool = passed or DIMENSIONS
    negative_pool = failed or DIMENSIONS

    primary = positive_pool[int(outcome_key, 2) % len(positive_pool)]
    secondary = negative_pool[(int(outcome_key[::-1], 2) + bit_count(outcome_key)) % len(negative_pool)]
    pattern = TITLE_PATTERNS[int(outcome_key, 2) % len(TITLE_PATTERNS)]
    title = pattern.format(
        primary_label=primary["pass_label"],
        secondary_label=secondary["fail_label"],
        primary_noun=primary["pass_noun"],
        secondary_noun=secondary["fail_noun"],
    )
    slug = f"davinci-{outcome_key}-{slugify(title)}"
    victory = victory_type(outcome_key)
    pass_labels = [dimension["pass_label"].lower() for dimension in passed]
    fail_labels = [dimension["fail_label"].lower() for dimension in failed]

    summary = (
        f"A {victory.lower()} Da Vinci ending where the life resolves as "
        f"{', '.join(pass_labels) if pass_labels else 'without clear victories'} while facing "
        f"{', '.join(fail_labels) if fail_labels else 'no major unresolved losses'}."
    )
    visual_tokens = ", ".join([dimension["positive"] for dimension in passed[:3]] + [dimension["negative"] for dimension in failed[:3]])
    art_prompt = (
        f"Da Vinci life-sim ending art for outcome {outcome_key}: {title}. "
        f"Cinematic symbolic life narrative, {visual_tokens}, emotionally rich final tableau, "
        f"premium game ending illustration, no readable text, no logo, no watermark, no collage."
    )

    return {
        "title": title,
        "slug": slug,
        "outcomeKey": outcome_key,
        "summary": summary,
        "victoryType": victory,
        "icon": f"/images/davinci/endings/{outcome_key}-icon.webp",
        "heroImage": f"/images/davinci/endings/{outcome_key}-hero.webp",
        "artPrompt": art_prompt,
        "metadata": {
            "passed": [dimension["key"] for dimension in passed],
            "failed": [dimension["key"] for dimension in failed],
            "passCount": bit_count(outcome_key),
            "dimensionOrder": [dimension["key"] for dimension in DIMENSIONS],
        },
        "milestone": {
            "label": title,
            "message": summary[:760],
            "icon": f"/images/davinci/endings/{outcome_key}-icon.webp",
            "triggerCode": f"davinci-ending-{outcome_key}",
            "tooltip": f"Unlock the Da Vinci ending: {title}",
            "isActive": True,
            "isRepeatable": False,
            "imagePath": f"/images/davinci/endings/{outcome_key}-hero.webp",
            "artPrompt": art_prompt,
        },
        "achievement": {
            "title": title,
            "slug": slug,
            "achievementType": "ENDING",
            "conditionKey": f"ending:{outcome_key}",
            "description": summary,
            "icon": f"/images/davinci/endings/{outcome_key}-icon.webp",
            "imagePath": f"/images/davinci/endings/{outcome_key}-hero.webp",
            "artPrompt": art_prompt,
        },
    }


def generate_endings() -> list[dict]:
    return [ending_for_key(format(index, "010b")) for index in range(1024)]


def art_queue_entries(endings: list[dict], offset: int, limit: int) -> dict:
    selected = endings[offset : offset + limit]
    entries = []
    for ending in selected:
        key = ending["outcomeKey"]
        entries.append(
            {
                "id": f"davinci-ending-{key}-icon",
                "source": "davinci-ending-seed",
                "status": "pending",
                "target_repo": "silasfelinus/kind_robots",
                "image_path": f"public/images/davinci/endings/{key}-icon.webp",
                "source_url": f"/images/davinci/endings/{key}-icon.webp",
                "variant": "icon",
                "size": "512x512",
                "label": f"{ending['title']} icon",
                "prompt": ending["artPrompt"] + " Square achievement badge composition, strong silhouette, readable at small size.",
            }
        )
        entries.append(
            {
                "id": f"davinci-ending-{key}-hero",
                "source": "davinci-ending-seed",
                "status": "pending",
                "target_repo": "silasfelinus/kind_robots",
                "image_path": f"public/images/davinci/endings/{key}-hero.webp",
                "source_url": f"/images/davinci/endings/{key}-hero.webp",
                "variant": "hero",
                "size": "1280x720",
                "label": f"{ending['title']} hero",
                "prompt": ending["artPrompt"] + " Widescreen ending reveal composition with cinematic depth.",
            }
        )
    return {"batch": {"entries": entries}}


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate deterministic Da Vinci ending seed data.")
    parser.add_argument("--format", choices=["json", "jsonl", "art-queue"], default="json")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    endings = generate_endings()
    if args.format == "json":
        payload = json.dumps({"endings": endings}, indent=2)
    elif args.format == "jsonl":
        payload = "\n".join(json.dumps(ending, separators=(",", ":")) for ending in endings)
    else:
        payload = json.dumps(art_queue_entries(endings, args.offset, args.limit), indent=2)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)


if __name__ == "__main__":
    main()
