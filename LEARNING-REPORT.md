# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-22T14:37:07Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **729**
- Outcomes: blocked: 15, cancelled: 1, done: 713
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
| model-builder | 75 | 100% |
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
| software | 713 | 99% |

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

- 2026-08-22 `appmaker/t-012` — apps.get.ts's pending-scaffold reader only ever recognized one of AppMaker's two self-serve scaffold flows' Todo titles (the monorepo flow's "Scaffold new app '...'", never the external-repo GitHub-integration flow's "Scaffold external app '...' via AppMaker GitHub integration") -- both the Prisma query's title filter and the extraction regex needed updating together, since fixing only one still silently drops the other flow's real, open Todos from the UI. Same "an endpoint reachable via direct API call, even with no front-end wired up yet, is still worth defending" precedent the prior cycle set for this exact pair of routes' slug-collision guard -- when two routes share a naming convention a downstream reader depends on, audit every reader against every writer, not just the one the current UI happens to call.

- 2026-08-22 `model-builder/t-029` — Cycle 46: closed the exact gap cycle 45's own kaizen note flagged as left open -- pitch/fieldsDraft/promptDraft were capped at MAX_DRAFT_TEXT_LENGTH on the item PATCH path but not on the run CREATE route's own items mapping, even though both write the same @db.Text columns. A cap added at one write path for a shared field is only half the fix until every other write path into that same column is audited too -- the same "one-way-clear-gap" shape as cycle 41/42's lastAutoBuildOutcome/statusMessage bugs, just for a validation cap instead of a state-clearing call. Importing the shared constant (MAX_DRAFT_TEXT_LENGTH) rather than hardcoding a second copy of the same number, plus a guard script asserting the import is actually used, is what keeps two independent write paths for the same column from drifting apart again silently.

- 2026-08-22 `model-builder/t-029` — Cycle 42: the same one-way-clear-gap defect shape from cycle 41 (lastAutoBuildOutcome) recurred in a completely different ephemeral field -- state.statusMessage/statusTone, the global status banner -- because eight mutating functions (approveStage, rejectStage, reopenStage, updatePitch, updateFields, updatePrompt, batchSetField, batchApproveStage) never called the store's own clearStatus() at the start of a fresh attempt, even though seven siblings already did. A single well-known bug class is worth checking function-by- function across an entire store rather than assuming one comprehensive fix closes the category -- the fix pattern (call an existing clear helper at the start of every mutating path, not just the ones that happened to need it last time) generalizes directly. Also reconfirmed (4th independent instance) that a delegated background agent's "waiting on a CI timer" self-report is not a real block -- the coordinating session must poll CI itself and merge, then explicitly tell the sub-agent to stop via SendMessage. Promoted this from a per-cycle TALKBACK observation to AGENTS.md hard safety rule 13.

- 2026-08-22 `model-builder/t-029` — Cycle 41: an ephemeral, client-only status field (BuildItem.lastAutoBuildOutcome) that a badge reads but no repair path ever clears is the same defect shape as cycle 30's stray in-progress marker -- any UI flag set as a side effect of one code path needs an explicit audit of every OTHER path that can legitimately supersede it (manual edit, AI redraft, single-item commit), not just the path that originally set it. Also: verifying a fix by running the full sibling test suite is worth doing even when it feels like overkill -- it surfaced a second, unrelated, pre-existing latent bug (a guard script's own comment-blind brace scanner) that this cycle's unrelated edits happened to expose as a false failure; treating a sibling guard's confusing break as evidence of a bug in that guard's own tooling, not as evidence the new change was wrong, was the right call.

- 2026-08-22 `ai-art-academy/t-075` — A shared coverage-contract helper generalizes cleanly across per-style (denominator = academyStyles.length) and per-nested-field (denominator = named-artist count) verifiers as long as the denominator stays a parameter rather than being hardcoded inside the helper.
- 2026-08-22 `ai-art-academy/t-072` — A genuinely large curation task (portrait likenesses for 116 named artists across 47 styles) scoped cleanly by following t-070's precedent: ship the schema/tooling foundation plus a real, well-verified partial batch (8 artists via the Met Collection API), file an honest follow-up for the rest rather than either stalling or rushing a low-quality full pass. The coverage verifier was deliberately built as a reporting tool, not a 100%-or-exception hard gate, since partial coverage is the correct steady state here (unlike exampleWorks' full-denominator gate) -- copying a sibling verifier's hard-gate shape without checking whether the underlying task actually wants 100% coverage would have been the wrong contract. Also: an unqualified `git checkout -- <file>` used to discard one unwanted change (a full-file prettier reformat) silently discarded a second, wanted uncommitted change to the same file in the same command -- stage or copy aside real edits before reverting formatting noise in the same file, rather than trusting `git checkout --` to be selective.

