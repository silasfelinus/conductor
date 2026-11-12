# Zuzu: Shifting Lands — main-game standard audit (2026-11-12, kind_robots 7ad1136)

This was a read-only audit of kind_robots at `origin/main` 7ad1136 and the conductor repo. Live records come from `https://kindrobots.org/api/achievements`, which has 145 records. Paths below are relative to `/home/user/kind_robots` unless they start with `conductor/`.

## Shared plumbing to know first

**How game achievements are wired:**
- **Definitions** live in `utils/achievements/catalog/games.ts`. The game must also be listed in `OTHER_GAMES` in `utils/achievements/gameAchievements.ts:78-136`.
- **Sections:** `AchievementSectionKey` (`gameAchievements.ts:14-15`) only allows site, arcade, zuzu, shifting-desks and emperor-of-dust. Ecotone, Memory Dungeon and Crystal Street each need a new section or have to reuse one.
- **Test rules** (`utils/scripts/verifyGameAchievements.test.ts`) apply to every entry:
  - label of 32 characters or fewer, plus a tooltip and a subtleHint
  - an art prompt of at least 30 words
  - an icon that exists in `assets/icons`
  - non-arcade games must use `rule: event`
  - the code must appear as a literal string in components, stores, pages or utils
- **Records:** `scripts/seed_achievements.ts` upserts them by triggerCode. You can also use admin `POST /api/achievements/batch`.
- **Display:** the strip only shows for games in `ACHIEVEMENT_GAMES`, through the workspace sheet's route match (`components/navigation/workspace-sheet.vue:176`). No game renders it inside its own UI yet.
- The header comment "three per game" in `gameAchievements.ts:3` is out of date.

---

## Zuzu: Shifting Lands (`/play/zuzu-shifting-lands`)

### A) Audit

| Item | Status | Evidence | Gap to close |
|---|---|---|---|
| Title screen | Missing | `pages/play/zuzu-shifting-lands.vue:3` mounts `ShiftingLandsJourneyBoard` directly and auto-restores the run. | Add a title console with New / Continue / Settings / Scrapbook / Achievements. |
| Settings | Partial | Journey menu (`components/shifting-lands-journey-board.vue:82-147`) has Motion on/off and Dice sound on/off, stored at `kr.shiftingLands.presentation.v1` (`utils/shiftingLands/presentationPreferences.ts:8`). "New journey" asks for confirmation (`journey-board.vue:1764`, `1884`). | Volume and music, text size, reading speed, high contrast, and a "reset all progress" option. |
| Save / load | Partial (local is Met) | `kr.shiftingLands.journeyLedger.v9` (`stores/shiftingLandsJourneyStore.ts:102`) is a replay ledger with a versioned migration chain from v2 to v9 (`:390-461`). Reload continues automatically, and a restoreWarning shows on failure. | No account-backed save. No store for unlocks that carry across runs. |
| 12+ achievements | Partial | 3 live: `zuzu-shifting-lands-open-door` / `canyon-warden` / `beyond-the-verge` (ids 1285-1287). Awarded in `awardJourneyDeeds` (store `:516-534`). The strip shows only in the workspace sheet. | 9 or more new achievements, plus the strip inside the board. The live messages name Zuzu ("Zuzu passed…"), so they need neutral rewording once the creator ships. |
| Scrapbook | Missing | The Trail Ledger (`journey-board.vue:1211+`) covers the current run only. "New journey" wipes it. | A persistent store for endings, cast met, art and run pages, shown with silhouettes and "X of N". |
| Endings | Partial | 19 distinct titles, listed below the table. Every ending renders the same plate, `/zuzu-gamebook/scenes/zuzu-alone.webp` (`journey-board.vue:677`). | 19 painted plates queued through an auto_submit ledger, and an `endingArt(kind)` helper in `sceneArt.ts`. |
| Characters | Missing | Zuzu is hard-coded (details in section B). | The character creator (conductor t-052). |
| Replay hooks | Partial (2 of 3) | Seeded layouts and card draws (`deckV6.ts` `drawFor`). Branching through deeds, marks and the kitchen-sister follower (`saveLedgerV9.ts`). | Unlockables that carry across runs, and alternate starting characters (the creator delivers the second). |

