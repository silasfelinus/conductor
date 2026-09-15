# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-15T00:31:59Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **963**
- Outcomes: blocked: 16, cancelled: 1, done: 946
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
| coloring-book | 35 | 100% |
| conductor | 102 | 100% |
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
| model-builder | 83 | 100% |
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
| software | 946 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 24 |
| transient | 15 |
| actionable | 14 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 47% success over 17 closed tasks; aim the next kaizen task here
- failure category `quality` — 24 occurrences; look for the shared cause across its records
- failure category `transient` — 15 occurrences; look for the shared cause across its records
- failure category `actionable` — 14 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-15 `conductor/t-161` — close_task.py built its close-out commit from the remote branch tip (origin/<branch> or origin/main) regardless of whether a same-named local branch existed with unpushed commits, so `--branch <my-current-branch>` did not behave like a normal git push -- it could silently rebuild from a stale base and force-push over local-only work (caught once already in coloring-book/t-046, kaizen-sourced this task). Fixed with a fail-closed branch-tip equality check before every commit attempt, tested against both the divergent and matching-tip cases. Any scratch-index git plumbing that targets a named branch without reading the caller's actual worktree state needs the same guard -- worth checking claim_task.py's branch-naming paths for the same class of assumption.
- 2026-09-14 `coloring-book/t-022` — finalize-pair (manage_coloring_book_production.py) crashed with a NameError on every live invocation -- it referenced an undefined `semantic` variable (a leftover name from a different script's local variable of the same purpose) instead of the queue entry's own `bw_semantic_score` field. This went unnoticed for weeks: all three coloring books accumulated dozens of slots with both an accepted color and accepted BW file (66 combined) while `final pairs` sat at 0/36 in every book, because nothing had ever tested `finalize_pair` and every attempt to run it in production would have failed loudly enough to be caught, yet apparently no prior cycle actually tried. Fixed the reference and landed the first 3 final pairs (Monster Recast mr-002/003/004). Worth a standing habit: an operation with zero successful invocations across many eligible candidates is a stronger signal than "not yet gotten to" -- check whether it has ever actually run, not just whether its inputs exist.
- 2026-09-14 `coloring-book/t-022` — A documented safety guard that is never actually wired into the code that runs is worse than no guard, because it reads as coverage that does not exist: monster-recast/art-modeler-request.yaml documented a content-safety negative_prompt (no explicit genitals/nipples/etc.) for months, but build_entries() only ever read a per-entry override that no entry in any of the 108 slots across all three books had ever set -- every render, Monster Recast included, only got the purely technical DEFAULT_NEGATIVE_PROMPT. Caught live when a routine re-render (not a targeted safety audit) came back with unrequested exposed nudity, and the pre-existing already-committed candidate for that same slot turned out to have the identical defect. The fix (bake the content-safety terms into every entry by default) was small, but finding it required actually tracing the negative_prompt value from the documented YAML through to the submitted payload rather than trusting that a file named art-modeler-request.yaml next to the render queue meant its contents were in effect. Worth a standing habit: when a generation pipeline documents a safety constraint in a config/request file, verify by reading the actual code path that consumes it, not by the file's existence or its prose.
- 2026-09-14 `coloring-book/t-022` — consume_coloring_book_studio_request.py had two independent call sites referencing coloring functions that were never actually defined (record_semantic_gate_error, fixed cycle 2; record_semantic_rejection, fixed cycle 8, same day) -- both a mismatch between this wrapper's error handling and consume_coloring_book_color_art.py's real public API, each only discovered by hitting the exact code path live. A single pass grepping every coloring.<name> call in the wrapper against the other module's actual def list would have caught both in one sitting instead of one crash at a time; filed as this cycle's kaizen suggestion rather than done inline to keep the cycle's diff scoped to the crash actually hit.
- 2026-09-14 `coloring-book/t-046` — Pinning a regression fixture against a real approved/ corpus is itself a calibration exercise, not just a testing exercise: building tests/test_art_quality.py to cover BW_*, COLOR_MIN_*, and TINT_* (as the task's own note asked) surfaced that BW_MIN_WHITE_FRACTION=0.30 would reject 4 of 17 real Silas-approved bw masters -- dense, heavily-shaded/stippled line art that is genuinely black-and-white by every other measure but has less open background than a simpler page. The fixture only becomes trustworthy once every real approved file actually lands on the correct side of it; a fixture that pins current behavior without checking it against real data first would have baked in the same false-rejection the threshold itself has. Visually inspecting the specific failing files (not just their stats) before touching the constant is what distinguished 'bad threshold' from 'bad data' -- same lesson as t-045's masked-countess case, now generalized to a second threshold family.
- 2026-09-14 `coloring-book/t-045` — Calibrating a quality-gate threshold against a bad example alone is not enough -- the first two signal designs tried here (global pixel-count hue histogram, then a spatial per-cell hue-family count) both caught mr-025's sepia wash cleanly but were never tested against the real *approved* corpus until asked to be, and both turned out to false-positive on genuinely good, Silas-approved art (masked-countess-color.webp) once they were. The spatial design's failure mode was subtle: it looked spatially principled but still only counted pixels above the same 'colorful' saturation cutoff, so a real illustration whose non-primary elements (black cloak, white mask, gold trim) are desaturated collapsed to the same single-family signal as an actual wash. What worked was measuring hue consistency in the *opposite* band -- the low-saturation pixels every other check ignores -- because that's the band a duotone/sepia tone-curve filter actually tints and a real illustration's true neutrals do not. Any pixel-statistic quality gate needs its negative-space calibration (the full trusted-good corpus, not just the one known-bad case) run before landing, and visually inspecting the disputed calibration file directly (not just its stats) is what actually explained why the second design failed.
- 2026-09-14 `kind-robots/t-098` — Session-end reconciliation caught this: implementation PR kind_robots#2727 merged over 2 hours before this sweep ran, but the roadmap task was left at status: review with a malformed implementation_pr field (a raw https:// URL instead of the owner/repo#N format check_pr_merged_drift.py's authoritative pass expects) -- so the drift check's title-text fallback caught it instead. Whatever closed the implementing PR didn't finish the roadmap close-out step in the same run. Reconciling promptly (same session that ran the drift check, not deferred) keeps status: review tasks from accumulating as false 'awaiting review' signals for a PR that already landed.
- 2026-09-14 `coloring-book/t-044` — art_quality.py's 'color' variant gate checked blank/degenerate, noise, and aspect but had no saturation floor at all -- a structurally valid, non-blank, non-noise render that came back essentially monochrome (mean_saturation ~0.01-0.02) silently passed every time, and had already been caught by hand three separate times across two sessions (mr-006/mr-008 on 2026-09-07, mr-025 on 2026-09-09) before mr-008 hit it a fourth time this cycle. Each prior catch documented the defect in a proposals.yaml note but nobody closed the loop by asking whether the mechanical gate itself should catch it -- the same shape as t-039's noise-detector gap, just for a different failure mode. When a defect gets manually caught 2+ times on the same objective, mechanically-measurable signal, that's the trigger to add a gate for it rather than keep relying on creative review to notice again; calibrating the threshold against the full existing corpus (115 real files, not just the one bad example) before picking a number is what kept it from being a guess.
- 2026-09-14 `text-generation/t-006` — A month-old design brief's file list (BRIEF.md's five confirmed chatStore.streamResponse consumers) had already drifted from the current tree -- one named file no longer existed, and two of the remaining four already had the exact fix this task was scoped to add, done incidentally by earlier unrelated work. A subagent sweep of current source (not the brief's own memory) caught both before writing any diff. Also: 'wire provider selection into the product surfaces' sounds like it could mean migrating chat UI onto the new unified /api/generate/text endpoint (the more impressive-looking fix) -- the brief's own 'explicitly out of scope' section said otherwise, and trusting that over the more expansive-sounding task title avoided a real scope violation.
- 2026-09-14 `kind-robots/t-078` — A remaining-polish list of 4 items had 2 already resolved by earlier, unrelated commits (home-dream-hero.vue's cast-row chevrons; Send-to-agent already answers-and-releases) -- checking each item against the CURRENT codebase before implementing anything caught this and avoided duplicate/no-op work on two of the four. The real bug in the other two (home-attention.vue's submission receipt) was a timing bug invisible from reading the template alone: the confirmation message and the row it needed to survive were removed from the DOM on the exact same reactive tick, so it only surfaces by tracing submitTaskAction's optimistic store update against the v-if that gates the whole message. The one item that didn't fit the task's own scope (whether the home showcase should server-render) was split into kind-robots/t-102 rather than attempted blind -- it touches the whole page's data flow, not one component, and carries hydration-mismatch risk this sandbox has no way to visually verify pre-merge; deciding NOT to convert it now, and recording why, is itself the 'normal technical decision' the task's own note granted latitude for.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-15T00:31:59Z_
