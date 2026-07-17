# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-17T08:53:10Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **223**
- Outcomes: blocked: 12, done: 211
- Success rate: **95%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 19 | 100% |
| alexa-integration | 2 | 100% |
| animation-manager | 4 | 100% |
| animation-studio | 1 | 100% |
| appmaker | 2 | 100% |
| approval-portal | 2 | 0% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 12 | 100% |
| conductor | 29 | 100% |
| digital-storefront | 6 | 100% |
| dream-cycle | 13 | 100% |
| ecosystem-map | 4 | 100% |
| global-ui | 7 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 1 | 100% |
| kind-robots | 24 | 96% |
| kindrobots-unraid | 4 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 27 | 100% |
| mural-design | 1 | 100% |
| newsfeed | 2 | 100% |
| packmaker | 5 | 100% |
| ruler-hooked | 2 | 100% |
| serendipity | 1 | 100% |
| superkate-hairstyle-ai | 15 | 100% |
| superkate-services-calculator | 11 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 208 | 99% |

## Failure categories

| Category | Count |
|---|---|
| actionable | 5 |
| quality | 3 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `actionable` — 5 occurrences; look for the shared cause across its records
- failure category `quality` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-07-17 `conductor/t-054` — Running the recheck script during a record-keeping migration paid off beyond bookkeeping: all previously 403-blocked hosts (metmuseum, wikimedia, stripe) probed REACHABLE this session, flipping three "blocked" tasks to genuinely workable — always re-probe before copying forward a "still blocked" claim. When the top of priority.yaml is systemically blocked (shared egress allowlist, missing API token) rather than task-specific, don't burn a cycle re-probing the same hosts across multiple tasks in the same blocked project -- one recheck via recheck_egress_blocks.py covers the whole cluster of tasks depending on that host. Walking down to the next project with genuinely actionable (no-dependency, no-egress) ready tasks is cheaper than repeatedly rediscovering the same block. Also: a fresh sandbox with no node_modules can fail npm install on an unrelated dev-only binary download (Cypress's CDN, itself egress-blocked here) -- rerun with CYPRESS_INSTALL_BINARY=0 rather than treating the whole install as blocked, and revert any incidental package-lock.json churn the reinstall introduces before committing (npm engine-version mismatch between the sandbox and the repo's pinned node/npm produces unrelated lockfile diffs that don't belong in an unrelated PR).

- 2026-07-17 `conductor/t-058` — When testing an early-exit gate, assert the negative too: an exploding api() stub proves main() returned before any work, which the exit code alone doesn't guarantee.

- 2026-07-17 `conductor/t-056` — The batch-merge dirty-state race is self-inflicted by the Reviewer's own prior merge, so the fix is procedural documentation (retry after re-fetching main), not more Worker-side rebasing — document races where the causing agent will read them, next to the conflict-resolution rule they modify.

- 2026-07-17 `conductor/t-057` — Discoverability docs pay for themselves: a proven script that only greppers can find gets re-derived; one paragraph in AGENTS.md at the point of need (the cross-repo section) is the whole fix.

- 2026-07-17 `conductor/t-060` — Priority.yaml drift fixes are pure record-keeping: placement "alongside similarly-scoped projects" is a judgment call, so state the chosen anchors in the task note (animation-studio after animation-manager, etc.) so the next drift audit can tell intent from accident. Retired-but-listed projects are harmless — overrides skip them at pick time.

- 2026-07-17 `global-ui/t-020` — Clean first-pass extraction of a shared component from two already-drifted copies: scoping the refactor to exactly the duplicated card (leaving the unrelated KAIZEN-category markup in conductor-page.vue untouched) kept the diff small and the CI green on the first try across both repos (kind_robots PR #344, conductor PR #678).

- 2026-07-17 `kind-robots/t-036` — A hermetic test's synthetic fixture data can itself trip a secret scanner if it's shaped like a real credential literal (mysql://user:pass@host) or uses a trigger-word identifier (a const literally named *PASSWORD*) even though it's fake test data. Assemble such fixtures from named constants via template literals (or .join for delimiter-containing pieces) rather than one quoted literal, and avoid secret-suggestive identifier names, to dodge false positives before they cost a round trip. Also: once a flagged literal lands in any commit, GitGuardian scans the whole PR's commit range, so a follow-up commit that removes it does not clear the check on its own — squash/rebase so the flagged text never appears in history.

- 2026-07-17 `kind-robots/t-032` — Task was claimed/worked under owner: reviewer even though it was implementation work (a doc PR), which the Security Model reserves for Worker. Harmless here since the output was correct and merged clean, but future burst-mode sessions doing doc/code work should claim as owner: worker regardless of which role slot the session is labeled.
- 2026-07-17 `global-ui/t-021` — A Worker session that just shipped a task can independently notice and fix a same-cycle staleness issue faster than the Reviewer can file and route a kaizen task for it -- kind_robots PR #340 landed 8 seconds after PR #338 merged, before the kaizen task even reached origin/main. No process gap here, just worth remembering that fast same-session follow-ups can outrun roadmap bookkeeping; check open PRs again after any merge before assuming the sweep is complete.
- 2026-07-17 `global-ui/t-017` — When a Worker session claims a task whose seed data references another in-flight task (t-017's manifest pointed at t-014 via acknowledgedGap), check whether the referenced task landed on main in the interim before merging — it may have shipped a real target (t-014's /for-you nav entry) that should replace the placeholder gap outright, saving a follow-up cycle.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-17T08:53:10Z_
