# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-07T16:53:29Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **535**
- Outcomes: blocked: 13, cancelled: 1, done: 521
- Success rate: **97%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 62 | 98% |
| alexa-integration | 2 | 100% |
| animation-manager | 13 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 6 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 25 | 100% |
| conductor | 67 | 100% |
| conductor-app | 2 | 100% |
| davinci | 2 | 100% |
| digital-storefront | 25 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 4 | 100% |
| interface-vision | 73 | 100% |
| kind-robots | 43 | 98% |
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
| software | 520 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 9 |
| actionable | 9 |
| transient | 9 |
| scope | 2 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `quality` — 9 occurrences; look for the shared cause across its records
- failure category `actionable` — 9 occurrences; look for the shared cause across its records
- failure category `transient` — 9 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-07 `interface-vision/t-107` — When a dead route has no obvious replacement, check whether the same codebase already encodes a canonical answer before guessing -- dashboardConfigs.builder's own defaultTab ('character' -> /characters) was the principled destination for two broken '/builder' nav entries, and git-blaming the referenced UI component (components/abandonware/builder/ builder-manager.vue) confirmed it had been deliberately parked as unreachable (kind_robots
- 2026-08-07 `interface-vision/t-102` — A static-analysis route inventory (grep the router/content config rather than crawl a live site) is enough to build an accurate numeric shrink-to-zero baseline for a reachability audit, and the process of building it is itself an effective way to surface real dead-route bugs -- two were found here (a stale /scenarios path live in three navigation payloads, fixed; a dead /builder path in two nav sources, filed as t-107 since its correct destination needed product judgment) that a pure documentation pass would have missed.
- 2026-08-07 `kind-robots/t-055` — Historical audit inventories should preserve their original findings while later path relocations are recorded as durable errata, avoiding noisy rewrites of completed audit notes.
- 2026-08-07 `conductor/t-103` — Fixed the third confirmed instance of process_task_events.py's rearm/ready/done path silently freezing a t-010-style recurring task's nested continuous_improvement counter (it only ever wrote top-level status/note fields). Took the schema-field approach the original task note flagged as easier than free-text note parsing: two new optional event fields (continuous_improvement_lane, continuous_improvement_pr) that a closing session sets explicitly, applied atomically alongside the normal status transition via the same pure update function bump_continuous_improvement.py's manual CLI already used. This closes the gap for future task-events-path close-outs but does not retroactively repair any already-stale counter -- a session hitting a drifted counter still needs to notice and hand-correct it once, same as before.
- 2026-08-07 `interface-vision/t-101` — Clean first-pass close of a site-audit correction task: both flagged path drifts (storybook-mockups.vue deleted, plan-projects-grid.vue moved to abandonware) traced cleanly to specific kind_robots PRs (#1294/#1297, #1475) confirming both were intentional, expected changes rather than regressions -- no code fix needed anywhere, just closing-note addenda. Separately: PR #1824's one required repo-tracked check (Validate queued task-events YAML) sat stuck queued (runner_id 0) for several minutes while every sibling job in the same workflow run completed normally -- confirmed via githubstatus.com as the same GitHub-acknowledged Actions incident already logged three times this week (2026-08-06), this time manifesting as delayed runner pickup rather than a failed action-download step. A second push (bundling a TALKBACK entry) got a fresh CI run that completed cleanly in under a minute, so no extended wait or forced merge was needed. Treating it as transient and letting a natural next commit re-trigger CI, rather than repeatedly polling the same stuck job, resolved it faster than waiting would have.
- 2026-08-06 `ai-art-academy/t-010` — Lane-2 cycle's real blocker was a genuine review catch (ROADMAP-AUDIT.json/.md generated at different times, disagreeing with each other) -- fixed in one commit by re-running audit_roadmaps.py once against final state. What actually consumed the cycle was a ~2h GitHub Actions infra degradation that hit repo-tracked ci.yml checks directly (Validate queued task-events YAML, Dream-cycle backlog guards, Dependency audit), not just the default CodeQL scan already noted in t-060's lesson -- all failed with the identical "Failed to resolve action download info: Service Unavailable" signature (GitHub's own actions-download CDN). GitHub auto-retried most of them on its own after roughly an hour and they passed; a couple of non-required jobs stayed cancelled/failed and didn't block the merge. Confirming the identical log signature across every failure before classifying it transient (rather than guessing from the red X) avoided burning a pass or touching the PR's actual content.
- 2026-08-06 `ai-art-academy/t-060` — Clean first-pass extension of verify_academy_style_preview_coverage.py: the fix (an independent full-slug enumeration diffed against the previewImageSrc-scoped set) was exactly the shape the task note prescribed, and the current academyStyles.ts already has 0 slugs in the new gap category -- proved via synthetic fixtures instead of a live regression. Merge took much longer than the diff warranted: the repo's default GitHub code-scanning CodeQL "Analyze (javascript-typescript)" job sat in "Perform CodeQL Analysis" unchanged for 50+ minutes (vs. ~5 min for the identical job on the immediately-prior PR #1803), while every actually repo-tracked CI check in ci.yml passed within a minute. It isn't a repo-tracked workflow file, so it's a default code-scanning setup job, not one AGENTS.md's "confirm the checks themselves" guidance was written to gate on -- confirmed non-blocking by GitHub's own merge endpoint accepting the merge while it was still in_progress. Worth noting for the next session that sees a lone Analyze(*) job stuck this long: it's very likely non-required scanning-infra slowness, not a real signal about this PR's diff.
- 2026-08-05 `ai-art-academy/t-055` — The task's own claim had gone stale for ~8h with no PR ever opened (found via check_pr_merged_drift.py, unrelated to this task's content) -- a session should treat a claimed-but-un-PR'd task surfaced by that sweep as reclaimable once past CLAIM_TTL_MINUTES rather than assuming it's still in flight. Also: art-prompts.yaml alone is not a reliable coverage signal for delivered assets since fulfilled entries get pruned -- a live delivery check is required to tell "already fine" from "needs a request," which is why verify_academy_style_preview_coverage.py checks live by default.
- 2026-08-05 `conductor/t-101` — Before implementing a kaizen task, re-verify its premise against current code -- validate_task_events.py already had the exact check this task asked for (since PR #851, 2026-07-19), so the real remaining work was narrower (test coverage) plus a root-cause finding (task-events written by direct push to main never hit the PR-time gate at all) that the original task note didn't anticipate.
- 2026-08-05 `kind-robots/t-051` — A shallow kind_robots clone's default commit horizon can be too short to find a file's add/remove history even a few weeks back on a very active repo -- git fetch --unshallow before concluding a path was "never added" or "vanished without a trace" (same trap already documented for branch_janitor.py's merge-base classification).

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-07T16:53:29Z_
