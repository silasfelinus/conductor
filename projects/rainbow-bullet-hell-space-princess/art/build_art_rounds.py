#!/usr/bin/env python3
"""Write the Rainbow Space Princess production art ledgers (rounds 2-7) for one house checkpoint.

Round 1 (ART-ROUND-1-CHECKPOINTS.yaml) picks the house Illustrious checkpoint. This script then writes one
enqueue_art_requests.py ledger per production round, every cell in that house lane:

  2  front end + cast   title/key art, pilot select, turnarounds, expressions, cockpit, off-duty, Lilt-7,
                        supporting cast, the four player ships
  3  enemy fleet        E01-E24 (WORLD-BIBLE.md enemy behavior atlas)
  4  bosses             B01-B09 hero shots plus the defeat/rescue image
  5  stages             S01-S09 four parallax planes each, plus the Act III/V quiet tableaux
  6  cinematics         C01-C17 storyboard plates (subtitles stay in UI, never painted in)
  7  pickups + HUD      U01-U12 pickup charms, shield/super/explosion effect sheets

Canon lives in CAST-BIBLE.md, WORLD-BIBLE.md, ACT-STRUCTURE.md, ART-DIRECTION.md and COMMS-AND-ENDINGS-BIBLE.md.
The supporting-cast looks (Purl, Opal, Nemi, the Lost Navigator, the Coral Choir) are first proposals authored
for t-020; reconcile them if Silas or a later bible says otherwise.

A ledger that already exists is never overwritten (it holds submitted job ids). Usage:

    python projects/rainbow-bullet-hell-space-princess/art/build_art_rounds.py \
        --checkpoint Illustrious/<file>.safetensors --label "<name>" [--steps 28 --cfg 5 --sampler euler_ancestral]
    python scripts/enqueue_art_requests.py projects/rainbow-bullet-hell-space-princess/art/ART-ROUND-2-FRONT-END.yaml --live
"""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
SLUG = "rainbow-bullet-hell-space-princess"

# Style: Silas, 2026-10-12 PT: "more like she ra princesses of power ... western cartoon, not faux realism"
# (ART-ROUND-1B-WESTERN-TOON.yaml). The show is a style reference only; its characters stay out (STYLE_NEG).
PREFIX = (
    "masterpiece, best quality, amazing quality, absurdres, toon (style), western cartoon, she-ra and the princesses "
    "of power (style), flat color, cel shading, clean lineart, bold outlines, simple shading, bold graphic shapes, "
    "expressive"
)
SUFFIX = (
    "flat pastel colors, candy pink, lilac, powder cyan, butter yellow, opalescent turquoise, deep navy, sparkles, "
    "glowing magic, 2d animation still"
)
STYLE_NEG = (
    "realistic, photorealistic, 3d, semi-realistic, painterly, oil painting, detailed shading, soft shading, airbrush, "
    "anime, manga, moe, she-ra (character), adora (she-ra), catra (she-ra), glimmer (she-ra)"
)

BASE_NEG = (
    "nsfw, nude, suggestive, lowres, worst quality, low quality, bad anatomy, deformed, watermark, signature, "
    "text, logo, letters, username, blurry, jpeg artifacts, " + STYLE_NEG
)
NEG_PERSON = (
    BASE_NEG + ", cleavage, revealing clothes, midriff, underboob, bad hands, extra fingers, missing fingers, "
    "extra limbs, child, loli, chibi"
)
NEG_SOLO = NEG_PERSON + ", multiple girls, 2girls, multiple views"
# Machines, places and props: keep people out without a negation in the positive prompt (prompt contract).
NEG_SCENE = "humans, person, 1girl, 1boy, " + BASE_NEG + ", grainy, muddy colors, grey, gritty, horror, gore"
# Round 1: "mecha" grew the Moonjelly Lantern dog legs on Arthemy and Mol_Keun, so machines ban legs outright.
NEG_MACHINE = NEG_SCENE + (
    ", legs, quadruped, walking, animal legs, feet, robot animal, creature, battleship, naval ship, boat, gun turrets"
)
# Round 1B: "battle cruiser" drew a literal naval battleship riding the seahorse.
NEG_GROUP = NEG_PERSON + ", identical faces, same face, same body type, pale skin on everyone, 5girls, 6+girls, extra person"

PORTRAIT = "832x1216"
WIDE = "1344x768"
LAND = "1216x832"

