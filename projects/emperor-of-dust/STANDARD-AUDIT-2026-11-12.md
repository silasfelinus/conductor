# Emperor of Dust — main-game standard audit (2026-11-12, kind_robots 7ad1136)

## A) Audit
| Item | Status | Evidence | Gap |
|---|---|---|---|
| Title screen | Partial | `components/EmperorFortressSplash.vue:43-66` has "Enter fortress" (silently continues the autosave) and "Chronicle of Ash". Shown every visit (`pages/play/emperor-of-dust.vue:354`) | No separate New Game / Continue, and no Settings, Scrapbook or Achievements on the title |
| Settings | Partial | Gear in play (`pages/play/emperor-of-dust.vue:118-127`) opens `EmperorFortressPreferences.vue`: reading size, font, width, high contrast, reduced motion, dialogue speed, reset preferences. Persisted under `kr-emperor-of-dust-reading-v1` and `-text-speed` (`stores/emperorFortressStore.ts:60-85`) | Not reachable from the title. No **reset progress**. No volume (no audio) |
| Save/load | Met (no account) | Autosave `kr-emperor-of-dust-fortress-auto-v3`. `SaveBook` is versioned (v3) and keeps a snapshot at every dawn so any day can be rewound (`utils/emperorOfDust/fortress/saves.ts`). 3 slots (`EmperorFortressChronicle.vue:78-126`). Unreadable saves are left untouched rather than overwritten. Relic vault and codex persist across runs | No account-backed save |
| Achievements | Partial | 3, Day 1 only (`stores/emperorFortressStore.ts:288-313`) | t-065 |
| Scrapbook | Partial | Codex only | t-064 |
| Endings + plates | Partial | 8 text-only endings (`endings.ts:8-17`, `endingOf` at `:81`) | t-064 |
| Characters | Missing | The Emperor is fixed. Followers have pronouns and portraits | see B |
| Replay hooks | Met | Seeded runs, relics carry over, persistent codex, rewind, 8 branching endings | t-066 deepens this |

## B) Characters
The player is the court, not an avatar. A light creator would fit a management game: ruler name, portrait from 4–6 painted options, and one starting "reign temperament" (Merciful / Iron / Cunning) that nudges starting faction affinity and some audience lines. Not doing it is also defensible, because the identity lives in follower choices. Silas decides.

## C) Proposed achievements (keep the existing 3)
| triggerCode | Label | Award at (`stores/emperorFortressStore.ts` unless noted) |
|---|---|---|
| emperor-of-dust-orders-carried-out / -day-well-ruled / -merciful-court | existing | `awardAchievements` |
| emperor-of-dust-reign-complete | Fifty Dawns | `finish()` when `isOver(run)` (`engine.ts:168`) |
| emperor-of-dust-bell-restored | The Bell Speaks | same point, `endingOf(run).id === 'bell-restored'` |
| emperor-of-dust-long-night | The Long Night | same, `'long-night'` |
| emperor-of-dust-hundred-candles | A Hundred Candles | same, `'hundred-candles'` |
| emperor-of-dust-no-names | No Names on the Wall | same, `run.memorials.length === 0` |
| emperor-of-dust-every-peace | Every Peace | all 8 endings in the persistent endings record (needs t-064) |
| emperor-of-dust-crypt-sealed | The Crypt Holds | `commit`/`finish` diff: flag `horror-sealed` newly present |
| emperor-of-dust-abbess-unmasked | Unmasked | flag `abbess-unmasked` newly present |
| emperor-of-dust-after-the-betrayal | The Tower Still Stands | `finish()` reaching Day 42 with a betrayal record |
| emperor-of-dust-triumph | Beyond Orders | `awardAchievements`, any quest tier `triumph` |
| emperor-of-dust-first-relic | Item of Power | `claimRelic` |
| emperor-of-dust-both-relics | The Vault Is Full | `claimRelic`, `vault.owned.length === 2` |
| emperor-of-dust-codex-complete | Knows Every Heart | `remember()`, `revealed.length === CODEX_SIZE` |
| emperor-of-dust-full-barracks | A Full House | `expandBarracks` at max, or `hire` at roster cap |
| emperor-of-dust-second-chance | The Hourglass Turns | `rewind()` |

## D) Three ~1-day PRs (beyond t-063..t-066)
1. **Title console.** In `components/EmperorFortressSplash.vue` and `pages/play/emperor-of-dust.vue`: Continue (shows "Day N"), New Reign (with confirmation, calls `newRun`), Settings (opens `EmperorFortressPreferences`), Chronicle, and the Achievements strip.
2. **Reset progress.** Add `resetProgress()` in the store (clears autosave, slots, codex, relic vault, intro key) behind a typed confirmation in `EmperorFortressPreferences.vue`. Fold `SPEED_KEY` into the reading-v1 record. Add a test in `utils/scripts/verifyEmperorFortressStore.test.ts`.
3. **Account save.** A shared `GameSave` Prisma model, `/api/game-save/[game]` GET/POST, and syncing autosave + codex + relics from `emperorFortressStore.persist`, keeping local as the fallback.

## E) Reusable
Emperor's save book (`saves.ts`), with versioning, dawn snapshots, slots and the never-overwrite-unreadable rule, is the best save design of the four.

## Shared notes
- Live `/api/achievements` on 2026-11-12: emperor 3, shifting-desks 3, zuzu-gamebook 3, slime-city 0.
- None of the four audited games has audio, so the "music/sound volume" setting has nothing to control until sound exists.
- None of them mounts `components/achievements/game-achievement-strip.vue`; only `pages/play/arcade/index.vue` and `components/navigation/workspace-sheet.vue` use it.
- The only account-backed save among the four is Slime City's `SlimeCityAccount`.
- Shared components:
  - **Settings + scrapbook kit:** `stores/playbookKitStore.ts` and `utils/playbookKit/settings.ts` (textSize, font, contrast, motion, textSpeed, sound, trailer, plus resetSettings, one versioned localStorage record per game), and `components/playbook-kit/playbook-kit-{settings,scrapbook,endings,shell}.vue`. Used today by monstrique, game-of-captains and every-villain-tactics. Emperor's own `FortressPreferences` duplicates it.
  - **Title console:** `components/monstrexx/monstrexx-front.vue` (New / Continue / settings / scrapbook panels; the standard's reference). It could be generalized into a `game-title-console` that takes a game slug and its art.
  - **Save:** Emperor's `saves.ts` for slots and rewind; Slime City's `SlimeCityAccount` + story GET/POST to generalize into a `GameSave` model for account-backed saves.
  - **Achievements:** `game-achievement-strip.vue` plus `achievementsForGame()`. Each game needs an `ACHIEVEMENT_SECTIONS` entry.
