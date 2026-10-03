# Survey: reusable Kind Robots parts for the comic maker (t-003)

date: 2026-10-03
scope: read-only survey of silasfelinus/kind_robots at main 909f548, for both surfaces this project now has:
the public free-to-play maker (`/play/comics`, t-004 to t-012) and Silas's admin Comic Studio
(`/play/comics/studio`, t-013 and t-014).

## Art generation

- Every render goes through durable ArtJobs, `POST /api/art/enqueue` (`server/api/art/enqueue.post.ts`).
  It already builds correct graphs per lane:
  - `comfy` + `checkpoint` (SDXL, Illustrious, Pony) with family sampler profiles from `utils/checkpointProfiles.ts`;
  - `zimage`, `krea2`, `flux`, `flux2`;
  - source-image lanes: `kontext`, `sdxl-img2img`.
- Admin callers are free (`server/utils/manaGate.ts`).
- Server-side callers use `event.$fetch('/api/art/enqueue')` with the caller's auth. Precedents: `server/utils/musicVideoScenes.ts`, `server/api/mandarin/requests/[id]/art.post.ts`.
- Status is a batch read of ArtJobs by id (`syncSceneJobs`).
- Requeueing reuses the same ArtJob (`server/api/art/queue/[id]/requeue.post.ts`).
- Conductor's `consume_art_queue.py` only knows krea2, flux and flux2-klein, and aliases `sdxl` to krea2. Non-Krea A/B ledgers go through `scripts/enqueue_art_requests.py`, which calls the enqueue route.
- The render box Resource registry (`GET /api/resources`) lists 53 checkpoints. SFW lanes that suit this comic:
  - `Illustrious/furrytoonmix_xlV3`, `Illustrious/realismIllustriousBy_v55FP16`
  - `SDXL/sdxlUnstableDiffusers_nihilmania`, `SDXL/RealitiesEdgeXLLIGHTNING_TURBOV7`
  - `Pony/realcartoonPony_v1`
  - Z-Image Turbo
  - Flux Kontext (consistency edits)

## Images

- Rendered images are ArtImages served by Kind Robots (round 2 lives under `/images/projects/comic-creator/...`).
- Private images need signed thumbnails: `galleryThumbnailUrl()` in `server/utils/artGalleryArchiveMedia.ts`, served by `server/api/art/image/[id]/thumbnail.get.ts` (480px WebP).

## Surfaces and registration

- A new page needs a channel tab with an exact `route:` (`content/channels/<channel>/<tab>.md`). `utils/scripts/verifyNoHiddenRoutes.ts` fails hidden pages.
- Admin tabs use `requiredRole: ADMIN`; precedent `content/channels/admin/aquarium.md` for `/play/aquarium`.
- New pages also need a `utils/dataSurfaceManifest.ts` entry.
- Layout contract (`utils/scripts/verifyLayoutContract.ts`):
  - `kr-surface` root;
  - one scroll strategy;
  - no `<h1>`;
  - container-width grids in shared components.

## Editor building blocks

- No drag-and-drop, canvas or PDF library in `package.json`.
- The in-repo drag pattern is native HTML5 drag for mouse, pointer events with `elementFromPoint` for touch, and buttons for keyboard (`components/narrative/narrative-role-assigner.vue`).
- Recommendation: no new drag dependency. Page layout is CSS geometry from a shared pure layout engine (`utils/comicLayouts.ts`, built for the studio and reused by t-004).

## Persistence

- The public maker stays client-only (IndexedDB plus JSON backup), per the approved design brief.
- The studio stores its data in Kind Robots MariaDB tables (`prisma/comic-studio.prisma`, additive migration).
  - This is deliberately not the coloring studio's Conductor-YAML-over-GitHub backend, which Silas does not want repeated.

## Recommendations still open for the public maker

- **PDF:** a hand-rolled single-image-per-page PDF writer, or `pdf-lib` if bundle budget allows (check `pwa-precache-budget.yml`).
- **Stickers:** transparent WebP, 1024px longest side, with a JSON manifest recording prompt, lane and seed.
