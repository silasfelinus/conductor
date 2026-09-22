# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-22T20:14:45Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1121**
- Outcomes: blocked: 18, cancelled: 2, done: 1101
- Success rate: **98%**
- Average passes on successful tasks: **0.3**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 73 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 15 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 11 | 100% |
| approval-portal | 2 | 0% |
| art-archive | 32 | 100% |
| art-generator-connect | 3 | 100% |
| brainstorm | 26 | 96% |
| butterfly-gallery | 32 | 94% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 39 | 100% |
| conductor | 133 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 51 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 27 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 140 | 100% |
| kapowarr | 52 | 100% |
| kind-economy | 10 | 100% |
| kind-robots | 67 | 99% |
| kindrobots-unraid | 9 | 100% |
| lora-ingestion | 6 | 100% |
| mandarin-tutor | 14 | 93% |
| media-watchlist | 12 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 85 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| rainbow-butterflies | 21 | 100% |
| ruler-hooked | 21 | 100% |
| scene-animator | 2 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 40 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 7 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 1104 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 39 |
| transient | 17 |
| actionable | 17 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 47% success over 17 closed tasks; aim the next kaizen task here
- failure category `quality` — 39 occurrences; look for the shared cause across its records
- failure category `transient` — 17 occurrences; look for the shared cause across its records
- failure category `actionable` — 17 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-22 `storybook/t-064` — test:lint-ratchet does NOT share test:prettier-ratchet's silent ambient-version-drift exposure: an unprovisioned npx eslint does resolve a different ambient version, but this repo's eslint.config.mjs unconditionally imports the Nuxt-generated .nuxt/eslint.config.mjs (only produced by nuxi prepare, part of npm ci's postinstall), so a bare npx eslint reproduction fails loud (ERR_MODULE_NOT_FOUND) before linting anything rather than silently misreporting a drifted count. Separately: pull_request_read's get_check_runs can serve stale cached in_progress status for a job that already completed (observed ~30 min stale here) -- cross-check with actions_get/get_workflow_job before treating a check as genuinely stuck.
- 2026-09-22 `storybook/t-063` — A local reproduction of a ratchet/version-sensitive CI gate (npm run test:prettier-ratchet) that disagreed with the task note's own open question about CI health turned out to be a sandbox artifact: no node_modules installed meant npx silently resolved an ambient prettier version instead of the lockfile-pinned one npm ci/CI actually use, producing a false '+30 files worse' reading. Before trusting any bare npx/npm-run reproduction of a version-sensitive check, provision deps first (npm ci or the repo's existing provisioning script) and confirm the installed tool version matches the lockfile -- an uninstalled or mismatched toolchain can fabricate drift that was never real.
- 2026-09-22 `storybook/t-062` — The same UI logic duplicated across two files (storybook-visual-setup.vue and conductor/storybook-page.vue both build the same StorybookStartInput draft) let an a11y fix (role=group/aria-label on choice grids, t-010) land in only one copy; a narrow textual guard scoped to a single file can't catch its sibling never getting the fix -- when auditing a fix's completeness, grep for other files building the same store/type shape, not just the one the original task touched.
- 2026-09-22 `conductor/t-193` — A same-day kaizen (t-192 -> t-193) that turns "found this bug by hand-grepping" into a structural test is cheap and worth doing immediately rather than deferring: the guard here is ~150 lines, ran in under a tenth of a second, and directly encodes the exact investigative step (grep every already_satisfied definition, check each one) that closed the parent bug. Mirroring an existing guard's shape (test_home_server_pm2_comfyui_direct_call_guard.py: glob the relevant files, define a positive-match regex/parser, assert clean, then self-test the parser/regex against a known offender so the test can't silently pass by never matching anything) made the design decision fast rather than open-ended -- worth reaching for an existing guard's shape before inventing a new one when the repo already has this pattern established.
- 2026-09-22 `conductor/t-192` — already_satisfied() == target_path(entry).exists() conflated two different questions: "has this ever rendered" and "does what's on disk answer the CURRENT pending request." They only diverge on a regeneration request (status flipped done -> pending after a prompt fix, reusing the same image_path), which is rare enough that the bug went undetected through the entire life of consume_art_requests.py/consume_art_inspirations.py -- until it silently ate two consecutive regeneration attempts on the same entry (ruler-hooked's choirfish) before anyone traced the actual job history. The fix (an explicit force: true per-entry field, cleared once fulfilled) generalizes: an idempotency check keyed on "does the output already exist" needs an explicit signal for "this specific pending cycle invalidates that output," because file/media existence alone cannot distinguish stale from current. Also load-bearing: this codebase's identical logic sometimes has TWO code paths (target_path().exists() vs. a live media-host HEAD check for kind_robots targets via consume_art_requests_to_media.py's wrapper) that look like one function from the caller's side -- a fix to the "obvious" one silently misses the production entrypoint a scheduled workflow actually calls.
- 2026-09-22 `storybook/t-010` — A file paused behind an upstream dependency (2026-09-12/13 TALKBACK note: don't polish storybook-visual-setup.vue until t-034/t-035/t-036's card-driven redesign lands) can sit unrevisited for over a week after the pause condition is actually met -- t-034/t-035/t-036 finished 2026-09-13, but nobody re-checked this file until this cycle (2026-09-22). The fix itself (role="group" + aria-label on two ungrouped choice-button grids) matched a pattern already fixed five times elsewhere in the project, confirmed to fail pre-fix via a git-stash round trip on the component. Worth generalizing: a pause note tied to a dependency's completion needs the same kind of staleness check this repo already runs for claimed tasks and stale recurring tasks, or "paused pending X" quietly becomes "paused forever" once X actually lands.
- 2026-09-22 `lora-ingestion/t-012` — When a broad UI utility patch trips the lint ratchet, repair the newly introduced lint findings on the same branch and require exact-head Actions completion before treating the retry as done.
- 2026-09-22 `lora-ingestion/t-011` — Two sessions independently implemented the same kaizen-filed fix (PowerShell paths-filter quote-only regex) within a ~30 minute window -- kind_robots#2969 (this task's own OpenAI Worker cycle, single/double-quote fix) and kind_robots#2970 (a different session, broader single/double/bare-scalar fix with a backreference guard), #2970 merging first. Discovered via #2969's PR showing mergeable_state=dirty on review; closed #2969 as redundant with a comment naming the superseding PR rather than resolving a conflict Reviewer has no push access to fix on a worker/* branch. No lost work -- the standard git-conflict backstop caught the collision as designed, just surfaced through PR mergeability instead of a rejected push.
- 2026-09-22 `lora-ingestion/t-010` — A same-day Claude session (session_01HHrZmwjtwx3T7A7H94irfo) opened kind_robots#2967 (LoRA purpose typing + randomized art batches, Silas-directed, additive migration) and correctly stood down on the one red CI check rather than force-merging or silently ignoring it -- but a session that authors and reviews its own work has no second party to actually merge it once it stands down. A later scheduled Conductor sweep found the open, ready-to-merge PR, independently re-verified the "pre-existing, unrelated" claim (reproduced the regex/quoting bug directly against origin/main) and the migration's additive-only shape, then merged. Worth normalizing: an agent authoring a PR should still expect a distinct review/merge pass to pick it up promptly rather than assuming the standing-down comment alone gets it to main.
- 2026-09-22 `conductor/t-190` — Implemented the zero-diff-close audit hint itself (roadmap_deps.zero_diff_close_hint, wired into run_worker.find_ready_task and next_ready_task.first_ready_task): an advisory audit_candidate/audit_candidate_reason field on the picked ready task, flagged when a done depends_on dependency's note mentions the ready task's own id. select_role.py inherits it for free via build_queue_summary(). Clean first-pass -- the pattern was already fully specified by the kaizen note itself (t-031/t-033), same "sibling task already proved the pattern" shape the note describes.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-22T20:14:45Z_
