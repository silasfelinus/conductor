# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-16T17:54:56Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **990**
- Outcomes: blocked: 16, cancelled: 1, done: 973
- Success rate: **98%**
- Average passes on successful tasks: **0.1**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 73 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 14 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 9 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| brainstorm | 26 | 96% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 38 | 100% |
| conductor | 119 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 51 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 23 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 135 | 100% |
| kapowarr | 52 | 100% |
| kind-economy | 10 | 100% |
| kind-robots | 61 | 98% |
| kindrobots-unraid | 9 | 100% |
| lora-ingestion | 1 | 100% |
| mandarin-tutor | 11 | 100% |
| media-watchlist | 12 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 84 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| rainbow-butterflies | 21 | 100% |
| ruler-hooked | 11 | 100% |
| scene-animator | 2 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 25 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 7 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 973 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 27 |
| transient | 16 |
| actionable | 15 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 47% success over 17 closed tasks; aim the next kaizen task here
- failure category `quality` — 27 occurrences; look for the shared cause across its records
- failure category `transient` — 16 occurrences; look for the shared cause across its records
- failure category `actionable` — 15 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-16 `conductor/t-175` — Not every asymmetry between two similar-looking code paths is a bug to converge. verify_event_ownership() (review/done) and the claim branch of compute_transition_ops() (t-173) both touch roadmap_claims.claim_is_stale(), but only the claim branch should: a fresh claim over a stale one only starts new work, while a stale session's late review/done event could silently overwrite a second session's in-progress reclaim. The existing claim path already gives a legitimate session a safe way to take over stale work, so no extension was needed -- documenting the asymmetry in the docstring (with a pinning regression test) closed the decision task without changing behavior.
- 2026-09-16 `conductor/t-173` — A three-call-site staleness rule (next_ready_task.py, claim_task.py, process_task_events.py) had silently drifted to two-out-of-three: the connector processor's claim collision check never consulted roadmap_claims.claim_is_stale(), so a prior session had to paper over the disagreement with a dedicated preflight script (promote_stale_task_event_claims.py) instead of fixing the root disagreement. Making the processor call the shared helper directly let that whole preflight (plus its test and workflow step) be deleted rather than maintained alongside the thing it was working around -- a smaller total diff than the workaround it replaced (68 insertions/177 deletions).
- 2026-09-16 `kind-robots/t-105` — A multi-session small-batch rollout (probe-plan -> enqueue -> verify write-back, repeated in bounded batches while checking render-box/relay health each cycle rather than firing all 223 jobs at once) closed cleanly: 2209/2228 LoRA-family Resources now carry owned preview art, the last job (ArtJob 26249, resourceId 1072) verified DONE with Resource.artImageId/imagePath confirmed written back. The remaining 18 rows are a genuine structural gap (no still-image probe recipe for SD 2.1 768 / Flux.1 Kontext bases), not further queue/relay work -- correctly left as a deferred scope decision for Silas rather than forced into this task or auto-filed as a new one.
- 2026-09-16 `conductor/t-174` — Test-only PR closing a kaizen-flagged coverage gap (main() integration tests for a script whose pure formatter already had unit coverage) merged clean on the first pass, all 25 checks green, no behavior change to the script under test.
- 2026-09-16 `conductor/t-172` — Clean first-pass success. A narrowly-scoped CI-annotation feature (one ::error:: line naming the first missing heading, existing stderr list untouched) with a regression test asserting the exact emitted text merged with all 23 checks green on the first push, including its own PR passing the handoff-template gate it is adjacent to.
- 2026-09-16 `coloring-book/t-022` — Wrapping a live production-mutating script call (consume_coloring_book_studio_request.py --live) in a shell-level `timeout` shorter than the script's own internal polling/recovery window SIGTERMs the process before it can record its own render_gate_job_id, discarding the graceful-preserve bookkeeping every other in-flight queue entry relies on for later recovery. coloring_queue_status.py's queue_integrity_safe/recovery_safe/retry_safe checks caught that this left the entry in a safe (if less useful) fresh-submission state rather than a duplicate/orphaned one -- always re-run that check immediately after any forcibly-terminated production script call, and prefer omitting an external timeout wrapper (or sizing it well past the script's documented internal timeout) over guessing a shorter one.
- 2026-09-16 `storybook/t-026` — A task titled "rename the API namespace and storage keys" can share a database table with a much larger adjacent engine (the generic /api/storybook/runs/* deck engine also reads/writes LifeRun rows) -- reading that overlap as license to migrate the client onto the larger engine would have been an undisclosed scope expansion; the literal rename (move the routes, thin-shim the old paths, dual-read the storage keys) was the correct, reversible scope the task actually asked for.
- 2026-09-16 `conductor/t-171` — Enforcing a documentation convention (the Worker PR handoff template) as a CI check on worker/* branches, verified against its own PR before merge, closes a kaizen loop more durably than relying on each Reviewer session to notice thin PR bodies ad hoc.
- 2026-09-16 `rainbow-butterflies/t-053` — A "document this orphaned API surface" task can surface a real design question (AgentProfile-bound credentials have no UI in kind_robots) without it being safe to file as a fix task, when the other half of the flow lives in a repo outside the session's access scope (rainbowbutterflies) -- flag the open question in the note for a session that can see both sides instead of guessing at scope.
- 2026-09-16 `conductor/t-132` — Cross-workflow stalls at unrelated steps, despite an existing job timeout, are runner/platform evidence; do not optimize the most frequently observed command unless the failure reproduces specifically there.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-16T17:54:56Z_
