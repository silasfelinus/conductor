# The Ruler Is Hooked — main-game standard audit (2026-11-12, kind_robots 7ad1136)

This was read-only. I changed no files, made no commits and called no write APIs. Code is from kind_robots `origin/main` @ 7ad1136. I checked live state with `curl`.

## Shared findings that apply

**Live achievements: 0.** `/api/achievements` returns 145 records and none has a ruler/cthulhu/aquarium/comet/prom/captain/couch prefix.

**A test blocks 12+ achievements in every game.** `utils/scripts/verifyGameAchievements.test.ts:20-32` requires every game in `ACHIEVEMENT_GAMES` to have exactly 3 achievements, one at each tier [1,2,3]. The header comment in `utils/achievements/gameAchievements.ts` says "three per game" too.
- A prerequisite PR has to change the test: arcade games keep exactly 3; main games need 12 or more, using tiers 1–3 repeatedly.
- The same test (`:145-151`) also requires every event code to appear literally as `'<code>'` in a `.ts`/`.vue` file. That's good: it forces the award to be wired.
- Icons must exist in `assets/icons` (`:53`).

**How to register a game's achievements:**
1. Add the game to `OTHER_GAMES` in `utils/achievements/gameAchievements.ts:80`. The `key` must be the conductor slug, because `achievementCode()` builds `<slug>-<key>`.
2. Add a section to `AchievementSectionKey`/`ACHIEVEMENT_SECTIONS`.
3. Add the definitions in `utils/achievements/catalog/` (one file per game is cleaner than growing `games.ts`).
4. Create the live records with `scripts/seed_achievements.ts`, which upserts by triggerCode; queue badge art with `scripts/generate_achievement_art.ts`.
5. `GameAchievementStrip` then shows automatically in the workspace sheet (`components/navigation/workspace-sheet.vue:176`), because `achievementGameForPath` matches the route.

Guests already get pending local awards (`stores/achievementStore.ts:755`).

**What "Playbook" means here.** The Ruler Is Hooked does not use the shared runtime shell (Playbook Kit). It only has a **Playbook Studio/Manager** adapter (`utils/playbook/rulerHooked.ts`), which is authoring and review only.
- Bug: `utils/playbook/rulerHooked.ts:120` points ending art at `ending-<key>.webp`, which returns 404 live. The game uses `endings/<key>.webp`, which returns 200.

**Reusable pieces:** save slots with schema migration in `utils/rulerHooked/save.ts`; save-code export/import in `utils/cometAcademy/consoleScreens.ts:107`; account-backed collection sync with a local fallback in `gameOfCaptainsStore.ts:150-270`.

**This game has no audio**, so the "music and sound volume" requirement can't be met until audio exists.

## 1. The Ruler Is Hooked (`/play/ruler-hooked`, conductor t-067 / t-068)

**A) Audit**

| Item | Status | Evidence | Gap to close |
|---|---|---|---|
| Title screen | Partial | `components/ruler-hooked/ruler-hooked-slots.vue:3-31` has "Begin a new reign" and "Continue a reign" | No Settings, Scrapbook or Achievements on the title |
| Settings | Partial | Only "Fishing settings" (`ruler-hooked-study-settings.vue`: mode, subject, pace, difficulty, direction, topics), reachable from the crown menu (`ruler-hooked-hud.vue:111`) | Text size, reduced motion, high contrast, reset with confirmation, settings from the title. No audio exists |
| Save/load | Met | Multi-slot localStorage, `SAVE_SCHEMA_VERSION=6` with `migrateSave` (`utils/rulerHooked/save.ts:22,62`). Autosaves on every action (`stores/rulerHookedStore.ts:381`). `init()` reopens the last active slot after reload (`:141`) | No account-backed save. Portraits are kept in IndexedDB only |
| Achievements 12+ | Missing | 0 live, not in the registry | See C |
| Scrapbook | Partial | Fishopedia: 18 species, silhouettes, "Collection X / 18" (`ruler-hooked-fishopedia.vue:63,90`); a Chronicle per reign | Everything is per save. Nothing persists across reigns: no endings collection, no reign pages, no characters met |
| Endings with plates | Met | 4 endings (`utils/rulerHooked/content.ts:2139`): druid-utopia, warlock-metropolis, thistlewood-empire, fishers-peace (SECRET). Each plate `/images/ruler-hooked/endings/<key>.webp` returns 200 live; shown at `ruler-hooked-court-screen.vue:37-76` | Fix the Studio art path only |
| Characters | Met | Name, honorific, 12 `RULER_PRESETS`, custom portrait upload, editable after creation (`rulerHookedStore.ts:158,194`) | No stats, which fits a cozy management game |
| Replay hooks (3+) | Met | Seeded runs, multiple slots, 3 arcs and 4 branching endings, quiz difficulty modes, 18-fish collection | Unlocks don't carry into the next reign |

