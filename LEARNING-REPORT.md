# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-20T04:06:09Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **306**
- Outcomes: blocked: 12, done: 294
- Success rate: **96%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 33 | 100% |
| alexa-integration | 2 | 100% |
| animation-manager | 7 | 100% |
| animation-studio | 1 | 100% |
| appmaker | 2 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 2 | 100% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 13 | 100% |
| conductor | 43 | 100% |
| digital-storefront | 12 | 100% |
| dream-cycle | 14 | 100% |
| ecosystem-map | 4 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 1 | 100% |
| kind-robots | 29 | 97% |
| kindrobots-unraid | 4 | 100% |
| media-watchlist | 1 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 29 | 100% |
| mural-design | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 2 | 100% |
| serendipity | 3 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 11 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 291 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 6 |
| actionable | 6 |
| transient | 4 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `quality` — 6 occurrences; look for the shared cause across its records
- failure category `actionable` — 6 occurrences; look for the shared cause across its records
- failure category `transient` — 4 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-07-20 `conductor/t-072` — Kaizen tasks phrased as 'test the class of bug beyond this one call site' can tempt an overly broad heuristic (e.g. scanning every nullable Prisma Int field). Grepping for the actual naming convention first (existing<Owner>Id) found only the two call sites the bug's own history named, both already fixed -- confirming no second live instance existed kept the new static contract (verifyExistingOwnerIdNullability.ts) narrow and false-positive-free instead of flagging the ~100+ unrelated authenticatedUserId/callerUserId params that are genuinely non-nullable. Also hit a reusable snag: importing a route handler file (server/api/resources/[id].patch.ts) directly in a DB-free test throws at import time because it pulls in server/utils/prisma.ts, which requires DATABASE_URL synchronously -- extracting the pure helper into its own compatibility.ts module (mirroring characters/compatibility.ts) sidesteps this cleanly and is a reusable pattern for future DB-free behavioral tests.
- 2026-07-20 `animation-manager/t-005` — New route content mounts (content/<slug>.md with a channelKey/tabKey pair) aren't self-sufficient -- verifyChannelContent.ts requires a matching content/channels/<channel>/<tab>.md tab document to exist too, or CI's Contract verifiers job fails with 'references unknown tab'. Adding a new WonderLab-style tab means touching both files (the route mount AND the channel tab registration), not just the route mount + dashboardHelper.ts/lab-manager.vue wiring that satisfies the front-end nav. Caught by CI on first push, fixed in a follow-up commit -- next time check for a content/channels/<channelKey>/ directory before assuming a new channelKey/tabKey pair needs no separate registration.
- 2026-07-19 `art-generator-connect/t-020` — Rotation collision on a cross-repo task: claim_task.py closes the conductor-side claim race but not the target-repo one -- two sessions can land the identical claim_task.py claim commit in the same window and then independently finish the same kind_robots implementation before either opens a PR, surfacing only at merge time via a dirty mergeable_state. No rework was needed here since both diffs were functionally identical; a cheap second check (grep the target repo's recent PRs for the task id before opening a new one) would catch this earlier next time.
- 2026-07-19 `conductor/t-069` — Verify a new contract check both ways -- clean against the real repo (proves the prior fix holds) and against a deliberately reintroduced instance of the bug (proves the check actually catches it), not just the former. Also: a project-wide typecheck gate (vue-tsc) can fail a PR for a reason unrelated to its diff if main itself broke earlier the same day (here, PR #569); when that happens, fix the one-line pre-existing break inline and flag it transparently in the PR body rather than blocking the actual task on it or silently expanding scope.
- 2026-07-19 `art-generator-connect/t-020` — A type widened during an extraction refactor (ArtQueueEntry.variant: ArtVariant -> string, kind_robots PR #108) is easy to miss since call sites still typecheck fine with valid literals -- the fix is cheapest when the narrower union is defined in the module that owns the contract (artRequestYaml.ts) and the consumer imports it, rather than each side declaring its own copy that can silently drift apart again.
- 2026-07-19 `newsfeed/t-013` — Batch-verifying a source registry against a live pipeline surfaces real breakage fast (6/15 FEED_SOURCES were 404/403, none of it visible from reading the code) -- but finding a *replacement* URL needs the same discipline as sourcing a bias rating: test the candidate through the app's own parser (fetchSourceItems), not just an HTTP 200, before committing it, and leave genuinely unfindable replacements verified: false with an inline note of what was tried rather than swapping in an off-topic or wrong-entity feed just to clear the red X.
- 2026-07-19 `newsfeed/t-018` — Sourcing a real bias rating (vs. leaving unrated) is a fast WebSearch+WebFetch task once a project's guardrail doc (BIAS-CONTROLS.md) already specifies the required provenance shape -- checked Media Bias/Fact Check's own site directly (not just search snippets) to get the exact label wording, and confirmed absence-of-rating for the second source via a site-scoped search before concluding it should stay unrated rather than guessing a plausible-sounding label.
- 2026-07-19 `ai-art-academy/t-010` — Two independent sessions within the same hour (this one, and conductor/t-071's tooling build) both found t-010 stuck at status: claimed with its own note confirming the referenced kind_robots PR #544 had merged and it should rearm to ready -- and both initially deferred fixing it per AGENTS.md's rotation-collision caution, since the task looked like it might still be another session's in-flight work. A task claim that's confirmed complete by its own note but left untouched twice out of caution is itself a signal worth acting on the second time, not deferring a third: check whether real time has actually passed (claimed_at vs now) and whether the referenced PR's merge timestamp predates the current sweep by a wide margin before assuming a stale-looking claim is still live.
- 2026-07-19 `conductor/t-070` — A branch push can 413 even with a tiny diff and no local history rewrite -- this session's push failed twice, once because the session branch simply didn't exist on the actual GitHub remote yet (local remote-tracking ref showed a stale SHA, but `git ls-remote` showed nothing), and again after a squash-merge when a follow-up single-field status flip needed to reach main. Both resolved via CLAUDE.md's documented workarounds (`create_branch` for the first, `git_plumbing.commit_file_on_ref` direct to `refs/heads/main` for the second) rather than attempting to hand-transcribe a ~130KB roadmap.yaml into `push_files`, which would have risked silently corrupting the shared roadmap for every other concurrent agent. When a file is too large to safely retype, prefer a git-plumbing helper that reads the exact bytes from disk over any path that requires the content to pass through generated text.
- 2026-07-19 `newsfeed/t-014` — A prior session's own note ("could not verify locally, needs a real preview-deploy connector") is a precise handoff -- the Vercel MCP list_teams/list_projects/list_deployments/web_fetch_vercel_url chain in AGENTS.md answers it directly against the live production deployment without needing a new PR or any code change. Worth checking whether a 'ready' task is actually a pure-verification task before assuming every ready task implies a code diff.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-20T04:06:09Z_
