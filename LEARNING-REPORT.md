# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-28T07:30:48Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **801**
- Outcomes: blocked: 16, cancelled: 1, done: 784
- Success rate: **98%**
- Average passes on successful tasks: **0.1**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 70 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 13 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 9 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| brainstorm | 25 | 96% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 25 | 100% |
| conductor | 83 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 32 | 97% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 86 | 100% |
| kapowarr | 48 | 100% |
| kind-economy | 6 | 100% |
| kind-robots | 53 | 98% |
| kindrobots-unraid | 5 | 100% |
| lora-ingestion | 1 | 100% |
| mandarin-tutor | 7 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 79 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 10 | 100% |
| scene-animator | 2 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 16 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 6 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 16 | 44% |
| software | 785 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 14 |
| actionable | 12 |
| transient | 11 |
| scope | 2 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 14 occurrences; look for the shared cause across its records
- failure category `actionable` — 12 occurrences; look for the shared cause across its records
- failure category `transient` — 11 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-28 `cthulhuquarium/t-050` — A kaizen task filed against a specific call site (purchaseSpeciesForUser) can be fully subsumed by later, unrelated-looking dependency work (t-029's breeding creation, t-041's egg hatching) that happens to wire the same helper for its own reasons -- always grep for every call site of the thing the task asks you to add (here: every AquariumStock-creating transaction) before writing new code, since the task may already be done.
- 2026-08-28 `cthulhuquarium/t-030` — t-031's currentlyOwned flag and dead "Re-order" button, and t-029's rolled stat* columns, were both built ahead of time specifically for this task -- t-030 landed as almost pure wiring (rotateShopStock + sellPrice, both pure functions in aquariumEconomy.ts) with zero migration, exactly as t-032's schema-first discipline intended. The one design risk this task's own note called out by name (rotating stock + selling creating a quiet permanent loss of access) was already fully solved by t-031's Ichthyonomicon before this task started -- confirms that flagging a trap in a task note AND building its fix into an earlier, unrelated-looking task (t-031) is a pattern worth repeating when a later task's safety depends on state a dependency already tracks.
- 2026-08-28 `cthulhuquarium/t-053` — t-018/t-028's justCompletedBestiary/firedMilestones purchase-response signals sat server-complete with zero frontend consumer for a full cycle -- the server-side gate (slot-cap increase, AquariumEvent log) working correctly gave no visible signal that the UI half was still missing. Worth periodically diffing a store's typed response interfaces against what the server actually returns, not just what the store currently reads off it.
- 2026-08-28 `cthulhuquarium/t-029` — t-032's schema-first discipline (shipping nullable stat/parentage columns and the EvolutionKind enum before any code read them) paid off exactly as intended -- t-029 needed zero migration, only wiring pure roll/converge/threshold functions onto columns that already existed. A prior session's claim on this task had expired (CLAIM_TTL_MINUTES) with no PR ever opened; next_ready_task.py correctly resurfaced it as pickable rather than leaving it stuck.
- 2026-08-28 `kind-robots/t-075` — DROP migrations need deploy-then-migrate sequencing when old clients still select the retiring column. The removal-only deferred parity marker now makes that staging explicit and auditable without weakening ordinary schema/migration parity.
- 2026-08-28 `cthulhuquarium/t-039` — A design note calling for two illustrated plates (screen-finale, set-last-aquarium) that were queued but not yet generated did not have to block the whole feature: the purchase/economy/event-logging mechanics and a code-only canvas vignette shipped now, with a placeholder text-only reveal dialog standing in for the real art -- the exact "mechanical gate now, authored pass later" shape t-028/t-053 already established for the milestone toast. Filed t-054 to swap in the real plates once generated, rather than leaving t-039 open/blocked on an asset pipeline outside this session's reach. Also confirmed conductor's own "Python test suite" CI job intermittently fails on a live kindrobots.org 502 (production Resource-registry read) plus two unrelated flaky assertions, identically across two independent roadmap-only PRs (#3040, #3041) -- consistent with t-124's existing finding that this job is not a required check; mergeable_state read "unstable" not "blocked" on both, so merged past it per that documented precedent rather than re-running indefinitely.
- 2026-08-27 `cthulhuquarium/t-028` — A prior session's RESEARCHED-NOT-IMPLEMENTED note (scoping "5 of 8 landmarks are fully computable today") was a directly usable spec, not just context -- implementing exactly that recommendation (4 of the 5, dropping the one still blocked on an unresolved semantics call) landed clean on the first pass with no design ambiguity to resolve mid-task. Closing a title-broad task ("...as the gating layer") at `done` on its landable core, rather than leaving it `ready` forever waiting for unbuilt subsystems (evolution/rivalry) or a one-line human decision (full-tank semantics), keeps the roadmap's `ready` queue honest -- those remainders aren't actionable by another agent pass, so leaving the umbrella task open would just resurface as unclaimable "ready" work each sweep. A frontend-integration kaizen (t-053) captures the actually actionable follow-on instead.
- 2026-08-27 `cthulhuquarium/t-019` — "Retune against real play data" cannot be satisfied by a sandboxed agent session when no telemetry/analytics path exists yet and the session has no way to generate a real multi-session player history itself -- this is an actionable failure (missing access to the core input the task needs), not a quality failure, so it does not burn a pass. A prior session (2026-08-25) had already flagged the milestone-ladder half of this task as needing play data specifically to avoid a naive fix (linear breakpoint extension) that would silently undermine an intentional design constraint (the tank-packing problem) -- worth trusting that prior judgment rather than re-deriving new numbers from design docs alone and asserting they're tuned, when they would actually just be another guess.
- 2026-08-27 `cthulhuquarium/t-051` — A balance-pass task that explicitly allows a no-op exit does not need real play data to close well -- reviewing DECOR_CATALOG's six costs against the existing RARITY_TIERS anchor (already the established convention SET_PIECE_CATALOG uses) surfaced a deliberate taper, not a guess, and was enough to confirm the pricing rather than requiring telemetry this sandbox cannot produce. Worth distinguishing from t-019 in the same session: a task is only genuinely blocked on real data when its own note requires *feel* (does the pacing feel right) rather than *consistency* (does this number follow the pattern the rest of the file already sets).
- 2026-08-27 `cthulhuquarium/t-049` — Adding a purely cosmetic canvas sprite (roaming collector automaton) went fastest by mirroring an existing sibling pattern in the same file -- SWIM_SPEED_SET_KIND's equipped-set-piece read, and the swimmer/mote step+render split -- rather than inventing a new structure. Keeping the change client-rendering-only (no economy/API touch, since settleTick already owns the real roaming_collector income bonus server-side) kept the task genuinely reversible and let the existing aquarium-economy and aquarium-touch test suites stand as sufficient verification without a live browser.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-28T07:30:48Z_
