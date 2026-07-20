# t-008 — Final MediaEntry schema + minimal browse API spec

Reconciles `SCHEMA-PROPOSAL.md` (2026-06-30, based on the 2025/2026 sample) and
`BROWSE-UX.md`'s schema additions against what `scripts/import_media.py` actually
produced from the real 2014-2026 log (`data/media-entries.json`, 2440 entries;
see `data/import-report.md`). Docs/spec only — no kind_robots code changes in
this task. Follow-on build task: media-watchlist/t-009.

---

## 1. What changed vs. the original proposal

| Field | SCHEMA-PROPOSAL.md (2026-06-30) | Real data (t-007, 2026-07-17) | Resolution |
|---|---|---|---|
| `MediaType` | 7 values (MOVIE, TV, BOOK, NOVELLA, AUDIOBOOK, COMIC, VIDEO_GAME) | 12 values — adds ANIME, PODCAST, THEATRE, SHORT, VIDEO_GAME_SHORT (log spans 2014-2026, not just the 2025/2026 sample) | Enum extended to 12 values (below) |
| `releaseYear` | Not in original 15-field list | Present in real data (`(2024)`, bare `Naked Gun 2025` in title) — 1 populated example (`Naked Gun`, 2025) in the current corpus | Add `Int?` |
| `issueRange` | Not in original list | Present for multi-issue comic runs (e.g. `Hellblazer 134-150 (17)`) | Add `String?` alongside `issueCount` |
| `rewatch` | BROWSE-UX.md proposed `Boolean` (`true` = second+ viewing) | Real importer emits an **Int** — `"x2"` in the source log parses to `rewatch: 2` (total watch count), not a flag. Only 1 of 2440 entries has a non-null value in the current corpus (`Parallel`, 2021, `rewatch: 2`) | **Correction: `rewatch` is `Int?`, not `Boolean`.** Null/absent means "no rewatch marker in source" — treat as a single (first) watch, not `0`. A future UI computing "is this a rewatch" should check `rewatch != null && rewatch > 1`, not truthiness of a boolean. |
| `sourceFile` | Not in original list | Present — `media_list.md` or `media_2021.md` (importer supports multi-file sources; future years drop in the same way) | Add `String?`, informational/audit only |
| `line`, `raw` | Not in original list | Present — `line` is the source line number, `raw` is the original unparsed text | **Not carried into the Prisma model as typed columns.** `raw` is folded into `notes` only when a parse note exists (see §2); `line` has no durable meaning once imported and is dropped. If exact source provenance is ever needed, re-derive from `sourceFile` + `title` + `dateRaw`, or keep `data/media-entries.json` as the import-of-record. |
| `review`, `reviewPublic`, `rating`, `externalId`, `externalUrl` | BROWSE-UX.md additions, not yet in any model | Not present in import data (expected — these are UI/enrichment-authored, not parsed from the log) | Carried into the final model unchanged, all nullable/defaulted; populated later by the review editor (t-003's UX) and enrichment tasks (t-004/t-005's INTEGRATIONS.md), not by the importer |

No other proposed fields changed shape. `watchedMonth`/`watchedDay`/`dateRaw`/`season`/`author`/`pageCount`/`durationHours`/`issueCount`/`starred`/`title`/`year`/`mediaType` all match the original proposal and the real data exactly.

---

## 2. Final Prisma schema block

```prisma
enum MediaType {
  MOVIE
  TV
  BOOK
  NOVELLA
  AUDIOBOOK
  COMIC
  VIDEO_GAME
  ANIME
  PODCAST
  THEATRE
  SHORT
  VIDEO_GAME_SHORT
}

model MediaEntry {
  id            Int        @id @default(autoincrement())
  createdAt     DateTime   @default(now())
  updatedAt     DateTime?  @default(now()) @updatedAt

  userId        Int?       @default(1)

  year          Int
  mediaType     MediaType
  title         String     @db.VarChar(512)
  starred       Boolean    @default(false)
  rewatch       Int?       // total watch count when the source marked a rewatch (e.g. "x2" -> 2); null = single/first watch, per source

  releaseYear   Int?
  watchedMonth  Int?
  watchedDay    Int?
  dateRaw       String?    @db.VarChar(32)

  season        Int?       // TV only
  author        String?    @db.VarChar(256)
  pageCount     Int?       // BOOK / NOVELLA
  durationHours Float?     // AUDIOBOOK
  issueCount    Int?       // COMIC
  issueRange    String?    @db.VarChar(64) // COMIC, e.g. "134-150"

  review        String?    @db.Text
  reviewPublic  Boolean    @default(false)
  rating        Int?       // 1-10, nullable
  externalId    String?    @db.VarChar(128) // e.g. Letterboxd film slug
  externalUrl   String?    @db.VarChar(512)

  notes         String?    @db.Text
  sourceFile    String?    @db.VarChar(128) // import provenance, e.g. "media_list.md"

  @@index([userId, year, mediaType])
  @@index([starred])
  @@index([title])
}
```

`userId` follows the existing `Todo` model's precedent (`userId Int? @default(1)`,
`prisma/schema.prisma`) — nullable with a default, so the log stays single-user
(Silas, id 1) for now without hard-coding it structurally. No `User` relation is
added yet; add `@relation` + FK enforcement only if/when this becomes multi-user.

---

## 3. Minimal browse API contract

Follows the house convention from `server/api/facets/index.get.ts` (filter/sort/paginate)
and `server/api/logs/index.get.ts` (`findMany` + `count` pair for totals), Prisma
singleton import (`import prisma from '~/server/utils/prisma'`), and the repo's
dominant `{ success, data }` response wrapper with `errorHandler(error)` in a
catch block.

