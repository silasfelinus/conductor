# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-12T19:51:50Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **936**
- Outcomes: blocked: 16, cancelled: 1, done: 919
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
| conductor | 98 | 100% |
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
| interface-vision | 131 | 100% |
| kapowarr | 52 | 100% |
| kind-economy | 10 | 100% |
| kind-robots | 55 | 98% |
| kindrobots-unraid | 6 | 100% |
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
| software | 919 | 99% |

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

- 2026-09-12 `conductor/t-149` — check_priority_queue_starvation.py was straightforward to build correctly on the first pass by reusing the exact shared modules (roadmap_claims, roadmap_deps, daily_gate, project_lifecycle) next_ready_task.py already uses, rather than reimplementing claim/staleness/dependency logic -- the two scripts structurally cannot disagree about what counts as claimable ready work. Worth defaulting to this pattern (grep for the existing shared module before writing new roadmap-walking logic) for any future roadmap-reading tool.
- 2026-09-12 `interface-vision/t-131` — A task can sit at status: review with a fully-implemented, pushed branch and never actually be reviewable, because no PR was ever opened from it -- observed for worker/interface-vision-t-131-20260912T151712Z-oai11 (real, scoped, single-line commit matching the task exactly). AGENTS.md's step 7 assumes 'set status: review before opening the PR' happens as one atomic sequence, but a session can crash or end between the roadmap edit and the actual gh pr create/GitHub MCP create_pull_request call, leaving status: review with nothing behind it -- indistinguishable from a genuinely in-review PR without checking GitHub directly. A later session (this one) found it by checking kind_robots' branch list against its open+closed PR list for a task at status: review and finding neither. Worth a lightweight check in whatever surfaces 'reviewable work' (select_role.py's reviewer signal, or a dedicated staleness check): a status: review task whose implementation branch has no open OR merged PR after some age is the same class of gap check_pr_merged_drift.py already covers in the other direction (a merged PR the roadmap doesn't know about).
- 2026-09-12 `interface-vision/t-104` — Slice 248 (kr-img-cover/size-full shorthand): a kr-* class-token codemod can break a hand-authored contract checker that does raw string matching on the literal source text of the class it migrates -- distinct from every failure class this umbrella has hit so far (layout-contract geometry checks, the tailwind @apply build-pipeline check from slice 247). verifyStorybookStudio.mjs asserted the bare string 'object-cover' inside narrative-ingredient-card.vue; the codemod correctly replaced it with .kr-img-cover (CSS-identical rendering, h-full w-full object-cover under @apply), so the intent the contract actually cared about (aspect-ratio + object-fit-cover + gradient overlay markup present) still held, but the literal substring no longer did. Caught by CI's dedicated contract-check job, not by eslint/vue-tsc/prettier/layout-contract/npm run build (none of which inspect for a specific class token's literal presence). Fixed by adding an includesAllOrAlternatives() helper so a contract entry can list acceptable alternate spellings of the same rendered shape. Before a future kr-* slice migrates a file, grep the repo's verify*.{mjs,ts} scripts for that file's basename AND for the specific class tokens being migrated -- a hardcoded string-literal assertion on a class name is a distinct risk class from the geometry/build-pipeline ones already documented, and grepping for the file alone (as this slice partly did before pushing) is not sufficient without also checking whether any hit asserts the literal token text.
- 2026-09-12 `interface-vision/t-104` — Slice 247: before writing @apply <bare-word> in tailwind.css for a new kr-* primitive, grep node_modules/daisyui and node_modules/tailwindcss for that exact token first -- a class that is still hand-rolled correctly in HTML (silently inert if unrecognized) is not proof the same token is @apply-able, since Tailwind's @apply requires every token to resolve to a real registered utility and errors the production build otherwise. `form-control` was removed from daisyUI in the v4->v5 upgrade but never swept from ~43 call sites across the repo, so it read as a normal hand-rolled component class right up until the build step. Caught by the CI "Build production image" job (the only one of ~50 checks that actually runs a real production build rather than vue-tsc/eslint/unit-level checks), not by any local verification step run before the first push -- worth treating a brand-new bare-word @apply target as needing this grep check up front, the same way BOUNDED_EXTRAS already gets checked before trusting an estimate.
- 2026-09-12 `interface-vision/t-134` — When a sized primitive (kr-toggle-<color>-sm) is added after its sizeless sibling (kr-toggle-<color>) already exists in the same codemod, FAMILIES ordering is a correctness requirement, not just style: the sizeless base token set is a strict subset of the sized one's, so trying the sizeless family first would silently swallow the size token as an unrecognized 'extra' and skip the more specific primitive. Listing every sized family before any sizeless one (verified by re-running the dry run to 0 remaining candidates) avoided that regardless of what BOUNDED_EXTRAS happened to allow.
- 2026-09-12 `interface-vision/t-104` — Slice 246: when a recurring umbrella's kaizen note calls for 'a fresh full-repo class-frequency survey outside all now-closed families' rather than naming the next target directly, build the survey as a small reusable script (kr_class_frequency_survey.py) rather than a one-off grep -- it excludes pure-layout combos (flex/gap/items/justify/etc) up front, since those risk the geometry changes this umbrella explicitly disclaims, and surfaces genuine component-color-variant candidates (DaisyUI toggle colors) instead. The same script is available for the next slice's survey too.
- 2026-09-12 `interface-vision/t-132` — A CI-config kaizen (adding a warning-only shellcheck pass to an existing bash -n step) is safest when it reuses the same changed-file discovery already computed in that step rather than re-running git diff -- one mapfile call, then bash -n and shellcheck back to back with `|| true` on the new one, so the existing hard-failing check's behavior is provably untouched. Installing the tool locally (apt-get install shellcheck) to confirm a real finding logs but doesn't propagate a nonzero exit was worth the minute it took -- cheaper than trusting `|| true` semantics from memory.
- 2026-09-12 `storybook/t-032` — Same DB-backed-verifier-catches-what-the-sandbox-cannot pattern as t-029, different write path: a character-sheet play created its LifeChoice row with rewardId null then patched it in a second update, so the persisted row ended up correct but the API response returned null for the played card on the very turn it was played. A two-step create-then-patch can be internally consistent in the database while still returning a wrong response for that one request -- resolve foreign keys before the transaction and write them on the initial create when the response of that same call needs to reflect them.
- 2026-09-12 `storybook/t-030` — Roadmap state can drift from reality even without a Reviewer rejection: kind_robots#2662 (implementing t-029/t-030/t-032/t-033) merged clean, but the four conductor tasks it closed were never flipped to done because this slice was never run through claim_task.py -- there was no queued task-events close-out to catch it. State-reconciliation after a cross-repo merge needs an explicit roadmap sweep, not just trust that a close-out event exists somewhere.
- 2026-09-12 `storybook/t-029` — kind_robots#2662's own DB-backed verifyStorybookPlayLoop.ts caught a real write-boundary bug the authoring sandbox (no database, no docker daemon) could not have found: the +-2 moveEffects clamp existed only inside the narration validator, one layer above where submitStoryTurn actually wrote LifeStat rows, so any caller that bypassed the validator could move an axis by 9 or write an axis the deck does not declare. Fixed by adding a clampEffectsToDeck() at the write boundary itself. When a schema-affecting engine PR's own body flags 'this DB-backed job is the one to watch, I could not run it locally' -- take that literally: wait for the real CI run and read its actual failure output before assuming a design-reviewed diff is safe to merge, even when every DB-free suite passed.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-12T19:51:50Z_
