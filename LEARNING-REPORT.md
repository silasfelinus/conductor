# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-02T05:05:00Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **460**
- Outcomes: blocked: 13, cancelled: 1, done: 446
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
| interface-vision | 19 | 100% |
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
| software | 445 | 99% |

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

- 2026-08-02 `interface-vision/t-014` — kind_robots PR #1292 (implemented and reviewed by a different session earlier in the day) went stale against main after this session merged the unrelated PR #1293 a few minutes later -- both PRs ran `prisma generate` independently against overlapping generated-client scaffolding (prisma/generated/prisma/internal/class.ts), producing a real textual conflict GitHub correctly flagged as `mergeable_state: dirty` despite a local `git merge-tree` dry run initially looking clean. Fix was mechanical and low-risk: merge main into the PR branch, let `prisma generate` regenerate the one conflicting file fresh rather than hand-resolving it, verify (prisma validate + vue-tsc clean), push, wait for CI, merge. Same class of "regenerate, don't hand-merge" fix as the STATUS.md/workspace.html auto-gen convention, just for kind_robots' generated Prisma client -- worth generalizing that convention beyond conductor's own auto-gen files.

- 2026-08-02 `interface-vision/t-015` — "Close the Builder gaps" bundled five independent fixes at very different scales (a new additive ProjectFacet table + migration, a Prisma-relation normalization needing no migration since the underlying FK constraints already existed, a missing Bot facets.put endpoint, a full Character client facet store + UI) plus registering PROJECT/FACET builders, which turned out to need a card-deck-scale UI buildout of its own. Splitting that one sub-part into t-042 rather than forcing it into the same PR kept the landed diff coherent and fully verified; a task note that lists N "also"s is worth pre-scanning for the one that's actually a different size class before claiming it as a single pass.

- 2026-08-02 `interface-vision/t-041` — Resolve stale navigation hints against the live dashboard manifest; do not invent tabs when the intended product placement is genuinely undecided.
- 2026-08-02 `interface-vision/t-038` — When a task's own name echoes the parent it lives under (a 'dashboard' tab inside a 'user' dashboard, mounting user-dashboard.vue), check every sibling for the same slot before picking a fix -- every other dashboardConfigs entry already used a real content-named default tab key, so renaming to match that pattern was a smaller, safer diff than inventing new always-shown-default semantics from scratch.
- 2026-08-02 `interface-vision/t-023` — Before sweeping a layout allow-list, audit exact-markup verifier locks so product cleanup updates the owning semantic contract instead of restoring obsolete markup.
- 2026-08-02 `interface-vision/t-037` — The task note asked for 2-3 mockups since the fold "needs real product decisions," mirroring t-001/t-002's blank-canvas aesthetic-pick pattern -- but the three open questions here (does cockpit content collapse to one kr-toolbar line, do the two tab strips merge or does one become a dropdown, does the decorative wrapper become .kr-surface) were already answered by this project's own t-004 contract, which built kr-toolbar and kr-surface specifically for this shape of problem. Not every "needs product decisions" task is a blank aesthetic choice like theater/storybook/playground -- some are structural questions the project's existing rules already resolve. Building throwaway A/B/C toggle scaffolding for a question the contract already answers would have been the over-engineering the task itself warns against elsewhere. Also: vercel.json disables PR-preview deploys for claude/*/worker/*/ agent/*/conductor/* branches (cost-saving), so visual verification for agent-authored branches has to happen post-merge against the production deployment, not via a pre-merge Vercel preview -- AGENTS.md's documented preview technique (~L338-366) doesn't currently note this exception.

- 2026-08-01 `interface-vision/t-013` — Before touching a large "un-nest this component" task, trace the actual mount path first -- conductor-page.vue's own 'overview' and 'brainstorm' viewMode branches, plus a chunk of its cockpit bar, were structurally unreachable because conductor-manager.vue (its sole importer) intercepts those workspaceCardKey values and renders a different component before ConductorPage ever mounts. A component can look nested/cluttered while actually being half dead code wearing live-code's clothes; grep for the component's importers and read the routing logic one level up before assuming every rendered-looking branch is reachable. Separately: when a task names multiple target files, verify each one's claim independently rather than assuming a shared premise -- art-manager.vue's "tabs are themselves dashboards" claim didn't hold on inspection even though the conductor-page.vue and user-manager.vue claims in the same task note did.

- 2026-08-01 `interface-vision/t-011` — A roadmap task note's factual claims about the codebase ("X is the most complete widget", "Y is imported by nothing") are a snapshot from planning time, not a live fact -- t-007 and t-009 both merged the same day this task's note was written, and by the time t-011 was picked up the note's premise (revive art-reactions.vue as canonical) was already stale: reaction-card.vue had already superseded it as the generic, actively-wired review panel. Read the current state of every file a note names before trusting its characterization, and when the literal instruction conflicts with what the code now shows, do the thing that closes the real gap (here: allowReviews was read by no gallery, not "no canonical panel exists") and document the deviation explicitly rather than either blindly following a stale instruction or silently reinterpreting it.

- 2026-08-01 `interface-vision/t-009` — Clean first pass (kind_robots PR #1269, all 14 CI checks green), but the task as originally scoped ("collapse three art-request pipelines into one") bundled a small, well-verified mechanical slice (repoint Project's art-replace onto the already-existing generic entity-art endpoint, delete two confirmed-dead routes, widen one component's type union) together with four genuinely separate decisions (a UX choice on Project's carousel UI, a product choice on Facet's dual art backends, a multi-entity schema migration, and a from-scratch admin UI) that each need their own PR and, in two cases, Silas's input before implementation. Investigating the actual code before implementing (rather than trusting the task note's characterization) also surfaced that one of the note's own technical claims was wrong: FacetArtImage was described as "declared-but-unused" but is live code serving a different purpose (ArtImage-to-Facet tagging, not a Facet art-history join) -- corrected in the split-out follow-up task (t-028) rather than propagated blind. Standing takeaway: a roadmap task note's own technical claims are a starting hypothesis, not verified fact, even when written carefully -- worth a quick repo-side confirmation pass before scoping work against a claim like "X is unused" or "Y already exists," especially when the note is old enough that the codebase could have moved under it.

- 2026-08-01 `interface-vision/t-006` — Clean first pass (kind_robots PR #1267), but the close-out step surfaced a real tooling gap this session had to work around by hand: claim_task.py pushed its claim commit straight to origin/main, and this session's local checkout was never re-fetched before set_task_field.py edited the roadmap to status: review -- set_task_field.py operates on whatever is in the local tree with no fetch of its own (its own docstring names this exact gotcha, conductor/t-077/davinci/t-014), so the resulting commit briefly clobbered the claim commit's owner/claimed_by/claimed_at fields on this session's branch. Caught before it reached main only because rebasing onto origin/main before opening this task's own conductor PR produced a merge conflict on the exact block claim_task.py had written -- resolved by keeping origin/main's claim metadata and folding in the intended status transition. Standing takeaway: after any claim_task.py call (or any other script documented to push straight to origin/main), fetch and fast-forward the local checkout before running set_task_field.py against the same file in the same session, not just before the final close-out push.


---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-02T05:05:00Z_
