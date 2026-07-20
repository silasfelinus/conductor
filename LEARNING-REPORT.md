# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-20T09:19:25Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **310**
- Outcomes: blocked: 12, done: 298
- Success rate: **96%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 33 | 100% |
| alexa-integration | 2 | 100% |
| animation-manager | 8 | 100% |
| animation-studio | 1 | 100% |
| appmaker | 3 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 2 | 100% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 13 | 100% |
| conductor | 43 | 100% |
| digital-storefront | 12 | 100% |
| dream-cycle | 14 | 100% |
| ecosystem-map | 5 | 100% |
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
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 11 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 295 | 99% |

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

- 2026-07-20 `appmaker/t-006` — Before implementing a 'create the kind_robots Project for slug parity' task, run scripts/sync_projects.py live first -- it's idempotent and prints UNCHANGED (with a real field-by-field comparison, not just a slug match) when parity is already satisfied, which was the case here (id=24 already had conductorSlug=appmaker). Confirmed this session also has genuine KR_API_TOKEN + kind_robots API egress, unlike ai-art-academy's documented relay/museum-egress blocks -- worth checking live rather than assuming blocked.
- 2026-07-20 `ecosystem-map/t-006` — Before writing new implementation tasks off a stale audit doc, re-verify the audit's claims live against the target repo -- FRONTEND-SURFACE-MAP.md's 2026-07-10 snapshot of 15 missing/incomplete surfaces was 10 days out of date; checking kind_robots main's dashboardHelper.ts and content/*.md directly showed all 15 already had scaffold routes, and each project's own roadmap.yaml already carried the matching 'Polish and upgrade <Project> front-end surface' follow-up task (5 done, 10 ready). Filing new tasks from the doc's text alone would have created 15 duplicate entries forking the same work into two roadmap locations. Also: closing a project's last open task can flip it into ACTIVE_PROJECT_ALL_DONE/ACTIVE_PROJECT_NO_OPEN_TASKS in audit_roadmaps.py -- left project-overrides.yaml's status untouched since flipping active->finished/paused looks like a Silas-approval decision per that file's existing precedent comments, matching how humboldt-scoop already sits in the identical state unremediated.
- 2026-07-20 `storymaker/t-009` — A task that says 'add a section to the session data model doc (or a pointer in notes_from_silas)' should not assume the primary doc exists -- t-001's 'session data model' was approved via its roadmap note only, never written as a standalone doc file, so checking for the doc's actual existence before picking an implementation shape (rather than defaulting to the first-listed option) avoided inventing an unread new file. notes_from_silas is a good landing spot for cross-project boundary rules precisely because AGENTS.md's picking-order rules make every future session read it first.
- 2026-07-20 `animation-manager/t-012` — Burst-mode rotation picking superkate-hairstyle-ai/t-019 and model-builder/t-022, t-029, t-031 next in priority.yaml order all turned out to need a live deployed backend (a Tailscale ts.net Comfy box or an admin-only action) this sandbox can't reach -- confirmed via each task's own note/TALKBACK history before skipping rather than claiming and stalling. animation-manager/t-012 (a kaizen from t-005's review) was the first genuinely pure-code ready task further down the list. The fix itself was a clean first pass: extracted the WORKING-attempt-to-supersede lookup as a pure, testable helper (findAttemptToSupersede in animationComponentHelper.ts) instead of inlining the filter in the store action, matching the existing listAnimationAttempts/getLatestAnimationAttempt pattern and letting the new behavior be covered in the same DB-free verify script (verifyAnimationComponentAttempts.ts) rather than needing a Pinia-mocking store test that doesn't exist yet for this store.
- 2026-07-20 `conductor/t-072` — Kaizen tasks phrased as 'test the class of bug beyond this one call site' can tempt an overly broad heuristic (e.g. scanning every nullable Prisma Int field). Grepping for the actual naming convention first (existing<Owner>Id) found only the two call sites the bug's own history named, both already fixed -- confirming no second live instance existed kept the new static contract (verifyExistingOwnerIdNullability.ts) narrow and false-positive-free instead of flagging the ~100+ unrelated authenticatedUserId/callerUserId params that are genuinely non-nullable. Also hit a reusable snag: importing a route handler file (server/api/resources/[id].patch.ts) directly in a DB-free test throws at import time because it pulls in server/utils/prisma.ts, which requires DATABASE_URL synchronously -- extracting the pure helper into its own compatibility.ts module (mirroring characters/compatibility.ts) sidesteps this cleanly and is a reusable pattern for future DB-free behavioral tests.
- 2026-07-20 `animation-manager/t-005` — New route content mounts (content/<slug>.md with a channelKey/tabKey pair) aren't self-sufficient -- verifyChannelContent.ts requires a matching content/channels/<channel>/<tab>.md tab document to exist too, or CI's Contract verifiers job fails with 'references unknown tab'. Adding a new WonderLab-style tab means touching both files (the route mount AND the channel tab registration), not just the route mount + dashboardHelper.ts/lab-manager.vue wiring that satisfies the front-end nav. Caught by CI on first push, fixed in a follow-up commit -- next time check for a content/channels/<channelKey>/ directory before assuming a new channelKey/tabKey pair needs no separate registration.
- 2026-07-19 `art-generator-connect/t-020` — Rotation collision on a cross-repo task: claim_task.py closes the conductor-side claim race but not the target-repo one -- two sessions can land the identical claim_task.py claim commit in the same window and then independently finish the same kind_robots implementation before either opens a PR, surfacing only at merge time via a dirty mergeable_state. No rework was needed here since both diffs were functionally identical; a cheap second check (grep the target repo's recent PRs for the task id before opening a new one) would catch this earlier next time.
- 2026-07-19 `conductor/t-069` — Verify a new contract check both ways -- clean against the real repo (proves the prior fix holds) and against a deliberately reintroduced instance of the bug (proves the check actually catches it), not just the former. Also: a project-wide typecheck gate (vue-tsc) can fail a PR for a reason unrelated to its diff if main itself broke earlier the same day (here, PR #569); when that happens, fix the one-line pre-existing break inline and flag it transparently in the PR body rather than blocking the actual task on it or silently expanding scope.
- 2026-07-19 `art-generator-connect/t-020` — A type widened during an extraction refactor (ArtQueueEntry.variant: ArtVariant -> string, kind_robots PR #108) is easy to miss since call sites still typecheck fine with valid literals -- the fix is cheapest when the narrower union is defined in the module that owns the contract (artRequestYaml.ts) and the consumer imports it, rather than each side declaring its own copy that can silently drift apart again.
- 2026-07-19 `newsfeed/t-013` — Batch-verifying a source registry against a live pipeline surfaces real breakage fast (6/15 FEED_SOURCES were 404/403, none of it visible from reading the code) -- but finding a *replacement* URL needs the same discipline as sourcing a bias rating: test the candidate through the app's own parser (fetchSourceItems), not just an HTTP 200, before committing it, and leave genuinely unfindable replacements verified: false with an inline note of what was tried rather than swapping in an off-topic or wrong-entity feed just to clear the red X.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-20T09:19:25Z_
