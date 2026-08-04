# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-04T22:27:23Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **512**
- Outcomes: blocked: 13, cancelled: 1, done: 498
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
| conductor | 61 | 100% |
| conductor-app | 2 | 100% |
| davinci | 2 | 100% |
| digital-storefront | 24 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 4 | 100% |
| interface-vision | 68 | 100% |
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
| software | 497 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 9 |
| actionable | 9 |
| transient | 8 |
| scope | 2 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `quality` — 9 occurrences; look for the shared cause across its records
- failure category `actionable` — 9 occurrences; look for the shared cause across its records
- failure category `transient` — 8 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-04 `interface-vision/t-086` — Multi-stage media fallback state must identify which candidate failed. A single failed boolean can represent one transition but cannot safely drive a chain with two or more candidates.
- 2026-08-04 `interface-vision/t-094` — Applied verifyLayoutContract.ts's existing baseline/ratchet pattern to a second contract check (auditWonderLabPreviews.ts) with an almost line-for-line-identical shape: allow-list of known-bad entries in a JSON file, --strict fails only on entries not in the allow-list, --update ratchets the baseline down and refuses to grow it. kind_robots PR #1434, merge 41b334248747da904c92245d7fabc9f1abca3f7e. Verified the negative case explicitly (injected a synthetic new required-prop component with no fixture, confirmed --strict flagged only the new one and not the pre-existing 29) rather than just the positive case -- worth doing for any future ratchet-pattern port, since a baseline that silently allow-lists everything (e.g. from a coding mistake) looks identical to a correct one on the happy path alone.
- 2026-08-04 `interface-vision/t-082` — A prior connector-only session released this task ("connector patch limitation" -- could not safely patch a 500+ line file, and had no local git/DNS). A session with full shell/git access hit no such limitation: mirrored add-reward.vue's Publishing section (isPublic/isMature toggles, t-080) onto add-scenario.vue verbatim, no store changes needed since scenarioStore already round-trips both fields. kind_robots PR #1433, merge 82f61b1e5d3ed5d0e992ecf76ab5fa1beb5aa501. Lesson: a connector-limited session's "actionable" release reason should be read literally -- it is a tooling gap for that session, not evidence the task itself is hard, so a shell-capable session should retry it directly rather than assuming the release implies deeper difficulty.
- 2026-08-04 `interface-vision/t-060` — Completed the final three reachable core-gallery migrations (character, reward, dream) and closed the measured 7/7 core-object beta gate without forcing row or dropdown variants into a shared grid abstraction. kind_robots PR #1418, merge 6b541a3ed4c65570659c37aed9d7748fb087d734.
- 2026-08-04 `conductor/t-097` — task-events/README.md documents a direct push to main as the normal workflow, so validate_task_events.py's PR-time gate never runs for the common case -- a malformed bare-string learning: field (the "learning: >-" folded scalar shape) recurred at least 5 times in a week and each time hard-failed process_task_events.py, silently red-flagging the shared "process" check for every unrelated PR. Coercing the string into {kind, stakes, lesson} (inferring kind/stakes from the task's own roadmap entry) instead of hard-rejecting it keeps the processor unblocked without losing the lesson text -- worth considering the same "recover gracefully from a common malformed shape" pattern for other task-events fields prone to hand-authoring mistakes.
- 2026-08-04 `interface-vision/t-089` — A plain "who imports this .vue file" grep at deletion time is not enough -- kind_robots PR #1405's conductor-art-gallery.vue deletion (t-026) missed a plugin that DOM-scraped the component's specific rendered markup and a CI workflow that named the file directly in its paths: trigger list. Documented the checklist in kind_robots' AGENTS.md (PR #1417): grep the deleted filename repo-wide (not just import sites), check .github/workflows/*.yml paths: blocks, and check plugins/*.client.ts for DOM-scraping selector strings before deleting a superseded component.
- 2026-08-04 `interface-vision/t-088` — The last of the three Phase 5 conversation-kit migrations (character-interact #1400, reward-interact t-087/#1406, scenario-interact t-088/#1408) was flagged in its own task note as "not a mechanical swap" -- it had two distinct duplications (a chat transcript and a separate intro-picker reusing the deleted choice-selector.vue's job), and the intro picker's long-paragraph hint text needed a non-italic kr-choice-list variant that didn't exist yet. Adding an opt-in `hintProse` prop (default false, every existing caller unaffected) was cheaper than a bespoke non-italic wrapper and kept the shared component as the single source of truth. Second occurrence of the same "lost the highlighted last-pick styling" gap reward-interact/t-087 hit -- two real surfaces is the signal to actually file the kr-chat-window selectedKey pass-through as a task (t-090) instead of deferring a third time.
- 2026-08-04 `interface-vision/t-087` — A prior PR (character-interact.vue, #1400) landing the exact same migration pattern (bespoke chat log -> kr-chat-window + kr-choice-list) turned this 1183-line surface into a same-session close rather than a design exploration -- read the reference implementation in full before starting, not just its diff summary. The one real design decision was mapping a caller's existing choice data onto kr-choice-list's fixed embedded contract: kr-chat-window hardcodes its per-turn choice list to layout="row" with no index badge, so a caller with long descriptive choice text (not short quick-topics) has to decide which of label/hint carries the short vs. long half -- picked short category as label, full text as hint, to keep the inline row pills compact. A second non-obvious win from adopting the shared kit: kr-chat-window's built-in streaming placeholder made a "keep it hidden until the request resolves, then push a finished turn" simplification natural, which incidentally fixed nothing broken but removed real state (a scroll ref, three call sites, a manual watcher) that existed only to fight the layout the bespoke markup created in the first place -- duplication removal often deletes more state than template.
- 2026-08-04 `interface-vision/t-026` — Deleting a bespoke duplicate component in favor of a shared canonical one (Silas's "one source ... kill the others" pick, resolving an A/B mockup) needs a full-repo grep for the deleted file's name, not just its obvious call site. Two silent-breakage risks turned up that a component-only diff would have missed: a DOM-scraping client plugin (project-art-prompt-suggest.client.ts) that keyed its button-injection logic on the deleted component's specific textarea maxlength and a <code> element it rendered -- fixed by gating on the shared component's entityType prop instead of brittle per-entity DOM shape -- and a GitHub Actions workflow (entity-art-manager-contract.yml) whose trigger `paths:` list still named the deleted file, caught by CI's verifyWorkflowPaths.ts after merge-adjacent push rather than before. Also worth noting: placing a new UI panel *before* an existing one in a component's template silently changes which element a `querySelector('img')`-style DOM heuristic elsewhere in the codebase picks up first -- moved the new panel after the existing one specifically to keep that heuristic pointed at the right image.
- 2026-08-04 `interface-vision/t-076` — A "needs a real design decision" task with two named options (rewrite the broken component, or swap in an already-correct one) resolved fast once the already-correct option's actual prop contract was read in full: character-card.vue already did everything option (a) would have had to build (a real character prop, no side-effecting store init, grid-proven usage), so option (b) collapsed to a small, mechanical swap. The type system caught a real latent gap the swap needed to resolve (a curated Pick<Character,...> relation missing two fields the target component's full prop type required) -- something the previous component's total absence of prop typing had let go unnoticed indefinitely. When a task's own note offers "use an existing correct component instead" as an option, read that component's actual prop surface before assuming a rewrite is the only path -- the smaller fix is often already built.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-04T22:27:23Z_
