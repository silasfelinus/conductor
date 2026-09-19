# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-19T02:54:12Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1043**
- Outcomes: blocked: 16, cancelled: 1, done: 1026
- Success rate: **98%**
- Average passes on successful tasks: **0.2**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 73 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 14 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 11 | 100% |
| approval-portal | 2 | 0% |
| art-archive | 15 | 100% |
| art-generator-connect | 3 | 100% |
| brainstorm | 26 | 96% |
| butterfly-gallery | 19 | 100% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 39 | 100% |
| conductor | 120 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 51 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 24 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 136 | 100% |
| kapowarr | 52 | 100% |
| kind-economy | 10 | 100% |
| kind-robots | 65 | 98% |
| kindrobots-unraid | 9 | 100% |
| lora-ingestion | 1 | 100% |
| mandarin-tutor | 11 | 100% |
| media-watchlist | 12 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 85 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| rainbow-butterflies | 21 | 100% |
| ruler-hooked | 14 | 100% |
| scene-animator | 2 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 30 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 7 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 1026 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 32 |
| transient | 17 |
| actionable | 15 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 47% success over 17 closed tasks; aim the next kaizen task here
- failure category `quality` — 32 occurrences; look for the shared cause across its records
- failure category `transient` — 17 occurrences; look for the shared cause across its records
- failure category `actionable` — 15 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-19 `butterfly-gallery/t-026` — Once a fixture provider and a real-backed provider both implement the same read contract (ButterflyGalleryFeedProvider here), a plain Object.keys().sort() shape-equality check across representative field-presence variants (nulls, missing optional fields, nested objects) is enough to catch a future field drop/rename on either side -- no need for a heavier structural-diff library. Comparing sorted key lists rather than deep-equal values keeps the test focused on shape parity, not incidental value differences between fixture and real data.
- 2026-09-19 `butterfly-gallery/t-028` — Wiring rendered ArtImage assets into placeholder CSS shapes reads cleanly when each replacement keeps the prior gradient/color as a literal CSS fallback layer (multi-background for gradients, `background: <color> url(...) center / cover no-repeat` shorthand for solid colors) rather than swapping the property outright -- a failed image load then degrades to the exact prior look with no extra code. Where a solid color carries semantic meaning (the five preset-bin variants: error/warning/accent/ success/info), `background-blend-mode: multiply` layers the art texture over the color instead of replacing it, preserving the color-coding. Border-thickness-sensitive replacements (a picture-frame graphic meant to become an actual `border-image`) are safer left as a `background` layer behind the existing CSS border when there is no PR-preview infra to verify pixel alignment pre-merge (this repo's post-Vercel-migration state) -- flag it as a documented follow-up rather than guessing at border-image slice values blind.
- 2026-09-19 `butterfly-gallery/t-022` — A task whose note implies broad scope ("a real art-archive-backed adapter swaps in later under t-022" -- from a sibling task's note, not t-022's own) is worth deliberately re-scoping to what the task's own title actually promises (here: the feed) plus only the sub-pieces with a clean 1:1 real-endpoint mapping, rather than either inventing unreviewed infrastructure (a schema migration, an id-resolution endpoint) to cover every implied piece or silently dropping them. Filing the honest gap as its own task (t-029) kept the delivered slice verifiable and reversible. Separately: real Nuxt-runtime code (anything importing stores/utils.ts, which pulls in stores/userStore.ts's snapshotLoader.ts) cannot be statically imported by a module a plain-tsx contract test also imports -- it crashes on import.meta.glob outside Vite. Keep the Nuxt-runtime-backed implementation in its own module and install it via a client plugin (setXFeedProvider()/setXActionAdapter() at app startup) rather than wiring it as the fixture module's own default.
- 2026-09-18 `butterfly-gallery/t-027` — When one bin/action kind in a family that's otherwise uniform (here: five of six ButterflyGalleryActionAdapter-backed bin kinds both mutate local state and persist through the adapter) silently skips the adapter call, grep the sibling switch statement (persistBinOutcome) for the same case rather than assuming a local-only mutation (applyBinOutcome's entry.matchState write) was a deliberate design choice -- it was a silent no-op instead, exactly the kind of gap a future real adapter swap (t-022) would otherwise inherit unnoticed.
- 2026-09-18 `art-archive/t-025` — When a task's target type is an untyped Record<string, unknown> (ArtJobPayloadRecord), check which concrete payload shape the field names actually mirror (here: A1111's flat fields, not a COMFY engine's built workflow graph) and say so explicitly in the PR rather than silently assuming the merge covers every engine.
- 2026-09-18 `butterfly-gallery/t-018` — A new component this repo's test:component-reachability check can't reach (not mounted anywhere from app.vue/pages/layouts/content) fails CI deterministically regardless of how clean the rest of the diff is. A "scoped slice" that adds a component should mount it behind even a minimal admin toggle in the same PR, not defer wiring to a following slice -- the reachability check is a hard invariant on every PR, not advisory.
- 2026-09-18 `kind-robots/t-110` — A container-log "Data too long for column" truncation warning is worth escalating immediately, not just noting: it means writes are already succeeding with silently corrupted data. This one (imagePath, since kind_robots#2814) escalated from a warning to hard ArtJob write failures (HTTP 500) within two days once enough long static-path values accumulated. When one column in a family of otherwise-consistent columns (13 other imagePath fields already at VarChar(764)) is the odd one left at Prisma's implicit VarChar(191) default, that inconsistency is itself the signal to check for -- grep every same-named column across the schema before assuming a single reported failure is isolated.
- 2026-09-18 `art-archive/t-013` — A field can be filterable and displayed in an admin browser for a while before anyone notices nothing ever writes it -- when a task note says "expose fast rating actions" for a field that already exists in the schema and the read path, check the write path specifically before assuming only UI wiring is missing.
- 2026-09-18 `art-archive/t-012` — Quarantine ("delete") from t-009 overwrote relativePath with the trash path and threw the original location away, so a "recoverable trash" task needs a place to remember where a file came from before it can add restore -- don't assume an existing quarantine/soft-delete action is already restore-ready just because it preserves the row via isActive: false. Also: `prisma format`/`prisma generate` in this sandbox reformats every .prisma file and regenerates the whole client, not just the one touched -- always diff and revert unrelated files before committing a schema change.
- 2026-09-18 `storybook/t-049` — A stale status: claimed with a note saying "releasing the claim" is a real drift, not just a stale note -- always re-check whether the described outcome actually landed in the status field before trusting the note. Separately: GitHub MCP create_or_update_file's content parameter is plain text, never pre-base64-encoded -- passing already-encoded content silently writes the base64 string itself as file content; verify a push by re-fetching real content, not just the tool's size/sha response.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-19T02:54:12Z_
