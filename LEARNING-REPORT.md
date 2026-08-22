# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-22T02:31:36Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **722**
- Outcomes: blocked: 15, cancelled: 1, done: 706
- Success rate: **98%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 67 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 13 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 8 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| brainstorm | 21 | 95% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 25 | 100% |
| conductor | 78 | 100% |
| conductor-app | 4 | 100% |
| davinci | 6 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 83 | 100% |
| kapowarr | 47 | 100% |
| kind-economy | 6 | 100% |
| kind-robots | 50 | 98% |
| kindrobots-unraid | 5 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 72 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 14 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 6 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 16 | 44% |
| software | 706 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 14 |
| actionable | 10 |
| transient | 9 |
| scope | 2 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 14 occurrences; look for the shared cause across its records
- failure category `actionable` — 10 occurrences; look for the shared cause across its records
- failure category `transient` — 9 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-22 `ai-art-academy/t-070` — A finite backfill task's coverage denominator silently going stale after the thing it counts (academyStyles.ts's canonical style list) grows is a real, recurring failure mode -- historical t-013 correctly reached 21/21 for its own cohort, but nothing kept that "21" honest as the curriculum expanded to 47 styles, so 26 lessons sat with no Example Works strip for roughly a month, completely undetected. The fix that generalizes: any "N/N complete" coverage claim needs its verifier computing the denominator from the CURRENT source of truth every run (here, academyStyles.length), never from a number written down when the task closed. Pairing that with an explicit, named exceptions file (config/academy-example-work-exceptions.json) rather than just lowering the bar to "however many exist today" is what makes a real partial-coverage state distinguishable from silent drift -- every uncovered item must resolve to either real coverage or a reasoned, tracked gap, never neither. Also confirmed a sourcing pattern worth remembering: an open-access museum API returning is_public_domain: true for the WORK does not guarantee the DIGITIZATION is unrestricted -- AIC's own API returned is_public_domain: false for both american-regionalism's named artists (Grant Wood incl. American Gothic, John Steuart Curry) despite both clearing the death-date prong, matching the same rights-society-restriction pattern the historical t-013 TALKBACK already found for Kandinsky/Klee/Gris -- a green light from one open-access API is necessary but not sufficient; check the specific work, not just the artist's era. Finally, this sandbox's Cloudflare-bot-challenged access to artic.edu's own IIIF image CDN (confirmed via a direct HEAD request returning cf-mitigated: challenge, while api.artic.edu's JSON search API worked fine) explains why the file's existing AIC- sourced exampleWorks entries route through Wikimedia Commons instead of citing AIC directly -- worth checking upload.wikimedia.org reachability first for any future AIC-collection sourcing rather than re-discovering the CDN block each time.

- 2026-08-22 `ai-art-academy/t-069` — A "verify current production" task is only as good as its weakest-evidence criterion -- splitting each acceptance item explicitly into LIVE (real HTTP against kindrobots.org/api responses) vs. SOURCE-traced (client-hydration-gated UI this sandbox's broken headless Chromium can't reach) kept the note honest about what was actually proven vs. inferred, per AGENTS.md's explicit "never blur verified and assumed" rule. For the one criterion needing a real render (a completed Kontext remix), KR_API_TOKEN as a Bearer token against the same server route/workflow builder the UI calls (POST /api/art/enqueue -> poll GET /api/art/queue/:id -> GET /api/art/image/:id?includeImageData=true) produced a genuine end-to-end artifact (ArtJob 9009, ArtImage 18263) that could be decoded and visually inspected, not just a "status: DONE" proxy -- this is the strongest verification shape available to a sandboxed session with no browser and is worth reusing for any future "does generation actually work in prod" task. Also worth remembering for next time: freshly-generated ArtImages in production have null path/imagePath and are delivered as inline base64 -> data: URI, not through the static /images/** bridge that lesson/starter assets use -- a future check that assumes every ArtImage has a static path will get a false negative.

