# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-15T10:54:14Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **969**
- Outcomes: blocked: 16, cancelled: 1, done: 952
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
| conductor | 105 | 100% |
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
| storybook | 21 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 7 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 952 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 25 |
| transient | 15 |
| actionable | 15 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 47% success over 17 closed tasks; aim the next kaizen task here
- failure category `quality` — 25 occurrences; look for the shared cause across its records
- failure category `transient` — 15 occurrences; look for the shared cause across its records
- failure category `actionable` — 15 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-15 `conductor/t-157` — check_hostbuf_failure.py's "unverified" state (a hostbuf failure older than the 2h alert window with no successful render since) was only ever reported via a `::warning::` line in that one hourly workflow run's own log -- a channel nothing else reads, so a stale unresolved incident could sit invisible indefinitely with no durable trace. Fixed by writing the same RENDER-BACKLOG.md ledger convention recheck_render_queue.py already uses, and giving the workflow contents: write plus a commit-back step so the entry actually reaches main. When a sentinel/check script's only failure signal is a workflow-log annotation, that is itself a gap worth closing -- durable state belongs in a file something else reads, not in a run nobody reopens.
- 2026-09-15 `coloring-book/t-022` — hwr-008 (Laboratory Tenor) failed creative review 4 times across 4 sessions on the same core requirement -- a trans man tenor with visible healed bilateral chest-surgery scars -- and the failure mode changed each time a wardrobe strategy was fixed: attempt 1-2 rendered a conventional young man with no scars; attempt 3 fixed the age/face but produced a fully buttoned tuxedo occluding any possible scar; attempt 4 opened the neckline but the exposed skin was smooth and unmarked. Two different wardrobe rewrites (closed tuxedo, then open cape) both failed to surface any scar once the neckline was actually open, which is stronger evidence than either alone that the render engine is declining to depict surgical scar texture on skin at all -- plausibly a content-safety-adjacent smoothing bias -- rather than a wardrobe-occlusion problem a prompt rewrite can keep chasing. When a creative-review slot keeps failing on the *same specific visual element* after the prompt-level cause it was blamed on gets fixed, stop revising wardrobe/pose/framing language and treat the element itself (not its surrounding context) as the suspect -- escalate for a human/engine-level call rather than a fifth blind wardrobe rewrite.
- 2026-09-15 `coloring-book/t-022` — manage_coloring_book_production.py's generate-bw leaves a stale bw_job_id/bw_status: running entry unrecovered indefinitely unless a future cycle happens to re-request that exact proposal id -- five Monster Recast slots (mr-005/007/009/011/012) sat at a week-old running status even though the render backend had actually completed and mechanically rejected all five as Kontext-engine noise a day after submission. Recovering them in one pass raised t-039's known-defect count from 2 to 7 of 7 checked attempts (100% failure), which is a materially different finding than "two isolated misses" -- when a recurring production task's queue-status tooling only reports the current batch, periodically sweep every bw_status/render_gate_error still marked running/pending regardless of the active batch, since a silently-completed-and-rejected job looks identical to a still-pending one until someone re-checks it.
- 2026-09-15 `model-builder/t-029` — A text-truncation guard that only asserts pickText()'s own cap (verifyModelBuilderCommitTextTruncationGuard.ts, cycle 33) does not cover every place raw user/AI text reaches a bounded DB column -- commit.post.ts's updateText()/createRecord() also assigned the raw, uncapped pitch/fieldsDraft blob directly as a fallback for Bot.description/botIntro/prompt (bounded VarChar columns) whenever the FIELDS stage left those blank, bypassing pickText and its cap entirely. When auditing a text-length bug class, trace every write site for the affected columns, not just the ones that already go through the sanctioned helper -- a fallback path written before or after the helper call is exactly where the same bug re-enters uncaught.
- 2026-09-15 `conductor/t-159` — Rotating an append-only log (TALKBACK.md) into monthly archives is safe when every archive write is verified byte-for-byte round-trip (write, re-read, re-extract, compare) before the source is ever rewritten, and the one real consumer that whole-file-parses the source for historical data (backfill_learning.py's --since all) gets fixed to read the archive directory too -- the archival carve-out only holds if every consumer of the pre-split file is checked, not just the file split itself.
- 2026-09-15 `conductor/t-163` — Factored close_task.py's equal/not-equal branch-tip check (t-161) into scripts/branch_ancestry.py's classify_relationship(), a pure primitive over `git merge-base --is-ancestor` that names the actual relationship (equal/ahead/ behind/diverged) instead of a bare SHA comparison. Refusal behavior is unchanged -- only "equal" is safe to build on -- but the primitive is now independently unit-tested and reusable. claim_task.py's branch-naming paths were flagged (not yet audited) as a plausible next caller of the same primitive.
- 2026-09-15 `conductor/t-161` — close_task.py built its close-out commit from the remote branch tip (origin/<branch> or origin/main) regardless of whether a same-named local branch existed with unpushed commits, so `--branch <my-current-branch>` did not behave like a normal git push -- it could silently rebuild from a stale base and force-push over local-only work (caught once already in coloring-book/t-046, kaizen-sourced this task). Fixed with a fail-closed branch-tip equality check before every commit attempt, tested against both the divergent and matching-tip cases. Any scratch-index git plumbing that targets a named branch without reading the caller's actual worktree state needs the same guard -- worth checking claim_task.py's branch-naming paths for the same class of assumption.
- 2026-09-14 `coloring-book/t-022` — finalize-pair (manage_coloring_book_production.py) crashed with a NameError on every live invocation -- it referenced an undefined `semantic` variable (a leftover name from a different script's local variable of the same purpose) instead of the queue entry's own `bw_semantic_score` field. This went unnoticed for weeks: all three coloring books accumulated dozens of slots with both an accepted color and accepted BW file (66 combined) while `final pairs` sat at 0/36 in every book, because nothing had ever tested `finalize_pair` and every attempt to run it in production would have failed loudly enough to be caught, yet apparently no prior cycle actually tried. Fixed the reference and landed the first 3 final pairs (Monster Recast mr-002/003/004). Worth a standing habit: an operation with zero successful invocations across many eligible candidates is a stronger signal than "not yet gotten to" -- check whether it has ever actually run, not just whether its inputs exist.
- 2026-09-14 `coloring-book/t-022` — A documented safety guard that is never actually wired into the code that runs is worse than no guard, because it reads as coverage that does not exist: monster-recast/art-modeler-request.yaml documented a content-safety negative_prompt (no explicit genitals/nipples/etc.) for months, but build_entries() only ever read a per-entry override that no entry in any of the 108 slots across all three books had ever set -- every render, Monster Recast included, only got the purely technical DEFAULT_NEGATIVE_PROMPT. Caught live when a routine re-render (not a targeted safety audit) came back with unrequested exposed nudity, and the pre-existing already-committed candidate for that same slot turned out to have the identical defect. The fix (bake the content-safety terms into every entry by default) was small, but finding it required actually tracing the negative_prompt value from the documented YAML through to the submitted payload rather than trusting that a file named art-modeler-request.yaml next to the render queue meant its contents were in effect. Worth a standing habit: when a generation pipeline documents a safety constraint in a config/request file, verify by reading the actual code path that consumes it, not by the file's existence or its prose.
- 2026-09-14 `coloring-book/t-022` — consume_coloring_book_studio_request.py had two independent call sites referencing coloring functions that were never actually defined (record_semantic_gate_error, fixed cycle 2; record_semantic_rejection, fixed cycle 8, same day) -- both a mismatch between this wrapper's error handling and consume_coloring_book_color_art.py's real public API, each only discovered by hitting the exact code path live. A single pass grepping every coloring.<name> call in the wrapper against the other module's actual def list would have caught both in one sitting instead of one crash at a time; filed as this cycle's kaizen suggestion rather than done inline to keep the cycle's diff scoped to the crash actually hit.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-15T10:54:14Z_
