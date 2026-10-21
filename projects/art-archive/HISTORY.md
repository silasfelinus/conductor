# art-archive — task history archive

Full `note:` prose for completed art-archive tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-001 — Write the design brief and audit existing Kind Robots art infrastructure

<!-- note:begin t-001 -->
DESIGN-BRIEF.md captures the requested archive workflow and the initial infrastructure audit. Existing ArtImage already has isPublic/isMature, checkpointResourceId, prompt/generation fields and LoraResources; existing ArtCollection already supports many-to-many ArtImages and parentFolder. Existing resourceProvenance.ts provides a conservative starting point for active CHECKPOINT/LORA/LYCORIS resolution.
<!-- note:end t-001 -->

## t-003 — Add the durable archive-entry ledger for file identity, processing state, rating, and match review

<!-- note:begin t-003 -->
Add only the minimum additive schema needed to remember filesystem state independently of ArtImage: stable content hash, current relative path, size/mtime hints, linked ArtImage, folder collection, processed/review state, 1-5 rating, extracted metadata/match summary, and a manual-match lock or equivalent. Structured payloads follow the repo's LongText/string convention. This ledger is indexing/curation state, not a second ArtImage.
Merged kind_robots#2815 (2026-09-18): added ArchiveEntry (prisma/art-archive.prisma) plus its hand-authored migration (prisma/migrations/20260918023500_add_archive_entry). Purely additive one-table schema: contentHash, relativePath (unique), parentFolder, fileSize/fileMtime, loose artImageId/folderCollectionId (no formal relation, matching ModelBuildItem's own convention), processState (PENDING/IMPORTED/ERROR/MISSING), matchState (UNMATCHED/SUGGESTED/CONFIRMED/MANUAL/AMBIGUOUS) + resourceMatchLocked, rating, extractedMetadata/matchSummary JSON. Verified via prisma validate, schemaMigrationParity self-test + verify, vue-tsc --noEmit (all clean), and CI's own "Replay migrations on MariaDB" job (confirms the hand-authored SQL applies cleanly against a real MariaDB instance). All 49 kind_robots checks green, mergeable_state clean. t-004 (recursive dry-run scanner) is now unblocked.
<!-- note:end t-003 -->

## t-004 — Build a recursive dry-run archive scanner with metadata extraction and root confinement

<!-- note:begin t-004 -->
Scan PRIVATE_PATH recursively without mutating files. Production already provides PRIVATE_PATH=/app/private, backed by /mnt/user/pc/kindrobots/private. Recognize supported image formats, compute a stable content hash, capture relative path/parent folder/size/mtime, and extract available A1111 PNG parameters, Comfy prompt/workflow metadata, EXIF/text metadata, prompt, negative prompt, seed, CFG, sampler, checkpoint names, hashes, and LoRA tokens. Every resolved path must remain inside the configured root. PR #2816 was corrected during review to use the existing PRIVATE_PATH contract rather than invent ART_ARCHIVE_ROOT.
Merged kind_robots#2816 (2026-09-18): recursive dry-run archive scanner (server/utils/artArchiveScanner.ts) with realpath-based root confinement, sha256 content hashing, and metadata extraction (server/utils/artArchiveMetadata.ts): PNG tEXt/iTXt A1111 "parameters" + ComfyUI "prompt" graph parsing, plus dependency-free JPEG/WebP EXIF (ImageDescription/UserComment)/XMP/COM extraction.
Review (openai-scheduled-2026-09-18T031849Z-artarchive-pr2816-a1) initially blocked the PR: the first pass returned supported:false for every JPEG/WebP unconditionally, which would have silently discarded exactly the EXIF/text-metadata evidence t-004's own note calls for. Fixed same-cycle: added a minimal TIFF/EXIF reader plus JPEG marker/WebP RIFF-chunk walking, with supported:false now reserved for files where nothing was actually found. New byte-level fixtures prove extraction survives.
Also rebased on top of Silas's own direct commits (c77d169, a1d6bbc) switching the archive-root variable from this session's invented ART_ARCHIVE_ROOT to the existing production PRIVATE_PATH mount -- see art-archive/t-017, which Silas closed done himself in the same window.
Verified: schema-free (no DB changes), prisma n/a, vue-tsc --noEmit clean, eslint clean, self-test (utils/scripts/verifyArtArchiveScanner.test.ts) covers A1111, ComfyUI, JPEG EXIF+COM, WebP EXIF+XMP, content hashing, and the root-confinement/ symlink-escape property. All 48 kind_robots checks green, mergeable_state clean. t-005 (ArtImage/ArtCollection import) and t-006 (Resource matching) are now unblocked and can consume this scanner's output directly.
<!-- note:end t-004 -->

## t-005 — Implement idempotent private+mature ArtImage and folder-ArtCollection import

<!-- note:begin t-005 -->
Reconcile scanner entries into ArtImage records with isPublic=false and isMature=true every time, never inferred from Resource metadata. Create or reuse a private+mature folder ArtCollection based on the image's immediate parent folder. Use parentFolder/full relative path to disambiguate repeated folder names. Re-scans must not duplicate existing content. A missing or unresolved checkpoint/LoRA never blocks image import; retain its raw metadata for later reconciliation.


Implemented an idempotent archive importer on a worker branch. It creates/reuses deterministic folder collections, forces archive ArtImages and collections private+mature on every pass, preserves extracted metadata, and reconnects existing ledger-linked images rather than duplicating them.

Reviewed and merged kind_robots#2818 (session openai-scheduled-2026-09-18T111821Z-art-
archive-t005-a1). Diff: server/utils/artArchiveImporter.ts
(+utils/scripts/verifyArtArchiveImporter.mjs), +188/-0. Forces
isPublic=false/isMature=true on every pass for both ArtImage and its folder
ArtCollection; folder identity keyed on sha256 of the full parent path (not the leaf
name), avoiding repeated-folder-name collisions; idempotent via
ArchiveEntry.relativePath lookup, reconnecting an existing ledger-linked ArtImage rather
than duplicating; raw scanner metadata preserved verbatim in extractedMetadata for
t-006's later Resource reconciliation. No schema/DB changes. All 47 kind_robots CI
checks green, mergeable_state clean. Posted REVIEWING marker before review. t-006
(confidence-ranked Resource matching) and t-008 (repeatable reconciliation) are now
unblocked.
<!-- note:end t-005 -->

## t-006 — Build confidence-ranked matching from legacy metadata to active checkpoint and LoRA Resources

