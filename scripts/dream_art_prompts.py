#!/usr/bin/env python3
"""Krea 2 art-prompt construction for the Daily Dream six-asset bundle.

Daily Dreams are portals into different worlds. The renderer must therefore keep
one day's six assets visually coherent without forcing every day through one
Kind Robots house look. Composition rules remain asset-specific, while a stable
per-world style selector supplies a materially different visual language.

Krea 2 runs at low CFG in the Kind Robots workflow, so these prompts use concrete
positive descriptions rather than relying on negative-prompt instructions.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

# These intentionally describe media/visual languages rather than named artists.
# One world gets one stable style, so its six assets belong together; a different
# world can look as if it came through an entirely different dimensional portal.
#
# The bank is data, not code: `scripts/data/art-style-catalog.json` is a
# byte-identical copy of kind_robots' `config/art-style-catalog.json`, which also
# feeds the art generator's Style picker (Silas, 2026-09-28: "an overall upgrade
# to the random default styles that we use for daily dream, including that super
# vibrant cartoon style ... and I want the default styles to all be included as
# options in the art generator"). Edit the kind_robots copy and copy it here.
#
# Each style carries a `weight`. Until 2026-09-28 every lane was equally likely,
# and four of the twelve (photorealism with restrained grading, charcoal cosmic
# horror, scratchboard, muted naturalist watercolour) were dark or desaturated,
# so a third of days rendered gloomy. The current 20 came out of the 2026-09-29
# bake-off (32 candidates, same three subjects and seeds on Krea 2); styles that
# collapsed into one generic cartoon or went pale were cut. Vibrant styles weigh
# 3-4 and the two moody ones 2: a gloomy world still turns up, about one day in
# fifteen.
STYLE_CATALOG_PATH = Path(__file__).resolve().parent / "data" / "art-style-catalog.json"
STYLE_CATALOG: tuple[dict, ...] = tuple(
    json.loads(STYLE_CATALOG_PATH.read_text(encoding="utf-8"))["styles"]
)
STYLE_DIRECTIONS: tuple[str, ...] = tuple(style["prompt"] for style in STYLE_CATALOG)
STYLE_WEIGHTS: tuple[int, ...] = tuple(int(style["weight"]) for style in STYLE_CATALOG)

# Compatibility alias for callers/tests that imported STYLE before the variety
# pass. Builders no longer use one universal STYLE.
STYLE = STYLE_DIRECTIONS[0]

# An orthogonal axis to STYLE_DIRECTIONS. The media multiplied by these treatments
# give the remaster enough room to replace a few hundred images without producing a few
# hundred cousins of the same diffusion look. Treatments describe camera, palette, and
# light — never medium — so a treatment can ride on any style without fighting it.
TREATMENTS = (
    "low hero angle, deep shadow, one hard key light, restricted palette of two hues",
    "overhead plan view, flat even daylight, chalky pastel palette, long soft shadows",
    "eye-level middle distance, overcast diffuse light, muted earth palette, fine haze",
    "extreme close framing with shallow focus, warm rim light against a cool ground",
    "wide horizon-low composition, dusk gradient sky, silhouette-forward staging",
    "tilted dynamic framing, hard coloured light from two directions, high saturation",
    "symmetrical centred framing, cold monochrome palette, one saturated accent colour",
    "backlit contre-jour staging, dust and moisture in the beam, deep bronze shadows",
    "high vantage looking down a steep drop, cool blue shade against a hot lit floor",
    "night scene lit by nearby lamps and lanterns, deep blacks, small warm pools",
)

CAST_DIRECTION = (
    "cast the figures who appear naturally across many species, ages, body sizes, "
    "body shapes, and gender presentations"
)

# Stated as adjectives, not exclusions. This used to read "an unpeopled frame,
# the subject stands alone with no bystanders, no onlookers, and no crowd",
# which names three kinds of people to an engine that cannot act on the word
# "no" -- Krea 2 renders at cfg 1, where the ComfyUI negative prompt is inert.
# "unpeopled" was the only part of it that worked; the tail after it was
# commissioning the very crowd the 2026-08-08 sweep existed to remove. Silas
# found the leftovers still rendering on 2026-09-19, six weeks later.
UNPEOPLED = (
    "an unpeopled setting, the subject alone, the space around it bare and deserted"
)

# Same rule, text instead of people: naming text to a Qwen-lineage model is how
# you order lettering. Describe the surface, not the absence.
NO_TEXT = "every surface bare and unmarked"
CARD_FRAMING = "vertical 2:3 portrait composition"
MAX_PROMPT_CHARS = 1400


def _clean(value: object) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    return text.rstrip(" .;,")


def _join(*parts: object) -> str:
    prompt = ", ".join(p for p in (_clean(x) for x in parts) if p)
    if len(prompt) <= MAX_PROMPT_CHARS:
        return prompt
    cut = prompt.rfind(", ", 0, MAX_PROMPT_CHARS)
    return prompt[: cut if cut > 0 else MAX_PROMPT_CHARS].rstrip(" ,")


def _a(name: str) -> str:
    name = _clean(name)
    if re.match(r"(?i)^(the|a|an)\s", name):
        return name
    return f"a single {name}"


def _the(name: str) -> str:
    """`the <name>` without doubling an article the title already carries."""
    name = _clean(name)
    return name if re.match(r"(?i)^(the|a|an)\s", name) else f"the {name}"


def _world_context(title: str, vibe_line: str) -> str:
    line = _clean(vibe_line)
    title = _clean(title)
    if title and line:
        return f"set in the world of {title}, where {line[0].lower() + line[1:]}"
    return f"set in the world of {title}" if title else ""


def _lane(world_title: str, salt: str, size: int, variant: int) -> int:
    """Deterministic lane index, offset by `variant` for a remaster restyle."""
    return (_world_hash(world_title, salt) + variant) % size


def _world_hash(world_title: str, salt: str) -> int:
    key = (_clean(world_title).casefold() + salt).encode("utf-8") or b"daily-dream"
    return int.from_bytes(hashlib.sha256(key).digest()[:4], "big")


def style_index_for_world(world_title: str, variant: int = 0) -> int:
    """Weighted, deterministic index into STYLE_DIRECTIONS.

    Heavier styles own proportionally more of the hash space. `variant` then steps
    the chosen lane along the bank, so a remaster restyle always moves a world off
    its default look regardless of weight.
    """
    slot = _world_hash(world_title, "") % sum(STYLE_WEIGHTS)
    for index, weight in enumerate(STYLE_WEIGHTS):
        if slot < weight:
            return (index + variant) % len(STYLE_DIRECTIONS)
        slot -= weight
    return variant % len(STYLE_DIRECTIONS)


def style_lane_share(index: int) -> float:
    """The fraction of worlds a style lane is expected to carry."""
    return STYLE_WEIGHTS[index] / sum(STYLE_WEIGHTS)


def style_for_world(world_title: str, variant: int = 0) -> str:
    """Return one deterministic visual language for all assets in a world.

    Python's built-in hash is intentionally randomized between processes, so use
    SHA-256 to keep rebuilds and retries stable. The lane is weighted by the
    catalog's `weight` (see STYLE_CATALOG) without turning style into another
    model call.

    `variant` walks a world deliberately off its default lane. The catalog remaster
    uses it to break up crowded lanes without making style selection random.
    """
    return STYLE_DIRECTIONS[style_index_for_world(world_title, variant)]


def treatment_for_world(world_title: str, variant: int = 0) -> str:
    """Camera/palette/light treatment for a world, orthogonal to its medium."""
    return TREATMENTS[_lane(world_title, "|treatment", len(TREATMENTS), variant)]


def visual_language(world_title: str, variant: int = 0) -> str:
    """Medium plus treatment — the full visual identity of one remastered world."""
    return f"{style_for_world(world_title, variant)}, {treatment_for_world(world_title, variant)}"


def world_prompt(title: str, idea: str, vibe_line: str, vibe_art: str = "",
                 style: str | None = None) -> str:
    return _join(
        f"establishing key art for {_clean(title)}",
        vibe_art or idea,
        f"the defining image of a place where {_clean(vibe_line).lower()}",
        CARD_FRAMING,
        "wide establishing view with a strong foreground anchor, clear middle ground, "
        "and deep atmospheric background",
        # Stated as a fact about the frame, never as a condition on one. Krea
        # cannot evaluate "any figures present" any more than it can evaluate
        # "no" -- and because the phrase has no leading when/if,
        # artPromptContract's CONDITIONAL_PATTERNS never matched it either. 103
        # dream records carried it past every check before anyone looked at a
        # picture (2026-09-20).
        "an expansive landscape, a few distant figures near the "
        "horizon giving it scale",
        style or style_for_world(title),
        NO_TEXT,
    )


# `known_for`, `carries`, and `role_drive` are complete sentences under the
# card-copy contract (dream_prose_quality), so they are introduced with a colon
# rather than spliced into a grammatical stem — "a place known for Its prismatic
# chambers turn ..." is not a phrase an image model can use.
def location_prompt(title: str, art_direction: str, known_for: str,
                    best_scene: str, world_title: str, vibe_line: str,
                    style: str | None = None) -> str:
    return _join(
        f"{_clean(art_direction)} — {_the(title)}",
        f"known for: {_clean(known_for)}" if known_for else "",
        f"staged at its most telling moment: {_clean(best_scene)}" if best_scene else "",
        _world_context(world_title, vibe_line),
        CARD_FRAMING,
        # Same fix as world_prompt above: a fact, not a condition.
        "architectural establishing shot, expansive architecture, a few "
        "distant figures near the horizon giving it scale",
        style or style_for_world(world_title),
        NO_TEXT,
    )


def character_prompt(name: str, look: str, role_drive: str, carries: str,
                     world_title: str, vibe_line: str,
                     style: str | None = None) -> str:
    return _join(
        f"character portrait of {_clean(name)}",
        _clean(look),
        f"visibly carrying: {_clean(carries)}" if carries else "",
        f"the bearing of someone driven by this: {_clean(role_drive)}" if role_drive else "",
        _world_context(world_title, vibe_line),
        CARD_FRAMING,
        "single figure, three-quarter view from the waist up, close-up, "
        "sharply separated from a simple world-specific background",
        style or style_for_world(world_title),
        NO_TEXT,
    )


def scene_prompt(scene: str, world_title: str, vibe_line: str,
                 style: str | None = None) -> str:
    """A hand-described scene, wrapped in the same world/framing/style tail the
    builders add. For an element whose picture is a specific moment rather than
    a portrait or an establishing shot (a rider on a turtle's back watching a
    butterfly, say), the author's own words lead and nothing is prepended that
    would fight them."""
    return _join(
        _clean(scene),
        _world_context(world_title, vibe_line),
        CARD_FRAMING,
        style or style_for_world(world_title),
        NO_TEXT,
    )


def reward_prompt(name: str, reward_type: str, look: str, grants: str,
                  rarity: str, world_title: str, vibe_line: str,
                  style: str | None = None) -> str:
    kind = str(reward_type or "ITEM").upper()
    look = _clean(look)
    grants = _clean(grants)
    rarity = _clean(rarity).lower()
    style = style or style_for_world(world_title)

    if kind == "SKILL":
        manifestation = look or (
            f"the visible signature of the technique in mid-use, the effect of {grants} "
            "shown as light, motion, and material change in the air"
        )
        return _join(
            f"{_clean(name)}, a single practiced technique caught mid-use",
            manifestation,
            f"the effect itself is the subject: {grants}" if grants else "",
            _world_context(world_title, vibe_line),
            CARD_FRAMING,
            # "no full figure, no faces, no onlookers" put three people nouns in
            # positive conditioning on 68 SKILL rewards. The positive form of
            # the same intent is a crop: say where the frame stops.
            "tight centered composition on the effect, cropped close so that only one "
            "pair of hands enters at the very edge to work it, "
            "wrists cropped tightly",
            f"rendered with the weight given a {rarity} ability" if rarity else "",
            style,
            NO_TEXT,
        )

    return _join(
        f"{_a(name)}, one object alone",
        look or f"a crafted object whose form makes plain what it does: {grants}",
        f"its purpose readable in its shape: {grants}" if grants and look else "",
        _world_context(world_title, vibe_line),
        CARD_FRAMING,
        "museum-like object study, the object centered in close-up, resting on a "
        "bare surface or floating against a simple ground, close enough to read material and wear",
        UNPEOPLED,
        f"rendered with the reverence given a {rarity} artifact" if rarity else "",
        style,
        NO_TEXT,
    )


def scenario_prompt(title: str, setup: str, location_title: str,
                    world_title: str, vibe_line: str,
                    style: str | None = None) -> str:
    return _join(
        f"establishing scene art for the moment titled {_clean(title)}",
        _clean(setup),
        f"staged at {_clean(location_title)}" if location_title else "",
        _world_context(world_title, vibe_line),
        CARD_FRAMING,
        "a single decisive moment with one clear focal action, foreground figures reacting, "
        "uncluttered staging so the event reads at a glance",
        CAST_DIRECTION,
        style or style_for_world(world_title),
        NO_TEXT,
    )
