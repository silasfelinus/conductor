# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-08T03:01:02Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **890**
- Outcomes: blocked: 16, cancelled: 1, done: 873
- Success rate: **98%**
- Average passes on successful tasks: **0.1**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 72 | 99% |
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
| conductor | 93 | 100% |
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
| interface-vision | 105 | 100% |
| kapowarr | 52 | 100% |
| kind-economy | 9 | 100% |
| kind-robots | 55 | 98% |
| kindrobots-unraid | 5 | 100% |
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
| software | 874 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 17 |
| transient | 13 |
| actionable | 12 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 17 occurrences; look for the shared cause across its records
- failure category `transient` — 13 occurrences; look for the shared cause across its records
- failure category `actionable` — 12 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-08 `kapowarr/t-041` — A source that is sometimes-restricted needs a per-item eligibility check enforced once at the data boundary (here, before a download link is ever built), not a per-source allow/deny decision like a fully-open or fully-restricted source would use -- and the adversarial test that matters most is proving the restricted case can never produce the real acquisition artifact, not just that the happy path works.
- 2026-09-08 `kapowarr/t-040` — Once Silas released the soft scope-gate with a conservative default (metadata/search discovery plus link-out only, never automate a download from the shadow library), the existing `DiscoverSources` registry in `backend.features.discover` (kind_robots-fork Kapowarr) already had the exact extension point this needed -- register a second `DiscoverSource` alongside GetComics, reusing all its merge/cross-reference/link-out plumbing untouched. Worth checking an existing plugin-style registry's own docstring for "a second X could be added later" promises before assuming a scope-constrained integration needs new orchestration.
- 2026-09-07 `kind-robots/t-061` — A pitch's own "Suggested first task" section splitting a two-part fix into two follow-on tasks is worth honoring literally rather than forcing both into one PR: the conductorSlug immutability guard landed clean and small (kind_robots#2497), while the slug-collision-helper consolidation (split into t-094) needs its own careful pass because an existing source-text regression guard (verifyAppmakerScaffoldCollisionGuard.ts) asserts the exact inline shape of the code it would refactor away.
- 2026-09-07 `kind-economy/t-023` — Same pattern as t-014/t-022 in this batch: a task released from needs-human back to ready under the 2026-09-07 human-gate-simplification policy already had its deliverable (THE-SIFT-DESIGN.md) complete and matching the release note's ask verbatim, including the hardest mechanical problem (attribution without custody) resolved concretely. Reconciled to done rather than treated as new design work owed.
- 2026-09-07 `kind-economy/t-022` — Same pattern as t-014 in this batch: a task released from needs-human back to ready under the 2026-09-07 human-gate-simplification policy already had its deliverable (BUTTERFLY-EVENT-PLAN.md) complete and matching the release note's ask verbatim. Reconciled to done rather than treated as new planning work owed.
- 2026-09-07 `kind-economy/t-014` — The 2026-09-07 human-gate simplification pass flipped several complete-but-parked needs-human design tasks back to ready with a "design around the accepted model, don't wait on Silas" instruction. For kind-economy/t-014 the deliverable (PAYOUT-MECHANISM-DESIGN.md) already matched that instruction verbatim from 2026-08-19 -- the correct action was reconciling stale roadmap state to done, not producing new design content. Check whether a task's own deliverable file already satisfies a "release" note before assuming more design work is owed.
- 2026-09-07 `cthulhuquarium/t-041` — The task's only open item (Decision 2: whether the egg purchase OPTION itself should be concealed, vs. only its CONTENTS) was resolved by Silas's 2026-09-07 default-recommendation policy in the task note itself -- keep the option visibly on sale, hide only the species. Re-reading the already-merged implementation (kind_robots PR #2172) against that decision found it already compliant end to end: the egg catalog API/UI exposes only rarity/size/cost/description, never species or the eligible pool; hatchEggForUser resolves the species server-side at hatch time only; the shop panel has no discovery gate on the purchase option; the hatch reveal dialog always shows the result, never silently. No code change was needed -- this closed as a verification-only pass. General lesson: when a roadmap task's remaining note is a Silas decision on an already-shipped feature rather than a design gate blocking new work, check the live diff against the decision before assuming implementation work remains -- a 'ready' status can mean 'verify and close', not always 'build something'.
- 2026-09-07 `cthulhuquarium/t-019` — Balance pass on real play data had no live DB/telemetry to retune hunger/debris/offline-income against (same gap the task's own note flagged weeks earlier), and Silas's 2026-09-07 policy resolved that by substituting a conservative data-and-design-driven pass rather than blocking further: extend the milestone ladder using the existing simulation and design docs, treat real telemetry as future iterative tuning. Extended the bestiary milestone ladder past bestiary_20 (4 breakpoints, +2 each, covering 20/151 species) with 7 new decelerating breakpoints (25/35/50/70/95/125/151, reward shrinking +2->+1->+0) landing on slots_cap 19 -- comfortably under the ~50 threshold already flagged as trivializing the tank-packing design. Re-ran simulate_economy.py to confirm no regression (output byte-identical since the 2-hour single-fish-line scenario never reaches a bestiary breakpoint) and added a structural (not just simulated) argument in ECONOMY.md for why offline income can never exceed active play under the current formula, rather than re-deriving it from scratch next time. General lesson: when a task's own gap note already sketches the shape of a defensible answer (decelerating ladder, terminate well below the collection total, later breakpoints pay in non-capacity rewards), a 'data-only, conservative' policy resolution is enough to act on directly -- it does not require re-opening design questions the note already closed. Also: a PR's CI 'Python test suite' failure should always be checked against origin/main before treating it as this diff's problem -- test_current_project_lifecycle.py's active-project-with-no-open-tasks check (alexa-integration/mandarin-tutor/media-watchlist/scene-animator) was already failing on main before this PR touched anything, confirmed by running the test against a fresh origin/main checkout.
- 2026-09-07 `interface-vision/t-104` — Slice 133 found kr-panel-compact-row (rounded-xl border border-base-300 bg-base-100 px-3 py-2, 5 occurrences across 4 files) by the same exact- contiguous-token-window survey method used since slice 130: extract every class attribute containing border-base-300, tokenize, and count fixed-width windows around it to surface repeated shapes not yet in VARIANTS, rather than scanning file-by-file. This slice's pool sat right at the established viability floor (5 safe occurrences after excluding 2 unsafe DaisyUI-label matches in art-interact.vue) -- worth noting for whoever eventually judges the umbrella's mechanical phase exhausted: the token-window survey keeps finding small-but-real pools well past the point slice 129's note predicted the VARIANTS list itself was exhausted, so 'small pool this slice' is not yet evidence the survey method has stopped paying off. No CI stall this slice (Build production image ~9.5min, all 49 checks green first try) -- contrasts with slice 130's two independent stalls in the same session; the conductor/t-132 and t-124-tracked infra flakiness remains intermittent, not constant.
- 2026-09-07 `interface-vision/t-104` — Slice 123 of the recurring kr-panel consistency sweep opened the first opacity-variant branch of the .kr-panel-muted family (.kr-panel-tint-sm/-md at bg-base-200/40) rather than continuing to treat every non-exact-match occurrence as needing manual review. Prior slices (117-122) only ever matched a class token sequence byte-for-byte against a solid-color background token; once the codemod also carries the opacity-suffixed token as its own listed variant, the exact-match approach generalizes cleanly to the alpha-channel dimension without loosening the matcher's safety guarantees (still a literal token-sequence match, still gated by the same safe-extras allowlist). Found 12 real occurrences across 8 files this way that a purely solid-background scan would never have surfaced. General lesson for a long-running class-consolidation sweep: when a 'needs manual review, not a safe codemod' note names a *reason* (here: opacity changes appearance) rather than a genuine ambiguity, check whether that reason is itself just an unhandled dimension of the same exact-match pattern before assuming the whole pool needs hand judgment -- an opacity-suffixed background is still a literal, deterministic token to match on, not a judgment call.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-08T03:01:02Z_
