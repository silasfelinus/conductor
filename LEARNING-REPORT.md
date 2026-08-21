# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-21T16:34:35Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **719**
- Outcomes: blocked: 15, cancelled: 1, done: 703
- Success rate: **98%**
- Average passes on successful tasks: **0.0**

## By project

| Project | Closed | Success rate |
|---|---|---|
| ai-art-academy | 64 | 98% |
| alexa-integration | 6 | 100% |
| animation-manager | 13 | 100% |
| animation-studio | 2 | 50% |
| appmaker | 8 | 100% |
| approval-portal | 2 | 0% |
| art-generator-connect | 3 | 100% |
| brainstorm | 21 | 95% |
| challenge-center | 16 | 100% |
| coat-dance | 9 | 11% |
| coloring-book | 25 | 100% |
| conductor | 78 | 100% |
| conductor-app | 4 | 100% |
| davinci | 6 | 100% |
| digital-storefront | 29 | 100% |
| dream-cycle | 19 | 100% |
| ecosystem-map | 5 | 100% |
| global-ui | 13 | 100% |
| humboldt-impropriety-calendar | 1 | 0% |
| humboldt-scoop | 1 | 100% |
| humboldt-scoop-cms | 21 | 95% |
| interface-vision | 83 | 100% |
| kapowarr | 47 | 100% |
| kind-economy | 6 | 100% |
| kind-robots | 50 | 98% |
| kindrobots-unraid | 5 | 100% |
| media-watchlist | 10 | 100% |
| mermaids-of-venice | 3 | 100% |
| model-builder | 72 | 100% |
| mona-salai | 1 | 100% |
| mural-design | 1 | 100% |
| music-mentor | 1 | 100% |
| newsfeed | 20 | 100% |
| packmaker | 10 | 100% |
| ruler-hooked | 4 | 100% |
| serendipity | 3 | 100% |
| sketchy | 3 | 100% |
| storybook | 14 | 100% |
| storymaker | 1 | 100% |
| superkate-hairstyle-ai | 18 | 100% |
| superkate-services-calculator | 12 | 100% |
| taskmaster | 3 | 100% |
| text-generation | 6 | 100% |

## By kind

| Kind | Closed | Success rate |
|---|---|---|
| content | 16 | 44% |
| software | 703 | 99% |

## Failure categories

| Category | Count |
|---|---|
| quality | 14 |
| actionable | 10 |
| transient | 9 |
| scope | 2 |

## Kaizen targets

- project `coat-dance` — 11% success over 9 closed tasks; aim the next kaizen task here
- kind `content` — 44% success over 16 closed tasks; aim the next kaizen task here
- failure category `quality` — 14 occurrences; look for the shared cause across its records
- failure category `actionable` — 10 occurrences; look for the shared cause across its records
- failure category `transient` — 9 occurrences; look for the shared cause across its records

## Recent lessons

- 2026-08-21 `brainstorm/t-027` — Scoping a broad "evaluate N surfaces" task by shipping the cheapest one first and filing the rest as named follow-ups (t-028 for Reward) kept the diff small (3 files) and avoided forcing a button onto Prompt, which has no standalone detail view yet. A surface with an existing adapter but no UI entry point (Scenario, from t-014) is the cheapest next slice on this kind of task -- check BRAINSTORM_SOURCE_ADAPTERS for already-wired-but-untriggered adapters before starting from scratch on any surface.

- 2026-08-21 `brainstorm/t-019` — Claimed and dispatched implementation for a task whose deliverable turned out to already exist, shipped by two earlier tasks (t-013, t-014) days prior. No harm done since the dispatched agent verified against actual shipped code before writing anything and correctly declined to manufacture a diff -- but the roadmap task itself should have been closed or re-scoped at the moment t-013/t-014 shipped equivalent coverage, not left `ready` to be rediscovered and re-investigated by a later cycle. When a task ships coverage that satisfies a different, still-open task's stated scope, check for and update that task in the same close-out cycle.

