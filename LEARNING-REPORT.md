# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-19T16:26:10Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1069**
- Outcomes: blocked: 18, cancelled: 1, done: 1050
- Success rate: **98%**
- Average passes on successful tasks: **0.2**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 73 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 14 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 11 | 100% |
| approval-portal | 2 | 0% |
| art-archive | 30 | 100% |
| art-generator-connect | 3 | 100% |
| brainstorm | 26 | 96% |
| butterfly-gallery | 29 | 93% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 39 | 100% |
| conductor | 120 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 51 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 24 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 136 | 100% |
| kapowarr | 52 | 100% |
| kind-economy | 10 | 100% |
| kind-robots | 65 | 98% |
| kindrobots-unraid | 9 | 100% |
| lora-ingestion | 2 | 100% |
| mandarin-tutor | 11 | 100% |
| media-watchlist | 12 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 85 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| rainbow-butterflies | 21 | 100% |
| ruler-hooked | 14 | 100% |
| scene-animator | 2 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 30 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 7 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 1052 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 36 |
| transient | 17 |
| actionable | 17 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 47% success over 17 closed tasks; aim the next kaizen task here
- failure category `quality` — 36 occurrences; look for the shared cause across its records
- failure category `transient` — 17 occurrences; look for the shared cause across its records
- failure category `actionable` — 17 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-19 `art-archive/t-034` — Tagging a new durable field onto an existing payload builder (mirroring how archiveEntryId/archivePresetId were already tagged) is a clean, low-risk change when every consumer already reads the payload generically -- no schema migration needed, just thread the field through the read path and the frontend type.
- 2026-09-19 `art-archive/t-032` — A third caller (this dry-run endpoint) reimplemented the same matchArchiveResources() aggregation t-037 was already filed to consolidate between the CLI and the t-031 import endpoint -- widen an existing consolidation task's scope instead of filing a near-duplicate kaizen task when a new PR reintroduces the same pattern.
- 2026-09-19 `art-archive/t-031` — Extending an existing admin endpoint to surface an already-built pure helper (matchArchiveResources, from t-023) is a clean, single-file, additive change when the helper's signature is reused as-is -- no new abstraction needed for a reporting-only slice.
- 2026-09-19 `art-archive/t-035` — The task was written as conditional ("if large originals turn out to be common"), but this sandbox has no way to measure real archive file sizes (private archive root lives on Silas's Unraid host, not reachable here, and ArchiveEntry stores no fileSize field). Built the medium cache unconditionally instead of blocking on an unmeasurable premise -- it mirrors the existing thumbnail-cache architecture exactly, is low-risk/reversible, and never hurts even if large originals turn out to be rare. Worth considering whether ArchiveEntry should record fileSize at scan time so a future session actually could measure this.
- 2026-09-19 `butterfly-gallery/t-016` — A task's original approach can go stale without its own status changing -- t-016 said to build the runway using the procedural Butterfly Scouts DOM/CSS renderer, but Silas's same-day update to ANIMATION-SHOT-LIST.md switched the canonical runway approach to AI-video (LTX/WAN) and explicitly forbade that substitution. Caught by reading the production motion contract directly rather than trusting the task note; flagged needs-human (soft) instead of building the now-wrong thing or silently reinterpreting scope across three related tasks (t-016/t-031/t-033).
- 2026-09-19 `butterfly-gallery/t-034` — A docs-only PR handoff can still fail "Validate Worker PR handoff" on a single missing heading (here, "### Notes for reviewer") even when every other required section is present and the content itself is correct -- the Reviewer edited the PR body directly to add the missing heading rather than kicking the whole task back to the Worker for a retry, since it was a template gap, not a quality/scope problem with the diff.
- 2026-09-19 `butterfly-gallery/t-014` — The shot list/task-note description of the video-enqueue payload omitted that renderScale is required for engine ltx/wan independent of presetId (the server never derives dimensional defaults from a preset id) -- reading the actual server route source before submitting caught this before it caused a rejected request; worth documenting the full required-field contract once rather than re-deriving it from source each time (see t-034).
- 2026-09-19 `art-archive/t-036` — A tracked counter (ArchiveScanResult.cacheHitCount) that is only ever printed as a raw number is easy to skim past when it silently regresses; pairing it with a percentage of the total in the same log line makes a partial cache-engagement regression visible without a dedicated benchmark. Also confirmed the two reporting paths' denominators (scan.files.length vs result.scannedFileCount) were actually equal before reusing the same formatting in both, rather than assuming.
- 2026-09-19 `lora-ingestion/t-009` — Capability filters must derive from the same taxonomy as the scanner/downloader; a separate hand-curated UI list silently fell behind Krea, Flux.2, ZImage, Qwen, and other supported families.
- 2026-09-19 `art-archive/t-030` — Before building a titled feature (persisted scan checkpoints), the Worker benchmarked the underlying assumption first and found a hidden cache-correctness bug instead (float vs truncated-integer mtime comparison defeating the existing hash cache); fixing that made the walk cheap enough that checkpoint tracking wasn't needed at all -- measure before building is cheaper than building the wrong thing.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-19T16:26:10Z_