- 2026-08-22 `ai-art-academy/t-073` — Kaizen-sourced tooling fix (grouped error-signature breakdown for GET /api/art/queue/stats, ai-art-academy/t-069's close-out pain point) landed clean across a kind_robots + conductor companion-PR pair. Separately: a background subagent given "verify CI, merge when green" as part of its scope has no way to schedule its own wait for external CI completion and can get stuck looping "waiting for a background timer" across several turns without one ever arriving -- the parent session had to take over the final re-check-and-merge step directly. Future delegated cycles whose scope includes a merge-when-green step should either have the parent handle that step, or be told explicitly to re-check synchronously/immediately rather than attempt a multi-turn wait.

- 2026-08-22 `ai-art-academy/t-070` — A finite backfill task's coverage denominator silently going stale after the thing it counts (academyStyles.ts's canonical style list) grows is a real, recurring failure mode -- historical t-013 correctly reached 21/21 for its own cohort, but nothing kept that "21" honest as the curriculum expanded to 47 styles, so 26 lessons sat with no Example Works strip for roughly a month, completely undetected. The fix that generalizes: any "N/N complete" coverage claim needs its verifier computing the denominator from the CURRENT source of truth every run (here, academyStyles.length), never from a number written down when the task closed. Pairing that with an explicit, named exceptions file (config/academy-example-work-exceptions.json) rather than just lowering the bar to "however many exist today" is what makes a real partial-coverage state distinguishable from silent drift -- every uncovered item must resolve to either real coverage or a reasoned, tracked gap, never neither. Also confirmed a sourcing pattern worth remembering: an open-access museum API returning is_public_domain: true for the WORK does not guarantee the DIGITIZATION is unrestricted -- AIC's own API returned is_public_domain: false for both american-regionalism's named artists (Grant Wood incl. American Gothic, John Steuart Curry) despite both clearing the death-date prong, matching the same rights-society-restriction pattern the historical t-013 TALKBACK already found for Kandinsky/Klee/Gris -- a green light from one open-access API is necessary but not sufficient; check the specific work, not just the artist's era. Finally, this sandbox's Cloudflare-bot-challenged access to artic.edu's own IIIF image CDN (confirmed via a direct HEAD request returning cf-mitigated: challenge, while api.artic.edu's JSON search API worked fine) explains why the file's existing AIC- sourced exampleWorks entries route through Wikimedia Commons instead of citing AIC directly -- worth checking upload.wikimedia.org reachability first for any future AIC-collection sourcing rather than re-discovering the CDN block each time.

- 2026-08-22 `ai-art-academy/t-069` — A "verify current production" task is only as good as its weakest-evidence criterion -- splitting each acceptance item explicitly into LIVE (real HTTP against kindrobots.org/api responses) vs. SOURCE-traced (client-hydration-gated UI this sandbox's broken headless Chromium can't reach) kept the note honest about what was actually proven vs. inferred, per AGENTS.md's explicit "never blur verified and assumed" rule. For the one criterion needing a real render (a completed Kontext remix), KR_API_TOKEN as a Bearer token against the same server route/workflow builder the UI calls (POST /api/art/enqueue -> poll GET /api/art/queue/:id -> GET /api/art/image/:id?includeImageData=true) produced a genuine end-to-end artifact (ArtJob 9009, ArtImage 18263) that could be decoded and visually inspected, not just a "status: DONE" proxy -- this is the strongest verification shape available to a sandboxed session with no browser and is worth reusing for any future "does generation actually work in prod" task. Also worth remembering for next time: freshly-generated ArtImages in production have null path/imagePath and are delivered as inline base64 -> data: URI, not through the static /images/** bridge that lesson/starter assets use -- a future check that assumes every ArtImage has a static path will get a false negative.

- 2026-08-22 `ai-art-academy/t-071` — Historical t-025 backfilled failureMode for every movement that existed at closure, but the curriculum expanded afterward with no coverage task tracking the new denominator -- the same drift pattern t-070 hit for exampleWorks. Re-measuring the canonical style list before editing (47 entries, not the roadmap note's stale "48") caught a small inaccuracy before it propagated into a false 12-vs-11 count. Also added a lightweight coverage contract (pass/fail on any style missing failureMode and not in a documented exceptions map) rather than only fixing the current gap -- the exact fix t-025 itself didn't have, which is why this task existed at all. Choosing t-071 over the also-ready but much larger t-070 (27-lesson rights-clearance content task) in the same cycle was deliberate scope discipline: t-070 got flagged as a kaizen suggestion to decompose rather than attempting all 27 lessons in one pass.


---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-22T14:37:07Z_