# ---------------------------------------------------------------- cast (CAST-BIBLE.md)
PILOTS = {
    "maribel": {
        "label": "P1 Maribel Rowan (pink, Petal Wing)",
        "id": "1girl, solo, adult woman, petite, wiry, tomboy, very short hair, pixie cut, (copper hair:1.2), auburn hair, "
        "freckles, light skin, strong nose, green eyes",
        "suit": "(rose pink utility flight jacket:1.2), asymmetrical zipped high collar, rolled sleeves, old radio clipped to "
        "shoulder, small four-petal badge, navy undershirt, cargo trousers, sturdy boots",
        "offduty": "repaired cream knit sweater, weatherproof trousers, sitting at a cluttered workbench, vintage radio "
        "receivers, soldering iron, warm lamp light, workshop full of antennas",
        "cockpit": "pink cockpit lights, petal-shaped canopy frame",
        "prop": "holding wrench, grease smudge on hands",
        "neg": NEG_SOLO + ", long hair, pink hair",
    },
    "azure": {
        "label": "P2 Azure Lin (cyan, Prism Lance)",
        "id": "1girl, solo, mature female, tall, long legs, slender, east asian, vietnamese, black hair, long braid, "
        "side undercut, dark eyes",
        "suit": "(powder cyan flight coat:1.3), cyan and white, asymmetrical coat, geometric seams, prism instrument on collar, dark gloves, "
        "constellation lines drawn on gloves, dark trousers, tall boots",
        "offduty": "loose cyan linen shirt, rolled sleeves, standing in a glass-domed observatory, hand-drawn star maps "
        "pinned everywhere, brass telescope, night sky full of stars",
        "cockpit": "cyan cockpit lights, holographic trajectory lines",
        "prop": "holding glowing star chart",
        "neg": NEG_SOLO + ", short, pink coat, white coat, yellow coat",
    },
    "solenne": {
        "label": "P3 Solenne Adisa (gold, Halo Fin)",
        "id": "1girl, solo, mature female, dark-skinned female, very dark skin, (muscular female:1.2), broad shoulders, toned "
        "arms, strong forearms, thick thighs, black hair, two-strand twists, hair up, ear cuff, brown eyes",
        "suit": "butter yellow and antique gold flight suit, sleeveless, reinforced shoulder plates, circular ring "
        "insignia, utility belt, gold boots",
        "offduty": "sleeveless mechanic work vest, standing in a rehearsal room, music stands, handwritten four-part "
        "harmony sheet music, warm golden light, conductor baton",
        "cockpit": "golden cockpit lights, two orbiting ring drones outside the canopy",
        "prop": "holding notebook with music notes",
        "neg": NEG_SOLO + ", pale skin, light skin, thin arms, skinny",
    },
    "vivi": {
        "label": "P4 Vivi Reyes (lilac, Comet Crown)",
        "id": "1girl, solo, mature female, plump, curvy, wide hips, soft belly, tan skin, latina, undercut, side shave, "
        "(dark brown hair:1.3), streaked hair, purple streaks, coral streaks, eyebrow piercing, ear piercings, painted nails",
        "suit": "lilac armored jacket, sewn patches, comet pins, quick-release belt, dark cargo pants, heavy boots, "
        "fully clothed",
        "offduty": "oversized lilac hoodie covered in stitched patches, combat boots, sitting on a small garage stage, "
        "speakers, tangled cables, synthesizer, string lights, cassette recordings labeled by hand",
        "cockpit": "lilac cockpit lights, three-pointed comet canopy",
        "prop": "holding music sampler",
        "neg": NEG_SOLO + ", skinny, thin waist, large breasts, text on clothes, graphic tee, light skin, pink hair, blonde hair",
    },
}
EXPRESSIONS = {
    "neutral": "neutral expression, closed mouth, calm",
    "delighted": "delighted, wide smile, open mouth, sparkling eyes",
    "fearful": "scared, worried, wide eyes, sweat",
    "confident": "confident smirk, determined eyes",
    "frustrated": "frustrated, frown, furrowed brow, clenched teeth",
    "laughing": "laughing, eyes closed, open mouth, head tilted back",
}

LILT_ID = (
    "solo, (androgynous:1.3), nonbinary, adult, mature, angular face, sharp features, flat chest, android, synthetic humanoid, translucent pearl glass skin, glowing cyan filaments under "
    "skin, golden eyes, small crack across one cheek, short sleek iridescent hair, high collar, pearl white "
    "mothership uniform"
)
LILT_EXPR = {
    "neutral": "calm deadpan expression",
    "teasing": "teasing half smile, one eyebrow raised",
    "worried": "worried, eyebrows drawn together",
    "defiant": "defiant, determined glare, hand raised in refusal",
    "laughing": "laughing softly, eyes closed",
    "speaking": "speaking, open mouth, hand gesture, explaining",
}

