# kapowarr/t-043 — Evaluate eMule/aMule for non-US comic catalogs

date: 2026-08-20
target repository: `silasfelinus/Kapowarr` (this document is an evaluation, not a
  patch — the task's own note says *"Require a maintainable client API and matching
  strategy before implementation,"* so the deliverable is whether those two
  preconditions hold)
grounded in: a read-only inspection of this fork at `main` = `b30a0dc`
upstream issue: Casvt/Kapowarr#178, preserved by this fork as "lower-priority
  acquisition research, especially for European and non-US catalogs poorly
  represented in the current source mix"

## The one-line answer

**Do not build it, and the reason is not the one the task anticipated.**

The task set two preconditions — a maintainable client API and a matching strategy —
expecting them to be the hard part. Both fail, and the client-API one fails in the
protocol's own documented words. But the finding that actually matters is upstream of
both: **ed2k cannot fix non-US catalog coverage, because acquisition is not where
that coverage is lost.** Kapowarr only searches for volumes already in the library,
and library volumes come from ComicVine and Metron — two anglophone databases. A
French *bande dessinée* or Italian *fumetto* that ed2k would have found is a volume
Kapowarr was never going to want, because it could not have been added.

Recommendation: **close t-043 as evaluated-and-declined**, and file the one real
lever it uncovered — a non-US metadata provider — as its own task. Two smaller
findings that help the sources we already have are filed alongside it.

Notably, the fork's architecture is *not* the obstacle. Every seam a fourth
acquisition protocol would need already exists and is clean. That is worth saying
plainly, because it means this verdict is about ed2k specifically and would not
transfer to some other future source.

## Precondition 1 — "a maintainable client API": fails, on the record

Every download client this fork speaks to today talks versioned HTTP:
`qBittorrent.py` (246 lines), `Transmission.py` (286), `SABnzbd.py` (337),
`NZBGet.py` (458). All four are small because the remote side does the work of
being an API.

aMule offers no such surface. Its three remote tools — `amulecmd`, `amuleweb`,
`amulegui` — all speak **EC (External Connections)**, a binary tag/TLV protocol on
TCP 4712 with an MD5 password-hash handshake. There is no REST or JSON interface;
`amuleweb` serves a session-cookie HTML application, not endpoints. eMule proper is
Windows-only and has no formal API at all.

Two independent facts make an in-tree EC client a maintenance liability rather than
a 250-line file:

1. **The EC protocol documents itself as a moving target.** From the protocol
   documentation: *"the protocol itself is considered stable and you can rely on it,
   but opcodes, tagnames, tag content formats, and values are still changing,"* with
   the advice to *"include `ECcodes.h` for the values, check this document often, or
   read the source itself."* A Python reimplementation has no versioning contract to
   hold onto — it tracks a C++ header by hand. Compare Kapowarr's other clients,
   which pin against published, versioned APIs.

2. **aMule enforces build-level lockstep.** aMule's own remote-access documentation
   requires that the `amuleweb`/`amulecmd` binary and the `amuled`/`amule` binary
   *come from the same release*, or the connection is rejected with "Invalid protocol
   version." Kapowarr cannot ship "the same release" as whatever aMule build a user
   happens to run. Every existing Kapowarr client tolerates version skew by design;
   this one is specified not to.

The obvious escapes do not survive contact:

| Escape | Why it fails |
|---|---|
| Use an existing Python EC library | The maintained ones do not exist. The best-known candidate, `njoyard/python-amule`, is 6 commits and 1 star, unpublished to PyPI. Nothing here is a dependency this fork should take. |
| Shell out to `amulecmd -c "search ..."` | `amulecmd`'s output is human-readable text with no machine-readable mode. It also puts `amule-utils` inside the Kapowarr container *and* re-imports the same-release lockstep, since the bundled `amulecmd` must match the user's remote `amuled`. |
| Talk to `amuleweb` | HTML plus session cookies. This is screen-scraping a second application, which is strictly worse than the GetComics scraping the fork already carries — GetComics at least has no version-locked binary counterpart. |

Verdict: there is no maintainable client API. This precondition is not close.

## Precondition 2 — "a matching strategy": fails, and specifically because of *our* query shape

This one is more interesting than a flat no, because the mismatch is between two
things that are each individually reasonable.

`ComicQueryBuilder` (`backend/implementations/query_builders.py`, registered for all
three current protocols at line 58) emits natural-language queries in these shapes:

```
{title} Vol. {volume_number} ({year}) TPB
{title} #{issue_number} ({year})
{title} Vol. {volume_number} #{issue_number}
```

Note what is invariant: **the series title always comes first.** That is exactly
right for Newznab/Torznab, which do substring and phrase matching over a full-text
index, and it is fine for GetComics.

It is close to worst-case for ed2k, on both of its networks:

