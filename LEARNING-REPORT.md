# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-27T14:10:52Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **383**
- Outcomes: blocked: 12, cancelled: 1, done: 370
- Success rate: **97%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 46 | 100% |
| alexa-integration | 2 | 100% |
| animation-manager | 11 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 5 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 14 | 100% |
| conductor | 53 | 100% |
| conductor-app | 2 | 100% |
| davinci | 1 | 100% |
| digital-storefront | 23 | 100% |
| dream-cycle | 15 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 4 | 100% |
| kind-robots | 39 | 97% |
| kindrobots-unraid | 4 | 100% |
| media-watchlist | 4 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 32 | 100% |
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

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 368 | 99% |

## Failure categories

| Category | Count |
|---|---|
| actionable | 8 |
| quality | 7 |
| transient | 5 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `actionable` — 8 occurrences; look for the shared cause across its records
- failure category `quality` — 7 occurrences; look for the shared cause across its records
- failure category `transient` — 5 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-07-27 `ai-art-academy/t-019` — Once conductor PR #1215 fixed distribute_images.py and proved one thumbnail (greek-vase-painting) actually live in production, t-019's gate ("at least one queued image present") was satisfied immediately — but the task itself sat unclaimed for a cycle because nothing re-checked it after the fix. Wiring the single confirmed-live image and shipping a graceful per-style fallback (rather than waiting for all 33 curriculum thumbnails to exist) let real progress land now instead of blocking on t-035's much larger re-queue-and-regenerate batch.
- 2026-07-27 `ai-art-academy/t-010` — distribute_images.py silently ate the 33 previously-queued academy style-preview requests because kind_robots-targeted files get copied into a LOCAL kind_robots checkout (when one is present, which is the norm for agent sandboxes) even though kind_robots' /public/images/** is git-ignored and never actually reaches production that way -- then the "delivered" request gets pruned from art-prompts.yaml, destroying the only record that real delivery (via the relay's direct media path) still hadn't happened. Any pipeline step that "moves" a file into a target and then deletes the pending-work record on that basis must confirm the move is actually durable (git-tracked, or otherwise reachable in production) before treating it as done -- a local copy into a git-ignored directory is indistinguishable from success unless someone checks .gitignore.
- 2026-07-27 `ai-art-academy/t-042` — A kaizen task filed as "grep for other instances of this bug shape" can close clean with no code PR when the audit turns up nothing — closing done with the full per-file audit trail in the task note (files checked, patterns searched, why each slice(/splice(/Promise.all( hit was or was not the shape) is a complete deliverable on its own, matching the kind-robots/t-027 precedent (2026-07-16). Recording exactly what was searched and why each candidate was ruled out is what makes the negative result trustworthy enough that a future session does not need to re-run the same grep from scratch.
- 2026-07-27 `ai-art-academy/t-004` — Verifying a "wired but unverified" code path (t-037's LoraLoaderModelOnly node) against a real render, rather than trusting that it works because the graph compiles, surfaced a genuine production bug affecting every BUILTIN_STYLES LoRA remix, not just this task's registry candidates — worth budgeting one real end-to-end render per newly-wired-but-unverified node before building further work on top of it. The actionable half (LoRA loading itself) was correctly split into its own task (t-044) rather than blocking the task's actual deliverable (a recorded config per style), which shipped complete at mode: prompt for all 18 styles.
- 2026-07-27 `dream-cycle/t-018` — A "pull live data from the site API" task is safe to implement directly when the target endpoint is public and cheap to probe first (curl before coding) — confirming shape and reachability up front avoided over-designing the fetch helper. The reusable pattern: make the live source the default with a same-signature fallback (here, GENRE_FAMILIES) and never let the fetch failure mode (network, HTTP, bad JSON, empty body) propagate past a None return, so a scheduled sweep can never be blocked by an external API being down.
- 2026-07-27 `ai-art-academy/t-009` — A "generate via the auto art pipeline" task can silently have no pipeline at all for its art-prompts.yaml section (the inspirations list had no consumer script, unlike the images/requests ones) — when a task assumes automation exists, verify a consumer actually reads that YAML key before trusting a "still pending" status as just a backlog problem. Separately, verify generated art landed on the real serving path (HEAD the public media URL), not just that the job returned success — the plain ArtJob response only writes a DB row plus a gitignored local checkout copy; only the direct-media payload fields make the relay write to production.
- 2026-07-27 `mona-salai/t-001` — Historical-identity experiments need the documentary baseline, candidate-attribution uncertainty, same-artist controls, and explicit falsification criteria fixed before computational scores are viewed; otherwise a model can turn style recurrence and selection bias into false certainty.
- 2026-07-27 `music-mentor/t-007` — Implementing YIN alongside the incumbent autocorrelation tracker and measuring both with a synthetic accuracy suite (not just trusting the textbook octave-error argument) surfaced a different real advantage than expected -- low-register voiced-detection rate, not octave-error count, which were tied at zero for both. For "evaluate X vs Y" tasks, build the comparison harness and report the measured mechanism, not the assumed one.

- 2026-07-27 `humboldt-scoop-cms/t-009` — For a portable field client, keep route data, persistence, and navigation handoff behind interfaces; boot with dummy data so UI work stays safe before real-address privacy and rollout gates are cleared.
- 2026-07-27 `conductor/t-086` — A stale task-event that carries a learning/note payload used to vanish silently when process_task_events.py's stale_reason() dropped it -- the only trace was a terse STALE skip line easy to miss in a run's stdout. Added a visible WARNING to stderr specifically when the dropped event has non-empty learning/note, and closed the other half of the gap in AGENTS.md: before hand-writing a task's status: done transition, check task-events/ for an already-queued completion event for the same project/task first, rather than racing it blind.


---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-27T14:10:52Z_
