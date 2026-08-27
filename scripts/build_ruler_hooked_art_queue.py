#!/usr/bin/env python3
"""Stage The Ruler Is Hooked art requests into projects/art-prompts.yaml.

WHY THIS EXISTS. ruler-hooked/t-008 pinned the look and wrote the prompt
templates (projects/ruler-hooked/docs/art-direction.md) but generated nothing --
KR_API_TOKEN was unset at the time, and the queue entries it describes in its
Section 6 are no longer in art-prompts.yaml. The project needs hundreds of
assets (FULL-GAME-GAP-AUDIT.md, 2026-08-26), so the prompts must be generated
from the specs rather than hand-typed once and left to drift, the same way
build_cthulhuquarium_art_queue.py reads the fish bible instead of copying it.

Two lanes, deliberately separated:

  concept  -- full-frame key art and cast portraits. No compositing contract
              applies, so these are unblocked and are what Silas asked for
              first: pieces that pin the look before production scales.
  fish     -- one species design per entry in projects/ruler-hooked/fish/
              vertical-slice.yaml, at <slug>/bestiary.webp per the art key
              convention in docs/fish-ecology.md. Prompts are built from the
              roster's own `silhouette` and `distinction` fields, so the roster
              stays the single source and later presentation variants
              (catch card, lake context, silhouette) derive from one design.
  layer    -- the 37-cell (region, state, time) environment matrix from the
              live regions manifest in kind_robots utils/rulerHooked/content.ts.
              Emitted with --include-layers. Unblocked 2026-08-26 once the
              format contract was settled -- see LAYER FORMAT, below.

LAYER FORMAT (settled 2026-08-26, ruler-hooked/t-017, kind_robots PR #2139).
A layer is a FULL-PLAY-SCREEN image, transparent everywhere outside its own depth
band, registered so the layers stack into one frame -- what docs/art-direction.md
Section 2 always specified. The shipped component had been drawing each region
inside its own flex-1 band with `object-cover` (roughly a 20:1 strip), which would
have cropped a correctly-authored layer to a slice of its own middle; it now
composites full-frame in z-order over one canvas, with the banded gradients kept
underneath as the placeholder floor. Staging the matrix was deliberately held
until that landed, because 37 renders against the losing contract is 37 wasted
renders.

The cast is read from kind_robots' content bundle so a character added there
cannot silently miss its portrait. Scene/UI concepts have no upstream source, so
their prompts live in this file -- that is the one place to edit them.

Usage:
    python scripts/build_ruler_hooked_art_queue.py            # dry run, print plan
    python scripts/build_ruler_hooked_art_queue.py --write    # stage into art-prompts.yaml
    python scripts/build_ruler_hooked_art_queue.py --check    # exit 1 if staging is stale
    python scripts/build_ruler_hooked_art_queue.py --include-layers --write
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
ART_PROMPTS = REPO / "projects" / "art-prompts.yaml"

# The content bundle lives in a sibling checkout whose location differs between a
# local clone and a session container, so look in both rather than guessing one.
FISH_ROSTER = REPO / "projects" / "ruler-hooked" / "fish" / "vertical-slice.yaml"

CONTENT_CANDIDATES = (
    REPO.parent / "kind_robots" / "utils" / "rulerHooked" / "content.ts",
    Path.home() / "kind_robots" / "utils" / "rulerHooked" / "content.ts",
    Path("/home/user/kind_robots/utils/rulerHooked/content.ts"),
)

ENGINE = "krea2"
WIDE = "1344x768"
PORTRAIT = "768x1024"
SQUARE = "1024x1024"

TARGET_REPO = "silasfelinus/kind_robots"
PAGE_URL = "https://kindrobots.org/plan/projects/ruler-hooked"
MEDIA_ORIGIN = "https://media.acrocatranch.com"

# Concept art goes ahead of the mandarin-tutor curriculum backlog (priority 80)
# so the pieces Silas asked to see first are not queued behind 572 flashcards.
# The layer matrix sits just above it instead of at the front.
CONCEPT_PRIORITY = 150
LAYER_PRIORITY = 100

# ---------------------------------------------------------------------------
# House style (docs/art-direction.md Section 1-2)
# ---------------------------------------------------------------------------

# Descriptive, never conditional. A diffusion model reads "include X when the
# scene calls for it" as the dense noun phrase "include X", which is how an
# earlier casting clause turned inanimate subjects into crowds of people
# (see scripts/repair_art_request_defaults.py's header).
STYLE_TAIL = (
    "cartoony goofy storybook illustration, soft confident hand-drawn linework, "
    "rounded generous shape language, warm saturated slightly-faded storybook palette, "
    "painterly depth and warm cinematic light, exaggerated expressive character acting, "
    "strong readable silhouettes, charming and wry, "
    "in the spirit of Monkey Island, Ralph Bakshi, Treasure Planet, Steven Universe, "
    "and She-Ra Princess of Power. Hand-drawn animation cel and gouache painting, "
    "visibly illustrated by a person"
)

# Stated as the wanted RESULT, not as a pile of exclusions. kind_robots'
# server/utils/artPromptContract.ts rejects more than four text-nouns-after-"no"
# on an engine whose negative prompt is inert (krea2 runs at cfg 1, where ComfyUI
# never applies one), because on Qwen-Image lineage each of those words lands in
# POSITIVE conditioning and produces the very text it was meant to forbid. An
# earlier draft of this file named text five times and every one of the 25
# submissions came back 422. One mention, plus the positive phrasing, is the fix.
NO_TEXT = (
    "every surface smooth and unmarked, no lettering anywhere, "
    "no collage, no contact sheet, no border"
)

# krea2 is distilled for cfg 1, so the ComfyUI negative prompt never runs and this
# field is inert at render time -- kept short and conventional for the non-distilled
# engines this queue may later target. The real steering against krea2's failure
# mode on this brief (competent nature/portrait photography, which sank the first
# Cthulhuquarium batch on 2026-08-25) lives POSITIVELY in STYLE_TAIL instead.
NEGATIVE = (
    "photorealistic, photograph, 3d render, cgi, grimdark, "
    "blurry, low quality, deformed, extra limbs, bad hands, cropped"
)

# docs/art-direction.md Section 4.1 TIME_MOD, verbatim in substance.
TIME_MOD = {
    "day": (
        "warm high-key daylight from screen-left, clear midday color, "
        "gentle ambient shadows"
    ),
    "night": (
        "cool low-key moonlight from screen-right, deep blue shadows, "
        "small warm window and lantern glows"
    ),
    "dawn": (
        "soft cool-to-warm sunrise, low mist, glistening morning dew highlights"
    ),
    "golden": (
        "long warm golden-hour rake light, amber rim-lighting, drifting dust motes"
    ),
    "dusk": (
        "fading violet-orange sky, elongated cool shadows, first lanterns lit"
    ),
}

# The player character is cosmetic-only and fully customizable (data-model.md
# `ruler.cosmetics` + `honorific`), so there is no canonical ruler and the art must
# not imply one.
#
# The first concept batch got this wrong. It pinned ONE monarch across every vista
# so the four time-of-day pieces would read as the same person in the same place --
# consistency worth having -- but bought that consistency by making the ruler a
# specific man, and every hero mockup of the game then showed a king. Silas,
# 2026-08-26: "the ruler should absolutely not always be male in our mockups, and
# we will need to add a character creator element that lets the user pick body
# shapes, skin color, and ruler title, etc."
#
# The fix is to stop treating the ruler as a constant. These presets are the range
# the character creator has to cover -- gender presentation, body shape and size,
# skin, age, species, and honorific all vary deliberately, per the art-prompts
# casting standard. They are rendered at the `ruler` region layer's own framing, so
# each one is simultaneously: a swappable game asset, the reference sheet the
# character creator is built against, and the thing that keeps any future
# ruler-bearing mockup from defaulting to one body.
RULER_PRESETS = [
    {
        "id": "king-osric",
        "title": "King",
        "look": "a plump contented middle-aged monarch with deep brown skin and "
        "grey-streaked locs, a slightly-too-large crown sitting askew, robes "
        "hitched up over bare feet",
    },
    {
        "id": "queen-mabel",
        "title": "Queen",
        "look": "a tall broad-shouldered monarch in her fifties, warm brown skin, "
        "close-cropped silver hair under a slim gold circlet, an embroidered "
        "fishing coat thrown over her royal robes, sleeves rolled to the elbow",
    },
    {
        "id": "sovereign-wren",
        "title": "Sovereign",
        "look": "a lanky young androgynous monarch, pale freckled skin, dark hair "
        "shaved at the sides, the circlet worn loose around the throat instead of "
        "the head, patched waders under a half-cape",
    },
    {
        "id": "regent-halvard",
        "title": "Regent",
        "look": "a very old wiry monarch, deep-set eyes and a long white beard "
        "tucked into a belt, olive skin, swimming in robes several sizes too big, "
        "a folding stool and a thermos",
    },
    {
        "id": "matriarch-oshun",
        "title": "Matriarch",
        "look": "a short and gloriously round monarch, rich dark skin, an enormous "
        "coiled crown of braided hair with the actual crown perched on top of it, "
        "beaded rings on every finger",
    },
    {
        "id": "chieftain-brakka",
        "title": "Chieftain",
        "look": "a powerfully built orcish monarch, moss-green skin, small proud "
        "tusks, a crown of shed antlers, forearms like tree roots, a rod that looks "
        "like a toothpick in one huge hand",
    },
    {
        "id": "heron-queen-sedge",
        "title": "Queen",
        "look": "a tall heron-folk monarch, soft grey-blue plumage and a long "
        "elegant neck, the crown balanced carefully between two head plumes, "
        "standing on one leg out of sheer habit",
    },
    {
        "id": "little-monarch-pip",
        "title": "Monarch",
        "look": "a tiny mouse-folk monarch barely taller than a boot, round ears, "
        "warm tan fur, an enormous crown resting on both ears at once, seated on a "
        "stack of unread royal ledgers, holding a rod three times their length",
    },
]
RULER_BY_ID = {preset["id"]: preset for preset in RULER_PRESETS}

# The four time-of-day vistas are a matched set: one ruler across all of them is
# what makes the cycle read as one place. Named rather than inlined so the already
# rendered and approved pieces stay reproducible, and so swapping the hero is one
# edit. The alternate vistas below carry the range instead.
HERO_RULER_ID = "king-osric"
THE_RULER = RULER_BY_ID[HERO_RULER_ID]["look"] + (
    ", a battered fishing rod held with total unearned confidence"
)

RULER_FRAME = (
    "seated in profile on a worn wooden fishing perch at the edge of a lake, rod "
    "out over the water, entirely at peace, full figure visible against a simple "
    "soft painted backdrop, character sheet framing, consistent side-on pose"
)

LAKESIDE = (
    "a wide storybook lake behind a small castle, reeds and a worn wooden fishing "
    "perch in the foreground, forested far bank, a village edge and castle grounds "
    "stepping back in clear horizontal depth bands"
)

# ---------------------------------------------------------------------------
# Concept lane -- scenes and UI (no upstream source; edit here)
# ---------------------------------------------------------------------------

SCENE_CONCEPTS = [
    (
        "key-art-day",
        WIDE,
        "Ruler Hooked key art (day)",
        f"The core promise of the game in one frame: {THE_RULER}, sitting alone "
        f"at the edge of {LAKESIDE}, line in the water, blissfully ignoring the "
        "kingdom behind them. The whole scene is calm, inviting, and a little bit "
        f"of a joke at the monarch's expense. {TIME_MOD['day']}",
    ),
    (
        "key-art-golden",
        WIDE,
        "Ruler Hooked key art (golden hour)",
        f"The same lakeside vista: {THE_RULER} fishing at the edge of {LAKESIDE}, "
        "the kingdom quiet behind them, the water gone to hammered gold. A brief, "
        f"beautiful moment the player happens to catch. {TIME_MOD['golden']}",
    ),
    (
        "key-art-night",
        WIDE,
        "Ruler Hooked key art (night)",
        f"The same lakeside vista after dark: {THE_RULER} fishing at the edge of "
        f"{LAKESIDE}, a lantern hooked on the fishing perch, fireflies drifting over "
        "the reeds, warm windows glowing in the distant village and castle. "
        f"{TIME_MOD['night']}",
    ),
    (
        "key-art-dawn",
        WIDE,
        "Ruler Hooked key art (dawn)",
        f"The same lakeside vista at first light: {THE_RULER} already out fishing "
        f"before anyone can find them, at the edge of {LAKESIDE}, mist lying flat on "
        f"the water, every reed beaded with dew. {TIME_MOD['dawn']}",
    ),
    (
        "kingdom-preserved",
        WIDE,
        "Kingdom pole: preserved",
        "The nature end of the kingdom's hue axis: the same lakeside kingdom grown "
        "lush and wild. Tangled thriving forest crowding the far bank, an untouched "
        "reedy shoreline with a heron, a small tidy castle with a vegetable garden "
        "and a laundry line, a handful of thatched roofs. Lush greens and golden "
        f"warmth throughout. {TIME_MOD['day']}",
    ),
    (
        "kingdom-developed",
        WIDE,
        "Kingdom pole: developed",
        "The development end of the kingdom's hue axis: the same lakeside kingdom "
        "comically over-built by a warlock land developer. Crooked smokestacks and "
        "tin roofs crowding the far bank, purple-tinged smog puffs, tree stumps and "
        "stacked timber where the forest was, scaffolding and cranes over a cramped "
        "boomtown, one lonely ornamental tree. Cool greys, tin-roof browns, and "
        f"warlock-purple accents. Absurd rather than menacing. {TIME_MOD['day']}",
    ),
    (
        "kingdom-prosperous",
        WIDE,
        "Kingdom pole: prosperous",
        "The comfortable middle of the kingdom's hue axis: the same lakeside kingdom "
        "doing genuinely well. Tidy patchwork farmland rolling to the far waterline, "
        "a groomed woodland with a spaced healthy treeline and a druid cairn, a busy "
        "village edge with market awnings and a cart, blooming castle gardens and "
        f"banners and a fountain. Warm, content, and thriving. {TIME_MOD['day']}",
    ),
    (
        "beat-the-interruption",
        WIDE,
        "Story beat: the interruption",
        f"The core comedy beat of the game: {THE_RULER} is mid-cast at the lake when "
        "a breathless courier bursts through the reeds brandishing an enormous "
        "unrolled scroll, boot deep in mud, utterly urgent. The monarch does not "
        "look away from the water. Staged like a comic adventure game screen, the "
        "two figures reading instantly by silhouette alone",
    ),
    (
        "beat-the-standoff",
        WIDE,
        "Story beat: warlock versus druid",
        "The kingdom's signature choice, staged as a standoff at the edge of the "
        "north woods: on one side a horned purple-robed warlock land developer with "
        "a rolled blueprint and a genuinely reasonable expression, on the other a "
        "leaf-cloaked druid preservationist radiating serene absolute certainty. "
        "Between them, the disputed treeline. Both are charming, both are a little "
        "bit wrong, and neither is a villain",
    ),
    (
        "beat-the-catch",
        WIDE,
        "Story beat: the catch",
        f"{THE_RULER} hauling an absurd storybook fish out of the lake at the moment "
        "of triumph, both of them equally surprised. Water arcing off the line, rod "
        "bent double, crown falling off. The fish is characterful and strange rather "
        "than realistic, with a personality of its own",
    ),
    (
        "beat-the-escape",
        WIDE,
        "Story beat: the escape",
        "A monarch's morning routine: a castle corridor hung with heavy tapestries, "
        f"{THE_RULER} tiptoeing out of frame with a fishing rod and a tackle basket "
        "held behind their back, while a knot of courtiers, ledgers, and petitioners "
        "argue among themselves and fail entirely to notice",
    ),
]

# Alternate hero vistas. The four key-art pieces above deliberately share one
# ruler; these carry the range into the mockups themselves, so "what this game
# looks like" is never a single body. Different preset, different time, same place.
ALT_HERO_VISTAS = [
    ("queen-mabel", "golden", "Alternate key art: the Queen at golden hour"),
    ("sovereign-wren", "night", "Alternate key art: the Sovereign at night"),
    ("chieftain-brakka", "day", "Alternate key art: the Chieftain by day"),
    ("little-monarch-pip", "dawn", "Alternate key art: the little Monarch at dawn"),
]

UI_CONCEPTS = [
    (
        "ui-event-card",
        SQUARE,
        "UI concept: event card",
        "A painted storybook moment of a mud-spattered petitioner presenting a "
        "grievance at an open-air lakeside court, held inside a tall soft-cornered "
        "panel of warm parchment, with two wide carved-wood plaques below it whose "
        "faces are smooth blank polished wood. Warm parchment and painted wood "
        "materials, playful and inviting",
    ),
    (
        "ui-fishopedia-plate",
        SQUARE,
        "UI concept: Fishopedia specimen plate",
        "A single strange storybook fish painted as a naturalist's study, centered "
        "on warm aged paper with a soft vignette, a measuring rule laid beside it "
        "and clean empty paper below it. Warm hand-painted natural-history feel, "
        "every writing area left as bare paper",
    ),
    (
        "ui-title-screen",
        WIDE,
        "UI concept: title screen",
        "A concept for the title screen of a comedic fishing and kingdom-management "
        f"game: {THE_RULER} very small at the bottom of a huge warm lakeside vista, "
        "back to the viewer, line already in the water, the kingdom rising behind "
        "them in clear painted depth bands. The upper third is generous empty sky, "
        "bare open air and nothing else",
    ),
]

# ---------------------------------------------------------------------------
# Concept lane -- cast portraits (read from the kind_robots content bundle)
# ---------------------------------------------------------------------------

# Visual direction per cast slug: archetype-then-twist (art-direction.md Section 3),
# with the casting deliberately varied across gender, race, age, body size, and
# species. The character's own name/role/drive/quirks come from content.ts.
CAST_LOOK = {
    "warlock-vex": (
        "a horned purple-robed warlock land developer, mid-forties, broad and "
        "well-fed, olive skin, an immaculate waistcoat under the robes, a rolled "
        "blueprint tucked under one arm and a business card held out with the warm "
        "unforced smile of someone whose offer is genuinely quite good"
    ),
    "druid-sela": (
        "a leaf-cloaked druid preservationist, elderly, slight and wiry, dark brown "
        "skin, white hair full of twigs and moss, bare feet rooted into the ground, "
        "one finger raised mid-lecture with the serene absolute certainty of someone "
        "who has never once considered being wrong"
    ),
    "heir-robin": (
        "a teenaged royal heir, lanky and freckled, pale skin and copper hair, a "
        "circlet shoved into a pocket rather than worn, travelling boots already "
        "laced, halfway through climbing out of a window with an expression of "
        "pure delighted guilt"
    ),
    "sweetheart-ash": (
        "a young commoner angler, soft-bodied and broad-shouldered, warm tan skin, "
        "patched fishing waders and a too-big coat, cradling a bucket of fish and "
        "talking to it, nervous and kind and hopelessly earnest"
    ),
    "envoy-thistle": (
        "a foreign trade envoy, tall and imperious, deep brown skin, an elaborate "
        "high-collared travelling coat in a rival kingdom's colors, gloved hands "
        "folded, chin lifted, visibly counting under her breath while she waits"
    ),
    "taxman-gristle": (
        "a royal tax assessor, thin and stooped, grey pallor, spectacles down the "
        "nose, an enormous ledger open across both forearms, sighing audibly at "
        "something joyful happening just out of frame"
    ),
    "captain-cordelia": (
        "a castle guard captain, powerfully built and middle-aged, light brown skin, "
        "close-cropped grey hair, dented practical armor, absent-mindedly polishing "
        "one pauldron with her thumb while standing at rigid attention"
    ),
    "bard-fen": (
        "a travelling bard, small and round and gleeful, freckled brown skin, a "
        "riot of mismatched patterned layers, a battered lute swung mid-strum, "
        "clearly narrating someone else's private moment in rhyme without permission"
    ),
    "smuggler-brack": (
        "a lakeside smuggler, rangy and weathered, a bearded amphibian-folk fisher "
        "with mottled green skin and a long oilskin coat, one crate half-hidden "
        "behind a boot, squinting at a horizon that is not in this picture"
    ),
    "witch-mossy": (
        "a bog witch, enormously round and cheerful, silver-blue skin and hair like "
        "pond weed, layered in trade-beads and bottles and dried herbs, holding out "
        "a jar of something wonderful with the air of answering a question nobody asked"
    ),
    "lake-spirit-nix": (
        "an ancient lake spirit, a tall serene translucent figure of standing water "
        "and drifting silt, a face suggested rather than drawn, water grasses and "
        "old coins turning slowly inside the body, patient and unreadable"
    ),
}

PORTRAIT_FRAME = (
    "three-quarter character concept portrait against a simple soft painted "
    "backdrop, full head and torso, one clear pose that reads the character "
    "instantly, character sheet framing"
)


def expect_all(parsed, block_text, label, source, key="slug"):
    """Fail when a regex matched only SOME of a block's entries.

    A parser that silently returns a subset is worse here than one that crashes:
    the batch still stages, still renders, still looks successful, and the missing
    assets are only discovered when something reaches for one. That is the exact
    drift this whole script exists to prevent, so it must be loud.

    Caught this on the rewards block: three of nine entries had `effect:` wrapped
    onto its own line by prettier, the same-line regex skipped them, and the run
    reported a cheerful "6 entries" with no indication anything was missing.
    """
    declared = len(re.findall(rf"^\s*{key}: '", block_text, re.M))
    if not parsed:
        raise SystemExit(f"{label}: block in {source} parsed to zero entries")
    if len(parsed) != declared:
        got = {entry.get(key) or entry.get("key") for entry in parsed}
        missing = [
            m.group(1)
            for m in re.finditer(rf"^\s*{key}: '([^']+)'", block_text, re.M)
            if m.group(1) not in got
        ]
        raise SystemExit(
            f"{label}: {source} declares {declared} entr(ies) but the parser matched "
            f"{len(parsed)}. Unmatched: {', '.join(missing)}. The upstream formatting "
            f"changed -- fix the pattern rather than shipping a partial batch."
        )
    return parsed


def find_content_bundle() -> Path:
    for candidate in CONTENT_CANDIDATES:
        if candidate.is_file():
            return candidate
    raise SystemExit(
        "could not find kind_robots utils/rulerHooked/content.ts in any of: "
        + ", ".join(str(c) for c in CONTENT_CANDIDATES)
    )


CHARACTER_RE = re.compile(
    r"\{\s*slug: '(?P<slug>[^']+)',\s*"
    r"name: '(?P<name>[^']+)',\s*"
    r"honorific: '(?P<honorific>[^']+)',\s*"
    r"alignment: '(?P<alignment>[^']+)',\s*"
    r"role: '(?P<role>[^']+)',\s*"
    r"drive: '(?P<drive>[^']+)',\s*"
    r"quirks: '(?P<quirks>[^']+)',",
    re.S,
)


def read_cast(content_ts: Path) -> list[dict[str, str]]:
    """The CharacterRef list from the bundle, so a new character cannot miss art."""
    text = content_ts.read_text(encoding="utf-8")
    block = re.search(r"\n  characters: \[(.*?)\n  \],\n", text, re.S)
    if not block:
        raise SystemExit(f"no characters: [...] block found in {content_ts}")
    cast = [m.groupdict() for m in CHARACTER_RE.finditer(block.group(1))]
    expect_all(cast, block.group(1), "characters", content_ts)
    return cast


REGION_RE = re.compile(
    r"^\s{6}(?P<key>[a-z_]+): \{(?P<body>.*?)\},?\s*$",
    re.S | re.M,
)


def read_regions(content_ts: Path) -> dict[str, dict[str, list[str]]]:
    """The (region -> states, times) manifest the compositor actually resolves."""
    text = content_ts.read_text(encoding="utf-8")
    block = re.search(r"\n  regions: \{\n    regions: \{\n(.*?)\n    \},\n  \},\n", text, re.S)
    if not block:
        raise SystemExit(f"no regions manifest found in {content_ts}")
    body = block.group(1)
    # Split on top-level "    key: {" entries (six-space indent inside the manifest).
    regions: dict[str, dict[str, list[str]]] = {}
    for match in re.finditer(r"^      (?P<key>[a-z_]+): \{", body, re.M):
        key = match.group("key")
        start = match.end()
        depth = 1
        index = start
        while index < len(body) and depth:
            if body[index] == "{":
                depth += 1
            elif body[index] == "}":
                depth -= 1
            index += 1
        chunk = body[start : index - 1]
        states = re.search(r"states: \[(.*?)\]", chunk, re.S)
        times = re.search(r"times: \[(.*?)\]", chunk, re.S)
        regions[key] = {
            "states": re.findall(r"'([^']+)'", states.group(1)) if states else [],
            "times": re.findall(r"'([^']+)'", times.group(1)) if times else [],
        }
    if not regions:
        raise SystemExit(f"regions manifest in {content_ts} parsed to zero regions")
    return regions


# BASE strings per (region, state), from docs/art-direction.md Section 5.
REGION_BASE = {
    ("sky", "open"): (
        "wide empty storybook sky over a lakeside kingdom, soft clouds, distant birds, "
        "nothing but atmosphere"
    ),
    ("far_shore", "pristine"): (
        "the far bank of a calm lake seen across the water, untouched wild shoreline, "
        "reeds, a heron, soft forest edge"
    ),
    ("far_shore", "farmed"): (
        "the far bank of a calm lake as tidy patchwork farmland rolling to the "
        "waterline, little fences and haystacks, friendly and cultivated"
    ),
    ("far_shore", "industrial"): (
        "the far bank of a calm lake crowded with goofy warlock-financed development, "
        "crooked smokestacks, tin roofs, purple-tinged smog puffs, comically over-built"
    ),
    ("treeline", "wild"): (
        "a lush overgrown forest band, tall tangled trees, dappled canopy, hidden "
        "critter eyes, thriving"
    ),
    ("treeline", "tended"): (
        "a groomed woodland band, spaced healthy trees, a tidy path, a druid cairn, "
        "cared-for and calm"
    ),
    ("treeline", "logged"): (
        "a thinned forest band with fresh stumps and stacked timber, a few survivor "
        "trees, wistful, mid-transformation"
    ),
    ("treeline", "overbuilt"): (
        "a former forest band replaced by cheerful cramped cottages and scaffolding, "
        "one lonely ornamental tree, goofy sprawl"
    ),
    ("village_edge", "hamlet"): (
        "a tiny cluster of thatched rooftops at a settlement fringe, smoke curls, "
        "a well, sleepy and small"
    ),
    ("village_edge", "township"): (
        "a growing village edge, more rooftops, a market awning, a cart, busier "
        "and prosperous"
    ),
    ("village_edge", "boomtown"): (
        "a bustling overgrown town edge crammed with mismatched buildings, cranes, "
        "banners, comically booming"
    ),
    ("castle_grounds", "humble"): (
        "modest royal grounds beside a lake, a small tidy castle, a vegetable garden, "
        "a laundry line, cozy and unpretentious"
    ),
    ("castle_grounds", "flourishing"): (
        "well-kept royal grounds, blooming gardens, banners, a fountain, content "
        "and thriving"
    ),
    ("castle_grounds", "gaudy"): (
        "wildly over-decorated royal grounds, gold statues of a monarch fishing, "
        "too many fountains, endearingly tacky"
    ),
    ("lake", "clear"): (
        "the sparkling near surface of a lake, gentle ripples, reflections, "
        "jumping fish"
    ),
    ("near_bank", "grassy"): (
        "a worn grassy near bank with reeds, a wooden fishing perch, a tackle basket, "
        "trodden footpath"
    ),
    ("ruler", "fishing"): (
        f"{THE_RULER}, seated in profile on a fishing perch, line in the water, "
        "entirely at peace"
    ),
}

# Per art-direction.md Section 2 and the contract t-017 settled: the layer occupies
# its own horizontal depth band and the rest of the frame is empty, so the layers
# register against one another on one canvas. Stated as the wanted result ("the
# rest of the frame empty") rather than as an exclusion pile, per the prompt
# contract -- and "transparent" is deliberately avoided as a prompt word, since a
# diffusion model renders a checkerboard when asked for transparency.
LAYER_TAIL = (
    "a single horizontal depth band of scenery running edge to edge across the "
    "frame, the rest of the frame empty flat open sky, flat-ish banded depth, "
    "scenery only, at most a few tiny ambient background figures"
)


def concept_entries(cast: list[dict[str, str]]) -> list[dict]:
    entries: list[dict] = []

    for key, size, label, body in SCENE_CONCEPTS + UI_CONCEPTS:
        entries.append(
            make_entry(
                request_id=f"ruler-hooked-concept-{key}",
                image_path=f"public/images/ruler-hooked/concept/{key}.webp",
                label=f"Ruler Hooked concept: {label}",
                size=size,
                prompt=f"{body}. {STYLE_TAIL}. {NO_TEXT}",
                priority=CONCEPT_PRIORITY,
                lane="concept",
            )
        )

    for character in cast:
        slug = character["slug"]
        look = CAST_LOOK.get(slug)
        if not look:
            raise SystemExit(
                f"cast member {slug!r} is in content.ts but has no CAST_LOOK entry; "
                "add its visual direction to this script"
            )
        body = (
            f"Character concept art for {character['name']} {character['honorific']}, "
            f"{character['role']} in a comedic fantasy kingdom: {look}. "
            f"The character reads instantly as their archetype and then undercuts it: "
            f"they want {character['drive']}, and {character['quirks']}. "
            f"{PORTRAIT_FRAME}"
        )
        entries.append(
            make_entry(
                request_id=f"ruler-hooked-character-{slug}",
                image_path=f"public/images/ruler-hooked/characters/{slug}.webp",
                label=f"Ruler Hooked cast: {character['name']} {character['honorific']}",
                size=PORTRAIT,
                prompt=f"{body}. {STYLE_TAIL}. {NO_TEXT}",
                priority=CONCEPT_PRIORITY,
                lane="concept",
            )
        )

    return entries


# Ruler Hooked and Cthulhuquarium share a creature catalog, and docs/fish-ecology.md
# is explicit that a shared species keeps one recognizable design across both games
# while each game may need its own presentation variant. These are the `bestiary`
# variant: the species design itself, which every later variant (catch card, lake
# context, silhouette) is derived from. Getting the design right once, first, is
# what stops the two games drifting into near-duplicate species.
FISH_FRAME = (
    "a single fish specimen study, the whole creature clearly visible in profile "
    "against soft open water, nothing else competing for attention in the frame"
)


def fish_entries() -> list[dict]:
    """Species designs for the vertical-slice roster, read from the roster file."""
    if not FISH_ROSTER.is_file():
        raise SystemExit(f"fish roster not found at {FISH_ROSTER}")
    roster = yaml.safe_load(FISH_ROSTER.read_text(encoding="utf-8")) or {}
    fish = roster.get("fish") or []
    if not fish:
        raise SystemExit(f"{FISH_ROSTER} parsed to zero fish")

    entries: list[dict] = []
    for species in fish:
        slug = str(species["slug"])
        # `silhouette` and `distinction` are already written as visual direction --
        # use them verbatim rather than paraphrasing, so the roster stays the single
        # source and an edit there reaches the art without passing through a person.
        body = (
            f"{species['name']}, a fantastical freshwater fish in a comedic fantasy "
            f"kingdom: {species['silhouette']}. "
            f"{' '.join(str(species['distinction']).split())} "
            f"{FISH_FRAME}"
        )
        entries.append(
            make_entry(
                request_id=f"ruler-hooked-fish-{slug}",
                image_path=f"public/images/ruler-hooked/fish/{slug}/bestiary.webp",
                label=f"Ruler Hooked fish: {species['name']} ({species['affinity']}, {species['rarity']})",
                size=WIDE,
                prompt=f"{body}. {STYLE_TAIL}. {NO_TEXT}",
                priority=CONCEPT_PRIORITY,
                lane="fish",
            )
        )
    return entries


def ruler_entries() -> list[dict]:
    """One piece per ruler preset, at the `ruler` layer's own framing.

    Three jobs at once: the swappable ruler asset, the reference sheet the
    character creator is built against, and the guarantee that the range exists
    as art rather than only as an intention in a design doc.
    """
    entries: list[dict] = []
    for preset in RULER_PRESETS:
        body = (
            f"The player-character ruler of a comedic fantasy kingdom, who would "
            f"rather fish than rule: {preset['look']}, holding a battered fishing "
            f"rod with total unearned confidence. {RULER_FRAME}"
        )
        entries.append(
            make_entry(
                request_id=f"ruler-hooked-ruler-{preset['id']}",
                image_path=f"public/images/ruler-hooked/ruler/{preset['id']}.webp",
                label=f"Ruler Hooked ruler preset: {preset['title']} ({preset['id']})",
                size=PORTRAIT,
                prompt=f"{body}. {STYLE_TAIL}. {NO_TEXT}",
                priority=CONCEPT_PRIORITY,
                lane="ruler",
            )
        )
    return entries


def alt_vista_entries() -> list[dict]:
    """Key-art vistas featuring rulers other than the hero preset."""
    entries: list[dict] = []
    for preset_id, time, label in ALT_HERO_VISTAS:
        preset = RULER_BY_ID[preset_id]
        body = (
            f"The core promise of the game in one frame: {preset['look']}, holding "
            f"a battered fishing rod, sitting alone at the edge of {LAKESIDE}, line "
            f"in the water, blissfully ignoring the kingdom behind them. "
            f"{TIME_MOD[time]}"
        )
        entries.append(
            make_entry(
                request_id=f"ruler-hooked-concept-key-art-{preset_id}",
                image_path=f"public/images/ruler-hooked/concept/key-art-{preset_id}.webp",
                label=f"Ruler Hooked concept: {label}",
                size=WIDE,
                prompt=f"{body}. {STYLE_TAIL}. {NO_TEXT}",
                priority=CONCEPT_PRIORITY,
                lane="concept",
            )
        )
    return entries


REWARD_FRAME = (
    "a single object presented alone and centered against a simple soft painted "
    "backdrop, clear readable silhouette, nothing else in the frame"
)


def reward_entries(content_ts: Path) -> list[dict]:
    """One object study per Reward in the content bundle, read from the bundle."""
    text = content_ts.read_text(encoding="utf-8")
    block = re.search(r"\n  rewards: \[(.*?)\n  \],\n", text, re.S)
    if not block:
        raise SystemExit(f"no rewards: [...] block found in {content_ts}")
    pattern = re.compile(
        r"\{\s*slug: '(?P<slug>[^']+)',\s*"
        r"name: '(?P<name>[^']+)',\s*"
        r"rewardType: '(?P<kind>[^']+)',\s*"
        r"rarity: '(?P<rarity>[^']+)',\s*"
        r"effect:\s*'(?P<effect>[^']+)',",
        re.S,
    )
    rewards = [m.groupdict() for m in pattern.finditer(block.group(1))]
    expect_all(rewards, block.group(1), "rewards", content_ts)

    entries: list[dict] = []
    for reward in rewards:
        name = reward["name"].replace("\u2019", "'")
        effect = reward["effect"].replace("\u2019", "'")
        # SKILL rewards have no physical form of their own, so they are rendered as
        # the token or charm that represents them rather than as an abstract glow.
        body = (
            f"{name}, a {reward['rarity'].lower()} keepsake from a comedic fantasy "
            f"fishing kingdom. What it does: {effect} Render it as one tangible "
            f"hand-made object a person could pick up. {REWARD_FRAME}"
        )
        entries.append(
            make_entry(
                request_id=f"ruler-hooked-reward-{reward['slug']}",
                image_path=f"public/images/ruler-hooked/rewards/{reward['slug']}.webp",
                label=f"Ruler Hooked reward: {name} ({reward['kind']}, {reward['rarity']})",
                size=SQUARE,
                prompt=f"{body}. {STYLE_TAIL}. {NO_TEXT}",
                priority=CONCEPT_PRIORITY,
                lane="reward",
            )
        )
    return entries


def ending_entries(content_ts: Path) -> list[dict]:
    """One closing illustration per authored ending, read from the bundle.

    The ending's own `body` line is the art direction: it is already one vivid
    sentence about what the kingdom became, which is exactly what the picture is.
    """
    text = content_ts.read_text(encoding="utf-8")
    block = re.search(r"\n  endings: \[(.*?)\n  \],\n\}", text, re.S)
    if not block:
        raise SystemExit(f"no endings: [...] block found in {content_ts}")
    pattern = re.compile(
        r"outcomeKey: '(?P<key>[^']+)',\s*"
        r"victoryType: '(?P<victory>[^']+)',\s*"
        r"title: '(?P<title>[^']+)',\s*"
        r"body: '(?P<body>[^']+)',",
        re.S,
    )
    endings = [m.groupdict() for m in pattern.finditer(block.group(1))]
    expect_all(endings, block.group(1), "endings", content_ts, key="outcomeKey")

    entries: list[dict] = []
    for ending in endings:
        title = ending["title"].replace("\u2019", "'")
        line = ending["body"].replace("\u2019", "'").replace("\u2026", "...")
        body = (
            f"The closing image of a comedic fantasy fishing kingdom, titled "
            f"{title}: {line} Show the kingdom and its lake as that sentence leaves "
            f"them, wide and final and a little wistful"
        )
        entries.append(
            make_entry(
                request_id=f"ruler-hooked-ending-{ending['key']}",
                image_path=f"public/images/ruler-hooked/endings/{ending['key']}.webp",
                label=f"Ruler Hooked ending: {title} ({ending['victory']})",
                size=WIDE,
                prompt=f"{body}. {STYLE_TAIL}. {NO_TEXT}",
                priority=CONCEPT_PRIORITY,
                lane="ending",
            )
        )
    return entries


def layer_entries(regions: dict[str, dict[str, list[str]]]) -> list[dict]:
    """The (region, state, time) matrix, named exactly as assetCandidates() resolves."""
    entries: list[dict] = []
    for region, spec in regions.items():
        for state in spec["states"]:
            base = REGION_BASE.get((region, state))
            if not base:
                raise SystemExit(
                    f"region state {region}/{state} is in the manifest but has no "
                    "REGION_BASE prompt; add it to this script"
                )
            for time in spec["times"] or [None]:
                stem = f"{region}-{state}" + (f"-{time}" if time else "")
                lighting = f". {TIME_MOD[time]}" if time else ""
                entries.append(
                    make_entry(
                        request_id=f"ruler-hooked-layer-{stem}",
                        image_path=f"public/images/ruler-hooked/{stem}.webp",
                        label=f"Ruler Hooked layer: {stem}",
                        size=WIDE,
                        prompt=f"{base}{lighting}. {LAYER_TAIL}. {STYLE_TAIL}. {NO_TEXT}",
                        priority=LAYER_PRIORITY,
                        lane="layer",
                    )
                )
    return entries


def make_entry(*, request_id, image_path, label, size, prompt, priority, lane) -> dict:
    return {
        "id": request_id,
        "source": "ruler-hooked",
        "status": "pending",
        "priority": priority,
        "target_repo": TARGET_REPO,
        "project_slug": "ruler-hooked",
        "lane": lane,
        "image_path": image_path,
        "source_url": f"{MEDIA_ORIGIN}/{image_path[len('public/'):]}",
        "page_url": PAGE_URL,
        "variant": "image",
        "label": label,
        "engine": ENGINE,
        "size": size,
        "negative_prompt": NEGATIVE,
        "prompt": " ".join(prompt.split()),
    }


# ---------------------------------------------------------------------------
# Local mirror of kind_robots server/utils/artPromptContract.ts
# ---------------------------------------------------------------------------
#
# The enqueue endpoint rejects a contract-violating prompt with a 422, one job at
# a time, after the batch is already staged. Checking here instead turns "25
# failed submissions and a puzzled read of the server source" into a failure at
# build time, which is the same trade the contract's own header argues for.
# Mirror only -- kind_robots is authoritative; if a rule changes there, change it
# here in the same commit.

TEXT_EXCLUSION_NOUNS = {
    "text", "lettering", "letters", "words", "wording", "logo", "logos",
    "watermark", "watermarks", "signature", "signatures", "caption", "captions",
    "typography", "writing",
}
MAX_TEXT_EXCLUSIONS = 4
NEGATION_CLAUSE = re.compile(
    r"\bno[ -](?:readable |visible |legible |written |accidental )?([a-z][a-z-]*)",
    re.I,
)
CONDITIONAL_PATTERNS = [
    r"\bonly (?:when|if)\b",
    r"\bwhen (?:the )?(?:subject|scene|context)\b",
    r"\b(?:if|unless) (?:the )?(?:subject|scene|context|prompt)\b",
    r"\bwhere (?:appropriate|relevant|applicable)\b",
    r"\bas (?:needed|appropriate)\b",
    r"\b(?:when|if|where|whenever|unless)\s+(?:any\s+|some\s+|the\s+|no\s+)?"
    r"(?:figures?|people|persons?|characters?|humans?|robots?|creatures?|bystanders?|"
    r"crowds?|onlookers?)\s+(?:do\s+|are\s+|is\s+)?"
    r"(?:appear|present|shown|show up|included|visible|featured|depicted)\b",
]
FORMAT_PATTERNS = [
    r"\b(?:trading[- ])?card (?:illustration|artwork|composition|art)\b",
    r"\b(?:treasure|ability|item|reward)[- ]card\b",
    r"\b(?:movie |film |book )?(?:poster|book cover|magazine cover|album cover)\b"
    r"(?!\s+(?:composition|framing|layout|crop))",
    r"\bcomic (?:page|panel|strip)\b",
]
VAGUE_BRAND_STYLE = (
    r"\b(?:(?:rich|cohesive|friendly)\s+)?Kind Robots\s+(?:visual\s+)?(?:style|language)\b"
)


def contract_violations(prompt: str) -> list[str]:
    """Every reason kind_robots' enqueue endpoint would 422 this prompt."""
    found: list[str] = []

    for pattern in CONDITIONAL_PATTERNS:
        match = re.search(pattern, prompt, re.I)
        if match:
            found.append(f"conditional-instruction: {match.group(0)!r}")

    for pattern in FORMAT_PATTERNS:
        match = re.search(pattern, prompt, re.I)
        if not match:
            continue
        before = prompt[max(0, match.start() - 12) : match.start()].lower()
        if re.search(r"\b(?:no|not|without|avoid|never)\s+[a-z-]*\s*$", before):
            continue  # excluding a format is the opposite of requesting one
        found.append(f"format-vocabulary: {match.group(0)!r}")

    if re.search(VAGUE_BRAND_STYLE, prompt, re.I):
        found.append("vague-brand-style")

    # ENGINE is krea2 throughout, which runs at cfg 1 -- guidance is inert, so
    # every exclusion lands in positive conditioning.
    piles = [
        m.group(0)
        for m in NEGATION_CLAUSE.finditer(prompt)
        if (m.group(1) or "").lower() in TEXT_EXCLUSION_NOUNS
    ]
    if len(piles) > MAX_TEXT_EXCLUSIONS:
        found.append(f"text-exclusion-pile: {len(piles)} ({', '.join(piles)})")

    return found


