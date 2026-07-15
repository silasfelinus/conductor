# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-15T07:14:37Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **54**
- Outcomes: done: 54
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
| conductor | 9 | 100% |
| digital-storefront | 3 | 100% |
| ecosystem-map | 2 | 100% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 1 | 100% |
| kind-robots | 2 | 100% |
| model-builder | 13 | 100% |
| newsfeed | 1 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 3 | 100% |
| software | 51 | 100% |

## Failure categories

| Category | Count |
|---|---|
| actionable | 2 |
| quality | 2 |

## Kaizen targets

_No systematic weaknesses above thresholds. Kaizen freely._

## Recent lessons

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
- 2026-07-15 `challenge-center/t-021` — nodejs.org's own dist host is reachable through the sandbox proxy even
though deb.nodesource.com and CI's Azure Blob artifact redirects are not --
scripts/provision_node24.sh fetches a pinned Node 24.x tarball directly from
there instead of relying on nvm/fnm (not preinstalled, no durable cross-session
install path since every hourly session is a fresh container). Source it before
any future kind_robots CI reproduction rather than re-deriving the workaround.
- 2026-07-14 `challenge-center/t-020` — A cherry-pick onto the real live claim commit (status/owner/claimed_by/claimed_at) surfaced
the exact failure mode this task fixes -- resolving it was three surgical field re-applies
via set_task_field.py/roadmap_text_patch.py instead of a full-file merge conflict, which is
itself a live demonstration that the patcher works. Also: when a task's 'learning' payload
needs validating, do it BEFORE any roadmap write so an invalid payload can't strand an
already-applied, now-unrepeatable transition with its event file undeleted.
- 2026-07-14 `challenge-center/t-019` — A roadmap task's description of current state can be stale even when the task itself is legitimate -- verify against the live repo (both the target page/component AND the specific config structure the task names, e.g. 'tutorialChannels.wonder.sections') before writing code, since a task written when a feature was a placeholder may find that feature already complete by the time it's picked up, and a task assuming a config key exists may find it doesn't. Also: when the standard art-generation queue (art-prompts.yaml) isn't executable in a sandboxed session, reusing already-approved project art at matching dimensions (rather than leaving a queued-and-blocked placeholder) is a legitimate terminal action if the provenance is documented -- but this doesn't replace the queue for cases needing genuinely new art. Also: local CI reproduction can drift from the real thing in more than one way at once (Node major version AND a newly-added `prisma generate` pre-step) -- when an exact error-count match isn't achievable, the decisive check is file-isolation (does any local variant, however imperfect, ever put an error in the PR's actual changed files), not chasing a byte-exact reproduction.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-15T07:14:37Z_
