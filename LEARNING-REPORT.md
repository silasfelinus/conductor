# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-08T07:54:06Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **541**
- Outcomes: blocked: 13, cancelled: 1, done: 527
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
| conductor | 67 | 100% |
| conductor-app | 2 | 100% |
| davinci | 2 | 100% |
| digital-storefront | 26 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 4 | 100% |
| interface-vision | 76 | 100% |
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
| software | 526 | 99% |

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

- 2026-08-08 `interface-vision/t-108` — 4th fix attempt for the same bug finally worked: swapping an eager Image() probe for an IntersectionObserver-gated request restored native lazy-loading behavior AND kept the dedup benefit -- the 3rd attempt's Reviewer rejection (eager probe defeats loading="lazy", increases burst pressure) was correct and specific enough to fix in one retry without re-guessing. Reading the PR's own deployment-triggered audit RAW (not pass/fail) was again the only way to confirm the fix actually worked, and it also surfaced a genuinely unrelated regression (t-112's /taskmaster crush) in the same run -- worth remembering that a full-suite audit failing overall does not mean the specific route under test is still broken; read the specific route's lines before concluding either way.
- 2026-08-08 `digital-storefront/t-037` — A stack of roadmap tasks marked done (t-011..t-036) turned out to be almost entirely accurate against the real code when independently re-audited -- Mermaids PDF, subscriptions, mana top-ups, and the giving page were all genuinely BUILT-AND-VISIBLE end-to-end, and the prior tasks' own notes correctly predicted exactly where the remaining gaps would be (no KR-logo SKU, no live DLC catalog, no POD vendor integration). Dispatching a single read-only investigation subagent with a precise per-catalog-item checklist and an explicit 5-way classification (built-and-visible / built-but-unreachable / placeholder / delegated / missing) produced a citation-backed audit in one pass instead of several rounds of spot checks -- worth reusing this shape (structured checklist + forced classification + cite file:line) for any 're-verify a large already-done surface against reality' task.
- 2026-08-08 `interface-vision/t-112` — Batching independent-but-related small layout fixes into one PR (t-110+t-112, same audit run, same flexbox root cause pattern) avoided contending with the responsive-audit workflow's one-run-at-a-time serialization -- worth defaulting to when a slice's several small findings would otherwise each wait behind the same queue.
- 2026-08-08 `interface-vision/t-110` — kind_robots PR #1585 (batched t-110+t-112) was returned once by the reviewer for a repo-convention defect, not a functional one -- three large explanatory template comments added around the fix, violating kind_robots/AGENTS.md's 'avoid inline and template comments, let naming carry the meaning' rule. Worth checking that convention before writing comment blocks to justify a non-obvious CSS fix in kind_robots; put the reasoning in the PR description/roadmap note instead, where it already belongs per this repo's own template.
- 2026-08-08 `ai-art-academy/t-066` — @vite-pwa/nuxt's Nuxt module does NOT inject installability meta tags (viewport/ theme-color/apple-touch-icon) or the manifest <link> via useHead for an SSR app -- only a client-side SW-registration plugin and a nitro route for the manifest file itself. For any SSR (non-`nuxt generate`) app, those meta/link tags must be added explicitly in nuxt.config's app.head or they silently never render, even though the manifest file and service worker both build correctly. Worth checking directly against the built output (grep .output/public or curl the live site) rather than trusting the module's 'zero-config' framing for SSR specifically.
- 2026-08-07 `ai-art-academy/t-061` — For a "choose the smallest durable path" audit task, a direct filesystem/package.json search for the actual infra (PWA module, Capacitor config, native dirs, install-meta tags) beats guessing from feature docs -- kind_robots had zero mobile-delivery infrastructure despite an unrelated Flutter client (Conductor App) existing as a superficially similar precedent that turned out to share no code or relevance. Sequencing the follow-on tasks (PWA foundation before Android/iOS "builds") let t-062/t-063 stay scoped as PWA verification passes instead of full native pipelines, deferring the real cost (store accounts, code-signing, native build tooling) until Silas actually asks for store distribution.
- 2026-08-07 `interface-vision/t-107` — When a dead route has no obvious replacement, check whether the same codebase already encodes a canonical answer before guessing -- dashboardConfigs.builder's own defaultTab ('character' -> /characters) was the principled destination for two broken '/builder' nav entries, and git-blaming the referenced UI component (components/abandonware/builder/ builder-manager.vue) confirmed it had been deliberately parked as unreachable (kind_robots
- 2026-08-07 `interface-vision/t-102` — A static-analysis route inventory (grep the router/content config rather than crawl a live site) is enough to build an accurate numeric shrink-to-zero baseline for a reachability audit, and the process of building it is itself an effective way to surface real dead-route bugs -- two were found here (a stale /scenarios path live in three navigation payloads, fixed; a dead /builder path in two nav sources, filed as t-107 since its correct destination needed product judgment) that a pure documentation pass would have missed.
- 2026-08-07 `kind-robots/t-055` — Historical audit inventories should preserve their original findings while later path relocations are recorded as durable errata, avoiding noisy rewrites of completed audit notes.
- 2026-08-07 `conductor/t-103` — Fixed the third confirmed instance of process_task_events.py's rearm/ready/done path silently freezing a t-010-style recurring task's nested continuous_improvement counter (it only ever wrote top-level status/note fields). Took the schema-field approach the original task note flagged as easier than free-text note parsing: two new optional event fields (continuous_improvement_lane, continuous_improvement_pr) that a closing session sets explicitly, applied atomically alongside the normal status transition via the same pure update function bump_continuous_improvement.py's manual CLI already used. This closes the gap for future task-events-path close-outs but does not retroactively repair any already-stale counter -- a session hitting a drifted counter still needs to notice and hand-correct it once, same as before.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-08T07:54:06Z_