SUPPORT = {
    "purl": ("Captain Purl, retired sea-mine navigator and training mentor (proposed design)",
             "solo, old man, elderly, brown skin, neat white beard, laugh lines, kind eyes, navy captain coat, pearl "
             "buttons, faded medals shaped like sea mines, captain hat, leaning on a cane, upper body, looking at "
             "viewer, mothership training deck background, chart table"),
    "opal": ("Professor Opal, engineer and powerup host (proposed design)",
             "1girl, solo, middle-aged woman, plump, fat, medium brown skin, grey curly hair in a bun, round goggles on "
             "forehead, opal iridescent lab coat over overalls, tool belt, cheerful grin, holding glowing powerup "
             "capsule, upper body, looking at viewer, workshop background, floating holographic schematics"),
    "nemi": ("Nemi, rescued jellyfish pilot and translator (proposed design)",
             "solo, jellyfish creature, small translucent jellyfish person, bell-shaped head, glowing pink and cyan "
             "tentacles, big gentle eyes, tiny pilot scarf, floating, curious, cute, looking at viewer, "
             "bioluminescent water glow background"),
    "navigator": ("The Lost Navigator, rescued optional ally (proposed design)",
                  "solo, middle-aged person, androgynous, weathered skin, silver hair, long tattered navigator cloak "
                  "covered in faded star charts, brass sextant, tired hopeful eyes, upper body, looking at viewer, "
                  "mirrored crystal cavern background"),
    "choir": ("The Coral Choir, survivor collective (proposed design)",
              "group, multiple people, diverse survivors of different ages, elderly, adults, different skin tones, "
              "different body types, singing together, coral station interior, bioluminescent coral pipes, warm "
              "light, hopeful, wide shot"),
}

SHIPS = {
    "petal-wing": ("P1 Petal Wing", "sleek rose gold and pink hull, four swept swallowtail wings shaped like petals, "
                   "pearl white accents, glowing pink thrusters"),
    "prism-lance": ("P2 Prism Lance", "long needle-shaped powder cyan hull, one long pointed dorsal fin, prism crystal "
                    "nose, glowing cyan thrusters"),
    "halo-fin": ("P3 Halo Fin", "broad round butter yellow disc hull, twin gold rings around nacelles, two small "
                 "orbiting drones, glowing gold thrusters"),
    "comet-crown": ("P4 Comet Crown", "lilac triangular three-pronged arrowhead hull, star-shaped crown fins, "
                    "glowing lilac and coral thrusters"),
}
SHIP_VIEWS = {
    "side": "side view, profile, facing right",
    "top": "from above, top-down view",
    "hero": "three-quarter view, dynamic angle, flying, speed lines, thruster trail",
}

# ---------------------------------------------------------------- enemies (WORLD-BIBLE.md E01-E24)
ENEMIES = [
    ("e01", "Seahorse Picket", "small robotic seahorse spaceship, curled tail, upright prow, glowing thruster tail"),
    ("e02", "Seahorse Spiral Scout", "robotic seahorse spaceship, tightly curled fin, spiral tail, scout drone"),
    ("e03", "Seahorse Anchor", "heavy robotic seahorse spaceship, dropping glowing pearl mine beads, anchor tail"),
    ("e04", "Pearl Urchin", "round robotic sea urchin drone, bristling crystal spines, pearl core"),
    ("e05", "Moonjelly Lantern", "robotic jellyfish spaceship, translucent glass bell hull, glowing core, electric "
     "tentacle antennae"),
    ("e06", "Moonjelly Relay", "pair of robotic jellyfish drones linked by tentacles, relay antenna, lightning"),
    ("e07", "Moonjelly Skimmer", "flat robotic jellyfish skimmer, folded bell, dangling electric beads"),
    ("e08", "Coral Drifter", "floating coral chamber drone, branching coral armor, glowing vents"),
    ("e09", "Clawstrike Shrimp", "robotic mantis shrimp gunship, retracting forward punch cannon, segmented armor"),
    ("e10", "Pistol Shrimp Shuttle", "robotic pistol shrimp shuttle, oversized bubble cannon claw, coils"),
    ("e11", "Angler Decoy", "robotic anglerfish ship, glowing lure halo, hidden jaws"),
    ("e12", "Glassfin Skate", "flat robotic skate ray ship, mirrored glass fins, tilted"),
    ("e13", "Dolphin Pair", "two sleek robotic dolphin fighter ships flying side by side, twin beacons"),
    ("e14", "Dolphin Courier", "robotic dolphin cargo ship, glowing cargo pods, fast"),
    ("e15", "Electric Eel Threader", "long segmented robotic eel ship, glowing electric segments"),
    ("e16", "Shark Cutter", "wedge-nosed robotic shark strike craft, open jaws, sharp fins"),
    ("e17", "Shark Hammerhead", "robotic hammerhead shark gunship, missile pods on the hammer fins"),
    ("e18", "Octopus Salvager", "robotic octopus salvage ship, four grabbing mechanical arms, armor plates"),
    ("e19", "Manta Broodship", "large flat robotic manta ray carrier ship, small interceptors launching from wings"),
    ("e20", "Reef Turret", "mechanical coral flower turret, unfolding petals, glowing stem"),
    ("e21", "Nautilus Bulwark", "robotic nautilus shell fortress, spiral shell, glowing eye window"),
    ("e22", "Mirror Eel", "silver robotic eel ship with blue afterimages, mirrored scales"),
    ("e23", "Crystal Squid", "robotic squid ship with crystal lens head, prismatic glitter, tentacles"),
    ("e24", "Crown Harbinger", "ornate prismatic crown-shaped starship, glowing prism core, stained glass panels"),
]

