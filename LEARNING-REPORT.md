# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-08T21:31:34Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **897**
- Outcomes: blocked: 16, cancelled: 1, done: 880
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
| coloring-book | 25 | 100% |
| conductor | 95 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 43 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 23 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 108 | 100% |
| kapowarr | 52 | 100% |
| kind-economy | 9 | 100% |
| kind-robots | 55 | 98% |
| kindrobots-unraid | 6 | 100% |
| lora-ingestion | 1 | 100% |
| mandarin-tutor | 11 | 100% |
| media-watchlist | 11 | 100% |
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
| storybook | 18 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 6 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 16 | 44% |
| software | 881 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 17 |
| transient | 15 |
| actionable | 13 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 17 occurrences; look for the shared cause across its records
- failure category `transient` — 15 occurrences; look for the shared cause across its records
- failure category `actionable` — 13 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-08 `ai-art-academy/t-045` — A "DONE" render-queue job is not proof of a usable image -- t-045's 5-style Kontext+LoRA re-run all completed DONE with valid 1024x1024 PNGs (correct file format, correct dimensions) that were nonetheless pure uniform static/noise with zero recognizable content, identical corruption signature across all 5 independent LoRA files. A polling script that only checks job status/artImageId presence, never image content, will report success on a systemically broken render path. Add a cheap low-entropy/ uniform-pixel sanity check (e.g. stddev of decoded pixel values) to any future job-polling script before treating DONE as "safe to compare/ promote" -- would have caught this the moment results first came back instead of needing a manual visual compare pass.
- 2026-09-08 `interface-vision/t-104` — A new `.kr-*` primitive that wraps daisyUI tokens via `@apply` can pass every local check (vue-tsc, eslint, layout-contract, lint-ratchet, prettier) and still fail CI's `Build production image` check alone: `@apply label-text font-bold` broke with `Cannot apply unknown utility class 'label-text'` because `label-text` is dead markup left over from a pre-5 daisyUI form convention -- present in 200+ templates but with zero matching CSS rule anywhere in daisyUI 5's own dist CSS or this repo's assets/. Tailwind v4's `@apply` validates its argument against real utilities; a raw template `class="..."` attribute is never validated, so the dead token was invisible everywhere except the actual production build (the most expensive place to discover it, ~8-10 minutes per run). Before writing a new `kr-*` primitive's `@apply` line, grep the base tokens against `node_modules/daisyui/dist/*.css` (or the app's own `assets/`) for an actual CSS rule first -- a class present in markup is not proof it is a real, applyable utility, especially across a daisyUI major-version bump.
- 2026-09-08 `interface-vision/t-104` — Shrinking a long `class="..."` attribute down to a short primitive name can leave stale multi-line Vue-template formatting behind: prettier had wrapped the original long class onto its own line inside a 3-line `<span>\n  class="..."\n>`, and after the codemod collapsed it to `kr-icon-tile` that wrapping was no longer prettier's own preference, so `prettier --check` flagged it as newly non-conforming on files that were otherwise already prettier-clean. The fix is NOT `prettier --write` on the whole file when the file has *other*, unrelated pre-existing prettier violations (a real trap hit mid-slice: running it reformatted unrelated code throughout build-bench.vue, privacy-page.vue, and wallet-page.vue, turning a 4-line diff into a 100+-line one) -- diff `git stash` baseline vs. current per file first, and hand-collapse just the specific tag when the file has pre-existing noise the tool would otherwise sweep in.
- 2026-09-08 `interface-vision/t-104` — A codemod's subset-match convention (base tokens present, extras preserved) generalizes further than a manual literal grep once written -- the initial grep for the exact string "rounded-2xl bg-base-200 p-3" found 10 occurrences, but the codemod's subset match found 22 once it stopped caring about surrounding utility tokens (max-h-96, text-sm, sm:p-4, ...). The inverse risk showed up in the same slice: two occurrences (stylist-manager.vue, checkpoint-card.vue) matched the same base-token subset but also carried a `border border-base-300` token the target primitive doesn't have -- a structurally different bordered shape, not a superset of the borderless one. Subset-matching on the tokens you want is not enough; a family that is defined by the *absence* of a token (no border) needs an explicit negative check too, or it silently strips that token from occurrences that actually need it.
- 2026-09-08 `kindrobots-unraid/t-015` — A site-wide kindrobots.org 502 outage (02:56-05:53 UTC, ~2h57m) recovered on its own before root cause could be investigated -- the second such occurrence after t-014's ~4h15m outage with the same unconfirmed container-recreate-without-restart theory. Closed per docs/state-reconciliation.md's incident-recovery closure pathway (10/10 clean 200s on both / and /api/health/database) with approved_by_human left false, matching t-014's precedent. Recurring unexplained outages with no external health-probe/alerting in place mean each one is only ever observed-and-cleared by whichever session happens to sweep during the window -- the standing follow-up (an external probe/alert task) is still unfiled after two occurrences.
- 2026-09-08 `conductor/t-111` — When a suppression filter needs to distinguish "genuinely stale, keep hiding it" from "the disputed thing itself, must surface," reach for a narrow content classifier on the task's own title before reaching for timing heuristics (e.g. "how close is the task's updated: to the override's status change"). A real check here (pinball-hero/t-002's updated: was only ~1 week after its project's retirement date -- well within any generous same-day-ish margin) showed a date-proximity threshold would have reintroduced the exact false positive the original filter existed to prevent. Matching what the task's title is actually about was both simpler and correct where a tuned margin was neither.
- 2026-09-08 `conductor/t-148` — A flaky test that asserts on positional order of a shared mutable list (e.g. "the first matching log line") rather than content that only its own code path can produce is a signal to look for concurrent producers with no lifecycle boundary between tests -- here, every other test in the same file intentionally leaves a daemon thread running forever, and the production code re-reads its config/behavior off live module globals each iteration, so a still-running thread from an earlier test races the current test's own thread using whatever the current test has monkeypatched. Fix the race by waiting for and asserting on a signature only the current test's own call can produce, not by loosening the assertion or adding thread-lifecycle management the rest of the suite doesn't use.
- 2026-09-08 `kapowarr/t-041` — A source that is sometimes-restricted needs a per-item eligibility check enforced once at the data boundary (here, before a download link is ever built), not a per-source allow/deny decision like a fully-open or fully-restricted source would use -- and the adversarial test that matters most is proving the restricted case can never produce the real acquisition artifact, not just that the happy path works.
- 2026-09-08 `kapowarr/t-040` — Once Silas released the soft scope-gate with a conservative default (metadata/search discovery plus link-out only, never automate a download from the shadow library), the existing `DiscoverSources` registry in `backend.features.discover` (kind_robots-fork Kapowarr) already had the exact extension point this needed -- register a second `DiscoverSource` alongside GetComics, reusing all its merge/cross-reference/link-out plumbing untouched. Worth checking an existing plugin-style registry's own docstring for "a second X could be added later" promises before assuming a scope-constrained integration needs new orchestration.
- 2026-09-07 `kind-robots/t-061` — A pitch's own "Suggested first task" section splitting a two-part fix into two follow-on tasks is worth honoring literally rather than forcing both into one PR: the conductorSlug immutability guard landed clean and small (kind_robots#2497), while the slug-collision-helper consolidation (split into t-094) needs its own careful pass because an existing source-text regression guard (verifyAppmakerScaffoldCollisionGuard.ts) asserts the exact inline shape of the code it would refactor away.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-08T21:31:34Z_
