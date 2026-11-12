# Save the Plumber — main-game standard audit (2026-11-12, kind_robots 7ad1136)

I audited four games against the main-game standard: Every Villain Tactics, MONSTRIQUE, Rainbow Bullet Hell Space Princess and Save the Plumber. Nothing was edited. Code is kind_robots origin/main 7ad1136 (all paths below are relative to /home/user/kind_robots). Live check of `/api/achievements` on 2026-11-12: 145 records, and **0** start with any of the four slugs.

## Problems that affect all four games (fix these first)

1. **A test blocks having 12+ achievements.** `utils/scripts/verifyGameAchievements.test.ts:20-31` asserts every game has exactly 3 achievements, with tiers [1,2,3].
   - Fix: add a `mainGame: true` flag to `AchievementGame` and assert ≥12 (tiers 1–3) for those games.
   - The header comment in `utils/achievements/gameAchievements.ts:1-8` ("three per game") needs the same change.
2. **None of the four games is registered for achievements.**
   - `ACHIEVEMENT_GAMES` only holds `ARCADE_GAMES` plus `OTHER_GAMES` (`gameAchievements.ts:80-149`).
   - Rainbow and Plumber are `PREVIEW_GAMES` (`utils/arcade/games.ts:818-880`), not `ARCADE_GAMES`, so `build()` would throw "Unknown achievement game".
   - Fix: add all four to `OTHER_GAMES` with `arcade:false`. Codes then come out as `<slug>-<key>`, which matches the standard's prefix rule.
3. **Rainbow and Plumber already have an award path in the cabinet.**
   - `components/arcade/arcade-cabinet.vue:1381-1382`: `game.drainFeats()` → `arcadeStore.awardFeats(slug, feats)` awards `${slug}-${feat}` (`stores/arcadeStore.ts:276-285`).
   - Mastery ids already go through `awardRunAchievements` → `arcadeAchievementsEarned`, which accepts `rule:{kind:'mastery',id}` (`gameAchievements.ts:223-235`).
   - The engines only need to emit feat or mastery ids.
4. **How records get created and shown.**
   - Records: `scripts/seed_achievements.ts` (upsert by triggerCode) or POST `/api/achievements/batch`. Badge art: `scripts/generate_achievement_art.ts`.
   - Strip: `GameAchievementStrip` appears automatically in `components/navigation/workspace-sheet.vue:176` when `achievementGameForPath` exactly matches the game's `route`. Use `adminOnly:true` for `/admin/*` routes.
5. **No game has an account-backed save.** All four save to localStorage only.
6. **No title screen has an Achievements entry, including the MONSTRIQUE reference console.**

---

## 4. Save the Plumber (`/play/save-the-plumber`)

**A) Audit**

| Item | Status | Evidence | Gap to close |
|---|---|---|---|
| Title screen | Partial | Start/Continue (one button), Level Maker, Story, World Select, Heroines, Controls (`pages/play/save-the-plumber.vue:55-118`). In-cabinet 3-slot file select with armed erase (`utils/arcade/games/savePlumberPreview.ts:438-443`). | Separate New Game and Continue; add Settings, Scrapbook and Achievements |
| Settings | Missing | Only the cabinet volume slider; title video follows system reduced-motion | Settings screen: volume, reduced motion, contrast, text size, reset |
| Save/load | Met (local only) | File v3 with 3 slots migrating v1/v2 (`utils/arcade/games/savePlumberSave.ts`). `remember()` on map entry, clear, gear and death (`savePlumberPreview.ts:623,787,915,936,2122`). Endless best kept separately. | A reload mid-stage restarts the stage (acceptable). Account-backed save. |
| 12+ achievements | Missing | 0; no `mastered` / `drainFeats` | See C |
| Scrapbook | Missing | World Select is static info with no progress (`save-the-plumber.vue:176-225`) | Progress album |
| Endings + plates | Missing | One finale, "THE RIVERS RUN HOME!", plate `cutscene('finale-reversal')` (`savePlumberPreview.ts:4333-4370`) | 2+ more endings with plates |
| Customizable characters | Partial | 8 painted heroines, each with a unique special (`utils/arcade/games/savePlumberRoster.ts`); seed-based name/look (`savePlumberHeroine.ts`); finale uses her name | No name entry; story barely adapts |
| 3+ replay hooks | Met | 32 Golden Gears, secret exits (`savePlumberOverworld.ts:434`), 3 slots, seeded Endless, 8 heroines, Level Maker + reviews | — |

