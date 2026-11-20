# Portfolio Intent Audit — 2026-11-20 (UTC file date; reviewed the evening of 2026-11-19 PT)

A scheduled Conductor agent did this review. It used no paid model API and no device testing.

Sources read:
- `OVERSIGHT-AGENT.md`, `AGENTS.md` and the 2026-11-18 audit.
- The diffs to `CONTROL.md`, `priority.yaml` and `project-overrides.yaml` since 11-17: conductor#7563, #7566, #7594, #7598 and 0cb6345.
- `project_triage.py`, `audit_roadmaps.py`, `check_pr_merged_drift.py` and `PORTFOLIO-OVERSIGHT.md`.
- The open-task lists for slime-city, emperor-of-dust, rainbow-bullet-hell-space-princess, save-the-plumber and chessweeper.
- Task notes for slime-city t-009, t-012 and t-041, emperor-of-dust t-033, t-063 and t-064, and chessweeper/t-001.
- kind_robots#5305 and #5379, and conductor#7630 and #7632.
- The kind_robots `main` tree, checked for Emperor item art and Chessweeper assets.
- A live HTTP check of the Chessweeper art URLs on kindrobots.org.

## Verified

- **New human direction since 11-18 is reflected consistently everywhere.**
  - **Downward Mobility** (slug `shifting-desks`): Silas renamed it on 11-17 PT and approved early public playtest. It is `playtest`/`normal`, has an owner waiver listing five open tasks, and moved to the playtest band in `priority.yaml`. Source: #7563 and #7566.
  - **Ecotone** (`weird-humboldt`): Silas handed it to playtest on 11-18 PT. It is `playtest`/`normal`, left the focus tier, and was removed from the CONTROL "Priority order this week" line. Source: #7594.
  - **Chessweeper**: new on 11-17 PT, `active`/`high`, and listed in `priority.yaml`. Source: #7565 and #7598.
  - **brainstorm**: changed to `finished` from the workspace UI on 11-19 (0cb6345).
- **The priority order matches the newest direction.** CONTROL now reads slime-city → emperor-of-dust → rainbow-bullet-hell-space-princess → save-the-plumber → …, which matches the top of `priority.yaml`.
- **Slime City's CLASH 300 actually landed, not just its bookkeeping.** t-041 is `done` on kind_robots#5379 (squash 5b715a7, all 15 checks green):
  - 230 LIVE_QA rows were promoted to QA_PASSED.
  - The 294-card matchup suite plus the constructed suite cover all 300 cards.
  - kind_robots#5357 gives all 300 cards curated L2 and L3 art.
  - What's left is t-012 (input and controller QA, actively claimed 02:18Z) and three of Silas's gates: t-009, t-014 and t-015.
- **Both questions carried from 11-16 and 11-18 are closed.**
  - The Zuzu verdict tasks (gamebook t-017, shifting-lands t-018) are out of the roadmaps; both projects now have `POST-PLAYTEST-DECISIONS.md`.
  - Ecotone t-020 and t-027 are `done`.
- **The Emperor private-art intake is contained.** conductor#7632 made `emperor-of-dust-private-art-review.yml` manual-dispatch-only.
  - #7630 is closed unmerged. Its only extra change was moving the host to the retired Vercel URL, which was wrong.
  - Its stale branch `worker/emperor-of-dust-t-064-intake-safety-20261119` kept routing `select_role.py` to `reviewer`. This session cleared it through `branch-janitor` (`force_delete_branches`).
  - The key-custody decision is still Silas's security gate on t-064.
- **Structure.** `audit_roadmaps.py` reports 0 errors across 97 roadmaps. Project parity has 0 forward drift and 0 reverse orphans.

## Corrected (this cycle)

- **emperor-of-dust/t-033 is real work again, not a dead wait.** Its note (last updated 10-21) says the 30 market-item icons are "PENDING behind a slow queue".
  - In fact `ITEMS-ROUND-1.yaml` has all 30 jobs `DONE`.
  - On kind_robots `main`, `ITEM_ART` is still an empty set, and `public/emperor-of-dust/items/` doesn't exist.
  - So the market still shows placeholder glyphs a month after the renders finished.
  - This is the top ready task of the #2 priority project. This session picks it up next (curate, then export) rather than leaving it to age.

## Still questionable

1. **Chessweeper t-001 (`publish` gate) and kind_robots#5305.**
   - #5305 is merged (11-19 09:24 PT, by the `silasfelinus` account). Its body said "Do not merge or deploy without explicit human release approval".
   - t-001 is still `needs-human`.
   - Agents also act through that account, so the merge alone can't show who made the publish decision.
   - **Choice for Silas:** if you merged it, mark t-001 approved and done. If you didn't, say whether to keep it live or revert it.
2. **The Chessweeper art pack exists only on the host.**
   - The five WebPs return 200 on kindrobots.org, but they are not in the kind_robots repo: `public/images/chessweeper/` is missing from `main`.
   - Five files reference them: home directory, posters, the route icon, `art.css` and `progression.js`.
   - A clean redeploy from git would break all five.
   - **Recommendation:** commit the five files from the host checkout. That needs physical or host access, so Silas or a host-side session has to do it. Alternatively, let chessweeper/t-003 replace them with ArtJob renders.
3. **Slime City lifecycle after t-012.** Once t-012 closes, Slime City will be an `active` project whose only open tasks are Silas's gates (t-009, t-014, t-015). It would still sit at the top of the priority list.
   - Ecotone and Downward Mobility set the precedent: move to `playtest`/`normal` with a handoff.
   - **Recommendation:** do the same when t-012 lands. Lifecycle is Silas's call, so this is flagged rather than applied.
4. **Carried:** emperor-of-dust/t-064's key custody stays a `security` gate. The art-archive and butterfly-gallery questions from 11-18 were not re-checked this cycle.

## Next review

2026-11-23 (three days).
