# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-24T20:29:43Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **748**
- Outcomes: blocked: 15, cancelled: 1, done: 732
- Success rate: **98%**
- Average passes on successful tasks: **0.2**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 70 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 13 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 9 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| brainstorm | 25 | 96% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 25 | 100% |
| conductor | 80 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 4 | 100% |
| davinci | 7 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 83 | 100% |
| kapowarr | 48 | 100% |
| kind-economy | 6 | 100% |
| kind-robots | 50 | 98% |
| kindrobots-unraid | 5 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 79 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
| scene-animator | 1 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 16 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 6 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 16 | 44% |
| software | 732 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 14 |
| actionable | 10 |
| transient | 10 |
| scope | 2 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 14 occurrences; look for the shared cause across its records
- failure category `actionable` — 10 occurrences; look for the shared cause across its records
- failure category `transient` — 10 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-24 `cthulhuquarium/t-006` — A research task benefits from live web search over training-data recall alone, even for well-established reference games: search surfaced AbyssRium's specific documented failure mode (hidden/undocumented unlock triggers requiring a wiki) and current retention-benchmark figures that made the adopt/adapt/reject list's reasoning concrete and sourced rather than generic genre-savvy assertion. Cross- referencing every finding against the project's own already-committed design docs (DESIGN-BRIEF/SYSTEMS/ECONOMY) before writing anything down kept the output as confirmation-plus-authoring-guidance for named downstream tasks rather than a survey that risked relitigating settled decisions.