- 2026-08-22 `ai-art-academy/t-071` — Historical t-025 backfilled failureMode for every movement that existed at closure, but the curriculum expanded afterward with no coverage task tracking the new denominator -- the same drift pattern t-070 hit for exampleWorks. Re-measuring the canonical style list before editing (47 entries, not the roadmap note's stale "48") caught a small inaccuracy before it propagated into a false 12-vs-11 count. Also added a lightweight coverage contract (pass/fail on any style missing failureMode and not in a documented exceptions map) rather than only fixing the current gap -- the exact fix t-025 itself didn't have, which is why this task existed at all. Choosing t-071 over the also-ready but much larger t-070 (27-lesson rights-clearance content task) in the same cycle was deliberate scope discipline: t-070 got flagged as a kaizen suggestion to decompose rather than attempting all 27 lessons in one pass.

- 2026-08-21 `brainstorm/t-027` — Scoping a broad "evaluate N surfaces" task by shipping the cheapest one first and filing the rest as named follow-ups (t-028 for Reward) kept the diff small (3 files) and avoided forcing a button onto Prompt, which has no standalone detail view yet. A surface with an existing adapter but no UI entry point (Scenario, from t-014) is the cheapest next slice on this kind of task -- check BRAINSTORM_SOURCE_ADAPTERS for already-wired-but-untriggered adapters before starting from scratch on any surface.

- 2026-08-21 `brainstorm/t-019` — Claimed and dispatched implementation for a task whose deliverable turned out to already exist, shipped by two earlier tasks (t-013, t-014) days prior. No harm done since the dispatched agent verified against actual shipped code before writing anything and correctly declined to manufacture a diff -- but the roadmap task itself should have been closed or re-scoped at the moment t-013/t-014 shipped equivalent coverage, not left `ready` to be rediscovered and re-investigated by a later cycle. When a task ships coverage that satisfies a different, still-open task's stated scope, check for and update that task in the same close-out cycle.

- 2026-08-21 `brainstorm/t-017` — Found the established precedent (modelBuilderStore.ts's pollAsyncArtJob -> finalizeQueuedArtImage split) before designing a bespoke "verify the delivered image" path for Brainstorm's own enqueue/poll loop -- reusing it caught more than a hand-rolled check would have (finalizeQueuedArtImage re-fetches the ArtImage row itself, not just trusting the job's artImageId field, and routes through the same collection-attachment semantics every other art surface uses). Also worth noting: a "failed" outcome had literally zero persisted signal before this task -- only a transient, session-local busy flag distinguished "generating" from "never tried" or "gave up," so any per-candidate/per-item async operation with a client-visible outcome should be checked for this same gap (state that only lives in memory during the operation, with nothing surviving a reload once it ends) before assuming existing coverage is complete.

- 2026-08-21 `brainstorm/t-016` — Clean first-pass success on a real feature build (not a bugfix cycle): grepping for existing-but-unused scaffolding (BrainstormCandidate.meta.art) before implementing prevented inventing a parallel tracking mechanism, and it also surfaced a genuine latent bug (client localStorage round-trip silently dropping a JSON meta field the server path already preserved generically) that a narrower "just wire the button" implementation would have missed entirely. Worth generalizing: when a Prisma model's `meta`/JSON column is preserved generically server-side but the client has a hand-written normalizer that only lifts out known sub-fields, any new sub-field added to that type needs an explicit normalizer update or it silently vanishes on the client-only persistence path (localStorage/autosave) even though the server path never had the bug.

- 2026-08-21 `model-builder/t-029` — Cycle 30 of a long-running recurring bug-hunt task: a transient, client-local 'in-progress' marker written directly onto item.stages before an async call (commitItem's COMMIT marker, generateItemAsset's GENERATE_ASSETS marker) has no store-level enforcement stopping an unrelated stageStatuses-diffing write from reading and re-persisting it as real. Three of four batch functions lacked the isItemManualActionInFlight guard their sibling autoBuildItem already had -- the fourth instance of this exact shape across cycles 25, 28, and 29 (see cycle 20's and cycle 25's own entries in this file). Patching one more call site per cycle works but never closes the class; the durable fix is moving the in-flight flag into a separate ephemeral field never serialized into a stageStatuses payload, the same way artJobId/queueState already are kept out of item.stages.

- 2026-08-20 `kapowarr/t-062` — A prior evaluation doc that names exact measured traps (response shapes, pagination ceilings, a 404-not-JSON edge case) turns an "implement a REST client" task into something closer to transcription than design -- the risk shifts from "did I miss a trap" to "did I quietly widen scope while transcribing it." Re-reading the evaluation doc's own recommendation section against the actual diff before opening the PR (does every field mapping trace to a table row, is every new file/setting/test named in the doc's follow-on task description) is what kept this PR three files instead of six -- the doc's own field tables for `Series`/`overview` rows against `VolumeMetadata`/ `IssueMetadata` could be pasted almost directly into code comments, and the two schema-shape questions the doc explicitly left unmeasured (a `title` field on overview rows, `longest_story.synopsis`) were exactly the two places worth flagging as judgment calls in the PR body rather than silently guessing. Second: an existing sibling provider is not automatically a safe copy source. Reading `metron.py` for the pattern surfaced a real latent bug in it (`test_key()` imports `run` from `backend.base.helpers`, which re-exports `subprocess.run`, not an async runner -- calling `subprocess.run(<coroutine>)` raises, it doesn't return `False`; the sibling `comicvine.py` gets this right via `from asyncio import gather, run, sleep`). Never had a test covering `test_key()`'s actual return value, so it shipped unnoticed. Filed as kapowarr/t-066 rather than folded into this PR, but the general point is that "match the existing provider's pattern" needs the same scrutiny as any other code being read for reuse, not a pass just because it already merged.

- 2026-08-20 `kapowarr/t-063` — A test written to catch a silent regression must be shown to fail against that regression, not merely to pass against current behaviour -- and for an ordering policy this is cheap to do: break the policy deliberately, run the suite, restore from a byte-copy. Doing it here proved the task's premise rather than assuming it. Transposing two rating components failed four tests, but inserting a NEW component above match correctness failed only the new table guard while all 22 pre-existing pairwise tests passed. That is the exact gap the task described, demonstrated instead of argued, and it is the evidence that belongs in the PR body. Second: lexicographic list comparison is what makes a whole-order assertion possible in one place. Because a result degraded at tier N differs from the baseline first at index N, it loses to one degraded at any later tier regardless of magnitudes -- so ranking one result per tier and sorting them reproduces the policy backwards, and six adjacent-boundary assertions collapse into one readable list. Third: when two ranking components share an input (pack preference and issue-number fit both read result['issue_number']), no single result can vary one alone. Patching the component's return value rather than driving it through a real preference is what isolates it -- and the coupling itself is worth writing into the test, since it is otherwise only discoverable by trying and failing to construct the case.


---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-22T02:31:36Z_
