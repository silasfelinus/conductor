# Expression reconcile script — spec

Task: kind-robots/t-011. Companion to `GENERATION.md` and kind_robots
`sample/generation/expressions.md`.

## Purpose

Make the expression folders the source of truth for pixels while the
`ExpressionMedia` rows stay the queryable index. Today the two can
drift: files exist with no row (art generated but never registered),
rows point at files that don't exist (renamed/removed art), or metadata
disagrees with the filename. This script detects and repairs that drift
in one direction: **folder → rows**. It never writes, moves, or deletes
image files.

## Inputs

- A checkout (or GitHub raw listing) of kind_robots
  `public/images/bots/expressions/{slug}/` and
  `public/images/characters/expressions/{slug}/`
- The kind_robots API with `KR_API_TOKEN` (same auth pattern as
  `scripts/fetch_todos.py`)
- Owner resolution: folder `{slug}` → Bot.slug or Character.slug via
  `GET /api/bots` / `GET /api/characters` (a folder matching neither is
  reported, never guessed)

## File convention parsed

`{key}_{nn}.webp` — `key` is a lowercase canonical expressionKey (one of
the 20 enum names) or a custom slug; `_01` is the promoted take (higher
numbers are variants and are ignored for row purposes). `{key}_loop.webp`
→ `videoPath`. `{from}_to_{to}.webp` → ExpressionTransition.

## Behavior

1. **Scan** every expression folder; build the expected row set per owner.
2. **Diff** against existing rows (`GET /api/narrators/…` or a bots/
   characters expression listing):
   - file without row → CREATE (via `POST /api/bots/expressions`
     batch upsert; kind inferred from the canonical key, `CUSTOM` +
     `kind: ACTION` for unknown keys; `designer: 'reconcile-script'`)
   - row whose `imagePath` file is missing → REPORT (and with
     `--deactivate`, set `isActive: false`; never delete)
   - row/file metadata mismatch (imagePath differs from convention) →
     UPDATE imagePath only; never touch `message`, `additionalPhrases`,
     `label`, `emoticon`, or `artPrompt` — those are richer than
     anything derivable from a filename
3. **Transitions**: same treatment via `POST /api/bots/transitions`.
4. **Report**: print created/updated/reported counts per owner plus a
   drift summary; exit nonzero if drift was found in `--check` mode (CI
   usable).

## Modes

- default: dry-run — full report, no writes (mirrors the API's
  `dryRun: true` support)
- `--apply`: perform the creates/updates
- `--deactivate`: with `--apply`, also flip `isActive: false` on rows
  whose files are gone
- `--owner {slug}`: limit to one bot/character

## Boundaries

- API writes only (`KR_API_TOKEN`), never raw SQL — consistent with
  BOUNDARY.md's consume-don't-modify rule; the endpoints already exist.
- Creates and updates are additive/reversible; the only "removal" is a
  soft `isActive: false` behind two explicit flags.
- No ArtImage rows are ever created (see expressions.md rule 3).

## Deliverable

`scripts/reconcile_expressions.py` in conductor (house style:
`fetch_todos.py` / `sync_projects_to_dreams.py`), plus a short usage
section appended to this doc. Optional follow-up once trusted: a CI
check that runs `--check` after image-distribution pushes.

## Usage (shipped 2026-07-09)

```bash
# Report drift, write nothing (kind_robots checkout at ../kind_robots):
python scripts/reconcile_expressions.py

# One owner, CI-style (exit 2 on drift):
python scripts/reconcile_expressions.py --owner brass-lampkeeper --check

# Repair drift (requires KR_API_TOKEN admin/server key):
python scripts/reconcile_expressions.py --apply

# Also soft-disable rows whose files are gone:
python scripts/reconcile_expressions.py --apply --deactivate
```

Flags: `--type bot|character`, `--owner {slug}`, `--skip-transitions`;
env `KR_BASE_URL`, `KIND_ROBOTS_ROOT`. Reads are public endpoints
(`/api/bots`, `/api/characters`, `/api/narrators/{type}/{slug}`); writes
go through the batch upserts, each batch validated with the endpoint's
`dryRun: true` before the real call.

Implementation notes (verified against a live folder scan 2026-07-09):

- Owners whose narrator endpoint 404s (inactive/private) get minimal
  blind upserts (imagePath/videoPath only) — safe because the upsert's
  update half skips omitted fields, so richer metadata and a deliberate
  `isActive: false` both survive.
- Single-digit takes (`anxious_1.webp`) are tolerated; files that don't
  match the convention at all (`0001surprised.webp`) are reported, never
  guessed. Folders matching no bot/character slug are reported the same
  way (the live scan found 60+ expression folders for bots not yet in
  the database — expected while narrator seeding is ahead of art
  registration; the script leaves them alone).
- Loop videos with no matching still are reported and skipped — a row
  needs a promoted still first.