- 2026-08-24 `cthulhuquarium/t-004` — "Simulate it, don't just spec it" caught a real methodology bug before it could look like a balance bug: a naive active-vs-idle coin-balance comparison showed idle beating active over two hours, which would have read as a genuine MVP-requirement violation (DESIGN-BRIEF's "idling rewarded but strictly worse than playing"). The actual cause was comparing raw liquid balance, which conflates spending (buying a fish, an investment) with losing. Switching to net worth (coins + owned-asset value) and gross income earned (cumulative production before spend) reversed the finding to a healthy 3-3.5x active/idle gap that widens over time via reinvestment compounding. Worth generalizing: any economy simulation comparing two spending strategies needs a wealth metric that survives the comparison, not a currency balance that a strategy's own spending pattern can arbitrarily deflate.

- 2026-08-24 `cthulhuquarium/t-007` — A live-DB migration doesn't have to stay unverifiable in a sandbox with no docker daemon: `apt-get install mariadb-server`, running `mariadbd` directly (no systemd) under the `mysql` user, and connecting via the local socket to create the app user took under a minute and gave a real MySQL-compatible target to run `prisma migrate deploy` against. Running it through the FULL existing migration history (62 migrations), not just the new one in isolation, is what actually proves the new migration composes cleanly with everything before it -- and `prisma migrate status` reporting zero drift afterward is stronger evidence than `prisma validate` alone, which only checks the schema file's own internal consistency. Worth adding to AGENTS.md's cross-repo/kind_robots verification section as a documented option alongside `provision_kind_robots_deps.sh`'s dummy-DATABASE_URL `prisma generate` path, since that path alone doesn't catch a migration.sql that doesn't actually match what schema.prisma implies.

- 2026-08-24 `cthulhuquarium/t-025` — A recurring umbrella task at the top of priority.yaml's ready queue (interface-vision/t-104) had already been independently re-confirmed exhausted by three sessions the same day; spot-checking the one new upstream commit since the last check (rather than re-running the full sweep) confirmed nothing changed, and the session moved on to real work further down the priority order instead of manufacturing a fifth identical no-op. cthulhuquarium/t-025 was a clean fit: a self-contained design-decision task whose own note explicitly authorized an agent recommendation with reasoning, flagged (soft_gate: true) rather than hard-gated, so the answer could unblock downstream tasks (t-026/t-027) same-session instead of stalling on a human reply.

- 2026-08-24 `conductor/t-127` — A task's note can go stale between when it's filed and when a session picks it up -- Silas hand-fixed the acute incident this task described (three stuck operation: note events) hours before this session claimed it. Re-checking live git history and roadmap state before implementing found the task was actually asking for two things bundled together: the acute fix (already done, by hand) and a systemic guard (still open). Scoping the PR to only the still-open half, and following the human's own stated root-cause reasoning in the commit that did the acute fix, avoided both redundant work and contradicting a judgment call Silas had already made.

- 2026-08-24 `scene-animator/t-001` — The PR (kind_robots#2072) opened with a red TypeScript check: an ArtJob.include of a non-existent ArtImage Prisma relation (ArtJob only carries a plain artImageId int column), Content-Length passed as a stringified value where h3's typed header wants a number, and a Pinia ref (durationSeconds) that inferred a narrow literal union from an `as const satisfies`-typed presets catalog instead of number. All six errors were mechanical and caught deterministically by `npm run test` (vue-tsc); none needed a design change. Fixed and pushed as the Reviewer rather than rejecting back to the Worker, since the errors were narrow, unambiguous, and confined to the task's own new files. Re-affirms running the repo's local typecheck before opening a PR would have caught this before CI did.

- 2026-08-24 `brainstorm/t-031` — Task scope (add a real "promote candidate into an entity" action, carrying its art across) explicitly flagged its own hardest design question -- meta.art.imageIds is an array, the target entity's art model (entityArt.ts) is one scalar id per slot -- rather than leaving it implicit; tracing the array's one mutation site to confirm it was append-only (so "last entry" unambiguously means "most recent delivery") turned a could-have-been-a-guess into an evidence-based, one-line design decision. Also: before implementing, re-verified the prior task's (t-026) negative "no such action exists" finding rather than trusting it blind -- doing so surfaced the one precedent that DOES exist (promptStore.promoteToDream / dreamStore.promotePromptToDream) but is dead code, called from nowhere, which shaped which store to add the new function to and confirmed this was genuinely the first promotion pattern with a live caller. A UI wiring change that adds a new busy/loading state needs to check what the busy prop passed to the child component actually depends on, not just add the new emit -- isCandidateBusy here only checked state that regenerate/branch's shared runGeneration() call sets, so the new promote action's spinner would have silently never appeared without also folding pendingCandidateAction into that check. Third occurrence this session of the over-broad `prettier --write` trap (storybook/t-023, then here) -- worth normalizing as a standing habit: check `git diff --stat` immediately after any `prettier --write`, before staging, on any file with pre-existing formatting drift.

- 2026-08-24 `storybook/t-023` — Task scope (audit taskmasterStore's localStorage read path against storybookStore's restore guards) required tracing every real caller before deciding whether the missing `restoredFromStorage`-style guard was a bug: content/taskmaster.md mounts `:taskmaster-page` as the only call site, with no wrapper double-mounting it the way storybook-library-page.vue wraps StorybookPage, so no reachable race exists and the guard was correctly out of scope -- the parity gap alone was not sufficient, matching the cycle-36 lesson this task was scoped from. Fixed the unambiguous half (move `getItem()` inside the try) and left the caller-tracing result as an in-code comment. Also worth recording: a full-file `prettier --write` on a file with pre-existing prettier-version drift silently reformats unrelated lines far beyond the actual diff -- caught via `git diff --stat` before committing; the safe pattern is formatting only the new/changed region and verifying it in isolation, never running `--write` on the whole file when the rest carries known drift. Separately, this cycle hit a second occurrence of the documented conductor/t-124 "Python test suite" check-run reporting-lag pattern (job logs showed it passed and finished cleanup ~11 minutes before the check-run API reported completion) -- confirmed via job logs rather than assumed, and merged once confirmed rather than re-running blind.

- 2026-08-24 `brainstorm/t-026` — Task scope was explicitly conditional ("find, or confirm there isn't yet, a promote-candidate action, and IF one exists, wire the art across") -- a repo-wide search (candidate card's emitted events, the manager's kept-candidate bulk actions, server/api/brainstorm/, and a grep for promote/convert/"turn into"/createFrom) confirmed no such action exists anywhere. The honest close for a conditional investigation task with a negative finding is `done`, not a forced implementation and not `needs-human` -- the literal scope asked a yes/no question and got a firm no. Filed the actual feature (t-031) as new scope instead of expanding this task's diff, since building an unrequested promotion UI would have been scope creep past what t-026 asked for. Also worth recording for whoever picks up t-031: entityArt.ts's art-slot model is one scalar id per named slot per entity, while Brainstorm's meta.art.imageIds is an array -- there is no existing 1:1 precedent in the repo (promptStore.promoteToDream's Prompt only ever has one artImageId) for the many-to-one reduction that promotion will need.

- 2026-08-24 `storybook/t-010` — Cycle 36: after five consecutive cycles that either found a shrinking-returns polish item or no-op'd, the fresh angle that produced a real correctness bug was the one the PREVIOUS cycle had already written down and not taken -- "Pinia persistence edge cases have not had a dedicated pass in this task's history." The bug was a sibling-parity gap of exactly the shape a shared-helper family invites: taskmasterStore.ts's saveToLocalStorage() was the one localStorage writer of four in the narrative family with no try/catch, while its three siblings each carried an explicit private-browsing/quota comment explaining why they had one. Two lessons. First, a recurring bug-hunt task's own "next lead" note is a real work queue, not a formality -- reading it before inventing a new lens is cheaper than re-deriving one, and a lead that survives a cycle unclaimed is more likely to be untouched ground than a lens the task has already swept. Second, and the inverse of cycle 61's model-builder lesson: a found inconsistency IS a fixable sibling-parity bug when the two sides are genuinely the same kind of moment, and here the codebase said so itself -- the shared helper's own header asserted the two stores were "byte-for-byte the same shape," so the asymmetry was a documented invariant being violated rather than a pattern-match on surface similarity. Confirming the impact still required tracing all ten call sites individually: the sharpest one (updateBeatArt() running as an uncaught `void poll(...)` callback, where a throw both became an unhandled rejection and killed the art poll loop, stranding the illustration with no retry affordance) was not the one the shape of the bug suggested up front. Finally: when a fix restores an invariant a contract script already claims to enforce, extend that script -- and verify the new assertion fails against the pre-fix code, or it may be vacuously true.


---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-24T20:29:43Z_
