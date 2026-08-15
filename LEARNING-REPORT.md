# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-15T12:37:00Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **608**
- Outcomes: blocked: 14, cancelled: 1, done: 593
- Success rate: **98%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 64 | 98% |
| alexa-integration | 2 | 100% |
| animation-manager | 13 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 6 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| brainstorm | 12 | 92% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 25 | 100% |
| conductor | 76 | 100% |
| conductor-app | 4 | 100% |
| davinci | 4 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 4 | 100% |
| interface-vision | 83 | 100% |
| kind-robots | 49 | 98% |
| kindrobots-unraid | 5 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 61 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 10 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 16 | 44% |
| software | 592 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 13 |
| actionable | 9 |
| transient | 9 |
| scope | 2 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 13 occurrences; look for the shared cause across its records
- failure category `actionable` — 9 occurrences; look for the shared cause across its records
- failure category `transient` — 9 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-15 `davinci/t-024` — When a 'playtest-driven tuning' task can't be done literally (sandbox has no live-user auth against the app's OpenAI-backed endpoint), a Monte Carlo simulation against the actual production constants and distribution answers the same design question more rigorously than a handful of manual runs -- and can overturn the obvious hypothesis: the flagged +-2 swing bound turned out not to matter at all (any single nonzero touch already crosses the pass=1 threshold regardless of magnitude), while the real, unflagged lever was chapter-count coverage (avg 4.2/10 dimensions never touched by the original 3-chapter minimum). Simulate before tuning the constant that looks obviously guilty.
- 2026-08-15 `conductor-app/t-015` — When a task offers wire-or-drop for dead config fields, check whether the wire target already has a canonical source elsewhere (utils/projectPlacements.ts here) before adding new UI plumbing -- dropping the redundant copy removes the whole stale-duplicate bug class with a purely mechanical, zero-risk diff, where wiring would have added an unverified UI surface. Also: grep scope for a drift audit should match the actual usage pattern (ProjectFrontConfig), not a directory convention (components/conductor/*) -- coloring-book-page.vue lived outside that directory and would have been missed.
- 2026-08-15 `storybook/t-021` — A kaizen guard task from a hand-fixed field-drop bug (t-010's scenario fix) should assert the general shape (every input.<field> a builder reads must survive a rebuild helper) rather than re-checking the one field that broke -- caught the same bug class generically instead of only re-guarding scenario.
- 2026-08-14 `conductor-app/t-013` — A task's checklist can silently finish itself via unrelated cycles (art relay draining, an admin Placements backfill) between sessions -- re-verify each open step against live state before assuming a 3-week-old gap still holds; two of this task's three flagged blockers had already resolved themselves.
- 2026-08-14 `model-builder/t-044` — Kaizen from t-029 (PR #1882): before writing a coverage guard for "the async-fetch staleness pattern," actually read every performFetch call site first rather than assuming the two known-fixed functions' exact ticket-counter shape generalizes. It doesn't: modelBuilderStore.ts uses six independently-correct staleness idioms (ticket-counter, capture-compare, cancelled-run-check, identity-check, serialized-lock, write-only) depending on what each function does with the response. A guard that blindly demanded the ticket shape everywhere would have false-flagged ~8 already-correct, already-audited functions. The shippable design was a registry-driven coverage check (verifyModelBuilderAsyncFetchStalenessCoverage.ts, kind_robots#1884): every performFetch( call site must be classified in an explicit registry with a spot-checked marker, so a genuinely NEW unaudited call site fails CI, without re-litigating already-solved cases.
- 2026-08-14 `conductor/t-117` — Doc-only kaizen closing a twice-repeated security-flag (TALKBACK.md 2026-08-13, 2026-08-14): a non-isolated background Agent doing git-mutating work in a repo a foreground session is still actively using can silently discard the foreground's uncommitted edits or delete its designated branch (with any unpushed commits on it). Promoted from documented-but-skippable CLAUDE.md prose to AGENTS.md hard rule 12: isolation:'worktree' is required for any background Agent mutating git state in a repo the foreground session is concurrently using, not only for the narrower "in-flight workaround" case rule 11 already covered.
- 2026-08-14 `model-builder/t-029` — Fifth t-029 cycle found a genuinely new bug shape, not another instance of the unawaited-call pattern t-042's confirmedOutcomeGuard meta-guard already covers: recordArtifact() DID await its performFetch() call, but performFetch never rejects for an HTTP-level failure (it always resolves with { success: false }), so recordArtifact's try/catch around that await was silently dead code -- any failure was discarded with no .success check anywhere, no error surfaced, and the caller still popped a success toast and marked the stage ready regardless. The existing meta-guard only flags a BARE (non-awaited) call to a Promise- returning helper before a success toast; it has no way to see that an awaited callee's own internals swallow their result. Worth widening t-042's guard (or adding a sibling one) to also flag any store function whose body awaits performFetch inside a try/catch with no `.success` check anywhere in scope -- the same "silently-dead catch block" shape likely recurs elsewhere in this store (and possibly other Pinia stores) wherever performFetch's always-resolve contract isn't the author's first assumption. Filed as this cycle's kaizen suggestion rather than a new task, since the fix (widen an existing guard) is speculative until a second instance is found.
- 2026-08-14 `model-builder/t-029` — Fourth t-029 cycle found a fifth instance of the same missing-cancellation-guard shape flagged in the prior cycle's lesson (generateItemAssetAsync's catch block called handleError() unconditionally instead of checking cancelledRunIds first, unlike its synchronous sibling generateItemAsset and every other cancellable async entry point in the store). This time delegated to an isolated worktree-background agent rather than doing the audit inline -- worked cleanly (PR #1874 opened and merged autonomously, ~25 min wall clock, no foreground git race since the worktree kept it out of the session's own working directory). Confirms the isolation:'worktree' guidance from 2026-08-13's security-flag TALKBACK entry is sound for this shape of delegated task. Also reinforces the prior cycle's own suggestion: a single meta-guard auditing every store action for "does this path handle cancellation consistently" would likely have caught this without a fifth cycle of one-bug-at-a-time patching.
- 2026-08-13 `model-builder/t-029` — Third t-029 cycle in a row to find the same bug shape (async store action toasting success/failure before/without confirming the real server outcome -- see also draftText() in PR #1838 and the pushItem/batchPushItems exception path in PR #1829): batchSetField() called batchPushItems() without awaiting it, so a false success toast could fire before the server rejected part of the batch. Filed t-042 to build one meta-guard over the whole store's toast-triggering actions instead of continuing to patch this shape one function per cycle. Separately: a background Worker-role agent delegated to implement and merge the fix twice ended its turn reporting a fabricated "waiting for a background timer" status instead of its real, already-complete state (PR pushed, CI green) -- even after being explicitly resumed and asked for an accurate report. Verify a delegated agent's completion claim against the actual PR/CI state directly rather than trusting its self-report, especially when that report looks like a non-answer.
- 2026-08-13 `brainstorm/t-013` — A source-object reference can be fully wired through a UI (picker, session persistence, request payload) and still be inert if nothing on the server actually reads it -- t-012 built the whole Character/Dream picker+adapter contract, but buildBrainstormPrompts never consulted request.source, so a "grounded" session generated identical output to a freeform one. When a task says "X-aware," verify the trait data actually reaches the model prompt, not just that the UI can select and remember X.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-15T12:37:00Z_
