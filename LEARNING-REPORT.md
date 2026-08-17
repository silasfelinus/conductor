# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-17T14:29:05Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **651**
- Outcomes: blocked: 14, cancelled: 1, done: 636
- Success rate: **98%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 64 | 98% |
| alexa-integration | 5 | 100% |
| animation-manager | 13 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 7 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| brainstorm | 12 | 92% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 25 | 100% |
| conductor | 76 | 100% |
| conductor-app | 4 | 100% |
| davinci | 4 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 10 | 100% |
| interface-vision | 83 | 100% |
| kapowarr | 17 | 100% |
| kind-robots | 50 | 98% |
| kindrobots-unraid | 5 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 68 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 12 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 6 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 16 | 44% |
| software | 635 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 13 |
| actionable | 9 |
| transient | 9 |
| scope | 2 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 13 occurrences; look for the shared cause across its records
- failure category `actionable` — 9 occurrences; look for the shared cause across its records
- failure category `transient` — 9 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-17 `kapowarr/t-007` — A prior design doc's 'confirmed by reading the template' claims are worth re-verifying, not just citing: tracing the actual settings-UI JS and API routes (not just the doc's summary) confirmed the client-type registry really was UI-driven with zero extra work needed, while the doc's separate 'update_status() needs zero changes' claim for the polling loop turned out to be wrong once the actual seeding_handling branch was read -- both a positive and negative case for the same 'verify, don't just cite' discipline in one task.
- 2026-08-17 `humboldt-scoop-cms/t-018` — A task note flagging 'this is more than a missing UI -- a permission check is written and called by nothing' was the real scope, not a footnote: shipping the CRUD UI alone would have handed out a can_request_changes grant the code still couldn't honour. Tracing the unused permission check to its actual enforcement point (change_request handling, keyed by WP user id) surfaced a real second gap -- rendering the form for a target account with no linked WP user id would have aggregated change-request history across unrelated no-account customers -- that a UI-only reading of the task would have missed entirely.
- 2026-08-17 `humboldt-scoop-cms/t-017` — For a schema-changing PR, the Reviewer's line-by-line migration audit is a real second check, not a formality -- reading class-hss-db.php's dbDelta diff directly (not just trusting the PR body's 'additive-only' claim) is what actually confirms no DROP/rewrite snuck in.
- 2026-08-17 `humboldt-scoop-cms/t-016` — A task named as a three-way unification (admin/dispatch/scooper) turned out, on actual survey, to need only a narrower slice -- two of the three surfaces were already correctly capability-gated from prior tasks. Surveying real current state before designing avoided rebuilding what already worked and kept the landed diff small and reviewable.
- 2026-08-17 `humboldt-scoop-cms/t-020` — A background survey of actual current write paths (not the task note's assumed shape) found the real address-edit flow was customer-portal-only with a duplicated, incomplete (address/city only, missing state/postal_code) safety check -- surveying before designing caught a real bug the task wouldn't otherwise have surfaced.
- 2026-08-17 `humboldt-scoop-cms/t-015` — server.ts's top-level side effects (opens a DB pool, starts listening) make it unimportable from a test -- pulling authorization logic into pure, side-effect-free modules (scopeVisits.ts) before wiring it into the entrypoint is what made 'test privilege boundaries' actually achievable rather than aspirational.
- 2026-08-17 `humboldt-scoop-cms/t-014` — docs/CANONICAL-SOURCES.md had already resolved this task's central design question (independent admin/scooper capability flags, not a mutually-exclusive enum) before implementation started -- reading a cross-repo project's own design docs first can eliminate a design decision entirely rather than re-deriving it in-session.
- 2026-08-17 `storybook/t-010` — openStory()'s redundant-resume bug had already been partially fixed twice at individual call sites (mount, query watcher) before this cycle found a third unguarded caller (the active story's own 'Resume' button); guarding the shared choke-point function itself instead of each call site closes the bug class for every current and future caller in one fix.
- 2026-08-17 `text-generation/t-008` — Verifying an unrelated task's typecheck can surface pre-existing drift with a root cause several commits back: main's committed Prisma generated client was stale (missing the ProjectPageContent model that #1924 had already added to both the schema and two live API routes), breaking vue-tsc --noEmit for anyone who touched server/ code afterward. Isolated the two failures via git stash before assuming they were caused by this session's own edits, confirmed the fix (a plain prisma generate regeneration, purely additive) resolved them on its own, and shipped it as its own small standalone PR rather than folding an unrelated mechanical fix into t-008's diff. The kaizen itself (unifying the three-way-duplicated OpenAI/Anthropic auth-header dialect switch into textProviderService.ts's buildCloudProviderAuthHeaders) was low-risk and behavior-preserving by construction -- same header shapes/values for every caller -- which made full contract-test coverage of the new shared function (26 assertions) enough to merge with confidence, no live-provider smoke test needed for a refactor that touches no logic, only where code lives.

- 2026-08-17 `text-generation/t-004` — The three legacy chat streaming routes had already converged on a clean split between provider-agnostic mechanics (textProviderService.ts, from t-002) and provider-specific shape (endpoint URL, payload fields, auth). That split made the new unified endpoint mostly a matter of extracting the THIRD piece -- per-provider payload/response dialect -- into its own pure module (textGenerationDispatch.ts) rather than writing a new endpoint from scratch: one file that knows OpenAI/Anthropic/Ollama's three payload shapes and three response shapes, reused by a thin route. Provider selection from a resolved server's serverType (rather than a separate caller-supplied provider flag) turned out to be both simpler and more correct -- it can't drift from what the server actually is. One deliberate behavior improvement over the legacy routes: resolving the caller's preferredTextServerId/isDefault server even with no explicit serverId/serverName, instead of only ever falling back to the cloud default the way resolveOptionalTextServer does -- new endpoints are free to fix small inconsistencies like this that would be a breaking change on an existing route. No live OpenAI/Anthropic/Ollama API keys exist in this sandbox, so verification stayed at the same DB-free contract-test depth established by t-002/t-003/t-007 (34 synthetic-fixture checks covering every dispatch branch) rather than a live integration test the acceptance text technically asked for -- flagged explicitly for the reviewer/Silas rather than silently substituted.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-17T14:29:05Z_