**B) Character customization.** It exists and suits the genre. The story mostly reflects the player through name and honorific; presets are cosmetic. No exception needed.

**C) Proposed achievements (16)**

All award calls go in `stores/rulerHookedStore.ts` unless noted. `:298` is the LANDED branch of `advanceFishing`.

| triggerCode | Label | Message | Award at |
|---|---|---|---|
| ruler-hooked-crowned | Long May You Fish | You swore the oath and took the throne. | `newGame` :158 |
| ruler-hooked-own-face | A Face for the Coins | Your own portrait now graces the realm. | `newGame`/`updateCosmetics` :194 when `customPortraitId` is set |
| ruler-hooked-first-catch | Hooked | The first fish of your reign. | `:298` |
| ruler-hooked-legendary-catch | The One That Didn't Get Away | You landed a legendary fish. | `:298` when `result.catch` rarity is LEGENDARY |
| ruler-hooked-naturalist | Field Naturalist | Half the lake is in your Fishopedia. | `:298` when 9 or more of 18 are in `save.fishopedia` |
| ruler-hooked-fishopedia-complete | Royal Ichthyologist | Every species, recorded. | `:298` at 18/18 |
| ruler-hooked-scholar | Scholar of the Shallows | 25 correct answers while fishing. | `stores/rulerHookedQuizStore.ts:381` `answer()` when a `correct[module]` total reaches 25 |
| ruler-hooked-fluent | Fluent Angler | 100 Mandarin answers landed. | same place, when `correct.mandarin` reaches 100 |
| ruler-hooked-arc-elope | Love Finds a Way | The heir's secret sweetheart story closed. | `choose` :326 on the final step of arc `child-elopes` |
| ruler-hooked-arc-treaty | Ink and Salt | The envoy's treaty is settled. | `choose` :326, arc `envoy-treaty` |
| ruler-hooked-arc-witch | A Bargain Kept | You dealt fairly with the bog witch. | `choose` :326, arc `bog-witch-bargain` |
| ruler-hooked-ending-grove | The Angler's Grove | Your reign ends in a druid utopia. | `acceptEnding` :341, `druid-utopia` |
| ruler-hooked-ending-boomtown | Boomtown by the Lake | Progress, at a price. | `:341`, `warlock-metropolis` |
| ruler-hooked-ending-empire | The Thistlewood Empire | An empire, built between casts. | `:341`, `thistlewood-empire` |
| ruler-hooked-ending-never-ruled | The Ruler Who Never Ruled | The secret ending: you just fished. | `:341`, `fishers-peace` |
| ruler-hooked-one-more-cast | Just One More Cast | You turned down an ending to keep fishing. | `declineEnding` :350 |

**D) Three PRs (about a day each)**
1. **Achievements.** Relax the shared test. Add `utils/achievements/catalog/rulerHooked.ts` and an `OTHER_GAMES` entry. Wire the calls in `rulerHookedStore.ts` and `rulerHookedQuizStore.ts`. Add `GameAchievementStrip` to the crown menu and title (`ruler-hooked-hud.vue`, `ruler-hooked-slots.vue`). Seed the records and verify one award live.
2. **Settings and title.** Add a new `ruler-hooked-settings.vue` with text size, reduced motion, high contrast, and "erase all reigns" behind a confirmation (uses `deleteSlot`). Persist it under `rulerHooked:settings`. Add Settings / Scrapbook / Achievements buttons to `ruler-hooked-slots.vue`.
3. **Royal Archive (cross-reign scrapbook).** Add a `rulerHooked:legacy` record in `utils/rulerHooked/save.ts`, written in `acceptEnding` and the `:298` catch branch. It holds endings earned, fish ever caught, and a summary page per reign (ruler, turns, arc choices, ending). The screen shows the 4 ending plates as silhouettes until earned, a lifetime Fishopedia, and "X of N". This also adds a carry-over unlock as a replay hook.

**E)** `save.ts` slots and migration are the best local-save pattern of the four games.
