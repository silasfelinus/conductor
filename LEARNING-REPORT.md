# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-27T03:39:54Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **774**
- Outcomes: blocked: 15, cancelled: 1, done: 758
- Success rate: **98%**
- Average passes on successful tasks: **0.1**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 70 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 13 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 9 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| brainstorm | 25 | 96% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 25 | 100% |
| conductor | 82 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 10 | 100% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 85 | 100% |
| kapowarr | 48 | 100% |
| kind-economy | 6 | 100% |
| kind-robots | 52 | 98% |
| kindrobots-unraid | 5 | 100% |
| lora-ingestion | 1 | 100% |
| mandarin-tutor | 7 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 79 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 8 | 100% |
| scene-animator | 2 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 16 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 6 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 16 | 44% |
| software | 758 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 14 |
| actionable | 11 |
| transient | 10 |
| scope | 2 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 14 occurrences; look for the shared cause across its records
- failure category `actionable` — 11 occurrences; look for the shared cause across its records
- failure category `transient` — 10 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-27 `cthulhuquarium/t-044` — A batch generator that writes image_path == the staging directory consume_art_queue_core.py itself renders into is a self-referential destination for every entry it will ever produce, not an occasional edge case -- distribute_images.py's own self-referential-path guard (added the day before to stop a crash) had already surfaced this exact shape once and the root cause was deferred as "still open"; it recurred immediately on the very next batch through the same generator. When a bug's fix note says the root cause is open, treat the next batch that touches the same code path as a live suspect before assuming a downstream "unmatched"/"no-op" result is unrelated.

- 2026-08-27 `ruler-hooked/t-017` — The task's own note already named its exact done condition ('flip to done when #2139 merges') -- reconciling status after a companion cross-repo PR merges is a one-line check against that condition, not a re-review of the work.
- 2026-08-26 `ruler-hooked/t-017` — Two coherent specs in different repos can contradict each other indefinitely when nothing connects them; the art direction said layers are full-frame and transparent outside their band while the component cropped each to a 20:1 strip, and only generating against it surfaced the conflict.
- 2026-08-26 `ruler-hooked/t-020` — A rejected suggestion can still contain a real finding: Silas preferred the existing presets over his own six-ruler proposal, but that proposal named the age gap (no child ruler) the presets actually had.
- 2026-08-26 `ruler-hooked/t-016` — Pinning one character as a constant for cross-piece consistency silently makes that character the product's default; parameterize the cast and name the hero instead.
- 2026-08-26 `cthulhuquarium/t-043` — An existing generic pattern (server/utils/entityArt.ts, already wired for Character/Scenario/Reward/etc.) doesn't have to be extended to cover every entity with art fields -- Monster's fields are shaped identically but the actual need (link an already-generated ArtImage id directly, admin-only, no owner concept) was narrower than that system's generate/upload/history workflow. A small dedicated route was less code and easier to review than threading a new case through six switch statements in a shared file built for a different job.

- 2026-08-26 `conductor/t-130` — check_render_box.py's render_throughput_verdict short-circuited on "any completion in the window is healthy," hiding a stale RUNNING claim with a PENDING backlog behind older completions -- the distinguishing signal (staleRunningCount, queueDepth.PENDING) was already in the same stats payload the caller fetches and just wasn't being read. When a health-check function ignores fields already present in its input, check whether the unused fields are exactly the signal needed before reaching for a new API call or backend change.

- 2026-08-26 `interface-vision/t-104` — Slice 52: before searching fresh, checked slice 39's flagged runner-up candidate (user-manager.vue's managerError/"Unknown user tab" notices) against the roadmap note history first and found slice 40 had already closed it -- avoided a wasted duplicate-work search. The actual fix this slice (watchlist-browse.vue's errorMessage banner missing font-semibold) was found by grepping for the exact hand-rolled kr-note shape and then confirming a genuine live sibling inconsistency via a second, narrower grep for the same errorMessage variable/aria-live wrapper pattern already converted elsewhere (newsfeed-feed.vue) -- cheap to check and turns a plausible-looking candidate into a documented, not-blind substitution matching the standing "same element rendering two different ways across sibling components" rule.

- 2026-08-26 `mandarin-tutor/t-017` — A Pinia store method entangled with Nuxt/user-store runtime (loadCloudState) can still get real regression coverage without a mock framework: extracting its merge decision (server-authoritative, local-only entries kept and re-pushed) into two pure functions in a plain utils module, then having the store call them, made the logic testable with node:assert alone -- same pattern as server/utils/mandarinSrs.ts. No behavior changed; the store's call sites shrank from inline set-difference logic to two function calls.

- 2026-08-26 `mandarin-tutor/t-016` — Mirroring an already-established pattern exactly (MandarinCardProgress's userId-scalar-ownership, house JSON-as-serialized-text convention, upsert-by- client-generated-id) made a full-stack task (migration + 3 endpoints + store wiring) verifiable and mergeable in one pass with zero CI churn. The one design call worth flagging for future similar tasks: syncing a whole client-owned collection (customSets) as a full-array replace-on-every-mutation is tempting for simplicity but risks a second device's unsynced local mutation clobbering a set the first device already pushed -- upserting one item at a time by its client-generated id sidesteps that without needing real conflict resolution.


---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-27T03:39:54Z_
