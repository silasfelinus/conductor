# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-05T22:53:39Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **528**
- Outcomes: blocked: 13, cancelled: 1, done: 514
- Success rate: **97%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 60 | 98% |
| alexa-integration | 2 | 100% |
| animation-manager | 13 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 6 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 25 | 100% |
| conductor | 66 | 100% |
| conductor-app | 2 | 100% |
| davinci | 2 | 100% |
| digital-storefront | 25 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 4 | 100% |
| interface-vision | 70 | 100% |
| kind-robots | 42 | 98% |
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
| software | 513 | 99% |

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

- 2026-08-05 `ai-art-academy/t-055` — The task's own claim had gone stale for ~8h with no PR ever opened (found via check_pr_merged_drift.py, unrelated to this task's content) -- a session should treat a claimed-but-un-PR'd task surfaced by that sweep as reclaimable once past CLAIM_TTL_MINUTES rather than assuming it's still in flight. Also: art-prompts.yaml alone is not a reliable coverage signal for delivered assets since fulfilled entries get pruned -- a live delivery check is required to tell "already fine" from "needs a request," which is why verify_academy_style_preview_coverage.py checks live by default.
- 2026-08-05 `conductor/t-101` — Before implementing a kaizen task, re-verify its premise against current code -- validate_task_events.py already had the exact check this task asked for (since PR #851, 2026-07-19), so the real remaining work was narrower (test coverage) plus a root-cause finding (task-events written by direct push to main never hit the PR-time gate at all) that the original task note didn't anticipate.
- 2026-08-05 `kind-robots/t-051` — A shallow kind_robots clone's default commit horizon can be too short to find a file's add/remove history even a few weeks back on a very active repo -- git fetch --unshallow before concluding a path was "never added" or "vanished without a trace" (same trap already documented for branch_janitor.py's merge-base classification).
- 2026-08-05 `kind-robots/t-054` — Branch cleanup must use full history for reliable merge-base classification; stale unmerged branches remain review-only so automation cannot erase unique work.
- 2026-08-05 `conductor/t-082` — A standalone FOR-SILAS confirmation task with no dependents and no gate_human/approved_by_human requirement can be closed straight from a "SENT BACK ... confirmed" Kind Robots For You note once the task's own closing instruction says so explicitly -- unlike a gate_human task, there is no ambiguity to preserve for Silas here.
- 2026-08-05 `ai-art-academy/t-056` — A kaizen note asking for a field that doesn't exist in the source data (here: "region") is worth implementing as closely as the real schema allows rather than skipping outright -- era-based sort/overlap-detection delivered the same practical benefit (spotting a coverage gap before adding a new curriculum entry) using only fields that actually exist.
- 2026-08-05 `ai-art-academy/t-043` — Keep curriculum inclusion, reproduction rights, and generation-preset permissions as separate policy questions. Collapsing them into one death-date cutoff can erase historically important artists while still failing to express the actual copyright and commercial-use constraints.
- 2026-08-05 `conductor/t-099` — Adding a "strongest evidence" field/tier to a multi-pass classifier isn't complete until the code path that decides "does this field apply" also distinguishes absent-and-should-fall-back from present-but-corrupt-and-should-not. A single parse_x() -> Optional[T] helper collapses both into None, which reads fine until a caller uses "is None" as the fallback trigger -- a malformed value then silently gets treated as if the stronger evidence were never there at all, quietly replaced by a weaker heuristic instead of surfacing. Caught by external review before merge (PR #1737) rather than by the implementing session's own test pass, since the tests written alongside the feature covered field-present/field-absent but not field-present-but-malformed -- a reminder to enumerate all three states explicitly whenever a field is optional AND has a shape to validate, not just "present vs. absent."
- 2026-08-05 `conductor/t-099` — A dedicated implementation_pr field, written once at close time, is strictly stronger evidence than any post-hoc heuristic (title search or note-quoted PR reference) for reconciling roadmap state against reality -- it's self-reported by the session that actually did the work, immune to title-convention drift, and free to check (one direct PR lookup vs. a search). The one sharp edge worth remembering: a field that is present-but-malformed is not the same case as a field that is absent -- both `parse` to None, but conflating them lets corrupted roadmap data silently fall back to weaker search/note evidence and report a false "clean" instead of surfacing as unresolved. Route "truthy but unparseable" to unresolved explicitly, never through the same branch as "falsy/missing".
- 2026-08-05 `conductor/t-098` — A note-quoted PR reference cannot distinguish a task's implementing PR from the PR whose kaizen suggestion filed the task -- both are quoted the same way in prose. A much stronger signal, and one that's basically free once the convention holds, is searching for a merged PR whose own TITLE names "<project>/<task-id>" (the convention close-out PRs already follow in practice). Prefer that self-reported, task-authored signal over parsing free-text notes whenever a tool needs to associate a task with "the PR that actually did this," and treat any weaker/inferred signal (like a note reference) as advisory, not proof, in the tool's own output.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-05T22:53:39Z_
