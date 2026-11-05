# Cthulhuquarium console redesign — t-098 (UI) and t-099 (fish)

Silas, 2026-11-05 PT, with four ChatGPT mockups saved in `reference-2026-11-05/`
(`tank`, `feed`, `creatures`, `market`):

> Cthulhuquarium has some ways to go before it's ready for primetime. It still looks more like a
> webapp than a console game, and a lot of the fish designs are boring. I asked ChatGPT to create
> some art representing a finished draft. This version is a little more freeware slop than I want,
> the design is a little too childish, but it's still better than what we have. I need a front end
> redesign, actual art assets generated, and much better fish designs for a lot of our fish.

The mockups are a **structure** reference, not a style target. The rule is to keep their
structure and leave out the childishness.

## What the reference gets right (keep)

1. **The tank is the stage.** One painted, bezelled tank fills the screen at every width. Menus
   sit *on* the tank or replace its contents inside the same bezel; they never push it off the page
   or turn into a scrolling web page under it.
2. **A gilt-and-iron console bezel.** The tank sits in a heavy dark frame with brass/gilt corner
   ornament, tentacle flourishes at the corners and candles in the lower corners. The frame
   makes it look like a console game. Flat cards and rounded web panels make it look like a web app.
3. **Top HUD capsules, top-right:** coins, tank capacity (`5 / 8`), day and time. Small framed
   capsules, icon plus number, all the same height.
4. **Left care meters:** hunger, cleanliness, mood. An icon roundel plus a label, a percentage and
   a thin bar each, stacked top-left over the water. They are glanceable, not a dashboard.
5. **A bottom command deck:** five big illustrated tabs (**Tank, Feed, Creatures, Relics,
   Market**), each an icon painted above a label, with `L` / `R` shoulder hints at the ends. The
   active tab glows. This deck is the whole navigation.
6. **A button-prompt footer**, bottom-right or bottom-centre (`A Select · X Details · Y Favorite ·
   B Back`), changing per screen. Map it to keyboard keys and gamepad buttons, and show tap hints
   on touch devices.
7. **Creatures screen:** a left filter rail (All, Favorites, By rarity, By habitat, By type), a
   large featured-creature panel with name, epithet, quoted field note, rarity seal and that
   creature's own meters, and below them a horizontally paged card strip with rarity ribbons,
   a favourite star and a `Collected 28 / 36` count.
8. **Market screen:** the shopkeeper in the scene behind a counter with a speech bark, and five
   **pedestal cards**. Each card has the item art on a plinth, a name plaque, two lines of
   description and a coin price.
9. **Speech barks:** small framed bubbles from a creature or keeper, one line, in the scene.
10. **A Feed screen** that is the tank with the food action live: a hint banner and the
    `A ×1 / X ×5 / Y ×10` prompt row. The creatures react in the water.

## What it gets wrong (leave out)

- **Chibi faces, blush marks, `^_^` eyes, sparkle stars on everything.** These are what made it
  read as childish. Our creatures have real anatomy and a dry face, as in the canon tone: Little
  Inferno, Sunless Sea, Tim Burton. Not cute and not grimdark.
- **Everything purple.** The violet-on-violet is a generic fantasy-game look. Our palette is
  deep sea-green and ink-blue water, gaslight amber, verdigris brass, oxblood, bone. Violet is an
  accent for rare or eldritch things only.
- **Glow on every edge.** Use glow for the focus state and for bioluminescent creatures only.
- **The generic jellyfish shopkeeper.** Our shopkeepers are Charlotte Fishmonger and Wilbur Stint,
  who already exist as canon art. Use them.
- **Invented stats we don't have.** Map the reference's labels onto real game state. "Relics"
  is our sets/collection/decor content, "Day 14" is whatever the tank's clock really is, and the
  meters are the tank's real cleanliness/feed state. Leave a slot out rather than show a fake
  number.

## UI material language (t-098)

| Element | Material |
|---|---|
| Bezel | blackened iron with gilt/brass beading, riveted corners, faint verdigris |
| Panels on the water | smoked glass (dark teal at about 70%) with a thin gilt hairline and an inner bevel |
| Tabs | dark lacquered plaques, each with a painted icon, and a brass rim that turns sea-glass cyan when active |
| Type | a high-contrast serif for titles (the existing display face, or Cinzel or Cormorant if none), and a readable humanist sans for numbers |
| Price/coin | old gold coin with an embossed eye |
| Rarity | Common bone, Uncommon verdigris, Rare sea-blue, Epic violet, Legendary amber, Mythic oxblood-and-gold |

Generated UI art is part of the job: tab icons (tank, feed bowl, creatures, relic, market stall),
a title cartouche, a coin, corner ornaments and a plinth. Until a render lands, draw the asset in
SVG at the same size so the layout does not shift. The **painted art is the deliverable** and the
SVG is only a fallback. The renders go through the canon repo's `ui` group (see t-099 below for
the pipeline).

## In-tank sprite house style (t-099)

**Decided 2026-11-05 PT: one painted Krea 2 register for every swimming sprite.** The book
plates (Ichthyonomicon cards) keep their eight lineages; the tank no longer inherits them. Canon
source of truth: `silasfelinus/cthulhuquarium` `ART-DIRECTION.md` "The tank register" and
`art/sprite-style.yaml` (merged in cthulhuquarium#79).

Style test, same four creatures (lamplight angler, a redesigned ledger-shaped auditor, drifting
bell, sardine). Sheets are in `style-test-2026-11-05/`:

| Engine / style | Result |
|---|---|
| flux, gouache naturalist (`flux-gouache.jpg`) | Handsome but harsh and natural-history. It lost the designed traits (the auditor came back a plain fish) and the glow. Silas: *"too harsh and naturalistic. Illustrious or Krea would probably give us a much more dynamic style and palette."* The other three flux styles were cancelled. |
| **Krea 2**, painted dark-comedy game illustration (`krea2-vs-illustrious.jpg`, row 1) | **Chosen.** Dynamic jewel-tone palette with inked outlines, strict profile on a clean pale backdrop (cuts out cleanly), and keeps the prose details. |
| Illustrious: Arthemy Western Art v3 (row 2), Illustrij v2.1 (row 3) | The most personality (Arthemy's monocled auditor), but the tags gave the angler and sardine legs, they render on dark floors with cast shadows, and tag prompts drop the bespoke concepts. A candidate for hero/plate art later. |

**Roster.** All 151 sprite prompts were rewritten as a bespoke subject, then the house clause,
then the cut-out framing. **44 species got new designs** because their concept was an object
or sheet layout that can't swim, or a stock fish with nothing to look at. Name, joke, field
note and voices are unchanged. Their card `art_prompt` subject changed too, with the plate
clause kept. 151 sprites and 13 UI art pieces were submitted to Krea 2 on 2026-11-05 (ArtJobs
64175–64338). Swim clips follow their new stills automatically (`render_art.py`).

**Delivery loop** (canon repo): `bash scripts/deliver.sh` harvests, cuts out, re-submits clips
whose new still landed, and syncs to kind_robots. Then review `scripts/contact_sheet.py`,
re-prompt misses (set `sprite.faces: left` for left-facing renders), and open the kind_robots
sync PR.
