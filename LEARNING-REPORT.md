# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-19T09:06:24Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **288**
- Outcomes: blocked: 12, done: 276
- Success rate: **96%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 32 | 100% |
| alexa-integration | 2 | 100% |
| animation-manager | 6 | 100% |
| animation-studio | 1 | 100% |
| appmaker | 2 | 100% |
| approval-portal | 2 | 0% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 13 | 100% |
| conductor | 38 | 100% |
| digital-storefront | 12 | 100% |
| dream-cycle | 14 | 100% |
| ecosystem-map | 4 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 1 | 100% |
| kind-robots | 29 | 97% |
| kindrobots-unraid | 4 | 100% |
| media-watchlist | 1 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 28 | 100% |
| mural-design | 1 | 100% |
| newsfeed | 12 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 2 | 100% |
| serendipity | 3 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 11 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 273 | 99% |

## Failure categories

| Category | Count |
|---|---|
| actionable | 6 |
| quality | 5 |
| transient | 3 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `actionable` — 6 occurrences; look for the shared cause across its records
- failure category `quality` — 5 occurrences; look for the shared cause across its records
- failure category `transient` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-07-19 `ai-art-academy/t-010` — A queued task-events/ entry stuck behind a sibling file's YAML syntax bug applied stale status/note state on top of this session's freshly-claimed t-010 once it finally processed -- process_task_events.py has no staleness check against the task's current claimed_at/updated, unlike claim_task.py's live-recheck guard for direct claims. Read a corrupted roadmap note carefully before re-editing it: the truncated/duplicated fragment was easy to mistake for legitimate history at a glance. Filed conductor/t-067 for the underlying gap.
- 2026-07-19 `animation-manager/t-009` — Building a mechanical verifier over a hand-authored YAML catalog is a good way to discover the catalog was never actually machine-parseable (an unquoted colon in one field broke every YAML loader) -- worth a quick parse-and-scan pass on the target file before assuming its structure is well-formed just because agents have been hand-editing it successfully.
- 2026-07-19 `superkate-hairstyle-ai/t-021` — When a task asks for coverage that turns out to be technically impossible as literally scoped (here: a real authenticated-admin Cypress session, blocked by no JWT-minting path being exposed to Cypress), investigate the actual mechanism before writing the test -- then ship the narrower assertion that IS real (the access-gate redirect) and file the precise gap as a kaizen suggestion, rather than faking the broader claim or silently doing less than asked.
- 2026-07-19 `newsfeed/t-011` — Clean single-pass implementation of staged BIAS-CONTROLS.md work; the honest 'nothing to visibly act on yet' flag (no FEED_SOURCES ratings seeded) was the right call over inventing plausible-looking ratings, and became the kaizen follow-up (t-018) instead of scope creep on this task.
- 2026-07-19 `ai-art-academy/t-010` — PR #506's file diff listed two files (stylist-mask-brush.vue, stylist-restyle.vue) that looked out of scope for an academyStyles.ts sync -- turned out to be the exact 'main already has equivalent content under a different squash SHA' pattern from CLAUDE.md, confirmed safe by diffing the PR's own commit content against origin/main directly rather than trusting the file-list at face value.
- 2026-07-19 `ai-art-academy/t-010` — continuous-improvement-checklist.md's coverage table already names the next verifiable action per area; reading it directly instead of re-auditing the curriculum from scratch is the fast path to a scoped, low-ambiguity t-010 cycle.
- 2026-07-19 `superkate-hairstyle-ai/t-018` — The task's own note already scoped two options (server-side seg node vs client brush) and flagged which one is sandbox-reachable; reading that scoping note before claiming avoided burning a pass on the infeasible option (a), which needs ComfyUI box access no agent session has.
- 2026-07-19 `newsfeed/t-008` — Two claimed tasks in the same project touching the same files (newsfeed t-008/t-010) can merge minutes apart and produce an avoidable conflict on the second review; check same-project open PRs' file lists for overlap before merging the first one, not just at merge time on the second.
- 2026-07-19 `newsfeed/t-010` — Accessibility-polish tasks (aria attributes, focus-visible, motion-safe, semantic timestamps) verify cleanly with vue-tsc/eslint/prettier alone when no live nuxt dev preview is reachable in-sandbox; keep flagging the missing visual/keyboard-nav check explicitly rather than treating static verification as sufficient proof.
- 2026-07-19 `conductor/t-039` — Two projects can duplicate scope task-for-task under different ids/titles (animation-studio/t-004 vs animation-manager/t-004, near-identical asks) with no explicit link between them -- when a roadmap gains a clear 'active continuation' project, check whether an older sibling project should retire via project-overrides.yaml rather than staying independently claimable and risking a Worker re-doing already-shipped work.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-19T09:06:24Z_