### `GET /api/media-entries`

Query params (all optional):

| Param | Type | Behavior |
|---|---|---|
| `year` | int | Exact match. Omit for all years. |
| `mediaType` | comma-separated `MediaType` values | Validated against the enum array before use (same pattern as `facets/index.get.ts`'s `kind` param); invalid values ignored, not 400'd. |
| `starred` | `"true"` | Filters `starred: true` only. Absent = no filter (not `false`). |
| `month` | comma-separated ints 1-12 | Maps to `watchedMonth: { in: [...] }`. |
| `season` | int | TV only; exact match on `season`. |
| `search` | string | `title` and `author` `contains`, case-insensitive (`mode: 'insensitive'`), combined with `OR`. |
| `sort` | `date_desc` (default) \| `date_asc` \| `title_asc` \| `title_desc` \| `starred_first` | Maps to `orderBy`; `date_*` orders by `[{ watchedMonth }, { watchedDay }]` with nulls sorted last (unknowns to the bottom, per BROWSE-UX.md's browse-view default). |
| `take` | int | Page size, default 50 (matches BROWSE-UX.md's pagination spec), clamped like `facets/index.get.ts`'s `toPositiveInt` helper (max e.g. 200). |
| `skip` | int | Offset, default 0. |

Response:

```jsonc
{
  "success": true,
  "data": [ /* MediaEntry[] */ ],
  "count": 50,   // entries in this page
  "total": 2440  // entries matching filters, for pagination UI
}
```

Errors funnel through the shared `errorHandler(error)` (`server/utils/error.ts`),
same as every other route in the house style.

### `GET /api/media-entries/stats`

Aggregate counts for the Stats view (BROWSE-UX.md §4), following the
`groupBy` + reducer pattern in `server/api/art/queue/stats.get.ts`:

- `prisma.mediaEntry.groupBy({ by: ['mediaType'], where: { year }, _count: { _all: true } })` → counts by type for the "By media type" bar chart.
- `prisma.mediaEntry.groupBy({ by: ['watchedMonth'], where: { year }, _count: { _all: true } })` → month sparkline (nulls excluded).
- `prisma.mediaEntry.aggregate({ where: { year, mediaType: 'AUDIOBOOK' }, _sum: { durationHours: true } })` → audiobook hours.
- `prisma.mediaEntry.aggregate({ where: { year, mediaType: { in: ['BOOK','NOVELLA'] } }, _sum: { pageCount: true } })` → pages read.
- `prisma.mediaEntry.count({ where: { year, starred: true } })` → starred count.

Response shape mirrors the existing stats-route convention (`{ success, data }`
with a flat object of the computed fields) — exact field names are a UI-layer
decision for t-009, not fixed here.

---

## 4. One-time seed/import path

Not a live API endpoint — a one-time (re-runnable, idempotent) seed script,
analogous to how `scripts/import_media.py` itself is documented as
"regenerate any time; do not hand-edit" for the JSON intermediate.

1. New script (suggested: `kind_robots/prisma/seed-media-entries.ts` or a
   one-off `scripts/` entry, per whatever seed convention the repo already
   uses for one-time data loads — t-009 to confirm) reads
   `data/media-entries.json` (2440 entries, already validated by
   `data/import-report.md`) and bulk-inserts via
   `prisma.mediaEntry.createMany({ data: [...], skipDuplicates: true })`.
2. Field mapping JSON → Prisma: direct 1:1 for `year`, `mediaType`, `title`,
   `starred`, `releaseYear`, `season`, `author`, `watchedMonth`, `watchedDay`,
   `dateRaw`, `pageCount`, `durationHours`, `issueCount`, `issueRange`,
   `notes`, `sourceFile`. `rewatch` maps directly too now that the column is
   `Int?` (no boolean coercion needed — see §1 correction). `userId` defaults
   to `1` (Silas) for every row. `line` and `raw` are **not** imported as
   columns (see §1) — if a future need arises to inspect the original text,
   re-run `import_media.py` against the source `.md` files rather than
   storing the redundant raw string per row.
3. Idempotency: since this is a single historical backfill (not an ongoing
   sync), guard the script with a pre-check —
   `prisma.mediaEntry.count()` should be `0` before running, or require an
   explicit `--force` flag — to avoid accidental duplicate imports if it's
   run twice. `createMany`'s `skipDuplicates` alone isn't sufficient here
   since there's no unique constraint to dedupe on (two genuinely identical
   watches of the same title/date are valid, e.g. re-watches without an
   `x2` marker in the source).
4. Going forward (post-backfill), new entries are expected to be added
   through the app UI (t-009's write path, out of scope here) rather than by
   re-running the importer — the importer's job ends at this one-time
   migration of Silas's existing hand-kept log.

---

## 5. Open items carried forward to t-009 (not blocking this spec)

- Exact seed-script location/convention (kind_robots may already have a
  `prisma/seed.ts` pattern to extend rather than a new script).
- `rating` scale reconciliation with `FORMAT-COMPARISON.md`'s note that
  Letterboxd (0.5-5) and Goodreads (0-5) use different scales than this
  model's proposed 1-10 — deferred to whichever enrichment task (t-004/t-005)
  actually writes `rating` values.
- Whether `MediaEntry` needs a `Bot`/`Dream`/`Project` relation for
  consistency with other kind_robots content models, or stays a standalone
  table (current recommendation: standalone — this is a personal log, not
  bot-generated or Dream-linked content).
