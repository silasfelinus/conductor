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
  console  -- the paintings the 2026-11-05 illustrated console redesign
              expects: screen backdrops, tab vignettes, daily-proclamation
              scenes and shop still lifes, at the exact image_path keys the
              kind_robots UI resolves. Silas's direction for it (an art-heavy
              design that does not look like a webapp, but not shiny freeware
              either) is docs/art-direction.md Section 9; CONSOLE_FINISH is
              that section in executable form.

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
    python scripts/build_ruler_hooked_art_queue.py --write --lane ruler   # stage one lane only
    python scripts/build_ruler_hooked_art_queue.py --write --lane console # the console redesign art
    python scripts/build_ruler_hooked_art_queue.py --list-lanes           # staged/unstaged per lane
    python scripts/build_ruler_hooked_art_queue.py --include-layers --list-lanes

LANE FILTER (ruler-hooked/t-036). `--write` with no `--lane` stages every not-yet-
staged entry across every lane -- fine for a fresh full build, but "stage the one
lane I just fixed" and "stage everything not yet staged" used to be the same
command, so a targeted fix could accidentally sweep in unrelated, deliberately
unstaged entries from other lanes too (ruler-hooked/t-025's first attempt did
exactly this: restaging 12 corrected `ruler` entries also staged 81 unrelated
concept/fish/reward/ending/card entries, caught only by eyeballing `git diff
--stat` before it shipped). Pass `--lane <name>` to scope `--write`/`--check` to
one lane at a time; omit it for the old stage-everything behavior.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from art_prompt_conditional_check import conditional_instruction_violations  # noqa: E402

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

# Every lane value an *_entries() function can hand to make_entry() -- kept as one
# set so --lane's choices and this being out of sync fail loudly instead of
# silently accepting a lane that never matches anything.
LANES = {"concept", "fish", "ruler", "reward", "ending", "card", "layer", "console"}
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
# TWO WORDS WERE DOING REAL DAMAGE HERE, both the same mistake in different
# clothes: vocabulary that means something to a person and something else
# entirely to a diffusion model, which has no notion of "craft term" and simply
# paints the densest noun phrase it is handed.
#
# 1. "strong readable silhouettes" -- a composition note to an illustrator, a
#    SUBJECT to Krea 2. The reward batch came back as literal black cut-out
#    silhouettes on painted backdrops (ArtJob 9958, druid-charm, and others).
#    The word appeared twice, here and in the reward frame, which only made it
#    louder. Say the wanted result -- shapes that read at a glance -- and never
#    the word.
#
# 2. The named reference points. docs/art-direction.md Section 1 lists Monkey
#    Island, Bakshi, Treasure Planet, Steven Universe and She-Ra as shorthand
#    FOR HUMANS about what the look should feel like. Pasted verbatim into a
#    prompt they stop being shorthand and start being instructions to reproduce
#    those properties -- and when a subject name collides with a character from
#    one of them, you get the character. `nix-pearl` ("Nix's Pearl") plus
#    "Steven Universe" returned a direct likeness of that show's Pearl. That is
#    both an obvious quality failure and an IP one, and it was entirely
#    predictable in hindsight.
#
# The fix is to say what those names were shorthand for. Every quality below is
# one of the five, translated: comedic staging and clear read (Monkey Island),
# loose characterful line (Bakshi), painterly depth and warm cinematic light
# (Treasure Planet), soft rounded shapes and emotionally legible faces (Steven
# Universe), bold clean colour blocking and heroic-goofy fantasy (She-Ra). The
# doc keeps the names, because the doc is read by people. The prompt does not.
STYLE_TAIL = (
    "cartoony goofy storybook illustration, soft confident hand-drawn linework, "
    "loose characterful line quality, rounded generous shape language, "
    "emotionally legible faces, bold clean colour blocking, "
    "warm saturated slightly-faded storybook palette, "
    "painterly depth and warm cinematic light, exaggerated expressive acting, "
    "clearly staged so the shapes read instantly at a glance, "
    "heroic and goofy and wry, charming, "
    "hand-drawn animation cel and gouache painting, visibly illustrated by a person"
)

