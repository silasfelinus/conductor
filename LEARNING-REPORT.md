# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-25T09:27:35Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **757**
- Outcomes: blocked: 15, cancelled: 1, done: 741
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
| mandarin-tutor | 3 | 100% |
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
| software | 741 | 99% |

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

- 2026-08-25 `mandarin-tutor/t-010` — A task's first implementation slice can merge (kind_robots PR) cleanly at status:review with no reconciliation checkpoint following. Reviewer sweeps should run check_pr_merged_drift.py every session, not only when a task looks stuck -- this one merged and sat 10+ minutes before the drift script caught it.
- 2026-08-25 `mandarin-tutor/t-005` — Keep target-blind speech recognition separate from reference-aware pronunciation feedback, and keep generated lexical facts visibly distinct from pinned dictionary/source data. Durable media identity belongs server-side so requested cards survive reloads and future native clients.
- 2026-08-25 `mandarin-tutor/t-001` — Keep ASR transcript and acoustic pronunciation evidence separate. Reusing the existing YIN pitch detector avoided a second speech-analysis stack. Kind Robots shared components must use container-responsive grid sizing, and Nitro $fetch calls with dynamic route strings must pin both generics.
- 2026-08-25 `cthulhuquarium/t-009` — close_task.py's --set note=... substitutes the roadmap note field rather than extending it, which silently discarded t-009's original task-spec note the same way it discarded t-033/t-034's investigative history minutes earlier (fixed by hand in kind_robots-adjacent conductor PR #2816). Caught and fixed before this close-out PR opened by re-adding the original note ahead of the DONE summary. The script itself is still unfixed -- every future close-out with `--set note=` is one keystroke away from repeating this. Worth a dedicated follow-up task (append-by-default or an explicit --append-note flag) rather than relying on every future session to catch it by hand, as this one and the #2816 session did.

- 2026-08-25 `cthulhuquarium/t-034` — Hardcoding model filenames as constants in two repos (kind_robots and conductor) with no validation against the Resource registry let an invented filename ship silently in both places and only fail at render time, months later, on an unrelated task. The fix (consume_art_queue_core.py resolving constants through the registry) deliberately warns-and-passes-through rather than hard-failing, because the registry is still incomplete (GGUF quants render fine with no Resource row) -- failing closed on an incomplete source of truth would have broken engines that demonstrably work. When migrating hardcoded config to a registry/source-of-truth lookup, ship the lenient version first and gate the strict version behind an opt-in flag until the source of truth is actually complete.

- 2026-08-25 `cthulhuquarium/t-033` — A read failure reported at the application layer (ComfyUI's hostbuf_file_reader_read failed) said almost nothing about which layer actually failed -- three diagnoses (corrupt file, shfs member disk, relayed tailnet path) were tried and disproved before the SMB client event log on the render box showed the real cause: the mount to Alexandria was dropping about once a minute. The transport-layer logs were available the whole time; reasoning forward from the application error alone cost three wrong turns. Next time a large-file read fails intermittently over a network mount, check the client-side connectivity event log before hypothesizing about the file or the storage layer underneath it.

- 2026-08-25 `lora-ingestion/t-008` — Disposable admin cleanup workflows can keep resumable review state in a dedicated localStorage-backed store while writing only canonical Resource fields through existing APIs, avoiding temporary schema or endpoint surface.
- 2026-08-24 `cthulhuquarium/t-003` — The task note assumed a starter fish bible already existed ("grow the seeded bestiary... from its starter set") but neither fish/SCHEMA.md, fish/*.yaml, nor validate_fish.py existed anywhere -- ECONOMY.md's own text had already flagged this exact gap. Cross-referencing every candidate field against the project's already-committed design docs (SYSTEMS.md's rivalry tag vocabulary, ECONOMY.md's rarity_tiers table, the Prisma schema's actual Character/ AquariumStock columns) before authoring anything resolved a real ambiguity the task note left open (tier and rarity read as two separate fields in the note, but the schema and economy docs establish they are the same axis) as a documented judgment call rather than an invented field with nowhere to land -- worth doing before writing bible content on any task whose note references a schema/starter-set that a plain repo search doesn't confirm.

- 2026-08-24 `davinci/t-021` — Chasing a prior cycle's own flagged next-lead ("concurrent tab/session interaction with the same run was not traced") rather than re-running an already-exhausted static-reading pass found a genuine correctness gap: the front end's "exactly one choice per chapter" invariant (chapterIndex derived from playedCount, only advanced on success) was never enforced server-side, so two open tabs or a client retry could double-apply LifeChoice effects. Fixing it by reusing the file's own existing idempotency idiom (resolveCompletedLifeRun's read-back-don't-recompute pattern) kept the change minimal and consistent rather than introducing a parallel guard shape. Where the sandbox couldn't execute the new live-DB regression case, saying so explicitly in the PR (rather than claiming full verification) kept the Verified section honest.

- 2026-08-24 `cthulhuquarium/t-006` — A research task benefits from live web search over training-data recall alone, even for well-established reference games: search surfaced AbyssRium's specific documented failure mode (hidden/undocumented unlock triggers requiring a wiki) and current retention-benchmark figures that made the adopt/adapt/reject list's reasoning concrete and sourced rather than generic genre-savvy assertion. Cross- referencing every finding against the project's own already-committed design docs (DESIGN-BRIEF/SYSTEMS/ECONOMY) before writing anything down kept the output as confirmation-plus-authoring-guidance for named downstream tasks rather than a survey that risked relitigating settled decisions.


---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-25T09:27:35Z_