def assert_contract(entries: list[dict]) -> None:
    bad = [(e["id"], v) for e in entries for v in [contract_violations(e["prompt"])] if v]
    if not bad:
        return
    for request_id, violations in bad:
        print(f"CONTRACT VIOLATION {request_id}:", file=sys.stderr)
        for violation in violations:
            print(f"    {violation}", file=sys.stderr)
    raise SystemExit(
        f"{len(bad)} prompt(s) would be rejected at enqueue; fix them before staging."
    )


def staged_ids(text: str) -> set[str]:
    data = yaml.safe_load(text) or {}
    return {
        str(r.get("id"))
        for r in (data.get("requests") or [])
        if isinstance(r, dict) and r.get("id")
    }


def render_block(entries: list[dict]) -> str:
    """YAML for the new entries only, appended so the curated header survives."""
    return yaml.safe_dump(
        entries,
        sort_keys=False,
        allow_unicode=True,
        width=100,
        default_flow_style=False,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="append new entries")
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit 1 if any entry this script would produce is not staged yet",
    )
    parser.add_argument(
        "--include-layers",
        action="store_true",
        help="also emit the region/state/time environment matrix (see the "
        "LAYER FORMAT CONFLICT note in this script's docstring first)",
    )
    args = parser.parse_args()

    content_ts = find_content_bundle()
    entries = (
        concept_entries(read_cast(content_ts))
        + alt_vista_entries()
        + ruler_entries()
        + fish_entries()
        + reward_entries(content_ts)
        + ending_entries(content_ts)
    )
    if args.include_layers:
        entries += layer_entries(read_regions(content_ts))
    assert_contract(entries)

    text = ART_PROMPTS.read_text(encoding="utf-8")
    existing = staged_ids(text)
    fresh = [e for e in entries if e["id"] not in existing]

    print(f"source bundle: {content_ts}")
    print(f"built {len(entries)} entr(ies); {len(fresh)} not yet staged")
    for entry in fresh:
        print(f"  + {entry['id']}  [{entry['lane']}, {entry['size']}]")

    if args.check:
        if fresh:
            print(
                f"CHECK FAILED: {len(fresh)} entr(ies) missing from "
                f"{ART_PROMPTS.relative_to(REPO)}",
                file=sys.stderr,
            )
            return 1
        print("CHECK OK: every entry is staged.")
        return 0

    if not fresh:
        print("nothing to stage.")
        return 0

    if not args.write:
        print("dry run; pass --write to stage these into art-prompts.yaml")
        return 0

    if not text.endswith("\n"):
        text += "\n"
    ART_PROMPTS.write_text(text + render_block(fresh), encoding="utf-8")
    print(f"staged {len(fresh)} entr(ies) into {ART_PROMPTS.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