- 2026-08-21 `brainstorm/t-017` — Found the established precedent (modelBuilderStore.ts's pollAsyncArtJob -> finalizeQueuedArtImage split) before designing a bespoke "verify the delivered image" path for Brainstorm's own enqueue/poll loop -- reusing it caught more than a hand-rolled check would have (finalizeQueuedArtImage re-fetches the ArtImage row itself, not just trusting the job's artImageId field, and routes through the same collection-attachment semantics every other art surface uses). Also worth noting: a "failed" outcome had literally zero persisted signal before this task -- only a transient, session-local busy flag distinguished "generating" from "never tried" or "gave up," so any per-candidate/per-item async operation with a client-visible outcome should be checked for this same gap (state that only lives in memory during the operation, with nothing surviving a reload once it ends) before assuming existing coverage is complete.

- 2026-08-21 `brainstorm/t-016` — Clean first-pass success on a real feature build (not a bugfix cycle): grepping for existing-but-unused scaffolding (BrainstormCandidate.meta.art) before implementing prevented inventing a parallel tracking mechanism, and it also surfaced a genuine latent bug (client localStorage round-trip silently dropping a JSON meta field the server path already preserved generically) that a narrower "just wire the button" implementation would have missed entirely. Worth generalizing: when a Prisma model's `meta`/JSON column is preserved generically server-side but the client has a hand-written normalizer that only lifts out known sub-fields, any new sub-field added to that type needs an explicit normalizer update or it silently vanishes on the client-only persistence path (localStorage/autosave) even though the server path never had the bug.

- 2026-08-21 `model-builder/t-029` — Cycle 30 of a long-running recurring bug-hunt task: a transient, client-local 'in-progress' marker written directly onto item.stages before an async call (commitItem's COMMIT marker, generateItemAsset's GENERATE_ASSETS marker) has no store-level enforcement stopping an unrelated stageStatuses-diffing write from reading and re-persisting it as real. Three of four batch functions lacked the isItemManualActionInFlight guard their sibling autoBuildItem already had -- the fourth instance of this exact shape across cycles 25, 28, and 29 (see cycle 20's and cycle 25's own entries in this file). Patching one more call site per cycle works but never closes the class; the durable fix is moving the in-flight flag into a separate ephemeral field never serialized into a stageStatuses payload, the same way artJobId/queueState already are kept out of item.stages.

- 2026-08-20 `kapowarr/t-062` — A prior evaluation doc that names exact measured traps (response shapes, pagination ceilings, a 404-not-JSON edge case) turns an "implement a REST client" task into something closer to transcription than design -- the risk shifts from "did I miss a trap" to "did I quietly widen scope while transcribing it." Re-reading the evaluation doc's own recommendation section against the actual diff before opening the PR (does every field mapping trace to a table row, is every new file/setting/test named in the doc's follow-on task description) is what kept this PR three files instead of six -- the doc's own field tables for `Series`/`overview` rows against `VolumeMetadata`/ `IssueMetadata` could be pasted almost directly into code comments, and the two schema-shape questions the doc explicitly left unmeasured (a `title` field on overview rows, `longest_story.synopsis`) were exactly the two places worth flagging as judgment calls in the PR body rather than silently guessing. Second: an existing sibling provider is not automatically a safe copy source. Reading `metron.py` for the pattern surfaced a real latent bug in it (`test_key()` imports `run` from `backend.base.helpers`, which re-exports `subprocess.run`, not an async runner -- calling `subprocess.run(<coroutine>)` raises, it doesn't return `False`; the sibling `comicvine.py` gets this right via `from asyncio import gather, run, sleep`). Never had a test covering `test_key()`'s actual return value, so it shipped unnoticed. Filed as kapowarr/t-066 rather than folded into this PR, but the general point is that "match the existing provider's pattern" needs the same scrutiny as any other code being read for reuse, not a pass just because it already merged.

- 2026-08-20 `kapowarr/t-063` — A test written to catch a silent regression must be shown to fail against that regression, not merely to pass against current behaviour -- and for an ordering policy this is cheap to do: break the policy deliberately, run the suite, restore from a byte-copy. Doing it here proved the task's premise rather than assuming it. Transposing two rating components failed four tests, but inserting a NEW component above match correctness failed only the new table guard while all 22 pre-existing pairwise tests passed. That is the exact gap the task described, demonstrated instead of argued, and it is the evidence that belongs in the PR body. Second: lexicographic list comparison is what makes a whole-order assertion possible in one place. Because a result degraded at tier N differs from the baseline first at index N, it loses to one degraded at any later tier regardless of magnitudes -- so ranking one result per tier and sorting them reproduces the policy backwards, and six adjacent-boundary assertions collapse into one readable list. Third: when two ranking components share an input (pack preference and issue-number fit both read result['issue_number']), no single result can vary one alone. Patching the component's return value rather than driving it through a real preference is what isolates it -- and the coupling itself is worth writing into the test, since it is otherwise only discoverable by trying and failing to construct the case.

