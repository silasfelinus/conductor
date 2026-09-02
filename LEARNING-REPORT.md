# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-02T13:11:43Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **859**
- Outcomes: blocked: 16, cancelled: 1, done: 842
- Success rate: **98%**
- Average passes on successful tasks: **0.1**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 72 | 99% |
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
| conductor | 91 | 100% |
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
| software | 843 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 16 |
| transient | 13 |
| actionable | 12 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 16 occurrences; look for the shared cause across its records
- failure category `transient` — 13 occurrences; look for the shared cause across its records
- failure category `actionable` — 12 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-02 `conductor/t-145` — A soft/advisory CI check belongs on its own continue-on-error step inside an existing job (GitHub Actions ::warning:: annotations), not a new blocking job -- git diff --numstat plus git show <ref>:<path> is enough to diff base vs head line counts for any watched file without a second full-file-read diffing path. This session's sandbox pytest tool was again missing PyYAML (the same documented gap as t-140's session) and needed uv tool install pytest --with pyyaml --force before the 13 new tests could run.
- 2026-09-02 `conductor/t-140` — close_task.py now warns (not fails) when a review/ready close omits --implementation-pr while the roadmap already holds a different owner/repo#N value -- the write-time half of the drift class t-139 targets from the read side. Companion note: this session's own sandbox pytest tool was missing PyYAML (AGENTS.md's documented gap) and needed `uv tool install pytest --with pyyaml --force` before the new regression tests could run.
- 2026-09-02 `conductor/t-143` — GitHub's Contents API silently returns encoding:none/content:'' for files over 1MB, so any read-modify-write into a growing conductor file (art-prompts.yaml, TALKBACK.md, LEARNING.yaml) must fall back to the Git Blobs API and throw rather than treat a bodiless-but-nonempty read as an empty file -- kind_robots#2320 fixed both the queue write path and conductorGet() with this pattern plus an append-only invariant check.
- 2026-09-02 `ai-art-academy/t-078` — A workflow's KR_BASE_URL must be verified against the current self-hosted host (kindrobots.org), not copied from an older *.vercel.app pattern -- a wrong default would have made the new sentinel look deployed while silently never reaching its signature check. Caught in review before merge, fixed in one retry.
- 2026-09-02 `conductor/t-142` — Ephemeral request rows cannot be the only deduplication source; producers must consult final artifact truth, and ambiguous origin probes should fail closed rather than create costly duplicate work.
- 2026-09-02 `ai-art-academy/t-077` — A gate-release answer from Silas via the Kind Robots "For You" mechanism unblocks the next agent to go verify -- it is not itself the verification. This task's note text ("temp outage, should be fixed") could have been closed on directly, but live GET /api/art/queue/stats and the character/bot API showed something the note didn't: the retry it asked for had already succeeded days earlier (portraits rendered 2026-08-28), and the failure signature it was filed over was itself a third recurrence of the same disk13-adjacent hardware fault (t-067/t-068 original, this task's own filing was recurrence #2, a third burst on 2026-09-01 caught only by this session's verification read). Filed ai-art-academy/t-078 as the standing fix: no check currently flags this specific recurring signature, so each occurrence has only ever been caught by an agent happening to read the stats endpoint while doing something else.
- 2026-09-02 `mandarin-tutor/t-020` — A production incident recovery task can sit at status: ready for days after the actual outage clears, if nothing re-checks it once Silas's "temporary outage, should be fixed" answer releases the gate -- the gate answer only unblocks the next agent to go verify, it doesn't verify anything itself. Recovery was confirmed here with tools that already existed (check_render_box.py, drain_failed_art_backlog.py's dry-run classification) -- no new code needed, just actually running them against current live state instead of trusting the multi-day-old note.
- 2026-09-02 `mandarin-tutor/t-010` — A dedicated read-only, media-origin HEAD-probe audit is worth writing even when a project already has "reach" tooling (queue_mandarin_tutor_art.py) that reports its own missing/staged counts -- that tooling's notion of "missing" is scoped to its own staging file (art-prompts.yaml), not to what actually rendered. Trusting it instead of probing the media origin directly would have hidden that "already staged: 0" no longer meant "nothing done" once the corpus's original request rows left the file. Re-running that same "reach" tool as a naive double-check (rather than the read-only audit) came within one command of re-staging an already-100%-rendered 577-card corpus as missing, which would have duplicate-submitted it against a host that just recovered from an outage -- filed as conductor/t-142. General lesson: a tool whose job is "make sure X is requested" is not a safe stand-in for auditing "is X actually done," even when it reports a count that looks like an audit.
- 2026-09-01 `model-builder/t-029` — Cycle 77: a new doc-comment's own prose can trip a regex-based static guard that scans for keywords without distinguishing code from comments -- verifyModelBuilder CompletionGate.ts's `\bawait\b`-based "find the function's first await" heuristic matched the bare word inside this cycle's own explanatory comment ("per-item-await loops"), shifting its notion of where real async work starts and flagging an unrelated pre-existing comment 20+ lines later as an ungated write. A regex-based guard against source text is exactly as blind to comments/strings as the pattern it's matching, so a new comment near guarded code should be checked against every such guard's actual matching logic, not just eyeballed for correctness.
- 2026-09-01 `interface-vision/t-104` — A recurring task's note: field narrated a merge and a "re-arming to ready" no-op cycle that its status: field never actually recorded -- the narrative outran the machine-readable state by at least one cycle before check_pr_merged_drift.py's merged-implementation_pr-vs-claimed-status check caught it. A cycle that intends to re-arm a recurring task should verify the status: field actually changed, not just that the note says it did.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-02T13:11:43Z_
