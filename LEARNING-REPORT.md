# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-26T14:32:58Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **366**
- Outcomes: blocked: 12, cancelled: 1, done: 353
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
| conductor | 48 | 100% |
| conductor-app | 2 | 100% |
| davinci | 1 | 100% |
| digital-storefront | 23 | 100% |
| dream-cycle | 14 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 3 | 100% |
| kind-robots | 39 | 97% |
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
| software | 351 | 99% |

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

- 2026-07-26 `humboldt-scoop-cms/t-012` — Infra scaffolding that can't be executed in-sandbox (Docker, external data fetch) is still verifiable to a meaningful degree without live execution -- config loads under its runtime, scripts pass a syntax check, and the checked-in contract matches what the calling app code already expects. Land it as scaffolding with an explicit "verify on the real box" flag rather than blocking on infrastructure access no sandbox session will ever have.
- 2026-07-26 `digital-storefront/t-035` — When two call sites independently re-implement the same eligibility-check-then-insert sequence, extracting a shared helper immediately after the second bug fix (rather than leaving both copies as "matching patterns") is cheap while the logic is fresh and prevents the next fix from landing in only one copy again.
- 2026-07-26 `digital-storefront/t-034` — A failure-record insert must not reference the same missing foreign key that caused the failure; preserve the paid-order audit trail by omitting the dependent row when its required parent no longer exists.
- 2026-07-26 `digital-storefront/t-034` — When a sibling code path already handles a case correctly (fulfillGiftshopPrintJob skipping PrintJob creation for a missing FK target), check for an older path implementing the same operation less safely (handleProductPurchase) before assuming a fix is novel.
- 2026-07-26 `conductor/t-080` — Preserve upstream structured failure detail at the boundary where it would otherwise be collapsed into a generic error; diagnosis cannot recover evidence that was never stored.
- 2026-07-26 `humboldt-scoop-cms/t-007` — Designing a pluggable RouteMatrixProvider interface let the deterministic route-plan API ship and be fully tested (including brute-force-verified optimizer correctness) even though no self-hosted OSRM/VROOM instance exists yet anywhere -- the Haversine fallback made the feature usable today, and the OSRM provider's request/response shape is already unit-tested against a mocked fetch, so standing up real infra later (t-012) is a config change, not a rewrite.
- 2026-07-26 `kind-robots/t-050` — Following the immediately-prior additive migration's exact SQL shape (add_grant_model's enum-MODIFY + CreateTable + AddForeignKey pattern) let the migration.sql be hand-written correctly on the first attempt with no live DB to verify against -- matching an existing precedent migration in the same repo is a reliable substitute for `prisma migrate dev` when no DB is reachable.
- 2026-07-26 `digital-storefront/t-033` — Carry identity-bearing fields through every checkout boundary and revalidate eligibility at fulfillment; dropping artImageId turned an apparently complete cart flow into audit-only fulfillment for physical goods.
- 2026-07-26 `digital-storefront/t-032` — Hand-typing a plausible-looking but coarse (round-hour) claim --session id instead of invoking date -u for real seconds precision is exactly the collision-prone pattern AGENTS.md's Rotation collisions section warns against -- this cycle hit a real concurrent-implementation collision on the same task (two sessions both shipped equivalent kind_robots PRs, #1008 and #1009, for digital-storefront/t-032) that a genuinely unique session id wouldn't have prevented outright (claim_task.py's atomicity gap is the deeper structural cause) but which muddies the claimed_by/TALKBACK trail in exactly the way the AGENTS.md warning describes. Always shell out to date -u +%Y%m%dT%H%M%SZ for the session id rather than typing a round timestamp by hand.
- 2026-07-26 `digital-storefront/t-032` — A takedown/eligibility gate enforced only at checkout-creation time leaves a real gap for anything fulfilled asynchronously at webhook time -- the window between session-create and payment-complete is exactly where a moderation action would need to take effect. Reusing the existing checkPrintEligibility() helper verbatim at the second enforcement point (rather than writing new logic) kept the two checks mechanically identical, and recording the failure as a PrintJob with status: FAILED (instead of skipping creation) preserves an audit trail for a payment that succeeded but wasn't fulfilled.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-26T14:32:58Z_
