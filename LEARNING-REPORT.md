# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-13T12:04:54Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **942**
- Outcomes: blocked: 16, cancelled: 1, done: 925
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
| conductor | 99 | 100% |
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
| interface-vision | 134 | 100% |
| kapowarr | 52 | 100% |
| kind-economy | 10 | 100% |
| kind-robots | 55 | 98% |
| kindrobots-unraid | 8 | 100% |
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
| text-generation | 6 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 925 | 99% |

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

- 2026-09-13 `interface-vision/t-104` — Slice 260: a fresh full-repo class-frequency survey scoped to component-styling token families (badge/btn/input/select/checkbox/textarea/text-/icon/loading/etc.) rather than raw flex-layout utility combos (flex gap-2 items-center and similar score far higher by count but are structural, not the visual/design-token surfaces this umbrella targets) found a clean new three-size family (kr-loading-primary-xs/-sm/-md) at 17 exact-match occurrences across 13 files. Reinforces slice 249/253's precedent of bundling sibling sizes/colors of the same shape into one slice with separate per-primitive codemods, and that vue-tsc/eslint/verifyKrClassCoverage.ts/verifyLayoutContract.ts run locally via provision_kind_robots_deps.sh catch what CI would catch, before ever opening the PR.
- 2026-09-13 `kindrobots-unraid/t-018` — Fourth occurrence of the 502/503 outage class (t-014, t-015, t-017, t-018), again caught only because a scheduled sweep happened to notice rather than any alerting. Closed on objective recovery evidence alone (8 consecutive healthy curls against / and /api/health/database over ~20s, schemaCurrent: true) per docs/state-reconciliation.md -- no Unraid/Alexandria access was needed or used, since the sandbox's unrestricted HTTPS egress to kindrobots.org is sufficient to confirm the task's own stated close-out criterion. approved_by_human stays false per the t-014/t-015/t-017 precedent. kindrobots-unraid/t-016 (external health probe/alert) is still ready/unclaimed after four occurrences -- this is the actual fix for the detection gap, not another manual sweep catching it by luck.
- 2026-09-13 `interface-vision/t-136` — Kaizen from t-135 closed the gap outright: verifyKrClassCoverage.ts (kind_robots#2696) asserts every static kr-* class token used in a components/+pages/ template has a matching .kr-* rule, no ratchet/baseline since an undefined kr-* reference is never intentional. The PR's own comment-migration-contract check was red at review time from an unrelated live kindrobots.org 502 (kindrobots-unraid/t-018, confirmed via direct curl and one re-run reproducing the identical error) -- correctly triaged as not-this-PR's failure and merged anyway once every check touching the actual diff was green.
- 2026-09-13 `interface-vision/t-135` — Four consecutive t-104 badge-migration slices (#2691-#2694, three different sessions) introduced and reused a CSS class name (kr-badge-accent-sm) that was never defined, because every check that passed on those PRs (TypeScript, eslint, layout-contract, the full Storybook/Narrative contract suite) type-checks templates and structure but never asserts that a referenced kr-* @apply target actually exists in tailwind.css -- so four real visual regressions (unstyled plain text instead of a badge) shipped to production invisibly. Caught only because a Reviewer pass grepped the CSS file directly instead of trusting green CI. Kaizen filed on the fix PR: add a cheap repo-wide check asserting every kr-* class token used in a class="..." attribute has a matching rule in tailwind.css, so the next missing-primitive slice fails fast in CI.
- 2026-09-13 `kindrobots-unraid/t-017` — A recovered production incident should be closed on objective evidence (health endpoint + SSR check + the actual fix commit on kind_robots main) rather than left needs-human pending root-cause paperwork once the root cause is already known from a merged fix -- docs/state-reconciliation.md's 'Closing human gates safely' section and CLAUDE.md's session-end rule both say so explicitly. approved_by_human stays false per the t-014/t-015 precedent for this exact outage class; only Silas sets that field. Third occurrence of this outage class with kindrobots-unraid/t-016 (external health probe) still unclaimed -- worth prioritizing so a lucky scheduled sweep isn't the detection mechanism again.
- 2026-09-12 `conductor/t-155` — Reused project_lifecycle.ordered_workable_slugs (the same helper check_priority_queue_starvation.py and next_ready_task.py already use) to sort audit_human_gates.py's report by priority-queue rank instead of writing new roadmap-walking logic -- confirms t-149's lesson generalizes: grep for the existing shared module before writing a new roadmap-ordering tool, and a report can be re-ordered by reusing pickup-order logic without touching what it detects.
- 2026-09-12 `conductor/t-149` — check_priority_queue_starvation.py was straightforward to build correctly on the first pass by reusing the exact shared modules (roadmap_claims, roadmap_deps, daily_gate, project_lifecycle) next_ready_task.py already uses, rather than reimplementing claim/staleness/dependency logic -- the two scripts structurally cannot disagree about what counts as claimable ready work. Worth defaulting to this pattern (grep for the existing shared module before writing new roadmap-walking logic) for any future roadmap-reading tool.
- 2026-09-12 `interface-vision/t-131` — A task can sit at status: review with a fully-implemented, pushed branch and never actually be reviewable, because no PR was ever opened from it -- observed for worker/interface-vision-t-131-20260912T151712Z-oai11 (real, scoped, single-line commit matching the task exactly). AGENTS.md's step 7 assumes 'set status: review before opening the PR' happens as one atomic sequence, but a session can crash or end between the roadmap edit and the actual gh pr create/GitHub MCP create_pull_request call, leaving status: review with nothing behind it -- indistinguishable from a genuinely in-review PR without checking GitHub directly. A later session (this one) found it by checking kind_robots' branch list against its open+closed PR list for a task at status: review and finding neither. Worth a lightweight check in whatever surfaces 'reviewable work' (select_role.py's reviewer signal, or a dedicated staleness check): a status: review task whose implementation branch has no open OR merged PR after some age is the same class of gap check_pr_merged_drift.py already covers in the other direction (a merged PR the roadmap doesn't know about).
- 2026-09-12 `interface-vision/t-104` — Slice 248 (kr-img-cover/size-full shorthand): a kr-* class-token codemod can break a hand-authored contract checker that does raw string matching on the literal source text of the class it migrates -- distinct from every failure class this umbrella has hit so far (layout-contract geometry checks, the tailwind @apply build-pipeline check from slice 247). verifyStorybookStudio.mjs asserted the bare string 'object-cover' inside narrative-ingredient-card.vue; the codemod correctly replaced it with .kr-img-cover (CSS-identical rendering, h-full w-full object-cover under @apply), so the intent the contract actually cared about (aspect-ratio + object-fit-cover + gradient overlay markup present) still held, but the literal substring no longer did. Caught by CI's dedicated contract-check job, not by eslint/vue-tsc/prettier/layout-contract/npm run build (none of which inspect for a specific class token's literal presence). Fixed by adding an includesAllOrAlternatives() helper so a contract entry can list acceptable alternate spellings of the same rendered shape. Before a future kr-* slice migrates a file, grep the repo's verify*.{mjs,ts} scripts for that file's basename AND for the specific class tokens being migrated -- a hardcoded string-literal assertion on a class name is a distinct risk class from the geometry/build-pipeline ones already documented, and grepping for the file alone (as this slice partly did before pushing) is not sufficient without also checking whether any hit asserts the literal token text.
- 2026-09-12 `interface-vision/t-104` — Slice 247: before writing @apply <bare-word> in tailwind.css for a new kr-* primitive, grep node_modules/daisyui and node_modules/tailwindcss for that exact token first -- a class that is still hand-rolled correctly in HTML (silently inert if unrecognized) is not proof the same token is @apply-able, since Tailwind's @apply requires every token to resolve to a real registered utility and errors the production build otherwise. `form-control` was removed from daisyUI in the v4->v5 upgrade but never swept from ~43 call sites across the repo, so it read as a normal hand-rolled component class right up until the build step. Caught by the CI "Build production image" job (the only one of ~50 checks that actually runs a real production build rather than vue-tsc/eslint/unit-level checks), not by any local verification step run before the first push -- worth treating a brand-new bare-word @apply target as needing this grep check up front, the same way BOUNDED_EXTRAS already gets checked before trusting an estimate.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-13T12:04:54Z_
