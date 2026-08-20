# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-20T16:49:36Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **706**
- Outcomes: blocked: 15, cancelled: 1, done: 690
- Success rate: **98%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 64 | 98% |
| alexa-integration | 6 | 100% |
| animation-manager | 13 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 8 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| brainstorm | 17 | 94% |
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
| kapowarr | 39 | 100% |
| kind-economy | 6 | 100% |
| kind-robots | 50 | 98% |
| kindrobots-unraid | 5 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 71 | 100% |
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
| software | 690 | 99% |

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

- 2026-08-20 `kapowarr/t-045` — Read a multi-part task's code before believing its note about what is left. This one read "add safe extraction for CBR/RAR first, then other practical formats" as though no part had shipped; CBR/RAR had in fact been in comic_reader.py since the reader landed, so the whole task was its second clause. A roadmap note is a snapshot of intent at filing time and goes stale silently -- three minutes of grep resized the work before any of it was planned wrong. The other lesson is that copying an existing pattern is not the same as copying its threat model. list_tar_pages/read_tar_member mirror the ZIP and RAR pairs almost line for line, and mirroring them exactly would have shipped a file-read primitive: a tar, unlike a zip, can carry symlink members, and extractfile() resolves the link target, so a member named 001.jpg pointing at /etc/passwd would have been served straight back through the authenticated page endpoint. The guard is one isfile() check, but nothing in the pattern being copied would have suggested needing it. When adding a sibling format, ask what the new container can express that the old one could not.

- 2026-08-20 `kapowarr/t-035` — Before writing an adapter for a third-party API you cannot reach, spend the time to read that service's own implementation, not just its documentation, and not memory. NZBGet's published API docs omit a required parameter from `append`'s argument list and ship an example passing 10 of 11 arguments; either would have produced a client that fails on its very first call. Reading the source also surfaced three facts that changed the design rather than the comments -- JSON-RPC 1.1 with no `jsonrpc` member in replies, post-processing happening in the queue so history is terminal, and the firm absence of any per-group download rate. Where a value's vocabulary is still uncertain, key on its stable part (a status prefix) and default the unknown case to the safe reading, so the adapter survives versions nobody here can test against.

- 2026-08-20 `kapowarr/t-034` — When adding an unattended path into an existing pipeline, the reusable seam is usually the one the manual version already uses -- here manual_import_files() plus the mass_rename/mass_convert/mass_process_files trio, rather than fabricating the Download object post_processing.py is built around for something that was never downloaded. Two things worth copying next time: enforce a stated scope boundary in code as well as prose (the "don't compete with continuous import" requirement became both a never-create-a-volume rule and a settings-level folder-collision check, from both sides), and check whether the repo has recently fixed the same shape of problem elsewhere -- a just-landed "large library stalls a background importer" fix was the direct reason this feature got a per-pass volume index instead of an O(files x volumes) database walk.

- 2026-08-20 `conductor/t-120` — A roadmap task in a status outside the documented lifecycle is invisible, not deferred -- every selection path matches `status == "ready"` exactly, so it never surfaces as ready work, a gate, or blocked. Eight such tasks hid the entire remaining backlog of the portfolio's top-priority project, and four scheduled cycles in one day silently fell through to a 12th-ranked recurring polish task as a result. audit_roadmaps.py had been reporting all eight as errors the whole time but is advisory and always exits 0 -- the second time an advisory-only finding (after DUPLICATE_TASK_ID) had to be promoted into validate_roadmaps.py's hard CI gate after it had already caused real damage. When a cycle reports "no claimable work" for a project ranked above the one it picks, verify the claim against a status histogram instead of recording it.

- 2026-08-20 `model-builder/t-029` — Cycle 25 of a long-running recurring polish task: two sibling store-wide "operation in flight" flags (state.autoBuilding for whole-run auto-build, state.batchingOutputKey for group batch ops) had each grown their own exclusion logic over many prior cycles without ever being cross-checked against each other, letting a user start two independent, interleaved orchestration passes over the same run's items concurrently. When a codebase accumulates many narrow single-purpose "in flight" guards over successive cycles, it's worth periodically tracing all such flags against each other as a set, not just auditing each one against the actions it already knows to check.

