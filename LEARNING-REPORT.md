# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-25T07:37:50Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **755**
- Outcomes: blocked: 15, cancelled: 1, done: 739
- Success rate: **98%**
- Average passes on successful tasks: **0.2**

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
| conductor | 80 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 8 | 100% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 83 | 100% |
| kapowarr | 48 | 100% |
| kind-economy | 6 | 100% |
| kind-robots | 50 | 98% |
| kindrobots-unraid | 5 | 100% |
| lora-ingestion | 1 | 100% |
| mandarin-tutor | 1 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 79 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
| scene-animator | 1 | 100% |
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
| software | 739 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 14 |
| actionable | 10 |
| transient | 10 |
| scope | 2 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 14 occurrences; look for the shared cause across its records
- failure category `actionable` — 10 occurrences; look for the shared cause across its records
- failure category `transient` — 10 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-25 `mandarin-tutor/t-001` — Keep ASR transcript and acoustic pronunciation evidence separate. Reusing the existing YIN pitch detector avoided a second speech-analysis stack. Kind Robots shared components must use container-responsive grid sizing, and Nitro $fetch calls with dynamic route strings must pin both generics.
- 2026-08-25 `cthulhuquarium/t-009` — close_task.py's --set note=... substitutes the roadmap note field rather than extending it, which silently discarded t-009's original task-spec note the same way it discarded t-033/t-034's investigative history minutes earlier (fixed by hand in kind_robots-adjacent conductor PR #2816). Caught and fixed before this close-out PR opened by re-adding the original note ahead of the DONE summary. The script itself is still unfixed -- every future close-out with `--set note=` is one keystroke away from repeating this. Worth a dedicated follow-up task (append-by-default or an explicit --append-note flag) rather than relying on every future session to catch it by hand, as this one and the #2816 session did.

- 2026-08-25 `cthulhuquarium/t-034` — Hardcoding model filenames as constants in two repos (kind_robots and conductor) with no validation against the Resource registry let an invented filename ship silently in both places and only fail at render time, months later, on an unrelated task. The fix (consume_art_queue_core.py resolving constants through the registry) deliberately warns-and-passes-through rather than hard-failing, because the registry is still incomplete (GGUF quants render fine with no Resource row) -- failing closed on an incomplete source of truth would have broken engines that demonstrably work. When migrating hardcoded config to a registry/source-of-truth lookup, ship the lenient version first and gate the strict version behind an opt-in flag until the source of truth is actually complete.

- 2026-08-25 `cthulhuquarium/t-033` — A read failure reported at the application layer (ComfyUI's hostbuf_file_reader_read failed) said almost nothing about which layer actually failed -- three diagnoses (corrupt file, shfs member disk, relayed tailnet path) were tried and disproved before the SMB client event log on the render box showed the real cause: the mount to Alexandria was dropping about once a minute. The transport-layer logs were available the whole time; reasoning forward from the application error alone cost three wrong turns. Next time a large-file read fails intermittently over a network mount, check the client-side connectivity event log before hypothesizing about the file or the storage layer underneath it.

- 2026-08-25 `lora-ingestion/t-008` — Disposable admin cleanup workflows can keep resumable review state in a dedicated localStorage-backed store while writing only canonical Resource fields through existing APIs, avoiding temporary schema or endpoint surface.
- 2026-08-24 `cthulhuquarium/t-003` — The task note assumed a starter fish bible already existed ("grow the seeded bestiary... from its starter set") but neither fish/SCHEMA.md, fish/*.yaml, nor validate_fish.py existed anywhere -- ECONOMY.md's own text had already flagged this exact gap. Cross-referencing every candidate field against the project's already-committed design docs (SYSTEMS.md's rivalry tag vocabulary, ECONOMY.md's rarity_tiers table, the Prisma schema's actual Character/ AquariumStock columns) before authoring anything resolved a real ambiguity the task note left open (tier and rarity read as two separate fields in the note, but the schema and economy docs establish they are the same axis) as a documented judgment call rather than an invented field with nowhere to land -- worth doing before writing bible content on any task whose note references a schema/starter-set that a plain repo search doesn't confirm.

- 2026-08-24 `davinci/t-021` — Chasing a prior cycle's own flagged next-lead ("concurrent tab/session interaction with the same run was not traced") rather than re-running an already-exhausted static-reading pass found a genuine correctness gap: the front end's "exactly one choice per chapter" invariant (chapterIndex derived from playedCount, only advanced on success) was never enforced server-side, so two open tabs or a client retry could double-apply LifeChoice effects. Fixing it by reusing the file's own existing idempotency idiom (resolveCompletedLifeRun's read-back-don't-recompute pattern) kept the change minimal and consistent rather than introducing a parallel guard shape. Where the sandbox couldn't execute the new live-DB regression case, saying so explicitly in the PR (rather than claiming full verification) kept the Verified section honest.

- 2026-08-24 `cthulhuquarium/t-006` — A research task benefits from live web search over training-data recall alone, even for well-established reference games: search surfaced AbyssRium's specific documented failure mode (hidden/undocumented unlock triggers requiring a wiki) and current retention-benchmark figures that made the adopt/adapt/reject list's reasoning concrete and sourced rather than generic genre-savvy assertion. Cross- referencing every finding against the project's own already-committed design docs (DESIGN-BRIEF/SYSTEMS/ECONOMY) before writing anything down kept the output as confirmation-plus-authoring-guidance for named downstream tasks rather than a survey that risked relitigating settled decisions.

- 2026-08-24 `cthulhuquarium/t-004` — "Simulate it, don't just spec it" caught a real methodology bug before it could look like a balance bug: a naive active-vs-idle coin-balance comparison showed idle beating active over two hours, which would have read as a genuine MVP-requirement violation (DESIGN-BRIEF's "idling rewarded but strictly worse than playing"). The actual cause was comparing raw liquid balance, which conflates spending (buying a fish, an investment) with losing. Switching to net worth (coins + owned-asset value) and gross income earned (cumulative production before spend) reversed the finding to a healthy 3-3.5x active/idle gap that widens over time via reinvestment compounding. Worth generalizing: any economy simulation comparing two spending strategies needs a wealth metric that survives the comparison, not a currency balance that a strategy's own spending pattern can arbitrarily deflate.

- 2026-08-24 `cthulhuquarium/t-007` — A live-DB migration doesn't have to stay unverifiable in a sandbox with no docker daemon: `apt-get install mariadb-server`, running `mariadbd` directly (no systemd) under the `mysql` user, and connecting via the local socket to create the app user took under a minute and gave a real MySQL-compatible target to run `prisma migrate deploy` against. Running it through the FULL existing migration history (62 migrations), not just the new one in isolation, is what actually proves the new migration composes cleanly with everything before it -- and `prisma migrate status` reporting zero drift afterward is stronger evidence than `prisma validate` alone, which only checks the schema file's own internal consistency. Worth adding to AGENTS.md's cross-repo/kind_robots verification section as a documented option alongside `provision_kind_robots_deps.sh`'s dummy-DATABASE_URL `prisma generate` path, since that path alone doesn't catch a migration.sql that doesn't actually match what schema.prisma implies.


---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-25T07:37:50Z_
