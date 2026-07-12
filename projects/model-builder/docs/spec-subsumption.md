# Model Builder — spec tasks subsumed by shipped code

The m1–m3 "write a spec doc" tasks were closed as **done by subsumption**: the
Model Builder was built directly, so the executable code + reference runs ARE the
specification. This maps each task to the artifact that satisfies it. (Same pattern
as the challenge-center t-003 close: verified-by-implementation.)

| Task | Original ask | Satisfied by (shipped) |
|---|---|---|
| **t-001** | SPEC.md — SourceModel/Recipe/BuildRun/Item/Artifact, the 4 stages, stale-invalidation, resume, DEFERRED/DRAFT_EARLY | `prisma/model-builder.prisma` (schema) + `stores/modelBuilderStore.ts` (stage/stale/resume logic) + `docs/persistence.md`, `docs/commit-executor.md` |
| **t-002** | API-INVENTORY.md — schema/routes/generation audit | `server/api/model-builder/*` (built against the audited routes) + `docs/commit-executor.md` (exact model fields/relations used) |
| **t-003** | RECIPES.md — model→recipe matrix + output catalog | `stores/helpers/modelBuilderRecipes.ts` (the executable catalog: source types, recipes, outputs, sizes, gates) |
| **t-004** | Durable BuildRun/Item/Artifact/Revision schema | **Shipped** — `prisma/model-builder.prisma` + migration + APIs (kind_robots #188) |
| **t-005** | Front-end source picker + gated progress matrix | **Shipped** — `components/model-builder/*` (kind_robots #184) |
| **t-006** | Normalized source adapters | **Shipped** — `SOURCE_TYPES` config + `adaptRun`/`adaptItem`/`sourceLabel` in the store |
| **t-007** | Marketing Deck recipe spec | `marketing-deck` recipe in the catalog + `reference-runs/hss-marketing-deck.md` (t-016) |
| **t-008** | Character Deck spec | `character-deck` recipe + `reference-runs/character-deck-amibot.md` (t-017) |
| **t-009** | Reward Deck spec (type-aware art, optional 3D) | `reward-deck` recipe in the catalog (fields/icon/card/hero/collection/3D-ref outputs). 3D/STL execution deferred (see below) |
| **t-010** | Art Upgrade recipe spec | `art-upgrade` recipe in the catalog |
| **t-011** | Relationship-expansion spec | `relationship-expansion` recipe + the CREATE+link executor + `reference-runs/dream-expansion-lantern-greenhouse.md` (t-018) |
| **t-012** | Comfy image/expression/video/3D orchestration | **Image + expression** wired (art generator reuse via the store; expression subset in t-017). **Video (LTX) and 3D (Hunyuan3D/STL) deferred** — always "separately selectable" per the brief; noted in the generate manifests |

## Explicitly still deferred (not claimed as done anywhere)

- **Video (LTX) generation** and **3D (Hunyuan3D → mesh QA → STL export → print-readiness)** — part of t-012's full scope; the recipes expose the outputs but the pipelines are not wired. Track as future work when needed.
- **t-022** — live smoke run against prod (generate + commit for real). Needs a human in the running app.

Everything else in milestones m1–m4 is shipped and deployed; m5 is done except the
live t-022 smoke.
