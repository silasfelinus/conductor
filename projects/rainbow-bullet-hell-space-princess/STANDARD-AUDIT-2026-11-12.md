# Rainbow Bullet Hell Space Princess — main-game standard audit (2026-11-12, kind_robots 7ad1136)

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

## 3. Rainbow Bullet Hell Space Princess (`/play/rainbow-bullet-hell-space-princess`)

**A) Audit**

| Item | Status | Evidence | Gap to close |
|---|---|---|---|
| Title screen | Partial | Page tabs Fly / Pilots / Seas (`pages/play/rainbow-bullet-hell-space-princess.vue:158-161`). In-canvas attract, CONTINUE/NEW resume menu and pilot+difficulty select (`utils/arcade/games/rainbowPrincessPreview.ts:1184-1196,3411-3434`). | No Settings, Scrapbook or Achievements entries |
| Settings | Partial | Cabinet volume slider, difficulty Cadet/Pilot/Ace, motion calm (`arcade-cabinet.vue:344-392`); Fever Dream look toggle. Arcade prefs persist. | No comms text size/speed, no high contrast (matters for bullet readability), no reset progress |
| Save/load | Partial | `RainbowSave` v1 with validation (`utils/arcade/games/rainbowLoadouts.ts`) kept in `kr-arcade-saves`. Written only at Act starts, `frame===0 && act>=2` (`rainbowPrincessPreview.ts:2185-2201`). Mastery persists permanently via `recordMastery`. | A reload mid-Act loses up to a whole Act. Save at section checkpoints too (`rainbowCheckpoints.ts` already defines them). |
| 12+ achievements | Missing | 0 live. 7 mastery goals exist (`rainbowLoadouts.ts`, `RAINBOW_MASTERY`) but aren't awardable (preview game) | See C |
| Scrapbook | Missing | Seas tab shows all 8 stage cards always unlocked; Pilots is a roster browser | Progress gallery |
| Endings + plates | Partial | 9 named endings (3 roads × restore/evacuate/sever, `utils/arcade/games/rainbowEclipseFinale.ts:116-170`). 3 plates painted (C14/C15/C16, art_image_id 246338-40, conductor `art/ART-ROUND-6-CINEMA.yaml`) but **not shipped**: nothing under `public/rainbow-princess-art`. | Ship the 3 plates (one per choice); tint or caption them per road |
| Customizable characters | Partial | 4 pilots with distinct ship/focus/special/evade (`rainbowLoadouts.ts`, `utils/arcade/games/rainbowPilots.ts`); 1–4 local seats | No call sign or paint |
| 3+ replay hooks | Met | Difficulty modes; branch routes (trench/wreck/reef/allegiance, `rainbowPrincessPreview.ts:1336-1844`); per-Act medals; mastery ladder; 9 endings; co-op | — |

**B) Characters.** Pilot select is the right genre fit; keep it. Add a Hangar step:
- call sign entry, shown in comms and credits
- 3 paint schemes per ship, unlocked by medals (also a replay hook)

**C) Achievements** (`rainbow-bullet-hell-space-princess-*`)

Use `rule:{kind:'mastery',id}` and award from `earn()` (`rainbowPrincessPreview.ts:2219`). Also push each id to a `feats` queue exposed as `drainFeats()`, so awards are immediate and players who already hold a mastery get it backfilled.

| triggerCode | Label | Message | Award event |
|---|---|---|---|
| `-first-light` | First Light | Pinkwake cleared. | existing `earn('first-light')` |
| `-gold-wing` | Gold Wing | An Act without a hit. | existing |
| `-guardian-breaker` | Guardian Breaker | All eight guardians down. | existing |
| `-no-one-left` | No One Left Behind | Every rescue, one flight. | existing |
| `-the-end` | The End | Through the Eclipse Crown. | existing (`:3840`) |
| `-every-ending` | Every Ending | Restored, evacuated, severed. | existing (parts) |
| `-ace-of-eclipse` | Ace of the Eclipse | THE END on Ace. | existing (`:3842`) |
| `-rebel-road` | Rebel Road | You swore against the Motherland. | `allegiance='rebel'` (`:1336`) |
| `-loyal-road` | Loyal Road | Orders kept. | `allegiance='loyal'` |
| `-vault-run` | Into the Vault | Took the salvage route. | `trenchRoute='vault'` (`:1844`) |
| `-kitty-power` | Princess Kitty Power | First super. | super fires (`ship.charge = 0`, `:2794`) |
| `-full-squadron` | Full Squadron | Cleared an Act with four pilots. | Act clear with `activePlayers===4` |
| `-all-pilots` | Whole Litter | Act I cleared with every pilot. | mastery parts `act1-<pilot>` |
| `-no-continue` | Unbroken Flight | THE END without a continue. | all medals silver+ at `awardMedal(9)` |
| `-all-gold` | Pure Gold | Gold on all nine Acts. | `awardMedal(9)` with every medal gold |

**D) PRs**
1. **Achievements.** Add an `OTHER_GAMES` entry; add defs; extend `RAINBOW_MASTERY` and `earn()`; add `drainFeats()` to the instance (`rainbowPrincessPreview.ts:4871` return block); add a strip on the play page; seed with a batch.
2. **Endings and scrapbook.** Export the 3 ending plates to `public/rainbow-princess-art/endings/` and draw them under the ending text (`rainbowEclipseFinale.ts`). Add a "Logbook" tab built from `arcadeStore.masteryFor`: endings by road, Act medals, guardians and rescues as locked silhouettes with "X of N".
3. **Save and settings.** Call `writeSave()` at section checkpoints; add a high-contrast pellet option, a comms text speed option and a two-step "Erase flight log" (clears `recordSave` + mastery for the slug) to the cabinet controls.

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
