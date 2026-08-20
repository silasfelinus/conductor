# kapowarr/t-059 — Evaluate a metadata provider with genuine non-US comic coverage (GCD first)

date: 2026-08-20
target repository: `silasfelinus/Kapowarr` (this document is an evaluation, not a
  patch — the task's own note says the deliverable is *"an evaluation doc with a
  recommendation, same shape as t-042/t-043; implement only if the contract fits
  without special-casing"*)
grounded in: a read-only inspection of this fork at `main` = `36d90f7`, plus live
  measurement against the Grand Comics Database's public API from this sandbox
filed from: t-043 (`projects/kapowarr/docs/t-043-ed2k-boundary.md`), which found that
  non-US coverage is lost at the metadata layer, not the acquisition layer

## The one-line answer

**Build it — but not as the first commit.** GCD's coverage is real and measured, and
the `MetadataProvider` contract fits it better than expected. What does *not* fit is
one function: `search_metadata_with_fallback()` is a hardcoded two-provider fan-out,
not a registry-driven one. A GCD provider dropped in today would have to special-case
itself beside Metron inside that function — precisely what this task's note says not
to do.

So the verdict splits cleanly:

- The **contract** (`MetadataProvider`, `MetadataProviderRegistry`,
  `MetadataIdentityStore`, `VolumeMetadata`/`IssueMetadata`, `Volume.add`) fits GCD
  with no special-casing at all. Verified by reading every call site.
- The **fan-out** does not, and the fix is to *remove* Metron's existing special-casing
  rather than add GCD's beside it. That is a small, self-contained refactor worth doing
  on its own merits.

Recommendation: **close t-059 as evaluated-and-approved**, and file two tasks — the
fan-out generalization, and the GCD provider that depends on it. Details in
"Recommendation" below.

One thing changed since this task was filed, and it changes the shape of the answer.
The task inherited t-043's assumption that GCD is a bulk-dump-only source ("publishes
bulk data dumps"). **That is now out of date: GCD has a live public REST API**, and it
is materially better suited to Kapowarr than the dump is. The evaluation below is
mostly about the API; the dump is covered because the API is explicitly labelled
unstable and the dump is the fallback.

## Precondition 1 — coverage: does GCD actually have non-US comics?

Yes, and this is the one part of the evaluation that needs no hedging, because it was
measured rather than assumed.

`GET /api/series/name/Tintin/` returns **145 series**. The first page of 50, grouped by
GCD's `country`/`language` fields:

| country/language | series | country/language | series |
|---|---|---|---|
| be/fr (Belgian French) | 12 | dk/da | 2 |
| fr/fr | 8 | be/en, be/nl, be/pcd (Picard) | 1 each |
| it/it | 4 | gb/sco, gb/gd, gb/ga, gb/cy | 1 each |
| pt/pt | 4 | th/th, no/no, de/de, nl/nl | 1 each |
| us/en | 3 | es/es | 3 |
| gb/en | 3 | | |

Franco-Belgian albums outnumber US editions 20 to 3 on that page. `Astérix` returns
188 series. `Tex` — the Italian fumetto t-043 named specifically — returns **389**,
the largest being *Collana del Tex* (`it`/`it`, 973 issues).

This is exactly the catalog t-043 said Kapowarr structurally cannot want today, and
GCD carries it as first-class data, not as an afterthought: `country` and `language`
are fields on every series record, not tags. Wikipedia's figures for the project
(March 2025) are 212,300 series and 2,110,000 issues across "over a hundred
languages."

Precondition 1 passes without qualification. This is the right provider for the stated
goal.

## Precondition 2 — access: the API exists, and it beats the dump for this use

t-043 assumed bulk dumps. Both paths exist; they are not close in suitability.

### The dump path (what the task inherited)

GCD publishes a full database dump — MySQL, PostgreSQL, and SQLite3 — regenerated
bi-weekly, behind a comics.org account login, at roughly 6 GB. The reference consumer
is `comictagger/gcd_talker`, and reading it is instructive about what this path costs:

- the user must create a GCD account, manually download a multi-GB file, and configure
  a filesystem path (`gcd_filepath`);
- the talker builds its own FTS5 virtual table and its own secondary index on first
  use (`CREATE VIRTUAL TABLE fts USING fts5(...)`, `CREATE INDEX issue_id_on_type_id
  ON gcd_story (type_id, issue_id)`), because the dump ships neither;
- **the dump contains no image URLs at all.** gcd_talker's README states this in bold.
  Its workaround is to scrape `comics.org/issue/<id>/cover/4` with BeautifulSoup and
  check for `id="challenge-error-title"` to detect Cloudflare blocking the scrape.

That last point matters for Kapowarr specifically, because `VolumeMetadata` carries
`cover_link`, `cover_source` and `cover` bytes, and `CoverProvenance` exists to record
where a cover came from. A dump-backed provider would have to either give up on covers
or reintroduce HTML scraping — and I reproduced the Cloudflare block from this sandbox
(see "What I verified" below), so the scrape is not reliably available here either.

The freshness story is also wrong for a monitoring application: bi-weekly, plus
however long between the user's manual re-downloads. Kapowarr's whole job is noticing
that a new issue exists.

### The API path

`https://www.comics.org/api/` is live, publicly reachable, and returns clean JSON. The
GCD project's own wiki describes it as "an initial version," with this caveat, quoted
because it is the main risk in this whole evaluation:

> While the API endpoints URLs are stable, the provided fields and data format should
> not be considered stable as this point.

and this one, which is the second-biggest risk:

> Currently the API is accessible for anonymous users with some limits on the number
> of accesses per hour and as a logged in [user] with some larger limits. This will
> likely change, e.g., the anonymous access will likely bye turned off at some point.

Authentication is `BasicAuthentication`/`SessionAuthentication` — a GCD account
username and password, **not** an API token.

The endpoints, from the OpenAPI schema at `/api/schema/`:

```
/api/series/                                     /api/publisher/
/api/series/{id}/                                /api/publisher/{id}/
/api/series/{id}/overview/                       /api/issue/{id}/
/api/series/name/{name}/                         /api/issue/on_sale_weekly/{year}/week/{week}/
/api/series/name/{name}/year/{year}/
/api/series/name/{name}/issue/{number}/
/api/series/name/{name}/issue/{number}/year/{year}/
```

Crucially, **the API returns cover URLs that the dump omits**. An issue record carries
`cover: "https://files1.comics.org//img/gcd/covers_by_id/550/w400/550394.jpg"`, and
the `overview` endpoint carries `cover_url` per issue. The API path solves the exact
problem that forces gcd_talker into scraping.

Precondition 2 passes for the API and fails for the dump. Build against the API; treat
the dump as a documented fallback if anonymous access is withdrawn, not as the design.

## Precondition 3 — does it fit `MetadataProvider`?

This is where the task said the real work was, and the answer is mostly yes with four
specific frictions.

### `search_volumes(query)` → `GET /api/series/name/{name}/`

Works, with two measured defects that an implementation must handle deliberately.

**(a) The query is a path segment, and encoded slashes 404.** A series whose title
contains `/` cannot be searched:

```
/api/series/name/Batman%2FSuperman/  ->  HTTP 404  (Apache HTML, not JSON)
/api/series/name/Ast%C3%A9rix/       ->  HTTP 200, count 188
```

Percent-encoding does not help — this is Apache's default `AllowEncodedSlashes off`,
upstream of Django. Note the failure returns an **Apache HTML error page, not a JSON
error body**, so a provider must guard its `json()` call the way Metron's `_get()`
already does (`except (ClientError, ValueError) -> MetronError`). Non-ASCII is fine.
The mitigation is to strip or split on `/` in the query, and accept that a handful of
titles are search-unreachable by name (they remain reachable by ID).

**(b) Page size is fixed at 50 and the result set is unbounded.** `page_size` and
`limit` are both silently ignored — the schema documents only `page` and `format` as
query parameters. A one-character query returns **178,526 results = 3,571 pages**:

```
/api/series/name/a/  ->  count 178526, page len 50
/api/series/name/Tex/?page_size=5  ->  count 389, page len 50   (page_size ignored)
```

Metron's `_all()` helper loops until `next` is null. **Reusing that helper verbatim for
GCD search would issue 3,571 requests for a short query.** A GCD provider needs its own
capped pagination for search (Metron caps effectively via `page_size: 50` on a smaller
corpus; GCD offers no such lever). This is the single most likely way a naive
implementation goes wrong.

Also worth recording because it cost me a request to discover: the API is Django REST
Framework with a browsable HTML renderer. Without `Accept: application/json` or
`?format=json` you get an HTML page, HTTP 200. Metron's `AsyncSession` would need the
header set explicitly.

### `fetch_volume(external_id)` → `GET /api/series/{id}/` + `GET /api/series/{id}/overview/`

This is the pleasant surprise. The `overview` endpoint — present in the schema but not
in the wiki — returns per-issue records shaped almost exactly like `IssueMetadata`:

```json
{"issue_id": 566399, "descriptor": "368 - King Ottokar's Sceptre", "number": "368",
 "publication_date": "1959", "on_sale_date": "", "key_date": "1959-00-00",
 "cover_url": "https://files1.comics.org//img/gcd/covers_by_id/550/w400/550394.jpg",
 "longest_story": {"type": "comic story", "title": "...", "page_count": "62.000", ...}}
```

That means Kapowarr can populate a volume's entire issue list without one detail
request per issue — the same optimization Metron's `fetch_volume()` makes deliberately
(`backend/implementations/metron.py:176-179`: *"Avoid a detail request per issue: a
long-running series can otherwise exhaust Metron's burst quota"*). The cost is
`ceil(issues / 50)` requests. Measured on the 973-issue *Collana del Tex*: **20
requests, 973 issues, 11.5 seconds, all HTTP 200, no throttling observed** anonymously.

The `Series` record itself maps less cleanly. Fields returned are `api_url, name,
country, language, active_issues, issue_descriptors, color, dimensions, paper_stock,
binding, publishing_format, notes, year_began, year_ended, publisher`. Against
`VolumeMetadata` (`backend/base/definitions.py:790`):

| `VolumeMetadata` field | GCD source | Friction |
|---|---|---|
| `title` | `name` | none |
| `year` | `year_began` | none |
| `external_id` / `provider_id` | series id / `'gcd'` | none |
| `comicvine_id` | — | `None`. GCD has no CV cross-link, unlike Metron's `cv_id`. Fine — `comicvine_id` is nullable throughout and `Volume.add` (`volumes.py:1100`) already treats it as optional. |
| `issue_count` | `len(active_issues)` | derived, not given |
| `site_url` | `https://www.comics.org/series/<id>/` | constructed |
| `description` | — | **no field.** `notes` is the nearest thing and is usually empty. Would be `''`. |
| `publisher` | `publisher` is a **URL** | **one extra request per series.** ComicVine and Metron both inline the publisher name. Fetch it in `fetch_volume` only, never per search result — 50 search hits would otherwise mean 50 extra requests. A small id→name cache is worth it; publishers repeat heavily. |
| `cover_link` / `cover_source` / `cover` | first `overview` row's `cover_url` | Metron already does exactly this fallback (`metron.py:173-175`). Note some issues have `cover_url: ""`. |
| `aliases` | — | `[]` |
| `volume_number` | — | **no equivalent.** See below. |
| `translated` | — | `False`, though `language` makes a real value derivable |

**`volume_number` is the one genuine semantic mismatch.** `VolumeMetadata` requires
`volume_number: int`. GCD has no series-level volume number; it has `year_began`, and
issue records carry a `volume` string that is frequently empty (`"volume": ""` on the
Tintin issue above). gcd_talker resolves this with a user setting,
`gcd_use_series_start_as_volume`, i.e. "use the series start year as the volume
number." Metron defaults to `int(data.get('volume') or 1)`. Defaulting to `1` is the
conservative choice and is what the contract tolerates; the year-as-volume behaviour
should not be adopted silently, because it changes folder naming and matching.

### `fetch_issues(volume_external_ids)` → the same `overview` endpoint

Direct. Per-issue mapping against `IssueMetadata` (`definitions.py:780`):

| field | GCD source | Friction |
|---|---|---|
| `external_id` | `issue_id` | none |
| `volume_external_id` | the requested series id | none |
| `issue_number` | `number` | none |
| `calculated_issue_number` | `extract_issue_number(number)` | reuse Metron's line verbatim |
| `title` | parse from `descriptor`, or `longest_story.title` | `descriptor` is `"368 - King Ottokar's Sceptre"`; the API also exposes `title` on the full issue record |
| `description` | `longest_story` synopsis | partial |
| `date` | `key_date` / `on_sale_date` / `publication_date` | **needs real normalization.** See below. |

**Dates need work.** GCD's `key_date` uses zero placeholders for unknown components —
`"1959-00-00"` is a real returned value, and it is not a valid date. `publication_date`
is free text (`"1959"`). `on_sale_date` is a proper ISO date when present and empty
when not (in the six-issue Tintin sample, one of six had it). Metron reads a single
settings-selected field (`self.date_type`, `cover_date` or `store_date`) and passes it
through unmodified. A GCD provider cannot do that — it needs an explicit
`on_sale_date or normalize(key_date) or None` ladder, where `normalize` rejects or
truncates `-00-` components rather than emitting them.

### `test_key()`, `fetch_volumes()`, capabilities

`fetch_volumes()` is a loop over `fetch_volume()`, exactly as Metron does
(`metron.py:190-193`). `test_key()` has no key to test — a cheap `GET /api/series/1/`
probe is the honest equivalent, and once credentials are configured it doubles as a
credential check. All five `MetadataCapability` members apply, `COVERS` included
(because the API returns cover URLs — this would be false for a dump-backed provider).

## The blocker the contract does not show you

Everything above is about the abstract class. The thing that actually stops a clean
drop-in is one concrete function.

`search_metadata_with_fallback()` (`backend/features/metadata.py:233`) is **hardcoded
to exactly two providers**:

```python
comicvine_search = search_provider('comicvine')
if not _metron_is_configured():
    return await comicvine_search

from backend.implementations.metron import MetronError
comicvine_result, metron_result = await gather(
    comicvine_search,
    get_metadata_provider('metron').search_volumes(query),
    return_exceptions=True
)
```

It imports `MetronError` by name, calls `_metron_is_configured()`
(`metadata.py:224`, which reads `settings.metron_*` directly), and its error handling
is a two-way `gather` with provider-specific exception branches. `_metron_is_configured()`
is called at four sites in that file.

The registry cannot help, because **the contract has no notion of "configured."**
`MetadataProvider` (`metadata.py:29`) declares `test_key`, `search_volumes`,
`fetch_volume`, `fetch_volumes`, `fetch_issues` — nothing that answers "should I be in
the fan-out." Metron's constructor raises `MetronError` when credentials are absent,
which is why the check lives outside as a settings peek.

Three smaller hardcodings compound it:

- `MetadataProviderRegistry.get()` (`metadata.py:133`) lazily imports `'comicvine'` or
  `'metron'` by name — a third provider needs a third branch.
- `MetadataProviderRegistry.capabilities()` (`metadata.py:147`) does the same.
- `Settings` (`backend/internals/settings.py:75-77`) declares `metron_api_token`,
  `metron_username`, `metron_password`, and those names are repeated in three more
  places including the secrets-masking lists (`settings.py:161, 198, 514`).

So the honest read of "does the contract fit without special-casing" is: **the contract
does; the code around it does not, yet.** But the required change is a generalization,
not a workaround — replacing `_metron_is_configured()` with an `is_configured()`
classmethod on `MetadataProvider` and iterating registered providers deletes Metron's
special-casing rather than adding GCD's alongside it. That is a strictly better
codebase afterwards, independent of whether GCD ever lands.

Worth saying plainly, because it is the opposite of t-043's finding: **everything
downstream of search is already generic.** `Volume.add(..., metadata_provider_id,
metadata_external_id)` (`volumes.py:1100`) dispatches through
`get_metadata_provider(provider_id).fetch_volume(external_id)` for anything that is
not ComicVine; the refresh path picks a provider from stored identity with a generic
`next(iter(identities.items()))` fallback (`volumes.py:1471-1477`); the POST
`/api/volumes` route already accepts `provider_id`/`external_id`
(`frontend/api.py:796`); and `MetadataIdentityStore` enforces one-ID-per-provider
additively. The Metron cycle bought real genericity everywhere except the fan-out.

## Cost model

Measured, anonymous, from this sandbox:

| Operation | Requests | Measured |
|---|---|---|
| Series-name search, one page | 1 | 3.1s for `Tex` (389 hits, 50 returned) |
| Add a 973-issue series (issues only) | 20 | 11.5s, all 200, no throttling |
| Add a typical 6-issue series | 1 series + 1 overview + 1 publisher = 3 | ~1.2s each |
| Full issue refresh for a series | `ceil(n/50)` | linear |

No `429` was returned across 20 sequential requests in 11.5 seconds. That is not proof
of a generous limit — the wiki says limits exist and are lower for anonymous users —
but it is enough to say the documented per-hour throttle is not tight enough to make
ordinary library operations awkward at this scale. **Not measured: the authenticated
limit, because I have no GCD account.**

## Licensing — a decision for Silas, not a blocker on this evaluation

GCD data is Creative Commons licensed and the license requires attribution and a link
back to the relevant comics.org page. I could **not** verify the current license
version from a primary source: `docs.comics.org` and `www.comics.org` HTML both return
Cloudflare `403 "Just a moment..."` from this sandbox, and search-result summaries
disagree between **CC BY 3.0** and **CC BY-SA 4.0**. The difference matters — ShareAlike
is a materially stronger obligation than plain Attribution — so this needs confirming
against the live site before implementation, not from search snippets.

Either way the practical requirement is the same shape: if Kapowarr displays GCD-derived
metadata, it should carry a GCD credit and a link back to the source page. `VolumeMetadata`
already has `site_url` and `CoverProvenance` (`definitions.py:774`) already records
provider/external-id/source-url per cover, so the data needed for correct attribution is
already in the model. What is missing is the UI decision about where the credit appears —
that is a product call, and it belongs to whoever implements, with Silas deciding the
placement.

This is not a gate on the evaluation, and it is not a reason to defer. It is a line item
in the implementation task.

## Recommendation

**Approve GCD, and close t-059 as evaluated.** This is the same verdict shape as t-042
(approve the architecture, sequence the work) rather than t-043 (decline). The
difference from t-043 is that nothing here is structural: GCD's coverage is real,
its API fits the contract, and the one thing that does not fit is our own code, which
we control.

Two follow-on tasks, in dependency order:

1. **Generalize the metadata search fan-out** — add `is_configured()` to
   `MetadataProvider`, make `search_metadata_with_fallback()` iterate configured
   registered providers instead of hardcoding ComicVine + Metron, and make the
   registry's lazy imports table-driven. Deletes `_metron_is_configured()` and its four
   call sites. `stakes: reversible`. Behaviour-preserving with Metron alone configured,
   which is exactly what the existing tests in `tests/Tbackend/metadata_providers.py`
   assert (`test_configured_metron_results_join_comicvine_results`,
   `test_metron_works_without_a_comicvine_key`), so those tests are the regression net.

2. **Implement the GCD metadata provider** — `depends_on` the above. Against the REST
   API, not the dump. The five things this document says to get right, because each is
   a measured trap rather than a guess:
   - cap search pagination explicitly; do **not** reuse Metron's unbounded `_all()`
     for `/series/name/` (a 1-char query is 3,571 pages);
   - send `Accept: application/json` or `?format=json`, or DRF serves HTML at 200;
   - guard JSON parsing — bad paths return Apache HTML 404, not a JSON error;
   - normalize dates: `on_sale_date or normalize(key_date) or None`, rejecting
     `-00-` placeholder components;
   - `volume_number` defaults to `1`; do not silently adopt year-as-volume.

   Plus: fetch the publisher name in `fetch_volume` only (never per search hit) with a
   small id→name cache, and settle the license/attribution question above with Silas
   before shipping user-visible GCD credits.

The third finding t-043 recorded — a `DownloadState` member for "handed off, waiting
in a remote queue" — is unaffected by this evaluation and stays where it is, noted on
t-060.

## What I verified, and what I did not

**Verified by live measurement against `https://www.comics.org/api/` from this sandbox
(2026-08-20, anonymous, no account):** that the API is reachable and returns JSON; the
full endpoint list and the `Series`/`IssueOnly`/`SeriesOverviewItem` field sets, from
the OpenAPI schema at `/api/schema/`; the Tintin country/language distribution (145
series, 20 Franco-Belgian vs 3 US on page 1); `Astérix` = 188 and `Tex` = 389 series;
that `/api/series/{id}/overview/` returns per-issue `number`/`key_date`/`on_sale_date`/
`cover_url`/`longest_story`; that `active_issues` and `issue_descriptors` are
positionally aligned (issue 566399 ↔ `"368 - King Ottokar's Sceptre"`, confirmed by
fetching the issue and reading `number: "368"`); that `page_size` and `limit` are
ignored and page size is fixed at 50; that `/api/series/name/a/` returns 178,526
results; that `%2F` in a series name yields an Apache HTML 404; that 20 sequential
overview pages (973 issues) completed in 11.5s with no `429`; that an issue record
carries a real `cover` image URL; that `publisher` is returned as a URL requiring a
second request.

**Verified by reading this fork at `36d90f7`:** that `search_metadata_with_fallback()`
hardcodes two providers and imports `MetronError` by name; that `_metron_is_configured()`
reads settings directly and is called at four sites; that `MetadataProvider` has no
`is_configured()`; that `MetadataProviderRegistry.get()`/`capabilities()` lazily import
`comicvine`/`metron` by name; that `Volume.add`, the refresh path, the POST
`/api/volumes` route and `MetadataIdentityStore` are provider-generic; the exact
`VolumeMetadata`/`IssueMetadata` field lists; that Metron avoids per-issue detail
requests by design and falls back to the first issue's image for a missing series
cover; the `metron_*` settings fields and their three repetitions.

**Verified against primary external sources:** the GCD API wiki's own "URLs are stable,
fields and data format should not be considered stable" and "anonymous access will
likely bye turned off at some point" caveats, and that auth is Basic/Session
(`GrandComicsDatabase/gcd-django` wiki, `API.md`); that `gcd_talker` requires a manually
downloaded SQLite dump, builds its own FTS5 index and secondary index, and scrapes
`comics.org/issue/<id>/cover/4` with BeautifulSoup while checking for
`id="challenge-error-title"` because **"GCD does not make their image URLs available via
their DB dumps"** (`comictagger/gcd_talker` README and `gcd_talker/gcd.py`); GCD's
March 2025 scale figures and "over a hundred languages" (Wikipedia).

**Reproduced directly:** `docs.comics.org` and `www.comics.org` HTML return Cloudflare
`403 "Just a moment... Enable JavaScript and cookies to continue"` from this sandbox,
across plain curl and full browser-header curl. `/api/` paths under the same host are
**not** challenged. Per `EGRESS-BLOCKERS.md`'s own definition — a real HTTP response
means *reachable*, only connection-level failure means *blocked* — this is not an
egress block and deliberately gets no ledger entry. It is a bot challenge on the HTML
site only, and it is the direct cause of gcd_talker's cover-scraping unreliability.

**Not verified — stated as judgment, not measurement:**

- **The current license version.** CC BY 3.0 vs CC BY-SA 4.0, unresolved; the primary
  source is behind the Cloudflare challenge above. Flagged in the implementation task.
- **The authenticated rate limit, and the anonymous one's actual numbers.** I have no
  GCD account. 20 requests in 11.5s drew no `429`; that is the whole of the evidence.
  The wiki says anonymous access will likely be withdrawn eventually, which is a real
  medium-term risk to a purely-anonymous implementation and the reason the dump stays
  documented as a fallback.
- **Dump size (~6 GB) and bi-weekly cadence.** From search-result summaries of the GCD
  Data Distribution page, not read directly — same Cloudflare block. The dump is not
  the recommended path, so this does not carry weight in the verdict.
- **How well GCD series titles match filenames in practice.** `extract_filename_data()`
  and the existing matching layer were not exercised against non-English titles. This
  is the most likely place the implementation finds an unpleasant surprise, and it is
  the right thing for the implementation task to test first rather than for this
  document to guess at.
- **Whether GCD's "series" granularity always matches Kapowarr's "volume."** GCD
  indexes magazines, albums and one-shots under the same `series` model, with
  `publishing_format` as free text (`"series"`, `"Limited series"`, ...). Franco-Belgian
  albums in particular are one-book-per-"series" far more often than US comics are.
  That is probably fine — Kapowarr already handles one-shots — but it was not tested.
