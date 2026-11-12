# Memory Dungeon — main-game standard audit (2026-11-12, kind_robots 7ad1136)

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

## Memory Dungeon (`/play/memory`, rendered by `components/pages/memory-dungeon*.vue`)

### A) Audit

| Item | Status | Evidence | Gap to close |
|---|---|---|---|
| Title screen | Partial | Launcher prologue (`components/pages/memory-dungeon-launcher.vue:180-205`): "Continue Briar Marches" or "Begin the tale", Classic Match, and a difficulty select. | Settings, Scrapbook and Achievements entries. |
| Settings | Partial | Overworld dialog (`memory-dungeon-overworld.vue:161-260`): card back, gallery deck, 3 checkpoints. A new Briar Camp run asks for confirmation (`:1188`). | Volume, text size, reading speed, reduced motion, high contrast, and a full reset. |
| Save / load | Met (local) | About 11 versioned localStorage keys (`stores/memoryWorldStore.ts:213-223`). 3 manual checkpoints (`utils/memoryDungeon/saveSlots.ts`, version 1). Medals, realm unlocks and the Chronicle persist apart from any run. Continue works after reload. | No account-backed save. |
| 12+ achievements | Missing (live) | Only the site-level `memory-master` (id 970; `stores/memoryStore.ts:701`, `memory-dungeon.vue:832`). There are 96 **local-only** medals: 8 Briar, 16 Dark, 12 House, 16 Vesper, 16 Night, 16 Cinder (`utils/memoryDungeon/achievements.ts`) and 12 Earth (`earthAchievements.ts`). They show as "Medals X/N" in `quest-log.vue:34-42`. | Turn a curated subset into live records. |
| Scrapbook | Partial | Threads and Medals (`quest-log.vue`), Earth Chronicle photos (`earth-chronicle.vue`), realm gallery with 32 World One cards (`realmGallery.ts`). | One unified scrapbook: endings, characters met, run pages, "X of N". |
| Endings | Partial | 12 House epilogues: 3 resolutions × 4 lenses (`houseEpilogues.ts:206`), each with its own `artPath`. Plates are rendered (all 23 subjects in `conductor/projects/memory-dungeon/art/ART-ROUND-2.yaml` are DONE, e.g. art_image_id 257312). But `/images/memory-dungeon/house/epilogues/*.webp` returns 404 live: the art was never exported. Realities e01–e08 add more outcomes. | Export the 12 plates (`scripts/export_round_art.py`). |
| Characters | Missing | Fixed protagonist Rowan (`launcher.vue:74`). Only deck and card-back cosmetics. | Silas decides (section B). |
| Replay hooks | Met | Classic difficulty, deck and gallery choice, collectible medals and photos, realm unlocks, 8 realities, branching scene choices. | None. |

### B) Character customization

The story is about Rowan's life being swapped with Morrow's, so a fully designed character fights the premise. I'd suggest either:
- **light customization:** name, pronouns, and a portrait of "your Earth self", plus a prologue "what you were good at" choice that biases one combat or memory stat; or
- **an exception** like the Zuzu Gamebook.

Silas decides.

### C) Proposed achievements (16, prefix `memory-dungeon-`; keep `memory-master` as it is)

Most can come from one hook. In `syncAchievements` (`memoryWorldStore.ts:400`), diff the new medal ids and map them to codes. Reality completions hook at the `completeMemoryExperience` calls in play paths only (`:641`, `653`, `769`, `787`, `860`, `1498`), not in `loadCheckpoint :966` or `hydrate :1142`.

1. `briar-cleared` "Out of the Briar": e01 (`grantBriarCompletion :858`).
2. `other-marches` "The Other Marches": e02 (`darkChooseScene :1498`).
3. `morrow-earth` "Morrow's Earth": e03 (`finishMorrowEarthReality :641`).
4. `earth-decided` "An Ordinary Life": e04 (`:653`).
5. `scylla` "Scylla's Tide": e05 (`finishScyllaReality :769`).
6. `twin-tide` "Twin Tide": e06 (`:787`).
7. `hoshimori` "Hoshimori Warm": e07 completed.
8. `hoshimori-night` "Night Council": first Night medal.
9. `hearth-release` "The Jars Go Home": House epilogue `release-*`.
10. `hearth-renew` "Hearth Renewed": epilogue `renew-*`.
11. `hearth-break` "Hearth Broken": epilogue `break-*`.
12. `fourth-column` "A Fourth Way Out": medal `the-fourth-column`.
13. `briar-medals` "Every Thread Tied": all 8 Briar medals.
14. `chronicle` "Recovered Photographs": 12 Earth photos.
15. `minefield` "Safe Steps": clear a minefield run (`minefieldMove`, board finished).
16. `guardian` "Guardian Down": `finishHouseCombat` with a win.

### D) Three smallest high-value PRs

1. **Achievements.** Edit `catalog/games.ts` and `gameAchievements.ts` (add a `memory-dungeon` game, `/play/memory`, and a section), add the medal→code map in `utils/memoryDungeon/achievements.ts`, award inside `syncAchievements` and at the play-path completions, and show the strip in `quest-log.vue`.
2. **Ship the 12 epilogue plates** (an export-only change) and add an Endings tab, "12 of N", to `quest-log.vue`.
3. **Settings and title.** Add an a11y and audio block to the overworld settings dialog, persisted under a new key such as `memoryDungeonSettingsV1`. Add Settings / Scrapbook / Achievements buttons to `memory-dungeon-launcher.vue`.

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
