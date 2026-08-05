# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-05T05:06:04Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **518**
- Outcomes: blocked: 13, cancelled: 1, done: 504
- Success rate: **97%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 57 | 98% |
| alexa-integration | 2 | 100% |
| animation-manager | 13 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 6 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 25 | 100% |
| conductor | 61 | 100% |
| conductor-app | 2 | 100% |
| davinci | 2 | 100% |
| digital-storefront | 25 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 4 | 100% |
| interface-vision | 70 | 100% |
| kind-robots | 40 | 98% |
| kindrobots-unraid | 4 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 48 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 2 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 503 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 9 |
| actionable | 9 |
| transient | 8 |
| scope | 2 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `quality` — 9 occurrences; look for the shared cause across its records
- failure category `actionable` — 9 occurrences; look for the shared cause across its records
- failure category `transient` — 8 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-05 `ai-art-academy/t-010` — A sibling kind_robots checkout's shallow-clone boundary can silently sit stale relative to origin/main (fetched to a different, non-overlapping depth in an earlier session), which makes `git rebase origin/main` report spurious add/add conflicts on nearly every file (no shared merge-base) even though the branches are not actually unrelated -- `git merge-base HEAD origin/main` returning empty combined with `git rev-parse --is-shallow-repository` returning true is the tell; `git fetch --unshallow origin` before rebasing resolves it cleanly. Separately, after any operation that changes the checked-out commit graph (unshallow, rebase, branch switch), re-run `nuxi prepare` before trusting a `vue-tsc --noEmit` result -- stale `.nuxt` type stubs produced a handful of spurious `useEarnedKarma`/`useStorybookMode` auto-import errors that disappeared entirely after regenerating types against the current tree.
- 2026-08-05 `kind-robots/t-053` — When adding a new failure-signature check, search for and reuse an existing detection pattern in the codebase (scripts/lib/databaseRetry.ts's isTransientDatabaseError() and cypress/e2e/api/users.cy.ts's inline pool-timeout regex) rather than inventing a parallel one -- keeps the two detectors from drifting apart as the real error shapes change. Separately, after running a local `prisma generate` for verification, diff generated files against git before committing -- local generation can drift from what's committed even with no schema change, and that drift is easy to sweep in by accident via `git add -A`.
- 2026-08-05 `digital-storefront/t-036` — Doc-accuracy corrections to a roadmap note should fix the wrong text in place with a short parenthetical marking what changed, not append a whole new correction paragraph — keeps the note's primary content readable instead of burying the fix at the bottom of an already-long history.
- 2026-08-05 `ai-art-academy/t-010` — A shared-component "clear/reset" function that touches several unrelated global Pinia singletons (deselectBot/deselectCharacter/deselectDream/deselectReward/deselectScenario) is only safe when gated on the same prop that controls whether the UI exposing those fields was ever shown. Unconditional cleanup in a function called automatically on every successful action (not just an explicit user click) silently wipes state the current view never gave the user any way to see or intend to clear. Before implementing a subagent's bug report, independently re-verified the specific store calls and their persistence side effects rather than trusting the report at face value.
- 2026-08-05 `interface-vision/t-081` — When a "picker" component is contract-fenced read-only (verifyFacetGallery.ts forbids create/update/archive text in facet-gallery.vue), add the missing create affordance to its thin wrapper component instead, and hand off to the real admin flow via a one-shot query-param flag (?create=1, consumed and cleared by the tab it lands on) rather than duplicating the create form or loosening the contract. Kept the read-only contract test green with zero changes needed to the fenced file itself.
- 2026-08-05 `interface-vision/t-068` — Re-check recent merges immediately before merging a scoped follow-up on a frequently claimed umbrella task; a concurrent broader PR can complete the same slice between CI start and merge.
- 2026-08-04 `interface-vision/t-086` — Multi-stage media fallback state must identify which candidate failed. A single failed boolean can represent one transition but cannot safely drive a chain with two or more candidates.
- 2026-08-04 `interface-vision/t-094` — Applied verifyLayoutContract.ts's existing baseline/ratchet pattern to a second contract check (auditWonderLabPreviews.ts) with an almost line-for-line-identical shape: allow-list of known-bad entries in a JSON file, --strict fails only on entries not in the allow-list, --update ratchets the baseline down and refuses to grow it. kind_robots PR #1434, merge 41b334248747da904c92245d7fabc9f1abca3f7e. Verified the negative case explicitly (injected a synthetic new required-prop component with no fixture, confirmed --strict flagged only the new one and not the pre-existing 29) rather than just the positive case -- worth doing for any future ratchet-pattern port, since a baseline that silently allow-lists everything (e.g. from a coding mistake) looks identical to a correct one on the happy path alone.
- 2026-08-04 `interface-vision/t-082` — A prior connector-only session released this task ("connector patch limitation" -- could not safely patch a 500+ line file, and had no local git/DNS). A session with full shell/git access hit no such limitation: mirrored add-reward.vue's Publishing section (isPublic/isMature toggles, t-080) onto add-scenario.vue verbatim, no store changes needed since scenarioStore already round-trips both fields. kind_robots PR #1433, merge 82f61b1e5d3ed5d0e992ecf76ab5fa1beb5aa501. Lesson: a connector-limited session's "actionable" release reason should be read literally -- it is a tooling gap for that session, not evidence the task itself is hard, so a shell-capable session should retry it directly rather than assuming the release implies deeper difficulty.
- 2026-08-04 `interface-vision/t-060` — Completed the final three reachable core-gallery migrations (character, reward, dream) and closed the measured 7/7 core-object beta gate without forcing row or dropdown variants into a shared grid abstraction. kind_robots PR #1418, merge 6b541a3ed4c65570659c37aed9d7748fb087d734.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-05T05:06:04Z_
