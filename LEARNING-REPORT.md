# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-17T19:53:28Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **241**
- Outcomes: blocked: 12, done: 229
- Success rate: **95%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 25 | 100% |
| alexa-integration | 2 | 100% |
| animation-manager | 4 | 100% |
| animation-studio | 1 | 100% |
| appmaker | 2 | 100% |
| approval-portal | 2 | 0% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 12 | 100% |
| conductor | 30 | 100% |
| digital-storefront | 8 | 100% |
| dream-cycle | 14 | 100% |
| ecosystem-map | 4 | 100% |
| global-ui | 9 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 1 | 100% |
| kind-robots | 26 | 96% |
| kindrobots-unraid | 4 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 28 | 100% |
| mural-design | 1 | 100% |
| newsfeed | 2 | 100% |
| packmaker | 7 | 100% |
| ruler-hooked | 2 | 100% |
| serendipity | 1 | 100% |
| superkate-hairstyle-ai | 16 | 100% |
| superkate-services-calculator | 11 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 226 | 99% |

## Failure categories

| Category | Count |
|---|---|
| actionable | 6 |
| quality | 3 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `actionable` — 6 occurrences; look for the shared cause across its records
- failure category `quality` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-07-17 `packmaker/t-004` — Cross-repo admin-surface task with an unmet ACL dependency (kind-robots t-008) landed clean by keeping every created record isPublic:false as an explicit interim rule and deferring release/storefront wiring entirely, rather than stubbing a half-working gate. Task sat at status: claimed (not review) while its PR was open -- next cycle should flip to status: review before gh pr create per AGENTS.md step 7, even for cross-repo tasks.
- 2026-07-17 `ai-art-academy/t-014` — art-styler.vue's source picker had no shared SourceImagePicker component or composable to extend -- upload/gallery state lived as plain inline refs. Adding a third source (the starter library) was still low-risk because generation (runStyleTransfer) only reads two refs (uploadedImageData/selectedSourceImage), so any new source that populates those two the same way needs zero changes downstream. Extracted the shared synthetic-ArtImage builder (buildSyntheticSourceImage) rather than duplicating it a second time. When a component's state is inline-only (no composable), check what the *consumer* function actually reads before assuming a new source needs its own code path through generation.
- 2026-07-17 `conductor/t-037` — A deterministic cross-repo write failure (4/4 identical retries while 31 reads succeeded) was correctly parked at needs-human rather than burning passes — the cause was environmental (expired KR_API_TOKEN + the t-022 DB-pool outage), invisible to client-side inspection. When the upstream incidents cleared, verification cost one Actions log read: the sync run showed both formerly-failing creates existing as rows (id=1281/1285). Deterministic-failure + clean-reads is a strong signal to check auth and infra before suspecting the payload.
- 2026-07-17 `packmaker/t-003` — Gated draft work (two DLC pack manifests) sat complete at needs-human for two days until Silas batch-cleared gates in a report session. Drafts validated against the t-002 schema before the gate meant zero rework on approval — front-loading schema validation makes human gates cheap to clear.
- 2026-07-17 `superkate-hairstyle-ai/t-020` — Process gap fixed at the AGENTS.md level (step 7: set status review before any PR, all session types) rather than per-project. The task itself then sat at status: review after its PR merged — the exact failure mode it documents — because the session ended without the review→done flip. A task whose deliverable is a process rule should be closed in the same commit that lands the rule.
- 2026-07-17 `kind-robots/t-022` — Production DB pool exhaustion (t-022, first seen 2026-07-15T08:56Z) had three false starts before the real fix: two app-code pool-config tweaks (#296 limit fallback, #300 TLS checkServerIdentity, #325/#327 pool lifecycle) each looked plausible and were confirmed live in prod, yet the outage kept recurring under a different signature each time (limit=10, then limit=1 'one-shot fallback'). The fix that actually held was a full revert (#342) of the one-shot-fallback mechanism (#336) rather than another patch on top of it -- when a pool/infra incident keeps changing shape after being 'fixed' twice, suspect the fix itself introduced a new failure mode and consider reverting the whole mechanism instead of patching further. Closed after 12+ hours / ~12 hourly cycles of sustained zero-503 confirmation, per Silas's own standing instruction to close once verified healthy.
- 2026-07-17 `dream-cycle/t-017` — An always-failing dependency (intermittent DB 503s) masked two schema/contract bugs that meant the daily-dream pipeline had NEVER shipped a row: extraData is a String column (json.dumps it, don't send an object) and dream slugs are globally unique (send explicit de-duped slugs). Build live end-to-end once, early — dry-runs and unit tests can't catch a Prisma type mismatch. Run long API builds detached (background), never in a 2-min-capped foreground call.
- 2026-07-17 `ai-art-academy/t-030` — Another self-contained conductor-only kaizen task, picked up burst-mode in an hourly Reviewer cycle with no open worker/* PR to review. Added Cloudflare challenge fallback signals (Server header + cf-chl cookie, __cf_chl_rt_tk body marker) behind defensive getattr()/callable() checks so the existing test doubles (which don't implement get_all()/read()) kept passing unchanged rather than needing every prior fixture updated — cheaper than the t-029 fixture-rewrite when the new code path is additive rather than a signature change.
- 2026-07-17 `ai-art-academy/t-029` — Self-contained conductor-only kaizen task (no cross-repo dependency): claimed, implemented, and merged in a single autonomous hourly cycle. probe_host()/append_entry() changed from a bool blocked/reachable signal to a three-way status string so a Cloudflare cf-mitigated challenge response is no longer silently folded into 'reachable' — the exact gap t-013 hit and hand-documented manually. Updating an existing test suite's fixtures (bool -> string) alongside new coverage, rather than only adding new tests, is what kept the refactor from leaving stale assertions that would pass for the wrong reason.
- 2026-07-17 `digital-storefront/t-013` — Cross-repo software task where the code PR (kind_robots#361) and the conductor bookkeeping PR (#700) were opened by a prior burst-mode session but left unmerged at status:review — the Reviewer cycle's job was purely to verify and merge both, then close the roadmap task. Delegating the payment-code diff review to a subagent (checking migration additivity, auth on the new cancel-subscription endpoint, and webhook signature verification) kept the large diff out of the main context while still confirming test-mode-only, no live keys, no cross-user cancellation.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-17T19:53:28Z_
