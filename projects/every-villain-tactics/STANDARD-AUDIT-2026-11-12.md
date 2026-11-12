# Every Villain Tactics — main-game standard audit (2026-11-12, kind_robots 7ad1136)

I audited four games against the main-game standard: Every Villain Tactics, MONSTRIQUE, Rainbow Bullet Hell Space Princess and Save the Plumber. Nothing was edited. Code is kind_robots origin/main 7ad1136 (all paths below are relative to /home/user/kind_robots). Live check of `/api/achievements` on 2026-11-12: 145 records, and **0** start with any of the four slugs.

## Problems that affect all four games (fix these first)

1. **A test blocks having 12+ achievements.** `utils/scripts/verifyGameAchievements.test.ts:20-31` asserts every game has exactly 3 achievements, with tiers [1,2,3].
   - Fix: add a `mainGame: true` flag to `AchievementGame` and assert ≥12 (tiers 1–3) for those games.
   - The header comment in `utils/achievements/gameAchievements.ts:1-8` ("three per game") needs the same change.
2. **None of the four games is registered for achievements.**
   - `ACHIEVEMENT_GAMES` only holds `ARCADE_GAMES` plus `OTHER_GAMES` (`gameAchievements.ts:80-149`).
   - Rainbow and Plumber are `PREVIEW_GAMES` (`utils/arcade/games.ts:818-880`), not `ARCADE_GAMES`, so `build()` would throw "Unknown achievement game".
   - Fix: add all four to `OTHER_GAMES` with `arcade:false`. Codes then come out as `<slug>-<key>`, which matches the standard's prefix rule.
4. **How records get created and shown.**
   - Records: `scripts/seed_achievements.ts` (upsert by triggerCode) or POST `/api/achievements/batch`. Badge art: `scripts/generate_achievement_art.ts`.
   - Strip: `GameAchievementStrip` appears automatically in `components/navigation/workspace-sheet.vue:176` when `achievementGameForPath` exactly matches the game's `route`. Use `adminOnly:true` for `/admin/*` routes.
5. **No game has an account-backed save.** All four save to localStorage only.
6. **No title screen has an Achievements entry, including the MONSTRIQUE reference console.**

---

## 1. Every Villain Tactics (`/admin/every-villain-tactics`, admin-only)

**A) Audit**

| Item | Status | Evidence | Gap to close |
|---|---|---|---|
| Title screen | Partial | `components/every-villain-tactics/every-villain-front-menu.vue:20-92`: New Story / Continue / One-Shot / Settings / Scrapbook / Tactics console | Add Achievements |
| Settings | Partial | Own panel at `:233-385`: animation speed incl. Off, confirm end turn, threat preview, restore defaults, two-step "Erase saves and scrapbook" (`:371`). Stored in `kr-every-villain-tactics:settings` (`utils/everyVillainTactics/frontMenu.ts:38`). Reachable in play via the console's title button (`pages/admin/every-villain-tactics.vue:24`). The `PlaybookKitShell` pane (`:8`) adds text size / contrast / motion / text speed / sound. | Two separate settings sheets. No volume slider (game has no audio). Merge into one. |
| Save/load | Met (local only) | 4 slots: auto + 3 (`utils/everyVillainTactics/saves.ts:42`), version 2 with v1 migration (`:40,220`). Autosaves every round and phase end (`stores/everyVillainTacticsStore.ts:1006,1028,1035`). `continueLatest` loads the newest valid slot (`:460`). | Account-backed save |
| 12+ achievements | Missing | 0 live, 0 award calls | See C |
| Scrapbook | Partial | 14 moments with "?" / "Not yet witnessed" and "X of N witnessed". Run pages with points and medals (`front-menu.vue:390-450`, `frontMenu.ts:84-205`). | No characters-met page and no endings section. The kit spec's moments/endings panes are never unlocked: the store has no `kit.unlock`. |
| Multiple endings + plates | Partial | Victory/defeat closings for 4 perspectives = 8 texts (`utils/everyVillainTactics/firstBellStory.ts:128,247,363,482`). Plates are reused Prom of Doom art (`endings/the-rescue-that-counted`, `the-broken-grid`). Painted "First Bell Cleared/Lost" exist (art_image_id 265020/265021 in conductor `projects/every-villain-tactics/art/TACTICAL-ARENAS-ROUND-1.yaml`) but are **not wired**. Kit spec lists 3 endings (`utils/playbookKit/games/everyVillainTactics.ts:91-135`) that gameplay never reaches. | Make the kit endings the real endings and give each a plate |
| Customizable characters | Partial | Viewpoint, squad lead from 48 identities, rival foil (`front-menu.vue:116-205`) | No name, look or loadout of your own |
| 3+ replay hooks | Met | 4 viewpoints × 48 leads × foils; 8 one-shots (`frontMenu.ts:326-370`); deterministic points and 6 medals (`utils/everyVillainTactics/scores.ts:108-115`); story decisions | — |