# ---------------------------------------------------------------- bosses (WORLD-BIBLE.md B01-B09)
BOSSES = [
    ("b01", "Pearl Seahorse", "giant robotic seahorse starship, tall coiled hull, glowing pearl in throat, "
     "rotating tail shield", "cracked pearl, a small glowing living pod escaping, safe and free"),
    ("b02", "Aurelia Array", "three giant translucent robotic jellyfish bells linked to a central antenna, current "
     "lanes", "freed luminous jellyfish colony drifting away, peaceful"),
    ("b03", "Clawburst", "giant robotic mantis shrimp starship, massive forward punch cannon, armored joint socket",
     "shattered cannon, rescued pilot waving from an escape pod"),
    ("b04", "Delphion", "two giant robotic dolphin scimitar warships coupled at the rear, synchronized",
     "two dolphin ships uncoupling and swimming free together"),
    ("b05", "Sawtooth Regent", "giant robotic shark wedge starship, sawtooth jaws, hinged jaw, hammerhead escorts",
     "broken teeth turning into falling coral rain, shark ship floating calm"),
    ("b06", "Lantern Ray", "immense robotic manta ray carrier, glowing underside beacons, drone nurseries",
     "baby manta rays drifting away alive and glowing"),
    ("b07", "Glass Eel", "colossal silver threaded robotic eel dreadnought, mirrored afterimages, glowing core",
     "mirrored shell fragments peeling back to reveal a living eel inside"),
    ("b08", "Prism Leviathan", "vast robotic whale palace escort, forehead prism gem, four spire locks on its back",
     "captive whale fleet freed, swimming through light"),
    ("b09", "Eclipse Crown", "colossal circular crown machine, eclipse halo, stained glass spokes, glowing heart node",
     "full-screen liberation, crown shattering into rainbow light, freed fleets everywhere"),
]

# ---------------------------------------------------------------- stages (WORLD-BIBLE.md S01-S09, far -> near)
STAGES = [
    ("s01", "Pinkwake Estuary", ["pink cloud sea, nebula clouds like ocean waves", "floating glass buoys",
                                 "pearly fish shoal", "pink coral silhouettes"]),
    ("s02", "Moonjelly Fields", ["translucent violet nebula", "floating jellyfish bell towers",
                                 "charged glowing tendrils", "passing glass fronds"]),
    ("s03", "Chromatic Trench", ["indigo void, deep trench", "glowing volcanic vents", "abandoned metal vaults",
                                 "rock ribs"]),
    ("s04", "Rosefin Express", ["streaming pink and cyan aurora", "giant transit rings", "migrating space trains",
                                "glowing light rails"]),
    ("s05", "Blossom Wreckyard", ["starship graveyard among stars", "pink petal wreck slabs", "dock cranes and "
                                  "machinery", "broken hull plates"]),
    ("s06", "Crown Reef", ["gold nebula", "coral megastructures", "bioluminescent coral arches",
                           "branching coral tendrils"]),
    ("s07", "Glass Current", ["mirrored star canyon", "crystalline strata", "fractured light beams",
                              "prism lens ribbons"]),
    ("s08", "Eclipse Palace", ["eclipse corona", "captive armada of ships in the distance", "palace heart spires",
                               "cracked pearl walls"]),
    ("s09", "Eclipse Crown finale", ["machine nerve halo", "fractured stained glass sky", "distant reunited fleet",
                                     "floating crown fragments"]),
]
LAYERS = [
    ("far", "far background layer, distant, soft focus, wide open sky"),
    ("mid", "midground layer, floating structures, atmospheric perspective"),
    ("near", "near layer, structures along the bottom edge, open space above"),
    ("fore", "foreground silhouettes along the bottom edge only, black background above, high contrast"),
]

