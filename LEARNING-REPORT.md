# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-27T11:01:16Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1168**
- Outcomes: blocked: 19, cancelled: 2, done: 1147
- Success rate: **98%**
- Average passes on successful tasks: **0.3**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 73 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 20 | 95% |
| animation-studio | 2 | 50% |
| appmaker | 11 | 100% |
| approval-portal | 2 | 0% |
| art-archive | 34 | 100% |
| art-generator-connect | 3 | 100% |
| brainstorm | 26 | 96% |
| butterfly-gallery | 32 | 94% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 42 | 100% |
| conductor | 137 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 51 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 30 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 22 | 95% |
| interface-vision | 140 | 100% |
| kapowarr | 52 | 100% |
| kind-economy | 11 | 100% |
| kind-robots | 73 | 99% |
| kindrobots-unraid | 9 | 100% |
| lora-ingestion | 11 | 100% |
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
| ruler-hooked | 28 | 100% |
| scene-animator | 2 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 44 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 7 | 100% |
| tzaddik-gallery | 6 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 1151 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 46 |
| transient | 18 |
| actionable | 17 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 47% success over 17 closed tasks; aim the next kaizen task here
- failure category `quality` — 46 occurrences; look for the shared cause across its records
- failure category `transient` — 18 occurrences; look for the shared cause across its records
- failure category `actionable` — 17 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-27 `coloring-book/t-049` — A kaizen task that names the exact race (two manage_coloring_book_production.py invocations racing on different proposal ids in the same shared color-art-jobs.yaml) and the smallest of three explicit fix options (a lockfile held for the whole live run, vs. narrowing the write path, vs. a docstring warning) is landable in one pass: an exclusive non-blocking flock on a sibling .lock file, held from load through every write, makes a racing second invocation fail fast with a clear error instead of silently reverting the first's already-persisted state. Verified with a real cross-process test (not just an in-process mock) since flock semantics depend on separate open-file-descriptions, which a same-process double-open can get subtly wrong. Filed t-052 to narrow the write path itself (read-modify-write only the touched entry) as a follow-on if whole-file rewrites become a real cost -- deliberately deferred rather than bundled, per the original note's own preference for the smallest safe fix.
- 2026-09-27 `tzaddik-gallery/t-022` — A kaizen task naming an exact file, function, and the mechanical reason ESLint double-flagged it (disable comment landing above a multi-line type instead of the line the `any` actually appears on) is landable in one pass with zero ambiguity: narrowing the map's `findUnique` argument type to the shape every call site actually passes removed the `any` outright, so no disable comment was needed at all. Confirmed via eslint (clean), vue-tsc --noEmit (clean), and test:lint-ratchet (-3 problems vs. baseline).
- 2026-09-27 `coloring-book/t-022` — A script that loads a shared YAML file once per process and writes the whole in-memory snapshot back at several points during its run is unsafe to invoke concurrently, even across entries the two invocations don't logically share -- the slower process's later write is based on a pre-change snapshot and silently reverts the faster process's already-persisted progress with no error. Reproduced live running manage_coloring_book_production.py's generate-bw for two different book/proposal ids at once: the first to finish had its bw_status: done reverted back to running by the second process's later write. Recovered safely only because the render and server-side ArtImage survived independently of the YAML bookkeeping and the enqueue step was idempotent against an existing job id -- a less careful recovery could have double-submitted a render job. Filed coloring-book/t-049 to fix the script; the immediate mitigation is to never run two invocations against the same shared state file in parallel, regardless of how independent their target keys look.
- 2026-09-27 `coloring-book/t-039` — When a fix's own task has already been closed prematurely twice on indirect evidence (a merged PR, a plausible diagnosis), closing it a third time needs a direct check of the actual deployed artifact, not the passage of time since merge: inspect the specific field the bug lived in (here, GET /api/art/queue/:id's stored workflow graph's UNETLoader checkpoint name) before spending a render cycle assuming a Force Update happened. Then verify the render's actual pixels, not just its mechanical pass/fail, before trusting the fix -- a mechanical rejection on a DIFFERENT input during the same verification pass (kind-robots kr-001) turned out to be an unrelated false positive in the quality gate itself, not evidence the fix was incomplete; reading the rejected file directly (not just its stats) was what told the two apart.
- 2026-09-27 `dream-cycle/t-006` — A workflow-step rename (changing a GitHub Actions step name, an ::warning:: message, or an error string a contract test greps for verbatim) is a repo-wide rename, not a local edit -- grep the whole tests/ tree for the exact old string before renaming, not just the test file you already know references it. Caught here as a Reviewer catch (not a Worker rejection) on silasfelinus/conductor#5264, which renamed several daily-digest.yml step names for the one-day render-runway fix but left 4 pre-existing tests hardcoding the old names, failing both the Python test suite and the dream-cycle contract CI job.
- 2026-09-27 `tzaddik-gallery/t-005` — Completing t-021's deferred step (2) -- karmaRefTypes.ts + the access rule -- for a model with no userId/isPublic pair means a bespoke branch in every place the generic {userId, isPublic} select would otherwise run (assertReactionTargetAccessible, getContentOwnerId, canViewReactionsOn), mirroring the existing chatId special case rather than adding a naive entry to contentTargetModel/OWNED_TARGETS. Name the new KarmaRefType after the <target>Id column's prefix exactly (tzaddikCandidate, not the shorter tzaddik the reaction-category enum happens to use) so verifyEarnedKarmaWiring.ts's regex-derived name and verifyReactionTargetCoverage.ts's ${target}Id equality check both pass without a special-case exception.
- 2026-09-27 `tzaddik-gallery/t-021` — Adding a new reaction target to kind_robots is two separable steps, not one: (1) the enum value + Reaction.<target>Id column/FK/migration + getExpectedTargetField's total-Record entry, which can land now mapped to null, and (2) utils/karmaRefTypes.ts's KARMA_REF_TYPES/KARMA_REF_TARGET_COLUMNS entry, which verifyEarnedKarmaWiring.ts and verifyReactionTargetCoverage.ts correctly refuse until the target column is actually access-checked end to end (they require every listed ref type to already be fully wired, on purpose, per the FACET/PROJECT/CHALLENGE_SUBMISSION incidents those scripts cite). Landing (1) alone and leaving (2) for the task that actually builds the access rule is the documented pattern (COMPONENT is the precedent) -- do not add to karmaRefTypes.ts just because the enum value exists.
- 2026-09-27 `tzaddik-gallery/t-004` — A brand-new project's data model (t-003) existing with zero curated rows means the correct first pass on the next UI task is the plumbing (API + store + gallery wiring) verified via typecheck/contract tests, not a claim that the feature has been seen working against real data -- say which of those two you actually verified rather than blurring them. Also: reuse the shared kr-gallery shell directly from the page rather than adding a wrapper *-gallery.vue component when the page itself already carries the tab logic -- verifyRouteGalleryContract.ts's Rule 2 only requires the route's own mounted subtree to render kr-gallery, not a dedicated component file.
- 2026-09-26 `tzaddik-gallery/t-003` — A schema.prisma change without a committed `npx prisma generate` diff fails test:generated-client-parity every time and is a pure mechanical fix -- when retry_context names the exact expected file list, regenerating and verifying locally before re-pushing resolves it in one pass with no need to touch the schema. Also: closing a task to done with dependents whose depends_on is now satisfied requires re-running resolve_deps.py in the same close-out PR, or the audit CI check will refuse to merge ("resolver should promote this task to ready") -- close_task.py does not do this automatically.
- 2026-09-26 `humboldt-scoop-cms/t-043` — The quote form's poopstakes checkbox has no address field to key a 'household' on (quote_requests only carries city) -- a naive implementation of the task note's literal 'household key (the property address)' would have been unbuildable for the common case of a lead who hasn't signed up yet. Tiering the household key (customer's property address, else normalized phone, else email) and recording which tier was used per winner made the ambiguous spec buildable without guessing silently; when a task note names a data field that doesn't actually exist on the row it's describing, build a documented fallback rather than blocking on it.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-27T11:01:16Z_
