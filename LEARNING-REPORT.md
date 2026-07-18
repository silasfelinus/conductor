# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-18T14:23:13Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **264**
- Outcomes: blocked: 12, done: 252
- Success rate: **95%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 28 | 100% |
| alexa-integration | 2 | 100% |
| animation-manager | 5 | 100% |
| animation-studio | 1 | 100% |
| appmaker | 2 | 100% |
| approval-portal | 2 | 0% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 13 | 100% |
| conductor | 36 | 100% |
| digital-storefront | 12 | 100% |
| dream-cycle | 14 | 100% |
| ecosystem-map | 4 | 100% |
| global-ui | 11 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 1 | 100% |
| kind-robots | 26 | 96% |
| kindrobots-unraid | 4 | 100% |
| media-watchlist | 1 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 28 | 100% |
| mural-design | 1 | 100% |
| newsfeed | 4 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 2 | 100% |
| serendipity | 1 | 100% |
| superkate-hairstyle-ai | 16 | 100% |
| superkate-services-calculator | 11 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 249 | 99% |

## Failure categories

| Category | Count |
|---|---|
| actionable | 6 |
| quality | 5 |
| transient | 1 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `actionable` — 6 occurrences; look for the shared cause across its records
- failure category `quality` — 5 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-07-18 `newsfeed/t-005` — The task note pointed at prs.get.ts's raw-array response shape as the model to follow, but that's a rare conductor-only outlier -- 110+ of this repo's other GET routes use a {success,message,data}+errorHandler convention instead. When a task note says 'model X on Y's shape,' check how common Y's specific pattern actually is across the codebase before copying it verbatim; the intended lesson (thin handler + shared util split, introduce caching) can be separable from the literal response contract.
- 2026-07-18 `digital-storefront/t-017` — A design-only task (no PR, per BOUNDARY.md) with follow-on tasks already filed (t-026, kind-robots/t-037) still needs an explicit status: done close -- the design doc landing on main and the follow-ons existing isn't itself a completion signal a later session will notice without checking. Same pattern as global-ui/t-025 this cycle: two independent status: review tasks both had their actual output already merged/landed, just missing the roadmap close.
- 2026-07-18 `global-ui/t-025` — kind_robots PR #420 merged cleanly (option (a): migrate both shadow-variant panels onto kr-panel/kr-panel-muted with the shadow layered as a template utility override) but the roadmap task sat at status: review for several hours/cycles with no session flipping it to done -- closing a task the Worker/Reviewer already merged is easy to defer past the same session. Check pull_request_read on any status: review task's referenced PR before picking new work; a merged PR with no roadmap follow-through is a same-session-fixable gap, not a needs-human one.
- 2026-07-18 `ai-art-academy/t-032` — art-styler.vue's generated emit carried only the result image, not which style produced it, so the consumer had to re-read current store state to attribute a completed generation -- exactly the kind of async gap where a mid-flight selection change mis-attributes the result. When an event fires after an awaited async call, pass the value that was true at request-start through the event payload itself rather than letting the consumer re-read live state after the fact.
- 2026-07-18 `newsfeed/t-003` — Relocating a component off a route can leave stale duplicate frontmatter behind on an unrelated nav/breadcrumb metadata file that shares the same route (content/channels/home/dashboard.md's dashboardKey/dashboardTab, separate from the actual page file content/index.md). Grep every content file that shares the target route, not just the one being edited, before calling a relocation complete.
- 2026-07-18 `animation-manager/t-010` — The task note called bubble-effect.vue 'orphaned/never registered' but it was actually already wired into animation-loader.vue's effectMap -- just missing from animationCatalog.ts, the catalog that actually gates which ids animationStore can select. Read both the consuming component AND the catalog before assuming a component is dead code; a component can be fully wired downstream and still be unreachable because its id never appears upstream.
- 2026-07-18 `conductor/t-053` — A recurring PR-template gap (missing Kaizen suggestion section) was only ever caught by a Reviewer noticing by hand, three times in one week. A tiny, network-free text check the Reviewer runs on content it already has (scripts/check_pr_kaizen.py) closes that gap cheaper than touching a second repo's CI config -- prefer the same-repo, no-new-dependency option when a task offers a choice of implementation paths.
- 2026-07-18 `conductor/t-049` — Static frontend fallback data (conductorCards.ts) drifts silently from the roadmap/project-overrides.yaml source of truth over time -- 9 of 22 cards had stale kind/status/tagline fields with no error surfaced anywhere, since the fallback only renders when the live DB API is unavailable. A periodic drift audit (this task) is the only thing that catches it; consider making it recurring rather than one-off.
- 2026-07-18 `digital-storefront/t-017` — A design task blocked on two cross-project note-level dependencies (invisible to resolve_deps.py/claim_task.py, which only check in-project depends_on) should re-verify each blocker's live status directly before claiming, per CONTROL.md's cross-project-collision note -- both packmaker/t-003 and kind-robots/t-008 were genuinely done here, but the task's own note explicitly warned not to trust the resolver's blind promotion.
- 2026-07-18 `conductor/t-055` — yaml.safe_dump round-tripping a human-edited YAML file silently strips every comment and blank-line separator on write -- any registration/patch helper that touches a file agents don't exclusively own (priority.yaml, project-overrides.yaml) should do targeted text-surgery (regex/line insertion, mirroring register_control_block) instead of load-mutate-dump, even when the mutation itself is a one-line append.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-18T14:23:13Z_