# ---------------------------------------------------------------- cinematics (WORLD-BIBLE.md C01-C17)
CINEMA = [
    ("c01", "calm Luminous Ocean palace", "scenery, pearl palace floating in a cosmic ocean, calm, peaceful fleet"),
    ("c02", "migrating fleet", "scenery, migrating fleet of whale and jellyfish shaped ships, stars, harmony"),
    ("c03", "alarm in mirror-glass", "scenery, mirror glass walls flashing red warning light, shadow of a crown"),
    ("c04-maribel", "Maribel powers up", None),
    ("c04-azure", "Azure powers up", None),
    ("c04-solenne", "Solenne powers up", None),
    ("c04-vivi", "Vivi powers up", None),
    ("c05", "launch bay", "scenery, four starfighters in a launch bay, pink cyan yellow lilac, launch lights"),
    ("c06", "launch choreography", "four starfighters launching out of a mothership in a spiral, rainbow trails"),
    ("c07", "Eclipse machine captures wildlife", "scenery, dark prismatic crown machine casting light beams that turn "
     "jellyfish into robotic ships"),
    ("c08", "first pearl carrier revealed", "giant robotic seahorse carrier emerging from pink clouds, ominous"),
    ("c09", "control handoff", "four starfighters diving toward enemy fleet, wide shot"),
    ("c10", "Nemi signal decoded", "small glowing jellyfish creature speaking through a hologram, cockpit"),
    ("c11", "choices acknowledged", "rescued jellyfish colony glowing around the mothership, gratitude"),
    ("c12", "Lost Navigator memory", "silver-haired navigator in a tattered star chart cloak, memory hologram, crystal"),
    ("c13", "machine motivation revealed", "colossal crown machine heart, stained glass, cold perfect order"),
    ("c14", "liberation ending", "scenery, freed fleets of sea creatures swimming through rainbow light, dawn"),
    ("c15", "evacuation ending", "scenery, mothership leading a convoy of rescued ships away from a collapsing "
     "palace"),
    ("c16", "bittersweet ending", "scenery, quiet memorial of lanterns floating on a cosmic sea, hopeful"),
    ("c17", "credits parade", "parade of rescued sea creature ships and four starfighters across a restored sky"),
]

# ---------------------------------------------------------------- pickups and effects (WORLD-BIBLE.md U01-U12)
PICKUPS = [
    ("u01", "Rose Petal Matrix", "pink fan-shaped diamond charm"),
    ("u02", "Prism Needle", "thin cyan crystal diamond"),
    ("u03", "Tide Tracker", "teal arrow charm"),
    ("u04", "Orbit Garden", "lilac ring charm"),
    ("u05", "Echo Charge", "gold crescent charm"),
    ("u06", "Bubble Shield", "white hexagon bubble"),
    ("u07", "Repair Pearl", "pink heart pearl with dark rim"),
    ("u08", "Super Shard", "prismatic star crystal"),
    ("u09", "Rescue Beacon", "green glowing beacon"),
    ("u10", "Mirror Lens", "blue outlined eye lens"),
    ("u11", "Score Coral", "gold coral bud"),
    ("u12", "Recovery Cache", "white chevron capsule"),
]
EFFECTS = [
    ("fx-friendly-shots", "sprite sheet of glowing friendly projectiles, pink petals, cyan needles, gold rings, lilac "
     "stars, game effects, black background"),
    ("fx-enemy-bullets", "sprite sheet of enemy bullets, round orbs with dark outlines and bright saturated centers, "
     "game effects, black background"),
    ("fx-shield", "glowing bubble shield effect, hexagon pattern, iridescent, game effect, black background"),
    ("fx-explosion", "sprite sheet of pastel explosions, pink and cyan bursts, sparkles, game effects, black "
     "background"),
    ("fx-super-bloom", "giant pink flower-shaped energy burst, Bloom Nova, radial petals, game effect, black "
     "background"),
    ("fx-super-tidal", "massive cyan prism beam, Tidal Prism, game effect, black background"),
    ("fx-super-halo", "golden ring shield dome, Halo Harbor, game effect, black background"),
    ("fx-super-comet", "parade of rainbow comet drones, Comet Parade, game effect, black background"),
]


