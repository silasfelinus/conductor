# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-12T14:29:54Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **930**
- Outcomes: blocked: 16, cancelled: 1, done: 913
- Success rate: **98%**
- Average passes on successful tasks: **0.1**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 73 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 14 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 9 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| brainstorm | 26 | 96% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 25 | 100% |
| conductor | 97 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 51 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 23 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 126 | 100% |
| kapowarr | 52 | 100% |
| kind-economy | 10 | 100% |
| kind-robots | 55 | 98% |
| kindrobots-unraid | 6 | 100% |
| lora-ingestion | 1 | 100% |
| mandarin-tutor | 11 | 100% |
| media-watchlist | 12 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 83 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| rainbow-butterflies | 20 | 100% |
| ruler-hooked | 11 | 100% |
| scene-animator | 2 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 21 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 6 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 913 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 19 |
| transient | 15 |
| actionable | 13 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 47% success over 17 closed tasks; aim the next kaizen task here
- failure category `quality` — 19 occurrences; look for the shared cause across its records
- failure category `transient` — 15 occurrences; look for the shared cause across its records
- failure category `actionable` — 13 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-12 `interface-vision/t-132` — A CI-config kaizen (adding a warning-only shellcheck pass to an existing bash -n step) is safest when it reuses the same changed-file discovery already computed in that step rather than re-running git diff -- one mapfile call, then bash -n and shellcheck back to back with `|| true` on the new one, so the existing hard-failing check's behavior is provably untouched. Installing the tool locally (apt-get install shellcheck) to confirm a real finding logs but doesn't propagate a nonzero exit was worth the minute it took -- cheaper than trusting `|| true` semantics from memory.
- 2026-09-12 `storybook/t-032` — Same DB-backed-verifier-catches-what-the-sandbox-cannot pattern as t-029, different write path: a character-sheet play created its LifeChoice row with rewardId null then patched it in a second update, so the persisted row ended up correct but the API response returned null for the played card on the very turn it was played. A two-step create-then-patch can be internally consistent in the database while still returning a wrong response for that one request -- resolve foreign keys before the transaction and write them on the initial create when the response of that same call needs to reflect them.
- 2026-09-12 `storybook/t-030` — Roadmap state can drift from reality even without a Reviewer rejection: kind_robots#2662 (implementing t-029/t-030/t-032/t-033) merged clean, but the four conductor tasks it closed were never flipped to done because this slice was never run through claim_task.py -- there was no queued task-events close-out to catch it. State-reconciliation after a cross-repo merge needs an explicit roadmap sweep, not just trust that a close-out event exists somewhere.
- 2026-09-12 `storybook/t-029` — kind_robots#2662's own DB-backed verifyStorybookPlayLoop.ts caught a real write-boundary bug the authoring sandbox (no database, no docker daemon) could not have found: the +-2 moveEffects clamp existed only inside the narration validator, one layer above where submitStoryTurn actually wrote LifeStat rows, so any caller that bypassed the validator could move an axis by 9 or write an axis the deck does not declare. Fixed by adding a clampEffectsToDeck() at the write boundary itself. When a schema-affecting engine PR's own body flags 'this DB-backed job is the one to watch, I could not run it locally' -- take that literally: wait for the real CI run and read its actual failure output before assuming a design-reviewed diff is safe to merge, even when every DB-free suite passed.
- 2026-09-12 `conductor/t-154` — select_role.py's commit_combined_state() called GET /repos/{owner}/{repo}/commits/{sha}/status (the legacy commit-status API), which only reflects legacy status-API integrations -- this repo's CI is entirely GitHub Actions check-runs, which post to the separate /commits/{sha}/check-runs endpoint instead, so the legacy call always returned {'state': 'pending', 'total_count': 0} regardless of real CI outcome. Both of its callers (find_reviewable_claude_prs, requiring 'success', and find_red_stale_prs_in_repo/pr-medic, requiring 'failure'/'error') were silently dead for every repo this script has ever checked. When computing a commit's combined CI state for a repo whose CI is GitHub-Actions-based, use the Checks API (/commits/{sha}/check-runs, paginated) and fold status/conclusion into pending/failure/success client-side -- never assume the legacy Status API reflects Actions-based check runs, even though both are commonly described as 'the commit's CI status'.
- 2026-09-12 `conductor/t-153` — check_pr_merged_drift.py's cross-repo GitHub Search API call (/search/issues?q=...) 403s unconditionally in this sandbox ('sessions are bound to their configured repositories'), even with GITHUB_TOKEN set, while repo-scoped endpoints (/repos/{owner}/{repo}/pulls, /repos/{owner}/{repo}/pulls/{number}) work fine. Any script that needs to find a PR by title/content across multiple repos should list-and-filter per repo rather than use the Search API, and should cache each repo's listing across multiple lookups in the same run rather than re-paginating per candidate. A residual per-repo 403 after this kind of fix is more likely an out-of-scope repo for the session's credentials (see AGENTS.md's Repository Scope) than the Search-API restriction -- check which case it is before assuming the fix didn't work.
- 2026-09-12 `interface-vision/t-104` — Mechanical size shorthand migrations are safe when the codemod is restricted to static class attributes and excludes text-/stroke-/fill-colored shapes; exact-head CI plus full diff review caught no behavioral or geometry change (slice 241, silasfelinus/kind_robots#2655).
- 2026-09-12 `interface-vision/t-130` — A kaizen task sourced directly from a real CI-escaping bug (t-128's inline-regex bash syntax error) landed clean first pass because the fix's own verification loop closed the gap it was fixing: the new bash -n step's PR ran inside the same layout-contract job it modifies, so a syntax error in the new step itself would have failed loudly rather than merging silently. Prefer this shape (the fix's CI run exercises the fix) over a purely textual review for any CI-workflow-editing task.
- 2026-09-12 `interface-vision/t-104` — Running a blanket `prettier --write` across every file a codemod touched (to tidy the one or two multi-line class attributes the codemod's edit legitimately shortened) also reformats unrelated pre-existing 80-col drift throughout each file -- drift kind_robots never enforces via a CI prettier check, so it silently accumulates. That incidental reflow broke two hardcoded literal-string contract scripts (verifyTaskmasterCheckpointEngine.mjs, verifyDailyDreamArchiveWorkbench.ts) that assume specific substrings stay on one line/one call. Caught by CI before merge (self-triaged and fixed in the same PR, no Reviewer round needed), but the fix was to stop running `prettier --write` at all rather than chase each incidental reflow -- this repo has no CI-enforced prettier check, so nothing requires it, and a pure mechanical 1:1 token substitution (no line-structure change) is both safer and a smaller diff. Future size/shorthand codemod slices should skip blanket prettier passes; if a specific line genuinely needs reformatting, target only that line/file, not `prettier --write <whole-changed-file-list>`.
- 2026-09-12 `interface-vision/t-129` — The viewport-grid layout-contract report dedups by (file, token) pair, not by raw occurrence count -- two lines in the same file carrying the identical breakpoint token (e.g. two 'sm:grid-cols-2' divs) show up as a single baseline entry, so the baseline count delta after a slice doesn't map 1:1 to 'lines touched'. Check the actual diff, not just the before/after baseline number, to confirm a slice's real scope.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-12T14:29:54Z_
