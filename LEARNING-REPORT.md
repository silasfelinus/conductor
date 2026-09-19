# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-19T10:18:59Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1058**
- Outcomes: blocked: 17, cancelled: 1, done: 1040
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
| art-archive | 23 | 100% |
| art-generator-connect | 3 | 100% |
| brainstorm | 26 | 96% |
| butterfly-gallery | 26 | 96% |
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
| lora-ingestion | 1 | 100% |
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
| software | 1041 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 35 |
| transient | 17 |
| actionable | 16 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 47% success over 17 closed tasks; aim the next kaizen task here
- failure category `quality` — 35 occurrences; look for the shared cause across its records
- failure category `transient` — 17 occurrences; look for the shared cause across its records
- failure category `actionable` — 16 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-19 `art-archive/t-027` — Reviewed and merged another session's stalled work (REVIEWING marker 46+ minutes past its 20-minute TTL, PR untouched since): the task's original premise (an integration check against COMFY workflow construction) did not match the actual code path, and the Worker correctly pivoted to testing the real risk (a JSON storage round trip) instead of building a test for a code path that doesn't exist -- worth trusting a Worker's documented investigation over a task's original wording when the two conflict, provided the PR explains why. Separately: the Worker's own kaizen task and this session's own concurrent kaizen task both independently claimed the same next_free_task_id (t-033) because each was computed against a different stale view of origin/main -- a real collision, caught only because merging the second PR surfaced a git conflict at the same file location, not by the id-reuse detector alone (it validates the final merged state, not concurrent claims in flight). Resolved by keeping both entries and renumbering the later one to t-034 rather than dropping either.
- 2026-09-19 `art-archive/t-028` — archiveEntryId/archivePresetId were already tagged onto every ArtJob payload for provenance (t-016) but never read back for display -- worth checking whether a 'surface X status' kaizen task can be satisfied entirely by reading data already being written, before assuming a new write path or schema field is needed. Also: a full production Docker build check can take ~15 minutes on this repo's PRs, well past the point most other checks finish -- worth budgeting for it rather than assuming CI is stuck when 53/54 checks are green and one is still running.
- 2026-09-19 `art-archive/t-019` — A regex negative-lookahead across a multi-line [\s\S]*? span cannot reliably prove a token is ABSENT from a function body -- it only checks one anchor point, not every position -- so it passed trivially on a first attempt to verify runDryRun() never calls a write path. Brace-matched extraction of the actual function source span, then a plain substring search on that extracted text, is the sound way to assert absence; also caught a false positive from a console.log string that literally contained the text of a forbidden call name as documentation, not an actual invocation. Separately: read the existing write-path code (importArchiveFile's hardcoded isPublic=false/isMature=true) before assuming a 'verify no privacy leakage' task needs new machinery -- the invariant was already there and already tested by test:art-archive-importer.
- 2026-09-19 `art-archive/t-023` — Reviewer rejected pass 1 for a static contract-verifier regex whose source-order assumption (UNMATCHED before evidence.name/evidence.hash) did not match formatOutcome()'s real build order (name -> hash -> weight -> UNMATCHED), even though the runtime output was already correct -- a reminder that a new regex-based contract check needs to be verified against the actual source it's asserting on, not just against the expected rendered string. The retry's one-line regex fix (matching the real order) landed clean on pass 2.
- 2026-09-19 `art-archive/t-018` — A task note listing five things (thumbnails, indexed filters, incremental hashing, bounded concurrency, resumable scans) was not one task -- two of the five (indexed filters, bounded concurrency) were already done or a small addition, and two more (real thumbnails, resumable scans) are genuinely separate, larger design surfaces (an image-resizing pipeline; persisted scan-cursor state). Landing the one clearly-scoped, testable core (incremental size/mtime caching) and splitting the rest into two named follow-on tasks (t-029, t-030) kept this a same-session, first-pass close instead of a half-finished multi-part PR. Also: vue-tsc caught a real nullable-field bug (ArchiveEntry.fileSize/fileMtime are Int?/DateTime? for pre-t-003 rows) that a hand-review of the Prisma schema before writing the cache-loader would have caught first -- worth checking a model's actual nullability before assuming a field is always populated.
- 2026-09-19 `art-archive/t-016` — The narrow-adapter framing worked cleanly here: buildArchiveEnqueuePayload() only builds a base ArtJob payload from ArtImage fields and merges the chosen preset via t-025's existing applyArchivePresetToPayload, so the endpoint itself stayed thin glue code. The 'no premature file removal' requirement needed no new schema/tracking field at all -- it falls out for free from the endpoint never calling any file-mutating or isActive-touching code path.
- 2026-09-19 `art-archive/t-015` — Reviewer rejected pass 1 for a deterministic verifyDisabledAffordances failure (a batch-scoped Clear button used :disabled instead of v-if with no selection); the retry matched the existing correct pattern already in the same file, landed clean on the second pass, and merged as kind_robots#2866 -- a reminder that this project's PRs should run the full Contract verifiers suite locally before pushing, not just feature-scoped test scripts.
- 2026-09-19 `art-archive/t-026` — Extracting a duplicated union-narrowing guard into one shared helper (narrowToPngMetadata) removes the exact TypeScript-compile-error class kind_robots#2824 hit, since the next module reading .a1111/.comfy can no longer re-derive the guard incorrectly by hand.
- 2026-09-19 `butterfly-gallery/t-014` — A tight cluster of ArtJobs changing status within seconds of each other is at least as likely to be a deliberate administrative/human action as a queue-system glitch -- do not requeue or otherwise "correct" it without first checking for very recent out-of-band human steering beyond CONTROL.md and the task's own note. When a corrective action is needed, prefer the narrowest reversible one (a cancel-shaped action) over one whose semantics you have not read closely (DELETE removed the ArtJob rows outright rather than restoring CANCELLED status).
- 2026-09-19 `butterfly-gallery/t-032` — A kaizen task filed from a PR body's own suggestion, claimed and implemented in the same session as the PR it came from, landed cleanly: reading five sibling route files to extract their shared guard shape (admin gate -> invalid-id 400 -> missing-entry 404 -> mutation) before writing the contract test, then adversarially verifying the test actually fails when a guard is removed, caught what a superficial "checks that the routes exist" test would have missed.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-19T10:18:59Z_
