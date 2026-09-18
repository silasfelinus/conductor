# Art Archive - Design Brief

## Purpose

Art Archive turns a pre-Kind-Robots filesystem of AI-generated images into a
durable, searchable, safely private part of Kind Robots without requiring the
source collection to be reorganized first.

The source folder is living storage, not a one-time migration dump. Silas should
be able to drop images or entire nested folders into it, rescan/reconcile, and
see new material appear in the archive without creating duplicate database rows
or losing prior curation work.

## Non-negotiable privacy boundary

Every file discovered through this archive pipeline is treated as mature and
private unless Silas explicitly changes that ArtImage later through some other
intentional workflow:

- ArtImage.isPublic = false
- ArtImage.isMature = true
- folder-derived ArtCollection.isPublic = false
- folder-derived ArtCollection.isMature = true

Resource provenance NEVER changes those values.

A harmless/SFW LoRA or checkpoint may have been used to generate explicit art.
Therefore "this ArtImage is linked to an SFW Resource" is metadata, not evidence
that the output is safe. Conversely a mature Resource does not need any special
visibility logic here because the archive image is already on the restrictive
side of the boundary.

Ordinary Resource galleries must not gain a reverse-display path that surfaces
linked archive images. The link answers "what produced this image?", not "show
every image ever produced with this Resource to everyone browsing the Resource."

The admin archive itself should require both admin authorization and an account
that is allowed to display mature content. Admin capability is not a maturity
override.

## Existing infrastructure to reuse

The current Kind Robots data model already supplies most of the destination:

- ArtImage has isPublic, isMature, imagePath/path/fileName, promptString,
  negativePrompt, seed, cfg, sampler, steps, checkpoint,
  checkpointResourceId, and related generation fields.
- ArtImage has the LoraResources many-to-many relation.
- ArtCollection already owns many-to-many ArtImages and has parentFolder,
  isPublic, isMature, slug, label, and imagePath.
- server/api/art/utils/resourceProvenance.ts already resolves active
  CHECKPOINT/LORA/LYCORIS Resources conservatively by id or exact
  localPath/name/customLabel. The archive matcher should build on that behavior
  rather than create incompatible Resource semantics.
- Durable new generation already belongs in ArtJob. Archive regeneration should
  adapt imported ArtImage provenance into normal ArtJob requests.

What is missing is persistent filesystem-ingestion state. ArtImage should stay
the image/content object; it should not become a filesystem crawler journal.

## Archive ledger

Add one small first-class archive-entry/index model. Exact naming is an
implementation choice, but its job is narrow:

- identify a source file by strong content hash;
- remember current relative path under the configured archive root;
- keep cheap size/mtime hints for incremental rescans;
- link to the imported ArtImage;
- link/identify the folder-derived ArtCollection;
- remember processed/review state;
- persist a 1-5 archive rating;
- retain extracted raw metadata and Resource-match evidence/candidates;
- distinguish automatic matches from manually confirmed/locked provenance;
- mark missing/trashed state without deleting history.

Structured diagnostic payloads should follow Kind Robots' existing serialized
LongText/string convention rather than adding native JSON columns.

The ledger is not a replacement image catalog. It exists so deleting, moving,
renaming, rescanning, or temporarily losing a file does not erase the fact that
Silas already reviewed it.

## Folder to ArtCollection mapping

The immediate containing folder of each source image is its folder-derived
ArtCollection label.

Example:

    archive/
      old-renders/
        vampires/
          session-4/
            image.png

The folder-derived collection label is "session-4".

Because identical folder names can occur in different branches, collection
identity must also retain the full relative folder path, using ArtCollection's
parentFolder or an equivalent stable path field. Slugs should therefore be
path-aware, not globally derived from the basename alone.

Folder-derived membership is automatic. Custom ArtCollection membership is
additional and may overlap it.

Moving a file through the admin UI updates its folder-derived membership but
does not remove custom collection memberships.

## Reconciliation model

A complete recursive scan is the authoritative discovery mechanism. Filesystem
watch events may accelerate discovery later, but correctness must not depend on
network-share watcher behavior.

A scan should:

1. walk supported image files beneath the configured root only;
2. reject path traversal/symlink escapes;
3. capture relative path, immediate parent folder, size, and modification time;
4. reuse an unchanged ledger row when cheap file metadata is unchanged;
5. hash bytes when needed to establish content identity;
6. extract embedded generation metadata;
7. compare with prior ledger state;
8. propose database/file changes;
9. apply only through an explicit reconciliation step.

A newly observed path with a hash matching a now-missing prior path is a likely
move. The scanner may suggest that interpretation but should remain careful when
both paths still exist, because that is a copy, not a move.

