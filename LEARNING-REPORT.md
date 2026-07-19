# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-19T00:23:51Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **278**
- Outcomes: blocked: 12, done: 266
- Success rate: **96%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 29 | 100% |
| alexa-integration | 2 | 100% |
| animation-manager | 5 | 100% |
| animation-studio | 1 | 100% |
| appmaker | 2 | 100% |
| approval-portal | 2 | 0% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 13 | 100% |
| conductor | 37 | 100% |
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
| newsfeed | 9 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 2 | 100% |
| serendipity | 3 | 100% |
| superkate-hairstyle-ai | 16 | 100% |
| superkate-services-calculator | 11 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 263 | 99% |

## Failure categories

| Category | Count |
|---|---|
| actionable | 6 |
| quality | 5 |
| transient | 1 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `actionable` — 6 occurrences; look for the shared cause across its records
- failure category `quality` — 5 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-07-19 `global-ui/t-023` — A task can reach a state where the only remaining item is an explicitly-flagged 'needs Silas's visual preference, not more digging' cosmetic call. Applying the task's own already-established default (leave ambiguous color additions as-is) and closing done is better than leaving it 'ready' indefinitely awaiting a low-stakes call nobody is blocked on -- reserve needs-human for calls that actually block something.
- 2026-07-19 `global-ui/t-012` — Task fully delegated its remaining scope to a sibling kaizen task (t-023) via note text ('see kaizen t-023') instead of a depends_on/blocks link, so nothing machine-readable pointed back at t-012 once t-023 finished. Worth closing the delegating task in the same pass that closes the delegate, rather than leaving a zombie 'ready' shell with no landable scope of its own.
- 2026-07-18 `ai-art-academy/t-034` — Fourth seed-sync task of this exact shape (t-015/t-018/t-020/t-031/t-034: mirror a new curriculum-outline.md movement into academyStyles.ts). The array is sorted by sortYear at runtime (academyTimeline), so literal insertion position in the source array is a readability convention, not a functional requirement -- worth remembering before treating chronological placement as a correctness constraint.
- 2026-07-18 `newsfeed/t-007` — Store-side work (feedPreferenceStore's enableFeed/disableFeed/reorderFeeds, t-004) had already shipped with zero UI consuming it -- worth checking for this shape generally: a 'ready' feature task may already be half-built by an earlier task's kaizen/over-scope, so grep the store/helpers layer for existing actions before assuming a feature needs building from scratch.
- 2026-07-18 `serendipity/t-011` — A fully-drafted implementation doc left behind by a blocked session (projects/serendipity/docs/t-011-serendipity-agent-todo-badge-filter.md) made this a near-zero-ambiguity patch-and-verify task; leaving such docs behind on a soft block is worth doing consistently since it turns the next session's work into transcription instead of redesign.
- 2026-07-18 `serendipity/t-008` — A prior connector-only session's GitHub write-safety-filter block does not mean the task is stuck -- a session with real git + GitHub MCP patch access can just implement the already-scoped fix directly; re-check for patch access before assuming a soft-blocked task needs another connector-only attempt.
- 2026-07-18 `newsfeed/t-015` — Before implementing a task whose note references a generated/shared file (here public/components.json / create-component-json.mjs), grep sibling projects' roadmaps for the same filename first -- this task duplicated kind-robots/t-039+t-040 verbatim and was closeable by cross-reference alone, with zero new code.
- 2026-07-18 `kind-robots/t-040` — Mechanical drift-correction tasks (regenerate a committed generated file after a generator fix lands) are clean one-pass work when scoped tight: ran the generator, diffed line-by-line to confirm only additions + alphabetical fixes (no reordering churn, no removals), left the generator's other untracked output file alone since it was never part of this repo's history.
- 2026-07-18 `kind-robots/t-039` — Pinning localeCompare(..., 'en') in create-component-json.mjs's three sort call sites made the generated manifest deterministic across Node/ICU builds. When a kaizen note bundles a determinism fix with a separate drift-correction (here: missing components in the committed file), keep the diff scoped to just the fix and file the drift correction as its own ready task (kind-robots/t-040) rather than expanding the PR.
- 2026-07-18 `newsfeed/t-009` — Stale-source tolerance (last-known-good cache per source, bounded to 24h, flagged stale: true) was the one real gap left after t-005/t-006 shipped bounded caching, stable identity, dedup, and partial-success -- verified with a local http.createServer fixture (serves once, then closes) instead of relying on live network egress to prove the fallback path.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-19T00:23:51Z_
