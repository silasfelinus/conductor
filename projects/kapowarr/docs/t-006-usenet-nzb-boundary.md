# kapowarr/t-006 — Design the Usenet/NZB boundary

date: 2026-08-15
target repository: `silasfelinus/Kapowarr` (this document is a design spec, not a
  patch — implementation is t-007/t-008, both `not-started`)
status: design only, per the task note ("research only; do not modify upstream").
  Grounded in a read-only inspection of the live fork source (currently an
  undiverged fork of `Casvt/Kapowarr`); nothing was written to that repository.

## The one-line answer

Usenet/NZB fits Kapowarr's existing architecture at **two separate seams that
already exist for exactly this purpose**: the external-client abstraction (for
submitting to and polling SABnzbd) and the search/result pipeline (for finding
NZBs). Neither seam needs to change shape — they need one new implementation each.
The GetComics scraper (`backend/implementations/getcomics.py`) is not touched by
either seam. This is a smaller, cleaner boundary than a "new download protocol"
suggests: upstream has already been future-proofing for it.

**Evidence upstream is already anticipating this:** `backend/base/definitions.py`
carries this comment directly above `DownloadSource`:

> "Future proofing. In the future, there'll be sources like 'torrent' and
> 'usenet'. In part of the code, we want access to all download sources, and in
> the other part we only want the GC services. So in preparation of the torrent
> and usenet sources coming, we're already making the distinction here."

This fork's m2 work is filling in a seam upstream already framed, not inventing a
new one — consistent with `DESIGN-BRIEF.md`'s framing via upstream issue #71.

## Seam 1 — the external-client abstraction (submission + status polling)

This is the client-facing half: how a download gets handed to SABnzbd and how its
progress gets read back. It is a peer addition next to the two existing external
client families, not a new mechanism.

**Existing shape** (`backend/implementations/external_clients.py`,
`backend/base/definitions.py`):

- `DownloadType` enum: `DIRECT = 1`, `TORRENT = 2`. **Add `USENET = 3`.**
- `ExternalDownloadClient` (ABC, `definitions.py`) defines the full client
  contract every external client must implement: `client_type`, `download_type`,
  `required_tokens`, `id`/`title`/`base_url`/`username`/`password`/`api_token`
  properties, `get_client_data()`, `update_client()`, `delete_client()`,
  `add_download(download_link, target_folder, download_name) -> str`,
  `get_download(download_id) -> dict | None`, `delete_download(download_id,
  delete_files)`, and the static `test(base_url, username, password, api_token)`.
- `BaseExternalClient` (`external_clients.py`) implements the DB-backed plumbing
  of that ABC (the `external_download_clients` table row: title, base_url, auth).
  Concrete clients (`qBittorrent`, `Transmission` in
  `backend/implementations/torrent_clients/`) subclass it and only need to
  implement the four operations above using their own client's API.
- `ExternalClients.get_client_types()` builds its registry via
  `get_subclasses(BaseExternalClient)`, but only after explicitly importing
  `backend.implementations.torrent_clients` first (so those subclasses actually
  exist in memory to be discovered) — see `external_clients.py` lines ~167-175.
  This import is the one place the registry is hand-wired to a package name.

**What to add:**

1. `backend/implementations/usenet_clients/SABnzbd.py` — a `SABnzbd(
   BaseExternalClient)` class, structured exactly like `qBittorrent.py`:
   - `client_type = 'SABnzbd'`, `download_type = DownloadType.USENET`
   - `required_tokens = ('title', 'base_url', 'api_token')` (SABnzbd auths via API
     key, not username/password — matches the existing "some clients don't need
     all fields" pattern already handled by `required_tokens` +
     `update_client()`'s filtering).
   - `add_download()` → SABnzbd's `mode=addurl` (or `addfile` for an uploaded
     `.nzb`) API call; returns SABnzbd's `nzo_id` as the external id (same role
     `qBittorrent.add_download()`'s torrent hash plays).
   - `get_download(download_id)` → poll `mode=queue`/`mode=history`, map SABnzbd's
     status strings to Kapowarr's `DownloadState` via a `state_mapping` dict — the
     exact pattern `qBittorrent.py` uses (`'queuedDL': DownloadState.QUEUED_STATE`,
     etc.) — and return `{'progress', 'speed', 'size', 'state'}`, matching what
     `TorrentDownload.update_status()` already expects verbatim (see Seam 1b).
   - `delete_download()` → SABnzbd's `mode=queue&name=delete` /
     `mode=history&name=delete`, with `delete_files` mapped to SABnzbd's
     `del_files` param.
   - `test()` → hit SABnzbd's `mode=version` or `mode=queue` endpoint with the
     API key; raise `ClientNotWorking`/`CredentialInvalid` exactly like the
     existing clients do.
