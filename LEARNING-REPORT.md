# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-16T23:08:52Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **996**
- Outcomes: blocked: 16, cancelled: 1, done: 979
- Success rate: **98%**
- Average passes on successful tasks: **0.1**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 73 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 14 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 9 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| brainstorm | 26 | 96% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 38 | 100% |
| conductor | 120 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 51 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 23 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 136 | 100% |
| kapowarr | 52 | 100% |
| kind-economy | 10 | 100% |
| kind-robots | 64 | 98% |
| kindrobots-unraid | 9 | 100% |
| lora-ingestion | 1 | 100% |
| mandarin-tutor | 11 | 100% |
| media-watchlist | 12 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 84 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| rainbow-butterflies | 21 | 100% |
| ruler-hooked | 12 | 100% |
| scene-animator | 2 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 25 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 7 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 979 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 27 |
| transient | 16 |
| actionable | 15 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 47% success over 17 closed tasks; aim the next kaizen task here
- failure category `quality` — 27 occurrences; look for the shared cause across its records
- failure category `transient` — 16 occurrences; look for the shared cause across its records
- failure category `actionable` — 15 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-16 `ruler-hooked/t-023` — Silas's in-session product feedback ("Deliverables and status does not belong, that's more of a project info section that should be redundant") named a leak in a SHARED component (project-front-page.vue) mounted by four separate product pages, not just the one he was playing. Following the precedent #2623 already established for this exact wrapper -- change what the shared component chooses to render, don't delete or fork it -- kept the fix to a one-line prop flip on three call sites plus the page-specific banner/sections work Ruler Hooked itself needed. Cross-referencing the task note against #2623's actual diff before starting caught that a superficially similar-sounding complaint (raw pitch text as page copy) was already fixed and out of scope, avoiding redundant work on the same file. No live preview exists for pre-merge UI verification (Vercel retired); eslint + vue-tsc + test:layout-contract + verifyPwaPrecacheBudget + verifyKrClassCoverage were the full pre-merge verification surface available, and none of them render a single template -- worth remembering as the ceiling of local certainty for this class of change until Chromium-through-proxy visual verification (see AGENTS.md's 2026-09-16 update) gets used more routinely for a merged/deployed follow-up look.
- 2026-09-16 `kind-robots/t-108` — A hand-measured methodology (t-106's clipped-pixel curve, described only as "the fraction of pixels at 0 or 255") was ambiguous enough to implement three different ways -- greyscale luminance, whole-pixel all-channels-clipped, and RGB per-channel-sample -- with wildly different results (0.86%, 0.09%, and 3.31% respectively on the same reference image, against a recorded 3.48%). Only re-deriving the number on the exact LoRA/render the original measurement named (AsheLoLXL's own cfg-10 datapoint) caught this before 769 production rows got written from the wrong one. When a task's note says "verify against the hand-measured reference before trusting it catalog-wide," that check is doing real work, not boilerplate -- budget time for it rather than picking the first plausible-sounding definition. Separately: a per-candidate network call inside a concurrency-limited batch (mapLimited) MUST be wrapped in its own try/catch -- an unhandled rejection (UND_ERR_HEADERS_TIMEOUT, seen live) aborts the whole Promise.all and kills every other in-flight candidate with it, not just the one that failed. Caught here before any writes happened, but a script over 700+ items should always assume the network will hiccup on at least one of them.
- 2026-09-16 `interface-vision/t-105` — Cycle: two of the Responsive Layout Audit's 19 reported failures were checker false positives rather than real defects -- a nested-scroll-ancestor walk that stopped at the first offscreen inner scroller instead of continuing to a fitting outer one (flagging shelf items inside an intentional home swipe rail), and a sub-32px flex text item flagged as crushed purely for being short rather than for its text actually being clipped (scrollWidth > clientWidth). Fixing the checker's own logic rather than suppressing the routes kept coverage intact. The one real defect (/messages forcing a two-column grid that crushed the empty thread pane to 4px on phones) was fixed with a CSS container query rather than a viewport media query, since the component can be embedded at different container widths elsewhere -- worth defaulting to container queries over viewport media queries for any reusable/embeddable panel component going forward.
- 2026-09-16 `kind-robots/t-107` — A one-line vue-tsc noUncheckedIndexedAccess rejection (TS18048 "possibly undefined" on array-destructured lookups used before arithmetic) cost a full retry cycle that a local `npm run test`/vue-tsc pass before opening the PR would have caught in seconds. The retry itself was clean: explicit `if (!x) return null`/`continue` guards immediately after each array lookup, before any arithmetic. Also confirms the by-now-recurring shape for backfill-style tasks that touch production rows: land the interpolation/ schema-opening prerequisite as its own small, fully-tested, zero-mutation PR first, and file the actual live-data mutation as a separate follow-up task (kind-robots/t-108 here) rather than bundling both into one PR.
- 2026-09-16 `conductor/t-176` — submit_daily_dream_art.py resubmits every status:pending entry in art-prompts.yaml on every daily-digest run with no attempt cap or standing-failure surfacing beyond a failing scheduled workflow, so one entry whose stored prompt trips kind_robots' artPromptContract.ts conditional-instruction rule ("only when X chooses to Y") re-fails identically forever until a human or session edits the stored text by hand. The upstream gate (dream_prose_quality.py's complaints(), run at proposal authoring/revision time) checked known_for/best_scene for length, label-echo, and self-reference but not for the phrasing its own downstream consumer (dream_art_prompts.py) would later fail on at ArtJob enqueue -- the two checks had never been tested against each other. When a producer and a downstream contract check live in different repos/layers, a validation gap between them can persist indefinitely with each side individually "passing." Mirroring the downstream contract's own regex patterns into the upstream gate (rather than inventing a new heuristic) keeps both sides provably in sync and was cheap once the downstream source was actually read.
- 2026-09-16 `kind-robots/t-106` — A task can sit re-armed across several connector-only sessions purely for lack of git/patch primitives (schema edits, prisma regen) rather than any real ambiguity in scope -- this slice (wiring the already-merged Resource.recommendedCfg column into the already-merged loraStackCfgCeiling helper) was fully specified two slices ago and only needed a session with local git + provisioned node_modules to land. Worth checking, on a stuck recurring/re-armed task, whether the blocker is genuinely unresolved scope or just tooling access before assuming it needs more design work. Also: touching a helper's own area surfaced that its contract test (verifyLoraCfg.test.ts, landed with a prior PR) had never been wired into package.json/CI at all -- a merged, passing-looking PR can still ship a test that never actually runs again after that one PR's own CI checked it inline.
- 2026-09-16 `conductor/t-175` — Not every asymmetry between two similar-looking code paths is a bug to converge. verify_event_ownership() (review/done) and the claim branch of compute_transition_ops() (t-173) both touch roadmap_claims.claim_is_stale(), but only the claim branch should: a fresh claim over a stale one only starts new work, while a stale session's late review/done event could silently overwrite a second session's in-progress reclaim. The existing claim path already gives a legitimate session a safe way to take over stale work, so no extension was needed -- documenting the asymmetry in the docstring (with a pinning regression test) closed the decision task without changing behavior.
- 2026-09-16 `conductor/t-173` — A three-call-site staleness rule (next_ready_task.py, claim_task.py, process_task_events.py) had silently drifted to two-out-of-three: the connector processor's claim collision check never consulted roadmap_claims.claim_is_stale(), so a prior session had to paper over the disagreement with a dedicated preflight script (promote_stale_task_event_claims.py) instead of fixing the root disagreement. Making the processor call the shared helper directly let that whole preflight (plus its test and workflow step) be deleted rather than maintained alongside the thing it was working around -- a smaller total diff than the workaround it replaced (68 insertions/177 deletions).
- 2026-09-16 `kind-robots/t-105` — A multi-session small-batch rollout (probe-plan -> enqueue -> verify write-back, repeated in bounded batches while checking render-box/relay health each cycle rather than firing all 223 jobs at once) closed cleanly: 2209/2228 LoRA-family Resources now carry owned preview art, the last job (ArtJob 26249, resourceId 1072) verified DONE with Resource.artImageId/imagePath confirmed written back. The remaining 18 rows are a genuine structural gap (no still-image probe recipe for SD 2.1 768 / Flux.1 Kontext bases), not further queue/relay work -- correctly left as a deferred scope decision for Silas rather than forced into this task or auto-filed as a new one.
- 2026-09-16 `conductor/t-174` — Test-only PR closing a kaizen-flagged coverage gap (main() integration tests for a script whose pure formatter already had unit coverage) merged clean on the first pass, all 25 checks green, no behavior change to the script under test.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-16T23:08:52Z_
