# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-19T20:13:56Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **300**
- Outcomes: blocked: 12, done: 288
- Success rate: **96%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 33 | 100% |
| alexa-integration | 2 | 100% |
| animation-manager | 6 | 100% |
| animation-studio | 1 | 100% |
| appmaker | 2 | 100% |
| approval-portal | 2 | 0% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 13 | 100% |
| conductor | 41 | 100% |
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
| newsfeed | 19 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 2 | 100% |
| serendipity | 3 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 11 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 285 | 99% |

## Failure categories

| Category | Count |
|---|---|
| actionable | 6 |
| quality | 5 |
| transient | 4 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `actionable` — 6 occurrences; look for the shared cause across its records
- failure category `quality` — 5 occurrences; look for the shared cause across its records
- failure category `transient` — 4 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-07-19 `newsfeed/t-018` — Sourcing a real bias rating (vs. leaving unrated) is a fast WebSearch+WebFetch task once a project's guardrail doc (BIAS-CONTROLS.md) already specifies the required provenance shape -- checked Media Bias/Fact Check's own site directly (not just search snippets) to get the exact label wording, and confirmed absence-of-rating for the second source via a site-scoped search before concluding it should stay unrated rather than guessing a plausible-sounding label.
- 2026-07-19 `ai-art-academy/t-010` — Two independent sessions within the same hour (this one, and conductor/t-071's tooling build) both found t-010 stuck at status: claimed with its own note confirming the referenced kind_robots PR #544 had merged and it should rearm to ready -- and both initially deferred fixing it per AGENTS.md's rotation-collision caution, since the task looked like it might still be another session's in-flight work. A task claim that's confirmed complete by its own note but left untouched twice out of caution is itself a signal worth acting on the second time, not deferring a third: check whether real time has actually passed (claimed_at vs now) and whether the referenced PR's merge timestamp predates the current sweep by a wide margin before assuming a stale-looking claim is still live.
- 2026-07-19 `conductor/t-070` — A branch push can 413 even with a tiny diff and no local history rewrite -- this session's push failed twice, once because the session branch simply didn't exist on the actual GitHub remote yet (local remote-tracking ref showed a stale SHA, but `git ls-remote` showed nothing), and again after a squash-merge when a follow-up single-field status flip needed to reach main. Both resolved via CLAUDE.md's documented workarounds (`create_branch` for the first, `git_plumbing.commit_file_on_ref` direct to `refs/heads/main` for the second) rather than attempting to hand-transcribe a ~130KB roadmap.yaml into `push_files`, which would have risked silently corrupting the shared roadmap for every other concurrent agent. When a file is too large to safely retype, prefer a git-plumbing helper that reads the exact bytes from disk over any path that requires the content to pass through generated text.
- 2026-07-19 `newsfeed/t-014` — A prior session's own note ("could not verify locally, needs a real preview-deploy connector") is a precise handoff -- the Vercel MCP list_teams/list_projects/list_deployments/web_fetch_vercel_url chain in AGENTS.md answers it directly against the live production deployment without needing a new PR or any code change. Worth checking whether a 'ready' task is actually a pure-verification task before assuming every ready task implies a code diff.
- 2026-07-19 `newsfeed/t-020` — When a tie-break/precedence rule (here, resolveTutorialChannelFromRoute's cross-key bestLen prefix match) has zero real-world data to exercise it, add optional test-only override parameters defaulted to the real production data -- this lets a unit test inject controlled overlapping fixtures without touching any real call site's behavior, rather than either skipping the test or waiting for production data to coincidentally collide.
- 2026-07-19 `newsfeed/t-019` — When a task offers an explicit design choice (single multi-route channel vs. per-tab-key split), the smaller-diff option that widens an existing type (string -> string | readonly string[]) beat fragmenting one coherent UI narrative into N near-duplicate config entries -- worth defaulting to the option that keeps content close to a shared idea in one place, then generalizing the plumbing, rather than duplicating structure to avoid a small type change.
- 2026-07-19 `model-builder/t-025` — When a render/generation backend has been failing every scheduled run for days (confirmed via the Actions API, not assumed), skip tasks that need it live and pick the next ready task that's verifiable by typecheck/lint alone -- don't burn a retry pass re-attempting a task blocked on infrastructure outside agent control.
- 2026-07-19 `newsfeed/t-012` — A task note can go stale even while the code moves fast underneath it: newsfeed-page.vue's own deliverables.next list still said "Category filtering" and "Perspective balancing UI" were pending, but both had fully shipped in prior cycles (newsfeed-filters.vue, feedPreferenceStore.ts) -- nothing was reading the front-page copy against the actual component tree to catch the drift. Worth checking a task's own rendered copy against its component implementation before assuming a roadmap note's status is current, not just the roadmap task's own status field.
- 2026-07-19 `conductor/t-068` — A validator module that reuses another module's file-listing helper (event_files()) instead of defining its own inherits that helper's module-global EVENT_DIR, not the caller's patched attribute -- tests patching MODULE.EVENT_DIR silently no-op unless the helper is defined in (or duplicated into) the same module it's called from.
- 2026-07-19 `newsfeed/t-016` — check_pr_file_overlap.py mirrors check_pr_kaizen.py's convention (pure function over pre-fetched PR title/body/files, no network calls, always exits 0, silent on a clean PR) rather than inventing a new shape -- worth deliberately matching an existing advisory-check convention when adding a sibling check, since it keeps the Reviewer's invocation surface predictable. Filed conductor/t-070 to eventually consolidate the two into one pre-merge pass.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-19T20:13:56Z_
