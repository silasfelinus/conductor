# Shifting Desks — main-game standard audit (2026-11-12, kind_robots 7ad1136)

## A) Audit
| Item | Status | Evidence | Gap |
|---|---|---|---|
| Title screen | Partial | Front desk, `pages/play/shifting-desks.vue:~150-205`: "Return to your desk" (Continue), "New game", Personnel Archive, Daily Memo, art-style picker | No Settings. Achievements sit inside the Archive only |
| Settings | Missing | Only the art style (`shifting-desks-art-style-v3`, `utils/shiftingDesks/artStyles.ts:47`), plus the CSS reduced-motion query (`:1925`) | Everything in item 2 |
| Save/load | Met (no account) | `stores/shiftingDesksStore.ts:34-39,72-108`: run / outcomes / endings / rewards / envelope keys, saved on every action. `upgradeRun` migrates v1 → v4+ (`utils/shiftingDesks/rules.ts:1838`). `RewardArchive` v1 | No account save |
| Achievements | Partial | 3 live (`stores/shiftingDesksStore.ts:192-217`). 10 local MILESTONES (`utils/shiftingDesks/rewards.ts:48-134`) | 9+ more |
| Scrapbook | Met (mostly) | `shifting-desks-personnel-archive.vue` tabs: milestones / endings (locked "Classified ending", X/11 count, `:370-415`) / Distinctions / runs (receipts, up to 30) | No "characters met" or art-unlocked tab |
| Endings + plates | **Met** | 11 endings (`utils/shiftingDesks/endings.json`: 9 board, 1 elimination, 1 secret). All 11 plates return 200 image/webp live at `/images/shifting-desks/endings/<id>.webp` | none |
| Characters | Partial | 5 job titles with 6 skills, a perk and a portrait (`rules.ts:577`) | No name or look |
| Replay hooks | Met | Daily Memo seed, 5 jobs, 6 societies, 8 mutations, endings collection, milestones, successors | none |

## B) Characters
The job title already works as a class pick with stats. To close the gap, add an employee name (and optional pronouns) shown on the personnel file, receipts and Board ending text, plus a badge-photo variant per job. This fits the bureaucratic-satire genre well.

## C) Proposed achievements (keep the existing 3)
Most of these come from the existing milestones (`shifting-desks-<milestoneId>`), awarded in `recordEnding` (`stores/shiftingDesksStore.ts:147`) by diffing `rewardArchive.milestones` before and after `recordReward`:
- shifting-desks-survived-review / -sub-level-zero / -faced-the-board (existing)
- shifting-desks-first-ending: "A Permanent Position", first ending
- shifting-desks-five-departments: "Entirely Reviewed", all 5 departments in one run
- shifting-desks-employee-of-the-month: "Let the Board make you an example"
- shifting-desks-mutation-used: "Medical Leave Denied". Also award directly in `useInstant('mutation')`
- shifting-desks-society-agent: "Discreet Membership". Also award directly in `useInstant('favor')`
- shifting-desks-successor: "Team Restructuring", used a Successor
- shifting-desks-forms-25: "A Paper Trail", 25 files in one run
- shifting-desks-three-endings: "Repeat Offender", 3 endings found
- shifting-desks-exceptional-empathy: "A Treatable Condition", Empathy 10+
- shifting-desks-posthumous-affairs: secret ending (`wearing-a-dead-mans-badge`), awarded in `recordEnding` by ending id
- shifting-desks-the-kind-rewrite: the kind ending, same point
- shifting-desks-all-endings: "Full Personnel File", 11/11 in `endingsFound`
- shifting-desks-daily-memo: finish a Daily run, in `recordEnding` when `run.daily`
- shifting-desks-every-job: a receipt for all 5 job titles in `rewardArchive.runs`

## D) Three ~1-day PRs
1. **Achievements to 18.** Seed the records via `/api/achievements/batch`, add the milestone diff and award calls in `stores/shiftingDesksStore.ts`, and mount the strip on the front desk.
2. **Settings panel.** New `components/shifting-desks/shifting-desks-settings.vue`, or reuse `components/playbook-kit/playbook-kit-settings.vue`. Controls: text size, transition/envelope speed, reduced motion, high contrast, art style (move the picker in), and reset progress with confirmation (clears the 6 keys). Open it from the front desk and the in-play header.
3. **Employee name.** Add a name field on the hire screen (`pages/play/shifting-desks.vue:217-322`), store it on `RunState` (bump the version and handle it in `upgradeRun`), and show it on the personnel file, receipts and ending text.

## E) Reusable
The Personnel Archive is the most complete scrapbook of the four: locked slots, X/N count, run receipts, and an achievement cabinet that reads `achievementsForGame()`. It's a good template for a generic scrapbook.

## Shared notes
- Live `/api/achievements` on 2026-11-12: emperor 3, shifting-desks 3, zuzu-gamebook 3, slime-city 0.
- None of the four audited games has audio, so the "music/sound volume" setting has nothing to control until sound exists.
- None of them mounts `components/achievements/game-achievement-strip.vue`; only `pages/play/arcade/index.vue` and `components/navigation/workspace-sheet.vue` use it.
- The only account-backed save among the four is Slime City's `SlimeCityAccount`.
- Shared components:
  - **Settings + scrapbook kit:** `stores/playbookKitStore.ts` and `utils/playbookKit/settings.ts` (textSize, font, contrast, motion, textSpeed, sound, trailer, plus resetSettings, one versioned localStorage record per game), and `components/playbook-kit/playbook-kit-{settings,scrapbook,endings,shell}.vue`. Used today by monstrique, game-of-captains and every-villain-tactics.
  - **Title console:** `components/monstrexx/monstrexx-front.vue` (New / Continue / settings / scrapbook panels; the standard's reference). It could be generalized into a `game-title-console` that takes a game slug and its art.
  - **Save:** Emperor's `saves.ts` for slots and rewind; Slime City's `SlimeCityAccount` + story GET/POST to generalize into a `GameSave` model for account-backed saves.
  - **Achievements:** `game-achievement-strip.vue` plus `achievementsForGame()`. Each game needs an `ACHIEVEMENT_SECTIONS` entry.
