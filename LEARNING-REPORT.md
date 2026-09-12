# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-12T03:47:22Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **917**
- Outcomes: blocked: 16, cancelled: 1, done: 900
- Success rate: **98%**
- Average passes on successful tasks: **0.1**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 73 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 14 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 9 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| brainstorm | 26 | 96% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 25 | 100% |
| conductor | 95 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 51 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 23 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 118 | 100% |
| kapowarr | 52 | 100% |
| kind-economy | 10 | 100% |
| kind-robots | 55 | 98% |
| kindrobots-unraid | 6 | 100% |
| lora-ingestion | 1 | 100% |
| mandarin-tutor | 11 | 100% |
| media-watchlist | 12 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 83 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| rainbow-butterflies | 20 | 100% |
| ruler-hooked | 11 | 100% |
| scene-animator | 2 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 18 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 6 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 900 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 17 |
| transient | 15 |
| actionable | 13 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 47% success over 17 closed tasks; aim the next kaizen task here
- failure category `quality` — 17 occurrences; look for the shared cause across its records
- failure category `transient` — 15 occurrences; look for the shared cause across its records
- failure category `actionable` — 13 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-12 `interface-vision/t-104` — A .kr-input*-family primitive whose base @apply drops a dead legacy class (input-bordered) doesn't fully close the family just because every DaisyUI size variant is named -- a separate axis (an explicit rounded-xl/rounded-2xl radius override coexisting with the same dead class) can carry 60+ occurrences unnoticed until a fresh full-repo survey checks for extra utility tokens riding alongside the base set, not just the base set's size suffixes alone.
- 2026-09-11 `interface-vision/t-104` — The kr-text-black-* family's sizes (-lg/-xl/-sm/-xs/-2xl) were named as they were surveyed, not against a known-finite set -- so 'family closed' claims in a prior slice's note undercounted: text-base, the Tailwind default size, went unnamed for 69 slices until a plain 'diff the family's suffixes against Tailwind's own text-size scale' check would have surfaced it immediately. Next time a kr-text-* (or any Tailwind-scale-keyed) family claims to be closed, check its suffixes against the underlying scale's full enumeration before trusting the claim.
- 2026-09-11 `cthulhuquarium/t-077` — Wiring a pure evaluator (t-075's evaluateRivalry) into a tick-settlement loop is cheapest done ONCE per settlement outside the per-tick inner loop, not once per (tick x fish): composition (which fish, their traits) is loop-invariant even though the production amount it multiplies varies every tick via hunger/debris. Same discipline as debrisEverHigh's sticky-flag pattern applied a second time (rivalryObserved) -- a landmark milestone that can go active/inactive repeatedly still only needs ONE persisted 'ever observed' flag plus the existing AquariumEvent-log idempotency check, not a second column for 'already resolved'.
- 2026-09-11 `cthulhuquarium/t-075` — A soft-gated feature task (Silas hasn't confirmed it's still wanted for v1) can still land a bounded, reversible first slice while the gate is open in parallel -- the pure rivalry evaluator shipped and tested clean, with runtime wiring split into a new task (t-077) rather than either blocking on the gate or scope-creeping the wiring into the same PR.
- 2026-09-11 `cthulhuquarium/t-074` — economy.yaml's first_full_tank/first_spotless_tank triggers looked pre-decided but weren't fully -- economy.yaml predates t-032's two-pool capacity split, and aquariumEconomy.ts's own comment flagged the "full" semantics as an unresolved ambiguity. Reading the actual trigger strings closely (economy.yaml still has "debris reaches 0 after having been >= 80" verbatim, and DEBRIS_BANDS' own worst-band threshold is that same 80) resolved both without needing a Silas round-trip: "every owned slot" maps to the weighed fish pool (currentReservedSize vs effectiveSizeCap), not setSlotsCap, since t-032's own comment says setSlotsCap is exclusively for set pieces. The debris trigger needed a small additive migration (Aquarium.debrisEverHigh) because a player can clean an 80+ debris level down to 0 across several separate requests, so "having been >= 80" can't be read off one request's before/after pair alone. Next task touching an old economy.yaml trigger: read the literal trigger string plus any nearby "this predates X" comment before guessing at intent -- the spec is usually more precise than the roadmap task summarizing it.
- 2026-09-11 `kind-economy/t-017` — Its own dependencies (t-003, t-014) had both just closed the same day (t-003 literally that morning, from a live Silas decision recorded in the roadmap note), which is why `next_ready_task.py` never surfaced this task before now despite it sitting `status: ready` for weeks. Drafting it was straightforward once the two upstream design docs (DESIGN-BRIEF.md, PAYOUT-MECHANISM-DESIGN.md) were read in full -- every number and policy in the draft traces to an already-decided default or explicit recommendation in those docs, with genuinely undecided items marked `[OPEN]` rather than guessed at. Closed to `done` (not `needs-human`) matching the same-project precedent on t-003/t-014/t-022: a complete draft under Silas's 2026-09-07 human-gate-simplification policy doesn't wait on him, only its eventual publication does.
- 2026-09-11 `media-watchlist/t-019` — The reported symptom ("failed to load, error message masked") had two independent root causes, and reading the actual auth flow rather than trusting the task's own working hypothesis found the more important one: the task guessed a stale/mis-scoped session, but grepping the component for Authorization-header attachment found there wasn't one at all -- every $fetch call in the feature was effectively anonymous, so every request failed the admin gate regardless of who was signed in. Cross-checked against the working `Authorization: Bearer` pattern already used elsewhere in the codebase (stores/artStore.ts, stylist-clients.vue) confirmed it wasn't a one-off omission but a gap specific to this feature's components. Separately, fixing the error-masking half (errorHandler() never calling setResponseStatus) surfaced a much larger house-wide pattern (432 call sites, only 8 already correct) -- filed as its own task (kind-robots/t-096) rather than attempted as a drive-by fix, since a mechanical change at that scale needs its own audit and codemod. Pattern worth repeating: when a task's own note proposes a hypothesis for "why does X fail," verify it against the actual code path before assuming it's the answer -- the real cause here was two frames of causation deeper (missing auth headers, not stale session state) and code reading found it in minutes.
- 2026-09-11 `cthulhuquarium/t-072` — Investigated both halves of the task before touching code, and that investigation changed the plan: the roadmap note offered "fix the path or delete" the dead importCthulhuquariumArt.mjs script as two equally valid options, but reading the actual delivered assets showed the script's per-prefix resize scheme (1280/960/640/512px by filename prefix) doesn't match what the real delivery (kind_robots#2620) actually shipped (uniform 512px-long-edge) -- "fixing" the path would have silently overwritten already-correct committed assets with differently-sized ones. Deletion was the only safe choice once that was known, not a coin flip. Separately, the task's other half (bulk-creating real ArtImage DB records and linking them to Monster rows) was real, well-precedented, buildable work -- but this sandbox has zero path to any live database (confirmed: no .env, dummy-only DATABASE_URL in the provisioning script, no reachable DB port) -- so attempting it here would have produced an unverifiable script at best. Split it into its own task (t-076) with the investigation's findings attached, rather than either skipping it silently or attempting unverifiable DB work. Pattern worth repeating: when a roadmap task bundles a quick fix with something that needs infrastructure this sandbox doesn't have, do the quick part, investigate the rest thoroughly enough to leave a real trail, and split rather than stall.
- 2026-09-11 `cthulhuquarium/t-070` — Filed directly by t-068's FULL-GAME-GAP-AUDIT.md as the highest-priority follow-up: t-065's earlier art-delivery fix only reached kr-art-plate calls in the bestiary/catalog/reveal-dialog panels, never the swim-canvas render loop (drawFish() in cthulhuquarium-game.vue), which is the one thing a player watches continuously. Fixed with a minimal, backward-compatible change -- a lazy per-slug HTMLImageElement cache feeding context.drawImage(), falling back to the original primitive silhouette when no art is cached yet or fails to load -- rather than a riskier rewrite of the render loop. Kept the existing hunger-based saturate()/globalAlpha desaturation and context.scale(facing, 1) flip behavior identical on both paths so the change is additive, not a redesign. Verified via eslint, vue-tsc --noEmit, prettier --check, and the full 46-check kind_robots CI suite (all green, including Contract verifiers and TypeScript) -- no visual/browser confirmation was possible from this sandbox, which is an honest gap worth a human spot-check on kindrobots.org next time the tank is opened, same caveat t-068 already flagged for the bestiary fix.
- 2026-09-11 `cthulhuquarium/t-068` — A roadmap can read 63-68/68 done while the game still fails the owner's own look, because "done" tracked whether a task closed, not whether its output reached the player -- t-065's art shipped as a client-side fallback into the bestiary/catalog/reveal panels only, leaving the one thing continuously on screen (the swim-canvas fish) exactly as primitive as before. A gap audit that reads the actual rendering code path, not just the task list, is what surfaces that kind of drift; filed as t-070, the highest-priority follow-up. Also: a live curl against the production host can independently confirm a delivery PR actually reached the deployed build (fingerprinted asset URLs serving 200) without needing a signed-out visual check -- useful evidence to attach to a needs-human task even when the subjective "does it look right" call still has to wait for the human.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-12T03:47:22Z_
