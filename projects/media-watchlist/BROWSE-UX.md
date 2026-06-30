# Media Watchlist — Browse and Stats UX Plan

Generated: 2026-06-30
Task: media-watchlist/t-003

---

## Product Goal

A personal media log browser for Silas. Private by default; no social features at MVP. The priorities are:
1. Fast find (search, filter, sort)
2. Stats at a glance (yearly totals, genre/type breakdowns)
3. Review editing that stays private until explicitly approved for publishing
4. Graceful handling of partial/unknown data (no dates, no authors, etc.)

---

## Views

### 1. Home / Summary Dashboard

- **Stats bar** at top:
  - This year: N movies, N books, N TV shows, N games, N podcasts (abbreviated pills)
  - Starred items this year: N ⭐
  - Most active month: "You consumed the most in [Month]: N entries"
- **Recent entries** (last 10, reverse-chronological; grouped by media type icon)
- **Quick filter chips**: Movies | Books | TV | Games | Audiobooks | Comics | All
- **Search bar**: full-text across title and author

---

### 2. Browse / List View

**Default**: all entries, current year, sorted by watchedMonth desc + watchedDay desc (most recent first). Unknowns (`dateRaw = null`) sorted to bottom.

**Filters (sidebar or drawer):**
- **Year**: pill selector for all available years (2025, 2026, ...)
- **Media type**: checkbox multi-select (MOVIE, TV, BOOK, NOVELLA, AUDIOBOOK, COMIC, VIDEO_GAME)
- **Starred only**: toggle
- **Month**: Jan–Dec selector (multi-select)
- **Season**: TV only; number range or "any"

**Sort options** (dropdown):
- Date consumed (newest first) — default
- Date consumed (oldest first)
- Title A→Z
- Title Z→A
- Starred first

**Entry card** (compact):
```
[★] Title                       Jan 9
    Movie • 2026
```

- Tap/click → detail view

**Pagination**: 50 entries per page; infinite scroll on mobile.

---

### 3. Entry Detail View

Displayed in a right-side panel or full-page on mobile.

```
★ Predator Badlands                    MOVIE
──────────────────────────────────────────────
Consumed: January 9, 2026
Year: 2026
Starred: Yes

[Review section — private until published]
  [+ Add review]  ← if no review exists
  or
  [Review text, truncated to 5 lines]  [Edit]  [Publish]

[Related entries — same title, other years or formats]
  None

[External links — when available]
  Letterboxd  (if linked)
  Comic Vine  (if linked)
```

---

### 4. Stats View

**Top-level stats (current year default; year switcher):**

| Stat | Display |
|---|---|
| Total entries | N items consumed |
| By media type | Horizontal bar chart (Movies: 47, Books: 23, TV: 31, ...) |
| By month | Sparkline bar chart (Jan–Dec) |
| Starred items | N starred; list of top 5 starred titles |
| Audiobook hours | N hours listened |
| Pages read | N pages (books + novellas) |
| Comics read | N issues |
| TV seasons | N seasons across N shows |
| Games played | N games (+ starred count) |

**Year-over-year comparison** (when 2+ years available):
- Side-by-side totals for each media type
- "Most watched month" comparison

**Export button** (CSV): downloads a filtered view as CSV. Private data; no public sharing at MVP.

---

### 5. Review Editor

Reviews are private by default. A review is a freeform text note attached to a MediaEntry.

**Create/edit flow:**
1. Open Entry Detail → "Add review" or "Edit review"
2. Markdown text editor (basic: bold, italic, bullets, no images)
3. Character limit: 4000 (long-form is fine)
4. Auto-save as draft
5. "Publish" button → sets `reviewPublic = true` (stored in DB; future UI can expose this)

**MVP rule:** The publish action only sets the flag; it does not push to any external service. Publishing is Silas-only and needs explicit future approval before review export is wired up.

---

## Schema Additions

These fields are not in SCHEMA-PROPOSAL.md and should be added to the MediaEntry model:

```
MediaEntry {
  ...existing fields...
  review       String?   @db.Text
  reviewPublic Boolean   @default(false)
  rating       Int?      // 1–10 scale; nullable (not all entries rated)
  rewatch      Boolean   @default(false)   // true = second+ viewing
  externalId   String?   @db.VarChar(128)  // e.g. Letterboxd film slug
  externalUrl  String?   @db.VarChar(512)  // e.g. letterboxd.com/film/...
}
```

`rating` and `externalId` are set during enrichment (t-004); `review` and `reviewPublic` are set via the UI.

---

## Empty States

| Situation | Display |
|---|---|
| No entries match filter | "No entries found. Try adjusting your filters." |
| No entries at all | "Your media log is empty. Import your media_list.md to get started." |
| No review | "+ Add a review" link |
| No date on entry | "Date unknown" badge (muted) |
| No author on book | Author field omitted from card (not shown as "Unknown") |

---

## What's Out of Scope at MVP

- Social sharing of reviews
- Following other users' watchlists
- Recommendations engine
- Real-time notifications
- Bulk edit
- Image covers (Letterboxd/OpenLibrary poster art — deferred to enrichment milestone)

This document feeds into media-watchlist implementation after t-002 and t-004 are complete.
