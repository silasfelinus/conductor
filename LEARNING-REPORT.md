# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-07T00:45:20Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **880**
- Outcomes: blocked: 16, cancelled: 1, done: 863
- Success rate: **98%**
- Average passes on successful tasks: **0.1**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 72 | 99% |
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
| conductor | 93 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 41 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 23 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 103 | 100% |
| kapowarr | 50 | 100% |
| kind-economy | 6 | 100% |
| kind-robots | 54 | 98% |
| kindrobots-unraid | 5 | 100% |
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
| software | 864 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 17 |
| transient | 13 |
| actionable | 12 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 17 occurrences; look for the shared cause across its records
- failure category `transient` — 13 occurrences; look for the shared cause across its records
- failure category `actionable` — 12 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-06 `interface-vision/t-104` — Slice 103 of the recurring kr-btn consistency sweep generalized the sweep's own tooling pattern instead of hand-picking a fourth single-family codemod: kr_btn_order_variant_codemod.py parses the live .kr-btn-* definitions out of tailwind.css and closes any remaining site whose class token *set* exactly matches an already-canonical shape but is written in a different word order -- a near-miss class every prior single-family codemod could only close one specific order for at a time, leaving scattered leftovers across many already-'cleared' families. Found by scanning all class="..." attributes containing 'btn' with no kr- prefix, grouping by sorted token set, and diffing against the frozenset->name map already encoded in tailwind.css's own @apply rules -- 19 occurrences surfaced across 6 different families and 12 files, none previously visible to any single-family tool. General lesson for a long-running incremental-discovery sweep: periodically re-derive the full canonical mapping and re-scan for exact-set matches across ALL prior targets at once, rather than only ever looking for the next new family -- word-order variants of already-solved shapes accumulate silently in between.
- 2026-09-06 `interface-vision/t-104` — Slice 101 of the recurring kr-btn-xs consistency sweep migrated the last 3 hand-rolled 'btn btn-xs ... rounded-xl' occurrences (brainstorm-manager.vue, taskmaster-page.vue, lora-triage.vue), then re-ran kr_btn_xs_codemod.py (no --path) against post-merge main and confirmed 0 occurrences remain across the whole repo. This is the first time this task's original btn-xs scope has run out entirely -- worth recording as a milestone rather than a routine bounded-slice cycle, and a reminder to verify a recurring sweep's backlog on the *merged* tree, not just the PR's own dry-run, since a concurrent unrelated merge could in principle reintroduce the pattern between dry-run and merge. Next session picking up this task should choose a new shared-class family to track (e.g. hand-rolled btn-sm/btn-md variants) rather than assume the umbrella is finished -- it is recurring precisely because the sweep itself never ends, only its current target family did.
- 2026-09-05 `interface-vision/t-104` — Slice 89 of the recurring kr-btn consistency sweep caught a real latent bug in the slice-88 codemod tool while running it: Python's Path.read_text()/write_text() always perform universal-newline translation, so any CRLF-terminated file the tool touched would silently collapse to LF for its entire content, not just the lines actually rewritten -- a 6-occurrence bounded slice would have become a 2566-line diff on one CRLF file. The tell was a large diff on one file next to a clean diff on another for the identical kind of change (3 class substitutions each) -- when two near-identical operations produce very different diff sizes, that asymmetry is itself worth investigating before trusting either result. Fixed by opening files directly with newline="" (disables translation on both read and write) instead of read_text()/write_text() (which gained a newline= param only in Python 3.13). General lesson for any line-oriented codemod script: verify it against a CRLF fixture if the target tree has any, since this failure mode produces no error and no warning -- only an oversized diff that is easy to miss if the tool's own dry-run output only reports occurrence counts, not diff size.
- 2026-09-05 `interface-vision/t-104` — Slice 88 of the recurring kr-btn consistency sweep was tooling-only, not another live-surface migration: hardened utils/scripts/codemods/kr_btn_xs_codemod.py with repeatable --path scoping (single .vue file or directory) and excluded components/abandonware/** from default scans, so future slices can target a coherent surface family instead of a repo-wide apply followed by a hand-revert of collateral changes. Worth recognizing when a recurring migration task's next useful slice is improving the tool itself rather than running it again -- the growing remaining-pool size (52+ occurrences across 25 families per slice 87) was the signal that scoping the codemod paid off more than one more blind repo-wide pass would have.
- 2026-09-05 `interface-vision/t-104` — Slice 83 of the recurring kr-btn consistency sweep: cross-checking the full existing .kr-btn-* size/radius grid for the bare (no color, no ghost) family before grepping found the gap directly -- .kr-btn-xs (btn btn-xs rounded-xl) was missing even though its ghost-family counterpart .kr-btn-ghost-xs already existed and the xs-size rounded-lg/rounded-2xl bare variants already existed too. Comparing across the family's established naming grid (color x size x radius) surfaces gaps faster than a fresh unconstrained grep every slice.
- 2026-09-05 `kapowarr/t-071` — library_conflicts.py's word-overlap heuristic for 'unrelated series sharing a folder' had a blind spot exactly at its most valuable case: volumes with the identical title share every word, so the check that skipped groups with any word in common skipped identical-title pairs before it skipped anything else -- and an identical-title pair sharing a folder is precisely the case where the importer cannot tell them apart and silently misattributes files. The fix asks the same match_title() function the importer itself uses, rather than inventing a second 'same series' notion in the diagnostic script. General lesson: when a diagnostic script re-implements a decision the system under test already makes elsewhere (here, 'are these two titles the same'), call the real function instead of a parallel heuristic -- a parallel heuristic can silently diverge from what actually happens at runtime, in exactly the direction that hides the worst cases.
- 2026-09-05 `dream-cycle/t-006` — kind_robots#2414's --repair-tainted path cancelled legacy PENDING ArtJobs and committed Facet.artPrompt updates before the eager queue.map(buildFacetArtPayload(...)) that can throw via assertArtPromptContract on any queued entry -- a destructive/cancelling write committed ahead of the step that can still fail, with no rollback. Pass 1's retry_context named the exact fix (build/validate jobRows before the cancellation); pass 2 fixed an adjacent real concern (deleted the unattended auto-merge repair workflow) but left the flagged file byte-identical, confirmed via git log on the changed file rather than trusting the PR description -- checking whether a retry actually touched the flagged file is what caught the drift before a third wasted pass. Pass 3 finally reordered validate-then-mutate as asked. General principle for any script that repairs/replaces existing state: build and validate the full replacement set first; only then commit any cancellation or in-place mutation of what it replaces.
- 2026-09-05 `interface-vision/t-104` — Slice 80 of the recurring kr-btn consistency sweep: the local kind_robots worktree checkout was found 8 commits behind origin/main (still at slice 71) before the candidate grep ran -- always fetch/ fast-forward the working checkout first, or a grep for the next uncovered class-set risks re-surfacing patterns already migrated by slices merged since the checkout was last synced, or missing that several prior slices already landed. Separately, a create_or_update_file API call built by hand (rather than passing already-read content through) wrote a literal placeholder string as the entire file content instead of the real payload -- caught immediately by reading the file back before opening the follow-on PR, fixed with a plain follow-up commit (no force-push). Always read back a large scripted file write before trusting it. Also: this task's TALKBACK.md had drifted four slices behind its own roadmap note (last entry was slice 69, though kind_robots slices 76-79 had already merged and the note already recorded them) -- worth a dedicated catch-up pass in a future slice.
- 2026-09-05 `storybook/t-010` — narratorStore.ts's activeDream.value?.id watch reset narratorSessionIds on Dream switch, but sendNarratorMessage() had no way to notice a switch that happened mid-await -- its addChat()/streamResponse() continuation still pushed the abandoned chat id into the new Dream's (already-reset) session list. Any store that (a) derives visible state from an array of ids scoped to some 'current context' ref, and (b) resets that array on a watch when the context changes, needs its own in-flight async writers to capture an epoch/ticket before their first await and re-check it after every await -- the same openRunRequestId shape already used in modelBuilderStore.ts. A stale retry_context is also worth checking before assuming a rejected fix was never resubmitted: git blame on the file it targets can confirm the fix already landed under a later, unlogged cycle, in which case the field should be cleared rather than left looking like an open rejection.
- 2026-09-04 `storybook/t-010` — A v-for split across several sibling lists by a computed classifier (narrative-role-assigner.vue's four casting tiers) is a real keyboard-focus hazard: an item that changes classification moves to a different <ul> entirely, which Vue cannot patch in place -- it unmounts the old node and mounts a fresh one, silently dropping focus to <body>. Any interactive element inside a re-classified v-for item needs an explicit post-nextTick refocus keyed on a stable identity (member+action), not just correctness of the classification logic itself. Worth checking other multi-tier/ multi-bucket v-for surfaces (stage role assignment, batch/queue boards) for the same pattern.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-07T00:45:20Z_
