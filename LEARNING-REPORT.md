# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-12T20:38:00Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **16**
- Outcomes: done: 16
- Success rate: **100%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| challenge-center | 2 | 100% |
| conductor | 2 | 100% |
| model-builder | 12 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 3 | 100% |
| software | 13 | 100% |

## Failure categories

_No failures recorded yet._

## Kaizen targets

_No systematic weaknesses above thresholds. Kaizen freely._

## Recent lessons

- 2026-07-12 `challenge-center/t-004` — Seed scripts that default to a validation-only dry run (schema field/enum shape checked in-process, no DATABASE_URL required) let a credential-free agent runtime still ship and merge a fully verifiable data-catalog change; the live --write step is then a separate, explicit, human/DB-having action. kind_robots PR #199, conductor handoff PR #440.
- 2026-07-12 `model-builder/t-026` — Minimal-interaction 'just create it' is cheap once the gated actions exist: autoBuildItem/autoBuildRun just chain the existing draft -> approve -> generate -> commit actions with defaults, and an includeArt toggle lets it skip art for a fast create-records-only path (ASSET_ONLY items need art, so skip them when it's off). No new backend — it orchestrates over the idempotent executor, so re-running is safe. kind_robots PR #196.
- 2026-07-12 `model-builder/t-024` — Generic AI drafts (a bland reward) come from a generic prompt with no field awareness. The fix is a single per-model field spec (modelBuilderFields: required/optional, defaults, choice pools grounded in the schema + builder *Cards) used to pre-fill the FIELDS box AND fed into the suggest context as 'Fields to fill', so the model returns a full specific record with valid choices. Kept the drafts rich but deferred writing the parsed fields to real columns (t-028) — that's a prod-write not worth shipping untested. kind_robots PR #195.
- 2026-07-12 `model-builder/t-001..t-012` — When a project is built directly rather than spec-first, the 'write a spec doc' tasks are closed by subsumption: the executable code + reference runs ARE the spec. Map each task to its shipped artifact (see docs/spec-subsumption.md) instead of writing redundant prose. Be honest about the tail — video (LTX) and 3D (Hunyuan3D/STL) inside t-012 stay explicitly deferred rather than folded into 'done'.
- 2026-07-12 `model-builder/t-020` — A registered /api/suggest sheet only helps if the client lets it: buildSuggestUserPrompt resolves extra.instruction BEFORE sheet.fieldPrompts, so a store that always sends extra.instruction silently overrides the sheet. Fix is two-sided — register the sheet (system prompt + per-field prompts + a buildContext that digests the source record's canon) AND stop the store force-sending an instruction (send only when explicitly provided). Then getSuggestSheet('model-builder') stops falling back to the adventure sheet. kind_robots PR #193.
- 2026-07-12 `model-builder/t-019` — The conductor->KR project sync (scripts/sync_projects.py) only processes slugs marked active in project-overrides.yaml AND, before this task, never transmitted goal/waypoints even though the KR /api/projects endpoint accepts them. To wire a project's identity: add the override entry, add goal/waypoints to roadmap top matter, and extend build_project_payload to send them (goal as text; waypoints serialized to KR's pipe-delimited string) only when present so other projects are not cleared. Nav is seed-driven: append a type:directory SmartIcon to stores/seeds/smartIcons.json (the navStore fallback) mirroring /art; a content page with an icon: frontmatter also auto-registers via npm run generatesmart.
- 2026-07-12 `model-builder/t-018` — Dream->3-Characters expansion runs autonomously end-to-end: pick a real Dream (Lantern Greenhouse, id 37) and let its `examples` seed the cast (one character per theme). The executor's guarantees ARE the t-018 proof points — three independent CREATE items (private/inactive, userId 10, unique @unique slugs), Dream links via the Characters implicit m2m, per-child idempotencyKey so a failed child retries alone and a COMMIT replay creates zero duplicates. A cohesive shared portrait style in the generate manifest keeps the cast visually tied to the dream.
- 2026-07-12 `model-builder/t-017` — Autonomous Character Deck reference run grounds best in a real flagship record (AMIb0t from stores/seeds/seedBots.ts). Identity consistency is the linchpin: generate the canonical NEUTRAL avatar FIRST, lock seed+checkpoint, reuse for icon/card/hero/expressions; prove on a small 5-key expression subset before any full 20-key batch (Expression enum has 10 emotions + 10 actions + CUSTOM; NEUTRAL is canonical; ExpressionMedia owner is Bot XOR Character). Character has only artImageId/imagePath (no icon/card/hero path fields — those are on Dream), so deck icon/card/hero are ArtImages in the owner's collection.
- 2026-07-12 `model-builder/t-016` — The Model Builder's four gates are OPTIONAL front-end pauses (skip an item, or stop after prompt to edit) — NOT a backend block that waits on a repo-file approval. Default is to create full objects for everything. I over-applied a 'needs-human, internal-draft-only' framing to the HSS marketing deck; the right move was a full example set with the visuals queued into the real art pipeline (projects/art-generate.yaml). Also: the art generator forbids text/logos, so marketing collateral splits into generated text-free imagery + a text/logo layout step over the real logo (no rebrand). Don't invent brand facts — pricing/area/logo/descriptor came from Silas and were folded into CONTENT-BRIEF.
- 2026-07-12 `model-builder/t-013` — Idempotent canonical writes without a live DB: an atomic claim on a unique key (updateMany where key IS NULL; count===0 means already committed) gives exactly-once semantics, releasing the key on write failure enables retry, and create+link in one $transaction prevents orphans. When you can't run the DB, keep writes to KNOWN exact field/relation names (pulled from schema) so vue-tsc validates every prisma.model.update/create at PR time — a wrong field name fails CI instead of corrupting prod. Covers t-013/t-014/t-015; kind_robots PR #190. Live proof still pending (t-022).

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-12T20:38:00Z_
