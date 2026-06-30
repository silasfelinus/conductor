# Media Watchlist — Parser Normalization Rules

Generated: 2026-06-30
Task: media-watchlist/t-002
Depends on: SCHEMA-PROPOSAL.md (t-001)

---

## Purpose

Define how raw entries in `media_list.md` normalize into the MediaEntry schema fields: mediaType, title, creator, year, consumedDate, rating/starred, and externalIds. Includes ambiguous-entry handling and regex patterns.

---

## 1. Entry Structure (by Media Type)

### MOVIE
```
Pattern 2025+:  [*]Title m/dd
                [*]Title mm/dd
Examples:       *Predator Badlands 1/9
                Good Luck Have Fun Dont Die 3/21
```

| Token | Field | Rule |
|---|---|---|
| Leading `*` | `starred = true` | Strip; else `starred = false` |
| Rest before `m/dd` | `title` | Everything before the last space-prefixed date token |
| `m/dd` | `watchedMonth`, `watchedDay` | Split on `/`; both int; month 1–12 |
| `m/x` or `m/?` | `watchedMonth`, `watchedDay = null` | Date is known-month, unknown-day |
| No date | `watchedMonth = null` | Title takes the rest |

---

### TV
```
Pattern:  [*]Title sNN m/dd
          [*]Title sNN m/?
          [*]Title sNN ?
Examples: *The Bear s03 1/23
          Euphoria s01 ?
          From s02 6/10
```

| Token | Field | Rule |
|---|---|---|
| `sNN` / `sN` | `season` | Strip `s` prefix; int |
| `[*]Title` | `title` | Everything before `sNN` token |
| `m/dd` | `watchedMonth`, `watchedDay` | Same as MOVIE |
| `?` | All date fields null | Set `dateRaw = "?"` |

Season token detection: regex `\bs(\d{1,2})\b` — must be a standalone token, not part of the title.

---

### BOOK and NOVELLA
```
2026 pattern:  Title - Author (pages) m/dd
2025 pattern:  Title m/dd (pages)
               Title m/dd
Examples:      Remarkably Bright Creatures - Shelby Van Pelt (359) 5/x
               Demon Copperhead 2/14 (549)     ← 2025
```

| Token | Field | Rule |
|---|---|---|
| ` - ` separator | Split into title / author | Only when ` - ` is present and not inside parens |
| `(N)` where N > 20 | `pageCount` | Distinguish from issueCount (comics always small: 1–50) |
| `m/dd` | date fields | Same as MOVIE |
| 2025 vs 2026 | detect year context | If `(N)` appears after the date, still parse as pageCount |

Author parse: take everything between ` - ` and `(pages)` or date, trimmed.

---

### AUDIOBOOK
```
Pattern:  [*]Title - Author (Nhrs) m/dd
          [*]Title (Nhrs) m/dd        ← author sometimes omitted
Examples: *The House of the Cerulean Sea - TJ Klune (11hrs) 1/15
          Expeditionary Force 1 (15th s) ?   ← ambiguous duration
```

| Token | Field | Rule |
|---|---|---|
| `(Nhrs)` or `(Nh)` | `durationHours` | Strip `hrs`/`h`; float |
| `(Nth s)` | `notes = "ambiguous: Nth in series, not duration"` | Flag for manual review |
| ` - Author ` | `author` | Optional; same as BOOK |
| No ` - ` | `author = null` | Title is everything before `(duration)` |

Duration normalization: `14hrs → 14.0`, `11h → 11.0`, `6.5hrs → 6.5`.

---

### COMIC
```
Pattern:  [*]Title(N)
          [*]Title (N)
Examples: *Absolute Batman(1)
          Ordinary Gods (1)
          *Dept. H (1-6)
```

| Token | Field | Rule |
|---|---|---|
| `(N)` | `issueCount = 1` (single issue) | The N is the issue number, not a count |
| `(N-M)` | `issueCount = M - N + 1` | A run of issues |
| No date | All date fields null | Comics section has no dates |

Disambiguation from BOOK pageCount: comics always appear in the COMIC section; pageCount is never set for comics.

---