2. `ExternalClients.get_client_types()` gets one more import line
   (`from backend.implementations.usenet_clients import SABnzbd`), same shape as
   the existing torrent import. No other change to that method — `get_subclasses`
   already discovers anything under `BaseExternalClient`.
3. Settings/credentials UI: `frontend/templates/settings_download_clients.html`
   already renders its client-type list from the client registry (confirmed by
   reading the template — it iterates client types, it doesn't hardcode
   torrent-only strings), so a new `USENET` client type should appear there
   automatically once registered. **Verify this assumption when t-007 is
   implemented** — flagging it here rather than asserting it as fact, since the
   template wasn't traced line-by-line against the live JS rendering it.

### Seam 1b — the download-object side (why polling needs zero new code)

`Download` (ABC) → `ExternalDownload` (ABC, adds `external_client`/`external_id`/
`sleep_event`) → `TorrentDownload(ExternalDownload, BaseDirectDownload)` is the
existing chain (`backend/base/definitions.py`,
`backend/implementations/download_clients.py`). Its `update_status()` is the
entire polling contract:

```python
def update_status(self) -> None:
    if not self.external_id:
        return
    torrent_status = self.external_client.get_download(self.external_id)
    if not torrent_status:
        if torrent_status is None:
            self._state = DownloadState.CANCELED_STATE
        return
    self._progress = torrent_status['progress']
    self._speed = torrent_status['speed']
    self._size = torrent_status['size']
    if self.state not in (DownloadState.CANCELED_STATE, DownloadState.SHUTDOWN_STATE):
        self._state = torrent_status['state']
```

Nothing here mentions torrents specifically — it calls `self.external_client
.get_download()` through the ABC interface and reads four fixed dict keys. **A new
`NZBDownload(ExternalDownload, BaseDirectDownload)` class in
`download_clients.py`, modeled directly on `TorrentDownload`, inherits this exact
method unchanged** (or needs, at most, a trivial override if NZB progress/size
semantics ever diverge — not expected). This is the concrete mechanism behind
"status polling... without coupling Usenet behavior to the existing scraper": the
polling loop was already written generically against the `ExternalDownloadClient`
interface, not against qBittorrent/Transmission specifically.

**One real (small) touchpoint, not zero:** `download_queue.py`'s
`__prepare_downloads_for_queue()` has one `isinstance(download, TorrentDownload)`
branch that starts the background polling thread
(`target=self.__run_torrent_download`). This needs to also recognize
`NZBDownload` — either `isinstance(download, (TorrentDownload, NZBDownload))`, or
better, widen the check to `isinstance(download, ExternalDownload)` and rename
`__run_torrent_download` to something protocol-neutral (e.g.
`__run_external_download`) since its body (start the thread, loop on
`sleep_event`, call `update_status()`) has no torrent-specific logic either, from
what this read-only pass could see. **Flag for t-007: confirm
`__run_torrent_download`'s body has no torrent-only assumptions before renaming
it** — this doc identifies the touchpoint and the likely fix, not a verified diff.

## Seam 2 — NZB discovery (search/indexer path)

This is the separate half the task note calls out explicitly: "Define normalized
search results and handoff so additional indexers/download clients can be
supported later" (this is actually t-008's note, but the boundary is the same
one this task maps).

**Existing shape** (`backend/features/search.py`,
`backend/implementations/getcomics.py`):

- `search_multiple_queries()` / `manual_search()` / `auto_search()` in
  `search.py` currently query exactly one source: GetComics, via
  `getcomics.py`'s scraper.
- Results flow as `SearchResultData` / `MatchedSearchResultData`
  (`definitions.py`) — a `TypedDict` with `link`, `display_title`, `source`, plus
  filename-parsed fields (from `FilenameData`) and match metadata
  (`SearchResultMatchData`). `_rank_search_result()` in `search.py` scores and
  sorts on this shape, source-agnostically — it reads parsed filename/issue data,
  not anything GetComics-specific.