def subj(key, title, tags, *, size=PORTRAIT, seed, negative=NEG_SCENE, ticket=None, prose=None):
    row = {"key": key, "title": title}
    if ticket:
        row["ticket"] = ticket
    row.update({"size": size, "seed": seed, "negative": negative, "prompt_prose": prose or title, "prompt_tags": tags})
    return row


def round_front_end():
    rows, seed = [], 420000
    ships_all = ("four starfighters flying in formation, pink swallowtail starfighter with four swept petal wings, "
                 "cyan needle starfighter with one long fin, butter yellow round disc starfighter with twin rings, "
                 "lilac three-pointed arrowhead starfighter")
    for n in range(4):
        seed += 1
        rows.append(subj(f"r2-title-keyart-{n + 1}", "title screen key art, four princess ships",
                         f"scenery, {ships_all}, rainbow light trails, glowing bullets, bullet hell, cosmic ocean, "
                         "pink and lilac nebula clouds like waves, small distant mechanical whale silhouette, "
                         "stars, ships in the foreground, large ships, dynamic angle, wide shot, epic key visual, sense of speed",
                         size=WIDE, seed=seed, ticket="FE-TITLE"))
    for n in range(2):
        seed += 1
        rows.append(subj(f"r2-title-backdrop-{n + 1}", "title menu backdrop, open center for the logo",
                         "scenery, cosmic ocean, pink and lilac nebula clouds like waves, pearl palace far away, "
                         "glowing horizon, stars, open sky in center, symmetrical, calm, wide shot, dreamy",
                         size=WIDE, seed=seed, ticket="FE-TITLE-BG"))
    for n in range(3):
        seed += 1
        rows.append(subj(f"r2-cast-group-{n + 1}", "ensemble key art, all four princesses before their ships",
                         "4girls, group, mature female, standing together on a luminous starport deck, different "
                         "heights, different body types, short petite tomboy with very short copper hair and freckles "
                         "in pink flight jacket, tall east asian woman with long black braid in cyan flight coat, "
                         "muscular dark-skinned woman with twists in yellow and gold sleeveless flight suit, curvy "
                         "latina punk with side shave and purple streaks in lilac patched jacket, four starfighters "
                         "behind them, pink cyan yellow lilac, opalescent sea nebula, confident, full body, key visual",
                         size=WIDE, seed=seed, negative=NEG_GROUP, ticket="CAST-GROUP"))
    for name, p in PILOTS.items():
        ident, suit = p["id"], p["suit"]
        for n in range(2):
            seed += 1
            rows.append(subj(f"r2-{name}-select-{n + 1}", f"pilot select full body, {p['label']}",
                             f"{ident}, {suit}, {p['prop']}, full body, standing, heroic pose, looking at viewer, "
                             "starship hangar background, glowing lights", seed=seed, negative=p["neg"],
                             ticket="FE-SELECT"))
        seed += 1
        rows.append(subj(f"r2-{name}-turnaround", f"turnaround sheet, {p['label']}",
                         f"{ident}, {suit}, character sheet, turnaround, multiple views, front view, side view, back "
                         "view, full body, standing, simple background, white background",
                         size=WIDE, seed=seed, negative=p["neg"].replace(", multiple views", ""),
                         ticket="A-PILOT-TURN"))
        seed += 1
        rows.append(subj(f"r2-{name}-cockpit", f"seated cockpit portrait, {p['label']}",
                         f"{ident}, {suit}, sitting in starfighter cockpit, pilot helmet, visor up, hands on controls, "
                         f"{p['cockpit']}, hud glow, upper body, looking at viewer", seed=seed, negative=p["neg"],
                         ticket="A-PILOT-COCKPIT"))
        seed += 1
        rows.append(subj(f"r2-{name}-comms", f"comms hologram portrait, helmet on, {p['label']}",
                         f"{ident}, {suit}, pilot helmet on, visor up, headset microphone, hologram, scanlines, comms "
                         "screen, bust portrait, looking at viewer, glowing", seed=seed, negative=p["neg"],
                         ticket="A-PILOT-COMMS"))
        seed += 1
        rows.append(subj(f"r2-{name}-offduty", f"off-duty portrait in a personal environment, {p['label']}",
                         f"{ident}, {p['offduty']}, relaxed, smile, upper body", seed=seed, negative=p["neg"],
                         ticket="A-PILOT-OFFDUTY"))
        for expr, tags in EXPRESSIONS.items():
            seed += 1
            rows.append(subj(f"r2-{name}-expr-{expr}", f"expression {expr}, {p['label']}",
                             f"{ident}, {suit}, {tags}, portrait, bust, looking at viewer, simple background, soft "
                             "pastel gradient background", seed=seed, negative=p["neg"], ticket="A-PILOT-EXPR"))
    lilt_neg = NEG_PERSON + ", multiple views, horror, creepy, mouthless, 1girl, cute, moe, girly, large breasts, pink hair"
    seed += 1
    rows.append(subj("r2-lilt-turnaround", "Lilt-7 turnaround sheet",
                     f"{LILT_ID}, character sheet, turnaround, multiple views, front view, side view, back view, "
                     "full body, standing, simple background, white background", size=WIDE, seed=seed,
                     negative=lilt_neg.replace(", multiple views", ""), ticket="A-LIAISON-01"))
    for expr, tags in LILT_EXPR.items():
        seed += 1
        rows.append(subj(f"r2-lilt-{expr}", f"Lilt-7 comms bust, {expr}",
                         f"{LILT_ID}, {tags}, hologram, scanlines, comms screen, bust portrait, looking at viewer, "
                         "mothership command bridge background, soft cyan and gold light", seed=seed,
                         negative=lilt_neg, ticket="A-LIAISON-01"))
    seed += 1
    rows.append(subj("r2-lilt-command-bay", "Aurora Mercy command bay plate",
                     "scenery, mothership command bridge interior, pearl white consoles, holographic star map, "
                     "large window onto pink cosmic ocean, cyan and gold light, wide shot",
                     size=WIDE, seed=seed, ticket="A-LIAISON-01"))
    for key, (title, tags) in SUPPORT.items():
        for n in range(2):
            seed += 1
            neg = NEG_PERSON if key == "choir" else NEG_PERSON + ", multiple views"
            rows.append(subj(f"r2-support-{key}-{n + 1}", title, tags, size=WIDE if key == "choir" else PORTRAIT,
                             seed=seed, negative=neg, ticket="A-SUPPORT"))
    seed += 1
    rows.append(subj("r2-crown-voice", "The Crown Voice comms presence",
                     "abstract prismatic crown hologram, circular stained glass machine, cold white glow, eclipse "
                     "halo, symmetrical, ominous but beautiful, dark background", seed=seed, ticket="A-SUPPORT"))
    for key, (label, tags) in SHIPS.items():
        for view, vtags in SHIP_VIEWS.items():
            seed += 1
            bg = ("cosmic ocean nebula background" if view == "hero"
                  else "single object, centered, full shot, simple background, dark navy background")
            rows.append(subj(f"r2-ship-{key}-{view}", f"{label} player ship, {view}",
                             f"mecha, spacecraft, starfighter, {tags}, cockpit canopy, iridescent metal, {vtags}, "
                             f"concept art, game asset, {bg}", size=LAND, seed=seed, ticket="A-PILOT-SHIP"))
    return rows


