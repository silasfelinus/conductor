# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-09T11:56:42Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **550**
- Outcomes: blocked: 13, cancelled: 1, done: 536
- Success rate: **97%**
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
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 25 | 100% |
| conductor | 70 | 100% |
| conductor-app | 2 | 100% |
| davinci | 2 | 100% |
| digital-storefront | 28 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 4 | 100% |
| interface-vision | 79 | 100% |
| kind-robots | 43 | 98% |
| kindrobots-unraid | 5 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 48 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 2 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 535 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 10 |
| actionable | 9 |
| transient | 9 |
| scope | 2 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `quality` — 10 occurrences; look for the shared cause across its records
- failure category `actionable` — 9 occurrences; look for the shared cause across its records
- failure category `transient` — 9 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-09 `conductor/t-110` — A default is a decision, and an unnamed one never gets reviewed. /api/art/enqueue resolved an omitted engine with `String(value || 'a1111')` — one word, no constant, no test — long after the relay stopped serving A1111, so "just enqueue this" meant "enqueue something that cannot render". The same shape hid a second bug next to it: buildDefaultComfyWorkflow passed a literal -1 seed into the KSampler where every sibling builder resolved a random one, pinning that lane to one image per Comfy install, and patchComfyWorkflow repeated the -1 immediately afterward so fixing only the builder would have been invisible. Both were invisible for the same reason — the value was inline, unnamed, and untested, so nothing ever asked whether it was still right. When a fallback decides behaviour for every caller that stays silent, give it a named constant and a test that states the intent; "krea2 is the default" and "an unspecified seed is random" are claims a test can hold, `|| 'a1111'` is not.

- 2026-08-09 `conductor/t-109` — When a hard gate will also be applied retroactively to an existing backlog, decide per-rule whether a pre-existing row should FAIL or be REPAIRED. kind_robots' prompt contract (2026-08-08) re-applies at claim time so pre-gate rows cannot render with stale settings — correct — but its only verdict was FAILED, so eight ArtJobs died on nothing but "krea2 runs at roughly 12 steps or fewer; got 20" with 27 more queued to die the same way. A step count above the engine's ceiling has one objectively correct repair and no authorial intent to preserve; rejecting it is not the conservative choice, just a different failure. Rules needing judgment (a conditional a diffusion model cannot evaluate, a format noun) must still fail. Two corollaries: a recovery endpoint that repairs everything EXCEPT the thing that killed the job is a loop, not a recovery (reenqueue-failed normalized paths/prompts/LoRAs but not the sampler); and fixing a per-engine DEFAULT without also bounding the explicit OVERRIDE leaves the door open at exactly the width of the original bug.

- 2026-08-09 `digital-storefront/t-038` — An umbrella task's remaining_scope_task pointer chain (t-038 -> t-003 -> t-004) can sit at status: review for days after its last referenced task actually reaches done, because nothing automatically re-checks the pointer once it stops changing. check_pr_merged_drift.py's title-search pass surfaced it only as "unverifiable" (no close-out PR titled after t-038 exists, since it was never meant to close via its own PR); the real signal was checking the remaining_scope_task's own status directly. A session picking up drift-check output should follow remaining_scope_task chains to their live end, not stop at "search found nothing."

- 2026-08-09 `kindrobots-unraid/t-006` — For self-hosted Node 24 services on Unraid, mounting one trusted .env and loading it with --env-file-if-exists avoids duplicating secrets while still allowing DockerMan environment variables to override deployment-specific keys. Excluding .env from the Docker build exposed a Prisma build dependency: prisma.config.ts requires DATABASE_URL even for generate, so image builds need a non-secret dead build-only URL rather than access to production credentials. Local Docker image tags can still be represented by a saved DockerMan template, keeping runtime settings editable in the Unraid WebGUI while registry publication remains optional.
- 2026-08-08 `digital-storefront/t-004` — A task note that frames N ad-hoc implementations as N variants of the same pattern can be wrong about that -- two of the four (Character, Reward) turned out to have no check at all, not a fourth variant. Dispatching a read-only investigation to re-verify the note's own framing before implementing caught this: "wire an existing check" and "add this route's first-ever check" are different risk categories (additive/behavior-preserving vs. a real behavior change for any caller relying on the open read), and conflating them would have either shipped an unreviewed security fix or silently dropped a real gap from the record. Split the genuinely mechanical pieces from the ones needing a human product decision rather than picking one bucket for the whole task.

- 2026-08-08 `interface-vision/t-114` — When a ratchet-baseline check's --update refuses to seed a brand-new rule (grownRatchetBuckets treats a bucket absent from the prior baseline as zero, so any pre-existing count reads as growth), that refusal is deliberate design, not a bootstrap bug -- see ratchetBaseline.ts's own doc comment. The correct move is to hand-seed the baseline JSON with the rule's current findings (generated via --report, not transcribed by hand) rather than to "fix" the shared ratchet helper. A brand-new rule with real pre-existing violations should grandfather them explicitly and let only new violations fail CI going forward -- exactly the same contract every other rule in the file already has.

- 2026-08-08 `interface-vision/t-103` — This umbrella took 6 slices plus 5 regression-chase sub-tasks (t-108 through t-113) to reach a genuinely zero-finding raw audit -- each "fixed" claim needed the PR's own deployment-triggered audit read RAW (not the pass/fail summary) before trusting it, and two of the five sub-tasks had a first fix attempt that looked plausible but was later disproven by a fresh raw read. The pattern that finally closed it: re-diagnose from current main instead of assuming a prior fix's approach still applies, and treat "audit conclusion: success" as necessary but not sufficient -- always grep the specific route/viewport lines.

- 2026-08-08 `interface-vision/t-113` — A prior fix attempt (t-112, PR #1585) removed a viewport-based breakpoint but left the shared ingredient-picker grid keyed to viewport width rather than container width -- it passed the audit at the time because the audit's viewport set didn't hit the exact narrow-host case, then regressed for real once /taskmaster placed the picker inside a narrower panel. Switching to a container-aware auto-fit grid (minmax with a min card width) is the general fix for "shared component crushes inside one specific narrow host" -- prefer it over another viewport-breakpoint patch when a regression repeats on the same component in a new host context.

- 2026-08-08 `conductor/t-104` — workflow-medic's own watch list only had one entry (process-task-events.yml) because it had never been exercised against real live-run history -- pulling that history for the "should we widen it" decision immediately surfaced a genuine 2+ day silent failure streak on hourly-conductor.yml (a script retrying an already-known-partial item forever instead of short-circuiting on it). Always pull real data before making a "should we expand monitoring" decision; mocked-test coverage alone can hide the exact class of incident the monitoring exists to catch.

- 2026-08-08 `interface-vision/t-108` — 4th fix attempt for the same bug finally worked: swapping an eager Image() probe for an IntersectionObserver-gated request restored native lazy-loading behavior AND kept the dedup benefit -- the 3rd attempt's Reviewer rejection (eager probe defeats loading="lazy", increases burst pressure) was correct and specific enough to fix in one retry without re-guessing. Reading the PR's own deployment-triggered audit RAW (not pass/fail) was again the only way to confirm the fix actually worked, and it also surfaced a genuinely unrelated regression (t-112's /taskmaster crush) in the same run -- worth remembering that a full-suite audit failing overall does not mean the specific route under test is still broken; read the specific route's lines before concluding either way.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-09T11:56:42Z_
