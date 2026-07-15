# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-15T04:54:24Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **50**
- Outcomes: done: 50
- Success rate: **100%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 1 | 100% |
| alexa-integration | 1 | 100% |
| animation-manager | 4 | 100% |
| animation-studio | 1 | 100% |
| challenge-center | 12 | 100% |
| coloring-book | 1 | 100% |
| conductor | 9 | 100% |
| digital-storefront | 1 | 100% |
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
| software | 47 | 100% |

## Failure categories

| Category | Count |
|---|---|
| actionable | 2 |
| quality | 2 |

## Kaizen targets

_No systematic weaknesses above thresholds. Kaizen freely._

## Recent lessons

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
- 2026-07-14 `challenge-center/t-018` — Before writing new validation logic for a 'add a CI check' kaizen task, check whether the target scripts already validate and just need wiring into CI -- scripts/seed_challenges.ts and scripts/seed_contenders.ts already had dry-run validation gated behind a --write flag from the task that originally created them (t-004), so the actual work was a 2-line CI step, not new code. Also: verify the negative case, not just the happy path -- fed validateChallengeSeeds a deliberately broken (duplicate-slug) catalog to confirm the new CI step actually fails on bad input, since a check that only ever passes is a false-confidence trap. Two more unrelated CI checks (Channel content contract, TypeScript) were red on this PR independent of its two-file diff; filed kind-robots/t-021 for the newly-observed one alongside the already-tracked t-020, following the established pattern of turning a stray red check into a trackable roadmap task rather than a one-off PR comment.
- 2026-07-14 `challenge-center/t-015` — A red CI TypeScript check on a PR that touches unrelated files should be reproduced in the exact CI environment (matching Node major version via a fresh local install + npm ci), not just re-run under whatever Node happens to be in the sandbox -- confirming byte-identical file:line errors against a known pre-existing tracked issue (kind-robots/t-020) is what actually justifies merging past a red check, not an assumption that it 'must be the same one as last time.'
- 2026-07-14 `coloring-book/t-019` — The task's own framing ('evolve the placeholder scaffold page') was stale -- a repo read of kind_robots showed the coloring engine (store/canvas/manager) is already a functionally complete region+raster-flood-fill implementation with undo and export, not a placeholder. Read the target repo before trusting a roadmap task's characterization of current state; the actual thin spots (generic Generate/Proposals/Prompts sub-tabs, single hardcoded page set) were narrower than the task description implied and got split into a new focused task (t-020) instead of driving an oversized diff. Also: art-asset generation for dashboard-tab/tutorial thumbnails is a queue-and-wait step (projects/art-prompts.yaml requests:), not something a single session executes end-to-end without KR_API_TOKEN -- queuing the request IS the correct terminal action for that sub-step, not a soft-gate blocker.
- 2026-07-14 `ai-art-academy/t-012` — A 'confirm the resolver has no type-specific branching' task closed clean on first pass by reading satisfied() directly (scripts/resolve_deps.py) -- it only checks status/gate_human/approved_by_human, never task kind, so a licensing DECISION and a brief-confirmation gate were already handled identically. Backed the finding with tests/test_resolve_deps.py (12 tests, zero prior coverage) instead of a note-only close, so the guarantee is now regression-tested rather than asserted. Also picked up mid-cycle after a real rotation collision on challenge-center/t-013 -- claim_task.py's live origin/main check caught it before any duplicate work was pushed.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-15T04:54:24Z_