- **Kad routes on the first keyword.** Kad is a Kademlia DHT whose search key is the
  hash of the *first* keyword in the query; the remaining terms are filtered by the
  client locally after results come back. So every Kapowarr query for a series routes
  to the node set keyed on that series' first word — `batman`, `spider`, `x` — the
  single most-contended keyword available, and the discriminating terms (volume,
  year, issue number) never influence which node is asked. Result caps therefore bite
  *before* the terms that would have made the result correct are considered. A query
  builder designed for Kad would put the rarest term first; ours structurally cannot,
  because the first slot is the series name.
- **ed2k servers tokenize away the discriminators.** Server-side search is a keyword
  AND over tokenized filenames. `#12`, `(2011)` and `Vol.` do not survive
  tokenization as the discriminators they are — the query degrades toward
  `batman vol tpb`. The issue number, which is the single most important term in an
  issue search, is the term most reliably destroyed.

There is a second, quieter half to this. ed2k returns filename, size, ed2k hash, and
a source count — nothing else. Filename is genuinely enough for
`extract_filename_data()`, which already handles arbitrary release-title strings from
Torznab, so parsing is *not* the problem. The problem is that the source count, which
is ed2k's only quality signal and the only thing that distinguishes a file that will
arrive from one that will not, has nowhere useful to go:

`SearchResultAvailabilityData` (`backend/base/definitions.py:660`) exists and carries
`seeders`/`leechers` — but `_rank_search_result()` (`backend/features/search.py:57`)
never reads it, and a grep confirms the only consumers are
`frontend/static/js/view_volume.js:385` and the manual-search table column. **Peer
availability is display-only today.** For torrents that is a tolerable gap. For ed2k,
where availability *is* the release quality, it means `auto_search` would pick
blind — and see the next section for what picking blind costs on this network
specifically.

Verdict: no matching strategy exists, and building one means changing the query
builder's contract for a protocol we have already decided not to add.

## The precondition nobody wrote down — the queue has no state for waiting

t-042 found that debrid's cache-wait phase has no `DownloadState` member. ed2k has
the same gap, worse, and as its *normal* case rather than an edge case.

`DownloadState` (`backend/base/definitions.py:564`) offers QUEUED (Kapowarr's own
pre-handoff queue), PAUSED, DOWNLOADING, SEEDING, IMPORTING, FAILED, CANCELED,
SHUTDOWN. Once a download is handed to an external client it reports DOWNLOADING.

ed2k's defining characteristic is that you sit in each source's *upload* queue,
often for hours or days, at position 40-something, transferring nothing. Kapowarr
would render that as DOWNLOADING at 0% indefinitely, with no timeout, no distinct
state, and — per the previous section — no availability signal that would have
predicted it at search time. A torrent with no seeders at least fails visibly and
fast; an ed2k file with two sources looks identical to one that will complete, right
up until it doesn't.

This is not fatal on its own — a "waiting in remote queue" state is a reasonable
thing to add, and debrid would want it too. It is listed here because it is the third
independent precondition, and because it is the one that would surface as user-visible
breakage rather than as developer friction.

## The premise check — and this is the finding that actually matters

Everything above answers "can we build it." This section asks whether it would help,
and the answer changes the shape of the recommendation.

The task's stated purpose is European and non-US catalogs. Trace where that coverage
is actually lost:

Kapowarr's acquisition path only ever runs for a volume **already in the library and
already monitored** — `auto_search(volume_id, issue_id)` searches for something
Kapowarr knows it wants. Volumes enter the library through the metadata layer, and
per `docs/metadata-providers.md` that layer is ComicVine (default authority) plus
Metron (native second provider). Both are anglophone, US-direct-market databases.

So for a Spanish *tebeo*, an Italian *fumetto*, or a Franco-Belgian album:

1. The series is usually absent from ComicVine and Metron.
2. Therefore the volume cannot be added.
3. Therefore nothing is monitored.
4. Therefore no search runs — on ed2k or on any other protocol.

Adding a fourth acquisition protocol does not enter this chain anywhere. **ed2k was
proposed as a fix for a coverage gap that is not an acquisition-layer gap.** Even
granting a perfect aMule client with a perfect Kad-shaped query builder, the set of
non-US comics it would be asked to find is approximately empty, because the library
has no way to want them.

The corollary is the useful part. `docs/metadata-providers.md` describes a real seam
here — providers subclass `MetadataProvider` and register with
`MetadataProviderRegistry`, and the fork already proved the seam works by landing
Metron beside ComicVine with additive `volume_external_ids` identity rather than ID
conversion. A provider with genuine European coverage (the Grand Comics Database is
the obvious candidate — international by construction, and it publishes bulk data
dumps) is the actual lever for this task's stated goal, and it uses a seam that
exists and has been exercised once already.

There is also a cheaper, zero-code answer worth stating for completeness: a user who
wants non-US releases *today* can configure a regional Newznab or Torznab indexer.
That path is already first-class. It does not solve the metadata problem above, but
it means the acquisition layer is not the thing standing in the way.

## What would have fit, for the record

The architecture deserves credit, because it means this verdict is about ed2k and not
about the fork being closed to new sources. A fourth protocol has clean seams waiting
for it:

