# Media Watchlist — Log Format vs. Letterboxd/Goodreads Comparison

Generated: 2026-06-30
Task: media-watchlist/t-005

---

## Purpose

Compare Silas's hand-written log format (media_list.md) against Letterboxd CSV and Goodreads CSV export shapes. Identifies where the formats align (auto-import) vs. where they diverge (manual mapping or one-time conversion pass). Informs the importer normalization rules in t-002.

---

## Silas's Log Format (Baseline)

From SCHEMA-PROPOSAL.md:
```
MOVIES:
*Predator Badlands 1/9
Good Luck Have Fun Dont Die 3/21

BOOKS:
Remarkably Bright Creatures - Shelby Van Pelt (359) 5/x

TV:
*The Bear s03 1/23
Euphoria s01 ?

AUDIOBOOKS:
*The House of the Cerulean Sea - TJ Klune (11hrs) 1/15

COMICS:
*Absolute Batman(1)
```

**Fields available in hand log:**
- `mediaType` (from section header)
- `title`
- `starred` (asterisk)
- `season` (TV)
- `watchedMonth`, `watchedDay` (often partial)
- `author` (books, audiobooks — when present)
- `pageCount` (books, novellas)
- `durationHours` (audiobooks)
- `issueCount` (comics)

**Fields NOT in hand log:**
- Rating/score
- Review text
- External IDs (Letterboxd, Goodreads, IMDb)
- Release year (only log year known)
- Publisher (comics)
- Genre
- Language

---

## Letterboxd CSV Export

```csv
Date,Name,Year,Letterboxd URI,Rating,Rewatch,Tags,Watched Date
2026-01-09,Predator: Badlands,2026,https://letterboxd.com/film/predator-badlands/,,,,2026-01-09
2025-03-21,Good Luck Have Fun Dont Die,2025,https://letterboxd.com/film/good-luck-...,,,,"2025-03-21"
```

### Field-by-field comparison

| Field | Letterboxd | Silas log | Match? | Notes |
|---|---|---|---|---|
| Title | `Name` (string) | Direct | ~90% | Letterboxd uses full punctuated titles ("Predator: Badlands"); Silas log may abbreviate or alter |
| Date | `Watched Date` (YYYY-MM-DD) | `m/dd` | ✓ Convert | Letterboxd has full ISO date; log has month/day only |
| Year | `Year` (int) | inferred from log year | Partial | Letterboxd year = film release year, not watched year |
| Rating | `Rating` (0.5–5.0 in 0.5 steps) | Not in log | ✗ | Letterboxd adds ratings; log has none |
| Rewatch | `Rewatch` (Y/N) | Not in log | ✗ | Letterboxd tracks rewatches explicitly |
| External URI | `Letterboxd URI` | Not in log | ✗ | Import adds this to `externalUrl` |
| Tags | `Tags` (comma-separated) | Not in log | ✗ | Ignore at MVP |

### Alignment summary (Letterboxd)

| Scenario | What to do |
|---|---|
| Title matches exactly | Auto-link; set `externalUrl` on existing MediaEntry |
| Title differs slightly (punctuation, subtitle) | Fuzzy match (Levenshtein ≤ 3); flag for manual confirm |
| Letterboxd entry not in log | Import as new MediaEntry (`starred = false`, `rewatch = false`) |
| Log entry not in Letterboxd | Leave as-is; some films may not be on Letterboxd |
| Rating conflict (Letterboxd has rating, log doesn't) | Add Letterboxd rating to `rating` field |
| Watched date conflict | Letterboxd date is more precise (full ISO); prefer it over `m/dd` |

---

## Goodreads CSV Export

```csv
Book Id,Title,Author,Author l-f,Additional Authors,ISBN,ISBN13,My Rating,Average Rating,
Publisher,Binding,Number of Pages,Year Published,Original Publication Year,Date Read,Date Added,
Bookshelves,Bookshelves with positions,Exclusive Shelf,My Review,...
12345,Remarkably Bright Creatures,Shelby Van Pelt,"Van Pelt, Shelby",,,,4,,Ecco,
Hardcover,359,2022,2022,2025/05/xx,2025/04/01,read,...
```

### Field-by-field comparison

| Field | Goodreads | Silas log | Match? | Notes |
|---|---|---|---|---|
| Title | `Title` | Direct | ✓ (mostly) | May differ in subtitle or edition tag |
| Author | `Author` | Present in 2026 log | ✓ | Goodreads: "First Last"; log: "First Last" format as well |
| Page count | `Number of Pages` | `(pages)` in log | ✓ | Can fill in when log is missing |
| Date read | `Date Read` (YYYY/MM/xx format!) | `m/x` partial | ~Match | Goodreads uses `xx` for unknown day — same pattern as log's `5/x` |
| Rating | `My Rating` (0–5 stars) | Not in log | ✗ | Add to `rating` field ×2 for 1–10 scale |
| Review | `My Review` | Not in log | ✗ | Import to `review` field |
| Publisher | `Publisher` | Not in log | ✗ | Add to new `publisher` field |
| Shelf | `Exclusive Shelf` | "BOOK" section | Partial | "read" = consumed; ignore "to-read", "currently-reading" |

### Alignment summary (Goodreads)

| Scenario | What to do |
|---|---|
| `(title, author)` exact match | Auto-link; fill in missing pageCount, rating, review |
| Title match, author differs | Flag for manual review (could be different edition or same book different publisher) |
| Goodreads entry on "to-read" shelf | Skip — not consumed yet |
| Date read is `xx` for day | Set `watchedDay = null`; `dateRaw = "YYYY/MM/xx"` |
| Log entry not in Goodreads | Keep as-is; Silas may have more books than tracked on Goodreads |
| Goodreads has NOVELLA as "book" | Dedupe by title; if in Silas log as NOVELLA, keep log type |

---

## Key Divergences (for Import Script)

| Issue | Description | Resolution |
|---|---|---|
| Title punctuation | Letterboxd: "Predator: Badlands"; log: "Predator Badlands" | Normalize: strip colons, lowercase, trim for comparison |
| Subtitle presence | Log often omits subtitles ("Foundation" vs "Foundation: The Psychohistorians") | Fuzzy match; prefer log title in output |
| Release year vs. consumed year | Letterboxd `Year` = release; log `year` = watch year | Keep log's watch year; add `releaseYear` as separate field |
| Goodreads mediaType conflation | All books = "book" regardless of NOVELLA, AUDIOBOOK | Match by section in Silas log; let log type win |
| Rating scale | Letterboxd: 0.5–5; Goodreads: 0–5; log: none | Normalize to 1–10 (×2) on import |
| Review encoding | Goodreads reviews may contain HTML entities (`&amp;`, `&#39;`) | Strip HTML entities on import |
| Goodreads date format | `YYYY/MM/xx` where `xx` = unknown day | Map `xx` → `watchedDay = null` |

---

## Import Priority

1. **Hand log is authoritative**: when hand log and external service conflict on title or media type, trust the hand log
2. **External service fills gaps**: external services can add rating, review, publisher, externalUrl when log doesn't have them
3. **No destructive overwrites**: importing CSV never removes an existing field from MediaEntry; it only adds or updates null fields

---

## Recommended Schema Additions (from this comparison)

```prisma
MediaEntry {
  ...
  releaseYear   Int?      // film/book release year (from Letterboxd/Goodreads); distinct from log year
  publisher     String?   @db.VarChar(128)   // from Goodreads
}
```

These additions feed back into the final MediaEntry schema before the import script is built in t-002.