# Stated as the wanted RESULT, not as a pile of exclusions. kind_robots'
# server/utils/artPromptContract.ts rejects more than four text-nouns-after-"no"
# on an engine whose negative prompt is inert (krea2 runs at cfg 1, where ComfyUI
# never applies one), because on Qwen-Image lineage each of those words lands in
# POSITIVE conditioning and produces the very text it was meant to forbid. An
# earlier draft of this file named text five times and every one of the 25
# submissions came back 422. One mention, plus the positive phrasing, is the fix.
# Every negation removed, not just trimmed below the contract threshold. Krea 2
# runs at cfg 1 where ComfyUI never applies a negative prompt, so "no lettering
# anywhere" is the word "lettering" in POSITIVE conditioning on a text-specialist
# model -- and the reward batch proved it: `smugglers-map` came back as a scroll
# covered in garbled pseudo-writing that was visibly trying to spell out the
# prompt's own sentences. State the wanted result and nothing else.
NO_TEXT = (
    "every surface left bare and unmarked, blank clean untouched surfaces, "
    "one single uncropped image filling the frame"
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
    # Child rulers, added 2026-08-26 on Silas's read of the first eight: "we can do
    # little boy and girl, middle aged, and old rulers". The eight above already ran
    # young-adult to elderly; a ruler who is actually a CHILD was the real gap, and
    # it is the most on-theme age the premise has -- a kid who would rather fish
    # than rule is not shirking, which makes the joke land differently and better.
    #
    # Deliberately a spread rather than a boy/girl pair: Silas flagged the binary
    # himself ("I hate to be binary") in the same breath as asking for both, so the
    # set answers the ask and keeps going past it.
    {
        "id": "boy-king-tobin",
        "title": "King",
        "look": "a small boy king of about eight, pale skin and a mop of red hair, "
        "a crown far too big for him pushed back off his forehead, ceremonial robes "
        "puddling around him, feet nowhere near the ground and swinging",
    },
    {
        "id": "girl-queen-marisol",
        "title": "Queen",
        "look": "a small girl queen of about nine, warm brown skin and two tight "
        "buns, a gap-toothed look of total concentration, a crown pinned firmly in "
        "place because she checked, sleeves shoved up past her elbows",
    },
    {
        "id": "cub-prince-bramble",
        "title": "Prince",
        "look": "a bear-cub-folk child ruler, round and shaggy in brown fur, a "
        "circlet of woven river-reeds instead of gold, enormous paws entirely "
        "unsuited to a delicate reel, deeply serious about the task",
    },
    {
        "id": "elder-tortoise-yew",
        "title": "Sovereign",
        "look": "an immensely old tortoise-folk sovereign, mossy shell and a "
        "kindly wrinkled face, a crown worn smooth by centuries, moving at a pace "
        "that suggests the fish will simply have to wait",
    },
]
RULER_BY_ID = {preset["id"]: preset for preset in RULER_PRESETS}

# The player's appearance is an opening-screen choice, never a canonical face
# in lake, kingdom, scene, catch or card artwork. Preset portraits are the only
# art lane allowed to show the player's ruler.
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
        f"A first-person viewpoint at the lakeside fishing station: {LAKESIDE}, an empty weathered "
        "fishing perch at the near bank, an idle fishing rod leaning against "
        "its rail, busy distant subjects visible across the lake. "
        f"Warm storybook exploration, wide visual game scene. {TIME_MOD['day']}",
    ),
    (
        "key-art-golden",
        WIDE,
        "Ruler Hooked key art (golden hour)",
        f"The same tranquil lakeside kingdom viewed from its fishing perch: {LAKESIDE}, "
        "the water like hammered gold, the near fishing basket and rod "
        "awaiting their unseen owner. "
        f"{TIME_MOD['golden']}",
    ),
    (
        "key-art-night",
        WIDE,
        "Ruler Hooked key art (night)",
        f"First-person view across {LAKESIDE} after dark, a lantern "
        "hooked on an unoccupied fishing perch and distant village windows "
        "glowing over the water. "
        f"{TIME_MOD['night']}",
    ),
    (
        "key-art-dawn",
        WIDE,
        "Ruler Hooked key art (dawn)",
        f"The peaceful lakeside kingdom from a fisher's eye level, {LAKESIDE}, "
        "mist over the lake, empty fishing perch, every reed jeweled with dew. "
        f"{TIME_MOD['dawn']}",
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
        "First-person eye-level view from a lakeside fishing perch: "
        "a breathless courier splashes through the reeds brandishing an "
        "enormous urgent scroll, boot deep in mud. The scroll and the "
        "petitioner's expressive face dominate the frame, with open "
        "water beyond. Cinematic illustrated NPC interruption.",
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
        "An enormous absurd storybook fish bursting from the lake at "
        "the end of a taut line coming from below the frame, water "
        "arcing spectacularly across a sunny lakeside kingdom. "
        "First-person catch reveal, the fish fills the picture with "
        "a brilliantly comic surprised expression.",
    ),
    (
        "beat-the-escape",
        WIDE,
        "Story beat: the escape",
        "A castle corridor hung with heavy tapestries: a bewildered knot "
        "of courtiers, petitioners and royal clerks argue over ledgers "
        "while a side door stands ajar, sunlight and lake reeds showing "
        "the secret route outdoors. Scene staged from the "
        "departing fisher's eye level, populated by NPCs only.",
    ),
]

