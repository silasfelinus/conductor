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
import re

# These intentionally describe media/visual languages rather than named artists.
# One world gets one stable style, so its six assets belong together; a different
# world can look as if it came through an entirely different dimensional portal.
STYLE_DIRECTIONS = (
    (
        "bold four-color superhero-comic aesthetic, muscular ink contours, "
        "saturated cel color, halftone texture, dramatic foreshortening, crisp graphic shadows"
    ),
    (
        "charcoal-and-chalk cosmic-horror drawing, rough paper grain, crushed blacks, "
        "pale luminous accents, smeared edges, unsettling shifts of scale"
    ),
    (
        "luminous gouache storybook painting, matte pigment, simplified confident shapes, "
        "soft edge variation, layered hand-painted texture"
    ),
    (
        "tactile stop-motion miniature aesthetic, sculpted clay and felt surfaces, "
        "handmade imperfections, practical miniature lighting, shallow depth of field"
    ),
    (
        "high-contrast risograph aesthetic, limited spot-color layers, coarse paper grain, "
        "slight registration offsets, bold graphic silhouettes"
    ),
    (
        "low-poly 3D diorama, faceted geometry, toy-scale materials, crisp ambient occlusion, "
        "clean volumetric lighting, deliberately simplified forms"
    ),
    (
        "cinematic photorealism, natural lens behavior, physically believable materials, "
        "volumetric atmosphere, restrained color grading, fine environmental detail"
    ),
    (
        "stained-glass mosaic aesthetic, strong leaded contours, jewel-tone translucent panes, "
        "fractured colored light, geometric shape language"
    ),
    (
        "watercolor-and-ink naturalist illustration, transparent washes, dry-brush texture, "
        "expressive line variation, visible paper tooth, selective fine detail"
    ),
    (
        "neon cel-animation aesthetic, clean graphic linework, flat luminous color, "
        "sharp rim lighting, dynamic perspective, controlled gradients"
    ),
    (
        "layered paper-cut collage, visible paper fibers, simplified cut shapes, "
        "physical layer shadows, tactile depth, hand-cut irregular edges"
    ),
    (
        "scratchboard engraving aesthetic, dense crosshatching and carved white lines, "
        "near-monochrome values, one restrained luminous accent, dramatic texture"
    ),
)

# Compatibility alias for callers/tests that imported STYLE before the variety
# pass. Builders no longer use one universal STYLE.
STYLE = STYLE_DIRECTIONS[0]

# An orthogonal axis to STYLE_DIRECTIONS. Twelve media multiplied by these treatments
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
    "night scene lit only by sources inside the frame, deep blacks, small warm pools",
)

CAST_DIRECTION = (
    "cast the figures who appear naturally across many species, ages, body sizes, "
    "body shapes, and gender presentations"
)

UNPEOPLED = (
    "an unpeopled frame, the subject stands alone with no bystanders, "
    "no onlookers, and no crowd"
)

NO_TEXT = "unmarked surfaces, free of text"
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
    key = (_clean(world_title).casefold() + salt).encode("utf-8") or b"daily-dream"
    index = int.from_bytes(hashlib.sha256(key).digest()[:4], "big")
    return (index + variant) % size


def style_for_world(world_title: str, variant: int = 0) -> str:
    """Return one deterministic visual language for all assets in a world.

    Python's built-in hash is intentionally randomized between processes, so use
    SHA-256 to keep rebuilds and retries stable. Twelve lanes make accidental
    adjacent-world repeats uncommon without turning style into another model call.

    `variant` walks a world deliberately off its default lane. The catalog remaster
    uses it to break up crowded lanes without making style selection random.
    """
    return STYLE_DIRECTIONS[_lane(world_title, "", len(STYLE_DIRECTIONS), variant)]


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
        "the setting is the subject; any figures present are incidental to the place",
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
        "architectural establishing shot, the environment is the subject and any figures "
        "present are small and incidental, included only for scale",
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
        "single figure, three-quarter view from the waist up, filling most of the frame, "
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
            "tight centered composition on the effect, at most one pair of hands entering "
            "frame at the edge to work it, no full figure, no faces, no onlookers",
            f"rendered with the weight given a {rarity} ability" if rarity else "",
            style,
            NO_TEXT,
        )

    return _join(
        f"{_a(name)}, one object alone in frame",
        look or f"a crafted object whose form makes plain what it does: {grants}",
        f"its purpose readable in its shape: {grants}" if grants and look else "",
        _world_context(world_title, vibe_line),
        CARD_FRAMING,
        "museum-like object study, the object centered and filling the frame, resting on a "
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
