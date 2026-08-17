# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-17T10:47:38Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **645**
- Outcomes: blocked: 14, cancelled: 1, done: 630
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
| humboldt-scoop-cms | 5 | 100% |
| interface-vision | 83 | 100% |
| kapowarr | 16 | 100% |
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
| software | 629 | 99% |

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

- 2026-08-17 `humboldt-scoop-cms/t-014` — docs/CANONICAL-SOURCES.md had already resolved this task's central design question (independent admin/scooper capability flags, not a mutually-exclusive enum) before implementation started -- reading a cross-repo project's own design docs first can eliminate a design decision entirely rather than re-deriving it in-session.
- 2026-08-17 `storybook/t-010` — openStory()'s redundant-resume bug had already been partially fixed twice at individual call sites (mount, query watcher) before this cycle found a third unguarded caller (the active story's own 'Resume' button); guarding the shared choke-point function itself instead of each call site closes the bug class for every current and future caller in one fix.
- 2026-08-17 `text-generation/t-008` — Verifying an unrelated task's typecheck can surface pre-existing drift with a root cause several commits back: main's committed Prisma generated client was stale (missing the ProjectPageContent model that #1924 had already added to both the schema and two live API routes), breaking vue-tsc --noEmit for anyone who touched server/ code afterward. Isolated the two failures via git stash before assuming they were caused by this session's own edits, confirmed the fix (a plain prisma generate regeneration, purely additive) resolved them on its own, and shipped it as its own small standalone PR rather than folding an unrelated mechanical fix into t-008's diff. The kaizen itself (unifying the three-way-duplicated OpenAI/Anthropic auth-header dialect switch into textProviderService.ts's buildCloudProviderAuthHeaders) was low-risk and behavior-preserving by construction -- same header shapes/values for every caller -- which made full contract-test coverage of the new shared function (26 assertions) enough to merge with confidence, no live-provider smoke test needed for a refactor that touches no logic, only where code lives.

- 2026-08-17 `text-generation/t-004` — The three legacy chat streaming routes had already converged on a clean split between provider-agnostic mechanics (textProviderService.ts, from t-002) and provider-specific shape (endpoint URL, payload fields, auth). That split made the new unified endpoint mostly a matter of extracting the THIRD piece -- per-provider payload/response dialect -- into its own pure module (textGenerationDispatch.ts) rather than writing a new endpoint from scratch: one file that knows OpenAI/Anthropic/Ollama's three payload shapes and three response shapes, reused by a thin route. Provider selection from a resolved server's serverType (rather than a separate caller-supplied provider flag) turned out to be both simpler and more correct -- it can't drift from what the server actually is. One deliberate behavior improvement over the legacy routes: resolving the caller's preferredTextServerId/isDefault server even with no explicit serverId/serverName, instead of only ever falling back to the cloud default the way resolveOptionalTextServer does -- new endpoints are free to fix small inconsistencies like this that would be a breaking change on an existing route. No live OpenAI/Anthropic/Ollama API keys exist in this sandbox, so verification stayed at the same DB-free contract-test depth established by t-002/t-003/t-007 (34 synthetic-fixture checks covering every dispatch branch) rather than a live integration test the acceptance text technically asked for -- flagged explicitly for the reviewer/Silas rather than silently substituted.
- 2026-08-17 `text-generation/t-007` — A dashboard's default query scope can silently exclude an entire class of records even after the underlying data becomes real and resolvable -- server/api/server/uptime.get.ts hardcoded ['A1111','COMFY'] as its default serverType filter from when the panel was built for art/GPU servers only; once t-003 made OPENAI/ANTHROPIC/OLLAMA/CUSTOM genuinely resolvable text servers, they still had zero uptime/latency visibility because nothing in the UI ever surfaced the ?serverType= override that would have shown them. The fix pattern from t-003 (extract the array into a pure, exported, DB-free-testable function) generalized directly: server/utils/serverUptimeScope.ts's getUptimeDefaultServerTypes() mirrors serverCapabilities.ts's getCapabilityServerTypes() closely enough that the same contract-test shape (assert each type-family present/absent, assert no duplicates, assert the exact expected set) could be reused with only the type list changed.
- 2026-08-17 `text-generation/t-003` — getCapabilityServerTypes()'s 'text'/'chat' where-clause excluded OLLAMA even though server/api/chats/ollama/stream.post.ts's own request path already worked end-to-end -- the exclusion only broke server-side *resolution* (serverId/serverName/preferredTextServerId lookups), not the route itself, so a request that already had its target server object in hand would still succeed while every id/name/preference-based lookup silently failed to find that same Ollama server. A route working in isolation is not evidence its resolver path works too when they're separate code paths sharing only a where-clause. Most of t-003's stated acceptance criteria (health/test operation, preferredTextServerId selection UI, explicit-server-add form) were already built by earlier server-selector/serverStore work -- reading the actual UI and API surface before assuming a gap existed narrowed the real fix to one array literal plus its missing test coverage, rather than re-implementing already-working infrastructure.
- 2026-08-17 `text-generation/t-002` — Extracting shared mechanics into a new server/utils/*.ts file risks a silent Nuxt auto-import name collision when the new file's export name happens to match an existing server/utils export -- nuxi prepare only WARNs ('Duplicated imports... ignored'), it does not fail the build, so a colliding helper name can quietly shadow (or be shadowed by) an unrelated existing function with different behavior. Ran into this for real: the shared module's first draft named its Server-auth-header builder `buildServerAuthHeaders`, identical to an existing, differently-shaped helper in serverApi.ts (Content-Type vs Accept header contract) used by two other call sites. Caught by actually running `nuxi prepare` locally and reading its warnings, not by vue-tsc/eslint (neither flags this). Renamed to a distinct name rather than merging the two behaviors, to keep the migration's 'no observable behavior change' guarantee intact. Also: a shared module that mixes pure helpers with one Prisma-touching function (via a static import chain through serverResolver.ts -> prisma.ts) will make an otherwise-DB-free self-test require DATABASE_URL just by importing the file -- dynamic-importing the Prisma-touching piece inside its own function body keeps the rest of the module importable standalone, which mattered here because contract-tests.yml is explicitly documented as a DB-free workflow.
- 2026-08-17 `text-generation/t-001` — The roadmap note assumed the private-server path was mostly unbuilt; a full read of server/api/chats/{openai,anthropic,ollama}/stream.post.ts, serverResolver.ts, and the Server Prisma model showed the opposite -- a working native Ollama route, full server CRUD/health infrastructure, and consistent mana gating already exist. The real gaps were narrower and more specific: serverResolver.ts's capabilityWhere('text') silently excludes OLLAMA from type-based resolution, three near-identical chat routes each duplicate a private cost estimator that has drifted from an already-correct shared estimateTextCostUsd (which also correctly multiplies by n, unlike the OpenAI route's local copy), and there is zero AbortController/cancellation wiring anywhere in the stack (server or chatStore.ts). Treating 'map the existing code' as a literal instruction rather than a formality caught a concrete, fixable billing-undercount bug (uncounted n) and a routing gap (Ollama) that a memory-based/greenfield-assuming brief would have missed or re-invented differently.
- 2026-08-16 `alexa-integration/t-021` — t-020's own kaizen note named a plausible-sounding follow-up scope (audit the 'unknown theme'/'no match' error branches) that turned out, on a fresh read, to already be functionally correct -- both branches already had the early return / proper if-else split needed to avoid a false-success ack. The real gap was regression coverage, not a bug: nothing protected those two branches from a future edit quietly dropping the early return, the lastError/pushLocalMessage report, or the postAck() success-only gating, which is exactly the false-success shape t-015/t-020 fixed for the action-mismatch case. Extended the existing checkSerendipityVoiceActionGuard.ts file with a second exported check (index-based anchor comparisons rather than full brace-parsing) instead of adding a fourth guard file, per the task note's own preference -- kept the fix inside the file whose npm script/CI step already covered it, so no workflow-file change was needed.
- 2026-08-16 `alexa-integration/t-020` — The target/action-mismatch bug class from t-015 (a shared VoiceBusCommand.action union reaching a dispatch branch where most of its values are meaningless) generalized cleanly to the other two targets once actually re-read fresh: applyThemeCommand() and applyArtCommand() never checked command.action at all, an omission invisible unless you specifically compare each dispatch function against its siblings for the same missing guard shape. Extending the existing guard into a TARGET_FUNCTIONS structure (mirroring modelBuilderStore.ts's own multi-function guard convention) kept the fix in one file instead of three near-duplicates.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-17T10:47:38Z_
