# Later-land authored decks: handoff and safe integration

These source packs extend the existing Homestead 12-card pack without changing any existing location IDs or importing records into Kind Robots.

| Land | Canonical locations | Authored cards | Choices | Written outcomes |
| --- | --- | ---: | ---: | ---: |
| Dustwater Crossing | ferry-landing, trading-post, dry-delta | 9 | 18 | 36 |
| Broken Tablelands | quarry, canyon-trail, canyon-camp | 9 | 18 | 36 |
| Storm-Crow Depths | cave-mouth, stone-hollow, underground-crossroads | 9 | 18 | 36 |
| Black Verge | obsidian-road, fortified-camp, last-threshold | 9 | 18 | 36 |
| **New total** | **12 locations** | **36** | **72** | **144** |

Together with the pre-existing **Homestead 12**, the design-source inventory is now **48 cards, 96 checked decisions, 192 authored success/failure passages** at all 15 canonical journey locations. The game still draws **one** fixed identity for each visited place; it never plays all three candidates in one run.

## Source authority and character identity

- Draft files are `DUSTWATER-9.json`, `TABLELANDS-9.json`, `STORM-CROW-9.json`, `BLACK-VERGE-9.json`; all use the original `ENCOUNTER-PACK.schema.json` and `WORLD-DECKS.json` v2 location IDs.
- The fixed cast and occupation are bespoke **design characters**, not asserted existing live Character database IDs. `locked_character_id: null` is intentional until the World Studio inventory verifies a match.
- No card claims its bespoke illustration already exists. `art.status = design-only` and `art_ref = null` prevent accidental use of unverified resources.
- Good, dangerous, and ambiguous cards are balanced **within every location**, not assigned by species. Cave/Verge gorillas appear under imposed supernatural conditions or in ordinary roles; the condition is not innate to the species.
- The storm-crow witches live in the cave, but occult motives and the unresolved former-human history are introduced by player-facing clues only. No draft announces an ending or grants secret knowledge to Zuzu without a corresponding encounter.
- Four scenes have explicit cause-dependent, prospective map shifts: Dry Delta water channel, Canyon Trail crumbling shelf, the Crossroads Below moving arch, and the cooling Obsidian Road seam. Older visited history must never be rewritten.

## Runtime integration is **not** part of this source-only deliverable

The Kind Robots `utils/shiftingLands/authoredJourney.ts` currently applies authored choices only at **Homestead**. On later lands its reducer still uses prototype `RESOLVE` actions. **Do not claim these new scenes are playable merely because these files merged.**

To make the next four lands playable:

1. Add a versioned import/verification step that converts each authored pack to the existing player-safe card DTO while omitting `developer_note`, unverified cast-resource IDs and art briefs from the displayed card reader.
2. Migrate the V3 replay ledger with an **explicit V4 contract or equivalent compatibility boundary**. An existing V3 run that already cleared a later land must remain replayable under its original prototype rules, with dice and visit history intact. Do not mutate `packSha` in place and silently reinterpret old saved actions.
3. Seed one fixed encounter ID per location, persist the location-specific choice/2d6/result and flags, and apply only author-approved causal shifts to *unvisited* places. Do not give a new card on revisits, reloads, or re-renders.
4. Connect the current private Admin reader and journal to the new land packs, preserving stable card flip/keyboard focus, one-use rewards, and the existing custom card backs. Use image-shaped pending art placeholders until scene-specific ArtImages are actually rendered and verified.
5. Run deterministic seed tests, mid-land reloads, V2/V3 migration coverage, invalid-save rejection and five-land balance sims before exposing any new public route. The public play route still requires the human t-018 release gate.

Validation: `node --test projects/zuzu-shifting-lands/encounters/later-lands.contract.test.mjs`; the Shifting Lands Manifest workflow runs this together with the existing Homestead and geography checks.
