# Prom of Doom — main-game standard audit (2026-11-12, kind_robots 7ad1136)

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

**What "Playbook" means here.** Prom of Doom does not use the shared runtime shell (Playbook Kit). It has a **Playbook Studio/Manager** adapter (`utils/playbook/promOfDoom.ts`), which is authoring and review only. The only runtime Playbook piece it uses is `PlaybookRunReview`, a star rating at run end (`pages/play/comet-city-academy.vue:1542`).

**Reusable pieces:** save slots with schema migration in `utils/rulerHooked/save.ts`; save-code export/import in `utils/cometAcademy/consoleScreens.ts:107`; account-backed collection sync with a local fallback in `gameOfCaptainsStore.ts:150-270`.

**This game has no audio**, so the "music and sound volume" requirement can't be met until audio exists.

## 3. Prom of Doom (`comet-city-academy`, `/play/comet-city-academy`, t-034 / t-035)

**A) Audit**

| Item | Status | Evidence | Gap to close |
|---|---|---|---|
| Title screen | Partial | `components/play/cometAcademy/AcademyOpening.vue:26-56` has NEW GAME, YEARBOOK (X/48), TACTICAL MODE, SETTINGS. The run auto-resumes on reload (`pages/play/comet-city-academy.vue:36`) | No Continue or Achievements button. TACTICAL MODE links non-admins to `/admin/every-villain-tactics` |
| Settings | Partial | Text speed, art on/off and card back are persisted (`utils/cometAcademy/consoleScreens.ts:58`). Save-code export/import and a confirm-gated reset of the term are in-game (`AcademyConsoleScreens.vue:591-614`). The title's "reduce opening animation" isn't persisted | Text size, high contrast, persisted reduced motion; reset of the whole Yearbook. No audio |
| Save/load | Partial | Autosave to `comet-city-academy-slice-v1` plus yearbook and dossier keys (`stores/cometAcademyStore.ts:75-78,130`) | `restoreAcademy` rejects any save with `version !== 1` (`utils/cometAcademy/rules.ts:3000`); this needs real migrations. No account save |
| Achievements 12+ | Missing | 0 live | See C |
| Scrapbook | Partial | In-game Scrapbook: earned moments this term, mastermind dossiers, all 12 ending plates locked or found (`AcademyConsoleScreens.vue:336-440`); Yearbook of 48 identities (`AcademyOpening.vue:42`) | Moments reset each term. No saved page per finished term |
| Endings with plates | Partial | 12 endings (`utils/cometAcademy/artSlots.ts:54`). 10 have their own art: 4 finale plates plus 6 under `endings/` (`artManifest.ts:36-41,352-355`). THE TRANSMITTER GOES DARK uses a stand-in; THE SHIELD CHANGES HANDS has none | Queue 2 plates |
| Characters | Met | 6 origins, 8 affinities, 48 signature identities with pronouns and stats, vows, earned evolved forms. Story arcs follow the identity | None |
| Replay hooks (3+) | Met | 12 endings, 48 identities, earned mantles that unlock replay forms (`cometAcademyStore.ts:210`), 7-day vs 30-day mode, seeded runs, campaign options | None |

**B) Character customization.** Exists and is strong. No exception needed.

**C) Proposed achievements (16)**

All in `stores/cometAcademyStore.ts`. Every ending is recorded in one place, `recordIdentity`, where `entry.endings.push` happens (around :118); award the ending achievements there.

| triggerCode | Label | Message | Award at |
|---|---|---|---|
| comet-city-academy-enrolled | First Day of the Last Month | Thirty days to graduation. | `begin` :210 |
| comet-city-academy-sim-honors | Honors in the Simulation | You aced week one. | `recordIdentity`, HONORS IN THE PROM SIMULATION |
| comet-city-academy-thousand-keys | A City with a Thousand Keys | The grid belongs to everyone. | `recordIdentity` |
| comet-city-academy-last-dance | The Last Dance Leaves by Boat | Everyone got out. | `recordIdentity` |
| comet-city-academy-master-shield | Master of the Shield | The city answers to you now. | `recordIdentity` |
| comet-city-academy-transmitter-dark | The Transmitter Goes Dark | You killed the signal at its source. | `recordIdentity` |
| comet-city-academy-collateral | Collateral Damage | Not every prom ends well. | `recordIdentity`, any of Broken Grid / Music After Glass / Price of a Single Switch / Shield Changes Hands |
| comet-city-academy-all-endings | Every Prom, Every Doom | All 12 endings in your Yearbook. | `recordIdentity`, union reaches 12 |
| comet-city-academy-unmasked | J'Accuse | You named the mastermind. | `accuse` :478 when correct / `recordDossier` :95 |
| comet-city-academy-dossiers | Rogues' Gallery | Every mastermind dossier is filed. | `recordDossier` :95 when all are filed |
| comet-city-academy-honors-fight | Honors Grade | A clean, honors-grade win. | `battleResolve` :429, grade `honors` |
| comet-city-academy-parley | Not Today, Villain | You turned a rival into an ally. | `battleParley('ally')` :395 |
| comet-city-academy-prom-date | Corsage Secured | You have a date to the Prom of Doom. | `social` :276 when `relationships.romance` is set |
| comet-city-academy-case-secret | The Hidden Truth | You found a case's secret. | first `missionClues` entry (`choose`/`dispatch` :443-455) |
| comet-city-academy-mantle | Earned the Mantle | Your hero evolved. | `recordIdentity` when a new form is pushed |
| comet-city-academy-many-faces | Many Faces | You graduated as five different heroes. | `recordIdentity`, 5 signatures with endings |

**D) Three PRs**
1. **Achievements.** Add `catalog/cometCityAcademy.ts` and the registry entry. Wire the calls in `cometAcademyStore.ts`. Show the strip on the title (an Achievements button in `AcademyOpening.vue`) and in the Scrapbook screen.
2. **Settings and title completion.** Add `textSize`, `contrast` and `reducedMotion` to `PromSettings` (`consoleScreens.ts:58`) and normalize them; persist the opening's reduce-motion. Add CONTINUE to the title when a run exists, and a confirm-gated "erase Yearbook". Replace `version !== 1` with a migration step in `rules.ts:2996`.
3. **Plates and term pages.** Queue plates for THE SHIELD CHANGES HANDS and THE TRANSMITTER GOES DARK in the conductor art ledger (auto_submit) and drop the stand-in. Add a saved page per finished term: on the ending, append signature, ending, rival fights, romance and mastermind to a `comet-city-academy-terms-v1` key, and show it in `AcademyConsoleScreens.vue` Scrapbook.

**E)** The save-code export/import in `consoleScreens.ts:107` could be shared by other games.
