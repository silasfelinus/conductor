# Kind Word Puzzles — spec

date: 2026-10-02 · task: kind-word-puzzles/t-003 · survey of silasfelinus/kind_robots (read-only, no code changes)

This spec fixes the three open decisions in DESIGN-BRIEF.md: where words come from, what the two puzzle formats are, and how a date picks a puzzle. It is the contract for t-004 (generator/validator), t-005 (first 14 puzzles) and t-006 (page).

## 1. Lexicon source

**What exists.** The entity tables in `prisma/schema.prisma` carry the names and prose we need:

| Table | Fields worth mining | Gate |
|---|---|---|
| `Character` | `name`, `species`, `class`, `genre`, `quirks` | `isPublic = true` |
| `Reward` | `name`, `collection`, `rewardType`, `flavorText`, `description` | `isPublic`, `isActive`, `isMature = false` |
| `Scenario` | `title`, `locations` (the "places"), `genres`, `description` | `isMature = false` |
| `Bot` | `name`, `theme`, `tagline` | `isPublic = true` |

Public read endpoints exist under `server/api/{characters,rewards,scenarios,bots}`. No database is reachable from an agent sandbox, so **the lexicon cannot be built live by a session**.

**Decision: a committed, static lexicon.**

1. A one-off export script (`utils/scripts/exportWordPuzzleLexicon.ts`, t-004) reads the public API (or a DB dump handed over by Silas) and writes `public/data/word-puzzles/lexicon.json`. The script is deterministic and sorted so diffs are reviewable.
2. Until an export exists, sessions author `lexicon.json` by hand from knowledge of the public gallery plus a seed list of Kind Robots vocabulary; every entry carries a `source` tag (`character | reward | place | scenario | bot | seed`) so a later export can replace seeds without touching puzzles.
3. After export, **nothing at runtime touches the database or any LLM**. The page reads static JSON only.

**Entry shape**

```json
{ "word": "LANTERN", "display": "Lantern", "source": "reward", "theme": "light", "clue": "Carried to find the way after dark." }
```

**Normalisation (`normalizeWord`)**: Unicode NFD, strip combining marks, uppercase, keep only `A–Z`; reject if the result differs in length from the letters-only display form by more than spaces/hyphens/apostrophes (so "Ms. Mu" becomes `MSMU`, but "Ångström & Co" is rejected for ambiguity). Length limits: word search 4–10 letters, crossword 3–5 letters.

**All-ages filter**: exclude `isMature`, anything private, and any word on `blocklist.json` (profanity, slurs, sexual and violence terms, plus a substring list used for filler checks, see 3.3). The blocklist is a committed file, reviewed once, and the validator enforces it on both listed words and the filler letters around them.

**Size and themes**: aim for 600+ distinct words in about 30 themes (matching the ~30 header illustrations in the art plan): e.g. Light, Garden, Ocean, Robots, Weather, Music, Kitchen, Space. A theme needs at least 24 words (word search uses 8–12; crossword draws 6–8 answers). Words may belong to one theme only; a word cannot be reused within 30 days of its last appearance (checked by the manifest validator, see 3.4).

## 2. Puzzle formats

Both formats are generated offline, validated, and committed as static JSON. The player never generates anything.

### 2.1 Word search

- Grid **10×10** (Mon–Fri), **12×12** (Sat–Sun).
- **8 words** weekdays, **12** weekends, all from one theme, 4–10 letters, no word contained in another.
- Directions: weekdays use right, down, down-right (easy); Saturday adds left and up; Sunday uses all eight. Weekday = the puzzle's calendar weekday in the schedule (3.1), not the player's.
- Filler letters come from a seeded PRNG weighted by English letter frequency, then **rejection-checked** (3.3).
- Interaction contract for t-006: drag or tap-tap start/end cell along a line, snap to the nearest of the 8 directions; keyboard: arrow keys move the cursor, Space/Enter marks start then end. Found words strike through in the list and stay highlighted.

### 2.2 Mini crossword

- Grid **5×5** with up to 6 black squares, rotationally symmetric. Every white square is checked (belongs to both an across and a down entry) except at most 2.
- Entries are 3–5 letters and each has **one hand-written clue**: kind, concrete, all-ages, ≤ 60 characters, no "see 3-Down", never contains the answer or its stem.
- Answers come from the lexicon; at most **half** of the answers may be from the puzzle theme's own source tag (so the grid is not all characters).
- Interaction contract for t-006: tap a cell to select, tap again to flip direction, built-in on-screen keyboard at 375px, arrow keys and letters on desktop, Backspace clears. A "check" button marks wrong cells; no reveal penalty, no timer.

### 2.3 Puzzle JSON (`public/data/word-puzzles/puzzles/<id>.json`)

```json
{
  "id": "ws-0001",
  "format": "wordsearch",
  "theme": "light",
  "title": "After Dark",
  "size": 10,
  "words": [{ "word": "LANTERN", "row": 2, "col": 0, "dir": "E" }],
  "grid": ["LANTERNXQZ", "..."],
  "seed": 1,
  "validatedAt": "2026-10-02",
  "validator": 1
}
```

