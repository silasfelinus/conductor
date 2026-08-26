# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-26T02:38:41Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **763**
- Outcomes: blocked: 15, cancelled: 1, done: 747
- Success rate: **98%**
- Average passes on successful tasks: **0.2**

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
| conductor | 81 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 8 | 100% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 84 | 100% |
| kapowarr | 48 | 100% |
| kind-economy | 6 | 100% |
| kind-robots | 52 | 98% |
| kindrobots-unraid | 5 | 100% |
| lora-ingestion | 1 | 100% |
| mandarin-tutor | 4 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 79 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
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
| software | 747 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 14 |
| actionable | 10 |
| transient | 10 |
| scope | 2 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 14 occurrences; look for the shared cause across its records
- failure category `actionable` — 10 occurrences; look for the shared cause across its records
- failure category `transient` — 10 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-25 `interface-vision/t-120` — A recurring-in-practice roadmap task (return-to-ready documented only in prose inside every slice's note) gives close_task.py's `recurring: true` guard nothing to key on, so a `done` close-out slips through silently -- this nearly happened to interface-vision/t-105 earlier the same day (conductor#2884 -> #2887). Setting the `recurring` field explicitly the moment a task's actual operating convention is "always returns to ready" -- not waiting for a mistaken done close-out to force the fix -- turns a 40+-paragraph prose convention into a mechanical refusal the next session can't miss.

- 2026-08-25 `mandarin-tutor/t-014` — GitHub serves raw .json files from raw.githubusercontent.com with Content-Type: text/plain, not application/json -- ofetch's default JSON auto-parsing keys off that header, so a $fetch call against such a URL with no explicit parseResponse/responseType override silently returns the raw response text instead of a parsed value. Confirmed directly against the live pinned source rather than assuming from the error message: without an override the response was a raw string, with `parseResponse: (t) => JSON.parse(t)` it parsed correctly. Any future $fetch against a raw.githubusercontent.com JSON file should pass an explicit parseResponse rather than relying on content-type sniffing -- checked the rest of server/ for the same pattern and found none left unguarded (mandarinCharacterData.ts already used responseType: 'text' with manual per-line JSON.parse for its NDJSON source, so it was never exposed).

- 2026-08-25 `scene-animator/t-004` — Batch-level retryFailed already existed server-side (enqueue.post.ts) and client-side (store.enqueue(true)) before this task -- the task's "failed-job retry" ask was really about per-source (single-card) retry, a narrower gap. Adding an optional sourceFile filter to the existing enqueue loop reused all its dedupe/reuse logic for free rather than duplicating it. For "per-folder completion summary," computing it from the ArtJob rows already fetched for the index endpoint (grouped by each job's own sourceFolder/sourceFile) was far cheaper than the literal reading -- re-hashing every source file's bytes across every folder would have multiplied an already per-file-read+sha256 cost by folder count for a feature that only needs a rough count.

- 2026-08-25 `kind-robots/t-070` — Both code halves of t-070 (the ResourceType enum values and conductor's localPath-prefix-table entries) had already been merged by an earlier session the same day -- re-check `git log`/`git diff` for the actual claimed scope before assuming a `ready` roadmap task still needs code work; it can be a stale status with only an operational follow-up left. That follow-up (one live-DB row mistyped before the new enum values existed) didn't need DB access at all: the app's own authenticated PATCH /api/resources/{id} endpoint made the correction in one call, which is worth reaching for before assuming a live-DB data fix is out of a sandboxed session's reach.

- 2026-08-25 `kind-robots/t-074` — t-074 was filed on an incomplete diagnosis: "nothing calls POST /api/conductor/overrides" was true but not the actual bug -- a separate, already-wired path (updateProject -> updateLifecycle -> POST /api/conductor/project-state) already synced status/priority to project-overrides.yaml; the real gap was that no UI control ever called it, only read-only badges existed. Also found conductor-manager.vue always routes a project slug to ProjectDetail, never ConductorPage, making ConductorPage's own parallel project-detail rendering path permanently dead code. When a task's note says "nothing calls endpoint X", grep for a second endpoint achieving the same effect before assuming X itself is the fix -- and check the actual component-routing logic, not just which components exist, before deciding where a new control belongs.

- 2026-08-25 `conductor/t-129` — close_task.py's --set note=... silently replaced a task's whole note instead of appending, which is how cthulhuquarium/t-033 and t-034 lost 199 lines of diagnostic history in one routine status flip. set_task_field_text() now refuses to replace a substantial note with a value that doesn't still contain it unless force=True, and close_task.py gained --append-note. Before widening a shared roadmap-editing primitive's default behavior, grep every caller (roadmap_text_patch.py's apply_task_field_ops feeds the automated task-events processor) -- one existing test was exercising the exact destructive pattern the guard now catches, not representative of the real caller's already-safe append-then-set convention.

- 2026-08-25 `mandarin-tutor/t-010` — A task's first implementation slice can merge (kind_robots PR) cleanly at status:review with no reconciliation checkpoint following. Reviewer sweeps should run check_pr_merged_drift.py every session, not only when a task looks stuck -- this one merged and sat 10+ minutes before the drift script caught it.
- 2026-08-25 `mandarin-tutor/t-005` — Keep target-blind speech recognition separate from reference-aware pronunciation feedback, and keep generated lexical facts visibly distinct from pinned dictionary/source data. Durable media identity belongs server-side so requested cards survive reloads and future native clients.
- 2026-08-25 `mandarin-tutor/t-001` — Keep ASR transcript and acoustic pronunciation evidence separate. Reusing the existing YIN pitch detector avoided a second speech-analysis stack. Kind Robots shared components must use container-responsive grid sizing, and Nitro $fetch calls with dynamic route strings must pin both generics.
- 2026-08-25 `cthulhuquarium/t-009` — close_task.py's --set note=... substitutes the roadmap note field rather than extending it, which silently discarded t-009's original task-spec note the same way it discarded t-033/t-034's investigative history minutes earlier (fixed by hand in kind_robots-adjacent conductor PR #2816). Caught and fixed before this close-out PR opened by re-adding the original note ahead of the DONE summary. The script itself is still unfixed -- every future close-out with `--set note=` is one keystroke away from repeating this. Worth a dedicated follow-up task (append-by-default or an explicit --append-note flag) rather than relying on every future session to catch it by hand, as this one and the #2816 session did.


---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-26T02:38:41Z_
