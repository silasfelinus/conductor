# Art Archive — TALKBACK

## 2026-09-18 | Agent (Claude, scheduled conductor run) | art-archive/t-003 | resolution

type: resolution

**Subject:** Claimed and closed t-003 (durable ArchiveEntry ledger) — first implementation cycle on this project.

**Detail:**
- Read the full roadmap and DESIGN-BRIEF.md before starting. t-003 was the only `ready` task (t-004 onward all `depends_on` it and were `waiting`).
- Added `prisma/art-archive.prisma` (`ArchiveEntry` model) plus a hand-authored matching migration in kind_robots, following two existing conventions rather than inventing new ones: `ModelBuildRun.sourceSnapshot`'s free-form-JSON-in-LongText pattern for `extractedMetadata`/`matchSummary`, and `ModelBuildItem.artImageId`'s loose (no formal `@relation`) foreign-key-shaped Int field, which meant `ArtImage`/`ArtCollection` needed zero schema changes to link an archive entry to either.
- Verified locally before pushing: `prisma validate`, the repo's own `schemaMigrationParity` self-test and verifier (confirms the migration file matches the schema diff), and `vue-tsc --noEmit`. `prisma format` flagged 4 *pre-existing* unrelated files as unformatted (`brainstorm.prisma`, `facet-catalog.prisma`, `mandarin_requests.prisma`, `schema.prisma`) — reverted that reformatting rather than folding it into this PR's diff (scope discipline; not enforced in CI either).
- kind_robots CI's "Replay migrations on MariaDB" job is the actual proof the hand-authored SQL is correct against a real database, since this sandbox has no `MIGRATION_DATABASE_URL`/shadow DB — it passed clean, along with all 49 other checks.
- Merged kind_robots#2815, then conductor#4592 (review) and this close-out (done).

**Suggested action:** t-004 (recursive dry-run scanner) is now unblocked and is the natural next slice — no design ambiguity left to resolve first, the ledger schema already anticipates what it needs to write (contentHash, relativePath, parentFolder, fileSize/fileMtime, processState).