Missing files are marked missing first. The scanner never automatically deletes
ArtImages or filesystem data.

## Legacy metadata extraction

The archive predates one consistent generation pipeline, so extraction should
be opportunistic and evidence-preserving.

Useful sources include:

- A1111 PNG "parameters" text;
- A1111 <lora:name:weight> prompt tokens;
- Comfy prompt/workflow metadata and loader node filenames;
- checkpoint/model name fields;
- prompt, negative prompt, sampler, scheduler, seed, steps, CFG;
- EXIF/text metadata where present;
- filename and directory names as low-confidence hints.

Raw metadata should remain inspectable even if parsing fails.

## Resource matching

Only active Resource rows with compatible types are eligible.

Confidence order:

1. explicit current Resource id, if valid;
2. exact localPath/name/customLabel match;
3. exact normalized basename match after stripping known model extensions;
4. exact model/LoRA name extracted from A1111 or Comfy metadata;
5. known alias/trigger evidence where unambiguous;
6. filename/folder hints;
7. fuzzy similarity as candidate generation only.

Auto-link only unique, defensible matches. Ambiguous or fuzzy matches belong in
an admin review queue with evidence.

Manual selections win forever until Silas explicitly unlocks them. A later
rescan must never "improve" a human correction away.

## Admin surface

This belongs inside the existing admin navigation, not a new top-level channel.

The main view should combine:

- a nested folder browser;
- ArtCollection selection;
- image grid with useful thumbnails;
- processed/unprocessed toggle;
- resource-match status filter;
- 1-5 rating filter;
- missing/trashed filter;
- search;
- multi-select;
- image detail/editor.

The detail editor should expose both extracted evidence and editable canonical
ArtImage provenance: prompt, negative prompt, checkpoint Resource, LoRA
Resources, common generation settings, folder/custom collections, rating, and
processing state.

## File operations

Every filesystem mutation is admin-only and root-confined.

Move:
- move within the configured archive root;
- update the ledger path;
- update folder-derived ArtCollection membership;
- preserve custom collections and manual resource choices.

Delete:
- the normal UI action moves the file to an archive-local trash area;
- mark the archive entry trashed and the linked ArtImage inactive as appropriate;
- retain enough history to undo or explain the action;
- permanent purge is a separate explicit action if it is added at all.

Automatic scanning never moves or deletes files.

## Curation board and action presets

Silas should be able to select or drag one/many images onto visible action
targets. Built-in targets include:

- Rate 1, 2, 3, 4, 5
- Delete / trash
- Add to collection
- Mark processed / unprocessed

Persisted generation presets can add targets such as:

- regenerate with additional LoRA X;
- remove/replace LoRA X;
- switch checkpoint;
- append prompt fragment;
- replace prompt fragment;
- change CFG/steps/sampler/seed behavior;
- generate an additional variant;
- generate a replacement candidate.

Presets describe changes to a normal ArtJob request. They do not create a
second generation queue.

## Imported image regeneration

Imported ArtImages may have no source ArtJob. A narrow archive adapter should
construct a new ArtJob from the ArtImage's stored generation metadata and
Resource provenance, then apply the chosen preset.

"Additional generation" keeps the source untouched.

"Replacement" is two-phase:
1. generate and verify the replacement ArtImage;
2. only then swap archive/canonical references and move the old source to trash
   if that is what the preset says.

A failed render must never destroy the source image.

## Scaling assumptions

Treat the collection as large from the beginning.

- Paginate database reads.
- Render thumbnails in grids, not original files.
- Bound scanner hashing and metadata parsing concurrency.
- Skip content hashing when a trusted ledger row has unchanged path/size/mtime,
  then periodically/auditably revalidate hashes.
- Make scans resumable and observable.
- Avoid loading an entire directory tree's originals into browser memory.
- Surface scan/import counts and partial failures.

## Production root

The archive path is configuration, not code. Do not hardcode a workstation or
Unraid absolute path.

The production container will need an explicit read/write mount for the chosen
media-server directory. Code work can proceed against a configured root before
that host-level mount is approved. The actual production mount remains a human
gate.

## Definition of done

The project is done when Silas can add nested folders/images to the archive and
Kind Robots reliably discovers them, imports them as mature/private ArtImages,
creates/reuses folder collections, recovers trustworthy checkpoint/LoRA
provenance where possible, remembers curation state across rescans and moves,
and provides an admin-only visual workspace for reviewing, rating, moving,
trashing, collecting, editing, and regenerating archive art at large-library
scale without leaking it into ordinary SFW browsing.
