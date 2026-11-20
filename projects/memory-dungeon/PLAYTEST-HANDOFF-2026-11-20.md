# Memory Dungeon: ready for human testing, 2026-11-20 PT

**Playable route:** https://kindrobots.org/play/memory. No sign-in needed. Progress autosaves in the browser.

**Lifecycle:** `playtest` / `normal` priority (Silas, 2026-11-20 PT: *"You are responsible for getting memory dungeon ready for human play tests, which will involve tagging and closing the open GitHub roadmap and then changing the kind robots project to 'playtest' with normal priority ... roadmap should aim to get to human play test ready, nothing beyond."*). The finite roadmap is closed: 32 tasks done and 41 cancelled as beyond playtest, each with a `cancelled_reason` that says what shipped. New fixes go in as `playtest_iteration: true` tasks. This handoff is **not** publication, promotion or creative sign-off.

## What testers get

- **Title screen.** Pick a deck (Enchanted, Your Art, or Kind Robots characters), then Begin the tale / Continue Briar Marches. Classic Match is one button away and unchanged.
- **Prologue.** Rowan trades lives with the changeling Morrow and picks what to hold onto.
- **World chain.** Each world opens when the one before it is finished:
  - **e01 Briar Marches:** a 64-site overworld revealed by memory matching in four waves, and the 36-room House That Remembers with three resolutions × four lenses (12 painted epilogues).
  - **e02 Dark Briar:** the twisted reflection of e01.
  - **e03/e04 Morrow's Earth:** Morrow's Shift, Sublevel B, the Unbelieving City and the flooding archive.
  - **e05/e06 Scylla:** the shore, the Glass Throat tunnels, the Undertide Crown and the Choking Works.
  - **e07/e08 Hoshimori:** Lantern Village and The Shut Doors (Vesper), with the Furnace of Names.
  - **e09 Pip's broken forest** and **e10 Morrow's broken city:** the first two collision maps.
- **End of the build.** After e10's verdict the game says the player has reached the end of this playtest build, and the bar shows "Playtest build complete" (kind_robots#5388). e11 and e12 are not built.
- **Around the edges:** memory combat with weapon shapes, Minefield logic floors, the Earth Chronicle photographs, Threads and Medals, 12+ live achievements, three manual checkpoints, card-back and deck settings.

## Verification on record (2026-11-20 PT)

- **Seeded suites on kind_robots main `d7cafdd2`:** all seven `npm run test:memory-*` suites pass.
  - World One: 20 seeded runs, 36,692 actions, 2,425 reloads, all three House endings, 0 softlocks or save drifts.
  - Dark Briar: 36 seeded runs, 18,871 actions, 1,741 reloads, 0 softlocks.
  - Combat: 5 player models × 3 boards × 200 seeds. Minefield: 160 guess-free floors.
- **Overworld catalog:** `verifyMemoryOverworldEvents` passes (768 cells across 12 graphs, fixed photos, no duplicate rewards).
- **Art:** `audit_memory_dungeon_art_delivery.py --live` shows 752 of 752 ArtJobs rendered and delivered to the media host.
- **Real browser on production, signed out, at 390, 820 and 1440 wide:** launcher → prologue → Briar overworld → reload → Continue all work, with no page scroll and no broken images. Flipping cards with the Enchanted deck and with the Kind Robots Character deck both show real art (the old "zero images" Character deck bug, t-049, no longer reproduces).

## Known limits

- **The story stops after e10.** e11 (Char), e12 (Vesper) and the ~32-ending finale are cancelled from this roadmap as beyond playtest. Their design docs stay in this folder for a future roadmap.
- **Deep worlds were not clicked through in a browser.** e03–e10 are covered by reducer, store and contract tests. The browser pass covered the start flow and World One's opening.
- **Saves are per-browser.** There is no account-backed save, so a tester who switches devices starts over.
- **Settings are minimal:** card back, gallery deck and checkpoints. No volume, text-size, reduced-motion or high-contrast options yet.
- **Realm Gallery deck** stays locked or shows "Art pending" until all 32 paintings for a realm are curated.
- **Console noise:** every width logs a harmless "Hydration completed but contains mismatches" message.
- **Signed-in and mature decks** were not rechecked in this pass.

## Owner decisions

- **Your fun verdict and acceptance** happen after this handoff, outside the roadmap.
- **Next production scope** (e11/e12, the endings finale, galleries, settings): a new roadmap if you want one. The cancelled tasks list exactly what was left.
- **Public promotion:** nothing here authorizes it.

## Human playtest checklist

1. **First visit, on a phone.** Open /play/memory. Does the title screen tell you what to do?
2. **Pick a deck.** Try the Kind Robots Character deck once. Do the cards show real pictures?
3. **Prologue.** Read it and pick a choice. Is the setup clear?
4. **Briar's first wave.** Match pairs to reveal map squares. Does matching feel like exploring?
5. **Reload mid-wave.** Close the tab, reopen /play/memory, press Continue. Did you land where you left off?
6. **An encounter.** Step onto a revealed site and play a combat board. Do weapon shapes make sense?
7. **The House That Remembers.** Find its entrance and reach one of the three endings. Is the ending painting shown?
8. **Dark Briar (e02).** Enter the reflection. Does it feel like a twisted mirror, not a recolor?
9. **Morrow's Earth and Scylla's sea (e03–e06).** Do the stories hold together? Any site that feels like filler?
10. **Hoshimori (e07/e08).** Is the night version actually unsettling?
11. **e09 and e10.** Do the collisions feel like earlier choices coming back? Is the end-of-build message clear?
12. **Pacing.** Where did you get bored or lost? (This replaces the cancelled t-051 rebalance.)

When reporting, include the world, the map coordinate if shown, the deck, device and window size, and a screenshot if you can.

**Master issue:** [Kind Robots #4136](https://github.com/silasfelinus/kind_robots/issues/4136). It is flagged for human testing and closed as completed because the playtest roadmap is done. That is not a claim that anyone has played or accepted it.
