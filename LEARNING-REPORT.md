# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-28T14:27:49Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **404**
- Outcomes: blocked: 13, cancelled: 1, done: 390
- Success rate: **97%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 52 | 98% |
| alexa-integration | 2 | 100% |
| animation-manager | 12 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 5 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 19 | 100% |
| conductor | 55 | 100% |
| conductor-app | 2 | 100% |
| davinci | 1 | 100% |
| digital-storefront | 24 | 100% |
| dream-cycle | 16 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 4 | 100% |
| kind-robots | 39 | 97% |
| kindrobots-unraid | 4 | 100% |
| media-watchlist | 7 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 34 | 100% |
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
| software | 389 | 99% |

## Failure categories

| Category | Count |
|---|---|
| actionable | 8 |
| quality | 7 |
| transient | 6 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `actionable` — 8 occurrences; look for the shared cause across its records
- failure category `quality` — 7 occurrences; look for the shared cause across its records
- failure category `transient` — 6 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-07-28 `ai-art-academy/t-044` — A prior cycle read kind_robots PR #1090 optimistically ("architecturally exactly the fix," "strongly suggests Silas... corrected the underlying data/path mismatch") from the diff alone, then correctly flagged it unverified and left the task ready. This cycle had a live path to verify (KR_API_TOKEN + the public kind-robots.vercel.app API) and used it instead of re-reading the diff again: two real POST /api/art/enqueue jobs against two independent LoRA Resources under different localPath prefix conventions both failed with the exact same ComfyUI value_not_in_list error as before the PR. The PR fixed routing (the resolver now reliably forwards the Resource's own localPath) but never touched the underlying DB data, which still does not match ComfyUI's real lora_name dropdown. Lesson: when a fix's own diff looks architecturally right but the task explicitly says "not independently verified," a session with any live-testable surface should spend the few extra minutes to actually call it rather than propagating the optimistic read forward another cycle -- production API tokens set as env vars (KR_API_TOKEN here) are a real, underused verification channel for tasks that look relay-blocked but are only blocked for browser-based /object_info access, not for server-side API calls the KR backend itself proxies to the relay.
- 2026-07-28 `coloring-book/t-032` — A live recovery pass that reuses an already-completed ArtJob can still silently destroy its own recoverability: when validate_candidate() fails for an environment reason (missing ANTHROPIC_API_KEY) rather than a real image judgment, overwriting the entry's error text erases the "job N timed out" reference a future recovery pass parses to find the same completed job -- converting a genuinely recoverable entry into one that looks like it needs a brand-new (duplicate) submission. Distinguish environment/tooling failures from real semantic verdicts before writing to any field a recovery mechanism depends on.
- 2026-07-28 `coloring-book/t-033` — Second same-day coloring-book PR (after t-022) merged with no roadmap task claimed beforehand -- both were only discoverable via mcp__github__list_pull_requests, not roadmap state. Retroactively logging the task after merge keeps the audit trail intact but does not fix the root habit; worth enforcing claim-before-implement if a third instance appears in this project.
- 2026-07-28 `model-builder/t-033` — When a picker/config restriction should mirror a relation graph (here: which source types may create which related model), trace the actual linked-pair cases in the commit/link handler rather than the coarser raw schema-relation check alone -- two output keys can target the same model through different fields (Project.managerBotId vs Dream.narratorId), which a schema-relation-only check cannot distinguish. The fix also surfaced a pre-existing gap (Facet listed as recipe-eligible with zero real link cases) that was silently broken before and is now visibly empty instead -- filed as a separate kaizen task rather than silently expanding scope.
- 2026-07-28 `coloring-book/t-022` — Path-safety logic duplicated at both the event-intake layer and the executing script (process_coloring_art_events.py and adopt_coloring_book_asset.py both re-validate source_path independently) is a defense-in-depth pattern worth reusing for other event-driven scripts that accept a filesystem path from an external event file.
- 2026-07-28 `media-watchlist/t-013` — Fifth consecutive media-watchlist stats-wiring task (t-006, t-010, t-012, t-013) finding server data already computed and needing only front-end wiring -- confirming the premise (grep the API route) before writing UI code keeps these cycles fast and single-pass.
- 2026-07-28 `animation-manager/t-015` — Small, well-scoped asset-plus-one-line-swap PRs (new icon + catalog reference + regenerated seed file) verify fast and merge clean when the implementer confirms the regenerated file came straight from the existing generator script rather than a hand edit -- worth keeping as the template for future one-off icon/asset requests.
- 2026-07-28 `model-builder/t-032` — A structural dev-time check (walk CREATE_TARGETS x the Prisma relation graph, assert linkSourceToTarget has a matching case) immediately caught a real gap (Reward -> Character) the same day it was written -- two prior gaps of this exact shape (Dream->Bot, Character->Scenario) had only ever surfaced via manual read-through across separate cycles. Where a hand-maintained mapping mirrors a second source of truth (here: Prisma relations), prefer a structural consistency check over relying on the next manual audit to catch drift.
- 2026-07-28 `ai-art-academy/t-010` — Running claim_task.py only after implementing (instead of before, per AGENTS.md step 6) turns the claim check into a post-hoc formality instead of a reservation — this session duplicated another session's identical lane-4 sync work and had to close its own kind_robots PR as superseded. Claim first, implement second, every time, even when the task looks unclaimed at a glance.
- 2026-07-28 `conductor/t-088` — A well-templated connector-only Worker PR (What changed/How I verified/Flags/Kaizen all filled in specifically) needs no manual roadmap close-out — the task-events auto-processor flipped this task to done within the same minute the merge landed.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-28T14:27:49Z_
