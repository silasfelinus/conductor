# Media Watchlist — External Integrations Scope

Generated: 2026-06-30
Task: media-watchlist/t-004

---

## Integration Targets

| Service | Use case | Priority |
|---|---|---|
| Letterboxd | Movie import, movie export, diary sync | High |
| Goodreads | Book import | Medium |
| Comic Vine | Comic metadata enrichment | Medium |
| Tautulli | Plex watch-history backfill | Low (requires local server) |

---

## 1. Letterboxd

### What it provides
- Personal movie diary export (CSV)
- Film metadata API (unofficial/fan-built; Letterboxd has no official public REST API)
- Import: paste Letterboxd export CSV → map to MediaEntry rows

### Letterboxd CSV export format
```csv
Date,Name,Year,Letterboxd URI,Rating,Rewatch,Tags,Watched Date
2026-01-09,Predator: Badlands,2026,https://letterboxd.com/film/predator-badlands/,,,,"2026-01-09"
```

| Letterboxd field | MediaEntry field |
|---|---|
| `Watched Date` | `watchedMonth`, `watchedDay`, `dateRaw` |
| `Name` | `title` |
| `Year` | (confirm release year vs. log year) |
| `Letterboxd URI` | `externalUrl` |
| `Rating` | `rating` (Letterboxd uses 0.5–5 stars; map to 1–10 scale: ×2) |
| `Rewatch` | `rewatch` (boolean) |

**Import strategy:** One-time import of Letterboxd CSV; then deduplicate against existing MediaEntry rows by `(title, watchedMonth, watchedDay, year)`. Manual review for collisions.

**Gap vs. hand log:** Letterboxd tracks movies only; Silas's log includes all media. The CSV import fills in Letterboxd movies for any year Silas exported; hand log covers everything else.

**No live API access at MVP.** Letterboxd has no public REST API. Integration is CSV-only.

---

## 2. Goodreads

### What it provides
- Book/shelf export (CSV)
- No public REST API (was shut down in 2020)

### Goodreads export CSV format
```csv
Book Id,Title,Author,Author l-f,Additional Authors,ISBN,ISBN13,My Rating,Average Rating,Publisher,Binding,Number of Pages,Year Published,Original Publication Year,Date Read,Date Added,Bookshelves,Bookshelves with positions,Exclusive Shelf,My Review,Spoiler,Private Notes,Read Count,Recommended For,Recommended By,Owned Copies,Original Purchase Date,Original Purchase Location,Condition,Condition Description,BCID
12345,Remarkably Bright Creatures,...
```

| Goodreads field | MediaEntry field |
|---|---|
| `Title` | `title` |
| `Author` | `author` |
| `Number of Pages` | `pageCount` |
| `Date Read` | `watchedMonth`, `watchedDay` |
| `My Rating` | `rating` (Goodreads: 1–5; map to 1–10: ×2) |
| `My Review` | `review` |
| `Exclusive Shelf` | (skip; "read" shelf is the default) |

**Import strategy:** Same as Letterboxd — one-time CSV import with dedupe against MediaEntry by `(title, author, year, watchedMonth)`. Silas hand log may have partial data (no author) that the Goodreads import can fill in.

**Gap:** Goodreads doesn't track novellas or audiobooks separately — all are "books." Delineation requires human review or relying on Silas's original log type.

---

## 3. Comic Vine

### What it provides
- REST API with volume/issue metadata: series name, issue number, publisher, release date, description
- API key required (free)

### Use case
Enrich comic entries with publisher, release year, and volume metadata. Silas's log only has title and issue count; Comic Vine adds release year, publisher, writer, artist.

### API call
```
GET https://comicvine.gamespot.com/api/issues/?api_key=KEY&format=json
    &filter=volume:TITLE,issue_number:N
```

Returns: `{ id, name, issue_number, volume { name, publisher { name } }, cover_date, description }`

### Mapping
| Comic Vine field | MediaEntry field |
|---|---|
| `volume.name` | Match to `title` |
| `issue_number` | Match to entry |
| `cover_date` | `dateRaw` (release date, not consumed date) → `externalReleaseYear` (add to schema if needed) |
| `volume.publisher.name` | Not in current schema; add `publisher String?` |
| Comic Vine volume ID | `externalId = "cv:volume:ID"` |

**Rate limits:** Comic Vine limits to 200 API requests per hour (resource API). For a comic collection of ~50 entries, one enrichment pass runs well within limits.

**Privacy:** The API key is stored server-side; never exposed to the client.

---

## 4. Tautulli (Plex Watch History)

### What it provides
- Local server API exposing Plex watch history
- Backfill: pull Plex movie and TV watch history into MediaEntry

### Requirements
- Tautulli must be running on Silas's local network (not cloud-accessible by default)
- Requires an API key from Tautulli settings

### Use case
Plex history contains movie and TV watches that may not be in the hand log (watched passively without noting). Backfill would create MediaEntry rows for all Plex plays in a date range.

### API call (example)
```
GET http://localhost:8181/api/v2?apikey=KEY&cmd=get_history
    &start=0&length=1000&media_type=movie
```

Returns array of `{ full_title, year, watched_status, date, play_count, ... }`

**Constraint:** Tautulli is local-only; the import must run on Silas's local machine or a home server with Tautulli access. No remote integration without setting up a reverse proxy.

**MVP recommendation:** Defer Tautulli integration until Letterboxd and Goodreads are confirmed useful. A manual CSV export from Tautulli is a simpler starting point.

---

## Schema Additions Required for Enrichment

```
MediaEntry {
  ...existing fields...
  externalId   String?   @db.VarChar(128)  // e.g. "cv:volume:12345", "lb:film/predator"
  externalUrl  String?   @db.VarChar(512)
  publisher    String?   @db.VarChar(128)  // comics: publisher name from Comic Vine
}
```

These fields are set by the enrichment scripts, not by the initial import.

---

## Enrichment Run Plan

| Phase | Source | Method | When |
|---|---|---|---|
| Initial import | media_list.md | `scripts/import_media.py` | Once, after t-002 |
| Letterboxd backfill | Letterboxd CSV export | `scripts/enrich_letterboxd.py` | Manual; export from Letterboxd.com |
| Goodreads backfill | Goodreads CSV export | `scripts/enrich_goodreads.py` | Manual; export from Goodreads |
| Comic Vine enrichment | Comic Vine REST API | `scripts/enrich_comicvine.py` | One-time + on new comic import |
| Tautulli backfill | Tautulli API | `scripts/enrich_tautulli.py` | Deferred; local only |

All enrichment scripts are **dry-run by default** and must be invoked with `--commit` to write to the DB. Never auto-run.

---

## Summary

| Service | API type | Auth | MVP? |
|---|---|---|---|
| Letterboxd | CSV export only | None (your own export) | Yes |
| Goodreads | CSV export only | None (your own export) | Yes |
| Comic Vine | REST API | Free API key | Yes (enrichment) |
| Tautulli | Local REST API | Local API key | Deferred |
