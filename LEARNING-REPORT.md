# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-27T02:32:26Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1163**
- Outcomes: blocked: 19, cancelled: 2, done: 1142
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
| coloring-book | 39 | 100% |
| conductor | 137 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 51 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 29 | 100% |
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
| tzaddik-gallery | 5 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 1146 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 43 |
| transient | 18 |
| actionable | 17 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 47% success over 17 closed tasks; aim the next kaizen task here
- failure category `quality` — 43 occurrences; look for the shared cause across its records
- failure category `transient` — 18 occurrences; look for the shared cause across its records
- failure category `actionable` — 17 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-27 `tzaddik-gallery/t-005` — Completing t-021's deferred step (2) -- karmaRefTypes.ts + the access rule -- for a model with no userId/isPublic pair means a bespoke branch in every place the generic {userId, isPublic} select would otherwise run (assertReactionTargetAccessible, getContentOwnerId, canViewReactionsOn), mirroring the existing chatId special case rather than adding a naive entry to contentTargetModel/OWNED_TARGETS. Name the new KarmaRefType after the <target>Id column's prefix exactly (tzaddikCandidate, not the shorter tzaddik the reaction-category enum happens to use) so verifyEarnedKarmaWiring.ts's regex-derived name and verifyReactionTargetCoverage.ts's ${target}Id equality check both pass without a special-case exception.
- 2026-09-27 `tzaddik-gallery/t-021` — Adding a new reaction target to kind_robots is two separable steps, not one: (1) the enum value + Reaction.<target>Id column/FK/migration + getExpectedTargetField's total-Record entry, which can land now mapped to null, and (2) utils/karmaRefTypes.ts's KARMA_REF_TYPES/KARMA_REF_TARGET_COLUMNS entry, which verifyEarnedKarmaWiring.ts and verifyReactionTargetCoverage.ts correctly refuse until the target column is actually access-checked end to end (they require every listed ref type to already be fully wired, on purpose, per the FACET/PROJECT/CHALLENGE_SUBMISSION incidents those scripts cite). Landing (1) alone and leaving (2) for the task that actually builds the access rule is the documented pattern (COMPONENT is the precedent) -- do not add to karmaRefTypes.ts just because the enum value exists.
- 2026-09-27 `tzaddik-gallery/t-004` — A brand-new project's data model (t-003) existing with zero curated rows means the correct first pass on the next UI task is the plumbing (API + store + gallery wiring) verified via typecheck/contract tests, not a claim that the feature has been seen working against real data -- say which of those two you actually verified rather than blurring them. Also: reuse the shared kr-gallery shell directly from the page rather than adding a wrapper *-gallery.vue component when the page itself already carries the tab logic -- verifyRouteGalleryContract.ts's Rule 2 only requires the route's own mounted subtree to render kr-gallery, not a dedicated component file.
- 2026-09-26 `tzaddik-gallery/t-003` — A schema.prisma change without a committed `npx prisma generate` diff fails test:generated-client-parity every time and is a pure mechanical fix -- when retry_context names the exact expected file list, regenerating and verifying locally before re-pushing resolves it in one pass with no need to touch the schema. Also: closing a task to done with dependents whose depends_on is now satisfied requires re-running resolve_deps.py in the same close-out PR, or the audit CI check will refuse to merge ("resolver should promote this task to ready") -- close_task.py does not do this automatically.
- 2026-09-26 `humboldt-scoop-cms/t-043` — The quote form's poopstakes checkbox has no address field to key a 'household' on (quote_requests only carries city) -- a naive implementation of the task note's literal 'household key (the property address)' would have been unbuildable for the common case of a lead who hasn't signed up yet. Tiering the household key (customer's property address, else normalized phone, else email) and recording which tier was used per winner made the ambiguous spec buildable without guessing silently; when a task note names a data field that doesn't actually exist on the row it's describing, build a documented fallback rather than blocking on it.
- 2026-09-26 `ruler-hooked/t-043` — A worker/* branch can be fully implemented, correctly scoped, and even have its roadmap task set to status: review, and still never get a PR opened if create_pull_request fails mid-session -- check_pr_merged_drift.py's stranded-branch check caught it two sessions later. Before reimplementing any review/ready task, check for a matching worker/<project>-<task-id>-* branch first; if the diff is complete and scoped, open the PR from it as-is and run full CI rather than trusting the original session's local verification alone.
- 2026-09-26 `ruler-hooked/t-042` — Extending timingVisualFor()'s existing per-rarity Record pattern (bandColorClass, markerShape) to a third cue (zoneGlyphs) kept the single-source-of-truth property free -- reusing an established per-field Record<Rarity, T> shape, rather than inventing a new lookup mechanism, made the addition a small, low-risk diff and let the selftest assert the new field against the same rarity ladder the existing fields already used.
- 2026-09-26 `ruler-hooked/t-041` — The last open candidate from t-026/t-033's kaizen note (rarity-based marker shape/band color) landed as a single pure-function addition (timingVisualFor()) plus a component wiring change, with a selftest that explicitly proves the new visual lookup never perturbs resolveTimingStop()'s output -- when a display-only feature sits next to a determinism-critical pure function, assert the non-interference directly in the test rather than relying on code review alone to notice a stray shared-state touch.
- 2026-09-26 `ruler-hooked/t-040` — Continuing t-033's bounded-slice discipline: landed the Sunspoke Koi APPROACH-pause slice (kind_robots#3052) as a small, purely-display animation change (a brief dwell at each end of the timing-bar sweep, gated on family==PATIENCE && phase==APPROACH) and filed the one remaining candidate (rarity-based marker shape/band color) as a fresh task (t-041) rather than reopening this one -- confirming the same family/reversed-flag mutual-exclusivity check (grep the reducer for where the flag is set) before assuming two display-only effects can't collide is a cheap, worthwhile step whenever a kaizen note bundles multiple per-species visual candidates.
- 2026-09-26 `ruler-hooked/t-033` — A note that says 'once Silas has actually played the mechanic and there is real signal' is design guidance, not a hard gate -- the task was still status: ready with gate_human: false, and the three suggested candidates were concrete/specific enough to implement as small, independently reversible, bounded slices rather than waiting speculatively; land one slice per PR, not a combined diff.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-27T02:32:26Z_