Crossword puzzles use `grid` rows of letters with `#` for black squares, plus `across` / `down` arrays of `{ number, row, col, answer, clue }`. IDs are `ws-NNNN` and `cw-NNNN`, zero padded, never reused or renumbered.

## 3. Daily selection

### 3.1 Date → puzzle

- **Schedule file** `public/data/word-puzzles/schedule.json`: `{ "epoch": "2026-10-02", "order": ["ws-0001", "cw-0001", ...] }`, where `order` is the committed play order for a year (365 entries minimum, alternating `ws`/`cw`; leave one `cw` out of every 14 for a themed "bonus" slot at the author's discretion).
- **Pure function** `puzzleIdForDate(isoDate, schedule)`: `index = daysBetween(epoch, isoDate) mod order.length`, with `daysBetween` computed on UTC date integers parsed from `YYYY-MM-DD`, so DST never shifts a day.
- **Which date**: the player's **local calendar date** (formatted `YYYY-MM-DD` from `Date` local fields). A player in Tokyo and one in Honolulu see different puzzles at the same instant; that is intended, a daily puzzle should flip at the player's midnight. Dates before the epoch fall back to index 0 and are not shown in the archive.
- **No randomness at runtime.** The schedule is the whole story, which makes the puzzle for any date testable and reproducible.
- After 365 days the order simply repeats (modulo); authors extend `order` in place and the epoch never moves.

### 3.2 Archive

The page lists every date from the epoch to today (never the future), each linking `?date=YYYY-MM-DD`. Future dates are refused in the pure function so a player cannot read ahead by editing the URL.

### 3.3 Validator (t-004 `utils/wordPuzzleValidator.ts`)

A puzzle passes only if all of these hold, each as a named, tested check:

1. **Words placed correctly**: every listed word is read from the grid along its stated direction from its stated cell, no out-of-bounds.
2. **Exactly one occurrence**: each listed word appears exactly once in all 8 directions (palindromes like `LEVEL` are rejected for word search).
3. **No accidental offensive strings**: no blocklist substring appears in any row, column, or diagonal, forwards or backwards, anywhere in the grid (this is the check the filler is rejection-sampled against).
4. **No unlisted lexicon words ≥ 5 letters** appear in a straight line (prevents the "I found a word that isn't on the list" frustration). Shorter ones are tolerated.
5. **Crossword**: grid is connected, symmetric, every entry has a clue, every across/down run of 3+ letters is a declared entry, no clue contains its own answer, and entries are distinct.
6. **Content rules**: clue length ≤ 60, ASCII-printable plus apostrophe, no all-caps shouting, no URLs.
7. **Schema and ID**: shape matches 2.3, ID unique, `validator` equals the current validator version.

Exit code 0 only if every puzzle file passes; self-test mode (`--self-test`) feeds known-bad fixtures and requires each to fail with the right check name. Wire it as `test:word-puzzles` in `package.json` and into the contract-tests step like the mandarin audits.

### 3.4 Manifest validation

`validateSchedule()` additionally checks: every ID in `order` exists on disk, no puzzle ID appears twice within 30 days, no theme appears more than 3 times in any 7-day window, and consecutive days alternate format.

## 4. Task implications

- **t-004**: pure TS under `utils/` — `normalizeWord`, `buildLexicon`, `generateWordSearch(seed, theme, size)`, `generateCrossword(seed, theme)`, `validatePuzzle`, `validateSchedule`, `puzzleIdForDate`, `mulberry32`. DB-free `tsx` tests; no `fs` in the pure modules (the CLI wrapper does I/O).
- **t-005**: hand-write `lexicon.json` (seed source) and 14 puzzles (7 `ws`, 7 `cw`) across 7 themes; the 14-day first slice is the schedule's first 14 entries. Cycle the clue bar: kind, concrete, short.
- **t-006**: page at `pages/play/word-puzzles.vue` (or `word-puzzles/index.vue` if archive becomes a route); Pinia store `stores/wordPuzzleStore.ts` owns date, puzzle, marks, and progress; components never fetch except through the store's one static-JSON loader. `localStorage` keys: `kr.wordPuzzles.progress.v1` and `kr.wordPuzzles.streak.v1`, every access in try/catch, page correct without them.
- **Art (later)**: one 2:3 header per theme, Krea 2 prompt contract, metadata in a manifest; the page must render with a plain CSS header when art is missing.

## 5. Resolved open questions

| Question | Answer |
|---|---|
| Live or static lexicon? | Static JSON, exported once, seeded by hand until then |
| Which formats? | Word search (10×10 / 12×12) and 5×5 mini crossword |
| How does the date pick a puzzle? | Local date → days since epoch → modulo schedule; no runtime randomness |
| How many words? | 600+ in ~30 themes; 8–12 per word search, 6–8 answers per crossword |
| What is "validated"? | The seven checks in 3.3, run by a self-testing CLI in CI |

Silas can redirect any of these with a one-line edit; none blocks t-004.
