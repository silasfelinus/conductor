# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-05T13:42:51Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **523**
- Outcomes: blocked: 13, cancelled: 1, done: 509
- Success rate: **97%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 59 | 98% |
| alexa-integration | 2 | 100% |
| animation-manager | 13 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 6 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 25 | 100% |
| conductor | 64 | 100% |
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
| software | 508 | 99% |

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

- 2026-08-05 `ai-art-academy/t-056` — A kaizen note asking for a field that doesn't exist in the source data (here: "region") is worth implementing as closely as the real schema allows rather than skipping outright -- era-based sort/overlap-detection delivered the same practical benefit (spotting a coverage gap before adding a new curriculum entry) using only fields that actually exist.
- 2026-08-05 `ai-art-academy/t-043` — Keep curriculum inclusion, reproduction rights, and generation-preset permissions as separate policy questions. Collapsing them into one death-date cutoff can erase historically important artists while still failing to express the actual copyright and commercial-use constraints.
- 2026-08-05 `conductor/t-099` — Adding a "strongest evidence" field/tier to a multi-pass classifier isn't complete until the code path that decides "does this field apply" also distinguishes absent-and-should-fall-back from present-but-corrupt-and-should-not. A single parse_x() -> Optional[T] helper collapses both into None, which reads fine until a caller uses "is None" as the fallback trigger -- a malformed value then silently gets treated as if the stronger evidence were never there at all, quietly replaced by a weaker heuristic instead of surfacing. Caught by external review before merge (PR #1737) rather than by the implementing session's own test pass, since the tests written alongside the feature covered field-present/field-absent but not field-present-but-malformed -- a reminder to enumerate all three states explicitly whenever a field is optional AND has a shape to validate, not just "present vs. absent."
- 2026-08-05 `conductor/t-099` — A dedicated implementation_pr field, written once at close time, is strictly stronger evidence than any post-hoc heuristic (title search or note-quoted PR reference) for reconciling roadmap state against reality -- it's self-reported by the session that actually did the work, immune to title-convention drift, and free to check (one direct PR lookup vs. a search). The one sharp edge worth remembering: a field that is present-but-malformed is not the same case as a field that is absent -- both `parse` to None, but conflating them lets corrupted roadmap data silently fall back to weaker search/note evidence and report a false "clean" instead of surfacing as unresolved. Route "truthy but unparseable" to unresolved explicitly, never through the same branch as "falsy/missing".
- 2026-08-05 `conductor/t-098` — A note-quoted PR reference cannot distinguish a task's implementing PR from the PR whose kaizen suggestion filed the task -- both are quoted the same way in prose. A much stronger signal, and one that's basically free once the convention holds, is searching for a merged PR whose own TITLE names "<project>/<task-id>" (the convention close-out PRs already follow in practice). Prefer that self-reported, task-authored signal over parsing free-text notes whenever a tool needs to associate a task with "the PR that actually did this," and treat any weaker/inferred signal (like a note reference) as advisory, not proof, in the tool's own output.
- 2026-08-05 `ai-art-academy/t-010` — A sibling kind_robots checkout's shallow-clone boundary can silently sit stale relative to origin/main (fetched to a different, non-overlapping depth in an earlier session), which makes `git rebase origin/main` report spurious add/add conflicts on nearly every file (no shared merge-base) even though the branches are not actually unrelated -- `git merge-base HEAD origin/main` returning empty combined with `git rev-parse --is-shallow-repository` returning true is the tell; `git fetch --unshallow origin` before rebasing resolves it cleanly. Separately, after any operation that changes the checked-out commit graph (unshallow, rebase, branch switch), re-run `nuxi prepare` before trusting a `vue-tsc --noEmit` result -- stale `.nuxt` type stubs produced a handful of spurious `useEarnedKarma`/`useStorybookMode` auto-import errors that disappeared entirely after regenerating types against the current tree.
- 2026-08-05 `kind-robots/t-053` — When adding a new failure-signature check, search for and reuse an existing detection pattern in the codebase (scripts/lib/databaseRetry.ts's isTransientDatabaseError() and cypress/e2e/api/users.cy.ts's inline pool-timeout regex) rather than inventing a parallel one -- keeps the two detectors from drifting apart as the real error shapes change. Separately, after running a local `prisma generate` for verification, diff generated files against git before committing -- local generation can drift from what's committed even with no schema change, and that drift is easy to sweep in by accident via `git add -A`.
- 2026-08-05 `digital-storefront/t-036` — Doc-accuracy corrections to a roadmap note should fix the wrong text in place with a short parenthetical marking what changed, not append a whole new correction paragraph — keeps the note's primary content readable instead of burying the fix at the bottom of an already-long history.
- 2026-08-05 `ai-art-academy/t-010` — A shared-component "clear/reset" function that touches several unrelated global Pinia singletons (deselectBot/deselectCharacter/deselectDream/deselectReward/deselectScenario) is only safe when gated on the same prop that controls whether the UI exposing those fields was ever shown. Unconditional cleanup in a function called automatically on every successful action (not just an explicit user click) silently wipes state the current view never gave the user any way to see or intend to clear. Before implementing a subagent's bug report, independently re-verified the specific store calls and their persistence side effects rather than trusting the report at face value.
- 2026-08-05 `interface-vision/t-081` — When a "picker" component is contract-fenced read-only (verifyFacetGallery.ts forbids create/update/archive text in facet-gallery.vue), add the missing create affordance to its thin wrapper component instead, and hand off to the real admin flow via a one-shot query-param flag (?create=1, consumed and cleared by the tab it lands on) rather than duplicating the create form or loosening the contract. Kept the read-only contract test green with zero changes needed to the fenced file itself.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-05T13:42:51Z_
