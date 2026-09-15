# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-15T15:29:06Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **974**
- Outcomes: blocked: 16, cancelled: 1, done: 957
- Success rate: **98%**
- Average passes on successful tasks: **0.1**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 73 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 14 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 9 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| brainstorm | 26 | 96% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 37 | 100% |
| conductor | 109 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 51 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 23 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 135 | 100% |
| kapowarr | 52 | 100% |
| kind-economy | 10 | 100% |
| kind-robots | 60 | 98% |
| kindrobots-unraid | 9 | 100% |
| lora-ingestion | 1 | 100% |
| mandarin-tutor | 11 | 100% |
| media-watchlist | 12 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 84 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| rainbow-butterflies | 20 | 100% |
| ruler-hooked | 11 | 100% |
| scene-animator | 2 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 22 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 7 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 957 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 26 |
| transient | 15 |
| actionable | 15 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 47% success over 17 closed tasks; aim the next kaizen task here
- failure category `quality` — 26 occurrences; look for the shared cause across its records
- failure category `transient` — 15 occurrences; look for the shared cause across its records
- failure category `actionable` — 15 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-15 `conductor/t-168` — scripts/kr_token_set.sh's exit killed the calling shell when sourced -- the documented safe usage -- silently dropping any chained command; fixed with sourced-vs-executed runtime detection and pinned with a subprocess-driven regression test since none existed.
- 2026-09-15 `storybook/t-027` — A recurring "check the real state and record it" audit task can surface a result the task's own follow-on wasn't designed for: t-028 assumed t-027 would find some endings missing art among an otherwise-seeded 1,024-row catalog, but the actual coverage call came back 0/1024 seeded -- zero rows exist at all, not partial art coverage. Letting the dependency resolver mechanically flip t-028 to `ready` on t-027's `done` would have handed a future worker a task it structurally could not start (nothing to attach art to). General lesson: when an audit's real result falls outside the shape its downstream task assumed, redirect the downstream task in the same close-out instead of letting an automatic status transition carry a stale scope forward -- the dependency graph tracks task completion, not whether the completed task's findings still match what its dependent expects.
- 2026-09-15 `conductor/t-166` — Two tests in test_check_render_box.py asserted on check.main()'s return value without mocking every function main() calls (engine_heartbeat_verdict), so they silently made a real network call every run -- caught only because the live render engine happened to be reporting unhealthy at the moment this session ran the full suite, which flipped their result from a coincidental pass to a real failure. General lesson: a test that patches some of a function's dependencies but not all of them is not actually isolated -- it just hasn't been caught yet by the unpatched dependency disagreeing with what the test expects. When fixing one, audit every other test hitting the same entry point for the identical gap (two more tests here were leaking the same call and passing by coincidence).
- 2026-09-15 `conductor/t-164` — check_pr_merged_drift.py's title-search and stranded-branch passes both scanned every repo in ALL_TRACKED_REPOS for every in-progress task, even though most tasks' own title/note history already names the one or two repos that actually matter for them. Added task_relevant_repos() to narrow both passes to a task's own cited repos first, falling back to the full list only when a task cites none. General lesson: when a checker scans "every tracked X" for "every candidate Y", check whether each Y already carries evidence of which X actually applies to it before paying the full cross-product cost -- the per-run caches already shared across tasks/repos mean this is a scope reduction, not just deferred work.
- 2026-09-15 `conductor/t-150` — check_pr_merged_drift.py's title-search and note-reference passes can only report drift when a PR actually exists to find -- a task whose implementing session never opened one at all (cthulhuquarium/t-076) read as a false "clean", the exact opposite failure mode from what the script was built to catch. Closed by adding a fifth pass that lists branches across the same tracked repos already scanned for title matches and flags one matching the worker naming convention with no open PR against it. General lesson: a checker built to catch "state A drifted from state B" should also ask whether state B (the PR/evidence it searches for) exists at all -- absence-of-evidence and evidence-of-absence are different findings and a search that only handles the former will read a genuinely missing PR as clean.
- 2026-09-15 `conductor/t-157` — check_hostbuf_failure.py's "unverified" state (a hostbuf failure older than the 2h alert window with no successful render since) was only ever reported via a `::warning::` line in that one hourly workflow run's own log -- a channel nothing else reads, so a stale unresolved incident could sit invisible indefinitely with no durable trace. Fixed by writing the same RENDER-BACKLOG.md ledger convention recheck_render_queue.py already uses, and giving the workflow contents: write plus a commit-back step so the entry actually reaches main. When a sentinel/check script's only failure signal is a workflow-log annotation, that is itself a gap worth closing -- durable state belongs in a file something else reads, not in a run nobody reopens.
- 2026-09-15 `coloring-book/t-022` — hwr-008 (Laboratory Tenor) failed creative review 4 times across 4 sessions on the same core requirement -- a trans man tenor with visible healed bilateral chest-surgery scars -- and the failure mode changed each time a wardrobe strategy was fixed: attempt 1-2 rendered a conventional young man with no scars; attempt 3 fixed the age/face but produced a fully buttoned tuxedo occluding any possible scar; attempt 4 opened the neckline but the exposed skin was smooth and unmarked. Two different wardrobe rewrites (closed tuxedo, then open cape) both failed to surface any scar once the neckline was actually open, which is stronger evidence than either alone that the render engine is declining to depict surgical scar texture on skin at all -- plausibly a content-safety-adjacent smoothing bias -- rather than a wardrobe-occlusion problem a prompt rewrite can keep chasing. When a creative-review slot keeps failing on the *same specific visual element* after the prompt-level cause it was blamed on gets fixed, stop revising wardrobe/pose/framing language and treat the element itself (not its surrounding context) as the suspect -- escalate for a human/engine-level call rather than a fifth blind wardrobe rewrite.
- 2026-09-15 `coloring-book/t-022` — manage_coloring_book_production.py's generate-bw leaves a stale bw_job_id/bw_status: running entry unrecovered indefinitely unless a future cycle happens to re-request that exact proposal id -- five Monster Recast slots (mr-005/007/009/011/012) sat at a week-old running status even though the render backend had actually completed and mechanically rejected all five as Kontext-engine noise a day after submission. Recovering them in one pass raised t-039's known-defect count from 2 to 7 of 7 checked attempts (100% failure), which is a materially different finding than "two isolated misses" -- when a recurring production task's queue-status tooling only reports the current batch, periodically sweep every bw_status/render_gate_error still marked running/pending regardless of the active batch, since a silently-completed-and-rejected job looks identical to a still-pending one until someone re-checks it.
- 2026-09-15 `model-builder/t-029` — A text-truncation guard that only asserts pickText()'s own cap (verifyModelBuilderCommitTextTruncationGuard.ts, cycle 33) does not cover every place raw user/AI text reaches a bounded DB column -- commit.post.ts's updateText()/createRecord() also assigned the raw, uncapped pitch/fieldsDraft blob directly as a fallback for Bot.description/botIntro/prompt (bounded VarChar columns) whenever the FIELDS stage left those blank, bypassing pickText and its cap entirely. When auditing a text-length bug class, trace every write site for the affected columns, not just the ones that already go through the sanctioned helper -- a fallback path written before or after the helper call is exactly where the same bug re-enters uncaught.
- 2026-09-15 `conductor/t-159` — Rotating an append-only log (TALKBACK.md) into monthly archives is safe when every archive write is verified byte-for-byte round-trip (write, re-read, re-extract, compare) before the source is ever rewritten, and the one real consumer that whole-file-parses the source for historical data (backfill_learning.py's --since all) gets fixed to read the archive directory too -- the archival carve-out only holds if every consumer of the pre-split file is checked, not just the file split itself.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-15T15:29:06Z_
