# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-21T23:13:46Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1105**
- Outcomes: blocked: 18, cancelled: 2, done: 1085
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
| art-archive | 32 | 100% |
| art-generator-connect | 3 | 100% |
| brainstorm | 26 | 96% |
| butterfly-gallery | 29 | 93% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 39 | 100% |
| conductor | 130 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 51 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 25 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 140 | 100% |
| kapowarr | 52 | 100% |
| kind-economy | 10 | 100% |
| kind-robots | 67 | 99% |
| kindrobots-unraid | 9 | 100% |
| lora-ingestion | 3 | 100% |
| mandarin-tutor | 14 | 93% |
| media-watchlist | 12 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 85 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| rainbow-butterflies | 21 | 100% |
| ruler-hooked | 21 | 100% |
| scene-animator | 2 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 36 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 7 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 1088 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 39 |
| transient | 17 |
| actionable | 17 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 47% success over 17 closed tasks; aim the next kaizen task here
- failure category `quality` — 39 occurrences; look for the shared cause across its records
- failure category `transient` — 17 occurrences; look for the shared cause across its records
- failure category `actionable` — 17 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-21 `storybook/t-061` — Shared slug-to-card resolution removes duplicated deep-link lookup logic while keeping gate behavior in one load-bearing helper; update literal contract guards in the same scoped refactor when they intentionally pin the old implementation shape.
- 2026-09-21 `storybook/t-060` — t-059's implementation sketch (lift board into storybookRunStore, capture it in playAgain() before leaveRun() clears the run, seed StorybookTable from it via the same per-slot deck lookups seedFromQuery() uses) held up exactly as written -- the one real design decision it left open was WHERE the capture could actually happen. playAgain() runs on the Ending screen, long after the Table (and its local board ref) has unmounted, so the board has to be recorded earlier, at the moment openStory() actually succeeds, not read fresh at playAgain() time. A future task inheriting a sketch written before the surrounding component lifecycle was traced should re-verify each named call site is still mounted/alive at the point the sketch assumes, not just implement the call graph as literally stated.
- 2026-09-21 `storybook/t-059` — When a task's own note offers a scoped, safe path (correct a misleading comment/label) alongside a larger, design-dependent path (implement real persistence behavior), an unattended scheduled session should take the scoped path rather than invent unreviewed product behavior -- storybook/t-059's note explicitly sanctioned this ("if board retention isn't meant to ship yet, correct the comment instead"), which made the call low-risk. A future cycle should treat the task's own concrete implementation sketch (lift board into storybookRunStore, seed StorybookTable from it via the same seedFromQuery() lookup pattern) as the starting point if board retention becomes something Silas actually wants shipped.
- 2026-09-21 `ruler-hooked/t-025` — art-prompts.yaml requests targeting kind_robots ship via the home relay's direct self-hosted media path (ops/home-server/SELF-HOSTED-MEDIA.md), never through a kind_robots git commit -- public/images/** is git-ignored there. A prior cycle almost wrote the renders into the local kind_robots checkout as "delivery"; verifying with a public HEAD against media.acrocatranch.com instead (matching what the doc already prescribes) is the correct and only proof of landing.
- 2026-09-21 `conductor/t-188` — t-187's missing_handoff_docs() guard only covered the connector (task-events) needs-human path; the direct close_task.py path most interactive sessions actually use was still unguarded. Extended the same check there, verifying against the committed base ref (not just the worktree) since close_task.py's scratch-index plumbing commits only roadmap.yaml -- a worktree-only check would have let an uncommitted handoff file pass while still stranding it outside the pushed close-out.
- 2026-09-21 `conductor/t-187` — A needs-human note can claim a connector-fallback handoff doc was "preserved" at a projects/<slug>/docs/*.md path without the file actually landing in the same commit/tree (ruler-hooked/t-037 rescue, 2026-09-21) -- it worked out by luck that time. Added a missing_handoff_docs() check to both validate_task_events.py (PR time) and process_task_events.py (apply time) that holds/rejects a needs-human event whose note references such a path when the file isn't actually present, instead of trusting the claim.
- 2026-09-21 `ruler-hooked/t-036` — A tooling gap that already caused a real incident (t-025 restaging 81 unrelated entries alongside 12 intended ones) is worth fixing proactively once filed as a kaizen, even when nobody has hit it a second time yet -- add scoping flags (--lane, --only, etc.) to any staging/build script whose full-sweep default can silently widen a targeted change.
- 2026-09-21 `conductor/t-181` — Merged #4931 (read-only pm2 service-migration preflight + pinned test) on first pass, but the Worker PR body used its own section names (Summary, Scope, Verification) instead of the exact AGENTS.md handoff headings (Task, What changed / what I produced, How I verified), which check_pr_handoff_template.py matches literally -- CI failed even though the content was complete and well-organized. Fixed by remapping the existing prose onto the required headings via update_pull_request rather than asking for a re-submission; the fix retriggered the same check via the workflow's `edited` trigger. Connector-only Worker sessions drafting a handoff body should copy the exact heading text from AGENTS.md's PR handoff template, not paraphrase it.
- 2026-09-21 `ruler-hooked/t-027` — Merged silasfelinus/kind_robots#2949 (catch-reveal art + image-first Fishopedia): the task's own art dependency (t-019) was still 1/15 species short (choirfish's corrected re-render pending), but 14/15 bestiary images already existed and the UI change didn't need to wait for the last one -- the broken-image-safe <img> pattern already established in ruler-hooked-cosmetics-picker.vue (hide on @error instead of a broken-image icon) made shipping against a mostly-complete asset set safe. General lesson: a task blocked on "the art isn't all done yet" is often still workable once the display layer degrades gracefully per-asset --  check whether the existing broken-image/fallback convention in the codebase covers the gap before treating partial asset completion as a hard blocker. Also worth noting: running `prettier --write` on a whole pre-existing file that predates the repo's prettier adoption reformats far more than the actual change (this repo tracks such files in a documented ratchet, `verifyPrettierRatchet.ts`) -- reverting and hand-editing to match the file's existing style kept the diff scoped to the 9 lines actually added.
- 2026-09-21 `dream-cycle/t-028` — Merged silasfelinus/conductor#4913: build_dream_records.py's queue_art() now runs every assembled art_prompt through the same conditional-instruction check build_ruler_hooked_art_queue.py already used, extracted into shared scripts/art_prompt_conditional_check.py so the regex lives in exactly one Python place instead of a third copy. A violation is recorded as an ordinary failed API-call entry rather than a bare exception, so it rides the existing partial-failure rollback path for free -- the whole bundle rolls back and stays unbuilt for the next sweep, and nothing reaches art-prompts.yaml where it would otherwise re-fail a scheduled digest run silently. General lesson: when a validation gap is found downstream (here, kind_robots' server-side 422), check whether the same build script already has a partial-failure/rollback mechanism before reaching for a bare raise -- routing the new check through the existing failure shape (a synthetic entry in the results list) is less code and gets atomic rollback for free.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-21T23:13:46Z_