**B) Characters.** A 48-hero roster fits the genre. Recommend a squad loadout step after picking the lead:
- 2 support slots from the lead's identity arc
- a codename-colour palette swap
- one perk choice (range / mobility / defence, which already exist as tactical roles in t-017)

Store it in the save and use the alias in closing lines.

**C) Achievements** (`every-villain-tactics-*`)

All award from one diff in `recordMoments()` (`stores/everyVillainTacticsStore.ts:223-239`), comparing new records and results against the old ones:

| triggerCode | Label | Message | Award event |
|---|---|---|---|
| `-first-bell-cleared` | Doors Open | The auditorium finally gave. | record `story:victory` |
| `-first-bell-lost` | Patrol Held | Not the way you planned. | record `story:defeat` |
| `-mercy` | Spared | A rival walked away. | completed save, `decisions` has `spare` |
| `-rescue-call` | Second Bell | You chose people over evidence. | `decisions` has `rescue` |
| `-every-side` | Everyone's Villain | You won First Bell from all four sides. | results, First Bell `victory` × 4 perspectives |
| `-rival-foil` | Chosen Nemesis | You beat a hand-picked foil. | victory result with `foil != null` |
| `-untouched` | Untouched | Not one point of damage. | medal `untouched` |
| `-no-knockouts` | Nobody Down | The whole squad walked out. | medal `no-knockouts` |
| `-every-civilian` | Headcount | Every civilian safe. | medal `every-civilian` |
| `-quick-clear` | Bell to Bell | Objective done early. | medal `quick-clear` |
| `-evidence` | Case File | Evidence recovered. | medal `evidence-recovered` |
| `-picnic-rescued` | Behind the Bandstand | Every picnicker got clear. | `picnic:all-rescued` |
| `-overtime` | Time and a Half | You outlasted overtime. | `picnic:overtime` |
| `-picnic-won` | Leftovers for Everyone | The plaza held. | `picnic:victory` |
| `-one-shot-sweep` | Stage Veteran | You won all 8 one-shots. | oneshot victory results cover `ONE_SHOT_MENU` |
| `-stage-architect` | Stage Studio | First custom stage saved. | `saveDraft()` (`store:267`) |
| `-scrapbook-full` | Yearbook | Every moment witnessed. | all 14 records present |

**D) PRs**
1. **Achievements.** Relax the test; add an `OTHER_GAMES` entry (`adminOnly`); add defs in `utils/achievements/catalog/games.ts`; add `utils/everyVillainTactics/achievements.ts` (pure `achievementsFor(oldBook, newBook, saves)`) called from `recordMoments`; seed with a batch; add a test.
2. **Endings.** Map victory/defeat × perspective onto kit endings (`doors-open`/`broken-orders`/`someone-else`) and call `kit.unlock('endings')` in the store. Wire the 265020/265021 plates. Queue the third plate in a new auto_submit ledger.
3. **Title, settings and scrapbook.** Add an Achievements item and a Cast page (characters met = leads/foils fought) to `every-villain-front-menu.vue`. Fold the kit text-size/contrast sheet into the front Settings.

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
