# kapowarr/t-042 — Evaluate debrid acquisition support

date: 2026-08-20
target repository: `silasfelinus/Kapowarr` (this document is an evaluation, not a
  patch — the task says "Implement only if it adds meaningful coverage without
  contaminating generic search/download architecture with a provider-specific
  shortcut," so the deliverable is the assessment and a recommendation)
grounded in: a read-only inspection of this fork at `main` = `b30a0dc`
upstream issue: [Casvt/Kapowarr#276](https://github.com/Casvt/Kapowarr/issues/276)

## The one-line answer

**The answer depends entirely on which "debrid support" is meant, and the two
readings have opposite verdicts.** The one upstream actually asked for —
*unrestrict a hoster link I already have* — fits an extension point Kapowarr
already has and needs no new abstraction. The one the word usually implies —
*feed a magnet to the service and wait for its cache* — has no home here and would
require the provider-specific contamination the task warns against.

Recommendation: **approve the first, rule out the second, build neither yet.**
See "Recommendation" for why the schedule answer differs from the architecture one.

## What was actually asked for — this is the crux

Upstream #276 is one sentence from @saezon:

> "I'd like for Kapowarr to add Debrid download support, such as real-debrid,
> instead of having to use Mega directly."

Read carefully: *instead of having to use Mega directly*. This is **not** the
`*arr`-typical debrid pattern. It is the **hoster-unrestrictor** pattern: the user
already has a Real-Debrid subscription, GetComics serves the comic behind a
Mega/MediaFire/Pixeldrain link, and they want Kapowarr to hand that link to their
debrid account and download the unrestricted result instead of fighting the free
tier.

Conflating the two is what makes "debrid support" sound like a large architectural
question. It is worth being explicit, because the verdict inverts:

| | hoster-unrestrictor (**what #276 asks**) | torrent-cache (what "debrid" usually means) |
|---|---|---|
| Input | an existing `GCDownloadSource` link | a magnet / `.torrent` |
| Output | a plain HTTPS URL | a plain HTTPS URL, after a cache wait |
| Fits an existing hook | **yes — `_convert_to_pure_link()`** | no |
| New `DownloadType` needed | none — it stays `DIRECT` | none, but see the migration trap below |
| Async "still caching" phase | no | **yes, and `DownloadState` has no member for it** |
| Result shape | one file | often many files, or a server-side ZIP |
| Touches seeding / `PostProcessorTorrentsCopy` | no | yes |

Everything below is about the first column unless it says otherwise.

## Why the unrestrictor half fits: the hook already exists and is already this shape

`backend/implementations/download_clients.py` defines `BaseDirectDownload`
(line 56) — a complete, self-contained HTTPS downloader with resume, retries,
chunked progress, websocket queue events and cancellation. Its run path calls this
at line 206:

```python
self._pure_link = self._convert_to_pure_link()
```

`_convert_to_pure_link()` (declared line 243) is overridden by every hoster
subclass — six overrides today, covering `DirectDownload`, `MediaFireDownload`,
`WeTransferDownload`, `PixelDrainDownload`, `MegaDownload` and the folder variants.
Its entire job is: *turn a share-page link into a URL that streams bytes*.

That is a debrid unrestrict call, verbatim. Real-Debrid's
`POST /rest/1.0/unrestrict/link` takes a hoster link and returns a direct download
URL; AllDebrid's `/link/unlock` and Premiumize's `/transfer/directdl` are the same
shape.

The template already exists and is almost exactly the target: **`PixelDrainDownload`**
(line 518) overrides `_convert_to_pure_link()` *and* `_fetch_pure_link()` (line 566)
to inject an `Authorization` header from a stored account credential. A
`DebridDownload(BaseDirectDownload)` is that class with a different endpoint.
It inherits progress, size, speed, state, pause/stop, the `DownloadHandler` queue,
and — critically — plain `PostProcessor` import, because from `main`'s point of
view it is an ordinary direct download of one file into the download folder. No
`RemoteMappings` translation, no seeding path, no `PostProcessorTorrentsCopy`.

Registration is free: `download_queue.py` line 54 builds
`download_type_to_class` from `get_subclasses(BaseDirectDownload)`, so a new
subclass with a unique `identifier` is reconstructable from the DB automatically.

## Where the credential belongs — and where it does not

Kapowarr has **two unrelated credential systems**, and picking the wrong one is the
easiest way to make this ugly:

- **`external_download_clients`** (`backend/internals/db.py:462`) — for daemons you
  poll (qBittorrent, SABnzbd, NZBGet). **Wrong home.** `base_url` is mandatory and
  non-null-checked in two places, so a debrid provider would need a fake constant
  stuffed into it; and the frontend form vocabulary is *closed* — the options API
  returns only `required_tokens`, and `settings_download_clients.js` renders three
  literal branches for `username`/`password`/`api_token`. Registration also
  requires editing a hardcoded import block inside `ExternalClients.get_client_types()`.
- **`credentials`** (`backend/implementations/credentials.py`, `CredentialSource`
  enum currently `MEGA`, `PIXELDRAIN`) — **right home.** It already models exactly
  "an account credential that a direct download consumes to unlock a link," and
  `PixelDrainDownload` already consumes it that way. Cost: one enum member plus one
  branch in `Credentials.add`'s `if/elif ... assert_never` chain. Caveat: there is
  no generic frontend form for credential sources the way there is for clients, so
  the UI is a small hand-built addition rather than free.

## The one genuinely awkward part: dispatch precedence

A debrid provider is a **transformer, not a source** — it wants to intercept links
another prepper already owns. `DownloadPreppers.get_for_link`
(`backend/implementations/download_preppers.py:75`) is a **first-match-wins linear
scan in decorator-registration order**, with no priority field. Making a debrid
prepper take precedence over `GetComicsDownloadPrepper` therefore means depending
on registration order — load-bearing behaviour expressed as source-file ordering,
which is exactly the kind of thing that breaks silently later.

Two workable shapes, both modest:

1. **Add a priority to the prepper registry** (small, general, benefits the three
   existing preppers too) and register debrid high.
2. **An early return inside `getcomics.py::__purify_link`** (~line 500), ahead of
   the existing `if/elif` chain on `GCDownloadSource`: if a debrid credential is
   configured, return `DebridDownload`; otherwise fall through untouched.

Option 1 is the better change and the one to prefer.

**On the task's "provider-specific shortcut" warning — the shortcut already
exists, ten times over.** This matters for judging the proposal fairly, so it is
worth listing rather than asserting:

- `__purify_link` is a flat `if/elif` on `GCDownloadSource` with URL-substring
  sub-branches per provider.
- `download_queue.py:725` `_remove_mega()` sweeps the queue by
  `isinstance(download, MegaDownload)`.
- `MegaDownload` (line 629) bypasses `BaseDirectDownload.__init__` entirely and
  reimplements `size`/`progress`/`speed` as properties delegating to `MegaABC` — a
  second progress model behind the same interface.
- `BaseDirectDownload.__init__` itself sniffs `Constants.PIXELDRAIN_API_URL` and a
  403 to raise `DownloadLimitReached` — provider logic leaked into the base class.
- `TorrentDownload.__init__` calls the third-party `magnet2torrent.com`.
- Torznab links carry a Kapowarr-invented fragment tag purely so the prepper
  registry can recognise them — a direct precedent for *tagging a link to route it*.
- `create_torznab_download` reuses `DownloadSource.GETCOMICS_TORRENT` for
  non-GetComics torrents, with a comment apologising for it.

Debrid would not be introducing provider-specific branching into a clean generic
architecture. It would be adding one branch to a seam that is already explicitly
provider-shaped — and, via option 1 above, could leave that seam slightly better
than it found it. That is an argument for the integration being cheap. It is not an
argument that this area of the codebase is clean.

## What it buys — the motivation is real and already modelled

Kapowarr already has a first-class failure mode for exactly the problem debrid
solves. `backend/base/definitions.py:502`:

```
ONLY_RATE_LIMITED_LINKS = "All working download links on the webpage are from rate limited services"
```

`getcomics.py:725` raises it when every candidate link on a page belongs to a
hoster that has rate-limited the user, and `download_clients.py` raises
`DownloadLimitReached(DownloadSource.PIXELDRAIN)` in two places when Pixeldrain's
`/misc/rate_limits` says the quota is spent.

The codebase already knows that "the comic is right there and the free tier won't
give it to me" is a distinct, common outcome — distinct enough to have its own enum
member and its own exception. A debrid account is the direct answer to that
specific failure, and a user holding one currently cannot use it. That is
meaningful coverage, not a novelty.

## Why the torrent-cache half is a different, worse proposition

Ruled out deliberately, not overlooked:

1. **No state for the wait.** `DownloadState` (`definitions.py:564`) has no
   "caching" member, and a not-yet-cached magnet is a real, minutes-long phase.
   Worse, `BaseDirectDownload.__init__` resolves the pure link **eagerly in the
   constructor** and calls `raise_for_status()` — an uncached magnet fails outright
   at enqueue rather than waiting.
2. **`DownloadType` is a settings-migration trap.** Adding a fourth member is not
   just an enum edit: `SOURCE_PREFERENCE_OPTIONS = ('direct','torrent','usenet')`
   in `acquisition_preferences.py:18` is **length- and set-validated** by
   `_validated_source_preference`, so a new member is a breaking settings
   migration. The unrestrictor design needs no new member; the cache design invites
   one.
3. **Multi-file results have no representation.** A cached torrent typically
   unrestricts to one URL per file. `Download.files` is a `List[str]`, but plain
   `PostProcessor.move_to_dest` only ever touches `files[0]`, and folder expansion
   (`_expand_external_download_root`) is wired only into the torrent/usenet
   processors. Nothing today combines "non-external download" with "folder result."

## Risks and honest unknowns for the half that is approved

1. **Link freshness is unmodelled — the sharpest real risk.**
   `BaseDirectDownload.__init__` resolves eagerly, and `__load_downloads`
   (`download_queue.py:600`) re-instantiates every queued download from the
   *persisted* `download_link` on restart. Storing the original hoster link and
   re-unrestricting on each construction is the correct shape and the abstraction
   supports it. But debrid direct URLs are typically short-lived and IP-bound, and
   `run()`'s retry loop re-`GET`s the same `pure_link` — there is **no hook for
   "link expired mid-download, re-resolve."** Any implementation needs to add one
   or accept that a long download that outlives its URL fails and restarts.
2. **Unverifiable, like the Usenet clients before it.** No debrid account is
   reachable from an agent sandbox, so an implementation ships on mocked tests plus
   a reading of the provider's API docs. That is the position `kapowarr/t-035`
   (NZBGet) shipped from — and t-035's own LEARNING entry records that NZBGet's
   *published docs were wrong* about a required parameter, caught only by reading
   the service's source. Real-Debrid has no public source to read. This is the
   largest risk and it is not architectural.
3. **Which providers.** Real-Debrid, AllDebrid, Premiumize, TorBox and Debrid-Link
   differ in endpoint shape and error vocabulary. Supporting one is the cost below;
   supporting "debrid" as a category multiplies it. #276 names only Real-Debrid.
4. **Terms of service.** Unrestricting a hoster link through a paid account the
   user owns is the service's advertised purpose, so this raises none of the
   questions `t-040`/`t-041` are gated on. Noted only so the distinction is on the
   record: those milestone-8 siblings are gated for a reason that does not apply
   here.
5. **Silent scope creep into the cache pattern.** Once an account is configured,
   "why doesn't it also take the magnets?" is the obvious next request. Any
   implementation should say in its own class docstring that it is deliberately
   unrestrict-only.

## Cost estimate (unrestrictor only)

Small, and mostly test surface:

- `DebridDownload(BaseDirectDownload)` overriding `_convert_to_pure_link()` and
  `_fetch_pure_link()`, modelled on `PixelDrainDownload` (~60 lines).
- Prepper priority in `DownloadPreppers`, plus a `DebridDownloadPrepper` (~30
  lines), or the `__purify_link` early return as the cheaper fallback.
- One `CredentialSource` member, one branch in `Credentials.add`, and a small
  settings-UI addition (no generic form exists for credential sources).
- Tests: mocked unrestrict responses, dispatch precedence, expired-link behaviour,
  and the "no debrid configured → existing behaviour byte-identical" case.

No DB migration. No new `DownloadType`. No post-processing change.

## Recommendation

**Architecturally: approve the unrestrictor, rule out the torrent-cache.** The
boundary is clean, the hook exists, the credential system already models this, and
the one awkward part (prepper precedence) is an improvement the registry wants
anyway.

**Schedule: not next.** Two reasons, both priority rather than fit:

- `docs/ARR_PARITY.md`'s "Near-term roadmap" lists seven items and debrid is not
  among them. Ahead of it: portable-metadata UI, ComicVine failure taxonomy,
  quality profiles, updates UX, navigation, import-list providers — all of which
  affect every user, where debrid affects only users holding a paid subscription.
- The risk that matters (2 above) is *reduced by waiting for Silas*, not by
  building sooner. If Silas has a Real-Debrid account, this becomes an ordinary
  verifiable feature and jumps the queue. If not, it is ship-on-mocks-and-hope
  against a paid API for a userbase of zero, and the honest move is to leave it in
  the backlog rather than write untestable code.

**Concretely:** `t-042` asked for an evaluation, and this document is it — the task
closes `done`. Implementation is filed separately as **`t-058`**, at soft
`needs-human`, because it turns on one question only Silas can answer: *does he
have a debrid account to verify against?* If yes, t-058 is an ordinary verifiable
feature and should jump the queue; if no, it stays in the backlog until the
ARR_PARITY near-term list is cleared.

A future implementer should not need to re-derive any of the above. Two open
questions remain, and both are decisions rather than research: **which provider,
and is there a live account to test against.**

## Appendix — files a future implementer will need

| File | Why |
|---|---|
| `backend/implementations/download_clients.py` | `BaseDirectDownload` (56); the `_convert_to_pure_link()` contract (206, 243); `PixelDrainDownload` (518) and its `_fetch_pure_link` (566) — the closest template; `MegaDownload` (629) for how far a subclass may diverge |
| `backend/implementations/download_preppers.py` | `DownloadPrepper` ABC (29) and `get_for_link` (75) — the first-match-wins scan that needs a priority |
| `backend/implementations/getcomics.py` | `__purify_link` (~482-565) — the fallback dispatch site |
| `backend/implementations/credentials.py` | `Credentials.add`'s `if/elif ... assert_never` chain (92-139) — where the API token registers |
| `backend/features/download_queue.py` | `download_type_to_class` (54), the auto-registry; `__load_downloads` (600), why link freshness matters; `_remove_mega` (725), the existing `isinstance` precedent |
| `backend/features/post_processing.py` | `PostProcessor.move_to_dest` (162) — the single-file assumption that rules out multi-file debrid results |
| `backend/base/definitions.py` | `DownloadType` (507), `DownloadState` (564), `GCDownloadSource` (515), `ONLY_RATE_LIMITED_LINKS` (502), `CredentialSource` (447) |
| `backend/features/acquisition_preferences.py` | `SOURCE_PREFERENCE_OPTIONS` (18) and `_validated_source_preference` (51) — why adding a `DownloadType` member is a breaking migration |
| `projects/kapowarr/docs/t-006-usenet-nzb-boundary.md` | the sibling evaluation this one is modelled on — Usenet genuinely needed two seams; debrid needs one |
