# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-29T13:45:24Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1198**
- Outcomes: blocked: 19, cancelled: 2, done: 1177
- Success rate: **98%**
- Average passes on successful tasks: **0.3**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 73 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 24 | 96% |
| animation-studio | 2 | 50% |
| appmaker | 11 | 100% |
| approval-portal | 2 | 0% |
| art-archive | 34 | 100% |
| art-generator-connect | 3 | 100% |
| brainstorm | 26 | 96% |
| butterfly-gallery | 32 | 94% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 46 | 100% |
| conductor | 138 | 100% |
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
| mandarin-tutor | 15 | 93% |
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
| tzaddik-gallery | 26 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 1181 | 99% |

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

- 2026-09-29 `mandarin-tutor/t-031` — When a teaching card already labels a component's role and gives its sourced origin, repeating the same role again in a helper sentence adds noise rather than instruction.
- 2026-09-28 `animation-manager/t-025` — kaleidoscope-bloom's own novelty section claimed no existing pitch used dihedral mirror-symmetry rendering, but a direct read of kaleidoscope-effect.vue showed it already ships the identical wedge-simulate + rotate/alternating-mirror technique -- the exact gap t-024 closed in check_animation_novelty.py (novelty was only ever checked against other PITCHES.yaml entries, not the shipped catalog). Retired rather than rewrote: when the overlap is in the rendering mechanism itself rather than surface theming, differentiating the surprise/title still ships a re-skin, not a genuinely new animation. Worth reading a pitch's actual claimed-novel technique against the real component source before trusting its own novelty section, not just running the automated checker.
- 2026-09-28 `animation-manager/t-023` — Found while closing t-007's 2026-09-27 cycle: 17 pitches had a live component + catalog registration + exactly one build entry but were still marked status: candidate at both the pitch and build level, identical to a gap already fixed once for geode-bloom alone (2026-09-21). Verified each id's component file and animationCatalog.ts registration individually against kind_robots@main before promoting -- grep, not assumption -- rather than batch-promoting on the roadmap note's word alone. Worth a small periodic checker script (filed as this task's kaizen suggestion) so this class of drift surfaces on its own instead of needing a Worker to notice it by hand during an unrelated cycle.
- 2026-09-28 `tzaddik-gallery/t-032` — t-031's kaizen note (above) named the exact gap this task closed: tzaddik-card.vue's own recheck buttons showed on any non-empty recheckReasonLabel(...), which is also true for a FAILED recheck, while resolveTzaddikRecheckReview 409s on any status other than NEEDS_REVIEW. Added a recheckNeedsReview computed reading RecheckRequests[0].status directly instead of re-deriving it from the reason-label helper. Currently unreachable in production per t-029's note (only the NEEDS_REVIEW queue filter's response carries RecheckRequests at all), same as t-031's equivalent fix on the detail sheet -- worth grepping for every other consumer of recheckReasonLabel/RecheckRequests[0] the next time this surface changes, since the same latent gap could recur on a third surface.
- 2026-09-28 `tzaddik-gallery/t-031` — Gated the detail sheet's new Update/Keep-current buttons on latestRecheck.status === 'NEEDS_REVIEW' explicitly rather than reusing the queue card's broader non-empty-reason-label condition -- the card's condition also renders for FAILED recheck requests, which /api/tzaddik/recheck-resolve rejects with a 409. Worth checking a sibling component's show-condition against the server's actual guard, not just copying it, when adding the same control to a second surface.
- 2026-09-28 `tzaddik-gallery/t-018` — check_pr_merged_drift.py caught a task left at status: review after its PR (kind_robots#3078) had already merged -- reconciled during the scheduled sweep's session-startup checks rather than sitting stale until a later Reviewer pass noticed it by hand.
- 2026-09-28 `tzaddik-gallery/t-030` — The kaizen note that spawned this task assumed 'existing recheck-resolution logic' to wire buttons to -- there wasn't any; recheck.post.ts detects an identity change but never applies it. Verify a kaizen task's premise against the actual code before implementing, not just its own wording, since a Reviewer's own kaizen suggestion can be wrong about what already exists.
- 2026-09-28 `tzaddik-gallery/t-029` — The server route already returned the data the card needed (RecheckRequests on the needsReview=true filter) -- the whole fix was rendering it and widening one store type. Extracting the existing recheckDetailLabel parsing logic out of the detail sheet into a shared util (rather than re-deriving it on the card) kept the two surfaces from reading resultJson.reason differently.
- 2026-09-28 `tzaddik-gallery/t-028` — Reusing the existing admin Review-queue tab (Pending/Archived) with a third filter value, instead of building a dedicated NEEDS_REVIEW page, kept the diff small and consistent with the site's own routes-and-surfaces guidance to prefer an existing surface over a new one.
- 2026-09-28 `tzaddik-gallery/t-019` — The recheck pipeline's schema, fetch util, and UI were already built across three earlier tasks (t-005/t-006/t-009) -- the only missing piece was recheck.post.ts actually calling fetchTzaddikSource. Check for already-built-but-unwired pieces before assuming a task needs new code from scratch.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-29T13:45:24Z_
