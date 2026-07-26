# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-26T06:04:32Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **348**
- Outcomes: blocked: 12, cancelled: 1, done: 335
- Success rate: **96%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 38 | 100% |
| alexa-integration | 2 | 100% |
| animation-manager | 10 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 5 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 14 | 100% |
| conductor | 47 | 100% |
| conductor-app | 2 | 100% |
| davinci | 1 | 100% |
| digital-storefront | 13 | 100% |
| dream-cycle | 14 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 1 | 100% |
| kind-robots | 36 | 97% |
| kindrobots-unraid | 4 | 100% |
| media-watchlist | 4 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 31 | 100% |
| mural-design | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 333 | 99% |

## Failure categories

| Category | Count |
|---|---|
| actionable | 7 |
| quality | 6 |
| transient | 5 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `actionable` — 7 occurrences; look for the shared cause across its records
- failure category `quality` — 6 occurrences; look for the shared cause across its records
- failure category `transient` — 5 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-07-26 `ai-art-academy/t-038` — When the priority-order top task (t-004) is genuinely operationally blocked and has already been rechecked twice the same day per its own note, the right move is to pick a different ready task within the same top-priority project rather than re-checking the blocker a third time or dropping to a lower-priority project. t-038 (extract a reusable inspiration-set template from an existing hand-rolled example) had no dependency on the live render backend, so it was a clean, fast, fully-verifiable-locally pick. Docs-only PR, all CI green (conductor PR #1100), merged same cycle.
- 2026-07-26 `kind-robots/t-047` — Additive migrations that ship with an already-identified real consumer (the approved pitch named digital-storefront's swag-rail query as the next task) review fast because the diff never has to justify itself speculatively -- ADD COLUMN + CREATE INDEX only, no seed/UI. Separately: a CI check (facet-catalog) hung indefinitely on 'Install dependencies' after a rebase and cancel_workflow_run didn't unstick it; pushing a trivial empty commit to force a fresh check run against a new head SHA resolved it in the normal ~90s, faster than waiting out or repeatedly cancelling the stuck run.
- 2026-07-26 `digital-storefront/t-027` — Weekly site-audit findings can go stale within days when the audited code keeps moving -- STORE-AUDIT.md described social-publisher.vue as the giftshop's most mature wired piece, but it was removed (migration 20260718200000_remove_social_publishing) three days after the audit date. A generated audit document isn't self-updating like STATUS.md; treat its findings as dated snapshots and re-verify against the current checkout (Glob for the file/model) before relying on an audit claim that's more than a few days old, especially for a fast-moving surface.
- 2026-07-26 `kind-robots/t-045` — Adding a NOT NULL/required column to a widely-selected Prisma model (Resource) breaks every narrower Prisma `select` object's derived type that a full-model-typed helper function consumes -- here resourceGallerySelect vs. checkpointScore(checkpoint: Resource, ...) in generate-preview.post.ts. A full vue-tsc/tsc run is the only reliable way to find every such break; grepping for the model name alone would have missed it. Also: this sandbox has no reachable DB, so any migration+seed-script task's live-data verification has to stop at typecheck/lint/a synthetic smoke test of the pure logic -- flag that gap explicitly in TALKBACK rather than claiming full verification.
- 2026-07-26 `kind-robots/t-048` — A prior PR's 'zero callers' claim about a Vue component (art-manager.vue) was wrong because its grep only checked pages/ and components/, missing Nuxt Content .md files that embed components via MDC syntax (:component-name). Caught before implementation by re-grepping content/**/*.md as well. When trusting a 'this component/route is dead' claim before deleting or gating something, check content/**/*.md (or any CMS/markdown layer that can reference components) in addition to the usual source directories.
- 2026-07-26 `kind-robots/t-044` — The Grant-model PR scoped itself tightly to exactly the pitch's first-task section (additive CREATE TABLE + 2 FKs, no route rewiring) and it paid off in review speed -- the migration.sql was auditable line-by-line in seconds (1 CREATE TABLE, 2 ADD CONSTRAINT, nothing else) precisely because nothing else was mixed into the diff. New authz helper (contentAccess.ts) shipped unwired on purpose, which kept the PR reviewable without needing to trace every call site it would eventually gate.
- 2026-07-26 `kind-robots/t-046` — When a feature appears missing, verify reachability before rebuilding it: video-generator.vue was already complete, but its only prior route lived behind dead dashboard configuration and an unwired manager component.
- 2026-07-26 `ai-art-academy/t-037` — Kontext's buildKontextWorkflow lacked a LoraLoaderModelOnly node despite two sibling workflow builders (simpleCheckpointWorkflow.ts, imageToVideoWorkflow.ts) already using that exact pattern -- when adding a new generation route, check whether an existing sibling route already solved the same wiring problem before assuming a field like loraPath reaching enqueue.post.ts as provenance metadata means it also reaches the render graph.
- 2026-07-25 `model-builder/t-022` — The model-builder COMMIT executor's CREATE/ASSET_ONLY/idempotency paths (PR #190) had zero non-CI coverage (no test file, no live smoke) despite already backing gated reference runs t-016/t-017/t-018 -- a live prod round-trip (throwaway private/inactive Dream + Characters, cleaned up via DELETE after verification) was the only way to prove the idempotencyKey claim-then-write pattern and the isPublic/isActive=false override actually hold outside a type-checker. Also: GET /api/characters ignores a `?id=` query string and silently returns the unfiltered list -- the working per-id lookup is the path-param route GET /api/characters/{id}; worth knowing before the next live-smoke task on this surface.
- 2026-07-25 `animation-manager/t-014` — Existing invariant-verifier scripts need explicit CI wiring or real regressions can remain invisible until a developer happens to run them locally.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-26T06:04:32Z_
