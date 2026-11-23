# Hopeful Hues: Superkate & the Kind Robots

**Project slug:** `hopeful-hues`
**Frontend:** `/admin/hopeful-hues` (admin preview; public `/play` promotion is a separate human gate)
**Static game:** `kind_robots/public/hopeful-hues/` (vanilla JS, no build step)
**Master issue:** [Kind Robots #5649](https://github.com/silasfelinus/kind_robots/issues/5649)

## Direction (Silas, 2026-11-23 PT, verbatim)

> New project, a desired clone of candy crush, but with a back button. Themed on superkate, kind
> robots, and general good vibes. I expect daily and weekly quests, achievements, loooooooong maps,
> sound, music, save load settings, scrapbook, character select, multiple pathways, unique endings,
> and an overall rainbow and colorful aesthetic. Hopecore. Cutecore.

Interpretation: an **original** match-three in the genre, not a recreation. No borrowed names,
characters, art, music, level layouts or look. The signature feature is the **Back button**: undo
any swap exactly, as often as you like (configurable limit in Settings), including from the "So
close" fail screen.

## Theme

Superkate (rainbow hair hero, Silas's partner's stylist persona) and the Kind Robots paint a world
back to color after the Grey Drizzle rinsed it grey. Hopecore/cutecore: no lives, no timers, no
purchases, gentle fail copy, a daily kindness note, and an ending where the antagonist is a lonely
cloud who just wanted to be in the picture.

Tiles: Rose heart, Tangerine star, Lemon sun, Mint leaf, Sky drop, Violet moon (each color has its
own shape and an optional symbol for colorblind play). Specials: Rainbow Comb (4 in a line, sweeps a
row or column), Glitter Bomb (L/T, 3x3 blast), Rainbow Dye (5 in a line, clears a color). Special +
special swaps make bigger combos. Blockers: Gloom (1 or 2 layers under tiles), Tangles (fixed
knots), Robot buddies (bring to the bottom row; a buddy can always step down one space; specials
beam buddies home).

## Structure

- 7 regions, 130 seeded levels. Sunrise Salon Street (18) forks to Glitter Grove or Gear Garden
  (18 each), each forks again to two far regions (19 each, the last a heart-shaped finale).
- One playthrough route is 55 levels. Four route endings (Lullaby, Parade, High Score, Letters)
  plus a secret fifth, *Everyone's Rainbow*, after finding all four.
- Heroes: Superkate (starts with a Rainbow Dye), Sprocket (+2 moves), Juniper (5x5 bombs),
  Marigold (big cascades give bonus moves). Each has their own ending epilogue.
- Meta: three save slots, export/import codes, daily (3 of 15) and weekly (3 of 9) quests,
  32 achievements, a five-tab scrapbook (story beats, region postcards, friends, endings,
  stickers), sparkles currency for +5 move gifts, settings (music, SFX, reduced motion, high
  contrast, tile symbols, large text, hints, Back limit).
- Audio: WebAudio-synthesized SFX and procedural per-region music; starts on first gesture.

## Quality bar

`npm run test:hopeful-hues` checks determinism, starting boards, special creation, exact Back
restoration, save round-trips, route/ending logic, and that a greedy one-move-lookahead bot wins
every one of the 130 levels (currently all without the +5 gift). Screens were checked at
390/768/1440 and 844x390 landscape.
