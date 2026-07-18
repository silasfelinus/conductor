# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-18T19:04:46Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **270**
- Outcomes: blocked: 12, done: 258
- Success rate: **96%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 28 | 100% |
| alexa-integration | 2 | 100% |
| animation-manager | 5 | 100% |
| animation-studio | 1 | 100% |
| appmaker | 2 | 100% |
| approval-portal | 2 | 0% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 13 | 100% |
| conductor | 37 | 100% |
| digital-storefront | 12 | 100% |
| dream-cycle | 14 | 100% |
| ecosystem-map | 4 | 100% |
| global-ui | 11 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 1 | 100% |
| kind-robots | 28 | 96% |
| kindrobots-unraid | 4 | 100% |
| media-watchlist | 1 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 28 | 100% |
| mural-design | 1 | 100% |
| newsfeed | 7 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 2 | 100% |
| serendipity | 1 | 100% |
| superkate-hairstyle-ai | 16 | 100% |
| superkate-services-calculator | 11 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 255 | 99% |

## Failure categories

| Category | Count |
|---|---|
| actionable | 6 |
| quality | 5 |
| transient | 1 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `actionable` — 6 occurrences; look for the shared cause across its records
- failure category `quality` — 5 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-07-18 `kind-robots/t-039` — Pinning localeCompare(..., 'en') in create-component-json.mjs's three sort call sites made the generated manifest deterministic across Node/ICU builds. When a kaizen note bundles a determinism fix with a separate drift-correction (here: missing components in the committed file), keep the diff scoped to just the fix and file the drift correction as its own ready task (kind-robots/t-040) rather than expanding the PR.
- 2026-07-18 `newsfeed/t-009` — Stale-source tolerance (last-known-good cache per source, bounded to 24h, flagged stale: true) was the one real gap left after t-005/t-006 shipped bounded caching, stable identity, dedup, and partial-success -- verified with a local http.createServer fixture (serves once, then closes) instead of relying on live network egress to prove the fallback path.
- 2026-07-18 `conductor/t-064` — set_task_field.py silently flattened hand-maintained note: |- block-literal scalars to a single quoted line on any edit -- fixed by detecting the existing block style and re-emitting new multiline values in the same style. A kaizen note that specifies the exact fix shape, the regression test to add, and a safe interim workaround (here: use Edit directly for block-literal notes) turns a same-day implementable fix instead of requiring rediscovery.
- 2026-07-18 `newsfeed/t-006` — Regenerating public/components.json via its own generator script (utils/scripts/create-component-json.mjs, run implicitly by nuxi prepare) in this sandbox reorders unrelated existing entries and adds real components missing from the committed file -- looks like environment-dependent Array.sort/localeCompare collation, or the committed file has just drifted. Hand-patching only the new folder entries kept the diff scoped; worth a follow-up task to make the generator's sort collation-stable (e.g. explicit localeCompare(b, 'en') or plain codepoint compare) so future sessions don't have to work around it.
- 2026-07-18 `newsfeed/t-006` — Reusing one feed-rendering component (NewsfeedFeed) in both the live homepage and the project pitch page's #interactive slot avoided duplicating feed logic across two surfaces -- when a project has both a real feature and a separate pitch/status page, slot the real component into the pitch page rather than keeping them as two independent implementations.
- 2026-07-18 `kind-robots/t-038` — Deleting a stale one-shot workflow file that references a since-merged branch/script cleared a required 'Contract verifiers' CI check that was red on every kind_robots PR regardless of diff -- worth grepping for other one-shot workflows with a 'delete after X lands' trailing comment where X has already landed, since they silently keep failing verifyWorkflowPaths.ts forever otherwise.
- 2026-07-18 `newsfeed/t-005` — The task note pointed at prs.get.ts's raw-array response shape as the model to follow, but that's a rare conductor-only outlier -- 110+ of this repo's other GET routes use a {success,message,data}+errorHandler convention instead. When a task note says 'model X on Y's shape,' check how common Y's specific pattern actually is across the codebase before copying it verbatim; the intended lesson (thin handler + shared util split, introduce caching) can be separable from the literal response contract.
- 2026-07-18 `digital-storefront/t-017` — A design-only task (no PR, per BOUNDARY.md) with follow-on tasks already filed (t-026, kind-robots/t-037) still needs an explicit status: done close -- the design doc landing on main and the follow-ons existing isn't itself a completion signal a later session will notice without checking. Same pattern as global-ui/t-025 this cycle: two independent status: review tasks both had their actual output already merged/landed, just missing the roadmap close.
- 2026-07-18 `global-ui/t-025` — kind_robots PR #420 merged cleanly (option (a): migrate both shadow-variant panels onto kr-panel/kr-panel-muted with the shadow layered as a template utility override) but the roadmap task sat at status: review for several hours/cycles with no session flipping it to done -- closing a task the Worker/Reviewer already merged is easy to defer past the same session. Check pull_request_read on any status: review task's referenced PR before picking new work; a merged PR with no roadmap follow-through is a same-session-fixable gap, not a needs-human one.
- 2026-07-18 `ai-art-academy/t-032` — art-styler.vue's generated emit carried only the result image, not which style produced it, so the consumer had to re-read current store state to attribute a completed generation -- exactly the kind of async gap where a mid-flight selection change mis-attributes the result. When an event fires after an awaited async call, pass the value that was true at request-start through the event payload itself rather than letting the consumer re-read live state after the fact.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-18T19:04:46Z_
