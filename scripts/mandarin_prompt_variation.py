#!/usr/bin/env python3
"""Apply Mandarin Tutor v2 per-card style variation to a manifest prompt.

Why this exists in Conductor at all
-----------------------------------

The Kind Robots manifest is the prompt authority: the tutor's per-card retry
button rebuilds its prompt from the server, so Conductor must not invent its own
art direction. But production is self-hosted on Alexandria and updates on Silas's
schedule, and the corpus is 577 cards with zero renders. Waiting for a container
update before submitting anything means the deck stays empty for however long
that takes.

So this module reproduces exactly one server-side edit -- the per-card style
draw added in kind_robots `server/utils/mandarinIllustrationStyle.ts` -- against
the prompt an older deployment is still serving. The kind_robots recipe was
written to make that possible: the style clauses are INSERTED into the original
sentence order, and the only text removed is "warm harmonious color, " from the
house-style sentence. Nothing else is reworded. Apply the same edit here and you
land on a byte-identical string.

Once Alexandria serves the new recipe, manifest entries carry `styleVariant`
directly and `apply_style_variation` becomes a no-op -- so this fallback retires
itself instead of drifting.

The axis lists below are a mirror. If you change one, change the other; the
kind_robots contract test and `--selftest` here both pin the same properties.
"""

from __future__ import annotations

import hashlib
import sys

RECIPE_ID = "modern-chinese-picturebook-v2"

# The house-style sentence as older deployments emit it, and as the current
# recipe emits it. The delta is the dropped "warm harmonious color, " -- the
# palette axis now names the colour, and leaving both in had every card asking
# for the same warm harmony regardless of which palette it drew.
HOUSE_STYLE_LEGACY = (
    "House style: modern Chinese educational picture-book art, hand-painted gouache with "
    "gentle watercolor and restrained ink-wash influence, matte pigments, subtle paper grain, "
    "clean shapes, clear silhouettes, limited deliberate detail, warm harmonious color, and "
    "generous negative space."
)
HOUSE_STYLE_CURRENT = (
    "House style: modern Chinese educational picture-book art, hand-painted gouache with "
    "gentle watercolor and restrained ink-wash influence, matte pigments, subtle paper grain, "
    "clean shapes, clear silhouettes, limited deliberate detail, and generous negative space."
)

FRAMINGS = (
    "Frame it as a close still life: the subject large in the square and lightly cropped by it, seen from a little above the surface it rests on.",
    "Frame it wide and quiet: the subject small and set low in the square, with a large calm field of paper above and around it.",
    "Frame it as a mid-distance vignette: the subject off-centre, with the scene painted only where it matters and dissolving into bare paper toward the edges.",
    "Frame it as a flat overhead view, looking straight down on a small arrangement laid out on a plain surface.",
    "Frame it at eye level, the subject reading clearly in profile or three-quarter view against a nearly empty ground.",
    "Frame it through an ordinary near edge such as a doorway, window frame, table edge, or shelf, keeping that near edge a simple dark shape and the subject just beyond it.",
)

LIGHTS = (
    "Light it with flat, even overcast daylight: soft shadows, no strong direction, gentle contrast.",
    "Light it with low late-afternoon sun from one side: long soft shadows and a warm cast on the lit planes.",
    "Light it with bright open shade around midday: cool clean light and crisp but shallow shadows.",
    "Light it with warm indoor lamplight after dark: one small pool of light, the rest of the square settling into quiet muted tone.",
    "Light it with cool early-morning window light: pale, slightly blue shadows and a calm low-contrast feel.",
)

PALETTES = (
    "Keep the palette to muted indigo, slate blue, and warm off-white, with a single soft persimmon accent.",
    "Keep the palette to dusty jade and bamboo green over cream, with a single clay-red accent.",
    "Keep the palette to warm ochre, tea brown, and unbleached paper, with a single deep teal accent.",
    "Keep the palette to soft brick red and terracotta against pale grey-green, with a single ink-black accent.",
    "Keep the palette to pale wheat, straw yellow, and warm grey, with a single dusty plum accent.",
    "Keep the palette to cool porcelain white and celadon with charcoal drawing, and a single mustard accent.",
)

HANDLINGS = (
    "Handle the paint as flat opaque gouache shapes with very little blending and honest visible brush edges.",
    "Handle the paint as wet watercolour washes bleeding softly into one another, with a few edges left deliberately hard.",
    "Handle the paint with a dry brush dragged over rough paper so the tooth of the sheet breaks the colour.",
    "Handle the paint as thin washes under an uneven hand-drawn ink line that changes weight and sometimes misses its own shape.",
    "Handle the paint in broad simple strokes, letting pigment pool and darken at the edge of each shape.",
)

GROUNDS = (
    "Leave the ground as bare untouched paper so the negative space is genuinely empty.",
    "Set the subject on a single flat wash of ground colour that stops short of the square edges.",
    "Set the subject against a soft irregular halo of wash that fades out before it reaches the corners.",
    "Set the subject on a simple band of ground colour across the lower part of the square, leaving the rest as paper.",
)

