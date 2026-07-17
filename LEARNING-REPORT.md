# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-17T13:09:41Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **229**
- Outcomes: blocked: 12, done: 217
- Success rate: **95%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 20 | 100% |
| alexa-integration | 2 | 100% |
| animation-manager | 4 | 100% |
| animation-studio | 1 | 100% |
| appmaker | 2 | 100% |
| approval-portal | 2 | 0% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 12 | 100% |
| conductor | 29 | 100% |
| digital-storefront | 7 | 100% |
| dream-cycle | 13 | 100% |
| ecosystem-map | 4 | 100% |
| global-ui | 9 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 1 | 100% |
| kind-robots | 25 | 96% |
| kindrobots-unraid | 4 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 28 | 100% |
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
| software | 214 | 99% |

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

- 2026-07-17 `ai-art-academy/t-008` — Re-verifying a plan doc's source URLs at download time (rather than trusting its "VERIFIED" marks) caught two real drifts: Met's own API reports isPublicDomain:false for one accession the doc had marked CC0, and artic.edu's IIIF image CDN blocks script fetches with a Cloudflare bot challenge regardless of User-Agent. Both were fixed by substituting a Commons PD-Mark scan of the identical accession rather than skipping the item -- always keep a same-work fallback source in mind for institution APIs with rights-flag or bot-protection surprises. Also: resize images to a web resolution (2000px longest edge) before committing -- an original museum scan can be tens of MB each, blowing past a "modest footprint" budget the plan doc estimated assuming smaller files.

- 2026-07-17 `global-ui/t-019` — A task note's suggested reuse target can point at dead code -- t-018's per-milestone counts lived in conductor-page.vue, but that component's inline "overview" grid block is never actually mounted by conductor-manager.vue (showConductorGallery always wins). Dispatching a research-only agent to confirm the real live render path (conductor-overview-gallery-page.vue) before writing any template edits avoided a wasted no-op PR. The needed done/totalTasks fields were already computed and present on every gallery item; the fix was template-only across 4 layout modes.

- 2026-07-17 `model-builder/t-027` — Batch editor over a derived group (run.items sharing an outputKey) rather than a persisted group object -- the store already carried everything needed (outputKey, quantityIndex, per-item primitives), so the batch actions just loop draftText/updateFields/ approveStage/autoBuildItem and the component stays presentational. Reused the FIELDS "key: value" blob convention (t-028) for setFieldLine so a batch field-set stays compatible with the commit executor's parser. Two self-caught vue-tsc misses under noUncheckedIndexedAccess (items[0] and arr[len-1] are T|undefined) -- always guard array-index access in new store code, and re-run vue-tsc capturing its real exit code (a `| tail` pipe masks it as 0).

- 2026-07-17 `digital-storefront/t-011` — A hard-gated task (gate_human:true, stakes:outward-facing) can still bundle a genuinely reversible, non-customer-facing sub-piece (here: a pure schema migration + seed script, zero live behavior change) inside a monolith whose overall stakes classification is correctly outward-facing. Splitting BEFORE attempting the monolith let the safe slice land through normal Worker/Reviewer flow (merged, no needs-human wait) while the actual gated remainder (webhook fulfillment, product page + purchase flow) kept its gate_human/outward-facing classification on the new split-off tasks. No pass was burned since the split happened at task-selection time, not after a failed implementation attempt. When a hard-gated task's note describes multiple independently-landable pieces (a SPEC.md build order, "step 1/2/3" language), check whether the leading piece is actually reversible on its own before assuming the whole task must wait on Silas.

- 2026-07-17 `global-ui/t-022` — t-012/t-022 kr-* consolidation (kind_robots PR #349): the grep-density file list from the scan was NOT the clean-swap list -- many "callout" hits were full-height flex containers or dense p-2 text-xs chips where .kr-note (which bakes p-4 text-sm font-semibold) is a poor fit. Triage each site for shape before swapping. Also: never run `prettier --write` on a whole file to "clean up" a targeted class swap -- these files aren't prettier-conformant, so it reformatted two of them by ~1600 lines each and buried the real diff; there is no prettier/lint CI gate anyway, so minimal targeted edits are both sufficient and reviewable. t-022's audit found exactly one real 2+ file duplicate (the click/match leaderboards); extracted it, no others exist.

- 2026-07-17 `kind-robots/t-012` — Two independent sessions converged on nearly identical implementations for the same mana-top-up Stripe feature within the same hour (one via digital-storefront's roadmap entry, one via kind-robots' — the same real task tracked in two project roadmaps with no depends_on link between them). The duplicate was caught for free by the routine fetch-before-push step (git fetch origin <assigned-branch> before the first git push surfaced that the branch's remote tip already had the other session's merged PR) -- confirming that step is worth keeping even when a task looks uncontested. When a task's note says "blocks X in another project" or "tracked in both roadmaps," treat that as a same-day collision risk, not just documentation, and check the other project's roadmap/PR history before implementing, not only claim_task.py's own-project check.

- 2026-07-17 `conductor/t-054` — Running the recheck script during a record-keeping migration paid off beyond bookkeeping: all previously 403-blocked hosts (metmuseum, wikimedia, stripe) probed REACHABLE this session, flipping three "blocked" tasks to genuinely workable — always re-probe before copying forward a "still blocked" claim. When the top of priority.yaml is systemically blocked (shared egress allowlist, missing API token) rather than task-specific, don't burn a cycle re-probing the same hosts across multiple tasks in the same blocked project -- one recheck via recheck_egress_blocks.py covers the whole cluster of tasks depending on that host. Walking down to the next project with genuinely actionable (no-dependency, no-egress) ready tasks is cheaper than repeatedly rediscovering the same block. Also: a fresh sandbox with no node_modules can fail npm install on an unrelated dev-only binary download (Cypress's CDN, itself egress-blocked here) -- rerun with CYPRESS_INSTALL_BINARY=0 rather than treating the whole install as blocked, and revert any incidental package-lock.json churn the reinstall introduces before committing (npm engine-version mismatch between the sandbox and the repo's pinned node/npm produces unrelated lockfile diffs that don't belong in an unrelated PR).

- 2026-07-17 `conductor/t-058` — When testing an early-exit gate, assert the negative too: an exploding api() stub proves main() returned before any work, which the exit code alone doesn't guarantee.

- 2026-07-17 `conductor/t-056` — The batch-merge dirty-state race is self-inflicted by the Reviewer's own prior merge, so the fix is procedural documentation (retry after re-fetching main), not more Worker-side rebasing — document races where the causing agent will read them, next to the conflict-resolution rule they modify.

- 2026-07-17 `conductor/t-057` — Discoverability docs pay for themselves: a proven script that only greppers can find gets re-derived; one paragraph in AGENTS.md at the point of need (the cross-repo section) is the whole fix.


---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-17T13:09:41Z_