def round_enemies():
    rows, seed = [], 430000
    for eid, name, tags in ENEMIES:
        for n in range(2):
            seed += 1
            rows.append(subj(f"r3-{eid}-{n + 1}", f"{eid.upper()} {name} enemy craft",
                             f"spaceship, vehicle, flying, {tags}, futuristic sea life starship, iridescent metal, bioluminescence, enemy "
                             "ship, side view, facing left, concept art, game asset, single object, centered, full "
                             "shot, simple background, dark navy background", size=LAND, seed=seed, negative=NEG_MACHINE,
                             ticket=f"A-ENEMY-{eid[1:]}"))
    return rows


def round_bosses():
    rows, seed = [], 440000
    for bid, name, tags, rescue in BOSSES:
        for n in range(2):
            seed += 1
            rows.append(subj(f"r4-{bid}-hero-{n + 1}", f"{bid.upper()} {name} boss",
                             f"starship, sci-fi spaceship shaped like a sea creature, {tags}, colossal boss starship, futuristic sea life, iridescent metal, glowing "
                             "weak point, side view, facing left, cosmic ocean background, epic scale, dramatic "
                             "lighting, boss battle, wide shot", size=WIDE, seed=seed, negative=NEG_MACHINE,
                             ticket=f"A-BOSS-{bid[1:]}"))
        seed += 1
        rows.append(subj(f"r4-{bid}-rescue", f"{bid.upper()} {name} defeat and rescue image",
                         f"{rescue}, aftermath, gentle light, hopeful, sparkles, cosmic ocean background, wide shot",
                         size=WIDE, seed=seed, ticket=f"A-BOSS-{bid[1:]}"))
    return rows


