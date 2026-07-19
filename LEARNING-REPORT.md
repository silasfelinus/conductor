# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-19T16:21:31Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **295**
- Outcomes: blocked: 12, done: 283
- Success rate: **96%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 32 | 100% |
| alexa-integration | 2 | 100% |
| animation-manager | 6 | 100% |
| animation-studio | 1 | 100% |
| appmaker | 2 | 100% |
| approval-portal | 2 | 0% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 13 | 100% |
| conductor | 40 | 100% |
| digital-storefront | 12 | 100% |
| dream-cycle | 14 | 100% |
| ecosystem-map | 4 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 1 | 100% |
| kind-robots | 29 | 97% |
| kindrobots-unraid | 4 | 100% |
| media-watchlist | 1 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 29 | 100% |
| mural-design | 1 | 100% |
| newsfeed | 16 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 2 | 100% |
| serendipity | 3 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 11 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 280 | 99% |

## Failure categories

| Category | Count |
|---|---|
| actionable | 6 |
| quality | 5 |
| transient | 3 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `actionable` — 6 occurrences; look for the shared cause across its records
- failure category `quality` — 5 occurrences; look for the shared cause across its records
- failure category `transient` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-07-19 `newsfeed/t-019` — When a task offers an explicit design choice (single multi-route channel vs. per-tab-key split), the smaller-diff option that widens an existing type (string -> string | readonly string[]) beat fragmenting one coherent UI narrative into N near-duplicate config entries -- worth defaulting to the option that keeps content close to a shared idea in one place, then generalizing the plumbing, rather than duplicating structure to avoid a small type change.
- 2026-07-19 `model-builder/t-025` — When a render/generation backend has been failing every scheduled run for days (confirmed via the Actions API, not assumed), skip tasks that need it live and pick the next ready task that's verifiable by typecheck/lint alone -- don't burn a retry pass re-attempting a task blocked on infrastructure outside agent control.
- 2026-07-19 `newsfeed/t-012` — A task note can go stale even while the code moves fast underneath it: newsfeed-page.vue's own deliverables.next list still said "Category filtering" and "Perspective balancing UI" were pending, but both had fully shipped in prior cycles (newsfeed-filters.vue, feedPreferenceStore.ts) -- nothing was reading the front-page copy against the actual component tree to catch the drift. Worth checking a task's own rendered copy against its component implementation before assuming a roadmap note's status is current, not just the roadmap task's own status field.
- 2026-07-19 `conductor/t-068` — A validator module that reuses another module's file-listing helper (event_files()) instead of defining its own inherits that helper's module-global EVENT_DIR, not the caller's patched attribute -- tests patching MODULE.EVENT_DIR silently no-op unless the helper is defined in (or duplicated into) the same module it's called from.
- 2026-07-19 `newsfeed/t-016` — check_pr_file_overlap.py mirrors check_pr_kaizen.py's convention (pure function over pre-fetched PR title/body/files, no network calls, always exits 0, silent on a clean PR) rather than inventing a new shape -- worth deliberately matching an existing advisory-check convention when adding a sibling check, since it keeps the Reviewer's invocation surface predictable. Filed conductor/t-070 to eventually consolidate the two into one pre-merge pass.
- 2026-07-19 `newsfeed/t-017` — The Vercel MCP connector (list_teams -> list_projects -> list_deployments -> web_fetch_vercel_url) does give a session a real rendered preview page for any open kind_robots PR, unblocking the recurring 'no local nuxt dev' wall (t-010/t-014/t-017); documented the concrete steps in AGENTS.md. Checking list_deployments' state field along the way surfaced a genuinely broken production build (unquoted Character, a reserved MariaDB word, in raw SQL across four call sites from a prior PR cluster) that had nothing to do with newsfeed -- worth always glancing at production deployment health while investigating an unrelated preview, since 'the change isn't showing up' can mean the whole build is failing, not that the change is wrong. Raw-SQL contract-test mocks that match on text prefixes cannot catch real grammar/parse errors; filed conductor/t-069 for a proper check.
- 2026-07-19 `conductor/t-067` — process_task_events.py now guards against the same staleness class claim_task.py already solves for direct claims: before applying a queued event, compare its own updated timestamp against the live task's claimed_at/updated and skip (log STALE, don't apply) if the task moved on since the event was queued. Clean first-pass fix with 4 new unit tests covering the reported regression, dry-run, no-timestamp, and ordinary-newer-event cases.
- 2026-07-19 `ai-art-academy/t-010` — A queued task-events/ entry stuck behind a sibling file's YAML syntax bug applied stale status/note state on top of this session's freshly-claimed t-010 once it finally processed -- process_task_events.py has no staleness check against the task's current claimed_at/updated, unlike claim_task.py's live-recheck guard for direct claims. Read a corrupted roadmap note carefully before re-editing it: the truncated/duplicated fragment was easy to mistake for legitimate history at a glance. Filed conductor/t-067 for the underlying gap.
- 2026-07-19 `animation-manager/t-009` — Building a mechanical verifier over a hand-authored YAML catalog is a good way to discover the catalog was never actually machine-parseable (an unquoted colon in one field broke every YAML loader) -- worth a quick parse-and-scan pass on the target file before assuming its structure is well-formed just because agents have been hand-editing it successfully.
- 2026-07-19 `superkate-hairstyle-ai/t-021` — When a task asks for coverage that turns out to be technically impossible as literally scoped (here: a real authenticated-admin Cypress session, blocked by no JWT-minting path being exposed to Cypress), investigate the actual mechanism before writing the test -- then ship the narrower assertion that IS real (the access-gate redirect) and file the precise gap as a kaizen suggestion, rather than faking the broader claim or silently doing less than asked.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-19T16:21:31Z_
