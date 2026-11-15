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

1. Finish and verify every finite build, art, text, QA and accessibility task. **Do not create, retain or require a human-playtest/verdict task in the build roadmap.** A human testing checklist is a handoff artifact, not a prerequisite verdict. Keep independent release, publication and wider-promotion decisions separate from the roadmap.
2. In **Conductor** `project-overrides.yaml`, set `status: playtest` and **`priority: normal`** (the normal/medium value); never edit Kind Robots' materialized coordination projection directly.
3. Let `.github/workflows/sync-playtest-master-issues.yml` verify finite readiness, prefix the indexed Kind Robots master issue `[FLAGGED FOR HUMAN TESTING]` and close it **as completed**. Verify the issue is closed and retain its canonical URL. The issue closes because agent production is complete, not because a human has played or accepted it.
4. Remove the game from the high-priority build queue. Future tweaks are explicitly scoped `playtest_iteration: true` tasks. Prepare a concise **human playtest checklist** and a project-specific 1080×1350 social-ready promotional image with verified playable link, actual art, accurate feature claims and editable source where practical. Do not publish/share the graphic, promote the game publicly or deploy without the distinct human authorization that applies to those actions.

## End of each hourly run

Report in at most five lines: game/task, shipped evidence (PR/commit/ArtJob or tests), CI/merge status, distance to playtest or successful transition (including closed issue), and the single next blocker. No generic status-only run, unsupported completion claim, fake green check, or branch without an open PR.