def round_stages():
    rows, seed = [], 450000
    for sid, name, planes in STAGES:
        for (layer, ltags), plane in zip(LAYERS, planes):
            seed += 1
            rows.append(subj(f"r5-{sid}-{layer}", f"{sid.upper()} {name} {layer} parallax plane",
                             f"scenery, outer space, {plane}, {ltags}, side-scrolling game background, parallax "
                             "layer, horizontal composition, wide shot", size=WIDE, seed=seed,
                             ticket=f"A-STAGE-{sid[1:]}"))
    for act, sid, tags in (("III", "s03", "safe salvage dock, repaired starfighters, quiet, lanterns"),
                           ("V", "s05", "memorial among wrecks, floating candles, recovery tents, quiet")):
        seed += 1
        rows.append(subj(f"r5-tableau-act-{act.lower()}", f"Act {act} quiet tableau",
                         f"scenery, {tags}, cosmic ocean, calm, wide shot", size=WIDE, seed=seed,
                         ticket=f"A-STAGE-{sid[1:]}-TABLEAU"))
    return rows


def round_cinema():
    rows, seed = [], 460000
    for cid, title, tags in CINEMA:
        seed += 1
        if tags is None:
            p = PILOTS[cid.split("-", 1)[1]]
            tags = (f"{p['id']}, {p['suit']}, powering up in a separate launch chamber, glowing energy rising, "
                    "determined, cinematic, upper body, dramatic lighting")
            neg = p["neg"]
        else:
            neg = NEG_PERSON if any(w in tags for w in ("navigator", "creature")) else NEG_SCENE
        rows.append(subj(f"r6-{cid}", f"{cid.upper()} {title}", f"{tags}, cinematic still, storyboard frame, wide shot",
                         size=WIDE, seed=seed, negative=neg, ticket=f"A-CIN-{cid[1:3]}"))
    return rows


def round_pickups():
    rows, seed = [], 470000
    for uid, name, tags in PICKUPS:
        seed += 1
        rows.append(subj(f"r7-{uid}", f"{uid.upper()} {name} pickup charm",
                         f"{tags}, glowing game pickup icon, item, single object, centered, dark outline, bright core, "
                         "simple background, dark navy background", size="1024x1024", seed=seed, ticket="A-HUD"))
    for key, tags in EFFECTS:
        seed += 1
        rows.append(subj(f"r7-{key}", key.replace("-", " "), tags, size="1024x1024", seed=seed, ticket="A-FX"))
    return rows


ROUNDS = [
    (2, "FRONT-END", "front end and cast", round_front_end),
    (3, "ENEMIES", "enemy fleet E01-E24", round_enemies),
    (4, "BOSSES", "bosses B01-B09", round_bosses),
    (5, "STAGES", "stage parallax planes S01-S09", round_stages),
    (6, "CINEMA", "cinematic storyboard C01-C17", round_cinema),
    (7, "PICKUPS-FX", "pickups U01-U12 and effects", round_pickups),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--checkpoint", required=True, help="house checkpoint, e.g. Illustrious/<file>.safetensors")
    ap.add_argument("--label", required=True, help="human name of the house checkpoint")
    ap.add_argument("--steps", type=int, default=28)
    ap.add_argument("--cfg", type=float, default=5)
    ap.add_argument("--sampler", default="euler_ancestral")
    ap.add_argument("--out", type=Path, default=HERE, help="directory for the ledgers (default: this folder)")
    args = ap.parse_args()
    lane = {"key": "house", "label": f"{args.label} (house, chosen in round 1)", "engine": "comfy",
            "checkpoint": args.checkpoint, "prompt": "tags", "prefix": PREFIX, "suffix": SUFFIX,
            "steps": args.steps, "cfg": args.cfg, "sampler": args.sampler}
    total = 0
    for number, tag, about, build in ROUNDS:
        path = args.out / f"ART-ROUND-{number}-{tag}.yaml"
        rows = build()
        total += len(rows)
        if path.exists():
            print(f"skip {path.name}: exists ({len(rows)} subjects authored)")
            continue
        header = (f"# Rainbow Space Princess art round {number}: {about} (t-020). Written by build_art_rounds.py in\n"
                  "# the house lane Silas chose from round 1. Private; generated art is inspiration until cropped,\n"
                  "# keyed and tested in the real cabinet. Submit with scripts/enqueue_art_requests.py --live.\n")
        ledger = {"round": number, "project_slug": SLUG, "designer": "Rainbow Space Princess art bay",
                  "is_public": False, "is_mature": False, "lanes": [lane], "subjects": rows}
        path.write_text(header + yaml.safe_dump(ledger, sort_keys=False, width=110, allow_unicode=True))
        print(f"wrote {path.name}: {len(rows)} subjects")
    print(f"{total} subjects across {len(ROUNDS)} rounds")


if __name__ == "__main__":
    main()
