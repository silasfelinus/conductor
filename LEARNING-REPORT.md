# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-02T05:40:29Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **853**
- Outcomes: blocked: 16, cancelled: 1, done: 836
- Success rate: **98%**
- Average passes on successful tasks: **0.1**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 70 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 14 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 9 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| brainstorm | 26 | 96% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 25 | 100% |
| conductor | 87 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 41 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 20 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 96 | 100% |
| kapowarr | 48 | 100% |
| kind-economy | 6 | 100% |
| kind-robots | 54 | 98% |
| kindrobots-unraid | 5 | 100% |
| lora-ingestion | 1 | 100% |
| mandarin-tutor | 11 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 81 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| rainbow-butterflies | 18 | 100% |
| ruler-hooked | 11 | 100% |
| scene-animator | 2 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 16 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 6 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 16 | 44% |
| software | 837 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 15 |
| transient | 13 |
| actionable | 12 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 15 occurrences; look for the shared cause across its records
- failure category `transient` — 13 occurrences; look for the shared cause across its records
- failure category `actionable` — 12 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-02 `mandarin-tutor/t-020` — A production incident recovery task can sit at status: ready for days after the actual outage clears, if nothing re-checks it once Silas's "temporary outage, should be fixed" answer releases the gate -- the gate answer only unblocks the next agent to go verify, it doesn't verify anything itself. Recovery was confirmed here with tools that already existed (check_render_box.py, drain_failed_art_backlog.py's dry-run classification) -- no new code needed, just actually running them against current live state instead of trusting the multi-day-old note.
- 2026-09-02 `mandarin-tutor/t-010` — A dedicated read-only, media-origin HEAD-probe audit is worth writing even when a project already has "reach" tooling (queue_mandarin_tutor_art.py) that reports its own missing/staged counts -- that tooling's notion of "missing" is scoped to its own staging file (art-prompts.yaml), not to what actually rendered. Trusting it instead of probing the media origin directly would have hidden that "already staged: 0" no longer meant "nothing done" once the corpus's original request rows left the file. Re-running that same "reach" tool as a naive double-check (rather than the read-only audit) came within one command of re-staging an already-100%-rendered 577-card corpus as missing, which would have duplicate-submitted it against a host that just recovered from an outage -- filed as conductor/t-142. General lesson: a tool whose job is "make sure X is requested" is not a safe stand-in for auditing "is X actually done," even when it reports a count that looks like an audit.
- 2026-09-01 `model-builder/t-029` — Cycle 77: a new doc-comment's own prose can trip a regex-based static guard that scans for keywords without distinguishing code from comments -- verifyModelBuilder CompletionGate.ts's `\bawait\b`-based "find the function's first await" heuristic matched the bare word inside this cycle's own explanatory comment ("per-item-await loops"), shifting its notion of where real async work starts and flagging an unrelated pre-existing comment 20+ lines later as an ungated write. A regex-based guard against source text is exactly as blind to comments/strings as the pattern it's matching, so a new comment near guarded code should be checked against every such guard's actual matching logic, not just eyeballed for correctness.
- 2026-09-01 `interface-vision/t-104` — A recurring task's note: field narrated a merge and a "re-arming to ready" no-op cycle that its status: field never actually recorded -- the narrative outran the machine-readable state by at least one cycle before check_pr_merged_drift.py's merged-implementation_pr-vs-claimed-status check caught it. A cycle that intends to re-arm a recurring task should verify the status: field actually changed, not just that the note says it did.
- 2026-09-01 `model-builder/t-029` — Cycle 76: a prior cycle's own regression fix (cycle 75's runId-based release guard) had a same-run-revisit gap -- a captured run id is not a one-shot token when the store caches and reuses run objects (openRun's cached-adopt branch, resumeRun's revisit branch), so re-checking a fix's *invariant* against the actual data model (can this id compare equal again after the abandon event?) rather than trusting the fix's own stated shape is what surfaced this. Fixed with a monotonic epoch counter instead of strengthening the id check further. Also had to broaden two existing guards' regexes (not just add a new one) since the fixed condition's shape legitimately changed -- worth checking whether a new guard should tighten or loosen a prior one when a fix's shape evolves, rather than always adding purely-additive checks.
- 2026-09-01 `rainbow-butterflies/t-037` — Straightforward kaizen-slice implementation (own PR, own review/merge under the standing merge-when-green authorization): reusing t-036's authAttemptLimit helper in login.post.ts surfaced a real, separate bug worth fixing in the same PR rather than filing separately -- the handler's catch block flattened every thrown error, including the helper's own 429, into a generic 500 via `sendError(event, new Error(message))`. A quick grep confirmed this exact "no isError() check before sendError" pattern doesn't recur elsewhere in server/api, so no follow-up kaizen task was warranted for it.
- 2026-09-01 `rainbow-butterflies/t-036` — Reviewed kind_robots#2297's rate-limit slice; its one CI failure was a real but narrow type error, not a scope/quality problem: h3 1.15.11 types the Retry-After response header as number, and the new helper passed String(...). Fixing and pushing a 2-line diff directly to the Worker's PR branch (rather than bouncing it back to the Worker with retry_context) got it green in one cycle. Also worth flagging: the PR auto-merged on its own once the known-flaky 'Contract verifiers'/ESLint-ratchet check (conductor/t-132) finally completed, without this session calling merge_pull_request -- consistent with the PR's opener having enabled auto-merge, and a reminder to re-check PR state (not just CI) before assuming a merge still needs to be triggered manually.
- 2026-09-01 `rainbow-butterflies/t-028` — Deployment roadmaps should reconcile against observed production state before retaining a launch gate; once the approved domain is already live, continuing to present activation as future work creates misleading project state.
- 2026-08-31 `rainbow-butterflies/t-013` — A prior session's claim on this task went stale (CLAIM_TTL_MINUTES expired) after 7 real implementation commits with no PR ever opened -- next_ready_task.py correctly surfaced it as reclaimable. Rather than re-implementing from scratch, fetched the actual worker/* branch, verified the existing diff was substantive real feature work (not scratch/placeholder), rebased it cleanly onto current main, fixed the lint/type issues it had never gotten past (eslint no-explicit-any and the resulting vue-tsc noUncheckedIndexedAccess fallout), and shipped it as kind_robots#2261. Preserving a stranded-but-real branch instead of discarding and redoing the work saved real effort and avoided a duplicate implementation. Also found the same session's CI run surfaced a genuinely broken base branch (Python test suite red on main from two malformed LEARNING.yaml records -- a YAML-breaking unescaped colon and an invalid failure_category enum value); root-caused and fixed both in a separate PR (#3316) rather than treating the failure as this PR's problem, confirming the fix by reproducing the original failure locally first.
- 2026-08-31 `interface-vision/t-104` — Slice 32 of the recurring kr-panel-flat consistency sweep -- pages/music-mentor.vue's feature-row div swapped hand-rolled "border border-base-300 bg-base-100" for the shared primitive, no geometry/behavior change; kind_robots#2256, 38/38 checks green. Also caught that check_pr_merged_drift.py's API-403 output was masking a genuine unreconciled gap, not just its usual unverifiable-transport false alarm: a separate, earlier slice (kind_robots#2253, Academy Timeline) had merged with zero note entry ever recorded for it. Cross-checked via the MCP connector rather than trusting the exit code alone, and backfilled the missing note before closing this cycle -- worth distinguishing "already reconciled, just can't verify from this sandbox" from "genuinely never reconciled" rather than assuming the former by default.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-02T05:40:29Z_
