#!/usr/bin/env python3
"""Krea 2 art-prompt construction for the daily-dream six-asset bundle.

Why this module exists (2026-08-08, Silas): a Reward called "Tidefortune Ladle"
rendered as a crowd of fifteen people with no ladle anywhere. Two causes, both
fixed here.

1. **An unconditional casting instruction.** Every dream prompt ended in the
   legacy phrase "cohesive Kind Robots visual style", which the Kind Robots
   enqueue path (`server/utils/artJobNormalization.ts` → `replaceVagueArtDirection`)
   rewrote into a 60-word house block whose middle third read "cast characters
   naturally across many species, ages, body sizes, body shapes, gender
   presentations, and levels of conventional attractiveness; include robots only
   when the subject or scene explicitly calls for them". That sentence is an
   *instruction* — it assumes a reader who can evaluate "only when the scene
   calls for it". Krea 2 is a distilled diffusion transformer, not an
   instruction-follower: it reads "characters ... many species, ages, body sizes,
   body shapes, gender presentations" as the densest, most concrete noun phrase
   in the prompt and paints exactly that. A crowd.

2. **A subject clause that could not compete.** The ladle's whole visual
   description was "stirred through any dish, it surfaces the hidden fortune
   buried in a person or object" — a *function*, not an appearance. No material,
   no shape, no scale, no framing. Twenty tokens of abstraction against ninety
   tokens of concrete people. The people won.

The rules encoded below follow from that:

- **Subject first, in physical nouns.** What the thing is made of and looks like
  leads; what it does comes second, as a visible consequence.
- **Never emit "Kind Robots visual style".** Write the style out explicitly so
  no downstream regex can substitute something subject-inappropriate.
- **Casting direction is opt-in.** `CAST_DIRECTION` is appended only for scenes
  whose authored action genuinely requires a cast. Single-character portraits
  encode singular framing directly; worlds and locations keep any figures
  optional/incidental instead of injecting crowd vocabulary.
- **Exclusions are stated positively where possible.** Krea 2 runs at cfg 1,
  which makes the ComfyUI negative prompt inert (see
  `server/api/comfy/krea2/utils/workflow.ts`). Every constraint has to survive
  inside the positive prompt, and "no people" is weaker than "alone on a bare
  surface".
- **Framing and scale are always explicit.** Krea 2 thrives on camera language;
  omitting it is how a hand-held object becomes an establishing shot.
"""
from __future__ import annotations

import re

# ── House style ──────────────────────────────────────────────────────────────
# Written out in full so it never depends on the legacy phrase-substitution.
STYLE = (
    "detailed mature western animation illustration, confident ink-like linework, "
    "dimensional forms, rich controlled color, tactile surface texture, "
    "clear readable silhouette"
)

# Applied ONLY where the frame actually contains people. See module docstring.
CAST_DIRECTION = (
    "cast the figures who appear naturally across many species, ages, body sizes, "
    "body shapes, and gender presentations"
)

# The counterweight for object and landscape subjects.
UNPEOPLED = (
    "an unpeopled frame — the subject stands alone with no bystanders, "
    "no onlookers, and no crowd"
)

# One short clause, not a list. Krea 2 is Qwen-Image lineage — the strongest
# open text renderer there is — and at cfg 1 the ComfyUI negative prompt is
# inert, so every word here lands in POSITIVE conditioning. Naming "text,
# lettering, logos, watermark, signature" five times told a text specialist to
# think about text five times. Say it once, and rely mainly on not describing
# anything that would carry writing.
NO_TEXT = "unmarked surfaces, free of text"

# Deliberately does NOT say "card". Asking Krea 2 for a "2:3 portrait card
# composition" — alongside "treasure card illustration" — got exactly what was
# asked for: a full trading card with a title bar, a type line, and a rules box
# of invented text (2026-08-08, rewards 2688/2616/2551). To a person "card
# illustration" means the art printed on a card; to the model it means a card.
CARD_FRAMING = "vertical 2:3 portrait composition"

MAX_PROMPT_CHARS = 1400


def _clean(value: object) -> str:
    """Collapse whitespace and strip trailing sentence punctuation."""
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    return text.rstrip(" .;,")


def _join(*parts: object) -> str:
    """Join non-empty clauses into one comma-separated prompt, length-capped."""
    prompt = ", ".join(p for p in (_clean(x) for x in parts) if p)
    if len(prompt) <= MAX_PROMPT_CHARS:
        return prompt
    # Trim at a clause boundary rather than mid-word so the tail stays legible.
    cut = prompt.rfind(", ", 0, MAX_PROMPT_CHARS)
    return prompt[: cut if cut > 0 else MAX_PROMPT_CHARS].rstrip(" ,")


def _a(name: str) -> str:
    """Prefix a subject with an article, unless its name already carries one.

    Reward names are authored freely, so half of them arrive as "The Corsair's
    Encore" and half as "Molt-Jar". "a single The Corsair's Encore" reads as
    noise to a text encoder trained on natural captions.
    """
    name = _clean(name)
    if re.match(r"(?i)^(the|a|an)\s", name):
        return name
    return f"a single {name}"