- 2026-08-20 `davinci/t-021` — Slice 10 of a recurring polish task: reading the prior slice's own REMAINING note as the literal scope handoff (rather than re-auditing the whole file) surfaced a real gap the narrower chapterRegion focus-loss fix (slice 9) couldn't catch on its own -- a nested click whose state transition unmounts the outer container the inner region lives inside, not just the inner region itself. Confirming this required tracing the actual call path (resolveLife -> resumeRun -> phase mutation) rather than assuming two focus-restoring regions at different nesting depths are independent.

- 2026-08-20 `conductor/t-119` — The status:review transition (AGENTS.md step 7) was left ambiguous between claim_task.py's sanctioned direct-to-main exception and close_task.py's branch+PR pattern -- resolved by routing it through close_task.py (which already supports arbitrary target statuses, review included) rather than inventing a new script or a new hard-rule-1 exception. model-builder/t-029 cycle 21's STATUS.md merge conflict, doing this transition by hand with set_task_field.py + a manually-managed branch, was a symptom of not using the existing fetch-fresh git plumbing, not evidence that branch+PR is the wrong shape for this transition.

- 2026-08-19 `storybook/t-010` — Cycle 20 of the recurring storybook/t-010 bug-hunt: Dream rows without a first-class Prisma model of their own (Location is just dreamType === 'LOCATION' on the generic Dream table) are easy to under-serve relative to Character/Reward/Scenario/Facet, which each have both a dedicated model and a dedicated detail component with its own "start a story" deep-link CTA. The generic dream-narration.vue detail surface had no such CTA for any Dream type, so seedFromQuery()'s ?location= query key had been dead code with no sender anywhere in the repo since it was added. Worth checking, for any future object type added to Storybook's seed-query set, whether it actually has a first-class detail component or only the generic Dream surface -- the generic surface is the one that silently misses new CTAs.

- 2026-08-19 `brainstorm/t-021` — Adding real behavioral test coverage for Pinia store logic in this repo hits a real environmental wall: a store file that imports another store transitively (brainstormStore.ts -> serverStore -> userStore -> achievementStore) can be unimportable from a plain tsx process even though none of the actual logic under test needs Pinia, because some unrelated store in the chain calls a Vite-only API (import.meta.glob) at module load time. The fix already has a name in this codebase -- brainstormSourceAdapterKit.ts/brainstormSourceContextKit.ts already split pure logic out for exactly this reason -- but it's not written down as a general rule anywhere, so it's worth re-deriving the "does this file transitively import a store with a Vite-only top-level call" question explicitly before assuming a store's exports are tsx-testable. Second lesson: a CI job that installs with `npm ci --ignore-scripts` (for speed) skips the `nuxi prepare` postinstall that generates the '@/' path-alias tsconfig -- any new tsx-run script under such a job must use relative imports, not '@/', or verify locally with `.nuxt` removed before trusting it'll pass in CI.

- 2026-08-19 `brainstorm/t-024` — The task's own "scope check first" step is what caught this: before building any UI, re-verified whether bot-gallery.vue was actually unmounted as the t-018 kaizen note claimed, and found the claim already false on current main -- content/bots.md -> bot-manager.vue -> bot-interact.vue -> bot-gallery.vue is a complete, CI-verified (test:route-gallery-contract) mount chain reachable via the play channel's normal nav, not just a direct URL. Closed with no code change and no kind_robots PR. Worth generalizing: a kaizen-sourced task's premise can go stale between when it was written and when it is picked up, especially for reachability/mounting claims in a codebase with this much concurrent agent activity -- re-verify the premise against live main before writing any diff, not just before merging one.


---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-20T16:49:36Z_