<!-- note:begin t-006 -->
Match only active Resources with compatible types. Prefer embedded ids, then exact localPath/name/customLabel and normalized basename matches, then parsed A1111/Comfy model and LoRA names/hashes. Folder/file-name clues and fuzzy matching are suggestions only. Return candidates with evidence and confidence; never let a Resource's maturity flag alter ArtImage privacy. Unmatched embedded names/hashes/tokens feed the missing-Resource backlog rather than being discarded.
Implemented matchArchiveResources() in server/utils/artArchiveResourceMatch.ts on kind_robots claude/eager-bohr-v8dejz. Tiered matching: embedded hash > exact name > normalized basename > folder/file-name substring suggestion; a tier is only consulted once every tier above it found nothing, and a same-tier tie returns all candidates rather than an arbitrary pick. Unmatched evidence retained per checkpoint/LoRA slot for t-021's backlog. JPEG/WebP return no evidence (t-004 has no structured fields for those formats). Never reads isMature/isPublic -- enforced by a self-test source scan, not just a comment. Also wired t-005's already-shipped verifyArtArchiveImporter.mjs into CI (existed since kind_robots#2818 but nothing ran it). Verified: eslint clean, self-test (verifyArtArchiveResourceMatch.test.ts) covers hash/exact/basename/suggested tiers, ambiguous ties, CHECKPOINT/LORA pool separation, unmatched backlog retention, unsupported-format short-circuit, and the isMature/isPublic structural invariant. vue- tsc running; PR opens once clean.
Merged kind_robots#2819. All 49 CI checks green (including the new resource-match self- test and t-005's now-wired importer contract), mergeable_state clean before merge. t-007 (apply high-confidence provenance) and t-021 (missing-Resource backlog) can now consume matchArchiveResources()'s output directly.
<!-- note:end t-006 -->

## t-007 — Apply high-confidence resource provenance while preserving manual corrections

<!-- note:begin t-007 -->
Populate ArtImage.checkpointResourceId and LoraResources only from unique, defensible matches. Store unresolved/ambiguous candidates for admin review. A manual resource choice locks that field against future automatic scans until explicitly unlocked.


Roadmap-auditor repair: dependency t-006 is done, so this waiting task is now eligible for work.

Implementation PR kind_robots#2821 merged 2026-09-18T06:19:06Z (all CI green, squash-
merged by Silas). Closing t-007 to done.
<!-- note:end t-007 -->

## t-008 — Add repeatable reconciliation for newly dropped, copied, moved, changed, and missing files

<!-- note:begin t-008 -->
Reconciliation, not a fragile filesystem watcher, is the source of truth. Manual rescan plus a safe scheduled/accelerated scan should make newly dropped files appear automatically. Content hash distinguishes moves from changes where possible; missing files are marked, not silently deleted.


Roadmap-auditor repair: dependency t-005 is done, so this waiting task is now eligible for work.

Implementation PR kind_robots#2822 open (repeatable reconciliation for
new/changed/moved/copied/missing files). Will follow up with status: done once CI-green
and merged.

Implementation PR kind_robots#2822 merged 2026-09-18T06:53:xxZ (49/49 CI checks green,
squash-merged). Fixed a CI-only bug found while implementing: the pure planner had to be
split into its own artArchiveReconcilerPlan.ts module (no Prisma import) since the
reconciler unit test runs without DATABASE_URL in CI. Closing t-008 to done.
<!-- note:end t-008 -->

## t-009 — Add admin-only archive APIs for browse/filter/detail and safe filesystem actions

<!-- note:begin t-009 -->
Require admin authentication and mature-content permission. Support folder, collection, processed state, rating, resource-match state, and search filters. File moves/deletes must be root-confined and path-traversal safe. Automatic scans never move/delete anything.


Roadmap-auditor repair: dependency t-005 is done, so this waiting task is now eligible for work.

Implementation PR kind_robots#2825 open (admin browse/filter/detail APIs + safe
filesystem move/quarantine actions). Will follow up with status: done once CI-green and
merged.

Merged kind_robots#2825 (squash 029f33d). All CI green except 'Build production image',
which was cancelled mid-run (infra/concurrency cancellation, not a code failure --
confirmed via job log: 'The operation was canceled' during docker buildx teardown, no
test/build step ever failed) while a second PR (#2826) was pushed concurrently in this
session; mergeable_state was 'unstable' but not 'dirty'/'blocked'. All 50 other checks
(TypeScript, Contract verifiers, layout-contract, facet-catalog, full
Storybook/Narrative/Taskmaster suite) passed. Reviewed the diff: admin-gated
browse/filter/detail endpoints plus root-confined, path-traversal-safe move/quarantine
actions (quarantine relocates into a reserved trash subtree rather than deleting,
matching stakes: reversible); scanner now skips that trash subtree so quarantine isn't
silently undone by the next rescan. t-010 (admin archive browser) is now fully
unblocked.
<!-- note:end t-009 -->

## t-010 — Build the admin archive browser with processed/unprocessed and folder/collection views

<!-- note:begin t-010 -->
Add this to the existing admin surface rather than creating a new top-level channel. Art-first dense gallery, folder tree/collection picker, processed and unprocessed toggles, match-state filters, rating filters, and a detail editor for prompt/checkpoint/LoRAs and extracted metadata.


Roadmap-auditor dependency repair: t-009 is done, so t-010 is now eligible for work.

Implemented the first admin Art Archive browser slice with store-owned API access, filters, pagination, dense 2:3 gallery cards, and provenance/detail inspection.

Reviewer rejection (pass 1, quality) on kind_robots#2836: two real CI failures
reproduced locally, not flaky. (1) TypeScript TS2551 at pages/admin/art-
archive.vue:108,116 -- `userStore.isInitialized` does not exist, correct field is
`initialized`. (2) kr-class-coverage failure -- template uses `class="kr-select ..."` on
every <select>, but assets/css/tailwind.css only defines `.kr-select-sm`/`.kr-select-
muted`, no bare `.kr-select`. Fix: rename the store field reference to
`userStore.initialized`, and either add a `.kr-select` base primitive to tailwind.css or
use an existing select class. All other 49 checks were green; scope/architecture of the
PR is otherwise fine. See PR comment for full detail.

Retry addresses pass-1 review feedback on kind_robots#2836: use userStore.initialized and the existing kr-select-sm primitive. Fresh CI is running on commit 7656be7f532accfb216c8800c0c98ec3ab447a0a.

Pass 2 merged: kind_robots#2836 squash-merged (fc3c161). Fixed userStore.initialized and
kr-select-sm from pass-1 rejection. 51/51 checks green.
<!-- note:end t-010 -->

## t-011 — Support root-safe moves plus folder-derived and custom ArtCollection membership

<!-- note:begin t-011 -->
Moving a file updates its archive path and folder-derived collection. Custom ArtCollections coexist with folder membership instead of replacing it. No operation may escape the archive root.


Added an admin-only custom ArtCollection membership endpoint for imported archive images. It preserves the folder-derived collection as path-owned state, validates active collections, and supports additive/removal membership without moving archive bytes.

Merged kind_robots#2839 (squash cec9d7b4). Existing t-009 move handling already root-confines filesystem moves, updates the archive path and folder-derived collection, and disconnects only the prior folder collection. Added an admin-only custom ArtCollection membership endpoint that connects/disconnects custom memberships while refusing manual removal of the path-owned folder collection. All 48 PR checks completed; no queued or in-progress checks remained and Contract Tests run 35349943355 completed successfully.
<!-- note:end t-011 -->

## t-012 — Add delete/remove workflow with recoverable trash semantics

<!-- note:begin t-012 -->
The normal Delete action should move the source file into an archive trash area and mark the ledger/ArtImage inactive rather than immediately destroying bytes. Permanent purge, if added, is an explicit separate admin action. Keep enough provenance to explain what happened.


Roadmap-auditor dependency repair: t-009 is done, so t-012 is now eligible for work.

Worker (Claude, scheduled conductor run): implemented recoverable delete/restore for
Art Archive. The existing quarantine ("delete") action from t-009 was backend-only,
never wired to any UI, and had no way back -- it overwrites relativePath with the
trash path, losing the original location. Added a nullable preQuarantineRelativePath
column (additive migration) that quarantine now populates, and a new restore.post.ts
endpoint that is quarantine's exact inverse: moves the file back (root-confined,
no-overwrite) and flips isActive back to true on the entry and its ArtImage. Wired
the admin page with a "Show trash" filter toggle, a Trashed badge, and Delete/Restore
buttons. vue-tsc, eslint, the fileops unit tests (including two new restore-round-trip
cases), kr-class-coverage, and the layout contract all pass. No manual browser
click-through was possible in this sandbox. kind_robots#2846 open, CI running.

