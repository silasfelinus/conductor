# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-02T06:48:50Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **462**
- Outcomes: blocked: 13, cancelled: 1, done: 448
- Success rate: **97%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 55 | 98% |
| alexa-integration | 2 | 100% |
| animation-manager | 13 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 6 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 25 | 100% |
| conductor | 59 | 100% |
| conductor-app | 2 | 100% |
| davinci | 2 | 100% |
| digital-storefront | 24 | 100% |
| dream-cycle | 18 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 4 | 100% |
| interface-vision | 21 | 100% |
| kind-robots | 39 | 97% |
| kindrobots-unraid | 4 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 48 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 2 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 447 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 9 |
| actionable | 9 |
| transient | 6 |
| scope | 1 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `quality` — 9 occurrences; look for the shared cause across its records
- failure category `actionable` — 9 occurrences; look for the shared cause across its records
- failure category `transient` — 6 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-02 `interface-vision/t-018` — The task note's orphan-audit claim ("only 6 components use displayStore.ts") was wrong in a load-bearing way -- it missed memoryStore.ts (a store, not a component) reading displayStore.viewportSize to size the live, routed Memory Dungeon board, and kind-loader.vue calling displayStore.initialize() as real app-startup wiring. Investigating before deleting (grep ALL importers, not just the ones matching the expected shape) caught this before it shipped as a silent behavior regression; the store was left in place and split into its own follow-up task (t-045) instead of forced through under the cleanup label.

- 2026-08-02 `interface-vision/t-014` — A dedicated research pass (Explore agent surveying existing layout-contract examples, karma/mana/achievement plumbing already shipped by t-010, and the User schema) before writing any code meant zero rework: every new UI section reused an existing store/component instead of duplicating one, and the only schema change needed was a single additive nullable column (introDismissedAt) for the one genuinely new piece of state (intro dismissal). Deliberately scoped out extending user-galleries.vue to the remaining two object types (Facets/Projects) rather than let the task grow past its landable core -- filed as a kaizen suggestion instead.

- 2026-08-02 `interface-vision/t-014` — kind_robots PR #1292 (implemented and reviewed by a different session earlier in the day) went stale against main after this session merged the unrelated PR #1293 a few minutes later -- both PRs ran `prisma generate` independently against overlapping generated-client scaffolding (prisma/generated/prisma/internal/class.ts), producing a real textual conflict GitHub correctly flagged as `mergeable_state: dirty` despite a local `git merge-tree` dry run initially looking clean. Fix was mechanical and low-risk: merge main into the PR branch, let `prisma generate` regenerate the one conflicting file fresh rather than hand-resolving it, verify (prisma validate + vue-tsc clean), push, wait for CI, merge. Same class of "regenerate, don't hand-merge" fix as the STATUS.md/workspace.html auto-gen convention, just for kind_robots' generated Prisma client -- worth generalizing that convention beyond conductor's own auto-gen files.

- 2026-08-02 `interface-vision/t-015` — "Close the Builder gaps" bundled five independent fixes at very different scales (a new additive ProjectFacet table + migration, a Prisma-relation normalization needing no migration since the underlying FK constraints already existed, a missing Bot facets.put endpoint, a full Character client facet store + UI) plus registering PROJECT/FACET builders, which turned out to need a card-deck-scale UI buildout of its own. Splitting that one sub-part into t-042 rather than forcing it into the same PR kept the landed diff coherent and fully verified; a task note that lists N "also"s is worth pre-scanning for the one that's actually a different size class before claiming it as a single pass.

- 2026-08-02 `interface-vision/t-041` — Resolve stale navigation hints against the live dashboard manifest; do not invent tabs when the intended product placement is genuinely undecided.
- 2026-08-02 `interface-vision/t-038` — When a task's own name echoes the parent it lives under (a 'dashboard' tab inside a 'user' dashboard, mounting user-dashboard.vue), check every sibling for the same slot before picking a fix -- every other dashboardConfigs entry already used a real content-named default tab key, so renaming to match that pattern was a smaller, safer diff than inventing new always-shown-default semantics from scratch.
- 2026-08-02 `interface-vision/t-023` — Before sweeping a layout allow-list, audit exact-markup verifier locks so product cleanup updates the owning semantic contract instead of restoring obsolete markup.
- 2026-08-02 `interface-vision/t-037` — The task note asked for 2-3 mockups since the fold "needs real product decisions," mirroring t-001/t-002's blank-canvas aesthetic-pick pattern -- but the three open questions here (does cockpit content collapse to one kr-toolbar line, do the two tab strips merge or does one become a dropdown, does the decorative wrapper become .kr-surface) were already answered by this project's own t-004 contract, which built kr-toolbar and kr-surface specifically for this shape of problem. Not every "needs product decisions" task is a blank aesthetic choice like theater/storybook/playground -- some are structural questions the project's existing rules already resolve. Building throwaway A/B/C toggle scaffolding for a question the contract already answers would have been the over-engineering the task itself warns against elsewhere. Also: vercel.json disables PR-preview deploys for claude/*/worker/*/ agent/*/conductor/* branches (cost-saving), so visual verification for agent-authored branches has to happen post-merge against the production deployment, not via a pre-merge Vercel preview -- AGENTS.md's documented preview technique (~L338-366) doesn't currently note this exception.

- 2026-08-01 `interface-vision/t-013` — Before touching a large "un-nest this component" task, trace the actual mount path first -- conductor-page.vue's own 'overview' and 'brainstorm' viewMode branches, plus a chunk of its cockpit bar, were structurally unreachable because conductor-manager.vue (its sole importer) intercepts those workspaceCardKey values and renders a different component before ConductorPage ever mounts. A component can look nested/cluttered while actually being half dead code wearing live-code's clothes; grep for the component's importers and read the routing logic one level up before assuming every rendered-looking branch is reachable. Separately: when a task names multiple target files, verify each one's claim independently rather than assuming a shared premise -- art-manager.vue's "tabs are themselves dashboards" claim didn't hold on inspection even though the conductor-page.vue and user-manager.vue claims in the same task note did.

- 2026-08-01 `interface-vision/t-011` — A roadmap task note's factual claims about the codebase ("X is the most complete widget", "Y is imported by nothing") are a snapshot from planning time, not a live fact -- t-007 and t-009 both merged the same day this task's note was written, and by the time t-011 was picked up the note's premise (revive art-reactions.vue as canonical) was already stale: reaction-card.vue had already superseded it as the generic, actively-wired review panel. Read the current state of every file a note names before trusting its characterization, and when the literal instruction conflicts with what the code now shows, do the thing that closes the real gap (here: allowReviews was read by no gallery, not "no canonical panel exists") and document the deviation explicitly rather than either blindly following a stale instruction or silently reinterpreting it.


---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-02T06:48:50Z_
