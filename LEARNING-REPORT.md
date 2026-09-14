# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-14T17:46:33Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **958**
- Outcomes: blocked: 16, cancelled: 1, done: 941
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
| coloring-book | 31 | 100% |
| conductor | 101 | 100% |
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
| software | 941 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 21 |
| transient | 15 |
| actionable | 14 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 47% success over 17 closed tasks; aim the next kaizen task here
- failure category `quality` — 21 occurrences; look for the shared cause across its records
- failure category `transient` — 15 occurrences; look for the shared cause across its records
- failure category `actionable` — 14 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-14 `coloring-book/t-045` — Calibrating a quality-gate threshold against a bad example alone is not enough -- the first two signal designs tried here (global pixel-count hue histogram, then a spatial per-cell hue-family count) both caught mr-025's sepia wash cleanly but were never tested against the real *approved* corpus until asked to be, and both turned out to false-positive on genuinely good, Silas-approved art (masked-countess-color.webp) once they were. The spatial design's failure mode was subtle: it looked spatially principled but still only counted pixels above the same 'colorful' saturation cutoff, so a real illustration whose non-primary elements (black cloak, white mask, gold trim) are desaturated collapsed to the same single-family signal as an actual wash. What worked was measuring hue consistency in the *opposite* band -- the low-saturation pixels every other check ignores -- because that's the band a duotone/sepia tone-curve filter actually tints and a real illustration's true neutrals do not. Any pixel-statistic quality gate needs its negative-space calibration (the full trusted-good corpus, not just the one known-bad case) run before landing, and visually inspecting the disputed calibration file directly (not just its stats) is what actually explained why the second design failed.
- 2026-09-14 `kind-robots/t-098` — Session-end reconciliation caught this: implementation PR kind_robots#2727 merged over 2 hours before this sweep ran, but the roadmap task was left at status: review with a malformed implementation_pr field (a raw https:// URL instead of the owner/repo#N format check_pr_merged_drift.py's authoritative pass expects) -- so the drift check's title-text fallback caught it instead. Whatever closed the implementing PR didn't finish the roadmap close-out step in the same run. Reconciling promptly (same session that ran the drift check, not deferred) keeps status: review tasks from accumulating as false 'awaiting review' signals for a PR that already landed.
- 2026-09-14 `coloring-book/t-044` — art_quality.py's 'color' variant gate checked blank/degenerate, noise, and aspect but had no saturation floor at all -- a structurally valid, non-blank, non-noise render that came back essentially monochrome (mean_saturation ~0.01-0.02) silently passed every time, and had already been caught by hand three separate times across two sessions (mr-006/mr-008 on 2026-09-07, mr-025 on 2026-09-09) before mr-008 hit it a fourth time this cycle. Each prior catch documented the defect in a proposals.yaml note but nobody closed the loop by asking whether the mechanical gate itself should catch it -- the same shape as t-039's noise-detector gap, just for a different failure mode. When a defect gets manually caught 2+ times on the same objective, mechanically-measurable signal, that's the trigger to add a gate for it rather than keep relying on creative review to notice again; calibrating the threshold against the full existing corpus (115 real files, not just the one bad example) before picking a number is what kept it from being a guess.
- 2026-09-14 `text-generation/t-006` — A month-old design brief's file list (BRIEF.md's five confirmed chatStore.streamResponse consumers) had already drifted from the current tree -- one named file no longer existed, and two of the remaining four already had the exact fix this task was scoped to add, done incidentally by earlier unrelated work. A subagent sweep of current source (not the brief's own memory) caught both before writing any diff. Also: 'wire provider selection into the product surfaces' sounds like it could mean migrating chat UI onto the new unified /api/generate/text endpoint (the more impressive-looking fix) -- the brief's own 'explicitly out of scope' section said otherwise, and trusting that over the more expansive-sounding task title avoided a real scope violation.
- 2026-09-14 `kind-robots/t-078` — A remaining-polish list of 4 items had 2 already resolved by earlier, unrelated commits (home-dream-hero.vue's cast-row chevrons; Send-to-agent already answers-and-releases) -- checking each item against the CURRENT codebase before implementing anything caught this and avoided duplicate/no-op work on two of the four. The real bug in the other two (home-attention.vue's submission receipt) was a timing bug invisible from reading the template alone: the confirmation message and the row it needed to survive were removed from the DOM on the exact same reactive tick, so it only surfaces by tracing submitTaskAction's optimistic store update against the v-if that gates the whole message. The one item that didn't fit the task's own scope (whether the home showcase should server-render) was split into kind-robots/t-102 rather than attempted blind -- it touches the whole page's data flow, not one component, and carries hydration-mismatch risk this sandbox has no way to visually verify pre-merge; deciding NOT to convert it now, and recording why, is itself the 'normal technical decision' the task's own note granted latitude for.
- 2026-09-14 `kind-robots/t-094` — The task's own note named three duplicated 'creation paths' to consolidate, but reading server/api/conductor/sync.post.ts closely showed its Project-slug handling isn't actually a copy of the same logic: it upserts Conductor-authoritative projects from an already-validated projection (update on collision), the opposite semantics of the two AppMaker routes' reject-on-collision check for user-supplied slugs. Forcing a third call site onto a shared reject-style helper would have silently changed sync.post.ts's behavior rather than just its shape -- worth verifying a task's premise against the actual code before extending a refactor's scope to match a filing's word count, and documenting the deliberate exclusion in the new helper's own comment so a later pass doesn't 'fix' it back in.
- 2026-09-14 `conductor/t-156` — recheck_render_queue.py's classify() checked only queueDepth.PENDING before check_render_box.py's own render_throughput_verdict() was ever consulted, so it wrote 'healthy' to RENDER-BACKLOG.md for a box that was actually down (every job failing fast, never leaving anything stuck PENDING) in the exact same live session where check_render_box.py correctly reported DOWN. Two scripts reading the same stats endpoint with different classifiers will disagree eventually -- when one is already the documented single source of truth for a judgment (here, 'is the render box actually rendering'), the other should delegate to it rather than reimplement a weaker version. Caught this live because the two scripts were run back-to-back in the same session on coloring-book/t-022; would otherwise have silently written a wrong ledger entry.
- 2026-09-14 `kind-robots/t-062` — This sandbox's local verification habit of running vue-tsc/eslint/prettier/test:layout-contract missed a fourth check bundled into the same CI job: test:kr-class-coverage, which failed on the first push over kr-text-sm -- a plausible-looking primitive name (the sm-size family is all modified: kr-text-black-sm, kr-text-dim-sm, kr-text-bold-sm, kr-text-faded-sm, but no bare kr-text-sm) that doesn't actually exist in assets/css/tailwind.css. Read a CI workflow file's full step list (.github/workflows/<job>.yml) before claiming local verification covers a job, rather than assuming the one script named in the job title is the whole job -- layout-contract.yml alone runs four separate npm scripts plus two fixture/selftest scripts. Also: a Grant-sharing pitch (kind-robots/t-044/t-050/t-062) that adds canView()/existsActiveGrant() to two view routes plus a minimal Share/Shared-with-me UI has no existing owner-facing edit surface to embed the share widget into for either Project or Resource -- shipped as two standalone /projects/[id]/share and /resources/[id]/share pages instead of wiring into the admin-only conductor project-detail panel, which is gated on isAdmin and would never reach the non-admin owners Grant sharing exists for.
- 2026-09-14 `interface-vision/t-133` — Real PR traffic touching *.sh files was too sparse to answer the task's own question from CI history alone (only one recent PR had an actual .sh diff, and it produced zero shellcheck findings) -- ran shellcheck directly against the full current *.sh corpus (12 scripts) as a stand-in evidence base instead of waiting indefinitely for more PR traffic. Only SC2086 had multiple true-positive hits with zero false positives; the other codes seen (SC2207/SC2010/SC2209/SC1003) each had a single occurrence and one (SC2209) was a confirmed false positive on this repo's TOOL=name assignment style, confirming the task's own caution against flipping the whole pass to blocking at once.
- 2026-09-13 `kind-robots/t-096` — The task's original filing (grep of 'return errorHandler(error)') undercounted the real call-site pattern -- most of the codebase actually writes 'const handled = errorHandler(error)' then a separate status line, so the literal grep matched only 19 of 470 real call sites and the filing concluded almost nothing was fixed (8/432) when in fact 429/470 already were. Re-derive the live count with a broader pattern (any errorHandler( call, cross-referenced against status-setting patterns) before trusting a stale filing's scope estimate, especially for a task that's sat open a couple of days -- the codebase moves. Also found and fixed a second, coupled bug while auditing: several routes called errorHandler() with a wrapper object ({error, context, statusCode}) instead of the actual Error, which errorHandler() doesn't recognize, silently discarding the intended status and message even in the JSON body -- worth checking call-site *shape*, not just call-site *presence*, when fixing a suspected systemic misuse.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-14T17:46:33Z_