kind_robots#2846 merged (squash 78d845f), all checks green including Contract verifiers
and the production image build. Closing t-012: restore.post.ts (quarantine's exact
inverse), the preQuarantineRelativePath column, and the admin UI (Show trash toggle,
Trashed badge, Delete/Restore buttons) are all live. A manual browser click-through was
not possible in this sandbox -- flagged in the PR's test plan for a future spot-check.
<!-- note:end t-012 -->

## t-013 — Persist 1-5 archive ratings and expose fast rating actions

<!-- note:begin t-013 -->
Rating is curation state on the archive entry and survives rescans/moves. Make 1/2/3/4/5 available as click and drag/drop targets and filterable in the gallery.
Worker (Claude, scheduled conductor run): rating already existed on ArchiveEntry (filterable, displayed) but had no write path. Added entries/[id]/rate.patch.ts (admin-gated PATCH, {rating: 1-5|null}) and wired the admin page with five rating targets above the grid that work as both click targets (rate the open detail entry) and drag/drop targets (drag any thumbnail onto one) -- grid entries are now draggable. Rating patches the entry in place in the store rather than a full refetch. vue-tsc, eslint, prettier, kr-class-coverage, and the layout contract all pass. No schema change needed. No manual browser click/drag-through was possible in this sandbox. kind_robots#2847 open, CI running.
kind_robots#2847 merged (squash 7545afd), all checks green. Closing t-013: rate.patch.ts and the five click/drag-drop rating targets above the grid are live.
<!-- note:end t-013 -->

## t-014 — Add persisted archive action presets for generation modifiers

<!-- note:begin t-014 -->
Presets describe reusable edits such as add/replace a LoRA, swap checkpoint, append/replace prompt text, change generation settings, create an additional render, or replace the source after successful generation. Reuse current ArtJob vocabulary rather than inventing a second renderer.
Reviewed and merged kind_robots#2826 (squash 9ff9790). Diff: purely additive migration (one new ArchiveActionPreset table, no existing table touched), zero-Prisma preset- modifiers validator (matches this session's own t-008/t-009 DB-free-testability convention) with full per-actionType unit coverage, four admin-gated CRUD endpoints (delete is soft via isActive: false, matching stakes: reversible). All 54 CI checks green, mergeable_state clean. Posted REVIEWING marker before review. t-015 (drag/drop curation board) now has both dependencies (t-010, t-014) in progress.
<!-- note:end t-014 -->

## t-015 — Build the drag/drop curation board with preset modifier targets

<!-- note:begin t-015 -->
Let the admin drag selected art onto visible action targets such as Rate 1-5, Delete, Add to collection, and named regeneration presets. Batch actions must preview scope and report partial failures clearly.


Implemented the first curation-board slice in Kind Robots: batch thumbnail selection, rating and recoverable-delete targets with explicit destructive confirmation and partial-failure retention, plus persisted preset targets loaded from the existing archive preset API. Durable preset execution remains intentionally owned by t-016 rather than inventing a second render queue.

Reviewer rejection (pass 1, quality): kind_robots#2866's 'Contract verifiers' CI check
fails -- verifyDisabledAffordances.ts flags pages/admin/art-archive.vue:30 (curation-
board Clear button rendered disabled with no subject when nothing is selected),
violating the standing Silas rule against blanked-out options. Not transient --
reproduced by CI on the current head commit, deterministic. Posted specific fix on
kind_robots#2866. status: ready, passes: 1, retry_context set below.

Retry addresses pass-1 disabled-affordance rejection: batch controls now appear only when a selection exists, and loading remains the only disabled state for live batch actions. Existing PR #2866 updated on its worker branch.

Retry addressed pass-1 rejection (verifyDisabledAffordances): Clear button now uses v-if
instead of :disabled. Reviewer re-verified all 48 checks green, mergeable_state clean,
diff matches the specified fix. Merged kind_robots#2866 (squash 6228ade).
<!-- note:end t-015 -->

## t-016 — Queue additional or replacement ArtJobs from imported images with editable provenance

<!-- note:begin t-016 -->
Imported ArtImages have no original ArtJob, so build a narrow adapter that creates a normal durable ArtJob from the stored prompt/settings/resource provenance plus the chosen preset. Replacement must not remove the source file until a new ArtImage is delivered and verified.
Implemented: buildArchiveEnqueuePayload() + POST /api/admin/art- archive/entries/[id]/enqueue, wired into the curation board's preset buttons (deferred in t-015). Never touches the entry's file/isActive state -- only creates a new ArtJob, satisfying the 'no removal until verified' requirement by construction. Verified locally: new unit test (5 assertions), vue-tsc, eslint, disabled-affordances/kr-class- coverage/layout-contract all clean. Opened kind_robots#2868.
Merged kind_robots#2868 (squash c70c0f0). All 54 CI checks green, mergeable_state clean. buildArchiveEnqueuePayload() + POST /api/admin/art-archive/entries/[id]/enqueue queue a durable ArtJob (A1111) from an imported entry's stored prompt/settings plus a chosen ArchiveActionPreset; the endpoint never touches the entry's file/isActive state, satisfying the no-premature-removal requirement by construction. Wired into the curation board's preset buttons.
<!-- note:end t-016 -->