AXES = (
    ("framing", FRAMINGS),
    ("light", LIGHTS),
    ("palette", PALETTES),
    ("handling", HANDLINGS),
    ("ground", GROUNDS),
)


def card_token(card_key: str) -> str:
    """The card's stable 24-hex token -- the same one that names its media file."""
    return hashlib.sha256(card_key.encode("utf-8")).hexdigest()[:24]


def style_variant(token: str) -> dict[str, str]:
    """The deterministic style draw for a card token.

    Each axis reads its own 4-hex slice, so two cards sharing a framing are no
    more likely to share a palette than any other pair.
    """
    normalized = token.strip().lower()
    variant: dict[str, str] = {}
    indices: list[int] = []
    for slot, (name, options) in enumerate(AXES):
        chunk = normalized[slot * 4 : slot * 4 + 4]
        try:
            value = int(chunk, 16)
        except ValueError:
            value = 0
        index = value % len(options)
        indices.append(index)
        variant[name] = options[index]
    variant["id"] = "f{}-l{}-p{}-h{}-g{}".format(*indices)
    return variant


def apply_style_variation(prompt: str, card_key: str) -> tuple[str, dict[str, str] | None]:
    """Return (prompt, variant) with this card's style draw folded in.

    A prompt that already carries the current house-style sentence came from a
    deployment that applies the draw itself; it is returned untouched with no
    variant, so a redeploy silently takes this fallback out of the loop.

    A prompt with neither house-style sentence is not a v2 prompt this module
    understands -- returned untouched rather than guessed at.
    """
    if HOUSE_STYLE_LEGACY not in prompt:
        return prompt, None

    variant = style_variant(card_token(card_key))
    clauses = " ".join(
        [HOUSE_STYLE_CURRENT] + [variant[name] for name, _ in AXES]
    )
    return prompt.replace(HOUSE_STYLE_LEGACY, clauses, 1), variant


def _selftest() -> int:
    failures = 0

    def check(condition: bool, label: str) -> None:
        nonlocal failures
        if not condition:
            failures += 1
            print(f"FAIL: {label}", file=sys.stderr)

    # Determinism, and insensitivity to token case/whitespace.
    token = card_token("hsk:1:的")
    check(style_variant(token) == style_variant(token), "variant is deterministic")
    check(
        style_variant(token) == style_variant(f"  {token.upper()}  "),
        "variant ignores token case and padding",
    )

    # The id names the actual draw.
    variant = style_variant(card_token("hsk:1:写"))
    parts = variant["id"].split("-")
    check(len(parts) == 5, "variant id has one index per axis")
    for part, (name, options) in zip(parts, AXES):
        check(options[int(part[1:])] == variant[name], f"variant id matches {name}")

    # Every option is reachable and none swallows the deck.
    keys = [f"hsk:{index % 6 + 1}:card-{index}" for index in range(621)]
    variants = [style_variant(card_token(key)) for key in keys]
    for name, options in AXES:
        seen = {variant[name] for variant in variants}
        check(len(seen) == len(options), f"every {name} option is reachable")
        for option in options:
            share = sum(1 for variant in variants if variant[name] == option) / len(variants)
            check(share < 0.4, f"no single {name} option dominates the deck")
    distinct = {variant["id"] for variant in variants}
    check(len(distinct) > len(variants) * 0.6, "most cards get a distinct style draw")

    # The insertion edits exactly the house-style sentence and nothing else.
    legacy = f"Concept sentence. {HOUSE_STYLE_LEGACY} Trailing guard rails."
    varied, applied = apply_style_variation(legacy, "hsk:1:的")
    check(applied is not None, "a legacy prompt gets a variant")
    check(varied.startswith("Concept sentence. "), "text before the house style is untouched")
    check(varied.endswith(" Trailing guard rails."), "text after the house style is untouched")
    check(HOUSE_STYLE_LEGACY not in varied, "the legacy house-style sentence is replaced")
    check(HOUSE_STYLE_CURRENT in varied, "the current house-style sentence is present")
    assert applied is not None
    for name, _ in AXES:
        check(applied[name] in varied, f"the {name} clause is present")

    # A prompt from a deployment that already varies is left alone.
    already, none_applied = apply_style_variation(varied, "hsk:1:的")
    check(already == varied, "an already-varied prompt is unchanged")
    check(none_applied is None, "an already-varied prompt reports no local variant")

    # No style clause may smuggle written language or tourist shorthand back in.
    for _, options in AXES:
        for option in options:
            lowered = option.lower()
            check(
                not any(
                    word in lowered
                    for word in ("caption", "signage", "watermark", "numeral", "lettering")
                ),
                f"style clause asks for written language: {option}",
            )
            check(
                not any(
                    word in lowered
                    for word in ("pagoda", "lantern", "dragon", "great wall")
                ),
                f"style clause hard-codes China shorthand: {option}",
            )

    if failures:
        print(f"{failures} failure(s).", file=sys.stderr)
        return 1
    print("mandarin_prompt_variation selftest: OK")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(_selftest())
    print(__doc__)