The 19 ending titles: 10 mark-based kinds (`utils/shiftingLands/endingsV6.ts:4-14`, each with complete, fallen and retired text), 2 V7 variants ("The Debt Carried Open" and "A Road Wide Enough for Everyone" in `endingsV7.ts`), and 7 constellation endings (`endingsConstellationsV7.ts:20-98`).

### B) Character customization: current state and creator plan

**Current stat model.** Six skills: steel 3, awareness 2, wits 2, bearing 2, resolve 2, insight 2, for a total of 13. HP maximum is 8, and play starts with 2 provisions. The skill table is copied in five places:
- `journey.ts:74`
- `deckV6.ts:169` (applied at `:350`)
- `authoredBosses.ts:52` (trial modifier at `:114`)
- `progression.ts:51`
- `authoredFiveLands.ts:38`

The HP ceiling of 8 is a literal in the clamps (`deckV6.ts` around `:370`, `journey.ts:482`, `authoredBosses.ts:128/213`) and in the type `maxHp: 8` (`progression.ts:41`). Progression is derived from authored outcomes: techniques, items, conditions and relationships.

**Where Zuzu is hard-coded:**
- `components/shifting-lands-character-rail.vue:4,9,19` (portrait `zuzu-alone.webp`, heading "Zuzu · Character sheet")
- `journey-board.vue:1237` ("Zuzu's travels"), `:1504` (the "Zuzu" tab) and `:677` (the ending plate)
- legacy `homestead.ts` (12 mentions, but only in the hidden workshop mode)
- the three live achievement messages

The good news: the deck validator rejects any card that names Zuzu (`deckV6.ts:556`). All deck JSON is second person, with zero hits for ronin, katana, koala or sword. Encounter text is already portable to other characters.

**Cast in encounters today.**
- The Abbess, an otter, is the Homestead trial boss (`authoredTrials.json`) and appears on cards such as `bread-under-the-long-table`, `the-infirmarys-last-cot` and `the-guest-book-on-the-lectern`.
- The kitchen sister is a convent novice, not the fennec sister. She is the V9 follower (`saveLedgerV9.ts`, `followerEchoesV8.ts`).
- Storm-crow cards appear throughout the cave land.
- Named NPCs Tamsin, Pell, Orrin, the Hallorans and a Broker each have their own card.
- `a-tithe-basket-at-the-gate` features "three hungry raccoon children".

**The fennec siblings and Jeffery Mittens do not appear in Shifting Lands at all** (zero grep hits). Book One canon (`conductor/projects/zuzu-gamebook/BOOK-ONE-OUTLINE.md:67-73`):
- the sister: fennec, about 10
- the toddler: fennec
- the Abbess: otter
- Jeffery Mittens: young raccoon looter
- also Sister Wren and the Coyote Vagrant

So "never meet yourself" needs a cast-tagging system plus new cameo cards. As things stand there is nothing to exclude.

**Fit.** Strong. Silas has already decided this (conductor t-052). I'd leave the Abbess out of the playable list because she is the Homestead trial boss.

**Implementation plan (about 3 PRs).**

1. **Data model: new `utils/shiftingLands/characters.ts`.**
   - `PlayableId = 'zuzu' | 'jeffery-mittens' | 'fennec-siblings' | 'coyote-vagrant' | 'custom'`
   - `ShiftingCharacter = { id, name, species, pronouns, portrait, skills: Record<Skill, number>, startProvisions, signatureFlags: string[], identity: string[], knows: string[] }`
   - **Zuzu** uses exactly today's numbers, so his runs replay unchanged.
   - **Jeffery:** steel 1, awareness 3, wits 3, bearing 1, resolve 2, insight 3. Signature flag `deed-knows-old-roads`, an existing deed that opens existing gated routes. This gives "stats change options" for free.
   - **Fennec siblings:** awareness 3, resolve 3, bearing 1, other skills 2.
   - **Custom:** point-buy on the same budget, total 13, each skill 0–4. Species comes from a static list of approved Zuzu-world species, not a database read, because the reducer has to stay pure. Name up to 24 characters, pronouns, and a species portrait.
   - Add `validateCharacter()`.