## t-017 — Confirm the real media-server archive root and production mount contract

<!-- note:begin t-017 -->
Resolved by Silas 2026-09-17. The existing Unraid container configuration maps host /mnt/user/pc/kindrobots/private to container /app/private and exposes PRIVATE_PATH=/app/private. The first archive batch is already in that directory and more files will be added incrementally. Scanner code should consume PRIVATE_PATH directly. This confirmation does not authorize destructive deletion of source files.
<!-- note:end t-017 -->

## t-018 — Harden large-library performance with pagination, thumbnails, incremental hashing, and bounded scans

<!-- note:begin t-018 -->
Assume the archive becomes large enough that full-image grids and re-hashing every byte on every request are unacceptable. Use thumbnails, indexed filters, incremental size/mtime checks before hashes, bounded concurrency, and resumable scans.
Implemented the landable core: scanArchiveRoot() now accepts an optional knownFiles cache (relativePath -> {contentHash, fileSize, fileMtimeMs, metadata}) and skips re- reading/re-hashing a file whose current stat (size+mtime) matches the cache exactly; loadKnownArchiveFiles() builds this from the live ArchiveEntry ledger and reconcileArtArchive.ts (the scheduled/repeated-scan CLI) now uses it, reporting a new "served from cache" count. File processing is also bounded-concurrent (default 8) instead of fully sequential. Verified: vue-tsc clean, eslint clean, test:art-archive- scanner (3 new assertions: cache-hit trust, cache-miss on stat mismatch, concurrency-vs- sequential result parity), test:art-archive-reconciler, and test:art-archive-reconcile- cli (contract regexes updated to match the new source) all pass. Pagination for the admin browse endpoint already existed (t-009); thumbnails and resumable scans are real, larger, separate design surfaces (an image-resizing pipeline/storage convention; persisted scan-cursor state) -- deferring both to follow-on tasks rather than a same- pass extension. PR: silasfelinus/kind_robots (branch worker/art-archive-t018-claude- scheduled-2026-09-19T0740Z).
Merged kind_robots#2870: incremental hashing (knownFiles cache, skips re-read/re-hash of stat-unchanged files) + bounded concurrency (default 8) in scanArchiveRoot(), wired into reconcileArtArchive.ts (the CLI meant for repeated/scheduled runs) via a new loadKnownArchiveFiles() helper. Pagination/indexed filters for the admin browse endpoint already existed (t-009). Verified: vue-tsc, eslint, and all relevant test:art-archive-* scripts pass; 47/47 kind_robots CI checks green. Thumbnails and resumable scans deferred to t-029/t-030 (real, separate design surfaces) rather than a same-pass extension.
<!-- note:end t-018 -->

## t-019 — Run production dry-run reconciliation and verify zero privacy leakage before bulk import

<!-- note:begin t-019 -->
Before applying the first large import, report counts for files, duplicates, folder collections, exact/high-confidence/ambiguous Resource matches, and proposed ArtImage writes. Verify every proposed ArtImage and folder ArtCollection is private+mature and that ordinary SFW Resource galleries do not expose linked archive images.
Implemented a --dry-run mode for reconcileArtArchive.ts (kind_robots#2871): reports the same new/changed/moved/copied/missing plan counts plus per-file resource-match evidence (t-023) via the pure planner and matchArchiveResources, with zero Prisma writes (verified by a static contract check that brace-extracts runDryRun's body and confirms it never calls reconcileArchiveScan/importArchiveFile/create/update/delete). Also audited every consumer of ArtImage.checkpointResourceId/LoraResources for the privacy- leakage concern in this task's note: server/api/resources/[id]/gallery.get.ts already runs every checkpoint/LoRA-use query through buildArtImageWhere(access), the same site- wide visibility filter every other private ArtImage goes through, so a non-admin/non- owning viewer cannot see a private+mature archive image via a Resource gallery. The importer's own privacy invariant (isPublic=false/isMature=true forced on every write) is unchanged and already durably enforced by test:art-archive-importer. Actually running --dry-run against the real archive needs PRIVATE_PATH (only mounted on the Unraid container, not this sandbox) -- next step for whoever has that shell access: PRIVATE_PATH=/app/private npx tsx utils/scripts/reconcileArtArchive.ts --dry-run, before the first bulk import.
<!-- note:end t-019 -->

## t-021 — Produce the missing checkpoint and LoRA acquisition backlog

<!-- note:begin t-021 -->
Aggregate unresolved checkpoint and LoRA evidence from scanned images into a deduplicated backlog instead of treating those images as failures. Preserve the raw embedded model name, filename/token, model hash when available, likely Resource type, occurrence count, representative ArtImage/ArchiveEntry examples, and candidate matches/confidence. Make the backlog queryable/exportable for Silas to track down and add missing Resources later. Once a Resource is added, the normal reconciliation path should re-attempt matching and clear resolved backlog entries without re-importing the image.


Implemented a queryable missing checkpoint/LoRA backlog that deduplicates unresolved evidence, preserves candidate confidence and representative archive examples, and automatically excludes resources once reconciliation applies a unique match.


Reviewer rejection (pass 1, quality): kind_robots#2824's TypeScript check fails to
compile, reproduced locally on the PR branch. rawEvidence() in the new
artArchiveMissingResourceBacklog.ts reads metadata.a1111/metadata.comfy without first
narrowing ExtractedArchiveMetadata away from its JpegWebpMetadata branch (which has
neither field), plus one downstream implicit-any on the loraTokens.map() token param.
Full errors and suggested fix posted on kind_robots#2824. Not transient -- reproduced
identically outside CI. status: ready, passes: 1, retry_context set below.

Reviewed and merged kind_robots#2824 (squash ef351f7). Retry addressed pass-1 rejection:
rawEvidence() now narrows ExtractedArchiveMetadata to the PNG branch (checks
!metadata.supported || metadata.format !== 'png') before touching .a1111/.comfy, and the
loraTokens.map() callback param is explicitly typed. All 59 CI checks green,
mergeable_state clean, diff purely additive (new backlog module + test + scoped CI
workflow, no existing files touched). Posted REVIEWING marker before review.
<!-- note:end t-021 -->

## t-022 — Wire a runnable entrypoint that calls the t-005 importer against real scanner output

<!-- note:begin t-022 -->
t-004 shipped utils/scripts/scanArtArchive.ts as a CLI entrypoint for the dry-run scanner, but t-005's importArchiveScan()/importArchiveFile() are exported functions with no script or admin route that actually invokes them against scanArchiveRoot()'s live output. Without this, the importer cannot be run against the real archive at all. Add a CLI script (mirroring scanArtArchive.ts's shape) or an admin-gated endpoint that feeds scanner results into the importer and reports created/reused counts.
Added utils/scripts/importArtArchive.ts on kind_robots claude/eager-bohr-v8dejz, mirroring scanArtArchive.ts's shape: scans the configured root then reconciles every file via importArchiveFile(), reporting created/reused image and collection counts; a per-file failure is recorded and reported, never fatal to the run. Resource matching (t-006) intentionally out of scope -- t-023 covers extending this entrypoint to report match candidates. Verified: eslint clean, regex-based contract verifier (verifyImportArtArchive.mjs, matching t-005's own convention) passes, vue-tsc running. PR opens once clean.
Merged kind_robots#2820. All 48 CI checks green, mergeable_state clean before merge. Run against the real archive via: PRIVATE_PATH=/app/private npm run art-archive:import (or npm run art-archive:import -- --root ... --user-id ...).
<!-- note:end t-022 -->

## t-023 — Extend t-022's runnable entrypoint to report resource-match candidates per file

<!-- note:begin t-023 -->
t-006 shipped matchArchiveResources() but nothing calls it yet outside its own self-test -- t-022's entrypoint imports the scanner and t-005's importer; once it exists, extend it (or the importer call site) to also run matchArchiveResources() per file and print/report each file's checkpoint/LoRA candidates, confidence tier, and any unmatched evidence, so Silas can see real match quality against the actual archive before t-007 starts applying anything automatically.


Extended the runnable Art Archive import CLI to invoke matchArchiveResources for each imported file, report checkpoint/LoRA candidate resource ids with confidence/evidence, preserve unmatched embedded evidence, and summarize match coverage. Updated the existing CLI contract verifier. Implementation branch is ready for PR review.

REJECTED pass 1 (quality) by Reviewer: kind_robots#2869 has a real CI failure on its
current head (c7eec168) -- the new "reports unmatched embedded evidence" Contract-
verifiers check does not match the actual source order in importArtArchive.ts. All other
45 checks pass and the PR is otherwise scoped and matches its own description. See
retry_context for the exact fix. Left the PR open for the Worker to push a fix to the
same branch.

Retry addressed pass-1 CI rejection by aligning the static unmatched-evidence verifier with formatOutcome() source order on kind_robots PR #2869.

Retry (pass 2) fixed the verifier regex exactly per retry_context (evidence.name ->
evidence.hash -> UNMATCHED source order). All 46 CI checks green on kind_robots#2869;
merged to main (327853b).
<!-- note:end t-023 -->

## t-024 — Add an admin-gated endpoint wrapping the t-022 import entrypoint

<!-- note:begin t-024 -->
t-022's own task note offered a CLI script or an admin-gated endpoint; the CLI was built first since it needed no new auth/route surface, but running it still requires shell access to the container. Add an admin-only API endpoint (matching the project's existing admin-gated convention) that triggers the same scan-then-import flow and returns the same created/reused counts as JSON, so this can eventually be wired into the admin archive-curation UI (m3) instead of requiring Silas to exec into the container.
Implementation PR kind_robots#2823 open (admin-gated endpoint wrapping the t-022 import entrypoint). Will follow up with status: done once CI-green and merged.
Implementation PR kind_robots#2823 merged 2026-09-18T07:0xZ (48/48 CI checks green, squash-merged). Closing t-024 to done.
<!-- note:end t-024 -->

