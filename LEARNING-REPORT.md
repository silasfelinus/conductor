# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-15T15:39:46Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **611**
- Outcomes: blocked: 14, cancelled: 1, done: 596
- Success rate: **98%**
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
| humboldt-scoop-cms | 4 | 100% |
| interface-vision | 83 | 100% |
| kapowarr | 3 | 100% |
| kind-robots | 49 | 98% |
| kindrobots-unraid | 5 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 61 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 10 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 16 | 44% |
| software | 595 | 99% |

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

- 2026-08-15 `kapowarr/t-005` — A read-only clone plus targeted grep for -arr-convention keywords (notification, webhook, health check, import_list, calendar) across the whole fork found two genuine, scoped gaps (no notification system, no health-warnings panel) while also confirming several areas the roadmap notes didn't call out as already mature (queue reorder/blocklist, per-issue search, download-client test-connection, multi-root-folder support) -- recording the negative findings in the audit doc, not just the positive ones, keeps a future audit from re-flagging already-solved territory. Deliberately declined to turn every absent feature into a task (import lists, calendar) when the friction was speculative rather than concrete, per the task's own 'convert concrete friction, not broad rewrites' instruction.
- 2026-08-15 `kapowarr/t-006` — A read-only git clone of the target repo (public HTTPS, no auth, distinct from the session's GitHub MCP scope) let a design-only task ground its spec in the actual ABC/class chain instead of the task note's abstractions -- found that TorrentDownload.update_status() already polls purely through the ExternalDownloadClient interface with zero torrent-specific logic, so a Usenet client is a peer implementation, not a new mechanism, and located the one real shared touchpoint (download_queue.py's TorrentDownload-specific isinstance dispatch) that does need to change. Worth doing before writing any cross-repo design/handoff doc: reading the real code turns a plausible design into a verified one and surfaces the one non-obvious shared edge a task note alone won't mention.
- 2026-08-15 `kapowarr/t-001` — For a brand-new project's first task (a design brief with no existing repo context in this session's GitHub scope), WebFetch against the public upstream and fork repos/docs grounded the architecture section in the project's real download-client model (built-in DDL vs. external clients) instead of guessing from the task notes alone -- worth doing for any design-brief task on a project this session hasn't touched before, especially when the target codebase itself is outside the session's repo scope.
- 2026-08-15 `davinci/t-024` — When a 'playtest-driven tuning' task can't be done literally (sandbox has no live-user auth against the app's OpenAI-backed endpoint), a Monte Carlo simulation against the actual production constants and distribution answers the same design question more rigorously than a handful of manual runs -- and can overturn the obvious hypothesis: the flagged +-2 swing bound turned out not to matter at all (any single nonzero touch already crosses the pass=1 threshold regardless of magnitude), while the real, unflagged lever was chapter-count coverage (avg 4.2/10 dimensions never touched by the original 3-chapter minimum). Simulate before tuning the constant that looks obviously guilty.
- 2026-08-15 `conductor-app/t-015` — When a task offers wire-or-drop for dead config fields, check whether the wire target already has a canonical source elsewhere (utils/projectPlacements.ts here) before adding new UI plumbing -- dropping the redundant copy removes the whole stale-duplicate bug class with a purely mechanical, zero-risk diff, where wiring would have added an unverified UI surface. Also: grep scope for a drift audit should match the actual usage pattern (ProjectFrontConfig), not a directory convention (components/conductor/*) -- coloring-book-page.vue lived outside that directory and would have been missed.
- 2026-08-15 `storybook/t-021` — A kaizen guard task from a hand-fixed field-drop bug (t-010's scenario fix) should assert the general shape (every input.<field> a builder reads must survive a rebuild helper) rather than re-checking the one field that broke -- caught the same bug class generically instead of only re-guarding scenario.
- 2026-08-14 `conductor-app/t-013` — A task's checklist can silently finish itself via unrelated cycles (art relay draining, an admin Placements backfill) between sessions -- re-verify each open step against live state before assuming a 3-week-old gap still holds; two of this task's three flagged blockers had already resolved themselves.
- 2026-08-14 `model-builder/t-044` — Kaizen from t-029 (PR #1882): before writing a coverage guard for "the async-fetch staleness pattern," actually read every performFetch call site first rather than assuming the two known-fixed functions' exact ticket-counter shape generalizes. It doesn't: modelBuilderStore.ts uses six independently-correct staleness idioms (ticket-counter, capture-compare, cancelled-run-check, identity-check, serialized-lock, write-only) depending on what each function does with the response. A guard that blindly demanded the ticket shape everywhere would have false-flagged ~8 already-correct, already-audited functions. The shippable design was a registry-driven coverage check (verifyModelBuilderAsyncFetchStalenessCoverage.ts, kind_robots#1884): every performFetch( call site must be classified in an explicit registry with a spot-checked marker, so a genuinely NEW unaudited call site fails CI, without re-litigating already-solved cases.
- 2026-08-14 `conductor/t-117` — Doc-only kaizen closing a twice-repeated security-flag (TALKBACK.md 2026-08-13, 2026-08-14): a non-isolated background Agent doing git-mutating work in a repo a foreground session is still actively using can silently discard the foreground's uncommitted edits or delete its designated branch (with any unpushed commits on it). Promoted from documented-but-skippable CLAUDE.md prose to AGENTS.md hard rule 12: isolation:'worktree' is required for any background Agent mutating git state in a repo the foreground session is concurrently using, not only for the narrower "in-flight workaround" case rule 11 already covered.
- 2026-08-14 `model-builder/t-029` — Fifth t-029 cycle found a genuinely new bug shape, not another instance of the unawaited-call pattern t-042's confirmedOutcomeGuard meta-guard already covers: recordArtifact() DID await its performFetch() call, but performFetch never rejects for an HTTP-level failure (it always resolves with { success: false }), so recordArtifact's try/catch around that await was silently dead code -- any failure was discarded with no .success check anywhere, no error surfaced, and the caller still popped a success toast and marked the stage ready regardless. The existing meta-guard only flags a BARE (non-awaited) call to a Promise- returning helper before a success toast; it has no way to see that an awaited callee's own internals swallow their result. Worth widening t-042's guard (or adding a sibling one) to also flag any store function whose body awaits performFetch inside a try/catch with no `.success` check anywhere in scope -- the same "silently-dead catch block" shape likely recurs elsewhere in this store (and possibly other Pinia stores) wherever performFetch's always-resolve contract isn't the author's first assumption. Filed as this cycle's kaizen suggestion rather than a new task, since the fix (widen an existing guard) is speculative until a second instance is found.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-15T15:39:46Z_