**B) Characters.** The roster of alternate heroines fits a platformer. Add:
- name entry at heroine select
- a one-line per-heroine epilogue and boss taunts that use her special

**C) Achievements** (`save-the-plumber-*`)

Add `drainFeats()` plus a `feats` queue to `PlumberRun` (`savePlumberPreview.ts:403`). Persistent cross-slot ones use mastery ids via a new `get mastered()`.

| triggerCode | Label | Message | Award event |
|---|---|---|---|
| `-first-valve` | First Valve | Stage 1-1 cleared. | `stageClear()` `:3096` |
| `-madame-pressure` | Pressure Released | World 1 boss down. | `nextStage()` with `this.boss`, W1 (`:934`) |
| `-halfway` | Fair's Over | Tick-Tock Duchess beaten. | same, W4 |
| `-teo-freed` | The Rivers Run Home | Teo is free. | `nextStage` boss and `last` |
| `-first-gear` | Golden Gear | First gear found. | `gears.add` `:2119` |
| `-gear-world` | Gearhead | Every gear in a world. | same, world complete |
| `-all-gears` | Clockmaker | 32/32 gears. | `gears.size===CAMPAIGN.length` |
| `-secret-exit` | Off the Map | First secret exit. | `nextStage('secret')` `:923` |
| `-all-secrets` | Cartographer | Every secret exit. | secrets complete |
| `-hundred-tokens` | Brass Hoarder | 100 tokens became a life. | `collectTokens` `:2287` |
| `-full-hearts` | Not a Drip | Stage cleared without a hit. | `stageClear` with no `hurt()` this stage |
| `-deathless-world` | Dry Run | A world with no lives lost. | track `deaths` per world |
| `-endless-500` | Long Haul | 500 m in Endless. | `rememberEndless` `:644` |
| `-full-roster` | Every Heroine | 1-1 cleared with all eight. | mastery parts per roster key |
| `-hundred-percent` | 100% | Complete save. | `completionPercent===100` |
| `-maker` | Level Designer | First Maker level saved. | `stores/savePlumberMakerStore.ts:291` `saveDraft` |

**D) PRs**
1. **Achievements.** Add an `OTHER_GAMES` entry; add defs; add `drainFeats` and `mastered` to `PlumberRun`; add a strip on the page; seed with a batch.
2. **Scrapbook.** Turn World Select into an Album: cleared / gear / secret badges from `useSavePlumberStore().progress` (`stores/savePlumberStore.ts`); 8 bosses as silhouettes until beaten; heroines played; endings; per-slot run page (deaths, time). Add "X of N" counts.
3. **Endings.** Add completion-based endings: base; all gears ("Teo's Clockwork Gift"); all secrets ("Lady Spigot Turns the Tap"). Queue 2 plates in an auto_submit ledger; branch in `renderFinale`. Settings screen as a follow-up.

---

## E) Shared and reusable pieces

- **Playbook Kit**
  - Parts: `components/playbook-kit/*`, `stores/playbookKitStore.ts`, `utils/playbookKit/settings.ts`.
  - What it gives: one settings sheet, a versioned `KitSave` holding progress (moments/reveals/endings) separately from runs, a locked-blur scrapbook with counts, an Endings pane, Cast, and a trailer.
  - Who uses it: MONSTRIQUE, Every Villain Tactics (shell only, never unlocked) and game-of-captains.
  - Gaps: no volume slider, no achievements pane, no run pages.
- **Title console.** `monstrexx-front.vue` and `every-villain-front-menu.vue` are two separate builds of the same idea. Extract a generic `components/game-front/game-title-console.vue` (splash, wordmark, items[] with confirm and disabled states, sheet panels as slots, built-in Achievements item rendering `GameAchievementStrip`). Keep `MonstrexxFront` as a thin wrapper; `utils/scripts/verifyMonstrexxMenu.test.ts` guards it.
- **Arcade cabinet** (`components/arcade/arcade-cabinet.vue` + `stores/arcadeStore.ts`): volume, difficulty, calm motion, versioned per-slug saves, permanent mastery, and feat/mastery → achievement awarding. This is the shared path for both action games.
- **`GameAchievementStrip`** (`components/achievements/game-achievement-strip.vue`): works for any registered game once the 3-only test is relaxed.
- **Save-slot patterns:** EVT 4-slot (`utils/everyVillainTactics/saves.ts`) and Plumber 3-slot file (`savePlumberSave.ts`). Both are good templates; neither is account-backed.
