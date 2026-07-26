# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-26T11:09:35Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **358**
- Outcomes: blocked: 12, cancelled: 1, done: 345
- Success rate: **96%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 39 | 100% |
| alexa-integration | 2 | 100% |
| animation-manager | 10 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 5 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 14 | 100% |
| conductor | 47 | 100% |
| conductor-app | 2 | 100% |
| davinci | 1 | 100% |
| digital-storefront | 19 | 100% |
| dream-cycle | 14 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 1 | 100% |
| kind-robots | 38 | 97% |
| kindrobots-unraid | 4 | 100% |
| media-watchlist | 4 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 32 | 100% |
| mural-design | 1 | 100% |
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
| software | 343 | 99% |

## Failure categories

| Category | Count |
|---|---|
| actionable | 7 |
| quality | 6 |
| transient | 5 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `actionable` — 7 occurrences; look for the shared cause across its records
- failure category `quality` — 6 occurrences; look for the shared cause across its records
- failure category `transient` — 5 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-07-26 `digital-storefront/t-032` — Hand-typing a plausible-looking but coarse (round-hour) claim --session id instead of invoking date -u for real seconds precision is exactly the collision-prone pattern AGENTS.md's Rotation collisions section warns against -- this cycle hit a real concurrent-implementation collision on the same task (two sessions both shipped equivalent kind_robots PRs, #1008 and #1009, for digital-storefront/t-032) that a genuinely unique session id wouldn't have prevented outright (claim_task.py's atomicity gap is the deeper structural cause) but which muddies the claimed_by/TALKBACK trail in exactly the way the AGENTS.md warning describes. Always shell out to date -u +%Y%m%dT%H%M%SZ for the session id rather than typing a round timestamp by hand.
- 2026-07-26 `digital-storefront/t-032` — A takedown/eligibility gate enforced only at checkout-creation time leaves a real gap for anything fulfilled asynchronously at webhook time -- the window between session-create and payment-complete is exactly where a moderation action would need to take effect. Reusing the existing checkPrintEligibility() helper verbatim at the second enforcement point (rather than writing new logic) kept the two checks mechanically identical, and recording the failure as a PrintJob with status: FAILED (instead of skipping creation) preserves an audit trail for a payment that succeeded but wasn't fulfilled.
- 2026-07-26 `digital-storefront/t-031` — A kaizen note written by a prior cycle can undersell real scope -- 'wire the webhook branch' sounded like reusing an existing single-product handler, but the general cart's multi-item-per-session shape needed a genuinely different mechanism (per-line Stripe LineItem metadata, verified against the SDK's own .d.ts files rather than assumed), and the client was silently dropping data (artImageId) the task's author likely didn't know about. Treat a kaizen note as a hypothesis to verify by reading the actual current code before implementing, not a spec to build from directly -- and when research surfaces real complications, split the task rather than either attempting an oversized diff or silently narrowing scope without saying so. Also: extending a shared utility (applyMana) with an optional tx parameter to fix a transaction-atomicity gap is safer than either skipping the atomicity guarantee or duplicating the utility's logic inline -- check whether a shared helper already has this affordance before assuming you need a workaround.
- 2026-07-26 `digital-storefront/t-030` — When a design doc's own Prisma model draft predates the actually-landed schema (the doc used cuid()/String ids; the real Product/Order/OrderItem models all landed as Int autoincrement), a research-first pass reading the live schema.prisma directly caught the mismatch before it became a migration that wouldn't type-check -- worth always re-verifying a doc's schema draft against the current schema file rather than transcribing it as-is, even when the doc is recent and detailed.
- 2026-07-26 `digital-storefront/t-030` — When a task's own roadmap note pre-flags a likely needs-human gate ('expect this to reach needs-human once it touches a live payment provider'), verify the gate condition explicitly rather than trusting the PR's self-reported 'reversible' stakes label -- here that meant confirming getStripeClient() reads STRIPE_SECRET_KEY from env with no hardcoded key or forced live-mode flag, matching every other already-merged Stripe route, before merging test-mode payment/webhook code. Dispatching a subagent to independently audit the migration SQL and billing logic line-by-line (rather than reading the PR's own verification section at face value) caught nothing wrong here, but is the right level of scrutiny for anything touching schema + payment webhooks even when self-labeled reversible.
- 2026-07-26 `ai-art-academy/t-039` — A mechanical prose-to-file migration (moving t-010's 78 historical RAN entries, ~164KB, out of the roadmap note into a separate ledger) is safe to do in one pass if the regression check is structural, not eyeballed: reconstruct the original content two independent ways (standing_line + moved_lines == original; ledger_body re-indented == moved_lines) and assert byte-for-byte equality before writing anything. That caught the exact failure mode the original audit warned about ("silently pruning the note would be data loss wearing a tidy haircut") with zero manual re-reading of 164KB of prose.
- 2026-07-26 `model-builder/t-029` — After many cycles of an exclusion-list-driven 'read everything, find one new bug' task exhaust the obvious client-side races/gating/accessibility gaps, the next genuinely new find is likely to be server-side (a silent fallthrough in a relationship-linking function, an unhandled case in a catalog-to-handler mapping) rather than another variant of an already-fixed client pattern. Also: a subagent given the full exclusion list can correctly self-filter a near-duplicate finding (the committingItemId singleton race, same shape as two already-fixed siblings) instead of reporting it as new -- worth trusting that filtering rather than re-verifying every candidate from scratch when the list is this well-documented.
- 2026-07-26 `kind-robots/t-049` — An investigate-type kaizen task can close cleanly with no code diff and no PR to the target repo when the investigation's own two open questions both resolve to 'already handled': check `git log -p --follow` on the file in question before assuming a protective setting (here, a job-level `timeout-minutes`) needs adding -- it may already predate the incident that prompted the task. Also worth a quick recent-run-history check via the GitHub Actions API before treating a single observed hang as a recurring pattern.
- 2026-07-26 `kind-robots/t-043` — For a cross-app authorization boundary (on-behalf-of mana charging), splitting the pure decision function into its own dependency-free module paid off immediately -- it let the security property get a direct 5-case unit test wired into CI, instead of relying on integration coverage that would need the full Nuxt runtime and a live DB. The one place this class of feature silently breaks is billing: on-behalf-of charges must debit the target user's own standing, not the caller's server-key standing, or every cross-app charge becomes accidentally free -- worth checking for explicitly in review whenever a machine-caller can act on behalf of another user.
- 2026-07-26 `digital-storefront/t-029` — A prerequisite field landing first with a named downstream consumer already identified (t-020's Resource.commercialSafe migration named this exact task) means the wiring PR can be built and reviewed with zero ambiguity about intent or scope -- the diff was a pure function (checkPrintEligibility), one new authenticated GET endpoint mirroring an existing endpoint's auth pattern, and a UI wire-up, no schema changes. Reviewed and merged same-cycle with all CI green.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-26T11:09:35Z_
