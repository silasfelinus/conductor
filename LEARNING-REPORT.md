# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-28T13:49:23Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1188**
- Outcomes: blocked: 19, cancelled: 2, done: 1167
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
| tzaddik-gallery | 19 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 1171 | 99% |

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

- 2026-09-28 `tzaddik-gallery/t-025` — kr-gallery's #item slot (already used by bot-gallery.vue) lets a new object type get a bespoke card without touching the generic GalleryItem renderer every other gallery shares -- the narrower, lower-blast-radius option when a task note offers a choice between a cross-cutting change and a per-gallery override. Also: verifyCardActionContract.ts's ENTITY_CARDS/SHARED_BODY_CARDS lists are a curated allowlist ('new models get added here'), not a glob -- a new *-card.vue wrapping reactable-card should be registered there explicitly.
- 2026-09-28 `tzaddik-gallery/t-024` — A 'kaizen from X, once Y lands' follow-up filed against a not-yet-merged dependency can end up fully subsumed by that dependency's actual implementation -- read the dependency's merged diff (not just its status: done) before claiming the downstream task, since the dependency's own PR description may already name the exact component the follow-up targets.
- 2026-09-28 `animation-manager/t-024` — check_animation_novelty.py's Jaccard-based collision score is meaningless once one side (a catalog tooltip) is far shorter than the other (a pitch's novelty prose) -- an exact shared word scores near zero once the longer side dilutes the union. Switching to an overlap coefficient (|A∩B| / min(|A|,|B|)) for that specific comparison fixed it; worth remembering for any future keyword-overlap check comparing texts of very different lengths.
- 2026-09-28 `tzaddik-gallery/t-009` — Deploy-lag reconciliation should probe the actual live listing endpoint (GET /api/tzaddik) rather than only re-testing the write endpoint (POST /api/tzaddik/import) each cycle -- the read side can go live and get seeded by another session's PR before a session re-checking only the write path would notice.
- 2026-09-28 `animation-manager/t-007` — Two things worth carrying forward. (1) check_animation_novelty.py only diffs a pitch against other PITCHES.yaml entries, not the already-shipped catalog in stores/animationCatalog.ts -- kaleidoscope-bloom (priority 27) sat undetected as a likely near-duplicate of the pre-pitch-pipeline kaleidoscope-effect.vue catalog entry; caught by hand, worked around by building the next pitch (moire-weave-engine) instead, filed as t-024/t-025 for a structural fix and a pitch-fate decision. (2) close_task.py's --branch defaults to reusing whatever close-out branch a prior status transition in the same cycle already created; if a separate fix (here, a roadmap duplicate-key bug) lands on main in between, that reused branch is still based on the pre-fix tip and the same duplicate-key error recurs even though origin/main is clean -- passing a fresh --branch name based on current origin/main resolved it. Worth close_task.py detecting this itself (a stale existing --branch whose base predates a needed fix) rather than requiring the caller to notice the base mismatch by hand.
- 2026-09-28 `tzaddik-gallery/t-026` — check_pr_merged_drift.py caught a real gap: t-026's implementing PR (kind_robots#3072) merged over an hour before any session reconciled the roadmap task off status=review. Worth running the merged-PR drift check as a matter of course after any worker cycle that touches a cross-repo project, not only at session start/end, since a PR can merge mid-session on its own CI schedule without the conductor session that opened it noticing.
- 2026-09-28 `tzaddik-gallery/t-012` — select_role.py's kind_robots candidate_reviewable_pr_count reported 0 while a real, fully green, mergeable claude/* PR (kind_robots#3071) had been sitting open for ~4 hours. A direct list_pull_requests call against kind_robots found it immediately. Worth checking select_role.py's kind_robots PR-scan filter (branch prefix? PR age? author?) against this specific miss before trusting its reviewable-PR count as complete -- a manual cross-repo PR listing is cheap insurance in the meantime.
- 2026-09-28 `tzaddik-gallery/t-010` — A stale claim (t-010 sat claimed by an openai session for 5+ hours with no branch ever pushed) is safe to reclaim and complete directly once the TTL has expired -- next_ready_task.py already surfaces this correctly. Placing the new research-pool content inside discovery/ (matching the dated dockets' heading/section/tzaddik-meta format) rather than at the project root meant excluded_names() picked it up for dedup automatically, with zero code changes -- worth defaulting to 'shape new content to fit an existing scan' before reaching for a scanner-code change.
- 2026-09-28 `tzaddik-gallery/t-027` — A kaizen task's premise can be invalidated by how its own dependency actually gets built, not just by scope drift over time -- t-027 assumed t-015 would need a kind_robots-database pull for dedup state, but t-015 (#5323) made that moot in the same PR that unblocked t-027. Closing it required only re-reading excluded_names() and its own test coverage, no implementation. Worth claiming and closing a downstream kaizen immediately when its resolution is already evident, rather than leaving a 'ready' task in the queue that looks like real work but isn't.
- 2026-09-28 `tzaddik-gallery/t-015` — 'Give Silas a review surface' does not have to mean a live kind_robots UI/DB build -- a conductor-side script plus a small human-editable YAML ledger (scripts/tzaddik_review.py + discovery-decisions.yaml) satisfied the actual contract (approve/reject/defer/show-full-profile, wired into the session digest) in one landable pass, matching how Daily Dream's own conductor-side state is already surfaced. Also caught mid-close: t-014's own kaizen (t-027) had assumed t-015 would need a kind_robots database, which turned out to be moot once excluded_names() was re-read closely -- it already dedupes every docketed name permanently regardless of decision. Re-verify a dependent kaizen task's premise against what actually got built, not what was assumed, before letting it sit as 'ready' work for someone else to discover is unnecessary.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-28T13:49:23Z_