# Alternate ruler-bearing lake mockups are retired. The twelve playable
# appearances belong to the in-game coronation portrait gallery only.

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
        "A large illustrated cinematic title screen for a comedic fishing and "
        "kingdom-management game: unoccupied royal fishing perch in the foreground "
        "of a grand warm lakeside vista, an unattended fishing rod, the kingdom "
        "rising behind in clear painted depth bands. The upper third is broad "
        "empty golden sky for UI lettering. First-person staging: the viewer remains outside the picture, never "
        "pictured as a character",
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

# The advisor is a person, not a pen: Quill is the steward's name.
STEWARD_LOOK = (
    "Quill the Steward, the castle's wry, devoted steward and royal advisor, a "
    "lanky older person with silver-streaked dark hair tied back, a long beaked "
    "nose, half-moon spectacles, an ink-stained plum-and-gold household livery "
    "coat with a ring of castle keys, cradling an enormous ledger under one arm "
    "and holding a feather quill pen like a conductor's baton, one eyebrow raised "
    "in fond exasperation"
)

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
# Singular "the whole creature" is correct for nearly every entry, but a species whose
# silhouette is a multi-body composition (e.g. choirfish's trio) needs its own frame text
# instead -- ruler-hooked/t-019 found the singular phrasing here silently overriding a
# multi-body silhouette on every render regardless of how explicit the silhouette wording
# was. Set a species-level `frame_override` in vertical-slice.yaml rather than editing this
# shared constant.
FISH_FRAME = (
    "a clean specimen study, the whole creature clearly visible in profile "
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
        frame = species.get("frame_override") or FISH_FRAME
        body = (
            f"{species['name']}, a fantastical freshwater fish in a comedic fantasy "
            f"kingdom: {species['silhouette']}. "
            f"{' '.join(str(species['distinction']).split())} "
            f"{frame}"
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
    """Opening ceremony portraits only. These never enter the world compositor."""
    entries: list[dict] = []
    for preset in RULER_PRESETS:
        body = (
            f"Coronation portrait for the in-game character creator: "
            f"{preset['look']}. Full-length illustrated character study, "
            f"crowned subject alone with an expressive face, formal "
            f"portrait staging and rich ceremonial fabric. {PORTRAIT_FRAME}"
        )
        entries.append(
            make_entry(
                request_id=f"ruler-hooked-ruler-{preset['id']}",
                image_path=f"public/images/ruler-hooked/ruler-{preset['id']}.webp",
                label=f"Ruler Hooked opening portrait: {preset['title']} ({preset['id']})",
                size=PORTRAIT,
                prompt=f"{body}. {STYLE_TAIL}. {NO_TEXT}",
                priority=CONCEPT_PRIORITY,
                lane="ruler",
            )
        )
    return entries


def alt_vista_entries() -> list[dict]:
    """Retired: alternative rulers must never appear in gameplay scenery."""
    return []


REWARD_FRAME = (
    "a single object presented alone and centered against a simple soft painted "
    "backdrop, lit so its shape reads instantly, nothing else in the frame"
)

# Per-slug visual direction, because a reward's name and its mechanical effect
# are not a description of what the thing LOOKS like -- and four of these nine
# are objects that carry writing in real life, which is exactly how the first
# batch produced a chart covered in garbled pseudo-text. Each of those is given
# abstract marks to draw instead, positively, rather than being told not to
# write.
REWARD_LOOK = {
    "druid-charm": "a small woven charm of braided river reeds and green twine, "
    "a polished acorn and a single blue feather bound into it",
    "gilded-lure": "an ornate gold fishing lure shaped like a fat little fish, "
    "jewelled eye, three barbed hooks, far too fancy for its job",
    "buildpermit-scroll": "a stiff official scroll half unrolled, its face "
    "covered in neat abstract ruled boxes, inked squiggles and a heavy blob of "
    "purple wax seal, patterned marks instead of writing",
    "treaty-seal": "a heavy wax seal disc on a trailing ribbon, an abstract "
    "crest of two clasped hands pressed into the wax, no lettering in the stamp",
    "smugglers-map": "a creased weathered chart, its face covered in wandering "
    "ink coastlines, dotted route lines, tiny drawn coves and small crosses, "
    "abstract cartographic marks instead of writing",
    "mossy-hex": "a knobbly clay bottle stoppered with cork and moss, wrapped in "
    "trade beads and dried herbs, something faintly glowing inside",
    "captains-pin": "a dented brass military pin shaped like a lake perch "
    "crossed with a spear, its enamel chipped and lovingly polished",
    "bards-ballad": "a rolled sheet of song parchment tied with red string, its "
    "face covered in abstract inked staves and dots and swirling flourishes, "
    "decorative marks instead of writing",
    "nix-pearl": "a single enormous iridescent freshwater pearl resting in an "
    "open oyster shell, faint silt and tiny old coins caught in its lustre",
}


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
        look = REWARD_LOOK.get(reward["slug"])
        if not look:
            raise SystemExit(
                f"reward {reward['slug']!r} is in the content bundle but has no "
                "REWARD_LOOK entry; add its visual direction to this script"
            )
        # The bundle's `effect` line is deliberately NOT in the prompt. It is
        # mechanics prose ("unlocks the sunken-cache choices"), not a description
        # of what the object looks like, and handing a text-specialist model a
        # sentence about an object that carries writing is how the first batch
        # produced a chart covered in garbled pseudo-text trying to spell it out.
        # What the thing DOES belongs on the card in the game; what it LOOKS like
        # is REWARD_LOOK, and that is all the renderer gets.
        rarity = reward["rarity"].lower()
        article = "an" if rarity[0] in "aeiou" else "a"
        body = (
            f"{name}, {article} {rarity} keepsake from a comedic fantasy fishing "
            f"kingdom: {look}. One tangible hand-made object a person could pick "
            f"up. {REWARD_FRAME}"
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


CARD_FRAME = (
    "a painted storybook moment staged from the player's first-person point of "
    "view, highlighting the visiting petitioners and NPCs, lively faces "
    "and the kingdom behind them, warm illustrated console-game lighting"
)

CARD_RE = re.compile(
    r"\bid: '(?P<id>[^']+)',\s*\n"
    r"(?:\s*\w+: [^\n]*\n)*?"
    r"\s*title: '(?P<title>(?:[^'\\]|\\.)*)',\s*\n"
    r"\s*body:\s*\n?\s*'(?P<body>(?:[^'\\]|\\.)*)',",
    re.M,
)


def read_cards(content_ts: Path) -> list[dict[str, str]]:
    """Every authored card, from both the free-draw decks and the arc steps.

    A card's `body` is already one vivid sentence staging the moment -- the same
    property that makes the fish roster's `silhouette` and an ending's `body`
    usable verbatim. It is the art direction; it does not need paraphrasing.
    """
    text = content_ts.read_text(encoding="utf-8")
    cards: list[dict[str, str]] = []
    seen: set[str] = set()
    for key in ("decks", "arcs"):
        block = re.search(rf"\n  {key}: \[(.*?)\n  \],\n", text, re.S)
        if not block:
            raise SystemExit(f"no {key}: [...] block found in {content_ts}")
        for m in CARD_RE.finditer(block.group(1)):
            card = m.groupdict()
            if card["id"] in seen:
                continue
            seen.add(card["id"])
            # Which cast members this card stages, so they are drawn the same
            # way here as in their own portrait -- Vex should look like Vex on
            # every card he appears on, not be reinvented per render.
            # `characters: [...]` sits BETWEEN the id and the title, so it is
            # inside the match itself, not before it.
            cast_match = re.search(r"characters: \[([^\]]*)\]", m.group(0))
            card["cast"] = (
                re.findall(r"'([a-z-]+)'", cast_match.group(1)) if cast_match else []
            )
            cards.append(card)
    if not cards:
        raise SystemExit(f"no cards parsed from {content_ts}")
    return cards


def card_entries(content_ts: Path) -> list[dict]:
    """One scene per authored card, keyed to the id the deck already references."""
    entries: list[dict] = []
    for card in read_cards(content_ts):
        title = card["title"].replace("\u2019", "'").replace("\\'", "'")
        body = card["body"].replace("\u2019", "'").replace("\\'", "'")
        who = [CAST_LOOK[s] for s in card.get("cast", []) if s in CAST_LOOK]
        cast_clause = (
            " In frame: " + "; ".join(who) + "."
            if who
            else ""
        )
        prompt_body = (
            f"{title}. {body}{cast_clause} {CARD_FRAME}"
        )
        entries.append(
            make_entry(
                request_id=f"ruler-hooked-card-{card['id']}",
                # cardArtPath() (utils/rulerHooked/cardArt.ts) resolves `card.art`
                # (the `card-<id>` key decks.md authors) to
                # /images/ruler-hooked/<key>.webp -- no `cards/` subdirectory, and
                # the `card-` prefix is part of the filename, not a folder. Must
                # match that contract exactly or a rendered image never resolves.
                image_path=f"public/images/ruler-hooked/card-{card['id']}.webp",
                label=f"Ruler Hooked card: {title}",
                size=WIDE,
                prompt=f"{prompt_body}. {STYLE_TAIL}. {NO_TEXT}",
                priority=CONCEPT_PRIORITY,
                lane="card",
            )
        )
    return entries


# ---------------------------------------------------------------------------
# Console lane -- the illustrated console redesign (2026-11-05)
# ---------------------------------------------------------------------------
#
# Silas, 2026-11-05: the target is "an illustrated, art-heavy design that doesn't
# look like a webapp", but NOT "too shiny freeware style". The rendered library
# already hits that -- hand-painted storybook gouache -- so this lane keeps
# matching it, and the image_path keys below are exactly the ones the redesigned
# kind_robots UI resolves under public/images/ruler-hooked/.
#
# CONSOLE_FINISH states the wanted matte, hand-made finish POSITIVELY. The things
# to avoid (glossy bevels, chrome gold, lens flare, sparkle, mobile-game sheen)
# are deliberately never named in a prompt: on krea2 the negative prompt is inert,
# so naming them would paint them. They live in docs/art-direction.md Section 9
# for people instead. The same rule keeps "people" out of the empty rooms below
# (kind_robots' people-negation contract rule): an empty room is described as
# empty and still, never as lacking anyone.
#
# Every entry is WIDE (1344x768), tab vignettes included, because the UI crops
# them itself. None depicts the player's ruler (Current POV rule above).
CONSOLE_PRIORITY = CONCEPT_PRIORITY

CONSOLE_FINISH = (
    "matte opaque gouache with visible brush strokes and a faint paper grain, "
    "soft diffuse natural light, flat matte colour, handmade and quiet"
)

CONSOLE_BACKDROPS = [
    (
        "title-lakeside",
        "title backdrop: lakeside at golden hour",
        "A wide calm lake at golden hour, a storybook castle with round towers on a "
        "far green hill across the water, and on the near grassy bank an empty "
        "carved wooden royal fishing chair with a red cushion, a fishing rod "
        "leaning against its arm and a little wicker tackle basket beside it. The "
        "upper-middle third of the picture is broad open soft golden sky, calm and "
        "uncluttered. Deserted and peaceful. "
        f"{TIME_MOD['golden']}",
    ),
    (
        "court-throne-room",
        "court backdrop: sunlit throne room",
        "A sunlit royal throne room: tall arched windows along the back wall "
        "looking out over a bright lake, long cloth banners each embroidered with "
        "one big plain fish shape, a long red carpet runner leading up to a low "
        "dais, and an empty carved throne on that dais at the right. The left "
        "third of the room is calm and simple, plain warm stone wall and soft "
        "floor light with open space. The hall is empty and still. "
        f"{TIME_MOD['day']}",
    ),
    (
        "royal-map",
        "map backdrop: hand-painted kingdom map",
        "A hand-painted kingdom map on aged parchment seen from directly above: a "
        "round blue castle lake at the centre, dense green wildwood across the "
        "top, a small thatched village on one bank, a tiny castle on a hill, a far "
        "shore of patchwork fields on the opposite bank, a white waterfall "
        "tumbling into the lake, and flat green lily pads spread across one "
        "shallow corner. Painted pictures only, tiny trees, rooftops, wavy ripple "
        "lines and dotted paths, with every margin and open area left as bare "
        "clean parchment",
    ),
    (
        "gear-tackle-room",
        "gear backdrop: royal tackle room",
        "A cosy royal tackle room inside a castle tower: fishing rods standing in "
        "wooden racks along the wall, glass jars full of colourful lures on "
        "shelves, nets and wicker creels hanging from the beams, a sturdy "
        "workbench with a reel half taken apart and small tools beside it, a warm "
        "lantern, and a small round window onto the lake. The room is empty and "
        "quiet",
    ),
    (
        "fishopedia-study",
        "Fishopedia backdrop: naturalist's study at night",
        "A naturalist's study at night: a big open specimen book on a wooden desk, "
        "its pages showing one painted fish and a pressed reed on bare cream "
        "paper, glass specimen jars holding tiny curious fish, a brass magnifying "
        "glass, a lit lantern glowing warm, and a tall window looking out over a "
        "moonlit lake. The study is empty and quiet. "
        f"{TIME_MOD['night']}",
    ),
]

# Tab vignettes are shown tiny, so each is one big centred subject with few
# details. Described as a painted vignette, never as an "icon" -- an icon request
# renders as a glossy app button, which is exactly the sheen Silas ruled out.
TAB_VIGNETTE = (
    "a single bold simple painted vignette, one large subject centred on a soft "
    "plain painted gouache ground, broad shapes and few details so it reads at a "
    "glance even very small"
)

CONSOLE_TABS = [
    ("lake", "a small round blue lake with one fish leaping out of it in a bright arc of water"),
    ("map", "a rolled parchment map tied with string beside a round brass compass with a plain needle"),
    ("court", "a red velvet throne with carved gold-painted wooden arms"),
    ("gear", "a fishing rod leaning against a little wooden tackle box with its lid open"),
    ("fishopedia", "an open book showing one painted fish across both pages"),
]

# Daily proclamations (kind_robots utils/rulerHooked/dailyEvents.ts). The fourth
# field names the cast slugs a scene stages; their look comes from CAST_LOOK and
# their name from the content bundle, so Gristle on the audit day is the same
# Gristle as on his portrait and his cards.
EVENT_VIEW = (
    "a lively painted storybook moment seen at eye level, the townsfolk facing "
    "the viewer"
)

CONSOLE_EVENTS = [
    (
        "market-day",
        "Market Day at the Wharf",
        "A bustling lakeside fish market along a wooden wharf: striped awnings "
        "over stalls heaped with silver fish and baskets of eels, fishmongers in "
        "aprons haggling cheerfully with villagers, rowboats tied along the wharf, "
        f"gulls wheeling overhead. {TIME_MOD['day']}",
        [],
    ),
    (
        "heron-festival",
        "The Heron Festival",
        "The lakeside village at dusk for the Heron Festival: folded paper herons "
        "perched on every thatched roof, strings of glowing paper lanterns between "
        "the houses, and villagers mid-dance in a ring on the green with a fiddler "
        f"stamping along. {TIME_MOD['dusk']}",
        [],
    ),
    (
        "druid-procession",
        "The Druids Walk the Shore",
        "A quiet procession of leaf-cloaked druids walking single file along a "
        "worn lakeshore at dawn, each one kneeling to press green reed shoots into "
        "the soft mud where the bank has worn thin, baskets of young reeds on their "
        f"backs. {TIME_MOD['dawn']}",
        [],
    ),
    (
        "tax-audit",
        "Gristle Audits the Ledgers",
        "{taxman-gristle} sits at a small desk in a lamplit counting room, dwarfed "
        "by a teetering mountain of closed leather-bound ledgers with plain brown "
        "spines, a single stray coin gleaming on the desk in front of him, "
        "grumbling villagers peering in at the doorway",
        ["taxman-gristle"],
    ),
    (
        "guard-parade",
        "The Watch Parades",
        "{captain-cordelia} drills the town watch in a cobbled village square: a "
        "slightly disorderly line of guards in blue tabards with spears held at "
        "many different angles, one guard a full step out of time, children "
        f"watching from the edge of a fountain. {TIME_MOD['day']}",
        ["captain-cordelia"],
    ),
    (
        "soft-rain",
        "A Soft Rain",
        "Gentle soft rain falling over the calm castle lake, rings spreading "
        "across the grey-green water, reeds bowing under the drops, the far shore "
        "soft and misty, a single duck sheltering under a lily pad. Cool silvery "
        "light, peaceful and deserted",
        [],
    ),
    (
        "bards-contest",
        "The Bards Contest",
        "A crowded wooden stage on the village green packed with seventeen rival "
        "bards all performing at once, lutes and horns and a drum and a bagpipe, "
        "and in the very middle {bard-fen}, one hand raised to judge while singing "
        "loudest of all, an audience of villagers laughing with their hands over "
        f"their ears. {TIME_MOD['golden']}",
        ["bard-fen"],
    ),
    (
        "duck-census",
        "The Annual Duck Census",
        "Earnest royal officials in tall hats and round spectacles standing in "
        "the reedy shallows of the lake, one clicking a brass hand counter and one "
        "sliding beads on a wooden abacus, as a long orderly queue of ducks "
        "waddles past a little wooden counting gate, one duck staring back "
        f"unimpressed. {TIME_MOD['day']}",
        [],
    ),
    (
        "lost-boot",
        "A Boot in the Shallows",
        "A battered old leather boot just hauled up out of the lake shallows on a "
        "taut fishing line rising from the near water, lake water and gold coins "
        "pouring out of it in a bright stream, ripples and reeds all around, "
        f"a startled frog sitting on the boot's toe. {TIME_MOD['day']}",
        [],
    ),
    (
        "quiet-day",
        "Nothing Whatsoever",
        "A perfectly calm empty lake in the early morning, the water a flawless "
        "mirror of pale sky and the far wooded shore, a single wooden rowboat "
        "moored and still at a little jetty, thin mist resting on the surface. "
        f"Utter peace, deserted and quiet. {TIME_MOD['dawn']}",
        [],
    ),
]

STILL_LIFE = (
    "a close still life on a worn wooden counter, warm lamplight from the left, "
    "the object large and centred"
)

# Shop goods (economy.ts GEAR_CATALOG) are still lifes; kingdom works
# (KINGDOM_CATALOG) are the place or thing the coins pay for.
CONSOLE_GEAR = [
    (
        "reinforced-rod",
        "Reinforced Rod",
        "A sturdy fishing rod of dark ash wood bound with bands of brass wire and "
        "fitted with a heavy brass reel, lying across the counter beside coils of "
        f"line and a small tin of hooks, {STILL_LIFE}",
    ),
    (
        "silk-line",
        "Silk Line",
        "A spool of fine pale-gold silk fishing line wound on a carved wooden "
        "reel, one loose shining strand trailing across a green felt cloth, "
        f"{STILL_LIFE}",
    ),
    (
        "balanced-lure",
        "Balanced Lure",
        "A small hand-carved wooden fishing lure painted in red and white "
        "stripes, a tiny brass weight under its belly and two hooks, resting on a "
        f"little brass stand, {STILL_LIFE}",
    ),
    (
        "riverbank-market",
        "Riverbank Market",
        "A row of striped canvas market stalls along a grassy riverbank beside "
        "the castle lake, baskets of fish, bread and apples on the counters, "
        "villagers in aprons bargaining and rowboats tied up at the bank, wide "
        f"view. {TIME_MOD['day']}",
    ),
    (
        "lakeside-shrine",
        "Lakeside Shrine",
        "A small round stone shrine with a mossy domed roof on a grassy point by "
        "the lake, wildflowers, smooth river stones and lit candles on its step, "
        "a carved stone fish on top of the dome, mist on the water, deserted and "
        f"peaceful. {TIME_MOD['dawn']}",
    ),
    (
        "festival-fund",
        "Festival Fund",
        "A village green beside the lake strung with paper lanterns and coloured "
        "bunting, a wooden bandstand with two fiddlers, and in the foreground a "
        "heavy leather coin purse spilling gold coins across a trestle table. "
        f"{TIME_MOD['dusk']}",
    ),
    (
        "watch-patrol",
        "Watch Patrol",
        "Two castle guards in blue tabards and steel caps walking a gravel road "
        "along the lake carrying lanterns and spears, a shaggy guard dog trotting "
        f"ahead of them. {TIME_MOD['dusk']}",
    ),
]


def console_entries(cast: list[dict[str, str]]) -> list[dict]:
    """Backdrops, tab vignettes, proclamation scenes and shop art for the console UI."""
    names = {c["slug"]: f"{c['name']} {c['honorific']}" for c in cast}

    def tail(body: str) -> str:
        return f"{body}. {CONSOLE_FINISH}. {STYLE_TAIL}. {NO_TEXT}"

    def entry(kind: str, key: str, label: str, body: str) -> dict:
        return make_entry(
            request_id=f"ruler-hooked-console-{kind}-{key}",
            image_path=f"public/images/ruler-hooked/{kind}/{key}.webp",
            label=f"Ruler Hooked console: {label}",
            size=WIDE,
            prompt=tail(body),
            priority=CONSOLE_PRIORITY,
            lane="console",
        )

    entries: list[dict] = []
    for key, label, body in CONSOLE_BACKDROPS:
        entries.append(entry("backdrops", key, label, body))

    for name, subject in CONSOLE_TABS:
        entries.append(
            make_entry(
                request_id=f"ruler-hooked-console-ui-tab-{name}",
                image_path=f"public/images/ruler-hooked/ui/tab-{name}.webp",
                label=f"Ruler Hooked console: {name} tab vignette",
                size=WIDE,
                prompt=tail(f"{subject}, {TAB_VIGNETTE}"),
                priority=CONSOLE_PRIORITY,
                lane="console",
            )
        )

    for key, title, body, slugs in CONSOLE_EVENTS:
        for slug in slugs:
            if slug not in names:
                raise SystemExit(
                    f"console event {key!r} stages {slug!r}, which is not in the "
                    "content bundle's cast; fix the slug or the bundle"
                )
            if slug not in CAST_LOOK:
                raise SystemExit(
                    f"console event {key!r} stages {slug!r}, which has no CAST_LOOK "
                    "entry; add its visual direction to this script"
                )
            body = body.replace("{" + slug + "}", f"{names[slug]}, {CAST_LOOK[slug]},")
        if "{" in body:
            raise SystemExit(f"console event {key!r} has an unfilled cast slot: {body}")
        entries.append(
            entry("events", key, f"daily proclamation: {title}", f"{body}. {EVENT_VIEW}")
        )

    for key, name, body in CONSOLE_GEAR:
        entries.append(entry("gear", key, f"shop: {name}", body))

    # Quill the Steward coaches the tutorial and presents court petitions, but
    # the only render of the advisor (character-steward-quill.webp, 256px) came
    # back as a literal feather pen. The console skips it; this replaces it.
    entries.append(
        make_entry(
            request_id="ruler-hooked-console-character-steward-quill",
            image_path="public/images/ruler-hooked/characters/steward-quill.webp",
            label="Ruler Hooked console: Quill the Steward portrait",
            size=PORTRAIT,
            prompt=(
                f"{STEWARD_LOOK}, {PORTRAIT_FRAME}. {CONSOLE_FINISH}. {STYLE_TAIL}. {NO_TEXT}"
            ),
            priority=CONSOLE_PRIORITY,
            lane="console",
        )
    )

    return entries


def layer_entries(regions: dict[str, dict[str, list[str]]]) -> list[dict]:
    """The (region, state, time) matrix, named exactly as assetCandidates() resolves."""
    entries: list[dict] = []
    for region, spec in regions.items():
        if region == "ruler":
            # The player chooses a portrait during coronation. The composited
            # game environment never depicts the ruler from outside.
            continue
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
    assert lane in LANES, f"unknown lane {lane!r}; add it to LANES"
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


# Tokens this project has already been burned by. Both classes are the same
# mistake: a word that means one thing to an illustrator and another to a
# diffusion model, which renders whatever noun it is given.
#
#   silhouette  -- a composition note to a person, a subject to the model. The
#                  first reward batch came back as literal black cut-outs.
#   named IP    -- reference points belong in docs/art-direction.md for humans.
#                  In a prompt they reproduce the reference, and a subject name
#                  that collides with a character from it returns the character
#                  ("Nix's Pearl" + "Steven Universe" -> that show's Pearl).
BANNED_PROMPT_TOKENS = {
    "silhouette": "renders as a literal black cut-out; say the shape reads at a glance",
    "silhouettes": "renders as literal black cut-outs; say the shapes read at a glance",
    "monkey island": "named reference; describe the quality instead",
    "bakshi": "named reference; describe the quality instead",
    "treasure planet": "named reference; describe the quality instead",
    "steven universe": "named reference; returned that show's Pearl for nix-pearl",
    "she-ra": "named reference; describe the quality instead",
    "princess of power": "named reference; describe the quality instead",
    "studio ghibli": "named reference; describe the quality instead",
    "disney": "named reference; describe the quality instead",
    "pixar": "named reference; describe the quality instead",
}


def banned_tokens(prompt: str) -> list[str]:
    low = prompt.lower()
    return [
        f"{token!r}: {why}"
        for token, why in sorted(BANNED_PROMPT_TOKENS.items())
        if re.search(rf"(?<![a-z]){re.escape(token)}(?![a-z])", low)
    ]


def contract_violations(prompt: str) -> list[str]:
    """Every reason kind_robots' enqueue endpoint would 422 this prompt."""
    found: list[str] = list(conditional_instruction_violations(prompt))

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

    # Local-only, stricter than the server contract: these render wrong rather
    # than getting rejected, so nothing upstream would ever catch them.
    found.extend(f"banned-token {b}" for b in banned_tokens(prompt))

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


def lane_counts(entries: list[dict], existing: set[str]) -> list[tuple[str, int, int]]:
    """(lane, staged, unstaged) for every lane in LANES, sorted by lane name."""
    rows = []
    for lane in sorted(LANES):
        in_lane = [e for e in entries if e["lane"] == lane]
        staged = sum(1 for e in in_lane if e["id"] in existing)
        rows.append((lane, staged, len(in_lane) - staged))
    return rows


def print_lane_table(rows: list[tuple[str, int, int]]) -> None:
    print(f"{'lane':<10} {'total':>6} {'staged':>7} {'unstaged':>9}")
    for lane, staged, unstaged in rows:
        print(f"{lane:<10} {staged + unstaged:>6} {staged:>7} {unstaged:>9}")


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
    parser.add_argument(
        "--lane",
        choices=sorted(LANES),
        help="only build/stage/check entries from this lane (default: all lanes). "
        "'layer' entries are only produced when --include-layers is also passed.",
    )
    parser.add_argument(
        "--list-lanes",
        action="store_true",
        help="print staged vs not-yet-staged counts for every produced lane and exit "
        "(read-only, even with --write)",
    )
    args = parser.parse_args()
    if args.list_lanes and args.lane:
        parser.error("--list-lanes summarizes every lane; do not combine it with --lane")

    content_ts = find_content_bundle()
    cast = read_cast(content_ts)
    entries = (
        concept_entries(cast)
        + alt_vista_entries()
        + ruler_entries()
        + fish_entries()
        + reward_entries(content_ts)
        + ending_entries(content_ts)
        + card_entries(content_ts)
        + console_entries(cast)
    )
    if args.include_layers:
        entries += layer_entries(read_regions(content_ts))
    assert_contract(entries)

    text = ART_PROMPTS.read_text(encoding="utf-8")
    existing = staged_ids(text)

    if args.list_lanes:
        print_lane_table(lane_counts(entries, existing))
        return 0

    if args.lane:
        entries = [e for e in entries if e["lane"] == args.lane]
    fresh = [e for e in entries if e["id"] not in existing]

    lane_suffix = f" (lane={args.lane})" if args.lane else ""
    print(f"source bundle: {content_ts}")
    print(f"built {len(entries)} entr(ies){lane_suffix}; {len(fresh)} not yet staged")
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
