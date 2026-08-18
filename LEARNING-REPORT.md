# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-18T14:35:26Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **675**
- Outcomes: blocked: 15, cancelled: 1, done: 659
- Success rate: **98%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 64 | 98% |
| alexa-integration | 5 | 100% |
| animation-manager | 13 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 7 | 100% |
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
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 83 | 100% |
| kapowarr | 28 | 100% |
| kind-robots | 50 | 98% |
| kindrobots-unraid | 5 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 69 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 13 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 6 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 16 | 44% |
| software | 659 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 14 |
| actionable | 9 |
| transient | 9 |
| scope | 2 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 14 occurrences; look for the shared cause across its records
- failure category `actionable` — 9 occurrences; look for the shared cause across its records
- failure category `transient` — 9 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-18 `storybook/t-010` — isolation:'worktree' stops a background agent from colliding on shared LOCAL git state, but does nothing to stop it from colliding with a dispatching session that starts fixing the SAME remote PR directly (e.g. after the agent's final report looked stuck/garbled) -- both sides independently diagnosed and fixed the identical CI failure and both called merge; GitHub's idempotent merge meant no harm this time, but a session should stop the agent or wait for its real completion before touching a PR it's still delegated, not race it.
- 2026-08-18 `model-builder/t-029` — A background agent that spawns its own Monitor and then reports back only "still waiting on it" (never a real final summary) is a distinct failure mode from prior background-agent guidance -- don't wait on it indefinitely; check GitHub directly (PR/branch/CI state) the same way you'd verify any other agent's self-report, since the agent's actual work product (the PR) can be sound even when its wrap-up communication isn't.
- 2026-08-18 `kapowarr/t-033` — A claim past CLAIM_TTL_MINUTES isn't automatically scratch work -- read the stale branch's actual diff before reclaiming; a small-but-sound partial scaffold (this one: a backend query + route registration, no UI/tests yet) is worth resuming on top of, not discarding and reimplementing from zero.
- 2026-08-18 `humboldt-scoop-cms/t-039` — For a task framed as "a real design question, not just a UI addition," resolve the architecture before delegating -- here that meant confirming the CMS and WordPress plugin share one physical database (not a network integration) and that only the WordPress side can send mail, then pointing the delegate at HSS_Notify's existing shared-table/wp-cron-sweep precedent instead of letting it invent a new synchronous cross-service call or a third-party email dependency. A fully-specified design (table/column names, transactional claim-to-token, generic-response account-enumeration guard, custom short cron interval, plaintext-nulled-atomically-with-send) produced a clean single-pass implementation with no security-relevant rework needed on review.
- 2026-08-18 `humboldt-scoop-cms/t-026` — A stakes:outward-facing task ("Finish Android production beta and Play Store readiness") still has a real, bounded, mergeable software slice inside it -- release-signing scaffold, permissions/endpoint audit (which caught a genuine bug, a missing INTERNET permission in the release manifest), crash logging, and drafted store/privacy docs -- even though the task as a whole can never reach done without Silas's accounts/keys/URLs. Splitting "what's mechanically buildable" from "what only a human with real-world credentials can do" and shipping the former as a merged PR, with the latter as a numbered checklist in the needs-human note, gets real progress landed instead of parking the whole task untouched until Silas has time to do everything himself.
- 2026-08-18 `humboldt-scoop-cms/t-036` — When a task explicitly says "revisit deliberately rather than assuming X belongs here," do the architecture investigation (grep the actual endpoints/write paths) in the foreground before delegating implementation -- handing an under-scoped judgment call to a background agent blind risks it either over-building (a mobile route planner nobody asked to keep) or under-building (skipping a genuinely useful feature). Concrete evidence handed to the delegate (exact file/line patterns to mirror) produced a clean single-pass implementation with no scope drift on either the declined half (route planning) or the built half (customer edit).
- 2026-08-18 `humboldt-scoop-cms/t-035` — A same-day sibling session (t-037 close-out, same rotation) had already read t-035's own self-gating note ("only worth doing once/if a second widget is proposed") and deliberately skipped it -- I claimed and implemented it anyway without first grepping today's TALKBACK/LEARNING.yaml for a prior skip decision on this exact task id, relying only on the roadmap note itself. The work was small, reversible, and harmless (kept merged rather than reverted), but the real gap is that a "ready but conditionally not-yet" task has no roadmap status that actually encodes that, so two same-day sessions made different individually-reasonable calls on the same task.
- 2026-08-18 `humboldt-scoop-cms/t-037` — Before picking the file-order-next ready task, read its note for a self-gating condition ("only worth doing once X is proposed") and check whether that condition actually holds -- t-035 gated on a second cross-host widget that doesn't exist yet, so it was correctly skipped in favor of t-037, one of t-025's real deferred follow-ups with a concrete existing pattern (HSS_Staff_Tokens) to mirror.
- 2026-08-18 `humboldt-scoop-cms/t-024` — Mirroring an existing durable-queue pattern in the same codebase (FilePhotoUploadQueue from t-023) made a genuinely large offline-durability feature (route cache + write queue + reconcile-on-fetch) tractable in one pass without changing the RouteApi/RouteStorage interfaces the task asked to preserve; also fixed a real latent bug found along the way (RouteStop.fromJson silently dropping crewNotes) that would have made cached completions lose their notes on app restart.
- 2026-08-18 `kapowarr/t-028` — Portable comic lists should preserve unresolved gaps and enrich source identity when local matching provides stronger IDs; acquisition should be an explicit action over resolved missing entries.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-18T14:35:26Z_
