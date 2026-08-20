# LEARNING-REPORT.md — task-outcome summary

Generated: 2026-08-20T22:37:52Z

Aggregated from the append-only `LEARNING.yaml` ledger. The Reviewer consults this before creating kaizen tasks — systematic weaknesses beat generic improvements (AGENTS.md § "Learning ledger").

## Overall

- Closed tasks recorded: **714**
- Outcomes: blocked: 15, cancelled: 1, done: 698
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
| brainstorm | 17 | 94% |
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
| model-builder | 71 | 100% |
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
| software | 698 | 99% |

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
- 2026-08-20 `kapowarr/t-057` — When a task hands you a premise, measure it before designing around it. t-057 said "a tar carries no per-member checksum, so opens-cleanly is all one could ever assert" and offered two outcomes built on that: implement UNREADABLE/EMPTY-only and never CORRUPT, or decline. The premise is half true. It holds for a bare .tar -- 521 of 531 flipped-byte fixtures open cleanly with the RIGHT member names and the RIGHT member sizes -- and fails for every compressed form, where reading the stream to its end caught every flip (1036/1036 gz, 1042/1042 bz2, 1047/1047 xz) through the wrapper's own checksum, which covers the tar headers as well as the payload and is therefore broader evidence than ZIP's per-member CRC, not weaker. Implementing the design the task specified would have thrown away a 100%-detection signal on the strength of a format claim nobody had tested. The larger lesson is the trap underneath it, and it generalises past tar: the obvious implementation was WORSE THAN DOING NOTHING. Verifying a compressed tar by iterating TarFile members caught 5 of 733 flips, and the other 728 did not merely pass -- they came back with a shorter member list that the existing name-based judge calls OK, so a corrupt five-page archive presents as a healthy one-page archive at every errorlevel setting. A check that degrades into a confident wrong answer is worse than an honest "no opinion", and you only find that out by building the naive version and measuring it rather than reasoning about it. Same shape as t-044's inverted EMPTY test: in this module the expensive mistake is always the false positive. Third: measure to find the honest limits too, not just the wins. The sweep turned up a blind spot nobody asked about -- a bare tar truncated exactly on a 512-byte block boundary still parses as a complete, shorter archive -- which is now a named test asserting the gap rather than a surprise for whoever next reads a passing verdict as a guarantee.
- 2026-08-20 `kapowarr/t-043` — An evaluation task hands you the preconditions it expects to be decisive, and the real work is checking whether they are the binding ones. t-043's note said "require a maintainable client API and matching strategy before implementation." Both fail -- aMule's EC protocol documents its own opcodes and tag formats as "still changing" and requires the client binary to come from the same release as the daemon, and Kad routes every search on the hash of the FIRST keyword, which our query builder guarantees is the series title, the most contended word available. Either finding alone justifies a decline. But answering only those two would have produced a correct verdict on the wrong question, because the task's stated PURPOSE was non-US catalog coverage, and acquisition is not where that coverage is lost: Kapowarr only searches for volumes already in the library, volumes enter via ComicVine + Metron, and a bande dessinee is absent from both -- so it is never added, never monitored, and no protocol is ever asked about it. A fourth download protocol does not enter that chain at any point. Check the premise, not just the preconditions. Second: say plainly when the architecture is NOT the obstacle. Every seam a fourth protocol needs is already open here (SearchSources, DownloadPreppers, ExternalDownloadClient, QueryBuilders are all registries; all 16 DownloadType. reference sites are registrations or lookups, no exhaustive switch). Recording that stops the next source evaluation from re-deriving it and keeps the decline scoped to ed2k instead of reading as "this fork is closed to new sources." Third: this declines rather than defers, and the distinction is worth carrying. t-042 deferred debrid because its one risk (no account to test against) shrinks by waiting. Nothing in t-043 shrinks by waiting -- EC's version lockstep is a property of aMule and first-keyword routing is a property of Kademlia. Leaving it open as "lower-priority research" would only guarantee a future session re-derives the same answer.
- 2026-08-20 `kapowarr/t-042` — Read the actual request before evaluating the feature its name implies. "Debrid support" almost always means feed-a-magnet-to-the-cache, and evaluating that would have produced a correct, well-argued, useless answer -- it has no home in this codebase. Upstream #276 is one sentence, and the operative clause is "instead of having to use Mega directly": the user wants a hoster link unrestricted, which maps onto BaseDirectDownload._convert_to_pure_link() so exactly that PixelDrainDownload is already the template. Same two words, opposite verdicts, and the only thing separating them was reading the issue rather than the label. Second: "does this contaminate the generic architecture with a provider-specific shortcut" cannot be answered without checking whether the architecture is generic today. It is not -- __purify_link is a per-hoster if/elif chain, the queue special-cases Mega by isinstance, and the base class sniffs for Pixeldrain's rate-limit URL. Ten such precedents. A constraint written to protect a clean seam reads very differently once you have confirmed the seam is already provider-shaped, and reporting that honestly is more useful than either enforcing the constraint literally or quietly ignoring it.

- 2026-08-20 `kapowarr/t-045` — Read a multi-part task's code before believing its note about what is left. This one read "add safe extraction for CBR/RAR first, then other practical formats" as though no part had shipped; CBR/RAR had in fact been in comic_reader.py since the reader landed, so the whole task was its second clause. A roadmap note is a snapshot of intent at filing time and goes stale silently -- three minutes of grep resized the work before any of it was planned wrong. The other lesson is that copying an existing pattern is not the same as copying its threat model. list_tar_pages/read_tar_member mirror the ZIP and RAR pairs almost line for line, and mirroring them exactly would have shipped a file-read primitive: a tar, unlike a zip, can carry symlink members, and extractfile() resolves the link target, so a member named 001.jpg pointing at /etc/passwd would have been served straight back through the authenticated page endpoint. The guard is one isfile() check, but nothing in the pattern being copied would have suggested needing it. When adding a sibling format, ask what the new container can express that the old one could not.

- 2026-08-20 `kapowarr/t-035` — Before writing an adapter for a third-party API you cannot reach, spend the time to read that service's own implementation, not just its documentation, and not memory. NZBGet's published API docs omit a required parameter from `append`'s argument list and ship an example passing 10 of 11 arguments; either would have produced a client that fails on its very first call. Reading the source also surfaced three facts that changed the design rather than the comments -- JSON-RPC 1.1 with no `jsonrpc` member in replies, post-processing happening in the queue so history is terminal, and the firm absence of any per-group download rate. Where a value's vocabulary is still uncertain, key on its stable part (a status prefix) and default the unknown case to the safe reading, so the adapter survives versions nobody here can test against.


---
_Auto-generated by `scripts/build_learning_summary.py` at 2026-08-20T22:37:52Z_
