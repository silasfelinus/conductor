# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-24T06:48:56Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **741**
- Outcomes: blocked: 15, cancelled: 1, done: 725
- Success rate: **98%**
- Average passes on successful tasks: **0.2**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 70 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 13 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 9 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| brainstorm | 24 | 96% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 25 | 100% |
| conductor | 79 | 100% |
| conductor-app | 4 | 100% |
| davinci | 7 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 83 | 100% |
| kapowarr | 48 | 100% |
| kind-economy | 6 | 100% |
| kind-robots | 50 | 98% |
| kindrobots-unraid | 5 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 79 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 16 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 6 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 16 | 44% |
| software | 725 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 14 |
| actionable | 10 |
| transient | 9 |
| scope | 2 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 14 occurrences; look for the shared cause across its records
- failure category `actionable` — 10 occurrences; look for the shared cause across its records
- failure category `transient` — 9 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-24 `storybook/t-023` — Task scope (audit taskmasterStore's localStorage read path against storybookStore's restore guards) required tracing every real caller before deciding whether the missing `restoredFromStorage`-style guard was a bug: content/taskmaster.md mounts `:taskmaster-page` as the only call site, with no wrapper double-mounting it the way storybook-library-page.vue wraps StorybookPage, so no reachable race exists and the guard was correctly out of scope -- the parity gap alone was not sufficient, matching the cycle-36 lesson this task was scoped from. Fixed the unambiguous half (move `getItem()` inside the try) and left the caller-tracing result as an in-code comment. Also worth recording: a full-file `prettier --write` on a file with pre-existing prettier-version drift silently reformats unrelated lines far beyond the actual diff -- caught via `git diff --stat` before committing; the safe pattern is formatting only the new/changed region and verifying it in isolation, never running `--write` on the whole file when the rest carries known drift. Separately, this cycle hit a second occurrence of the documented conductor/t-124 "Python test suite" check-run reporting-lag pattern (job logs showed it passed and finished cleanup ~11 minutes before the check-run API reported completion) -- confirmed via job logs rather than assumed, and merged once confirmed rather than re-running blind.

- 2026-08-24 `brainstorm/t-026` — Task scope was explicitly conditional ("find, or confirm there isn't yet, a promote-candidate action, and IF one exists, wire the art across") -- a repo-wide search (candidate card's emitted events, the manager's kept-candidate bulk actions, server/api/brainstorm/, and a grep for promote/convert/"turn into"/createFrom) confirmed no such action exists anywhere. The honest close for a conditional investigation task with a negative finding is `done`, not a forced implementation and not `needs-human` -- the literal scope asked a yes/no question and got a firm no. Filed the actual feature (t-031) as new scope instead of expanding this task's diff, since building an unrequested promotion UI would have been scope creep past what t-026 asked for. Also worth recording for whoever picks up t-031: entityArt.ts's art-slot model is one scalar id per named slot per entity, while Brainstorm's meta.art.imageIds is an array -- there is no existing 1:1 precedent in the repo (promptStore.promoteToDream's Prompt only ever has one artImageId) for the many-to-one reduction that promotion will need.

- 2026-08-24 `storybook/t-010` — Cycle 36: after five consecutive cycles that either found a shrinking-returns polish item or no-op'd, the fresh angle that produced a real correctness bug was the one the PREVIOUS cycle had already written down and not taken -- "Pinia persistence edge cases have not had a dedicated pass in this task's history." The bug was a sibling-parity gap of exactly the shape a shared-helper family invites: taskmasterStore.ts's saveToLocalStorage() was the one localStorage writer of four in the narrative family with no try/catch, while its three siblings each carried an explicit private-browsing/quota comment explaining why they had one. Two lessons. First, a recurring bug-hunt task's own "next lead" note is a real work queue, not a formality -- reading it before inventing a new lens is cheaper than re-deriving one, and a lead that survives a cycle unclaimed is more likely to be untouched ground than a lens the task has already swept. Second, and the inverse of cycle 61's model-builder lesson: a found inconsistency IS a fixable sibling-parity bug when the two sides are genuinely the same kind of moment, and here the codebase said so itself -- the shared helper's own header asserted the two stores were "byte-for-byte the same shape," so the asymmetry was a documented invariant being violated rather than a pattern-match on surface similarity. Confirming the impact still required tracing all ten call sites individually: the sharpest one (updateBeatArt() running as an uncaught `void poll(...)` callback, where a throw both became an unhandled rejection and killed the art poll loop, stranding the illustration with no retry affordance) was not the one the shape of the bug suggested up front. Finally: when a fix restores an invariant a contract script already claims to enforce, extend that script -- and verify the new assertion fails against the pre-fix code, or it may be vacuously true.

