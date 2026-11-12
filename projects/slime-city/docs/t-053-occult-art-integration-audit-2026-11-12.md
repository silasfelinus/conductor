# Meat Exchange occult art: integration readiness audit

2026-11-12 PT · Conductor slime-city/t-053 · session `2026-11-12T090700Z-slime-city-t053-a8c4`

## Verified source state

- `projects/slime-city/art/EXCHANGE-OCCULT-ROUND-1.yaml` contains **103 unique subjects**: **40 card plates** and **63 evolution plates**.
- All 103 subjects have a recorded `status: DONE` and nonempty `art_image_id`, numbered **269792–269894**. No subject in this ledger is marked pending or failed.
- None of those 103 new ArtImage IDs is present in Kind Robots `utils/slimeCity/artManifest.ts` at the time of this audit.
- This is a **ledger completion** audit, not authenticated image-byte verification or artistic approval. The manifest's own header explicitly prohibits treating DONE as proof of usable art.

## Why it matters

The playable Exchange identity was rewritten in PRs #5000, #5015 and #5027, but the runtime still selects earlier artwork. Merely replacing 103 manifest numbers would risk shipping uncaught lettering, incorrect characters, framing, or unsuitable renders. It would also replace fallback/previously curated art with unreviewed images.

## Safe integration procedure

1. Fetch each ArtImage through the authenticated image endpoint, verifying that the image bytes are returned successfully.
2. Build a labeled contact sheet of all **40 base card** and **63 evolution** plates, matching `asset` to the runtime key. Inspect the images and mark each **keep / redo / reject** with a reason. Prioritize base cards for an independently shippable first pass.
3. Update only **kept** subjects in `utils/slimeCity/artManifest.ts`, retaining existing IDs for rejected/redo subjects. Verify no duplicate assets or wrong evolution stages.
4. Add an automated manifest/ledger coverage test for curated keepers; run TypeScript, formatting, relevant tests, and preview checks. Open PR and merge only after complete successful CI.
5. Record rejected ArtJob/ArtImage IDs in the existing art ledger and requeue via the existing pipeline rather than inventing replacement images.

## Evidence links

- [Art ledger](https://github.com/silasfelinus/conductor/blob/main/projects/slime-city/art/EXCHANGE-OCCULT-ROUND-1.yaml)
- [Runtime art manifest](https://github.com/silasfelinus/kind_robots/blob/main/utils/slimeCity/artManifest.ts)
- [Canonical Slime City roadmap](https://github.com/silasfelinus/kind_robots/issues/4535)

**Remaining gate:** authenticated image fetch and visual curation. No new image generation or production publishing is authorized by this audit.
