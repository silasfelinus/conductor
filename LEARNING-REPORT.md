# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-11T14:46:41Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **910**
- Outcomes: blocked: 16, cancelled: 1, done: 893
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
| cthulhuquarium | 48 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 23 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 116 | 100% |
| kapowarr | 52 | 100% |
| kind-economy | 9 | 100% |
| kind-robots | 55 | 98% |
| kindrobots-unraid | 6 | 100% |
| lora-ingestion | 1 | 100% |
| mandarin-tutor | 11 | 100% |
| media-watchlist | 11 | 100% |
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
| content | 16 | 44% |
| software | 894 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 17 |
| transient | 15 |
| actionable | 13 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 17 occurrences; look for the shared cause across its records
- failure category `transient` — 15 occurrences; look for the shared cause across its records
- failure category `actionable` — 13 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-11 `cthulhuquarium/t-072` — Investigated both halves of the task before touching code, and that investigation changed the plan: the roadmap note offered "fix the path or delete" the dead importCthulhuquariumArt.mjs script as two equally valid options, but reading the actual delivered assets showed the script's per-prefix resize scheme (1280/960/640/512px by filename prefix) doesn't match what the real delivery (kind_robots#2620) actually shipped (uniform 512px-long-edge) -- "fixing" the path would have silently overwritten already-correct committed assets with differently-sized ones. Deletion was the only safe choice once that was known, not a coin flip. Separately, the task's other half (bulk-creating real ArtImage DB records and linking them to Monster rows) was real, well-precedented, buildable work -- but this sandbox has zero path to any live database (confirmed: no .env, dummy-only DATABASE_URL in the provisioning script, no reachable DB port) -- so attempting it here would have produced an unverifiable script at best. Split it into its own task (t-076) with the investigation's findings attached, rather than either skipping it silently or attempting unverifiable DB work. Pattern worth repeating: when a roadmap task bundles a quick fix with something that needs infrastructure this sandbox doesn't have, do the quick part, investigate the rest thoroughly enough to leave a real trail, and split rather than stall.
- 2026-09-11 `cthulhuquarium/t-070` — Filed directly by t-068's FULL-GAME-GAP-AUDIT.md as the highest-priority follow-up: t-065's earlier art-delivery fix only reached kr-art-plate calls in the bestiary/catalog/reveal-dialog panels, never the swim-canvas render loop (drawFish() in cthulhuquarium-game.vue), which is the one thing a player watches continuously. Fixed with a minimal, backward-compatible change -- a lazy per-slug HTMLImageElement cache feeding context.drawImage(), falling back to the original primitive silhouette when no art is cached yet or fails to load -- rather than a riskier rewrite of the render loop. Kept the existing hunger-based saturate()/globalAlpha desaturation and context.scale(facing, 1) flip behavior identical on both paths so the change is additive, not a redesign. Verified via eslint, vue-tsc --noEmit, prettier --check, and the full 46-check kind_robots CI suite (all green, including Contract verifiers and TypeScript) -- no visual/browser confirmation was possible from this sandbox, which is an honest gap worth a human spot-check on kindrobots.org next time the tank is opened, same caveat t-068 already flagged for the bestiary fix.
- 2026-09-11 `cthulhuquarium/t-068` — A roadmap can read 63-68/68 done while the game still fails the owner's own look, because "done" tracked whether a task closed, not whether its output reached the player -- t-065's art shipped as a client-side fallback into the bestiary/catalog/reveal panels only, leaving the one thing continuously on screen (the swim-canvas fish) exactly as primitive as before. A gap audit that reads the actual rendering code path, not just the task list, is what surfaces that kind of drift; filed as t-070, the highest-priority follow-up. Also: a live curl against the production host can independently confirm a delivery PR actually reached the deployed build (fingerprinted asset URLs serving 200) without needing a signed-out visual check -- useful evidence to attach to a needs-human task even when the subjective "does it look right" call still has to wait for the human.
- 2026-09-11 `cthulhuquarium/t-067` — kr-art-plate's shape="plate" aspect box always carries an internal w-full class, so a consumer's own size-* class loses the width cascade at equal specificity -- kr-entity-card-body.vue already hit and documented this exact bug for /characters icons (2026-08-05); grep for shape="plate"/"card"/etc. plus an external size-*/w-*/h-* class on any kr-art-plate call site before assuming a new report is a new bug.
- 2026-09-11 `cthulhuquarium/t-066` — Root cause was in a shared wrapper (components/conductor/project-front-page.vue), not the page that surfaced the symptom (aquarium): its view.description computed preferred the live Conductor-synced Project.description field over the page's own authored fallback, and that live field is seeded once from notesFromSilas (raw internal dictation) and never refreshed. Checking every other caller of the shared component before changing its default precedence (all of them already supplied their own description, so the fix was a safe no-op everywhere else) turned a single-page bug report into a fix for the whole class, at no extra risk.
- 2026-09-10 `interface-vision/t-104` — Slice 214 (kind_robots#2598)'s "Build production image" Docker check hung well past its normal duration -- comparable recent slice PRs with a near-identical mechanical diff completed the same job in ~8 minutes (21:37:43-21:45:59 and 21:47:25-21:55:40), but this run's single "Build and publish" step showed zero progress for 60+ minutes while every other check (including a ~340-step Contract verifiers job) passed normally. cancel_workflow_run did not take effect promptly either. Confirmed this workflow only logs in to GHCR on push (not pull_request), so it cannot be gating this repo's actual deploy image on a PR -- merged directly once every other check was green rather than waiting indefinitely on a stuck runner. Future sessions hitting an isolated stuck/non-progressing check on an otherwise-green PR should check whether it's actually required before treating it as a hard blocker, and a runner-health spot-check is worth doing if this recurs.
- 2026-09-10 `interface-vision/t-104` — Slice 212 (kind_robots#2594) touched assets/css/tailwind.css (the .kr-icon-4 doc comment) in addition to the usual .vue files. That path is in publish-container.yml's pull_request path filter, so this PR's CI included a ~10-minute "Build production image" Docker job on top of the usual ~50 contract/unit checks -- prior slices in this same series that only touched .vue files never triggered it and finished CI in ~2-3 minutes. Any future task/kaizen note estimating CI wall-clock for this recurring migration should account for whether the slice's doc-comment update to tailwind.css is included, not assume the faster .vue-only baseline. Also confirms components/pages was the last directory large enough to bound a slice by directory; the ~124 remaining occurrences (35 files) are thin enough that the next slice needs an occurrence-count-band strategy instead.
- 2026-09-10 `interface-vision/t-104` — Slice 196 (kind_robots#2577): a prior connector-only Worker session attempted this exact slice and correctly re-armed the task rather than risk corrupting assets/css/tailwind.css, because the GitHub Contents API returned a truncated response for that file and its protocol forbids reconstructing/replacing a large file from an abbreviated response. A shell-capable session with a local git checkout has no such limit and landed the identical scoped change safely on the next cycle. This is not a failure to route around -- it is the connector-only protocol working as intended (docs/github-connector-worker.md): large shared files like tailwind.css should be treated as a standing signal to prefer a shell-capable cycle for this recurring task's CSS-edit step specifically, rather than retrying the same Contents API edit repeatedly.
- 2026-09-10 `interface-vision/t-104` — Slice 191 (kind_robots#2572): a fresh full-repo class-frequency survey turned up both semantically-named shapes (h-5 w-5 text-primary, a bare icon glyph) and much higher-frequency generic layout idioms (h-4 w-4 at 301x, flex-1 min-w-0 at 103x, flex gap-2 items-center at 87x). Picking the icon shape over the layout idioms wasn't about frequency -- it was about matching this recurring umbrella's established scope: every prior slice targets a single-purpose, semantically-named style token (text color/weight/opacity, badge/label/input variant, icon size+color), never a structural layout composition. A frequency survey for this kind of recurring migration task should filter to the established shape-class before ranking by count, or it surfaces technically-larger but out-of-scope candidates ahead of the actually-bounded ones.
- 2026-09-09 `interface-vision/t-125` — Threaded the `navigation` frontmatter field through `ResolvedTab` (kind_robots#2570), replacing t-104's hand-maintained `NAVIGATION_HIDDEN_TABS` set in channelTabGroups.ts with a frontmatter-carried boolean, mirroring the existing `visible !== false` pattern. The one non-obvious spot: a regression script (verifyNavigationConsolidation.ts) builds synthetic ResolvedTab fixtures by hand rather than through resolveTabItem(), so switching the production check to read `tab.navigation` required updating those fixtures too, or the same six nested tabs it was meant to keep pinned would have silently reported navigable. When retiring a hardcoded lookup table in favor of a data-carried field, grep for every place a type's shape is hand-constructed (test fixtures, fallback objects) -- vue-tsc's required-field error caught one instance (workspace-header.vue's fallbackTab) for free, but the fixture-based regression script's *values* wouldn't have been caught by the typechecker, only by actually running it.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-11T14:46:41Z_
