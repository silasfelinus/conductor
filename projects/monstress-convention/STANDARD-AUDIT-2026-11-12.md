# MONSTRIQUE — main-game standard audit (2026-11-12, kind_robots 7ad1136)

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

## 2. MONSTRIQUE (`monstress-convention`; `/play/monstrique` public, `/admin/monstrique`; `/admin/monstrexx` redirects there)

**How the reference title console is built (PR #4848):** `components/monstrexx/monstrexx-front.vue`, 809 lines (template 1-290, script 291-395, scoped CSS 396-809).
- **Props and events:** props `panel` and `publicEdition`; emits `new`, `continue`, `panel`. The parent pages (`pages/play/monstrique.vue`, `pages/admin/monstrique.vue`) own the view switch home → `PlaybookKitShell` + scene.
- **Backdrop:** painted splash, wide and tall variants (`/monstrique/front/splash-*.webp`, or a server mature splash), with vignette and rain overlays.
- **Brand block:** wordmark, eyebrow, case number.
- **Menu buttons (`.mx-choice`):**
  - New Game has a two-press "START OVER?" confirm when a save exists (`:361`).
  - Continue is disabled with no save and shows the saved room name via `HOTEL_ROOMS` (`:76`).
  - Settings (`:95`) and Scrapbook (`:113`) open a right-hand `role=dialog` sheet. Esc or the close button returns; focus moves to close.
- **Settings sheet:** renders generic `KIT_SETTING_OPTIONS` with ◀/▶ steppers into `usePlaybookKitStore` (romance hidden for the general edition).
- **Scrapbook sheet:** tabs People (`PlaybookKitCast`), Memories (`PlaybookKitScrapbook`, blurred/greyscale locked tiles, "X of N") and Albums (`MonstriqueAlbumArchive`).
- **Reusability: low as-is.** It imports both MONSTRIQUE stores, `HOTEL_ROOMS` and `MONSTRESS_CONVENTION`, and hard-codes copy, splash paths and the Albums tab. The menu, sheet, settings stepper and kit tabs are generic. Extracting them is the shared-component PR in E.

**A) Audit**

| Item | Status | Evidence | Gap to close |
|---|---|---|---|
| Title screen | Partial | Above | No Achievements item |
| Settings | Partial | Text size, font, contrast, motion, text speed, sound on/off, trailer, romance (`utils/playbookKit/settings.ts:5-14`). In play via the shell Settings pane, which has two-press "Forget progress" (`components/playbook-kit/playbook-kit-settings.vue:54-61`). Stored in localStorage `kr-playbook-kit-<id>-v1`. | No volume slider. The title copy claims "saved for your account" but storage is per device. "Forget progress" doesn't clear the case save. The front sheet has only "Restore default settings" (`:216`). |
| Save/load | Met (local only) | Saves on every `commit()` (`stores/monstressConventionStore.ts:104-124`, `stores/monstriquePublicStore.ts:172`). Keys `kr-monstress-case-v2-<uid>` / `kr-monstrique-<aud>-v1-<uid>`. CaseState v3 restores v2 (`utils/monstressConvention/prologue.ts:1566`). Unreadable saves are left untouched. | Account-backed save |
| 12+ achievements | Missing | 0 | See C |
| Scrapbook | Partial | People / Memories (5) / Albums (7) | Endings appear only in the in-game shell pane, not on the title. No per-run pages. Memories are 5 entries. |
| Endings + plates | Partial/Missing | 2 endings, `lead-earned` and `reckless` (`prologue.ts:27,1526,1547`). Spec has art briefs with no `src` (`utils/playbookKit/games/monstressConvention.ts:99-126`). No ending ledger in conductor `projects/monstress-convention/art/` (only splash, pinups, studio card). | Plates for both; a third ending |
| Customizable characters | Missing | Fixed Iris/Norb duo, switchable (`prologue.ts:682`) | See B |
| 3+ replay hooks | Partial | Sierra score out of 205 (`prologue.ts:490-534`); 2 endings; per-investigator dialogue (`asked` keyed by actor); Good Graces | Only one act. Add collectible/branch hooks. |

**B) Characters.** This is an authored comedy duo, which argues for a Silas exception like Zuzu Gamebook's; ask him. If not granted, add a light "press pass": Iris's coat/camera palette (`utils/monstrique/characterModels.ts` already has `outfit`/`wardrobe` fields) plus a reporter specialty (Snoop / Charmer / Shutterbug) that adds one alternate hotspot line per room.

**C) Achievements** (`monstress-convention-*`)

Award all of these from a shared `achievementsFor(prev, next)` called in both stores' `commit()`. No mature-only items, so the general edition can earn everything.

| triggerCode | Label | Message | Award event |
|---|---|---|---|
| `-dead-client` | Your Client Is Dead | Odette hired you anyway. | flag `odette-hired-us` |
| `-room-205` | Two Women in Room 205 | The case begins. | flag `double-murder-discovered` |
| `-both-witnesses` | Two Ghosts | You heard both stories. | flags `odette-met` + `violet-met` |
| `-rental-fangs` | Forty-Dollar Fangs | Fangs returned. | flag `fangs-returned` |
| `-bill-squared` | Paid in Full | Violet's night is settled. | flag `violet-paid` |
| `-ice-timing` | Time on Ice | You pinned the time of death. | evidence `ice-timing` |
| `-not-the-fan` | Not the Fan | The stalker is cleared. | evidence `fan-exonerated` |
| `-prop-mark` | Beach Hex Prop | You read the knife's maker mark. | evidence `knife-prop-mark` |
| `-billboard` | Billboard Tourist | Snapped the sign. | flag `billboard-shot` |
| `-tag-team` | Tag Team | Norb asked a question too. | `asked` has both `iris:` and `nico:` entries |
| `-combiner` | Junk Drawer Genius | First successful combine. | changed result of `verb:'combine'` |
| `-convention` | Across Town | You reached the convention. | `room === 'convention-center'` |
| `-ending-lead` | Chapter One Filed | You earned the lead. | `ending === 'lead-earned'` |
| `-ending-reckless` | A Headline Too Early | Published too soon. | `ending === 'reckless'` |
| `-full-file` | Every Point | Perfect case score. | at ending, `caseScore === maxScore(audience)` |
| `-both-endings` | Both Sides of the Story | Both endings seen. | `kit.progress.endings` has both |

**D) PRs**
1. **Achievements.** Relax the test; add an `OTHER_GAMES` entry (route `/play/monstrique`); add defs; add `utils/monstressConvention/achievements.ts` called from `stores/monstressConventionStore.ts:104` and `stores/monstriquePublicStore.ts:172`; add a strip and an Achievements menu item in `monstrexx-front.vue`; seed with a batch.
2. **Endings.** Add an `art/ENDINGS-R1.yaml` auto_submit ledger for 2–3 plates and set `art.src` in the spec. Add an Endings tab to the title scrapbook (reuse `PlaybookKitEndings`).
3. **Settings.** Add a volume slider and a two-press "Erase case and scrapbook" (case key + `kit.resetProgress()`) to the front sheet. Correct the "for your account" copy.

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
