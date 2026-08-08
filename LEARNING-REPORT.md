# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-08T21:40:23Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **545**
- Outcomes: blocked: 13, cancelled: 1, done: 531
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
| conductor | 68 | 100% |
| conductor-app | 2 | 100% |
| davinci | 2 | 100% |
| digital-storefront | 26 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 4 | 100% |
| interface-vision | 79 | 100% |
| kind-robots | 43 | 98% |
| kindrobots-unraid | 4 | 100% |
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
| software | 530 | 99% |

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

- 2026-08-08 `interface-vision/t-114` — When a ratchet-baseline check's --update refuses to seed a brand-new rule (grownRatchetBuckets treats a bucket absent from the prior baseline as zero, so any pre-existing count reads as growth), that refusal is deliberate design, not a bootstrap bug -- see ratchetBaseline.ts's own doc comment. The correct move is to hand-seed the baseline JSON with the rule's current findings (generated via --report, not transcribed by hand) rather than to "fix" the shared ratchet helper. A brand-new rule with real pre-existing violations should grandfather them explicitly and let only new violations fail CI going forward -- exactly the same contract every other rule in the file already has.

- 2026-08-08 `interface-vision/t-103` — This umbrella took 6 slices plus 5 regression-chase sub-tasks (t-108 through t-113) to reach a genuinely zero-finding raw audit -- each "fixed" claim needed the PR's own deployment-triggered audit read RAW (not the pass/fail summary) before trusting it, and two of the five sub-tasks had a first fix attempt that looked plausible but was later disproven by a fresh raw read. The pattern that finally closed it: re-diagnose from current main instead of assuming a prior fix's approach still applies, and treat "audit conclusion: success" as necessary but not sufficient -- always grep the specific route/viewport lines.

- 2026-08-08 `interface-vision/t-113` — A prior fix attempt (t-112, PR #1585) removed a viewport-based breakpoint but left the shared ingredient-picker grid keyed to viewport width rather than container width -- it passed the audit at the time because the audit's viewport set didn't hit the exact narrow-host case, then regressed for real once /taskmaster placed the picker inside a narrower panel. Switching to a container-aware auto-fit grid (minmax with a min card width) is the general fix for "shared component crushes inside one specific narrow host" -- prefer it over another viewport-breakpoint patch when a regression repeats on the same component in a new host context.

- 2026-08-08 `conductor/t-104` — workflow-medic's own watch list only had one entry (process-task-events.yml) because it had never been exercised against real live-run history -- pulling that history for the "should we widen it" decision immediately surfaced a genuine 2+ day silent failure streak on hourly-conductor.yml (a script retrying an already-known-partial item forever instead of short-circuiting on it). Always pull real data before making a "should we expand monitoring" decision; mocked-test coverage alone can hide the exact class of incident the monitoring exists to catch.

- 2026-08-08 `interface-vision/t-108` — 4th fix attempt for the same bug finally worked: swapping an eager Image() probe for an IntersectionObserver-gated request restored native lazy-loading behavior AND kept the dedup benefit -- the 3rd attempt's Reviewer rejection (eager probe defeats loading="lazy", increases burst pressure) was correct and specific enough to fix in one retry without re-guessing. Reading the PR's own deployment-triggered audit RAW (not pass/fail) was again the only way to confirm the fix actually worked, and it also surfaced a genuinely unrelated regression (t-112's /taskmaster crush) in the same run -- worth remembering that a full-suite audit failing overall does not mean the specific route under test is still broken; read the specific route's lines before concluding either way.
- 2026-08-08 `digital-storefront/t-037` — A stack of roadmap tasks marked done (t-011..t-036) turned out to be almost entirely accurate against the real code when independently re-audited -- Mermaids PDF, subscriptions, mana top-ups, and the giving page were all genuinely BUILT-AND-VISIBLE end-to-end, and the prior tasks' own notes correctly predicted exactly where the remaining gaps would be (no KR-logo SKU, no live DLC catalog, no POD vendor integration). Dispatching a single read-only investigation subagent with a precise per-catalog-item checklist and an explicit 5-way classification (built-and-visible / built-but-unreachable / placeholder / delegated / missing) produced a citation-backed audit in one pass instead of several rounds of spot checks -- worth reusing this shape (structured checklist + forced classification + cite file:line) for any 're-verify a large already-done surface against reality' task.
- 2026-08-08 `interface-vision/t-112` — Batching independent-but-related small layout fixes into one PR (t-110+t-112, same audit run, same flexbox root cause pattern) avoided contending with the responsive-audit workflow's one-run-at-a-time serialization -- worth defaulting to when a slice's several small findings would otherwise each wait behind the same queue.
- 2026-08-08 `interface-vision/t-110` — kind_robots PR #1585 (batched t-110+t-112) was returned once by the reviewer for a repo-convention defect, not a functional one -- three large explanatory template comments added around the fix, violating kind_robots/AGENTS.md's 'avoid inline and template comments, let naming carry the meaning' rule. Worth checking that convention before writing comment blocks to justify a non-obvious CSS fix in kind_robots; put the reasoning in the PR description/roadmap note instead, where it already belongs per this repo's own template.
- 2026-08-08 `ai-art-academy/t-066` — @vite-pwa/nuxt's Nuxt module does NOT inject installability meta tags (viewport/ theme-color/apple-touch-icon) or the manifest <link> via useHead for an SSR app -- only a client-side SW-registration plugin and a nitro route for the manifest file itself. For any SSR (non-`nuxt generate`) app, those meta/link tags must be added explicitly in nuxt.config's app.head or they silently never render, even though the manifest file and service worker both build correctly. Worth checking directly against the built output (grep .output/public or curl the live site) rather than trusting the module's 'zero-config' framing for SSR specifically.
- 2026-08-07 `ai-art-academy/t-061` — For a "choose the smallest durable path" audit task, a direct filesystem/package.json search for the actual infra (PWA module, Capacitor config, native dirs, install-meta tags) beats guessing from feature docs -- kind_robots had zero mobile-delivery infrastructure despite an unrelated Flutter client (Conductor App) existing as a superficially similar precedent that turned out to share no code or relevance. Sequencing the follow-on tasks (PWA foundation before Android/iOS "builds") let t-062/t-063 stay scoped as PWA verification passes instead of full native pipelines, deferring the real cost (store accounts, code-signing, native build tooling) until Silas actually asks for store distribution.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-08T21:40:23Z_
