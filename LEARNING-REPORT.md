# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-15T10:16:24Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **57**
- Outcomes: done: 57
- Success rate: **100%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 2 | 100% |
| alexa-integration | 2 | 100% |
| animation-manager | 4 | 100% |
| animation-studio | 1 | 100% |
| challenge-center | 12 | 100% |
| coloring-book | 1 | 100% |
| conductor | 10 | 100% |
| digital-storefront | 3 | 100% |
| ecosystem-map | 2 | 100% |
| global-ui | 1 | 100% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 1 | 100% |
| kind-robots | 2 | 100% |
| kindrobots-unraid | 1 | 100% |
| model-builder | 13 | 100% |
| newsfeed | 1 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 3 | 100% |
| software | 54 | 100% |

## Failure categories

| Category | Count |
|---|---|
| actionable | 2 |
| quality | 2 |

## Kaizen targets

_No systematic weaknesses above thresholds. Kaizen freely._

## Recent lessons

- 2026-07-15 `global-ui/t-005` — A "produce the final map/spec" task pays off most when it re-verifies against the real implementation instead of re-printing the original design doc — t-005 found three real navigation gaps (honeydo has no top-level nav entry, no completed-task collapse, unconfirmed site-audit trigger) that a spec-only summary would have missed entirely. Filing gaps as new tasks rather than expanding the mapping task kept it a clean single-pass merge.

- 2026-07-15 `kindrobots-unraid/t-005` — Cross-repo tasks that finish with the real patch merged in the target repo and only conductor-side bookkeeping left in the conductor PR are safe to review purely on the target-repo diff + roadmap note; no need to re-derive the implementation review in conductor. Watch for merge-base drift on such bookkeeping PRs — a chore auto-commit landing on main between claim and PR open guarantees a STATUS.md conflict (see conductor/t-045).

- 2026-07-15 `conductor/t-044` — Task notes that embed example values (channelKey/tabKey) from the task that spawned them should be cross-checked against the actual target project's source, not copied verbatim — packmaker/mermaids each needed their own real tabKey looked up in projectPlacements.ts.
- 2026-07-15 `digital-storefront/t-016` — A design doc that just describes the happy path misses the actual blocker. Checking the schema directly (Resource had no license/commercial-safety field) surfaced a real gap between CONTROL.md's commercial-generation licensing rule and what the data model can currently enforce — worth grepping the shared schema for the field a design assumes exists before writing the doc as if it does, especially for anything touching monetization or generated-art rights.

- 2026-07-15 `digital-storefront/t-019` — A "confirmed blocked" TALKBACK note can go stale silently across sessions. Re-verifying with a fresh, timestamped curl/proxy-status check (rather than inheriting a prior session's claim) took under a minute and let every downstream task cite a concrete recheck timestamp instead of an aging assumption — cheap insurance against a blocker that's actually since cleared.

- 2026-07-15 `ai-art-academy/t-010` — A PR's CI failure isn't necessarily caused by the PR: before treating a red check as a blocker, diff it against the same check's result on main at the PR's base commit (list_workflow_runs filtered to that branch/sha). Here kind_robots' TypeScript check was already failing on main (kind-robots/t-020's 82-error backlog) before this PR existed; a local vue-tsc run confirming zero new errors in the changed files, plus a PR comment citing the base-commit failure, was enough to merge safely instead of stalling on an unrelated, already-tracked issue.

- 2026-07-15 `alexa-integration/t-008` — A ready task blocked only by a prior connector branch-write limitation (not a design question) is a great pick for any burst session that already has direct repo access — the preserved handoff doc in projects/<name>/docs/ applied almost verbatim. One gotcha: preserved patches can go stale against routing/dispatch logic that evolved after they were written even when the target module's own contract didn't change (here, t-013's control-adapter theme detection started swallowing the patch's own test phrase). Re-verify preserved fixtures against current routing before assuming they still round-trip; filed t-016 to fix the over-claiming root cause.

- 2026-07-15 `digital-storefront/t-015` — Genuinely research-only tasks (no cross-repo code, no external API dependency) are the right thing to rotate to when the priority-ordered project and even the current project's own top tasks are blocked by sandbox egress denial (api.stripe.com, museum sites) — confirmed the denials still applied this session before rotating rather than assuming a stale note. Recommendation (Printful, sticker first) was backed with live 2026 web research rather than reused verbatim from the older research/stores.md shortlist.

- 2026-07-15 `humboldt-scoop-cms/t-011` — Fourth confirmed instance of the "Polish and upgrade X front-end surface" stale-tutorialChannels-nesting pattern (after mural, challenges, humboldt-scoop). conductor/t-044 tracks the note-text fix for the two remaining ready instances (packmaker/t-006, mermaids-of-venice/t-012) — whoever picks those up should apply the same top-level-channel convention directly rather than re-deriving it. Also reused an existing approved project hero image for dashboard-tab/tutorial art in place of live generation (no KR_API_TOKEN this session), matching the humboldt-scoop/t-008 precedent — worth keeping as the standard fallback whenever a project already has an approved hero at matching dimensions.

- 2026-07-15 `humboldt-scoop/t-008` — The "Polish and upgrade X front-end surface" task template's note text
describes tutorial-channel wiring as a nested section under
tutorialChannels.<dashboard-tab-group>.sections, but the actual convention
(confirmed against tutorialCards.ts across 3 completed instances now) is a new
top-level ExtraTutorialKey channel keyed by the project's own tab key. Filed
conductor/t-044 to fix the note text on the remaining instances before they
hit the same stale-path confusion.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-15T10:16:24Z_