### VIDEO GAME
```
Pattern:  [*]Title [m/dd]
          [*]Title              ← date optional
Examples: *Balatro 1/6
          *Esoteric Ebb         ← no date
```

| Token | Field | Rule |
|---|---|---|
| Trailing `m/dd` | date fields | Same as MOVIE |
| No trailing date | All date fields null | Game completed/played, unknown date |

---

## 2. Ambiguous Entry Handling

| Situation | Detection | Resolution |
|---|---|---|
| Double-slash typo `5//19` | `//` in date token | Normalize to `5/19`; set `dateRaw = "5//19"` for audit trail |
| `(15th s)` duration | `\d+(th\|st\|nd\|rd) s` | Set `notes = "ambiguous: series ordinal not duration"`, `durationHours = null` |
| Title ends with `- Author` but no page count | No `(N)` after separator | Set `author`, `pageCount = null` |
| Re-watch (same title appears twice in same year) | Exact `(title, year, season)` duplicate | Import both; each is a separate MediaEntry |
| Unknown author in audiobook | No ` - ` separator | `author = null`; title includes everything before the duration |
| Section count header `MOVIES (139)` | Line matches `^\s*[A-Z]+\s+\(\d+\)` | Skip; use count as post-import validation target, not an entry |

---

## 3. Field Priority Rules

When multiple signals conflict:

1. **Star**: `*` at line start always means `starred = true`; no star means `starred = false` (never inherit from context)
2. **Season**: `sNN` token is definitive — always the season number, never part of the title
3. **Duration vs page count**: If the section is AUDIOBOOK, treat `(N)` as duration; if BOOK/NOVELLA, as page count; if ambiguous section (shouldn't happen), use `notes` to flag
4. **Date position**: 2025 entries may have date before page count in parens; 2026 entries have date after. If both `(N)` and date exist, assign by position: whichever comes last is the date
5. **Author**: only parse from ` - ` separator; never guess from title content

---

## 4. Regex Patterns (Reference)

```python
import re

DATE_PATTERN = re.compile(r'\b(\d{1,2})/(x|\?|\d{1,2})\b')
SEASON_PATTERN = re.compile(r'\bs(\d{1,2})\b', re.IGNORECASE)
PAGES_PATTERN = re.compile(r'\((\d{2,4})\)')       # > 20 = pages; ≤ 50 = issue count
DURATION_PATTERN = re.compile(r'\((\d+\.?\d*)\s*(?:hrs?)\)', re.IGNORECASE)
AMBIG_DURATION = re.compile(r'\((\d+)(th|st|nd|rd)\s+s\)', re.IGNORECASE)
SECTION_HEADER = re.compile(r'^\s*[A-Z ]+\s*(?:\(\d+\))?\s*:', re.MULTILINE)
DOUBLE_SLASH = re.compile(r'(\d{1,2})//(\d{1,2})')
AUTHOR_SPLIT = re.compile(r'\s+-\s+(?=[A-Z])')     # " - " before a capitalized author name
STAR_PREFIX = re.compile(r'^\*+')
ISSUE_COUNT = re.compile(r'\((\d+)(?:-(\d+))?\)')  # comics: (1) or (1-6)
```

---

## 5. Output Record Fields (Summary)

| Field | Source | Notes |
|---|---|---|
| `year` | Section header (`MEDIA 2026`) | Carry forward until next year header |
| `mediaType` | Sub-section header (`MOVIES:`) | Map to MediaType enum |
| `starred` | Leading `*` | Boolean |
| `title` | Remainder after stripping star, season, date, parens, author | Trim whitespace |
| `season` | `sNN` token (TV only) | Int |
| `author` | After ` - ` separator (books, audiobooks) | Nullable string |
| `watchedMonth` | From date token | 1–12 or null |
| `watchedDay` | From date token | 1–31 or null |
| `dateRaw` | Original date string verbatim | For audit trail |
| `pageCount` | `(N)` in book sections | N > 20 |
| `durationHours` | `(Nhrs)` in audiobook sections | Float |
| `issueCount` | `(N)` or `(N-M)` in comic sections | Int |
| `notes` | Ambiguities, parse warnings | Nullable text |

This document feeds into media-watchlist/t-002 implementation of `scripts/import_media.py`.