- 2026-08-20 `kapowarr/t-061` — Deleting special-casing from a fan-out is a contract problem before it is a control-flow problem. search_metadata_with_fallback() could not iterate providers because MetadataProvider had no way to answer "should I be in the fan-out" or "is this error me being unavailable, or a bug" -- so the two questions the old code answered inline (_metron_is_configured(), isinstance against MetronError / CVRateLimitReached) had to become is_configured() and unavailable_errors on the contract first. Once they were there the loop wrote itself. Second: preserve the exact success/failure algebra, not just the happy path. The old code returned ComicVine's results when Metron failed recoverably, even if ComicVine returned an empty list -- so the generalized version has to raise on "every provider was unavailable", tracked with an `answered` flag, NOT on "results is empty". Those two conditions look interchangeable and are not; an empty successful search is a valid answer. Third: order the provider list explicitly rather than inheriting dict insertion order. The registry's order depends on which module imported first, so the fan-out's result order would have been an import-order accident; sorting default-first then alphabetically makes the existing ['comicvine', 'metron'] assertion a guarantee instead of a coincidence.

- 2026-08-20 `kapowarr/t-060` — When a ranking signal is only available from some sources, the shape of the fix is
forced by the sources that lack it, not by the ones that have it. "Prefer available
releases" reads like it wants a seeder-count gradient, but peer counts come only from
Torznab, and a gradient cannot place a no-peer-data result anywhere on it without
either promoting or demoting every non-torrent source for no reason. The only shape
that satisfies "absent data ranks neutrally" is binary: demote proven-dead, treat
unknown and healthy identically. Four lines of production code, and the constraint
picked them.
Second: a rank component that encodes a fact about a release (it has no seeders, so
it cannot download) does not belong behind a user preference, even when every helper
beside it is preference-driven -- the only value a "prefer_available: off" setting
could carry is "please also consider releases that cannot download." A side benefit
worth knowing in this codebase: skipping the settings read also skips the database,
so the helper's unit tests need no Flask app_context, which is exactly why the
pre-existing ranking test has to patch pack_preference_rank.
Third: when placing a new component into an ordered rating list, pin the position
from both sides with named tests. Here availability was deliberately put one tier
above where the task note suggested (above pack preference, since preferring the
shape of an undownloadable release is meaningless); a reviewer who disagrees now sees
a failing named test rather than a silent behaviour change. The tier order is the
actual policy and was otherwise documented only in inline comments -- filed as t-063.
- 2026-08-20 `kapowarr/t-059` — A task note describing an external system's capabilities is a dated snapshot, and
re-checking it is the cheapest first move on any provider-evaluation task. t-059
inherited t-043's (correct-when-written, eight days stale) framing of the Grand Comics
Database as bulk-dump-only; GCD now runs a live public REST API, and the verdict flips
on which access path you evaluate — the dump omits image URLs entirely, forcing the
HTML cover-scraping that the reference consumer (comictagger/gcd_talker) has to do,
while the API returns cover URLs directly.
Second, and the more transferable half: "does the contract fit without special-casing"
is two questions, and the abstract base class answers only the easy one. MetadataProvider,
the registry, the identity store, Volume.add and the add route are all provider-generic
here, but search_metadata_with_fallback() hardcodes exactly two providers and the
contract has no is_configured() for the registry to route around it. Reading the ABC
would have said "fits"; reading every call site said "fits, after one refactor that
deletes the incumbent's special-casing rather than adding the newcomer's beside it."
Read the call sites, not the interface.
Third, four traps that each cost one request to find and would have cost a review cycle
later: fixed 50-item pages with page_size silently ignored (a 1-char query is 3,571
pages, so the incumbent provider's unbounded pagination helper is unsafe to reuse),
an Apache HTML 404 rather than a JSON error for encoded slashes, "1959-00-00" placeholder
dates, and no series-level volume number. Probe the API before designing against it.

---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-21T16:34:35Z_
