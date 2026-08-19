# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-19T06:44:45Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **689**
- Outcomes: blocked: 15, cancelled: 1, done: 673
- Success rate: **98%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 64 | 98% |
| alexa-integration | 6 | 100% |
| animation-manager | 13 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 8 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| brainstorm | 15 | 93% |
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
| kapowarr | 35 | 100% |
| kind-economy | 1 | 100% |
| kind-robots | 50 | 98% |
| kindrobots-unraid | 5 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 70 | 100% |
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
| software | 673 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 14 |
| actionable | 10 |
| transient | 9 |
| scope | 2 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 14 occurrences; look for the shared cause across its records
- failure category `actionable` — 10 occurrences; look for the shared cause across its records
- failure category `transient` — 9 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-19 `kind-economy/t-004` — When a live claim on the site outpaces the mechanism behind it, "future tense" is nearly always the right default over "leave it and document the gap" -- it costs nothing, is fully reversible, and removes a live credibility risk immediately. Also: a CI job stuck `queued` with the parent run auto-concluding `failure` (no logs, zero jobs actually run) is a transient infra stall, not a real check failure -- confirm by running the same commands locally before trusting the red state, then retry the workflow run to verify before merging.

- 2026-08-19 `kapowarr/t-038` — A provider abstraction does not by itself remove a legacy provider monopoly: database NOT NULL columns and Add-form assumptions remain product boundaries. Metron fallback was therefore shipped through its explicit ComicVine cross-links with durable Metron provenance, while native-only records were withheld from a knowingly broken Add path. Also, never follow an authenticated API's pagination URL verbatim; reconstruct the next page on the configured origin so credentials cannot cross an origin boundary.

- 2026-08-19 `kapowarr/t-055` — Human-triggered bulk operations should preserve successes and return item-level failures; background jobs can keep strict exception semantics for checkpointed retries.
- 2026-08-19 `kapowarr/t-037` — Separate stable external identity from provider credentials and UI policy; additive maps let alternate metadata coexist without destabilizing legacy libraries.
- 2026-08-19 `kapowarr/t-054` — Bound remote metadata resolution as a whole and pair every loading state with success and rejection exits; source health data should be visible before acquisition.
- 2026-08-19 `model-builder/t-029` — Twelfth cycle of this recurring bug-hunt task. The suggested accessibility lead from cycle 11 was genuinely exhausted (both target components already covered or not applicable), and the fallback -- read a genuinely fresh file (the store) rather than re-walking already-audited components -- surfaced a real sibling instance of a bug class an existing guard already covered for other functions (verifyModelBuilderAutoBuildFailedSummaryGuard's TARGET_FUNCTIONS list). When a guard is written against an explicit function allowlist, a later cycle should periodically check whether new or overlooked functions with the same shape are missing from that list, rather than assuming a fixed guard covers a whole bug class permanently.

- 2026-08-19 `kapowarr/t-036` — check_pr_merged_drift.py's gh-search fallback 403'd in this sandbox, but the GitHub MCP pull_request_read "get" method (as opposed to list_pull_requests, which reported merged:false for the same closed PR) confirmed silasfelinus/Kapowarr#56 was in fact merged directly by Silas. When the drift script can't verify a candidate via its own HTTP path, cross-check the single-PR MCP get method before treating it as unresolved -- the list endpoint's merged field is not reliable evidence on its own. Concurrent race note: by the time this reconciliation PR reached CI, origin/main had already picked up the same task's real close-out (with the full implementation note and squash SHA) from another session -- resolved by keeping origin/main's roadmap content and both LEARNING.yaml entries side by side rather than picking one.

- 2026-08-19 `kapowarr/t-036` — When matching release issue numbers, verify the exported helper name rather than trusting its stale docstring example; the dependency-backed import matrix catches this immediately.
- 2026-08-18 `kapowarr/t-047` — Scheduled tasks must record failure outcomes before leaving the queue, and scraped sources require live markup verification.
- 2026-08-18 `brainstorm/t-018` — A persona-recovery task with an open-ended "add flavor" instruction doesn't require inventing anything -- audit the live database first. The real, already-generated Brainbot Bot record (art, tagline, voice) sitting unused was a stronger fit than restoring a legacy gitignored asset or a stale seed-script record that never populated production. When multiple candidate sources of truth exist (a seed file, a content .md, a live DB record), the live DB record wins if it actually satisfies the ask -- verify what's live via the site's own API rather than trusting the most convenient-looking file in the repo.


---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-19T06:44:45Z_