## t-025 — Add a pure function that merges a preset's modifiers into an ArtJob payload

<!-- note:begin t-025 -->
Kaizen from t-014 (persisted archive action presets): the preset's `modifiers` JSON fragment already mirrors ArtJob payload field names by design (server/utils/artArchivePresetModifiers.ts), but nothing yet actually merges one into a real payload. Add a small, zero-Prisma, unit-tested function (e.g. `applyArchivePresetToPayload(actionType, modifiers, basePayload)`) that performs the actual per-actionType merge (add/replace a LoRA entry, swap checkpoint fields, append/replace prompt text, overwrite listed generation settings) and returns the resulting payload, matching ArtJobPayloadRecord's shape. This gives t-015's curation board (and any future "apply preset" endpoint) a tested foundation to call rather than reimplementing the merge inline against a live ArtJob write path.
<!-- note:end t-025 -->

## t-026 — Add a shared ExtractedArchiveMetadata narrowing helper

<!-- note:begin t-026 -->
Kaizen from t-021 (missing resource acquisition backlog, kind_robots#2824): the pass-1 rejection was a real TypeScript error from reading `metadata.a1111`/`metadata.comfy` before narrowing `ExtractedArchiveMetadata` away from its JpegWebpMetadata branch. The fix duplicated the same `!metadata.supported || metadata.format !== 'png'` guard that `artArchiveResourceMatch.ts`/`artArchiveMetadata.ts` already use independently. Add one shared helper (e.g. `narrowToPngMetadata(metadata): Png...Metadata | null` in `artArchiveMetadata.ts`) and have all three call sites use it, so the next module that reads `.a1111`/`.comfy` can't reintroduce the same unnarrowed-union compile error.
<!-- note:end t-026 -->

## t-027 — Add an integration check that a merged preset payload survives COMFY workflow construction

<!-- note:begin t-027 -->
Kaizen from t-025 (kind_robots#2854): applyArchivePresetToPayload() merges preset modifiers into the flat A1111-style payload shape (checkpoint, promptString, loras, cfg, etc.), matching artArchivePresetModifiers.ts's own vocabulary. It does not touch a COMFY engine's already-built workflow node graph, which is how most real ArtJob payloads (server/api/art/enqueue.post.ts's buildJobPayload) actually carry these fields. Add a focused integration-level check confirming a merged payload's fields still reach the right place after going through buildJobPayload for at least one COMFY engine (e.g. krea2), so t-015's curation board (or any future "apply preset" endpoint) has a real signal if the flat-payload merge and the graph-building step ever drift apart.
<!-- note:end t-027 -->

## t-028 — Surface queued preset-job status inline in the curation board

<!-- note:begin t-028 -->
Kaizen from t-016 (kind_robots#2868): applyPresetToSelected() queues an ArtJob per selected entry but the curation board never shows what happened to it afterward -- an admin has to separately check the general art queue (/api/art/queue/:id) to see whether a queued preset job is PENDING/RUNNING/DONE/FAILED. Add a small poll (or a "recent jobs" list keyed by the archiveEntryId/archivePresetId tags already written onto the payload) so the board itself reflects job status, once real usage shows which actionTypes admins actually reach for.
<!-- note:end t-028 -->

## t-029 — Generate real thumbnails for archive-sourced images

<!-- note:begin t-029 -->
Deferred scope from t-018 (kind_robots#2870): the admin browse endpoint already returns a thumbnailPath field, but it just falls back to the full-size ArtImage.path -- nothing actually generates a downscaled image. Design and implement a real thumbnail pipeline for archive-sourced images: pick an image-resizing approach (existing project convention if one exists elsewhere in kind_robots, otherwise a lightweight library), a storage path/naming convention alongside the original file, and a trigger point (at import time in importArchiveFile(), or lazily on first browse request). Must not touch/copy/derive from files outside the archive's own read path, and must preserve the existing private+mature invariants for anything written. A large legacy archive's grid view is the actual pain point this fixes -- full-size images in a grid of dozens/hundreds of thumbnails is the "unacceptable" case t-018's own note named.
Merged kind_robots#2875 (2026-09-19): real thumbnail generation (server/utils/artArchiveThumbnails.ts, 480px WebP q82, cached under a dot-prefixed .art- archive-thumbnails/ subtree keyed on ArchiveEntry id, invalidated by comparing cache mtime against the entry's own fileMtime -- same trust rule as the scanner's own known- file cache). Also added the byte-serving route this required: nothing previously served archive bytes over HTTP at all, so imagePath/thumbnailPath were unreachable raw filesystem paths -- server/api/admin/art-archive/entries/[id]/file.get.ts (admin-gated, root-confined via the existing artArchiveFileOps.ts helper) now serves the original or, with ?variant=thumbnail, the cached downscaled copy. entries/index.get.ts, entries/[id].get.ts, and the admin grid/detail Vue template were updated to actually use it -- the grid now renders thumbnailPath instead of the full-size imagePath. New contract test (test:art-archive-thumbnails) wired into CI. All 54 kind_robots checks green, mergeable_state clean.
<!-- note:end t-029 -->

## t-030 — Make large-archive scans resumable across process restarts

<!-- note:begin t-030 -->
Deferred scope from t-018 (kind_robots#2870): scanArchiveRoot() now skips re-hashing unchanged files via the knownFiles cache, but a scan of a very large archive that gets killed mid-walk (process restart, OOM, container recycle) still restarts from nothing -- there is no persisted cursor/checkpoint of which files/subtrees were already walked in the current pass. Design what "resumable" means here first (a full re-walk of the directory tree is comparatively cheap once hashing is cached via t-018's work -- the walk-order/readdir cost may already be small enough that this isn't worth building; confirm with a rough timing measurement against a real large archive before adding persisted state) and only build real checkpoint/cursor tracking if that measurement shows the walk itself, not the hashing, is the actual bottleneck at scale.
2026-09-19 Reviewer: merged kind_robots#2876 (squash d1ceaf9). Fixed a real mtime- precision cache-hit bug in scanArchiveRoot() (float mtimeMs vs truncated integer never matched, so every rescan re-hashed every file) rather than building the originally- titled checkpoint/cursor feature -- the PR's own benchmark shows a warm re-walk is cheap once the cache actually engages, answering this task's own gating question. All checks green, mergeable_state clean.
<!-- note:end t-030 -->

## t-031 — Surface t-023's resource-match reporting in the t-024 admin import endpoint

<!-- note:begin t-031 -->
Kaizen from t-023 (kind_robots#2869): the CLI entrypoint (utils/scripts/importArtArchive.ts) now runs matchArchiveResources() per file and prints checkpoint/LoRA candidates and unmatched evidence to the console, but the admin-gated endpoint from t-024 (server/api/admin/art-archive/import.post.ts) calls importArchiveImporter.ts's importArchiveScan() directly and never touches the matcher at all -- an admin using the endpoint (the whole point of t-024: reconciling without shell access) gets zero resource-match visibility. Extend importArchiveScan() (or add a thin wrapper) to also run matchArchiveResources() per file and include a per-file match summary (candidates + confidence/evidence, unmatched evidence) in the JSON response/summary object, mirroring what the CLI already reports, so Silas can see match quality via the endpoint before t-007 starts applying anything automatically.

Implemented admin import resource-match reporting on a scoped Kind Robots worker branch; opening PR after canonical review transition.

Reviewer merged kind_robots#2885 (squash 2839703) — all 48 checks green, mergeable_state
clean, diff scoped to exactly the admin-endpoint resource-match reporting t-031 asked
for (additive JSON fields only, no schema change). Closed to done.
<!-- note:end t-031 -->

## t-032 — Surface t-019's dry-run reconciliation report via an admin-gated endpoint

<!-- note:begin t-032 -->
Kaizen from t-019 (kind_robots#2871): reconcileArtArchive.ts's new --dry-run mode reports new/changed/moved/copied/missing plan counts plus resource-match evidence with zero database writes, but it is CLI-only -- there is still no way to preview a reconciliation pass without shell access to the production container, which is the exact gap t-024 closed for the (real) import path. Add an admin-gated endpoint (matching t-024's server/api/admin/art-archive/import.post.ts convention) that runs the same read-only plan + resource-match report and returns it as JSON, so Silas can preview counts and resource-match quality before the first bulk import without exec'ing into the container. Must remain provably write-free -- reuse or mirror utils/scripts/verifyReconcileArtArchiveCli.mjs's brace-extraction technique to assert the endpoint's handler never calls a write path.

Added an admin-gated read-only reconciliation preview endpoint in Kind Robots, including plan counts, cache stats, and resource-match evidence, plus a static write-path guard.

Merged kind_robots#2886 (squash d9477e6). All 49 checks green (Contract verifiers,
TypeScript, layout-contract included). Reviewed by scheduled Conductor Agent session;
endpoint is admin-gated, additive, and provably write-free per its own static verifier.
<!-- note:end t-032 -->

## t-034 — Persist archive-preset actionType on the ArtJob row (or its payload) independent of the preset row

<!-- note:begin t-034 -->
Kaizen from t-028 (kind_robots#2873): the new job-status board relies on archivePresetId to resolve an actionType for display, but that only works for as long as the referenced ArchiveActionPreset still exists -- an admin can edit or delete a preset later, silently orphaning the historical actionType for any job that already ran under it. Add actionType as its own tagged field on the ArtJob payload (matching how archiveEntryId/archivePresetId are already tagged in buildArchiveEnqueuePayload.ts), so a future report/aggregation by action type doesn't depend on presets never being edited or deleted.
(Renumbered from t-033 to t-034 during a PR merge conflict on 2026-09-19: a concurrent session independently filed its own t-033 -- "Confirm archive-preset ArtJobs are safe to always tag engine: 'A1111'" -- from the same t-027/t-016 investigation. Both are kept; this one moved to the next free id rather than either being dropped.)
Merged kind_robots#2887 (squash b6751ee). All 48 checks green (Contract verifiers, TypeScript, layout-contract, GitGuardian included; full local npm run test:contracts-db- free -- 364/364 -- also verified before push). actionType now tagged directly on the ArtJob payload in buildArchiveEnqueuePayload.ts, surfaced by pickLatestArchiveEntryJobs.ts, and threaded through stores/artArchiveStore.ts's ArchiveEntryJobStatus type.
<!-- note:end t-034 -->

## t-035 — Add a medium-sized cached preview for the archive detail panel

<!-- note:begin t-035 -->
Kaizen from t-029 (kind_robots#2875): the admin detail panel's larger preview always requests the full-size original via entries/[id]/file.get.ts, which could be slow on first paint for a very large source file. Add a "medium" cached variant (~1200px, reusing artArchiveThumbnails.ts's same dot-prefixed cache-folder pattern and mtime-based invalidation) and serve it from the detail panel instead of the untouched original, if large originals turn out to be common in the imported archive.
Added ensureArchiveMediumPreview (~1200px WebP, cached under .art-archive-medium/, same mtime-invalidation pattern as the existing thumbnail cache) and switched the admin detail panel's default imagePath to the medium variant; kept a new originalPath field + small 'View original' link so the untouched full-size file is still reachable. Verified: npm run test:art-archive-thumbnails (new medium-preview test included), vue-tsc --noEmit clean, eslint clean on all touched files, test:kr-class-coverage OK, test:layout- contract no new violations, and the full test:contracts-db-free suite (364/364 scripts) green. Could not measure real archive file-size distribution from this sandbox (private archive root lives on Silas's Unraid host, not reachable here, and ArchiveEntry has no stored fileSize field) -- built the feature unconditionally since it is low-risk, reversible, and mirrors the existing thumbnail-cache architecture exactly, rather than leaving it unbuilt for lack of a measurement this session could not take.
<!-- note:end t-035 -->

## t-036 — Report the archive scanner's cache-hit rate prominently in dry-run output

<!-- note:begin t-036 -->
Kaizen from t-030 (kind_robots#2876): that PR fixed a real bug where scanArchiveRoot()'s cache-hit check compared a live float mtimeMs against a truncated-integer known.fileMtimeMs and almost never matched, so every rescan silently re-hashed every unchanged file. ArchiveScanResult.cacheHitCount is already tracked but not prominently surfaced. Have reconcileArtArchive.ts's --dry-run output report the cache-hit count/percentage clearly, so a future regression of this kind (or any other cause of the cache silently not engaging) is visible from an ordinary dry-run instead of requiring someone to notice a scan running slower than expected.
Merged kind_robots#2883 (squash 00c607e): reconcileArtArchive.ts's --dry-run and real- run reporting blocks now print the cache-hit percentage (N/M, P.P%) alongside the existing raw count, closing the visibility gap t-030's fix left. Verified: eslint/vue- tsc clean, verifyReconcileArtArchiveCli.mjs (12/12 static contract checks incl. the existing /served from cache/ regex), verifyArtArchiveScanner.test.ts, verifyArtArchiveReconciler.test.ts all pass. Kaizen deferred: no new gap surfaced by this small, scoped fix.
<!-- note:end t-036 -->

## t-037 — Extract resource-match report aggregation into a shared pure helper for CLI and admin endpoint

<!-- note:begin t-037 -->
Kaizen from t-031 (kind_robots#2885): the admin import endpoint (server/api/admin/art-archive/import.post.ts) now computes its own filesWithMatchEvidence/unmatchedModels summary counts inline, right after utils/scripts/importArtArchive.ts's CLI computes the same kind of summary from the same matchArchiveResources() output independently. Extract the aggregation (candidate/evidence counting, unmatched-model tallying) into one shared pure helper both callers use, so the CLI and the admin endpoint cannot silently drift in what counts as "matched" or "unmatched" as the matcher evolves.
t-032's dry-run endpoint (kind_robots#2886, merged) adds a THIRD independent inline aggregation of matchArchiveResources() output (confidenceCounts/filesWithMatchEvidence/unmatchedModels), alongside the CLI and the t-031 import endpoint this task already targets. Scope now covers three call sites, not two.
<!-- note:end t-037 -->

## t-038 — Surface actionType on the admin curation board's job-status badge

<!-- note:begin t-038 -->
Kaizen from t-034 (kind_robots#2887): actionType is now tagged durably on the ArtJob payload and returned by GET /api/admin/art-archive/entries/jobs (ArchiveEntryJobStatus.actionType), but pages/admin/art-archive.vue's job-status badge still only shows "Job {{status}}" -- it never displays what action the job actually ran. Surface actionType in the badge (e.g. its title/tooltip, or appended to the label), now that it is durably available without a live preset lookup.
Merged kind_robots#2888 (squash 795a3d7). Appended actionType to the job-status badge's visible label and tooltip in pages/admin/art-archive.vue, when present. Verified: eslint clean, vue-tsc --noEmit clean, npm run test:contracts-db-free 364/364, and full CI (48 checks incl. Contract verifiers, TypeScript, layout-contract, GitGuardian) green before merge. Pre-existing prettier warning on this file confirmed unrelated (reproduces on main).
<!-- note:end t-038 -->

## t-039 — Add a dedicated verify script for the admin import.post.ts endpoint

<!-- note:begin t-039 -->
Kaizen from t-037 (kind_robots#2889): of the three call sites sharing matchArchiveResources() output (CLI, admin import endpoint, admin dry-run endpoint), only the CLI (verifyImportArtArchive.mjs) and the dry-run endpoint (verifyArtArchiveDryRunEndpoint.mjs) have a dedicated verify script. server/api/admin/art-archive/import.post.ts has none -- add one mirroring verifyArtArchiveDryRunEndpoint.mjs's shape (mock requireAdminApiUser/scanArchiveRoot/importArchiveScan/ matchArchiveResources, assert the response shape and the filesWithMatchEvidence/unmatchedModels aggregation), so all three call sites have equivalent contract coverage.
Implemented as utils/scripts/verifyArtArchiveImportEndpoint.mjs, mirroring verifyArtArchiveDryRunEndpoint.mjs's static source-contract shape. Verified locally against the real endpoint source before pushing. Merged kind_robots#2890.
<!-- note:end t-039 -->

## t-040 — Give the admin archive page Dry Run and Import controls

<!-- note:begin t-040 -->
Filed 2026-09-20 from Silas's question "where are we on the adult private import project?". The endpoints shipped without a caller: t-024 added POST /api/admin/art-archive/import and t-032 added POST /api/admin/art-archive/dry-run, and t-039 gave both verify coverage, but nothing in stores/ or pages/ ever called either one. The only way to ingest the production archive was a shell on the container with PRIVATE_PATH set -- which is exactly what blocked t-019 from finishing its own job and left production at 0 ArchiveEntry rows.
Adds runDryRun()/runImport() to stores/artArchiveStore.ts and an "Ingest from the media server" panel to pages/admin/art-archive.vue: Dry Run reports scanned/new/changed/moved/copied/unchanged/missing counts, cache hits, scan issues, per-confidence Resource match tiers, and the unresolved-model count; Import stays disabled until a dry run has reported, then takes an explicit confirmation, and afterwards shows created/reused images and collections plus any per-file failures. Contract pinned by utils/scripts/verifyArtArchiveIngestionControls.mjs (registered as test:art-archive-ingestion-controls and added to contract-tests.yml), which asserts the store owns both fetches, the page makes no direct API call, and the write endpoint is never one click away.
Merged kind_robots#2923. artArchiveStore gained runDryRun()/runImport(); pages/admin/art-archive.vue gained the 'Ingest from the media server' panel with a dry- run-first, confirm-then-write Import. Contract pinned by utils/scripts/verifyArtArchiveIngestionControls.mjs (test:art-archive-ingestion- controls, wired into contract-tests.yml). Verified before push: new contract test, eslint, vue-tsc --noEmit, test:layout-contract, test:disabled-affordances all clean. t-041 is now unblocked and waiting on Silas.
<!-- note:end t-040 -->

## t-042 — Fix archive previews and owner-controlled private/mature visibility in the main Gallery

<!-- note:begin t-042 -->
Filed from Silas's 2026-09-22 Gallery report. Imported private ArtImages are currently rendered from their PRIVATE_PATH-relative ArtImage.path as if it were under public/images, so the request 404s and image-card falls back to backtree.webp. Serve archive-backed ArtImage bytes through an authenticated, root-confined owner/admin media route and make image-card use that route for designer=art-archive rows. On the Gallery front, use the real persisted maturity consent toggle and add an independent Private toggle that includes the signed-in viewer's own private collections/images without exposing somebody else's private rows. Both toggles must filter collection cards and images consistently and maturity changes must refresh server-backed lists consistently.

Implementation is on kind_robots branch worker/art-archive-t-042-20260923t055430z. It adds an access-filtered PRIVATE_PATH archive media route, routes art-archive image cards through cached previews, replaces the Gallery's local maturity checkbox with the persisted maturity control, adds an owner-scoped Private toggle, covers mature image cards, refreshes Gallery data after maturity changes, and extends the maturity/privacy contract test.

Pass 1 failed (quality) on kind_robots#3007 exact head 10f6654cac44cba80ad3c147fab47ec8de8c7c65. Content Visibility Coverage run 35825635576 fails because the new capability-authorized ArtImage read is not recognized by the repository-wide visibility verifier; Contract Tests run 35825635538 also fails the Prettier ratchet. Retry must preserve the signed capability design while teaching the visibility contract to prove that narrow authorization (without allowlisting the route), add regression coverage that an unguarded ArtImage read still fails, format touched files, and rerun actual CI checks. Reviewer session openai-scheduled-2026-09-23T062035Z-art-archive-pr3007-a11.

Pushed kind_robots#3007 ce9692d: taught verifyContentVisibilityCoverage.ts to recognize
verifyGalleryArchiveMedia() as a per-object capability check (privacy+maturity), added a
regression test against the scanner's own classifier, and formatted the 3 files the
Prettier ratchet flagged. Local verification: vue-tsc clean, eslint ratchet unchanged
(330, same as CI), prettier ratchet holds (no directory worse), full test:contracts-db-
free green (394/394). Awaiting fresh CI on the pushed commit.

kind_robots#3007 merged (squash d8bd56e). Fixed CI on the pushed retry:
verifyContentVisibilityCoverage.ts now recognizes verifyGalleryArchiveMedia() as a per-
object capability check (both privacy and maturity), with a regression test
(verifyContentVisibilityCoverage.test.ts) pinning that an unrecognized/absent check
still fails; also formatted the 3 Prettier-ratchet-flagged files. All 53 kind_robots
checks green (including Contract verifiers), squash-merged.
<!-- note:end t-042 -->

## t-043 — Reconcile the two independent signed archive-media capability schemes from kind_robots#3006 and #3007

<!-- note:begin t-043 -->
Kaizen from t-042. #3007 (ArtImage/owner Gallery-oriented, merged as d8bd56e) and #3006
(ArchiveEntry/admin-oriented, still open as of this task's filing) each independently
built their own signed-capability-URL mechanism for the same underlying problem: an
authenticated JSON response minting a short-lived HMAC-signed URL so a plain <img> can
load PRIVATE_PATH-backed bytes without headers. #3007's landed first, so #3006 will need
to rebase onto main and now sits next to a second, differently-shaped implementation of
the same idea (artGalleryArchiveMedia.ts's id+variant+expiry scheme vs #3006's
entry-id+variant+expiry scheme gated on admin+mature). Read both once #3006 either merges
or is closed, and either consolidate onto one shared signing helper (both are HMAC over
id:variant:expiry with a derived key) or document precisely why they must stay separate
(different auth model: owner-of-row vs admin-only). Whichever wins, the loser's dead code
should be removed rather than left to double the surface a future security review has to
reason about.

Reconciliation verified 2026-09-23 (conductor scheduled Agent run): #3006 merged
(squash, merged_at 2026-09-23T07:56:48Z) and its own diff already performs exactly the
consolidation this task asked for -- it extracted a single shared
server/utils/signedMediaCapability.ts primitive
(deriveMediaSigningKey/signMediaCapability/verifyMediaCapability) and rebuilt both
server/utils/artArchiveSignedMedia.ts (admin+mature over ArchiveEntry, KEY_LABEL 'kind-
robots/art-archive-media/v1') and server/utils/artGalleryArchiveMedia.ts (#3007's owner-
of-row over ArtImage) on top of it, each keeping its own key label so a signature for
one domain cannot replay against the other -- the 'different auth model' case this
task's note allowed for, but the code was consolidatable after all: same HMAC, different
labels, not two authorization models needing separate crypto. #3006 also removed the
duplicate attacher module (server/utils/artArchiveMediaPaths.ts, referenced only as a
forbidden pattern now) so all three archive-rendering endpoints
(server/api/art/image/index.get.ts, server/api/art/image/[id].get.ts,
server/api/art/collection/index.get.ts) route through the one shared
attachGalleryArchiveMediaPaths helper. utils/scripts/verifyArtArchiveSignedMedia.test.ts
(added in #3006, registered in package.json + contract-tests.yml, part of the PR's green
CI) directly enforces 'ONE implementation, TWO key domains' and 'ONE attacher, not two',
including asserting artArchiveMediaPaths.ts no longer exists. Independently confirmed
against live kind_robots@main: server/utils/ listing shows signedMediaCapability.ts +
both domain files present and artArchiveMediaPaths.ts absent; a repo-wide code search
for the old duplicate attacher name (attachArchiveMediaPaths) returns zero hits outside
the contract test's own negative assertion. No further code change needed -- closing as
done rather than opening a redundant PR.
<!-- note:end t-043 -->
