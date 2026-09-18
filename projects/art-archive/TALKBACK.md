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

## 2026-09-18 | Reviewer → Worker | art-archive/t-004 | critique

type: critique

**Decision:** rejected (pass 1, quality), then merged after fix

**Subject:** First implementation of the recursive dry-run scanner scoped JPEG/WebP metadata extraction as unconditionally unsupported, missing the task's own explicit requirement.

**What was good:**
- The scanner itself (root confinement via `realpath`, sha256 hashing, symlink-escape handling as a non-fatal `issue` rather than a thrown error) and the PNG A1111/ComfyUI parsing were solid on the first pass — read-only, well-tested against real byte fixtures, no DB/filesystem writes.

**What to improve:**
- `extractArchiveImageMetadata()` returned `{supported: false}` for every JPEG/WebP file unconditionally, with the PR body reasoning that PNG is "the format that actually carries this data in practice." That's true for the common case but the task note (art-archive/t-004) explicitly asks to "extract available ... EXIF/text metadata" — JPEG/WebP EXIF UserComment/ImageDescription, XMP, and JPEG COM segments can and do carry real generation provenance from other tools. Returning a format-wide `false` would have silently discarded exactly the evidence the later importer/resource-matcher (t-005/t-006) needs to preserve. Review (`openai-scheduled-2026-09-18T031849Z-artarchive-pr2816-a1`) caught this and blocked the merge with a specific, actionable ask.
- The Worker (this session) fixed it same-cycle: added a dependency-free minimal TIFF/EXIF reader (`ImageDescription`/`UserComment` via IFD0 + the Exif sub-IFD) plus JPEG marker and WebP RIFF-chunk walking, with `supported: false` now reserved for files where nothing was actually found. New fixtures build real TIFF/JPEG/WebP byte structures rather than stubs, proving the fields actually survive extraction. Good, thorough recovery — the kind of fix that closes the actual gap rather than a narrower patch just to satisfy the review comment's letter.
- Separate note: Silas pushed two commits directly onto the Worker's branch mid-review, correcting an invented `ART_ARCHIVE_ROOT` env var to the already-existing production `PRIVATE_PATH` mount (and resolving art-archive/t-017 in the same motion). The Worker handled this correctly — fetched, rebased its own follow-up commit on top rather than force-pushing over Silas's edit, verified clean, re-pushed.

**Kaizen task:** none created — t-005/t-006 already exist as the natural next slices and don't need a new task to encode this lesson; the LEARNING.yaml record covers it.

**Pattern note:** This is the first review rejection on this project. Worth watching whether future cycles keep defaulting scope to "the common/easy case" when a task's note is more expansive than that — re-reading the task's exact wording against the diff before calling something out of scope is the concrete habit to reinforce.
