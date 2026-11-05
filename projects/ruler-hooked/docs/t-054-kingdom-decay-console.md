# The Ruler Is Hooked — kingdom-decay console redesign (t-054)

Silas, 2026-11-05 PT, with three mockups saved in `reference-2026-11-05-blight/` (`lake`, `map`, `court`):

> The designs have been too cutesy, so I had some demos done for when the kingdom goes bad due to poor
> management. This is still a work in progress, it needs more individuality, it looks like every other
> ai slop project. But it's a clear visual design and much closer than the webapp look we've had.

The live game (`/play/ruler-hooked`, checked 2026-11-05) is a soft pastel storybook castle-and-lake
painting inside a web-app chrome bar. The mockups are a **structure** reference and the **bad-reign
end of the visual range**. They are not a style to copy, because Silas calls their look generic.

## Keep (structure)

1. **First-person fishing stage, full screen.** The rod and the ruler's own sleeves sit in the
   foreground and the lake fills the view. This matches the existing first-person POV in the compositor
   (t-047 note).
2. **Top-left title cartouche, top-right HUD capsules:** treasury coins, day count, time of day
   (`Dusk`).
3. **Left kingdom meters**, one per axis with an icon roundel, a percentage and a coloured bar. The
   mockups say Hearts / Nature / Prosperity / Order. Ours are `joy` (shown as "Hearts"), `nature`,
   `prosperity` and `order`, with `treasury` as the coin capsule (`types/ruler-hooked.ts` `AXIS_KEYS`).
4. **A petition banner**, top-right: the newest interrupt card as a hanging pennant with a wax seal.
5. **A tension meter plus button prompts** while a fish is on the line (`A Tap to Reel`,
   `R Release for Slack`). It should drive the existing timing bar (t-053 reconciles that bar's UI
   consumer).
6. **Bottom five-tab deck: Lake, Map, Court, Gear, Fishopedia**, with an L/R and A/X/Y prompt footer.
7. **Map:** a painted kingdom map with named regions, a selected-region card (art, description, key
   fish, quest, travel time) and a Current Objective card.
8. **Court:** the petitioner large on the left, the edict on a parchment sheet, and **three choice
   cards, each with art and signed stat deltas** (`Prosperity +15%`, `Nature −18%` …). This is the
   card/effects model we already have (decks.md), made visible before you commit.

## Change (the decay is the point)

The mockups show only the ruined end. The game's identity is that **the same screen degrades or
flourishes with the reign**. The compositor already resolves `{region}-{state}-{time}` layers off the
axes (`utils/rulerHooked/content.ts`). The far shore, treeline, village and castle have state ramps.
The **lake (`clear` only), near bank (`grassy` only) and sky have none.** The mockups' strongest
decay signals all live in those three layers: the oil-sheen black water, the dead reeds and
floating bones, the smoke-choked sky. Add ramps:

| region | driver | ramp (bad → good) |
|---|---|---|
| lake | nature | poisoned (oil sheen, bones) → murky → clear |
| near_bank | nature | dead reeds and bones → trampled → grassy |
| sky | joy (Hearts) | smoke-choked → overcast → open |

Order very high while joy is low is tyranny. That drives gallows, pikes and guard towers on the
far_shore and village layers as **event overrides** (the compositor already supports pinned
overrides), not a separate ramp. The UI chrome should also take the reign's state: clean when
healthy, then tarnished, soot-stained and frayed as the meters fall.

## Individuality (open question, style test running)

What reads as "every other AI slop project" in the mockups: the orange-to-violet dusk sky,
hyper-detail at equal intensity everywhere, rope/bone/driftwood trim on every single element, and the
generic grim-medieval painterly look. A 2026-11-05 Krea 2 style test renders the blighted lake and the
court petition in three directions, so the pick is made from real images:

- **chronicle**: an illuminated-manuscript miniature (flat tilted perspective, tempera and gold leaf)
  that itself rots, with tarnished gold, soot, spilled ink and grotesque marginalia. The kingdom is
  painted as its own chronicle.
- **broadside**: a hand-coloured 16th-century woodcut broadside, the pamphlet printed *about* a bad
  king, in three hand-laid inks.
- **oil**: the mockups' painterly approach, minus the dusk cliché: chartreuse/slate/umber and flat
  overcast light.

Sheet: `style-test-2026-11-05/chronicle-broadside-oil.jpg` (Krea 2, ArtJobs 64339–64344; rows: chronicle, broadside, oil; columns: lake, court). Read: **chronicle** is the most individual. The fish-marginalia border and flat tempera are unlike any other game, and "the chronicle rots" carries the decay directly. **Broadside** is the most graphic and readable at game scale and composites cleanly. **Oil** is closest to the mockups and the least individual.

## Decided 2026-11-05 PT: Chronicle for the world, Broadside for its documents

Silas picked **Chronicle + Broadside** from the style test.

- **Chronicle (the world):** scene layers, map and UI chrome. The kingdom is painted as its own
  illuminated chronicle: flat tilted perspective, tempera, gold leaf, lapis and vermilion, and
  fish-bodied marginalia in the borders. **A healthy reign is pristine:** bright lapis, burnished
  gold, playful marginalia. **Misrule rots the book:** the gold tarnishes and flakes, soot and
  spilled ink spread, the vellum foxes and tears, and the marginalia fish turn grotesque. Scene
  layers render *without* the border (they composite), and the border becomes the UI frame, with a
  rotted variant per reign tier.
- **Broadside (documents in the world):** edicts, petitions, choice cards, notices and the
  Fishopedia entries. They are hand-coloured woodcut pamphlets on rag paper, in madder, ochre and
  verdigris. These are what the court *prints*, so their look stays the same and their tone sours
  (blunter edicts, cruder cuts) with the reign.
