# Ecotone: Weird Humboldt — main-game standard audit (2026-11-12, kind_robots 7ad1136)

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

## Ecotone: Weird Humboldt (`/play/ecotone`, slug weird-humboldt)

### A) Audit

| Item | Status | Evidence | Gap to close |
|---|---|---|---|
| Title screen | Partial | Title at `components/ecotone-board.vue:107-338` (key art, character setup, Start). It is skipped whenever a run exists (`:339`). The tab bar (`:2163-2165`) has Endings, Cases and Settings. | Show the title with Continue / Settings / Scrapbook / Achievements even when a run exists. |
| Settings | Partial | "Settings & Save Games" tab (`:984+`): text size in 4 steps, text reveal speed, art style (4 lanes), portrait. Stored at `kr.ecotone.display.v1` (`utils/ecotone/displaySettings.ts:8`). Reduced motion follows the OS setting only. | Reduced-motion and high-contrast toggles, and a reset-progress option with confirmation. The game has no audio, so volume doesn't apply until it gets sound. |
| Save / load | Met (local) | Autosave `kr.ecotone.run.v1`, undo `kr.ecotone.undo.v1`, 3 manual slots `kr.ecotone.manual-saves.v1`, JSON export/import (`stores/ecotoneStore.ts:48-52`, `261-330`). `RunState.version` with legacy restore. Endings and cases persist separately. | No account-backed save. |
| 12+ achievements | Missing | 0 live. Not listed in `OTHER_GAMES`. | All of it. |
| Scrapbook | Partial | Endings gallery with locked card backs and "Endings X/84" (`:1723-1811`, `slotStyle` at `:3130`). Case Files for 12 mysteries (`:1545+`). Journal for the current run only. | A "guides met" page, and persisted per-run pages with choices and outcome. |
| Endings | Partial | 84 ending IDs: 6 leads (mara, kit, juniper, cedar, alone, ecotopia) × 7 lenses × hope/dark (`utils/ecotone/content.ts:1084-1104`). Plus "The Long Table" chosen-family ending (`chosenFamily.ts`) and mystery real endings. Painted plates: 69 of 84 in each of 4 styles (`artManifest.ts`). | 15 plates missing: all 14 Mara endings and `ecotopia-mdma-dark`. |
| Characters | Met | Name up to 32 characters; 12 avatars plus a private upload; 6 personalities (`playerIdentity.ts`); 7 archetypes, each with a skill spread and origin perk (`content.ts:118-170`). | None. |
| Replay hooks | Met | 3 festival events; 4 guides plus alone or the Wild Way; lenses; 12 seeded mysteries, preferring unopened ones (`store:233`); archetypes; the endings collection. | None. |

**Discrepancy to reconcile.** `CONTROL.md` says the cocaine, meth and MDMA detours produce none of the "32 official" endings and are tracked as "Endings X/32". The code's `ENDING_LENSES` includes all three, which makes 84 endings and shows "X/84".

### B) Character customization

Already there and well suited to the genre. No change proposed.

### C) Proposed achievements (16, prefix `weird-humboldt-`)

Hook point: `useEcotoneStore().update(next)` at `stores/ecotoneStore.ts:211`, comparing the previous and next state. Do **not** award from `loadSlot`, `importSave` or initialize-restore, or imported saves could farm awards. I deliberately left out any achievement for choosing a drug lens.

1. `first-weekend` "Sunday Night": `phase === 'end'` for the first time.
2. `hopeful-county` "Fog Lifts": an ending with fate `hope`.
3. `dark-county` "Fog Stays": an ending with fate `dark`.
4. `mara-hope` "Mara's Line": ending `mara.*.hope`.
5. `kit-hope` "Kit's Cascade": ending `kit.*.hope`.
6. `juniper-hope` "Juniper's Grove": ending `juniper.*.hope`.
7. `cedar-hope` "Cedar's Road": ending `cedar.*.hope`.
8. `wild-way` "The Wild Way": ending `ecotopia.*.hope`.
9. `long-table` "The Long Table": `chosenFamilyEnding(...)` is non-null at the end.
10. `case-closed` "Case Closed": the first case record with a real ending.
11. `all-cases` "Twelve Strange Files": `casesOpened === 12`.
12. `clear-eyed` "Clear-Eyed": a hope ending with lens `sober`.
13. `long-shot` "Long Shot": a check passed when `chanceToSucceed` was below 0.3.
14. `free-hour` "An Hour Well Spent": first companion-time hour taken (`companionTime.ts`).
15. `full-car` "Full Car": `travelParty(run).length >= 3`.
16. `half-gallery` "Half the County": `endings.length >= 42`.

### D) Three smallest high-value PRs

1. **Achievements.** Edit `catalog/games.ts` and `gameAchievements.ts` (add a game entry and section), add the award diff in `ecotoneStore.update`, and render the strip on the Endings tab.
2. **Missing plates and title.** Queue 15 ending plates × 4 styles through `conductor/projects/weird-humboldt/art/ART-STANDARD.yaml` (auto_submit), then re-export `artManifest.ts`. On the title, add Continue / Settings / Endings / Achievements buttons when a run exists (`ecotone-board.vue:107`, `339`).
3. **Settings and scrapbook.** Add `motion` and `contrast` to `displaySettings.ts` with a settings-tab UI. Add "Reset endings & cases" with an armed confirmation. Add a guides-met page and `kr.ecotone.runs.v1` run pages built from `run.log` when the run ends.

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
