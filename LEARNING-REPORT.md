# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-27T06:52:35Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **778**
- Outcomes: blocked: 15, cancelled: 1, done: 762
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
| conductor | 83 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 12 | 100% |
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
| ruler-hooked | 9 | 100% |
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
| software | 762 | 99% |

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

- 2026-08-27 `ruler-hooked/t-022` — An asset-generation task's "review" status can mean "ArtJobs submitted, awaiting delivery confirmation" rather than "PR open awaiting human review" -- check_pr_merged_drift.py's PR-shaped heuristic can't verify this kind of task at all (no PR ever existed), so it correctly surfaces as unresolvable via that script alone. The task's own note already named the exact completion check (media paths live) -- reading that note before assuming "review" means "needs a PR" avoided treating genuinely-finished async delivery as stuck.

- 2026-08-27 `conductor/t-131` — A "shared helper" kaizen suggestion is easy to under-scope by only reading the two callers' surface signatures. Reading both fetch_queue_stats implementations closely first showed one call site (check_render_box.py) needed a swallow-all-exceptions probe contract and the other (recheck_render_queue.py) needed the raised RuntimeError itself, so the shared helper had to raise and let each caller decide -- a naive merge that picked either behavior would have silently broken the other caller.

- 2026-08-27 `cthulhuquarium/t-045` — A slug-to-artImageId mapping that "only exists in job logs" is still fully recoverable, not a hard gap -- get_job_logs with a generous tail_lines covered the whole relevant step, and simple regex extraction over the consume_art_queue_core.py's own printed "DONE ... (ArtImage {id})" lines reconstructed the batch's mapping completely. Worth defaulting to log recovery before treating an unrecorded mapping as lost, since the generating script already prints exactly what's needed.

- 2026-08-27 `cthulhuquarium/t-046` — A generator bug that was already root-caused and fixed (t-044's self-referential image_path) still had zero regression coverage until this task -- verifying a fix by hand once is not the same as making it impossible to reintroduce silently. Confirming a new test actually fails against the pre-fix code (not just passes against the post-fix code) is what makes a regression test trustworthy rather than a tautology.

- 2026-08-27 `cthulhuquarium/t-044` — A batch generator that writes image_path == the staging directory consume_art_queue_core.py itself renders into is a self-referential destination for every entry it will ever produce, not an occasional edge case -- distribute_images.py's own self-referential-path guard (added the day before to stop a crash) had already surfaced this exact shape once and the root cause was deferred as "still open"; it recurred immediately on the very next batch through the same generator. When a bug's fix note says the root cause is open, treat the next batch that touches the same code path as a live suspect before assuming a downstream "unmatched"/"no-op" result is unrelated.

- 2026-08-27 `ruler-hooked/t-017` — The task's own note already named its exact done condition ('flip to done when #2139 merges') -- reconciling status after a companion cross-repo PR merges is a one-line check against that condition, not a re-review of the work.
- 2026-08-26 `ruler-hooked/t-017` — Two coherent specs in different repos can contradict each other indefinitely when nothing connects them; the art direction said layers are full-frame and transparent outside their band while the component cropped each to a 20:1 strip, and only generating against it surfaced the conflict.
- 2026-08-26 `ruler-hooked/t-020` — A rejected suggestion can still contain a real finding: Silas preferred the existing presets over his own six-ruler proposal, but that proposal named the age gap (no child ruler) the presets actually had.
- 2026-08-26 `ruler-hooked/t-016` — Pinning one character as a constant for cross-piece consistency silently makes that character the product's default; parameterize the cast and name the hero instead.
- 2026-08-26 `cthulhuquarium/t-043` — An existing generic pattern (server/utils/entityArt.ts, already wired for Character/Scenario/Reward/etc.) doesn't have to be extended to cover every entity with art fields -- Monster's fields are shaped identically but the actual need (link an already-generated ArtImage id directly, admin-only, no owner concept) was narrower than that system's generate/upload/history workflow. A small dedicated route was less code and easier to review than threading a new case through six switch statements in a shared file built for a different job.


---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-27T06:52:35Z_
