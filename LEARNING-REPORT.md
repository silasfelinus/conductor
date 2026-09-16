# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-09-16T03:37:28Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **982**
- Outcomes: blocked: 16, cancelled: 1, done: 965
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
| coloring-book | 37 | 100% |
| conductor | 114 | 100% |
| conductor-app | 4 | 100% |
| cthulhuquarium | 51 | 98% |
| davinci | 8 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 23 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 135 | 100% |
| kapowarr | 52 | 100% |
| kind-economy | 10 | 100% |
| kind-robots | 60 | 98% |
| kindrobots-unraid | 9 | 100% |
| lora-ingestion | 1 | 100% |
| mandarin-tutor | 11 | 100% |
| media-watchlist | 12 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 84 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| rainbow-butterflies | 21 | 100% |
| ruler-hooked | 11 | 100% |
| scene-animator | 2 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 24 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 7 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 17 | 47% |
| software | 965 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 27 |
| transient | 15 |
| actionable | 15 |
| scope | 3 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 47% success over 17 closed tasks; aim the next kaizen task here
- failure category `quality` — 27 occurrences; look for the shared cause across its records
- failure category `transient` — 15 occurrences; look for the shared cause across its records
- failure category `actionable` — 15 occurrences; look for the shared cause across its records
- failure category `scope` — 3 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-09-16 `rainbow-butterflies/t-053` — A "document this orphaned API surface" task can surface a real design question (AgentProfile-bound credentials have no UI in kind_robots) without it being safe to file as a fix task, when the other half of the flow lives in a repo outside the session's access scope (rainbowbutterflies) -- flag the open question in the note for a session that can see both sides instead of guessing at scope.
- 2026-09-16 `conductor/t-132` — Cross-workflow stalls at unrelated steps, despite an existing job timeout, are runner/platform evidence; do not optimize the most frequently observed command unless the failure reproduces specifically there.
- 2026-09-16 `conductor/t-160` — Worker's PR handoff template omitted Stakes/Flags-for-Reviewer/Kaizen-suggestion even on a small doc-only PR; enforce full template discipline regardless of diff size so a real kaizen suggestion or flag isn't silently dropped.
- 2026-09-15 `storybook/t-050` — Clean first-pass mechanical kaizen: mirrored t-048's isMediaOriginReachable() guard
exactly onto verifyAcademyExamplesManifest.ts, the one sibling script t-048's own PR
(#2767) didn't cover despite sharing the identical unguarded-live-fetch shape.
Verified both paths concretely rather than trusting the diff: ran the check normally
(reachable) and again with MEDIA_ORIGIN pointed at a nonexistent host (simulated
unreachable), confirming exit 0 + warning on the latter instead of a hard failure.
kind_robots PR #2772's Contract verifiers check -- the one conductor/t-132 tracks as
occasionally hanging for 15-40+ minutes with zero step progress -- completed normally
this run, one more data point for that task's "monitor, don't force a repo-side fix"
conclusion. Lesson: when a kaizen task says "mirror X's diff exactly," find the
original commit first (git log/show) rather than reconstructing the pattern from
the task note's prose -- guarantees the two implementations stay byte-identical in
shape.
- 2026-09-15 `conductor/t-169` — Audited the 5 tasks whose notes were flagged >- (the historical
append_note_text() folding bug's signature label) for actual content loss, not just
length. Method: locate every entry-boundary marker (PROGRESS (, RECONCILED (, Cycle (,
DONE 202, CORRECTION (, etc.) in the parsed note string and inspect text immediately
before/after each for truncation or garbling. Finding: zero data loss across all 5 --
every original single-newline break between adjacent entries became one space on
folding, which loses paragraph/readability structure but never words or entries. The
earlier concern (this same task's own history) that folding caused a CI-hang was
already disproven by pulling the actual job logs (GitHub Actions status-reporting
flakiness, unrelated to note content). Lesson for a future note-format audit: a
`>-`/`|-` label mismatch alone is not evidence of damage -- verify by sampling actual
entry boundaries for coherence before assuming restoration work is needed.
- 2026-09-15 `conductor/t-170` — Clean first-pass fix (attempt-cap + quarantine for process_coloring_art_events.py), but
the new tests initially relied on this sandbox's ambient KR_API_TOKEN (a container-level
env var, not something kr_token_set.sh sets) instead of pinning it explicitly, so they
passed locally and failed on the GitHub Actions "Python test suite" job, which doesn't
inject that secret outside process-color-art-events.yml's own step. Caught by reading the
actual failing job log rather than assuming a plausible diff was CI-safe; fixed by
wrapping the three affected tests in patch.dict(os.environ, {"KR_API_TOKEN": ...}) and
re-verifying locally with `env -u KR_API_TOKEN pytest tests/ -q` before pushing again.
Lesson for future tests exercising code with credential-gated branches: never assume a
sandbox's ambient environment matches CI's; pin every env var the code under test
branches on, explicitly, in the test itself.
- 2026-09-15 `conductor/t-169` — append_note_text() forced every note to a folded `note: >-` block regardless of prior
style; on a note already stored as literal `note: |-` with substantial multi-line history,
a real YAML parser folds adjacent physical lines together on the next parse, silently
merging content. Hit for real on model-builder/t-029 (126KB note, 67+ cycles): the forced
`>-` rewrite collapsed it to a handful of enormous lines, which pathologically slowed the
"Python test suite" CI job (40+ min twice, vs. ~2 min normal) before the fix. Fixed by
preserving an existing `|-` style instead of always forcing `>-`; caught only by comparing
CI timing against recent successful runs and cancel/rerunning to confirm reproducibility
rather than trusting a plausible-looking diff. Filed conductor/t-169 to audit 5 other tasks
already showing the `>-`-plus-giant-line signature for the same latent risk.
- 2026-09-15 `storybook/t-048` — verifyAcademyStarterManifest.ts/verifyPopulationDraftQuality.ts fetched live data with no reachability guard, so a home-machine (Alexandria) reboot failed CI on main itself; fixed with a short-timeout probe that skips with a warning (exit 0) on a network-level failure only, verified by actually simulating an unreachable host rather than trusting the diff by inspection.
- 2026-09-15 `conductor/t-168` — scripts/kr_token_set.sh's exit killed the calling shell when sourced -- the documented safe usage -- silently dropping any chained command; fixed with sourced-vs-executed runtime detection and pinned with a subprocess-driven regression test since none existed.
- 2026-09-15 `storybook/t-027` — A recurring "check the real state and record it" audit task can surface a result the task's own follow-on wasn't designed for: t-028 assumed t-027 would find some endings missing art among an otherwise-seeded 1,024-row catalog, but the actual coverage call came back 0/1024 seeded -- zero rows exist at all, not partial art coverage. Letting the dependency resolver mechanically flip t-028 to `ready` on t-027's `done` would have handed a future worker a task it structurally could not start (nothing to attach art to). General lesson: when an audit's real result falls outside the shape its downstream task assumed, redirect the downstream task in the same close-out instead of letting an automatic status transition carry a stale scope forward -- the dependency graph tracks task completion, not whether the completed task's findings still match what its dependent expects.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-09-16T03:37:28Z_
