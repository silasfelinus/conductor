# Zuzu Gamebook: human-playtest readiness assessment
**As of:** 2026-11-14 PT  
**Decision:** NOT YET READY. Keep `active` / `high` and [master issue #4139](https://github.com/silasfelinus/kind_robots/issues/4139) open. This is an evidence-led remaining-work plan, not a new speculative feature list.

## What has already landed
- Nine-act deterministic Book One, with a historical checked baseline of **377 sections and 15 endings** (recount against current source at final handoff), dice, skills, Honor/Taint, combat, inventory and saves. Legal fresh-start seeds and frozen full-route replay witnesses for all 15 endings were added in [#4032](https://github.com/silasfelinus/kind_robots/pull/4032) and [#4037](https://github.com/silasfelinus/kind_robots/pull/4037) (15 fixtures, 1,217 player actions). Re-run on current `main` before handoff.
- **17 achievements** ([#5059](https://github.com/silasfelinus/kind_robots/pull/5059)); illustrated title, reading preferences, 15-ending ledger and per-run scrapbook ([#5070](https://github.com/silasfelinus/kind_robots/pull/5070)). Only Zuzu is the protagonist: character customization is expressly exempt.
- Two previously shared ending plates were delivered in [#5068](https://github.com/silasfelinus/kind_robots/pull/5068); **`ending-water` is still missing its own ending-specific plate** according to that PR.
- Combat odds/log/drawer/hit feedback ([#4826](https://github.com/silasfelinus/kind_robots/pull/4826), [#4864](https://github.com/silasfelinus/kind_robots/pull/4864)) and earned retreats from otherwise forced unwinnable fights ([#4780](https://github.com/silasfelinus/kind_robots/pull/4780)).
- Isolated malformed browser save slots so they cannot block recovery of valid neighboring slots ([#5154](https://github.com/silasfelinus/kind_robots/pull/5154), merged). This does **not** resolve account-backed save scope.

## Ordered remaining work, with exact owners and exit evidence

### P0. Finish and prove the art, not just ArtJob requests (`t-006`, `t-012`)
1. Reconcile the **35 scene-art gaps** in the most recent source-backed audit, current section-to-image bindings, image-load fallbacks and unique ending artwork; recount them against present `kind_robots/main`. `t-006` recorded Round 20's 14 candidates for seven scenes but did **not** confirm new ArtJob IDs, DONE media, keeper review or WebP delivery. Round 17/18 scene-fidelity work and staged Krea-to-Arthemy finishing also remain unresolved.
2. For every missing/mismatched scene and `ending-water`: obtain an actual DONE ArtJob or vetted existing image, visually approve at intended size, export the **public-safe approved WebP**, connect the correct section/ending, verify the final loaded image and provenance. Retire temporary SVG/fallbacks only when replacements work. Record an image coverage matrix, remaining defects and ArtJob/ArtImage IDs.
3. Resolve `t-012` **at the rendered-frame level**, not by checking that LoRAs exist. Zuzu plus a second LoRA still fuses bodies/costumes; Abbess portraits have human-face failures. Use separately rendered/composited characters, regional masks or another successful pipeline and independently assess two-character scenes for cast/canon fidelity. If a scene can legitimately be single-character, approve it against its text, not a blanket excuse.
**Exit:** every authored beat and all 15 endings have correct, reachable, accepted painted art; no open rendering, review, wrong-scene or placeholder blockers. Art queue submission by itself does not count.

### P1. Final complete-book editorial and mechanics pass (`t-007`, `t-008`, `t-013`)
4. Read complete representative playthrough transcripts end to end, check nine-act continuity, choice-to-consequence fidelity, moral agency, Ling/Bao and fixed-Zuzu canon, and endings that feel distinct. `t-007` identifies **Act V's 'deliver' shortcut (around 40% of sampled walks), Act IV's length, and the deliberate five-page Night Road slog** as concrete editorial review candidates. Fix meaningful shortcomings and preserve legitimate paths.
5. Finish `t-008` combat choice balance, combat-outcome imagery, restoration consistency and readable tactical feedback; verify actual Guard/Feint/Quiet Draw roles under legal route states. The optional shorter shared save code is polish, not an automatic acceptance blocker unless usability testing demonstrates a failure.
6. Close `t-013` with an **actual responsive inspection of the fight-warning cue at 390/768/1440px**; its note says the earned wounded fallback is already implemented in #4780. Re-run real wounded-entry/retreat witnesses rather than adding redundant escape paths.
**Exit:** no substantial editorial, fairness or UI defect remains; current-head graph, golden replay and combat tests pass with explicit results.

### P2. Finish the shared main-game floor (`t-015`)
7. Reconcile the account-backed Continue/save requirement (signed-in sync with safe local fallback, migration/conflict behavior and new-run preservation); #5154 only isolates corrupt local slots. Complete **cast-discovery, locked silhouettes and found counts** in the persistent scrapbook; audit journey history through reload, replay and new game. Confirm settings include required reading, motion/contrast, reset confirmations and audio controls as relevant to implemented audio. Do not redo the shipped title screen, 17 achievements or ending gallery.
**Exit:** main-game-standard audit updated with Met/Exempt evidence for each criterion; save/cast tests pass. `t-015` was `review` during this assessment while #5154 had already merged: reconcile task state before picking another slice.

### P3. Independent complete QA **after** P0-P2 (`t-009`)
8. Rebuild and validate the route graph, all reachable ending witnesses, 15 golden replay fixtures, conditional/locked branches and completion/death/low-resource states. Run the adversarial role/seed and all-combat matrices in the master issue; log exact command/run, seeds and findings. Fix failures, then rerun.
9. Test the actual Kind Robots reader at phone, tablet portrait/landscape, desktop and wide-short sizes; capture screenshots and inspect scene art, choices, story overflow, save/load, battle feedback, keyboard/focus, screen readers and reduced motion. Verify on the **self-hosted Kind Robots** experience, not on a retired Vercel preview. Resolve any high/critical visual or behavior defects.
10. Produce one **readiness evidence packet**: current section/ending counts, section-and-ending plate coverage with URLs/receipts, golden paths, test results, CI exact heads, screenshot links, editorial assessment and unresolved blocker list (empty). All scoped PRs merged and checks completed green; no work left only in branches or queued art.
**Exit:** `t-006`, `t-007`, `t-008`, `t-012`, `t-013`, `t-015`, and `t-009` all actually done. Do not turn the recurring `t-011` into an artificial endless blocker.

### P4. Verified handoff, **not** creative approval (`t-017`)
11. Transition the real final subjective gate `t-017` from `waiting` to **`needs-human`** and provide the playable route, coverage report and specific review asks. **Never set `approved_by_human` on Silas's behalf.**
12. In Conductor, flip `project-overrides.yaml` from **`active/high`** to **`playtest/normal`** and adjust the focused order in `projects/priority.yaml` and the matching `CONTROL.md` ordering language without disturbing other projects. Confirm the Kind Robots project projection shows PLAYTEST/NORMAL; keep its owned presentation fields intact.
13. Prefix the master issue title with **`[FLAGGED FOR HUMAN TESTING]`** and close it as **completed** after the handoff is verified, leaving its URL in `docs/agents/master-issues.yaml`. This removes it from the open build queue, **not** from the historical index. Any later substantive fixes are new scoped `playtest_iteration: true` tasks. Neither issue closure nor `needs-human` authorizes publishing, billing or launch.

## Execution order
Art fidelity and final editorial work can run in parallel if separate task claims do not collide. Save/scrapbook work is independent of most art. **Run `t-009` only after those finite streams finish; handoff `t-017` only after verified `t-009`.** Keep the master issue current with each actual merged acceptance increment. Cross-reference this dossier and avoid copying the entire issue into task notes.
