# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-27T21:26:49Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **388**
- Outcomes: blocked: 12, cancelled: 1, done: 375
- Success rate: **97%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 48 | 100% |
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
| digital-storefront | 24 | 100% |
| dream-cycle | 15 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 4 | 100% |
| kind-robots | 39 | 97% |
| kindrobots-unraid | 4 | 100% |
| media-watchlist | 6 | 100% |
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
| software | 373 | 99% |

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

- 2026-07-27 `ai-art-academy/t-047` — A kaizen task naming the exact fix (which consumers, which store method) still needs an investigation pass before editing -- checking whether the target genuinely never needs to survive a component's unmount (in-flight uploads, other readers) turned a plausible-looking one-liner into a verified-safe change across all 7 call sites in one pass.
- 2026-07-27 `media-watchlist/t-012` — Third cycle in a row on watchlist-browse.vue finding server-computed/validated data (month/season filters this time) that the UI never surfaced -- worth a full BROWSE-UX.md vs. UI audit rather than one gap per cycle.
- 2026-07-27 `digital-storefront/t-023` — A hard needs-human gate does not have to sit idle waiting for a scheduled Reviewer sweep -- Silas merged kind_robots PR #1056 directly within ~30 minutes of it opening. Treat a direct merge by the repo owner as the explicit clearance event itself (confirm via merged_by on the PR, not just merged: true, since an agent must never self-grant approved_by_human) rather than waiting for a separate roadmap-editing round from Silas -- close the loop (approved_by_human: true, status: done) in the same session once that signal is confirmed.
- 2026-07-27 `ai-art-academy/t-046` — A rearm-to-ready transition is not automatically symmetric with every other ready transition in the same processor -- the rearm branch of compute_transition_ops had cleared owner but not claimed_by/claimed_at, letting stale claim metadata survive an entire cycle. When adding a new status-transition branch to a shared state-machine function, diff its field clears against the other branches for the same target status rather than assuming symmetry; the regression test should assert clearance, not just the status value.
- 2026-07-27 `media-watchlist/t-006` — Third cycle in a row on this recurring polish task (2026-07-20, 2026-07-26, 2026-07-27) that found real server-side data already computed/accepted (CSV export filters, then Year+comics+TV-season stats) sitting unused because the front end never caught up. When touching a "polish the front end" task on a project whose backend predates the UI work, diff the API response/query-param shape against what the component actually renders/sends before assuming new backend scope is needed -- the gap is often pure wiring, which keeps the diff small and the pass clean.
- 2026-07-27 `ai-art-academy/t-019` — Once conductor PR #1215 fixed distribute_images.py and proved one thumbnail (greek-vase-painting) actually live in production, t-019's gate ("at least one queued image present") was satisfied immediately — but the task itself sat unclaimed for a cycle because nothing re-checked it after the fix. Wiring the single confirmed-live image and shipping a graceful per-style fallback (rather than waiting for all 33 curriculum thumbnails to exist) let real progress land now instead of blocking on t-035's much larger re-queue-and-regenerate batch.
- 2026-07-27 `ai-art-academy/t-010` — distribute_images.py silently ate the 33 previously-queued academy style-preview requests because kind_robots-targeted files get copied into a LOCAL kind_robots checkout (when one is present, which is the norm for agent sandboxes) even though kind_robots' /public/images/** is git-ignored and never actually reaches production that way -- then the "delivered" request gets pruned from art-prompts.yaml, destroying the only record that real delivery (via the relay's direct media path) still hadn't happened. Any pipeline step that "moves" a file into a target and then deletes the pending-work record on that basis must confirm the move is actually durable (git-tracked, or otherwise reachable in production) before treating it as done -- a local copy into a git-ignored directory is indistinguishable from success unless someone checks .gitignore.
- 2026-07-27 `ai-art-academy/t-042` — A kaizen task filed as "grep for other instances of this bug shape" can close clean with no code PR when the audit turns up nothing — closing done with the full per-file audit trail in the task note (files checked, patterns searched, why each slice(/splice(/Promise.all( hit was or was not the shape) is a complete deliverable on its own, matching the kind-robots/t-027 precedent (2026-07-16). Recording exactly what was searched and why each candidate was ruled out is what makes the negative result trustworthy enough that a future session does not need to re-run the same grep from scratch.
- 2026-07-27 `ai-art-academy/t-004` — Verifying a "wired but unverified" code path (t-037's LoraLoaderModelOnly node) against a real render, rather than trusting that it works because the graph compiles, surfaced a genuine production bug affecting every BUILTIN_STYLES LoRA remix, not just this task's registry candidates — worth budgeting one real end-to-end render per newly-wired-but-unverified node before building further work on top of it. The actionable half (LoRA loading itself) was correctly split into its own task (t-044) rather than blocking the task's actual deliverable (a recorded config per style), which shipped complete at mode: prompt for all 18 styles.
- 2026-07-27 `dream-cycle/t-018` — A "pull live data from the site API" task is safe to implement directly when the target endpoint is public and cheap to probe first (curl before coding) — confirming shape and reachability up front avoided over-designing the fetch helper. The reusable pattern: make the live source the default with a same-signature fallback (here, GENRE_FAMILIES) and never let the fetch failure mode (network, HTTP, bad JSON, empty body) propagate past a None return, so a scheduled sweep can never be blocked by an external API being down.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-27T21:26:49Z_