def _world_context(title: str, vibe_line: str) -> str:
    """A short, bounded 'where this lives' clause — never the primary subject."""
    line = _clean(vibe_line)
    title = _clean(title)
    if title and line:
        return f"set in the world of {title}, where {line[0].lower() + line[1:]}"
    return f"set in the world of {title}" if title else ""


# ── Per-element builders ─────────────────────────────────────────────────────

def world_prompt(title: str, idea: str, vibe_line: str, vibe_art: str = "") -> str:
    """Establishing key art for the umbrella PITCH dream."""
    return _join(
        f"establishing key art for {_clean(title)}",
        vibe_art or idea,
        f"the defining image of a place where {_clean(vibe_line).lower()}",
        CARD_FRAMING,
        "wide establishing view with a strong foreground anchor, "
        "clear middle ground, and deep atmospheric background",
        "the setting is the subject; any figures present are incidental to the place",
        "cinematic directional light, layered depth",
        STYLE,
        NO_TEXT,
    )


def location_prompt(title: str, art_direction: str, known_for: str,
                    best_scene: str, world_title: str, vibe_line: str) -> str:
    """A place. People may appear, but the architecture is the subject."""
    return _join(
        f"{_clean(art_direction)} — the {_clean(title)}",
        f"a place known for {_clean(known_for)}" if known_for else "",
        f"staged at its most telling moment: {_clean(best_scene)}" if best_scene else "",
        _world_context(world_title, vibe_line),
        CARD_FRAMING,
        "architectural establishing shot, the environment is the subject and any "
        "figures present are small and incidental, included only for scale",
        "cinematic directional light raking across the structures, "
        "deep atmospheric perspective",
        STYLE,
        NO_TEXT,
    )


def character_prompt(name: str, look: str, role_drive: str, carries: str,
                     world_title: str, vibe_line: str) -> str:
    """A single figure. The one element where a person IS the subject."""
    return _join(
        f"character portrait of {_clean(name)}",
        _clean(look),
        f"visibly carrying {_clean(carries)}" if carries else "",
        f"bearing of someone whose purpose is to {_clean(role_drive).lower()}" if role_drive else "",
        _world_context(world_title, vibe_line),
        CARD_FRAMING,
        "single figure, three-quarter view from the waist up, filling most of the "
        "frame, sharply separated from a softly out-of-focus background",
        "directional key light shaping the face and form, warm rim light",
        STYLE,
        NO_TEXT,
    )


def reward_prompt(name: str, reward_type: str, look: str, grants: str,
                  rarity: str, world_title: str, vibe_line: str) -> str:
    """A Reward. This is the case the old builder got catastrophically wrong.

    ITEM  → a physical object, product-shot framing, nobody in frame.
    SKILL → the *visible manifestation* of an ability: the effect in the air,
            the tools and residue it leaves. Hands may appear; a cast may not.
    """
    kind = str(reward_type or "ITEM").upper()
    look = _clean(look)
    grants = _clean(grants)
    rarity = _clean(rarity).lower()

    if kind == "SKILL":
        # A skill has no body, so name the visible evidence of it instead. Left
        # unanchored, "a skill" resolves to "a person" and the crowd returns.
        manifestation = look or (
            f"the visible signature of the technique in mid-use — the effect of "
            f"{grants} shown as light, motion, and material change in the air"
        )
        return _join(
            f"{_clean(name)}, a single practiced technique caught mid-use",
            manifestation,
            f"the effect itself is the subject: {grants}" if grants else "",
            _world_context(world_title, vibe_line),
            CARD_FRAMING,
            "tight centered composition on the effect, at most one pair of hands "
            "entering frame at the edge to work it, no full figure, no faces, "
            "no onlookers",
            f"rendered with the weight given a {rarity} ability" if rarity else "",
            "glowing volumetric light emanating from the effect itself, "
            "dark uncluttered surroundings",
            STYLE,
            NO_TEXT,
        )

    return _join(
        f"{_a(name)}, one object alone in frame",
        look or f"a crafted object whose form makes plain what it does: {grants}",
        f"its purpose readable in its shape: {grants}" if grants and look else "",
        _world_context(world_title, vibe_line),
        CARD_FRAMING,
        "museum product shot, the object centered and filling the frame, resting "
        "on a bare surface or floating against a plain dark ground, close enough "
        "to read its material and wear",
        UNPEOPLED,
        f"rendered with the reverence given a {rarity} artifact" if rarity else "",
        "focused directional light picking out material, edge, and texture",
        STYLE,
        NO_TEXT,
    )


def scenario_prompt(title: str, setup: str, location_title: str,
                    world_title: str, vibe_line: str) -> str:
    """One dramatic beat. People belong here; the moment must still read."""
    return _join(
        f"establishing scene art for the moment titled {_clean(title)}",
        _clean(setup),
        f"staged at {_clean(location_title)}" if location_title else "",
        _world_context(world_title, vibe_line),
        CARD_FRAMING,
        "a single decisive moment with one clear focal action, foreground figures "
        "reacting, uncluttered staging so the event reads at a glance",
        "cinematic key light on the focal action, atmosphere falling away behind it",
        CAST_DIRECTION,
        STYLE,
        NO_TEXT,
    )