2. **Ledger: `saveLedgerV10.ts`.**
   - `JourneyLedgerV10 = V9 & { version: 10; character: ShiftingCharacter }`.
   - Store a *snapshot* of the character, not an id, so later premade tuning never rescores old saves.
   - V9 saves restore as the Zuzu snapshot.
   - Save key `kr.shiftingLands.journeyLedger.v10`, with v9 added to the store's legacy chain.
   - `newJourneyLedgerV10(seed, character)` pre-seeds `signatureFlags` into `flags`.
3. **Stat threading.**
   - Add an optional `skills` parameter, defaulting to the base table, to `chooseV6` / `stepJourneyV6` (`deckV6.ts:350`) and `stepAuthoredTrial` (`authoredBosses.ts:114`). V6–V9 replays then stay byte-identical.
   - `stepJourneyLedgerV10` passes `ledger.character.skills`.
   - `v6CharacterSheet` / `journeyCharacterSheet` take skills and portrait.
   - Keep the HP maximum at 8 in this first version to limit churn.
4. **Identity exclusion.**
   - New `utils/shiftingLands/castCardsV10.json` with cameo cards, each with a `cast: string[]` field and an optional `selfVariant`:
     - "Two Fennecs at the Ferry" (dustwater)
     - "A Raccoon Stripping Boots" (tablelands)
     - "Coyote at the Well" (homestead)
   - A sidecar `castTags.ts` maps existing card ids to cast. For example, the Abbess cards, and the raccoon children card as a species echo.
   - Use a sidecar rather than editing `authoredDecksV6.json`. The deck fingerprint and schemaVersion pin replay; t-049 used the same sidecar pattern (`deckV6.ts:53-58`).
   - Add `v10Pool(locationId, character)`: the V6 pool plus cast cards, minus any card whose `cast` overlaps `character.identity`. If the card has a `selfVariant` (for example, "your old raider crew recognizes you" when playing Jeffery), swap it in instead of dropping it.
   - Keep `drawFor` hashing unchanged.
   - Knowledge gates: add deed flags such as `deed-knows-fennec-siblings` to `DEED_FLAGS`. Zuzu's `knows` entries pre-seed these, which unlocks "recognize them" choices. The validator rejects gates on non-deed flags (`deckV6.ts` around `:591`), so these must go into `DEED_FLAGS`.
5. **UI.**
   - New `components/shifting-lands-character-creator.vue`: premade cards plus a point-buy stepper showing odds via `trialOdds.ts`.
   - Shown on first run and from "New journey" (`journey-board.vue:1764`).
   - The store's `fresh(character)` (`shiftingLandsJourneyStore.ts:574`) and a new `character` computed.
   - The rail, tab label and ending plate read `game.character`.
   - Rewrite achievement messages to second person in `catalog/games.ts:193-235` and reseed.
6. **Tests: new `utils/scripts/verifyShiftingCharacterCreator.test.ts`.**
   - A V9 fixture restores as Zuzu and its outcomes match V9 exactly.
   - A Zuzu V10 run with the same seed and actions matches V9.
   - Point-buy rejects totals other than 13, values below 0 and values above 4.
   - Deterministic sweep: for every playable character and seeds 1–500, every location's drawn card has no cast/identity overlap, and every pool is non-empty.
   - Jeffery's wits flips a known check for a fixed seed.
   - `restore` rejects a tampered snapshot.
   - Validate the cast cards with the same rules as `validateDeckV6`.
7. **Art.** Queue an auto_submit portrait ledger at `conductor/projects/zuzu-shifting-lands/art/` (Jeffery, fennec siblings, coyote, custom-species set). The `public/zuzu-showdown-portraits/mittens-*` files exist as stand-ins, but they're fighting-game style.

