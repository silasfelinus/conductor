# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-28T15:23:56Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1192**
- Outcomes: blocked: 19, cancelled: 2, done: 1171
- Success rate: **98%**
- Average passes on successful tasks: **0.3**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 73 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 22 | 95% |
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
| tzaddik-gallery | 23 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 1175 | 99% |

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

- 2026-09-28 `tzaddik-gallery/t-030` — The kaizen note that spawned this task assumed 'existing recheck-resolution logic' to wire buttons to -- there wasn't any; recheck.post.ts detects an identity change but never applies it. Verify a kaizen task's premise against the actual code before implementing, not just its own wording, since a Reviewer's own kaizen suggestion can be wrong about what already exists.
- 2026-09-28 `tzaddik-gallery/t-029` — The server route already returned the data the card needed (RecheckRequests on the needsReview=true filter) -- the whole fix was rendering it and widening one store type. Extracting the existing recheckDetailLabel parsing logic out of the detail sheet into a shared util (rather than re-deriving it on the card) kept the two surfaces from reading resultJson.reason differently.
- 2026-09-28 `tzaddik-gallery/t-028` — Reusing the existing admin Review-queue tab (Pending/Archived) with a third filter value, instead of building a dedicated NEEDS_REVIEW page, kept the diff small and consistent with the site's own routes-and-surfaces guidance to prefer an existing surface over a new one.
- 2026-09-28 `tzaddik-gallery/t-019` — The recheck pipeline's schema, fetch util, and UI were already built across three earlier tasks (t-005/t-006/t-009) -- the only missing piece was recheck.post.ts actually calling fetchTzaddikSource. Check for already-built-but-unwired pieces before assuming a task needs new code from scratch.
- 2026-09-28 `tzaddik-gallery/t-025` — kr-gallery's #item slot (already used by bot-gallery.vue) lets a new object type get a bespoke card without touching the generic GalleryItem renderer every other gallery shares -- the narrower, lower-blast-radius option when a task note offers a choice between a cross-cutting change and a per-gallery override. Also: verifyCardActionContract.ts's ENTITY_CARDS/SHARED_BODY_CARDS lists are a curated allowlist ('new models get added here'), not a glob -- a new *-card.vue wrapping reactable-card should be registered there explicitly.
- 2026-09-28 `tzaddik-gallery/t-024` — A 'kaizen from X, once Y lands' follow-up filed against a not-yet-merged dependency can end up fully subsumed by that dependency's actual implementation -- read the dependency's merged diff (not just its status: done) before claiming the downstream task, since the dependency's own PR description may already name the exact component the follow-up targets.
- 2026-09-28 `animation-manager/t-024` — check_animation_novelty.py's Jaccard-based collision score is meaningless once one side (a catalog tooltip) is far shorter than the other (a pitch's novelty prose) -- an exact shared word scores near zero once the longer side dilutes the union. Switching to an overlap coefficient (|A∩B| / min(|A|,|B|)) for that specific comparison fixed it; worth remembering for any future keyword-overlap check comparing texts of very different lengths.
- 2026-09-28 `tzaddik-gallery/t-009` — Deploy-lag reconciliation should probe the actual live listing endpoint (GET /api/tzaddik) rather than only re-testing the write endpoint (POST /api/tzaddik/import) each cycle -- the read side can go live and get seeded by another session's PR before a session re-checking only the write path would notice.
- 2026-09-28 `animation-manager/t-007` — Two things worth carrying forward. (1) check_animation_novelty.py only diffs a pitch against other PITCHES.yaml entries, not the already-shipped catalog in stores/animationCatalog.ts -- kaleidoscope-bloom (priority 27) sat undetected as a likely near-duplicate of the pre-pitch-pipeline kaleidoscope-effect.vue catalog entry; caught by hand, worked around by building the next pitch (moire-weave-engine) instead, filed as t-024/t-025 for a structural fix and a pitch-fate decision. (2) close_task.py's --branch defaults to reusing whatever close-out branch a prior status transition in the same cycle already created; if a separate fix (here, a roadmap duplicate-key bug) lands on main in between, that reused branch is still based on the pre-fix tip and the same duplicate-key error recurs even though origin/main is clean -- passing a fresh --branch name based on current origin/main resolved it. Worth close_task.py detecting this itself (a stale existing --branch whose base predates a needed fix) rather than requiring the caller to notice the base mismatch by hand.
- 2026-09-28 `tzaddik-gallery/t-026` — check_pr_merged_drift.py caught a real gap: t-026's implementing PR (kind_robots#3072) merged over an hour before any session reconciled the roadmap task off status=review. Worth running the merged-PR drift check as a matter of course after any worker cycle that touches a cross-repo project, not only at session start/end, since a PR can merge mid-session on its own CI schedule without the conductor session that opened it noticing.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-28T15:23:56Z_
