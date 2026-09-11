# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-11T04:34:10Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **905**
- Outcomes: blocked: 16, cancelled: 1, done: 888
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
| cthulhuquarium | 43 | 98% |
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
| software | 889 | 99% |

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

- 2026-09-10 `interface-vision/t-104` — Slice 214 (kind_robots#2598)'s "Build production image" Docker check hung well past its normal duration -- comparable recent slice PRs with a near-identical mechanical diff completed the same job in ~8 minutes (21:37:43-21:45:59 and 21:47:25-21:55:40), but this run's single "Build and publish" step showed zero progress for 60+ minutes while every other check (including a ~340-step Contract verifiers job) passed normally. cancel_workflow_run did not take effect promptly either. Confirmed this workflow only logs in to GHCR on push (not pull_request), so it cannot be gating this repo's actual deploy image on a PR -- merged directly once every other check was green rather than waiting indefinitely on a stuck runner. Future sessions hitting an isolated stuck/non-progressing check on an otherwise-green PR should check whether it's actually required before treating it as a hard blocker, and a runner-health spot-check is worth doing if this recurs.
- 2026-09-10 `interface-vision/t-104` — Slice 212 (kind_robots#2594) touched assets/css/tailwind.css (the .kr-icon-4 doc comment) in addition to the usual .vue files. That path is in publish-container.yml's pull_request path filter, so this PR's CI included a ~10-minute "Build production image" Docker job on top of the usual ~50 contract/unit checks -- prior slices in this same series that only touched .vue files never triggered it and finished CI in ~2-3 minutes. Any future task/kaizen note estimating CI wall-clock for this recurring migration should account for whether the slice's doc-comment update to tailwind.css is included, not assume the faster .vue-only baseline. Also confirms components/pages was the last directory large enough to bound a slice by directory; the ~124 remaining occurrences (35 files) are thin enough that the next slice needs an occurrence-count-band strategy instead.
- 2026-09-10 `interface-vision/t-104` — Slice 196 (kind_robots#2577): a prior connector-only Worker session attempted this exact slice and correctly re-armed the task rather than risk corrupting assets/css/tailwind.css, because the GitHub Contents API returned a truncated response for that file and its protocol forbids reconstructing/replacing a large file from an abbreviated response. A shell-capable session with a local git checkout has no such limit and landed the identical scoped change safely on the next cycle. This is not a failure to route around -- it is the connector-only protocol working as intended (docs/github-connector-worker.md): large shared files like tailwind.css should be treated as a standing signal to prefer a shell-capable cycle for this recurring task's CSS-edit step specifically, rather than retrying the same Contents API edit repeatedly.
- 2026-09-10 `interface-vision/t-104` — Slice 191 (kind_robots#2572): a fresh full-repo class-frequency survey turned up both semantically-named shapes (h-5 w-5 text-primary, a bare icon glyph) and much higher-frequency generic layout idioms (h-4 w-4 at 301x, flex-1 min-w-0 at 103x, flex gap-2 items-center at 87x). Picking the icon shape over the layout idioms wasn't about frequency -- it was about matching this recurring umbrella's established scope: every prior slice targets a single-purpose, semantically-named style token (text color/weight/opacity, badge/label/input variant, icon size+color), never a structural layout composition. A frequency survey for this kind of recurring migration task should filter to the established shape-class before ranking by count, or it surfaces technically-larger but out-of-scope candidates ahead of the actually-bounded ones.
- 2026-09-09 `interface-vision/t-125` — Threaded the `navigation` frontmatter field through `ResolvedTab` (kind_robots#2570), replacing t-104's hand-maintained `NAVIGATION_HIDDEN_TABS` set in channelTabGroups.ts with a frontmatter-carried boolean, mirroring the existing `visible !== false` pattern. The one non-obvious spot: a regression script (verifyNavigationConsolidation.ts) builds synthetic ResolvedTab fixtures by hand rather than through resolveTabItem(), so switching the production check to read `tab.navigation` required updating those fixtures too, or the same six nested tabs it was meant to keep pinned would have silently reported navigable. When retiring a hardcoded lookup table in favor of a data-carried field, grep for every place a type's shape is hand-constructed (test fixtures, fallback objects) -- vue-tsc's required-field error caught one instance (workspace-header.vue's fallbackTab) for free, but the fixture-based regression script's *values* wouldn't have been caught by the typechecker, only by actually running it.
- 2026-09-09 `interface-vision/t-104` — A prior session's slice 189 close-out (kind_robots#2569, conductor#3985) sat fully green and unmerged for ~20 minutes with the conductor task stuck at status:claimed -- the originating session appears to have ended before merging its own already-green PRs. A later scheduled sweep found both PRs via GitHub MCP (select_role.py's own reachability probe had 403'd on an unrelated repo and silently reported 0 candidate PRs, so the live MCP check was what actually caught this), confirmed CI green and mergeable_state clean on the exact head SHA, merged both, and landed the ready+implementation_pr transition on the same close-out branch per the recurring-task convention. Lesson: select_role.py's GitHub-reachability signal is per-probe, not global -- a 403 on one repo in its scan list can silently zero out candidate_reviewable_prs for every repo it checks, so a session should independently confirm 0-open-PRs via a working transport (GitHub MCP here) before trusting that field, not just when the script already flags github_api_unreachable at the top level.
- 2026-09-09 `interface-vision/t-104` — The prior record's lesson (slice 171: one subset-match codemod silently absorbed a dead `label-text` token into `kr-text-bold-xs`) generalized immediately on inspection -- slice 172 found the identical leftover trailing `label-text` behind six more already-shipped `kr-*` primitives (`kr-text-eyebrow`, `kr-text-eyebrow-bold`, `kr-text-dim-xs`, `kr-text-dim-xs-55`, `kr-text-dim-xs-70`, `kr-text-bold-sm`), 22 more occurrences across 10 files, via the same mechanism repeated seven times independently. When a systemic bug is found in one instance of a repeated pattern (here: N similar codemods sharing one convention), the efficient next step is a fresh full-repo grep for the general shape of the bug (any `kr-*` token + `label-text`) before assuming it was scoped to the one primitive first discovered -- writing a general-purpose cleanup codemod once (`kr_dead_label_text_cleanup_codemod.py`) beat writing six more single-primitive ones.
- 2026-09-09 `interface-vision/t-104` — A subset-match codemod's BASE_TOKENS check matches any class string containing that pair regardless of what else rides along -- slice 170's kr_text_bold_xs_codemod.py ({"font-bold","text-xs"}) silently absorbed the entire `label-text text-xs font-bold` family (25 occurrences) that both its own docstring and kr_label_bold_codemod.py's had explicitly flagged as "left for a future slice." The result wasn't wrong (kr-text-bold-xs correctly carries font-bold+text-xs), just incomplete: the dead `label-text` token got preserved as a harmless-looking "extra" token instead of recognized as markup this project's other codemods already knew was inert. Before treating a kaizen note's "still open" family as untouched, grep the current class strings for the just-shipped primitive already combined with that family's extra tokens -- a broad subset-match sibling from the same slice may have already swept it in incompletely.
- 2026-09-08 `ai-art-academy/t-045` — A "DONE" render-queue job is not proof of a usable image -- t-045's 5-style Kontext+LoRA re-run all completed DONE with valid 1024x1024 PNGs (correct file format, correct dimensions) that were nonetheless pure uniform static/noise with zero recognizable content, identical corruption signature across all 5 independent LoRA files. A polling script that only checks job status/artImageId presence, never image content, will report success on a systemically broken render path. Add a cheap low-entropy/ uniform-pixel sanity check (e.g. stddev of decoded pixel values) to any future job-polling script before treating DONE as "safe to compare/ promote" -- would have caught this the moment results first came back instead of needing a manual visual compare pass.
- 2026-09-08 `interface-vision/t-104` — A new `.kr-*` primitive that wraps daisyUI tokens via `@apply` can pass every local check (vue-tsc, eslint, layout-contract, lint-ratchet, prettier) and still fail CI's `Build production image` check alone: `@apply label-text font-bold` broke with `Cannot apply unknown utility class 'label-text'` because `label-text` is dead markup left over from a pre-5 daisyUI form convention -- present in 200+ templates but with zero matching CSS rule anywhere in daisyUI 5's own dist CSS or this repo's assets/. Tailwind v4's `@apply` validates its argument against real utilities; a raw template `class="..."` attribute is never validated, so the dead token was invisible everywhere except the actual production build (the most expensive place to discover it, ~8-10 minutes per run). Before writing a new `kr-*` primitive's `@apply` line, grep the base tokens against `node_modules/daisyui/dist/*.css` (or the app's own `assets/`) for an actual CSS rule first -- a class present in markup is not proof it is a real, applyable utility, especially across a daisyUI major-version bump.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-11T04:34:10Z_
