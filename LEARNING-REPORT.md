# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-10T12:50:45Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **570**
- Outcomes: blocked: 13, cancelled: 1, done: 556
- Success rate: **98%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 64 | 98% |
| alexa-integration | 2 | 100% |
| animation-manager | 13 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 6 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| brainstorm | 9 | 100% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 25 | 100% |
| conductor | 70 | 100% |
| conductor-app | 2 | 100% |
| davinci | 2 | 100% |
| digital-storefront | 28 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 4 | 100% |
| interface-vision | 82 | 100% |
| kind-robots | 49 | 98% |
| kindrobots-unraid | 5 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 49 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 1 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 2 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 555 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 12 |
| actionable | 9 |
| transient | 9 |
| scope | 2 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `quality` — 12 occurrences; look for the shared cause across its records
- failure category `actionable` — 9 occurrences; look for the shared cause across its records
- failure category `transient` — 9 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-10 `brainstorm/t-010` — A creative workspace deserves its own persistence semantics when existing models encode different domains; keep local draft continuity automatic, make durable account saves explicit/private, and validate a full candidate/revision/branch snapshot round-trip before trusting the schema.
- 2026-08-10 `brainstorm/t-009` — Creative lineage needs immutable snapshots of the exact parent revision; a live parentId alone can rewrite history after later edits. Restoring old creative work should append history rather than erase newer revisions.
- 2026-08-10 `brainstorm/t-008` — Creative response weighting is clearer as exact human-readable counts plus Auto/wildcard slots than percentage model knobs; enforce the requested mix in structured output and validation, not only prompt prose.
- 2026-08-10 `brainstorm/t-007` — After a rejected UI retry, review the current head and current check runs rather than treating an earlier red diagnostic as permanent; require the concrete regression fixture and completed green checks before merge.
- 2026-08-10 `model-builder/t-029` — autoBuildItem()'s FIELDS_AND_PROMPTS branch drafted artPrompt unconditionally instead of only when empty, unlike its own PITCH branch -- the ~33rd cycle of this recurring read-through task, still finding new instances of "review/intent gate enforced in one branch but not its sibling." Worth checking sibling branches of any stage-gating conditional whenever one gets a fix, not just the branch that was reported.
- 2026-08-10 `brainstorm/t-006` — The current text stack has multiple useful abstractions but no single provider layer covers every Kind Robots text server: generic textServer assumes OpenAI-style requests while Suggest explicitly handles Anthropic/Ollama/compatible servers. Brainstorm therefore resolves the canonical Server row first, then uses the provider-specific caller while keeping one validated candidate envelope. Never forward first-party provider credentials to arbitrary compatible URLs.
- 2026-08-10 `brainstorm/t-005` — Treat a generated batch as durable creative working state, not one disposable response. Keeping batch identity and candidate lineage in the client contract now gives later history, persistence, art, and object-context work stable seams without forcing provider or Dream semantics into Brainstorm state.
- 2026-08-10 `brainstorm/t-004` — Shared MDC-mounted workbench components cannot choose column counts from viewport breakpoints. Brainstorm must remain container-responsive because it can live inside different navigation shells and panes; use intrinsic auto-fit/minmax or current kr layout primitives instead.
- 2026-08-10 `brainstorm/t-003` — The June Dream workaround preserved useful UI ideas but discarded structure twice: the endpoint returns structured candidates, dreamStore normalizes them to prose, and the Vue component reparses prose into candidates. Restoring Brainstorm should keep structured candidate data end-to-end and reuse the current active text-server/provider and mana plumbing instead of inheriting that compatibility loop.
- 2026-08-10 `brainstorm/t-002` — Legacy product restoration should trace the latest coherent live behavior and the migration that removed it before resurrecting old code. Brainstorm survived into June 2026 and was lost specifically because the Pitch domain was removed into Dream; its UX can be revived without reversing that data-model migration.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-10T12:50:45Z_
