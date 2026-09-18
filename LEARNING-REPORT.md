# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-18T14:56:58Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1031**
- Outcomes: blocked: 16, cancelled: 1, done: 1014
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
| art-archive | 12 | 100% |
| art-generator-connect | 3 | 100% |
| brainstorm | 26 | 96% |
| butterfly-gallery | 12 | 100% |
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
| kind-robots | 64 | 98% |
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
| storybook | 29 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 7 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 1014 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 30 |
| transient | 17 |
| actionable | 15 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 47% success over 17 closed tasks; aim the next kaizen task here
- failure category `quality` — 30 occurrences; look for the shared cause across its records
- failure category `transient` — 17 occurrences; look for the shared cause across its records
- failure category `actionable` — 15 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-18 `butterfly-gallery/t-017` — When a CSS animation targets a property an inline style already sets for layout (e.g. pileStyle()'s inline `transform: translateX(...) rotate(...)`), animate the standalone `scale`/`translate`/`rotate` CSS properties instead of `transform` -- they compose independently with the inline `transform` rather than clobbering it for the animation's duration. This codebase already used this pattern for .pile-card's hover lift (`translate: 0 -14px` rather than `transform: translateY(-14px)`) before this task extended it to a selection-pop keyframe.
- 2026-09-18 `butterfly-gallery/t-012` — check_pr_handoff_template.py's check-run history can carry a stale `failure` entry from an earlier PR-body revision (e.g. missing the "### Notes for reviewer" heading) even after the Worker edits the body and a later run of the same check passes. Verify mergeable_state plus the latest commit's own check-run/PR_BODY content via get_job_logs before treating an older failed run as a live blocker.
- 2026-09-18 `butterfly-gallery/t-011` — A sandbox with no production DATABASE_URL can still queue real ArtJobs by POSTing to /api/art/queue with KR_API_TOKEN as x-api-key, building the Krea2 workflow via the real buildKrea2WorkflowFromRequest under tsx (a node_modules/~ symlink workaround resolves the repo's '~' import alias without a full Nuxt build). "Producing" a static art asset set is a two-step task, queuing the ArtJob now, then a separate follow-up (filed as t-028) to wire the rendered images in once the async relay finishes — don't block the first step's closure on the second happening within the same session.
- 2026-09-18 `art-archive/t-011` — Preserve path-derived membership as system-owned state and expose custom membership as an additive relation, rather than reusing replace-style collection APIs that could erase the folder invariant.
- 2026-09-18 `butterfly-gallery/t-009` — Reading the store's existing visiblePile filter logic before building any UI surfaced a real, previously-invisible bug: trash visibility was folded into matchState === 'missing' by the earlier t-003 scaffolding, but trashing an entry never touches matchState, so that path never actually revealed a real trashed entry (confirmed against the fixture data: entry 9005 is trashed:true, matchState:'matched'). Fixed by giving trash visibility its own filters.trashView dimension, decoupled from matchState, and adding direct unit coverage for the decoupling rather than assuming the old combined check was intentional just because it had shipped before.
- 2026-09-18 `art-archive/t-010` — Pass-1 rejection (kind_robots#2836) flagged two real, locally-reproduced defects in the new admin Art Archive browser -- a nonexistent userStore.isInitialized field (correct name: initialized) and a bare kr-select class with no matching tailwind.css primitive (kr-select-sm already existed and was the fix). The Worker's pass-2 retry addressed both directly and named them in the PR body; all 51 checks went green on the first re-run. Confirms retry_context written at rejection time is enough for a clean second pass when the failures are concrete and locally reproducible rather than ambiguous.
- 2026-09-18 `butterfly-gallery/t-007` — Extracting the field-level action rules into small, pure appliers (stores/helpers/butterflyGalleryActions.ts) before wiring them behind an injectable adapter made the whole task independently unit-testable via a plain tsx script (this repo has no vitest) without needing Pinia/component setup at all -- the store's existing sync setRating()/applyBinOutcome() mutated a plain object reference regardless of whether it was reactive, so the refactor into standalone functions cost nothing and paid for itself immediately in test coverage.
- 2026-09-18 `butterfly-gallery/t-010` — Verified against the merged file directly (grep for runway-slot/drop-funnel/ preset-bin/right-rail/pile-card/robot-animation-slot) rather than trusting the PR description alone before marking this milestone-3 task done -- the PR's own self-report matched what actually shipped, but checking the diff itself is what makes that confidence earned rather than assumed.
- 2026-09-18 `butterfly-gallery/t-008` — Same PR (kind_robots#2834) substantially implemented the right-rail Image Info panel ahead of its own roadmap task being claimed. Closed with two minor field-list gaps noted (no filename/title or dimensions in the compact view) rather than reopening or leaving it artificially at ready -- the note's core ask (compact panel + Details expand + Cleanup/Trash below it) is met, and gating done-ness on a cosmetic completeness nit would misrepresent the task's actual state.
- 2026-09-18 `butterfly-gallery/t-006` — Reconciled from kind_robots#2834 rather than implemented directly this cycle -- Silas built the full approved-stage composition himself in a live session that ran concurrently with this session's t-005 work, superseding t-005's narrower component-extraction approach and covering t-006/t-008/t-010's scope in one PR. The conflict this produced (both PRs touched pages/butterfly-gallery.vue, based on the same stale pre-t-005 commit) resolved cleanly by keeping the newer, more complete implementation and removing the now-orphaned t-005 components/store additions that nothing referenced. Worth a standing habit: when a design-lock/spec commit lands mid-task (visible via a fresh git log on the docs/roadmap repo), re-check for a matching implementation PR before assuming your own in-flight work is still the only game in town.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-18T14:56:58Z_
