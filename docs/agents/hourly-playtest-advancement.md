# Hourly playtest advancement (Claude scheduled session)

**Cadence:** once per hour in the external Claude task scheduler. This file describes the work; it does **not** create a second GitHub Actions cron or authorize API-credit spend.

**Objective:** ship one substantial, independently useful increment per run that moves a **high-priority, active Kind Robots game** toward a verified `playtest` handoff. Optimize for *more games reaching playtest*, not activity reports, roadmap churn, or endless polishing of the same game.

## Start of each run

1. Follow `AGENTS.md`, `CONTROL.md`, `project-overrides.yaml`, `projects/priority.yaml`, and the selected game's roadmap and master GitHub issue. Honor explicit human direction and the claim/PR/CI/human-gate protocols. The current project state in Conductor is authoritative.
2. Use `python scripts/project_triage.py --json` (or the same evidence via GitHub if connector-only) to identify **active** games whose project override has `priority: high`. Exclude `playtest`, `continuous`, `paused`, `retired`, `finished`, member projects, non-games and already-claimed tasks. Do not accidentally abandon Silas's protected creative priorities.
3. Prefer an unblocked game **closest to playtest** (tier A, then B, then C), weighted by whether this session can truly clear its last art, narrative, QA, or integration blocker. When similar, use `projects/priority.yaml` and latest `CONTROL.md` direction. Rotate among games rather than repeatedly choosing familiar work. Review existing code/PRs/branches before duplicating implementation. A missing human decision is not a reason to stop improvements on another game.

## Ship something real

Claim one eligible task with a unique session and work within that scope. Prioritize, in order of *what is actually missing*:

- **Build/story:** finish gameplay loops, real choices, endings, save/resume, state transitions, and project-specific scope. Revise weak first-draft prose; a task titled `done` does not substitute for complete authored routes.
- **Art:** queue, render, deliver, select, and wire actual assets with provenance. Merely writing prompts or counting pending ArtJobs does not prove art completion. If rendering is pending, ship another independently useful unblocked improvement.
- **Verification:** deterministic and adversarial full-path playthroughs, failure/recovery tests, usable controls, phone/tablet/desktop art-first presentation, and evidence-backed bug fixes. Check real gameplay rather than a smoke test alone.
- **Closeout:** reconcile merged PRs and roadmap state; test and merge safe reversible work **only after CI checks actually finish green**. Keep gated/public/publishing changes unmerged.

A run must produce a concrete, reviewable result: tested code merged to main, delivered assets, completed story content, verified QA with real findings or a justified readiness transition. If a chosen task is blocked or already claimed, pick the next candidate. Do not mark an unfinished production task `playtest_iteration` or hide missing work behind a human gate.

## Graduation: high-priority active → playtest/medium

A game graduates **only when** `scripts/playtest_readiness.py`'s finite-task gate passes **and** the real game has all planned authored art/text available, full gameplay/endings and saved progress usable, build and QA evidence, complete playthrough/adversarial tests, and a legible front end. Confirm the goal against the actual app, not only a checkbox count.

1. In the roadmap, leave a genuine final `gate_human: true`, `gate_reason: subjective-acceptance` (or `creative-approval`) task at `status: needs-human`, **unapproved**, with a concise `FOR SILAS` handoff: where to play, what is ready, what to evaluate, what is intentionally not approved, and any known limits. Never set `approved_by_human: true`.
2. In **Conductor** `project-overrides.yaml`, set `status: playtest` and **`priority: normal`**, the existing middle/medium priority value (the schema uses `high | normal | low`, not `medium`). Do not modify Kind Robots' projected coordination fields directly.
3. Let `.github/workflows/sync-playtest-master-issues.yml` verify readiness, prefix the indexed Kind Robots master roadmap issue with `[FLAGGED FOR HUMAN TESTING]`, and **close it as completed**. Verify the issue is actually closed; keep its URL indexed in `docs/agents/master-issues.yaml`. The GitHub issue closes because **agent production is complete**, not because Silas has accepted or released the game.
4. Remove the game from normal high-priority development rotation. Future changes are only scoped `playtest_iteration: true` polish/bug fixes in the fallback lane, plus Silas's still-open acceptance gate. Public launch, production deploys, spending, and subjective acceptance are separate hard gates.

## End of each hourly run

Report in at most five lines: game/task, shipped evidence (PR/commit/ArtJob or tests), CI/merge status, distance to playtest or successful transition (including closed issue), and the single next blocker. No generic status-only run, unsupported completion claim, fake green check, or branch without an open PR.
