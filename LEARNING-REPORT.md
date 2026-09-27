# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-27T17:57:57Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **1173**
- Outcomes: blocked: 19, cancelled: 2, done: 1152
- Success rate: **98%**
- Average passes on successful tasks: **0.3**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 73 | 99% |
| alexa-integration | 6 | 100% |
| animation-manager | 20 | 95% |
| animation-studio | 2 | 50% |
| appmaker | 11 | 100% |
| approval-portal | 2 | 0% |
| art-archive | 34 | 100% |
| art-generator-connect | 3 | 100% |
| brainstorm | 26 | 96% |
| butterfly-gallery | 32 | 94% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 46 | 100% |
| conductor | 138 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 51 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 30 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 22 | 95% |
| interface-vision | 140 | 100% |
| kapowarr | 52 | 100% |
| kind-economy | 11 | 100% |
| kind-robots | 73 | 99% |
| kindrobots-unraid | 9 | 100% |
| lora-ingestion | 11 | 100% |
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
| ruler-hooked | 28 | 100% |
| scene-animator | 2 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 44 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 7 | 100% |
| tzaddik-gallery | 6 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 1156 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 46 |
| transient | 18 |
| actionable | 17 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 47% success over 17 closed tasks; aim the next kaizen task here
- failure category `quality` — 46 occurrences; look for the shared cause across its records
- failure category `transient` — 18 occurrences; look for the shared cause across its records
- failure category `actionable` — 17 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-27 `coloring-book/t-057` — The task's own predicted grep counts (1/25/21) matched the raw 'no text' substring hit count exactly, but 3 of those hits (2 in hollywood-recast, 1 in kind-robots) were inside historical NOT-ACCEPTED/recovery notes quoting the old wording in past tense, not live prompt.text fields -- rewriting them would have misrepresented what was actually tried and served no purpose since notes are never resubmitted as prompts. Checking each occurrence's YAML context (notes: list vs. prompt.text) before editing caught this; a blind find-and-replace across the matched line numbers would not have. Also surfaced a broader family of 'text'-adjacent clauses ("no readable text", "no logo or text", etc.) explicitly left out of scope since the task's own count only covered the literal two-word phrase -- filed as t-061 rather than scope-creeping into the same diff.
- 2026-09-27 `coloring-book/t-054` — A frozen fixture pinned to a live production file path is only as stable as that path's own guarantee of immutability -- color-art-jobs.yaml's production scripts move a superseded render to a rejected/ or revisions/ subdirectory rather than deleting it, so the original archived bytes usually still exist in the repo even after the canonical path is overwritten by a real accepted illustration. Finding and swapping in that archived original (same character, same historical measurements) fixes drift with zero loss of test coverage, instead of hunting for an unrelated known-bad substitute or dropping coverage entirely. Caught a SECOND live occurrence of the identical class (hwr-021) mid-fix, flagged by an independent concurrent session's roadmap note on the same task -- worth re-reading a task's own note for fresh evidence appended after a claim, not just what it said at claim time, since two unrelated production cycles hit the same drift class the same day.
- 2026-09-27 `coloring-book/t-052` — The whole-file-rewrite cost t-049 deliberately deferred (write_yaml(QUEUE_FILE, queue) dumping the entire ~3,000-line/~130KB in-memory tree on every single-entry mutation) narrows cleanly by mirroring a pattern the same file already had precedent for: replace_ledger_pair_value already text-splices one field of one ledger entry in place rather than rewriting the ledger. Generalizing that to a whole entry one nesting level deeper (books -> entries) needed only locating each level's block boundaries by its own list-item marker (0-indent '- order:' for books, 2-indent '  - ' for entries) and re-serializing just the touched entry with a fixed re-indent, rather than any structural rewrite of the read/load path. Verified beyond the unit-test round trip by running the new write function against a real scratch copy of the actual ~130KB production queue file and diffing every other book/entry and all top-level scalar keys before/after -- a synthetic fixture alone would not have caught an edge case specific to the real file's shape (e.g. a book or entry ordering quirk), and none existed here (108-entries, 3-books, all entry blocks IDed correctly).
- 2026-09-27 `conductor/t-198` — A test that calls a production CLI's main() end-to-end without mocking its network-dependent branch is only as isolated as the branch's own gating condition happens to be closed in the current process -- test_annotate_daily_dream_art_queue.py's isolation flake existed because _live_job_fetcher()'s bare `import consume_art_requests` failed silently (ImportError -> None) unless some *other* test file had already put scripts/ on sys.path, an accidental protection that full-suite collection order defeats deterministically while single-file runs never exercise. When a CLI-level test's correctness implicitly depends on an ambient secret/import/environment condition rather than an explicit mock, make that condition explicit (monkeypatch.delenv, an injected fetch_job, etc.) rather than fixing the accident that happened to mask it -- the accident (sys.path scope) is not the actual isolation boundary the test needs.
- 2026-09-27 `coloring-book/t-048` — art_quality.py's NOISE_MIN_HF_RATIO (0.55) false-positived on legitimate busy/detail-dense line art (kind-robots/kr-001's dense repeated-icon composition) because the task note's own diagnosis was already precise. Rather than take the note's offered book-specific-threshold shortcut, pulled every hf_ratio ever recorded in color-art-jobs.yaml across all three books and found a clean, wide, unused gap between real noise (0.857-0.876) and every legitimate render including the false positive (<=0.5953) -- letting a single global recalibration (0.72) fix it safely for every book, with regression fixtures pinning both groups so a future change that would flip either shows up as a named test failure. When a false-positive/true-positive pair both have recorded historical measurements, check the full distribution before reaching for a per-case carve-out or a new heuristic -- the simpler global fix is often already safe and just needs the data to prove it. (A concurrent t-022 cycle 80 session independently hit and diagnosed the same bug via a different route -- monster-recast mr-010, hf_ratio 0.5732, a completely different composition style -- landed as a real rotation collision on scripts/art_quality.py; reconciled at merge by keeping this fix as canonical and folding the second data point in as supplementary regression tests rather than a duplicate threshold change.)
- 2026-09-27 `coloring-book/t-049` — A kaizen task that names the exact race (two manage_coloring_book_production.py invocations racing on different proposal ids in the same shared color-art-jobs.yaml) and the smallest of three explicit fix options (a lockfile held for the whole live run, vs. narrowing the write path, vs. a docstring warning) is landable in one pass: an exclusive non-blocking flock on a sibling .lock file, held from load through every write, makes a racing second invocation fail fast with a clear error instead of silently reverting the first's already-persisted state. Verified with a real cross-process test (not just an in-process mock) since flock semantics depend on separate open-file-descriptions, which a same-process double-open can get subtly wrong. Filed t-052 to narrow the write path itself (read-modify-write only the touched entry) as a follow-on if whole-file rewrites become a real cost -- deliberately deferred rather than bundled, per the original note's own preference for the smallest safe fix.
- 2026-09-27 `tzaddik-gallery/t-022` — A kaizen task naming an exact file, function, and the mechanical reason ESLint double-flagged it (disable comment landing above a multi-line type instead of the line the `any` actually appears on) is landable in one pass with zero ambiguity: narrowing the map's `findUnique` argument type to the shape every call site actually passes removed the `any` outright, so no disable comment was needed at all. Confirmed via eslint (clean), vue-tsc --noEmit (clean), and test:lint-ratchet (-3 problems vs. baseline).
- 2026-09-27 `coloring-book/t-022` — A script that loads a shared YAML file once per process and writes the whole in-memory snapshot back at several points during its run is unsafe to invoke concurrently, even across entries the two invocations don't logically share -- the slower process's later write is based on a pre-change snapshot and silently reverts the faster process's already-persisted progress with no error. Reproduced live running manage_coloring_book_production.py's generate-bw for two different book/proposal ids at once: the first to finish had its bw_status: done reverted back to running by the second process's later write. Recovered safely only because the render and server-side ArtImage survived independently of the YAML bookkeeping and the enqueue step was idempotent against an existing job id -- a less careful recovery could have double-submitted a render job. Filed coloring-book/t-049 to fix the script; the immediate mitigation is to never run two invocations against the same shared state file in parallel, regardless of how independent their target keys look.
- 2026-09-27 `coloring-book/t-039` — When a fix's own task has already been closed prematurely twice on indirect evidence (a merged PR, a plausible diagnosis), closing it a third time needs a direct check of the actual deployed artifact, not the passage of time since merge: inspect the specific field the bug lived in (here, GET /api/art/queue/:id's stored workflow graph's UNETLoader checkpoint name) before spending a render cycle assuming a Force Update happened. Then verify the render's actual pixels, not just its mechanical pass/fail, before trusting the fix -- a mechanical rejection on a DIFFERENT input during the same verification pass (kind-robots kr-001) turned out to be an unrelated false positive in the quality gate itself, not evidence the fix was incomplete; reading the rejected file directly (not just its stats) was what told the two apart.
- 2026-09-27 `dream-cycle/t-006` — A workflow-step rename (changing a GitHub Actions step name, an ::warning:: message, or an error string a contract test greps for verbatim) is a repo-wide rename, not a local edit -- grep the whole tests/ tree for the exact old string before renaming, not just the test file you already know references it. Caught here as a Reviewer catch (not a Worker rejection) on silasfelinus/conductor#5264, which renamed several daily-digest.yml step names for the one-day render-runway fix but left 4 pre-existing tests hardcoding the old names, failing both the Python test suite and the dream-cycle contract CI job.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-27T17:57:57Z_
