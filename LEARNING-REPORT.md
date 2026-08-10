# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-10T01:27:28Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **555**
- Outcomes: blocked: 13, cancelled: 1, done: 541
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
| interface-vision | 82 | 100% |
| kind-robots | 45 | 98% |
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
| software | 540 | 99% |

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

- 2026-08-09 `kind-robots/t-056` — A source-shape "guard test" (utils/scripts/verifyDatabasePoolDefaults.ts asserting a literal code string still appears in a route file) can break on an otherwise correct, intentional refactor -- the fix is usually to relocate the new behavior so the guarded shape survives unchanged, not to weaken the guard. Also: don't trust a PR body's "How I verified" section at face value -- independently re-running eslint/vue-tsc/the specific failing script on the actual current head caught a real TS2339 the Worker's own note had claimed was code/CI verified.

- 2026-08-09 `interface-vision/t-104` — Slice 26 of the kr-container consistency migration: four components (add-bot, add-character, add-reward, add-scenario) sharing an identical root class string were an exact byte-for-byte match for kr-container-wide's own @apply, found via a plain grep for the mx-auto/w-full/max-w-7xl triple across the repo rather than a codemod. Landed clean on the first pass, zero deviation from the established verification method (eslint, vue-tsc, layout-contract, git-stash-diffed prettier baseline check).

- 2026-08-09 `kind-robots/t-014` — When a roadmap task's original implementation gap is already present on current main and later human evidence confirms the feature works, reconcile and close the stale task instead of spawning a duplicate patch or repeatedly returning it to the human.
- 2026-08-09 `interface-vision/t-104` — Slice 20 of the kr-panel-flat consistency migration: applying t-116's corrected codemod scan to its own newly-surfaced 47-occurrence pool landed clean on the first pass with zero deviation from the established slice 8-19 method (exact-match substitution, git-stash-diffed prettier reformatting, compiled-CSS verification for skips). No new lesson beyond t-116's own record -- filed mainly so the outcome ledger reflects that the corrected pool is real, landable work, not just a diagnosis.

- 2026-08-09 `interface-vision/t-116` — A codemod's own "pool exhausted" conclusion is only as good as its scan boundary. kr_panel_codemod.py used re.search for the FIRST </template> in a file to find the template region's end, but an SFC can nest a named-slot/conditional <template v-if #slot> block that closes with its own </template> well before the real end -- silently truncating the scan and hiding every real candidate after it. Two prior slices (15, 18) trusted "0 automatable substitutions" as proof the pool was empty when it was actually an artifact of the scan bug. Fix: scan for the LAST </template> in the file, not the first. Re-running the corrected scan surfaced 47 previously-invisible candidates across 21 files in one pass -- a reminder that a static-analysis/codemod tool's exhaustion claim needs to be re-derived from its actual scan boundary, not taken at face value from its summary output.

- 2026-08-09 `conductor/t-110` — A default is a decision, and an unnamed one never gets reviewed. /api/art/enqueue resolved an omitted engine with `String(value || 'a1111')` — one word, no constant, no test — long after the relay stopped serving A1111, so "just enqueue this" meant "enqueue something that cannot render". The same shape hid a second bug next to it: buildDefaultComfyWorkflow passed a literal -1 seed into the KSampler where every sibling builder resolved a random one, pinning that lane to one image per Comfy install, and patchComfyWorkflow repeated the -1 immediately afterward so fixing only the builder would have been invisible. Both were invisible for the same reason — the value was inline, unnamed, and untested, so nothing ever asked whether it was still right. When a fallback decides behaviour for every caller that stays silent, give it a named constant and a test that states the intent; "krea2 is the default" and "an unspecified seed is random" are claims a test can hold, `|| 'a1111'` is not.

- 2026-08-09 `conductor/t-109` — When a hard gate will also be applied retroactively to an existing backlog, decide per-rule whether a pre-existing row should FAIL or be REPAIRED. kind_robots' prompt contract (2026-08-08) re-applies at claim time so pre-gate rows cannot render with stale settings — correct — but its only verdict was FAILED, so eight ArtJobs died on nothing but "krea2 runs at roughly 12 steps or fewer; got 20" with 27 more queued to die the same way. A step count above the engine's ceiling has one objectively correct repair and no authorial intent to preserve; rejecting it is not the conservative choice, just a different failure. Rules needing judgment (a conditional a diffusion model cannot evaluate, a format noun) must still fail. Two corollaries: a recovery endpoint that repairs everything EXCEPT the thing that killed the job is a loop, not a recovery (reenqueue-failed normalized paths/prompts/LoRAs but not the sampler); and fixing a per-engine DEFAULT without also bounding the explicit OVERRIDE leaves the door open at exactly the width of the original bug.

- 2026-08-09 `digital-storefront/t-038` — An umbrella task's remaining_scope_task pointer chain (t-038 -> t-003 -> t-004) can sit at status: review for days after its last referenced task actually reaches done, because nothing automatically re-checks the pointer once it stops changing. check_pr_merged_drift.py's title-search pass surfaced it only as "unverifiable" (no close-out PR titled after t-038 exists, since it was never meant to close via its own PR); the real signal was checking the remaining_scope_task's own status directly. A session picking up drift-check output should follow remaining_scope_task chains to their live end, not stop at "search found nothing."

- 2026-08-09 `kindrobots-unraid/t-006` — For self-hosted Node 24 services on Unraid, mounting one trusted .env and loading it with --env-file-if-exists avoids duplicating secrets while still allowing DockerMan environment variables to override deployment-specific keys. Excluding .env from the Docker build exposed a Prisma build dependency: prisma.config.ts requires DATABASE_URL even for generate, so image builds need a non-secret dead build-only URL rather than access to production credentials. Local Docker image tags can still be represented by a saved DockerMan template, keeping runtime settings editable in the Unraid WebGUI while registry publication remains optional.
- 2026-08-08 `digital-storefront/t-004` — A task note that frames N ad-hoc implementations as N variants of the same pattern can be wrong about that -- two of the four (Character, Reward) turned out to have no check at all, not a fourth variant. Dispatching a read-only investigation to re-verify the note's own framing before implementing caught this: "wire an existing check" and "add this route's first-ever check" are different risk categories (additive/behavior-preserving vs. a real behavior change for any caller relying on the open read), and conflating them would have either shipped an unreviewed security fix or silently dropped a real gap from the record. Split the genuinely mechanical pieces from the ones needing a human product decision rather than picking one bucket for the whole task.


---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-10T01:27:28Z_