- `SearchSources.register(DownloadType.X)` (`backend/features/search.py:26`) — a
  protocol registry keyed by download type, with `active_types()` derived from what
  registered. Adding a member is additive.
- `DownloadPreppers.register(identifier)`
  (`backend/implementations/download_preppers.py`) — link-recognition dispatch, so a
  new `ed2k://` prepper needs no special case in the queue.
- `ExternalDownloadClient` (`backend/base/definitions.py:1190`) — a protocol-agnostic
  client ABC carrying its own `download_type`, with routing via
  `ExternalClients.get_least_used_client(DownloadType.X)`.
- `QueryBuilders.register(*download_types)` — already anticipates per-protocol query
  divergence, which is exactly where a Kad-shaped rarest-keyword-first builder would
  have gone.

A grep for `DownloadType.` across the backend returns 16 sites, all of them
registrations or lookups. There is no exhaustive switch that a fourth member would
break. The contamination the task warned about would not have happened here.

The blockers are entirely external: the protocol aMule speaks, the semantics of the
network, and the metadata layer's reach.

## Recommendation

**Decline t-043.** Not "defer" — the two preconditions the task itself set are not
merely unmet today, they are unmet for structural reasons that do not improve with
time. EC's version-lockstep requirement is a design property of aMule, and Kad's
first-keyword routing is a design property of Kademlia. Waiting changes neither.

This differs deliberately from t-042's verdict on debrid, which was *approve the
architecture, defer the schedule* — there, the one risk (no reachable account to test
against) shrank by waiting. Here nothing shrinks by waiting, so leaving t-043 open as
"lower-priority research" would just mean a future session re-deriving this same
answer. Recording the answer is more useful than preserving the question.

Three follow-ups are proposed instead, in descending order of how directly they serve
what t-043 was actually asking for:

1. **Non-US metadata provider** — the real lever. Evaluate a provider with genuine
   international coverage (GCD first) against the existing `MetadataProvider` /
   `MetadataProviderRegistry` seam. This is what unblocks European catalogs; ed2k
   never was.
2. **Make peer availability count** — `SearchResultAvailabilityData` is populated by
   Torznab and consumed only by a UI column. Teaching `_rank_search_result()` to
   prefer available releases helps torrents *today*, independent of any new protocol.
3. **A "waiting in remote queue" download state** — the gap t-042 found for debrid
   caching and this task found for ed2k source queues. Worth its own task whenever
   either lands, and worth the shared design either way.

Only (1) is scoped to this task's stated goal; (2) and (3) are recorded here because
this evaluation is where they surfaced, per scope discipline.

## What I verified, and what I did not

**Verified by reading this fork at `b30a0dc`:** the query formats and their
title-first invariant; that `_rank_search_result()` does not read seeders and that
the only consumers are the frontend table; that `SearchSources`, `DownloadPreppers`,
`ExternalDownloadClient` and `QueryBuilders` are open registries; that
`DownloadState` has no remote-queue member; that all 16 `DownloadType.` reference
sites are registrations or lookups with no exhaustive switch; the four existing
client implementations and their line counts; and that the metadata layer is
ComicVine plus Metron per `docs/metadata-providers.md`.

**Verified against primary external sources:** `amulecmd`'s full command set and that
its output is human-readable text (Debian manpage); that EC is the only bidirectional
remote surface and that amuleweb/amuled must come from the same release (aMule
project remote-access documentation); the EC protocol's own "opcodes, tagnames, tag
content formats, and values are still changing" caveat (EC protocol documentation);
Kad's first-keyword-hash routing with local filtering of remaining terms
(eMule project board); the state of `njoyard/python-amule` (6 commits, 1 star, no
PyPI release).

**Not verified — stated as judgment, not measurement:**

- **Current ed2k/Kad network health.** Sources on this are qualitative and partly
  promotional; I found no trustworthy 2026 figures for server count, active peers, or
  comic-content depth, and I did not connect to the network from this sandbox. The
  recommendation does not rest on the network being dead — it rests on the two
  preconditions and the metadata premise, all three of which hold regardless of how
  healthy ed2k currently is.
- **That GCD is the right non-US provider.** It is the obvious first candidate on
  coverage grounds; its API/dump ergonomics against the `MetadataProvider` contract
  are exactly what follow-up (1) should establish, and this document does not
  pre-judge them.
- **How badly the queries actually degrade in practice.** The tokenization and
  routing behaviour is documented; I did not run live searches to measure the hit
  rate. The structural argument does not depend on the size of the degradation.

**Explicitly not a licensing or legality assessment.** A user-run aMule instance is
the same shape as a user-run qBittorrent, and this fork already leaves that boundary
to the user. One small difference is worth flagging for whoever revisits this: ed2k
needs bootstrap data (a server list, or a `nodes.dat` for Kad) from *somewhere*,
which would be the first time Kapowarr shipped or defaulted to a specific network
endpoint rather than having the user configure one. That is a decision for Silas, not
an agent, and it is moot unless the preconditions above ever change.
