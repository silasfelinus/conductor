# Hopeful Hues: human playtest checklist

**Prepared:** 2026-11-25 PT, after kind_robots#5856. **Where:** `/play/hopeful-hues` (standalone Play
page). This is a handoff for people to play, not a gate the build roadmap waits on. Agents verified
everything in "Already machine-verified"; humans are asked only for what a machine cannot judge.
Promo card (not for posting until Silas approves sharing): `promo/hopeful-hues-promo-1080x1350.webp`.

## Already machine-verified

- **Every level winnable.** `npm run test:hopeful-hues` has a bot win all 495 levels across nine
  worlds without gifts. It also checks saves, quests, achievements, endings, the scrapbook, and the
  three board mechanics: conveyor rows, portals and buddy dispensers.
- **Played in a real browser.** `verifyHopefulHuesBrowser.browser.test.mjs` runs at 390/768 by touch
  and at 1440 by mouse and keyboard. It covers:
  - no audio until the first tap
  - the first-level tutorial, and level 1 won by dragging tiles
  - Back restoring the board exactly
  - keyboard swaps
  - a quest claimed
  - switching worlds
  - save export and import
  - calm motion
  - a world finale played to its ending
  - no sideways scroll at any width
- **Art.** All 118 painted in-game images are delivered and render: heroes, world keys, regions, maps,
  54 story beats and 10 endings. All 90 board tiles are painted too (six jewels, rainbow, buddy, knot
  and Gloom mist per world), checked in play at 390 and 1440 with the colorblind symbols on top.

## Please play and tell us

1. **First five minutes (phone).** Start a new adventure with Superkate. Is the tutorial clear? Does
   the Back button feel like the special thing it is?
2. **Difficulty.** Play Sunrise Salon Street levels 1–10. Too easy, right, or frustrating? Note where
   you first used Back because you were stuck.
3. **New mechanics.** In Coral Carnival (conveyor rows) and Rainbow Falls (portals), and in
   Clanktown's Clocktower (buddy chutes): are the markers and the first-time tip enough to understand
   them?
4. **Other worlds.** Try two other heroes (for example Ottilie's Rosewood Nocturne and Captain
   Jubilee's Starlet Corsair). Do they feel different enough?
5. **Story and endings.** Do the story pages and the ending feel warm and hopeful? Is anything
   confusing for an 11-year-old?
6. **Sound.** Music and sound effects on a real phone speaker and on headphones. Are the Settings
   volumes comfortable?
7. **Quests and rewards.** Do the daily and weekly quests and the Sparkles feel rewarding without being
   pushy? (No lives, timers or purchases, by design.)
8. **Look and feel.** Anything that looks unfinished or hard to read? On a phone, can you tell every
   painted jewel in a world apart at a glance (try Circus and Dust and Neon, which had look-alikes fixed)?

## Decisions only Silas can make

- Public promotion, sharing the promo card, and any deploy (Force Update).

Report findings as `playtest_iteration: true` tasks in `projects/hopeful-hues/roadmap.yaml`, or as
comments on kind_robots#5649.
