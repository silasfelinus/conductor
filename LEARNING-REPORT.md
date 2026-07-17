# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-17T22:08:50Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **247**
- Outcomes: blocked: 12, done: 235
- Success rate: **95%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 26 | 100% |
| alexa-integration | 2 | 100% |
| animation-manager | 4 | 100% |
| animation-studio | 1 | 100% |
| appmaker | 2 | 100% |
| approval-portal | 2 | 0% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 12 | 100% |
| conductor | 30 | 100% |
| digital-storefront | 9 | 100% |
| dream-cycle | 14 | 100% |
| ecosystem-map | 4 | 100% |
| global-ui | 9 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 1 | 100% |
| kind-robots | 26 | 96% |
| kindrobots-unraid | 4 | 100% |
| media-watchlist | 1 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 28 | 100% |
| mural-design | 1 | 100% |
| newsfeed | 2 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 2 | 100% |
| serendipity | 1 | 100% |
| superkate-hairstyle-ai | 16 | 100% |
| superkate-services-calculator | 11 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 232 | 99% |

## Failure categories

| Category | Count |
|---|---|
| actionable | 6 |
| quality | 4 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `actionable` — 6 occurrences; look for the shared cause across its records
- failure category `quality` — 4 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-07-17 `packmaker/t-010` — Reusing an established hermetic-VM contract-test pattern (t-008's validatePackManifest test) for a sibling function made a same-cycle kaizen pickup fast and low-risk — the one wrinkle was that assert.deepEqual on objects returned from vm.runInNewContext fails on cross-realm prototype mismatch even when data is structurally identical; round-trip through JSON.parse(JSON.stringify(...)) to normalize before comparing.
- 2026-07-17 `packmaker/t-009` — A cross-cutting infra fix (suggest providers hardcoding max_tokens 512) surfaced naturally while building one feature's LLM call — landing it in the same PR benefited every suggest caller instead of needing a separate follow-up task.
- 2026-07-17 `digital-storefront/t-024` — Clean first-pass auth fix mirroring an existing correct sibling endpoint (cancel-subscription.post.ts) — copying a proven pattern in the same file family is a reliable way to close a security kaizen quickly.
- 2026-07-17 `packmaker/t-008` — Pure logic embedded in a Nuxt store may not import cleanly in lightweight CI; execute the exact source in a hermetic TypeScript VM or extract it into a dependency-light module rather than mocking or copying the implementation.
- 2026-07-17 `ai-art-academy/t-013` — A soft needs-human task blocked purely by a connector limitation (full-blob-only file replacement risking truncation) is not the same as a task blocked by missing data — the handoff doc already had fully sourced, license-verified, byte-exact content ready to apply. Any later session with a real local git checkout of the target repo should treat such a handoff as directly actionable, not re-park it at needs-human.
- 2026-07-17 `media-watchlist/t-007` — A 12-year hand-maintained log had ~6 format regimes the 2-year design sample never showed (unheadered year blocks, reversed headers, mixed-case sections, embedded stats tables, prose). Structural detection (a repeating section type implies a new unheadered year) beat hardcoded line numbers, and the log's own hand-tallies served as free validation targets — 2342 entries parsed with 0 unparseable lines and every mismatch traced to source-side drift, not parser error.
- 2026-07-17 `packmaker/t-004` — Cross-repo admin-surface task with an unmet ACL dependency (kind-robots t-008) landed clean by keeping every created record isPublic:false as an explicit interim rule and deferring release/storefront wiring entirely, rather than stubbing a half-working gate. Task sat at status: claimed (not review) while its PR was open -- next cycle should flip to status: review before gh pr create per AGENTS.md step 7, even for cross-repo tasks.
- 2026-07-17 `ai-art-academy/t-014` — art-styler.vue's source picker had no shared SourceImagePicker component or composable to extend -- upload/gallery state lived as plain inline refs. Adding a third source (the starter library) was still low-risk because generation (runStyleTransfer) only reads two refs (uploadedImageData/selectedSourceImage), so any new source that populates those two the same way needs zero changes downstream. Extracted the shared synthetic-ArtImage builder (buildSyntheticSourceImage) rather than duplicating it a second time. When a component's state is inline-only (no composable), check what the *consumer* function actually reads before assuming a new source needs its own code path through generation.
- 2026-07-17 `conductor/t-037` — A deterministic cross-repo write failure (4/4 identical retries while 31 reads succeeded) was correctly parked at needs-human rather than burning passes — the cause was environmental (expired KR_API_TOKEN + the t-022 DB-pool outage), invisible to client-side inspection. When the upstream incidents cleared, verification cost one Actions log read: the sync run showed both formerly-failing creates existing as rows (id=1281/1285). Deterministic-failure + clean-reads is a strong signal to check auth and infra before suspecting the payload.
- 2026-07-17 `packmaker/t-003` — Gated draft work (two DLC pack manifests) sat complete at needs-human for two days until Silas batch-cleared gates in a report session. Drafts validated against the t-002 schema before the gate meant zero rework on approval — front-loading schema validation makes human gates cheap to clear.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-17T22:08:50Z_
