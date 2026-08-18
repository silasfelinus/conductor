# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-18T11:28:56Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **672**
- Outcomes: blocked: 15, cancelled: 1, done: 656
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
| kapowarr | 27 | 100% |
| kind-robots | 50 | 98% |
| kindrobots-unraid | 5 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 68 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 12 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 6 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 16 | 44% |
| software | 656 | 99% |

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

- 2026-08-18 `humboldt-scoop-cms/t-039` — For a task framed as "a real design question, not just a UI addition," resolve the architecture before delegating -- here that meant confirming the CMS and WordPress plugin share one physical database (not a network integration) and that only the WordPress side can send mail, then pointing the delegate at HSS_Notify's existing shared-table/wp-cron-sweep precedent instead of letting it invent a new synchronous cross-service call or a third-party email dependency. A fully-specified design (table/column names, transactional claim-to-token, generic-response account-enumeration guard, custom short cron interval, plaintext-nulled-atomically-with-send) produced a clean single-pass implementation with no security-relevant rework needed on review.
- 2026-08-18 `humboldt-scoop-cms/t-026` — A stakes:outward-facing task ("Finish Android production beta and Play Store readiness") still has a real, bounded, mergeable software slice inside it -- release-signing scaffold, permissions/endpoint audit (which caught a genuine bug, a missing INTERNET permission in the release manifest), crash logging, and drafted store/privacy docs -- even though the task as a whole can never reach done without Silas's accounts/keys/URLs. Splitting "what's mechanically buildable" from "what only a human with real-world credentials can do" and shipping the former as a merged PR, with the latter as a numbered checklist in the needs-human note, gets real progress landed instead of parking the whole task untouched until Silas has time to do everything himself.
- 2026-08-18 `humboldt-scoop-cms/t-036` — When a task explicitly says "revisit deliberately rather than assuming X belongs here," do the architecture investigation (grep the actual endpoints/write paths) in the foreground before delegating implementation -- handing an under-scoped judgment call to a background agent blind risks it either over-building (a mobile route planner nobody asked to keep) or under-building (skipping a genuinely useful feature). Concrete evidence handed to the delegate (exact file/line patterns to mirror) produced a clean single-pass implementation with no scope drift on either the declined half (route planning) or the built half (customer edit).
- 2026-08-18 `humboldt-scoop-cms/t-035` — A same-day sibling session (t-037 close-out, same rotation) had already read t-035's own self-gating note ("only worth doing once/if a second widget is proposed") and deliberately skipped it -- I claimed and implemented it anyway without first grepping today's TALKBACK/LEARNING.yaml for a prior skip decision on this exact task id, relying only on the roadmap note itself. The work was small, reversible, and harmless (kept merged rather than reverted), but the real gap is that a "ready but conditionally not-yet" task has no roadmap status that actually encodes that, so two same-day sessions made different individually-reasonable calls on the same task.
- 2026-08-18 `humboldt-scoop-cms/t-037` — Before picking the file-order-next ready task, read its note for a self-gating condition ("only worth doing once X is proposed") and check whether that condition actually holds -- t-035 gated on a second cross-host widget that doesn't exist yet, so it was correctly skipped in favor of t-037, one of t-025's real deferred follow-ups with a concrete existing pattern (HSS_Staff_Tokens) to mirror.
- 2026-08-18 `humboldt-scoop-cms/t-024` — Mirroring an existing durable-queue pattern in the same codebase (FilePhotoUploadQueue from t-023) made a genuinely large offline-durability feature (route cache + write queue + reconcile-on-fetch) tractable in one pass without changing the RouteApi/RouteStorage interfaces the task asked to preserve; also fixed a real latent bug found along the way (RouteStop.fromJson silently dropping crewNotes) that would have made cached completions lose their notes on app restart.
- 2026-08-18 `kapowarr/t-028` — Portable comic lists should preserve unresolved gaps and enrich source identity when local matching provides stronger IDs; acquisition should be an explicit action over resolved missing entries.
- 2026-08-18 `kapowarr/t-046` — Documented the content-API push workaround's stale-base risk (AGENT_WORKFLOW_NOTES.md, Kapowarr#43) — any agent forced to push via create_branch+push_files instead of git push must re-fetch each touched file's live content immediately before writing, and reviewing sessions must diff the actual PR file list against main before merging rather than trusting green CI alone.
- 2026-08-18 `kapowarr/t-031` — Preserve mature post-processing contracts where possible; test seed-safety behavior directly and keep range metadata optional on legacy download paths.
- 2026-08-18 `kapowarr/t-027` — A background agent pushing via the GitHub content API (create_branch/push_files) instead of git, because sandbox isolation blocks git-mutating ops against a shared checkout, works from a point-in-time file snapshot with no non-fast-forward safety net -- if a concurrent PR merges a change to a file it also touches, its push can silently revert that change. Neither isolated-copy tests nor CI caught it here (an import-only removal with no direct test coverage). Reviewing sessions merging such a PR must diff every touched file against live main, not just trust green CI.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-18T11:28:56Z_
