# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-10T07:40:32Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **560**
- Outcomes: blocked: 13, cancelled: 1, done: 546
- Success rate: **98%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 64 | 98% |
| alexa-integration | 2 | 100% |
| animation-manager | 13 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 6 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 25 | 100% |
| conductor | 70 | 100% |
| conductor-app | 2 | 100% |
| davinci | 2 | 100% |
| digital-storefront | 28 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 4 | 100% |
| interface-vision | 82 | 100% |
| kind-robots | 49 | 98% |
| kindrobots-unraid | 5 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 48 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 1 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 2 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 545 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 11 |
| actionable | 9 |
| transient | 9 |
| scope | 2 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `quality` — 11 occurrences; look for the shared cause across its records
- failure category `actionable` — 9 occurrences; look for the shared cause across its records
- failure category `transient` — 9 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-10 `storybook/t-014` — When moving grandfathered UI out of an allow-listed component, do not transfer the exception to the new file. Satisfy both ratchets: keep interact components thin and make newly extracted working surfaces container-responsive.
- 2026-08-10 `kind-robots/t-060` — Live-sanitizing a slug field on every keystroke (lowercase + collapse + trim) breaks manual typing of hyphenated slugs: a hyphen is trailing (and therefore gets trimmed) the instant it's typed, before the next character lands, so "my-project" becomes impossible to type by hand. Split it into a light per-keystroke filter (lowercase, drop disallowed chars only) plus a full slugify() on blur/submit instead. Also: attaching `.statusCode` to a thrown Error in a Pinia store action is a safe additive way to let one caller branch on HTTP status (409 vs. other) without touching the route/API contract or breaking other callers that only read `.message`.

- 2026-08-10 `kind-robots/t-059` — A "document every live surface" task benefits from an exhaustive code-level grep (grep -rn "\.project\.create(" server/ scripts/) rather than trusting the audit note's own count -- t-058's note said "at least three" then "all five" for what turned out to be 4 distinct route files, and the grep also surfaced that Surface 1's description (sync_projects.py -> per-project POST /api/projects) and Surfaces 2/3's "auto-Todo not yet implemented" pitch notes were themselves stale against current code (scripts/sync_kind_robots_projection.py -> POST /api/conductor/sync bulk upsert; createProjectWithScaffoldTodo() already files the Todo). Fixing those in the same docs-only pass kept the doc actually accurate instead of technically-task-complete-but-still-wrong.

- 2026-08-10 `kind-robots/t-058` — An audit task's own findings can be correct while its proposed follow-up disposition is wrong: this project's BOUNDARY.md routes any shared-backend/API change through pitches/ first, and SHARING-SPEC.md explicitly labels its own documented Grant API surface "illustrative -- routes, not committed contracts" -- filing that as a direct `ready` implementation task (first attempt, PR #2002) is a scope/process violation even though the underlying evidence was sound. Retry preserved the audit doc unchanged and only revised the disposition: kept genuinely local/front-end/docs-only findings as `ready` tasks, and wrote a pitch file per backend-touching finding, bundling closely-coupled backend follow-ups (Grant API + its two route migrations + the UI that depends on it) into one pitch rather than four separate approval asks for one capability.

- 2026-08-10 `kind-robots/t-057` — contract-tests.yml is explicitly DB-free ("No database or Nuxt build is needed"), so a "behavioral" contract test for a database-writing code path has to be a source-inspection test (assert.match against readFileSync'd source), not a live integration test -- matching the existing verify*.ts convention rather than reaching for a real Prisma/DB fixture that this CI job structurally cannot run. Also: when SQL identifiers are backtick-quoted inside a template literal, they appear on disk as an escaped \` pair, not a bare backtick -- normalize (.replaceAll('\\`', '`')) before regex-matching raw SQL source, or the match silently fails on the escaping, not the content. Verified the new assertions actually catch a regression (not vacuously true) by manually breaking each of the three invariants and confirming the test failed, before wiring it into CI.

- 2026-08-09 `kind-robots/t-056` — A source-shape "guard test" (utils/scripts/verifyDatabasePoolDefaults.ts asserting a literal code string still appears in a route file) can break on an otherwise correct, intentional refactor -- the fix is usually to relocate the new behavior so the guarded shape survives unchanged, not to weaken the guard. Also: don't trust a PR body's "How I verified" section at face value -- independently re-running eslint/vue-tsc/the specific failing script on the actual current head caught a real TS2339 the Worker's own note had claimed was code/CI verified.

- 2026-08-09 `interface-vision/t-104` — Slice 26 of the kr-container consistency migration: four components (add-bot, add-character, add-reward, add-scenario) sharing an identical root class string were an exact byte-for-byte match for kr-container-wide's own @apply, found via a plain grep for the mx-auto/w-full/max-w-7xl triple across the repo rather than a codemod. Landed clean on the first pass, zero deviation from the established verification method (eslint, vue-tsc, layout-contract, git-stash-diffed prettier baseline check).

- 2026-08-09 `kind-robots/t-014` — When a roadmap task's original implementation gap is already present on current main and later human evidence confirms the feature works, reconcile and close the stale task instead of spawning a duplicate patch or repeatedly returning it to the human.
- 2026-08-09 `interface-vision/t-104` — Slice 20 of the kr-panel-flat consistency migration: applying t-116's corrected codemod scan to its own newly-surfaced 47-occurrence pool landed clean on the first pass with zero deviation from the established slice 8-19 method (exact-match substitution, git-stash-diffed prettier reformatting, compiled-CSS verification for skips). No new lesson beyond t-116's own record -- filed mainly so the outcome ledger reflects that the corrected pool is real, landable work, not just a diagnosis.

- 2026-08-09 `interface-vision/t-116` — A codemod's own "pool exhausted" conclusion is only as good as its scan boundary. kr_panel_codemod.py used re.search for the FIRST </template> in a file to find the template region's end, but an SFC can nest a named-slot/conditional <template v-if #slot> block that closes with its own </template> well before the real end -- silently truncating the scan and hiding every real candidate after it. Two prior slices (15, 18) trusted "0 automatable substitutions" as proof the pool was empty when it was actually an artifact of the scan bug. Fix: scan for the LAST </template> in the file, not the first. Re-running the corrected scan surfaced 47 previously-invisible candidates across 21 files in one pass -- a reminder that a static-analysis/codemod tool's exhaustion claim needs to be re-derived from its actual scan boundary, not taken at face value from its summary output.


---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-10T07:40:32Z_
