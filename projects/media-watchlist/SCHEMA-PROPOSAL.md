# SCHEMA-PROPOSAL.md — media-watchlist

Proposed import schema for `projects/media-watchlist/media_list.md`.

Generated: 2026-06-30
Source file: `projects/media-watchlist/media_list.md`

---

## 1. Observed format patterns

The file contains two years of data (2025, 2026) across seven media types. Formats differ slightly between years and across types.

### Sections and headers

```
MEDIA <YEAR>
<TYPE>:
<TYPE> (<count>):    ← 2025 sections include total count in header
```

### Entry patterns by type

| Type | 2026 pattern | 2025 pattern | Notes |
|---|---|---|---|
| MOVIE | `[*]Title m/dd` | `[*]Title m/dd` | Same both years |
| TV | `[*]Title sNN m/dd` | `[*]Title sNN m/dd` | Season always present; date may be `?` |
| BOOK | `Title - Author (pages) m/dd` | `Title m/dd (pages)` | Field order swapped between years |
| NOVELLA | `Title - Author (pages) m/dd` | `Title m/dd (pages)` | Same swap |
| AUDIOBOOK | `[*]Title - Author (Nhrs) m/dd` | `Title (Nhrs) m/dd` | Author optional; duration before date |
| COMIC | `[*]Title (N)` | — | No dates in 2026; no 2025 comics section |
| VIDEO GAME | `[*]Title [m/dd]` | `Title m/dd` | Date is optional in 2026 |

---

## 2. Edge cases and parse decisions

| Edge case | Example | Parse decision |
|---|---|---|
| Asterisk prefix | `*Predator Badlands 1/9` | Strip asterisk; set `starred = true` |
| Unknown day | `Remarkably Bright Creatures 5/x` | `watchedMonth = 5`, `watchedDay = null`, `dateRaw = "5/x"` |
| Typo double-slash | `*Faces of Death 5//19` | Normalize to `5/19`; set `watchedMonth = 5`, `watchedDay = 19` |
| Unknown date | `Euphoria s01 ?` | `watchedMonth = null`, `watchedDay = null`, `dateRaw = "?"` |
| No date (comics) | `Absolute Batman(1)` | All date fields `null`; `dateRaw = null` |
| No date (games) | `*Esoteric Ebb` | Same as comics |
| Duration format variation | `14hrs`, `11hrs`, `14h`, `(15th s)` | Normalize to float hours: `14.0`, `11.0`, `14.0`. `"(15th s)"` = `15.0` (Expeditionary Force entry — "15th" is a series index, not duration; treat as parse warning) |
| Possible re-watch | `Good Luck Have Fun Dont Die` appears twice in 2026 movies | Import both entries — each watch is a separate record |
| Multi-season same show | `Sherlock s01 4/16`, `Sherlock s02 4/18`, etc. | Each season = separate record (same title, different `season`) |
| Section count header | `MOVIES (139)` | Parse count as metadata; use as a post-import validation check, not a schema field |
| Author in parenthetical position | Some 2025 novellas lack author; audiobooks sometimes omit author | `author` is nullable; attempt author parse only when `—` separator is present |
| `From s02 6/10` vs `From s01 5/x` | Same show, two seasons, both with limited dates | Import both; `watchedDay = null` when day is `x` |

---

## 3. Inferred field list

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | Int | Yes | Auto-increment PK |
| `year` | Int | Yes | 2025 or 2026; inferred from section header |
| `mediaType` | MediaType enum | Yes | MOVIE, TV, BOOK, NOVELLA, AUDIOBOOK, COMIC, VIDEO_GAME |
| `title` | String | Yes | Cleaned title (no `*`, no `sNN` season token) |
| `starred` | Boolean | Yes | `true` if asterisk prefix; default `false` |
| `watchedMonth` | Int? | No | 1–12; null if unknown |
| `watchedDay` | Int? | No | 1–31; null if unknown or `x` |
| `dateRaw` | String? | No | Original date string verbatim: `"1/6"`, `"5/x"`, `"?"`, null |
| `season` | Int? | No | TV only; from `sNN` token; null for other types |
| `author` | String? | No | Books, novellas, some audiobooks; from `Title - Author` pattern |
| `pageCount` | Int? | No | Books and novellas; from `(N)` where N > 20 and not obviously hours |
| `durationHours` | Float? | No | Audiobooks; from `(Nhrs)` or `(Nh)` |
| `issueCount` | Int? | No | Comics; from `(N)` |
| `notes` | String? | No | Parse warnings, ambiguous tokens, or anything that doesn't fit cleanly |

---

## 4. Recommended Prisma schema block

```prisma
enum MediaType {
  MOVIE
  TV
  BOOK
  NOVELLA
  AUDIOBOOK
  COMIC
  VIDEO_GAME
}

model MediaEntry {
  id           Int       @id @default(autoincrement())
  createdAt    DateTime  @default(now())
  updatedAt    DateTime? @default(now()) @updatedAt

  year         Int
  mediaType    MediaType
  title        String    @db.VarChar(512)
  starred      Boolean   @default(false)

  watchedMonth Int?
  watchedDay   Int?
  dateRaw      String?   @db.VarChar(32)

  season       Int?      // TV only
  author       String?   @db.VarChar(256)
  pageCount    Int?      // BOOK / NOVELLA
  durationHours Float?   // AUDIOBOOK
  issueCount   Int?      // COMIC

  notes        String?   @db.Text

  @@index([year, mediaType])
  @@index([starred])
  @@index([title])
}
```

---

## 5. Validation checks (post-import)

- **Count header check:** 2025 MOVIES header says `(139)`. After import, `COUNT(*) WHERE year=2025 AND mediaType=MOVIE` should equal 139. Discrepancy indicates a missed entry.
- **TV season integrity:** every TV entry should have a non-null `season`. Flag any TV rows where `season IS NULL`.
- **Book/novella page count:** most book/novella entries have a page count. Flag entries where `pageCount IS NULL AND mediaType IN (BOOK, NOVELLA)` — these may be parse misses.
- **Audio duration:** all audiobook entries should have `durationHours IS NOT NULL`. One ambiguous entry (`Expeditionary Force 1 (16th s)`) needs manual review.
- **Duplicate titles per year:** select `title, year, season, COUNT(*)` — counts > 1 are either re-watches (expected) or parse errors (check).

---

## 6. Recommended next steps

1. Silas confirms: does asterisk mean "recommended" or something else?
2. Confirm whether `Expeditionary Force 1 (16th s)` should be `durationHours = 15.0` or is a series label.
3. If re-watches should be distinguished from first watches, add a `rewatch: Boolean` field.
4. If ratings/review data is planned, add `rating Int?` and `review String?` now before the first import.
5. Implement `scripts/import_media.py` (next task) to do the parse and populate the DB.
