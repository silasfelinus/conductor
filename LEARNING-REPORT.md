# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-07-21T21:43:34Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **329**
- Outcomes: blocked: 12, done: 317
- Success rate: **96%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 35 | 100% |
| alexa-integration | 2 | 100% |
| animation-manager | 8 | 100% |
| animation-studio | 1 | 100% |
| appmaker | 5 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| challenge-center | 16 | 100% |
| coat-dance | 8 | 0% |
| coloring-book | 13 | 100% |
| conductor | 46 | 100% |
| conductor-app | 2 | 100% |
| davinci | 1 | 100% |
| digital-storefront | 12 | 100% |
| dream-cycle | 14 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 1 | 100% |
| kind-robots | 30 | 97% |
| kindrobots-unraid | 4 | 100% |
| media-watchlist | 4 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 29 | 100% |
| mural-design | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
| serendipity | 3 | 100% |
| sketchy | 2 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 11 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 15 | 40% |
| software | 314 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 6 |
| actionable | 6 |
| transient | 5 |

## Kaizen targets

- project `coat-dance` — 0% success over 8 closed tasks; aim the next kaizen task here
- kind `content` — 40% success over 15 closed tasks; aim the next kaizen task here
- failure category `quality` — 6 occurrences; look for the shared cause across its records
- failure category `actionable` — 6 occurrences; look for the shared cause across its records
- failure category `transient` — 5 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-07-21 `conductor/t-077` — This session's designated git-push transport (http://127.0.0.1:41729 relay) 413'd on every plain `git push` to its own session branch -- even a brand-new throwaway branch with a 1-byte diff and a ~59KB pack -- while pushing directly to `main` via claim_task.py's git-plumbing helper worked fine. This doesn't match either of CLAUDE.md's two documented HTTP-413 causes (new-ref full-pack, post-rebase force-push). Workaround that eventually worked: retry the SAME single-file git-plumbing commit approach (scratch index + commit-tree + `git push <sha>:<ref>`) against the session branch itself, not just main -- it succeeded where a bulkier `git push -u origin <branch>` failed, before falling back to the heavier push_files MCP tool. Separately: when relaying a large file's full content through push_files (no diff/patch mode exists), ALWAYS diff the pushed remote content byte-for-byte against the local working tree immediately after (e.g. `git show origin/<branch>:<path> | diff - <local-path>`) before trusting it -- a transcription slip during one such relay silently dropped a clause from one note field, and a later slip (pasting an incomplete draft) briefly truncated the entire 2198-line roadmap.yaml to just its 22-line header, discovered only because this verification step is now habitual. Both were caught and fixed before the PR was even opened, with zero cost to Silas -- but only because verification happened immediately, not after moving on.
- 2026-07-21 `sketchy/t-008` — A project's milestones can show every spec task as done while nothing has actually been built against those specs -- check milestone status against real code state (does the app scaffold still show generated boilerplate?), not just task-list completion, before assuming a project has no available work. Also: app-ci.yml tests every app in apps/ within one shared job whenever its changed-app diff detection doesn't isolate to a single app, so an unrelated app's flaky/hung test can make an otherwise-clean PR's CI look broken -- read the full job log for which app actually failed before assuming your own diff caused it; a test that passes cleanly in the first few seconds of a job that then hangs for 10 more minutes on a different app's test file is not your regression.
- 2026-07-21 `davinci/t-014` — set_task_field.py edits whatever is on the caller's local working tree, unlike claim_task.py which fetches origin/main fresh and pushes via git plumbing -- calling set_task_field.py right after claim_task.py in the same session without an intervening fetch+ff-only can silently reapply a stale claimed_by/claimed_at (or any other field) on top of the real claim. Always fetch and fast-forward the local branch before any set_task_field.py call that follows a claim_task.py call. Separately: hand-appending a new paragraph to a folded (>) YAML note: field needs a blank line between paragraphs, not just a newline -- YAML's folded-scalar rule collapses adjacent non-blank lines into one line with a space, so a missing blank line silently merges the new paragraph into the previous one on next parse. Verify by re-parsing the note and diffing paragraph-boundary bytes, not by eyeballing the raw text diff.
- 2026-07-21 `ai-art-academy/t-036` — A recurring rotation task (t-010) can strand a green, unmerged kind_robots PR at session end if the completion checklist only names the terminal-state requirement generically instead of listing 'poll CI and merge (or explicitly park) before the cycle ends' as its own explicit bullet -- this had already happened twice (PR #942, PR #814) under slightly different framings before it was made an explicit, lane-agnostic checklist item. When a recurring task's own history shows the same failure shape twice, generalize the fix beyond the specific lane/step where it was first noticed, since the underlying gap (an implicit 'PR opened' being mistaken for 'cycle done') can recur on any lane that opens a PR.
- 2026-07-21 `conductor-app/t-012` — Before assuming a feature needs new backend endpoints, check what the existing API already returns/accepts -- GET /api/dreams/:id already embedded up to 12 linked ArtCollections with up to 12 ArtImages each, and POST /api/conductor/art-request already existed pre-built and admin-gated, so the whole task (ArtCollection browsing + admin art-request form) was pure Flutter client work with zero kind_robots changes needed. Also: a sandboxed toolchain pinned to a fixed version can silently drift stale against CI's unpinned 'stable' channel and produce false-positive analyze errors (including on files never touched this cycle) -- when a fresh error appears on pre-existing code, suspect the toolchain version before the diff, and verify against the actual current stable before trusting the result.
- 2026-07-21 `conductor/t-075` — A reused coarse hour/rotation-label session id never breaks claim_task.py's correctness (it keys on project/task), but it does corrupt the audit trail when two concurrent sessions pick the same label within the same hour, making one session's TALKBACK/claimed_by history look like it belongs to another. Prefer a full ISO timestamp with seconds plus a task-specific suffix, or a random token, over a coarse label string.
- 2026-07-21 `kind-robots/t-042` — A new static-source contract test is only trustworthy once it's been proven to actually catch the pattern it claims to guard against -- write a synthetic violating sample first (cover edge cases like nested generics that could produce false negatives in a bracket-depth parser), confirm it fails as expected, then remove the sample and confirm the real codebase passes clean. Testing only the 'passes on real code' direction would have missed a parser bug that let violations through silently.
- 2026-07-21 `appmaker/t-009` — A cryptic CI type error in a file the task never touched is not automatically 'pre-existing and unrelated' -- it can be a genuine, if indirect, regression the diff triggered (here: 2 new server/api/** route files grew the typed $fetch route-key union just enough to push vue-tsc's TS2589 recursion limit on unrelated call sites). A same-tree local repro without the diff isn't conclusive either, since sandbox vs real CI can diverge -- cross-check against the base commit's actual CI history before concluding a failure is pre-existing. Root-causing (pinning $fetch's R generic, 12 files) was cheap once understood and is a durable fix, versus a band-aid on the one file CI happened to name first.
- 2026-07-21 `ruler-hooked/t-007` — A task can outlive its own blocker without anyone noticing: t-007's completion condition (PR #328 merged AND t-012 landing the playable screen meeting all four DESIGN-BRIEF m2 exit criteria) had been fully satisfied since t-012 merged earlier the same day, but t-007 itself still sat at status: ready/claimed pending someone to actually check and flip it. When a task's note already states an explicit, checkable completion condition, re-verify it directly (fresh checkout, self-tests, full typecheck) before assuming more code work is needed -- sometimes the task is closing bookkeeping, not new implementation.
- 2026-07-21 `ruler-hooked/t-012` — A task's retry_context can go stale when a human merges the referenced PR directly, bypassing the normal reject->retry->re-review loop (t-012's retry_context described a pass-1 rejection of kind_robots PR #329 written at 21:55Z on 2026-07-16, but Silas merged that same PR 9 minutes later at 22:04:56Z). Before acting on any retry_context for a cross-repo task, check whether the referenced PR already merged and re-verify against current target-repo main first -- don't assume a recorded rejection is still live. See conductor/t-074 (kaizen task filed this cycle) for the AGENTS.md doc fix.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-07-21T21:43:34Z_