### C) Proposed achievements (18, prefix `zuzu-shifting-lands-`)

All hooks go in `awardJourneyDeeds`, `store:516`. Widen it to receive the previous and next ledger plus the action.

1. `open-door` (keep): pass the homestead trial.
2. `canyon-warden` (keep): pass the tablelands trial.
3. `beyond-the-verge` (keep): phase becomes `complete`.
4. `crossing-gate` "The Crossing Gate": newest boss landId is `dustwater`.
5. `storm-crow-depths` "Out of the Depths": newest boss landId is `cave`.
6. `hard-roll` "Against the Odds": the latest outcome has `roll.difficulty >= 10` and succeeded.
7. `witness-trial` "Many Voices": the latest trialResult has choiceId `witness` and `roll.success`.
8. `scouted` "Scouted Ahead": a trial passed after a `PREPARE` for that land.
9. `kitchen-loyal` "Two Witnesses": the V9 follower choice is `stand-as-witness`.
10. `restitution` "Bread for Bread": follower choice `offer-restitution`.
11. `spent-deed` "Paid in Deeds": a CHOOSE where `choiceSpends(...)` is non-empty.
12. `healer` "Willow Bark": `USE_REWARD` with `willow-bark-dose`.
13. `honest-road` "No Toll Taken": complete the run with no `tribute` or `coerce` trial choices.
14. `wide-road` "Wide Enough": ending title is "A Road Wide Enough for Everyone".
15. `debt-carried` "The Debt Carried": ending path is "Reckoning and partial repair".
16. `constellation` "Star-Read Road": a constellation ending is applied (`moralConstellationEndingV7` changed the base).
17. `turn-back` "Knowing When": phase becomes `retired`.
18. `ending-collector` "Five Roads Remembered": 5 distinct ending kinds in the scrapbook. This depends on the scrapbook PR.

After the creator ships: add `own-legend` (complete as a custom character) and `mittens-road` (pass a trial as Jeffery).

### D) Three smallest high-value PRs (the creator is its own task)

1. **Achievements 3 → 18.** Edit `catalog/games.ts`, the award logic in `stores/shiftingLandsJourneyStore.ts`, and add `GameAchievementStrip` to the journey-menu dropdown.
2. **Title console and scrapbook.**
   - New `utils/shiftingLands/scrapbook.ts`, key `kr.shiftingLands.scrapbook.v1`, holding endings, runs, cast met and plates.
   - New `components/shifting-lands-title.vue` and `components/shifting-lands-scrapbook.vue`.
   - `fresh()` records the finished run before resetting.
3. **Ending plates and settings.**
   - Queue 19 plates in the conductor ledger, add `endingArt()` in `sceneArt.ts`, and swap `journey-board.vue:677`.
   - Extend `presentationPreferences.ts` with text size, contrast, volume and a confirmed reset.

---

## E) Shared and reusable components

- **Playbook Kit** (`components/playbook-kit/*`, `stores/playbookKitStore.ts`, `utils/playbookKit/settings.ts`):
  - settings for text size, font, contrast, motion, text speed, sound, trailer and romance
  - scrapbook, endings, secrets, cast and trailer panes
  - one versioned localStorage record per game
  - Used by Monstrique, Game of Captains and Every Villain Tactics. It's the closest thing to a standard settings panel, scrapbook and title console. Its settings pane could be lifted for Shifting Lands and Memory Dungeon.
- **Crystal Street's** title / settings / scrapbook / endings set (`components/crystal-street/*`) is the most complete per-game example: armed-confirm reset and the "???" endings wall.
- **3-slot saves with export/import:** Ecotone (`stores/ecotoneStore.ts:261-330`) and Memory Dungeon (`utils/memoryDungeon/saveSlots.ts`). They follow the same pattern and could share a helper.
- **`components/achievements/game-achievement-strip.vue`** is reusable, but nobody mounts it inside a game today.
- **`PlaybookRunReview`** (`stores/playbookRunReviewStore.ts`) is a per-run feedback form, not a scrapbook. Don't count it toward item 5.
