# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-13T15:05:21Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **598**
- Outcomes: blocked: 14, cancelled: 1, done: 583
- Success rate: **97%**
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
| brainstorm | 11 | 91% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 25 | 100% |
| conductor | 75 | 100% |
| conductor-app | 2 | 100% |
| davinci | 3 | 100% |
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
| model-builder | 57 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 9 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 16 | 44% |
| software | 582 | 99% |

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

- 2026-08-13 `conductor/t-116` — Two independent sessions leaked KR_API_TOKEN into their own transcripts with the identical broken probe (${VAR:-no} substitutes the live value once set, it isn't a safe fallback) despite one prior TALKBACK entry already documenting the correct -n/-z pattern in prose. Prose-only guidance in a log file is not discoverable enough to stop a repeat mistake -- a copy-pasteable helper script referenced from AGENTS.md is the fix that actually generalizes.
- 2026-08-13 `conductor/t-115` — select_role.py's github_api_unreachable flag existed but nothing acted on it -- a session could read role: worker at face value and skip reviewing mergeable work the local git checks simply couldn't see (missed 3 green PRs, 2026-08-13 ~05:15 UTC). Downgrading worker/idle to reviewer-uncertain whenever the flag is true closes the gap structurally instead of relying on every session noticing a caveat field. General lesson: a script that already computes a reliability signal should fold it into its top-line recommendation, not just expose it alongside the recommendation for callers to remember to check.
- 2026-08-13 `model-builder/t-041` — Kaizen chain from t-029 (kind_robots#1825) landed cleanly first-pass: the same run-scoping gate (setStatusForRun) needed to cover both the {success:false} response branch AND the raw network-exception (.catch) branch of pushItem/batchPushItems, not just the one the original PR touched. When a kaizen task targets "the same class of issue" in a sibling code path, check for other branches of the same conditional (success vs. exception) that need the identical fix, not just the one named in the kaizen note.
- 2026-08-12 `conductor/t-114` — A backslash inside an f-string expression part is invalid grammar before Python 3.12 -- CI's "Lint Python scripts" syntax check runs 3.12 so it never caught this, only this sandbox's local 3.11 pytest did (via a collection-time SyntaxError, not a real test failure). Worth generalizing -- when a script targets an f-string with any escaped-quote/backslash content in its {} expression part, extract the literal to a plain variable first regardless of which Python version the immediate CI check happens to run, since the actual production runner's version is often not the same as CI's syntax-check job.
- 2026-08-12 `brainstorm/t-012` — A fail-open picker defect (adapter returns cached rows when a forced-fresh revalidation fails) needed an explicit "fail closed on unsuccessful fresh retrieval" helper, not just forcing the fetch call itself -- four separate quality rejections traced increasingly specific slices of the same class before the fix finally covered both the by-id resolve path and the list-search path on both adapters at once (fetchFreshSourceRows checking store.error rather than trusting the returned array). Worth generalizing into a shared contract check the next time an authorization-sensitive picker is added, rather than re-deriving it per adapter.
- 2026-08-12 `brainstorm/t-012` — Authorization-sensitive pickers must distinguish a successful fresh retrieval from store fallback/cache behavior; forcing a fetch is insufficient if the store fails open or the adapter ignores the fresh return value.
- 2026-08-12 `model-builder/t-029` — verifyModelBuilderCompletionGate.ts's post-await stage-write scanner only matches direct `item.stages.KEY = ...` assignments in async functions -- it can't see a write that happens indirectly through a synchronous helper call like approveStage() (bracket-notation write inside its own body). autoBuildItem() slipped an unconditional approveStage() call past that existing guard for exactly this reason, silently re-approving a stage a concurrent Edit click had just marked stale mid-await. A new narrow per-call-site guard (verifyModelBuilderAutoBuildApprovalRaceGuard.ts) closed this instance; the completion-gate scanner itself would be more robust generalized to flag any approveStage/rejectStage call after an await with no adjacent status check, rather than needing a new file per call site each time this shape recurs.

- 2026-08-12 `model-builder/t-029` — A prior session's branch-medic flag (stranded worker/model-builder-t-029-20260811-c4a91f, real tested fix never turned into a PR) was picked up and opened as PR #1792 by a later session, then reviewed/merged cleanly by this one -- the cross-session rescue handoff described in AGENTS.md's branch-medic role worked end-to-end without any direct coordination between the three sessions involved.
- 2026-08-11 `digital-storefront/t-005` — Routine state reconciliation (checking a PR referenced by a hard-gated needs-human task, not because anything prompted it) found Silas had already merged kind_robots #1668 himself -- decisive objective evidence per docs/state-reconciliation.md that he'd answered the gate's own multiple-choice question. But the merge only covered 4 of the 5 originally-flagged routes; a fifth (rewards/random.get.ts) still had the identical unfiltered-access gap. Closing a human gate on "the human acted" evidence still needs a scope check against the gate's own original list -- a partial fix that matches the merged precedent exactly is safe to finish without going back for a second decision, since the policy call was already made, but silently marking the whole task done on the merge alone would have left a real gap open while reporting it closed.

- 2026-08-11 `model-builder/t-029` — An Explore subagent given an explicit list of every bug class already fixed this same day (two singleton-clearing fixes plus an aria-pressed fix) and told to read the actual store/component code rather than trust a summary found a genuinely different bug shape: three textareas bound to local component refs that only pushed to the store on @change (blur), so the store's own "don't clobber a newer edit" guard in draftText() -- which only compares against the store's value -- couldn't see text the user was still mid-typing. The fix (disable the textarea while its own field is drafting) mirrors a gate already present one UI element over (the "Draft with AI" button), which is often a good signal that an adjacent, un-gated control was simply missed rather than intentionally left open.


---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-13T15:05:21Z_