- 2026-08-24 `kapowarr/t-068` — Rendering in batches is not enough if the browser is still instructed to consume every batch immediately. For large galleries, cap total off-screen DOM work to a viewport runway and let user movement demand the next chunk; otherwise background batching merely turns one long freeze into sustained jank, especially on setTimeout-based fallbacks.
- 2026-08-23 `model-builder/t-029` — Cycle 61: with no new kind_robots commits touching model-builder since cycle 59 and the repo-wide reference grep turning up no unaudited file, took the task brief's own "accessibility gaps" lens explicitly for the first time in this task's 61-cycle history. Found a real-looking sibling inconsistency (two components wrap their loading state in role="status"/aria-live="polite"/aria-busy="true", two others' analogous spinners have neither) but tracing it further showed the two pairs aren't actually comparable: the guarded pair is a full-region "loading this list from the network at mount" state, the unguarded pair is a button-internal in-flight spinner -- a state shape that is uniformly unguarded across every button in this component family, not selectively skipped on two components. Lesson: a found inconsistency is only a fixable sibling-parity bug if the two sides are actually the same kind of moment -- pattern-matching on "this attribute is present here and absent there" needs a check that the "there" is truly analogous to "here," or the fix ends up either wrong-shaped (fixing the wrong two files) or scope-creeping into a repo-wide convention decision that a single-bug-per-cycle task isn't set up to make well.

- 2026-08-23 `brainstorm/t-029` — Third clean first-pass adapter/CTA task in a row (t-027 Scenario, t-028 Reward, t-029 Bot) following the same BrainstormSourceAdapter registry + gated startBrainstormWith*() CTA + verifyBrainstormObjectEntryLinks.mjs assertion pattern -- confirms this is now a well-worn, low-risk template for onboarding a new source entity, not something that needs fresh design judgment each time. When a recurring kaizen note explicitly names the next entity to follow the same pattern (here: Project, per t-027's original note), treat that as a ready-made task rather than re-deriving scope from scratch.
- 2026-08-23 `davinci/t-025` — Before scoping a 'extract the shared pattern between these two call sites' refactor, grep the WHOLE repo for the symbol being extracted, not just the two sites already named in the task note -- a third, byte-for-byte identical call site (taskmasterStore.ts) existed and was missed by hand-picking files instead of searching, only caught because a repo-owned contract test (verifyNarrativeArtPersistence.mjs) enforced the two stores stay in lockstep and failed CI. Also: running `prettier --write` on a whole pre-existing file to fix one targeted edit's formatting can reformat large unrelated regions if the file was already prettier-noncompliant before the change (confirmed via git stash/checkout) -- restore the pristine file and apply only the intended edit via a scoped replace, never a full-file --write, when touching a file the task doesn't already fully own.
- 2026-08-23 `brainstorm/t-028` — Following an already-established adapter pattern (Character/Scenario) end to end -- registry entry, gated CTA, contract-script assertion, workflow path trigger -- landed clean first pass with zero findings; the pattern itself, not novel judgment, was the main risk-reducer.
- 2026-08-23 `model-builder/t-029` — Cycle 57's fix covered three places that swap state.run for a different run (goToStep /selectSource, openRun's two branches, resumeRun's branch) without clearing the in-flight singletons resetRun/resetAll already clear -- but only checked whether each call site clears the singletons, not whether the RESPONSE feeding that call site could itself be stale. resumeRun() has exactly one call site (a component's onMounted) yet was still racy, because unmounting a Vue component does not cancel its in-flight promises: navigating away and back before a slow resumeRun() resolves creates a second concurrent call against the same Pinia singleton, and the older call's stale response can land after the newer one already resolved and the user moved on. Lesson for future cycles: "this function's call site is singular / not button-driven" is not the same guarantee as "this function cannot run twice concurrently" -- component remounts (navigation, not just explicit user clicks) are a second, easy-to-miss source of concurrent async calls against a shared store, and any async chain writing shared state on completion needs a request-ticket guard regardless of how simple its trigger looks.

- 2026-08-23 `conductor/t-123` — Kaizen from an earlier same-day session's mermaids-of-venice/t-013 wasted claim (conductor#2720). Added scripts/daily_gate.py, detecting a task whose note declares an explicit "Pacific calendar day" daily-gate contract and already records an outcome for today's Pacific date, and wired the skip into both task-selection paths -- next_ready_task.py's first_ready_task AND run_worker.py's find_ready_task. The second wiring mattered most: select_role.py's underlying "worker" recommendation (the path that actually surfaced the stale t-013 pick in the first place) calls build_queue_summary() -> find_ready_task(), not next_ready_task.py -- a fix scoped only to the connector-only picker would have left the real collision path unpatched. Lesson: when a kaizen task names "the sweep step" as the target, check which of the repo's (sometimes more than one) selection implementations that step actually calls before assuming a single shared module covers it.


---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-24T06:48:56Z_