- `GC_DOWNLOAD_SOURCE_TERMS` / `GCDownloadSource` in `definitions.py` are
  explicitly GetComics-scoped (mapping button text on GC pages to a source enum)
  — **do not reuse or extend these for NZB indexers**; they're a different
  concern (parsing one webpage's DOM) from what an indexer search needs.

**What to add (t-008's scope, mapped here so t-007/t-008 don't have to
re-derive it):**

1. A new, separate module (e.g. `backend/implementations/nzb_indexers.py` or a
   package mirroring `torrent_clients/`'s shape if multiple indexer protocols are
   ever needed — Newznab/Torznab-style indexers being the realistic first
   target) that queries configured indexer(s) and returns results already shaped
   as `SearchResultData` (or a subtype) — `link` being the NZB download URL (or
   an indexer-specific token SABnzbd's `add_download` can consume), `source`
   naming the indexer.
2. `search.py`'s `search_multiple_queries()` (or `manual_search`/`auto_search`,
   whichever proves to be the right seam once t-008 is implemented) calls both
   the existing GetComics path and the new indexer path, concatenates the
   results, and lets the existing `_rank_search_result()` do the same
   source-agnostic ranking it already does — **no change to the ranking/matching
   logic itself**, only to what feeds it.
3. `DownloadSource` (`definitions.py`) gets NZB/indexer-specific member(s) added
   (the enum already has the "torrent and usenet sources coming" comment sitting
   right above it — this is the field it was written for).
4. When a user accepts an NZB search result, the handoff to Seam 1 is: construct
   an `NZBDownload` (parallel to how `TorrentDownload` is constructed from an
   accepted torrent/magnet result) with `download_link` = the NZB URL/token,
   `source_type` = the new `DownloadSource` member. `NZBDownload.run()` calls
   `self.external_client.add_download(...)` exactly like
   `TorrentDownload.run()` does today.

**Explicit non-goal, per the task note:** treat upstream issue #71 and any
upstream discussion as research context only. No upstream PR, issue comment, or
code change. This document and the eventual t-007/t-008 implementation are
entirely fork-local.

## Summary — the boundary in one table

| Concern | Existing mechanism | Usenet/NZB addition | Touches scraper? |
|---|---|---|---|
| Submit + poll download | `ExternalDownloadClient` ABC, `ExternalClients` registry | New `SABnzbd(BaseExternalClient)` (t-007) | No |
| Download-object lifecycle | `Download` → `ExternalDownload` → (`TorrentDownload`) | New `NZBDownload(ExternalDownload, BaseDirectDownload)` (t-007) | No |
| Queue thread dispatch | `isinstance(download, TorrentDownload)` in `download_queue.py` | Widen the check (or add a second branch) — the one real shared touchpoint | No |
| Find things to download | `search.py` + `getcomics.py` scraper | New indexer module (t-008), feeds the same `SearchResultData` shape into existing ranking | No — additive, parallel path |
| Enum surface | `DownloadType`, `DownloadSource` | Add `USENET`/indexer members — upstream already left a comment marking this spot | No |

Usenet/NZB support is additive at every seam identified above. The existing
scraper, ranking, and torrent-client code paths need zero behavioral changes;
they need one new sibling each, plus the one queue-dispatch `isinstance` widening
flagged above.

## What this session could not verify

- Did not run the app, so the `settings_download_clients.html` "new client type
  appears automatically" claim in Seam 1 point 3 is a strong inference from
  reading the template, not a confirmed behavior.
- Did not trace `__run_torrent_download`'s full body to confirm it truly has zero
  torrent-specific logic before recommending the rename in Seam 1b — flagged
  explicitly as a t-007 verification step, not asserted as done.
- SABnzbd's actual API response shapes (`mode=queue`/`mode=history` JSON) were
  not fetched from SABnzbd's own docs in this pass — t-007 needs to pull SABnzbd's
  API reference directly when writing the real `state_mapping` table (the
  `qBittorrent.py` `state_mapping` shown above is the pattern to follow, not the
  actual SABnzbd status strings, which are unrelated to qBittorrent's).

## Safety boundaries respected

- Read-only against `silasfelinus/Kapowarr` and `Casvt/Kapowarr` (public GitHub
  content only); no writes, no upstream PR/issue.
- No secrets, DNS, billing, or deploy actions.
- This document is the entire task output — t-006 was scoped as design/research
  only, so (unlike t-002) there is no separate "can't push the patch" gap here:
  the deliverable is complete in `conductor`.
