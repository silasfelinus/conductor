# Scene Animator — Design Brief

## What it is

Scene Animator is an admin production tool for turning a directory of still scene images into short generated clips without hand-authoring motion prompts image by image.

The operator selects a source folder, chooses a Kind Robots video preset and clip duration, sets maturity, and starts or resumes the batch. Scene Animator supplies one conservative scene-preserving motion instruction automatically and delegates rendering to the existing Kind Robots video path.

## Product rule

**The image is the prompt.** The automation should not invent a new story for each still. Its fixed motion instruction asks the video model to preserve composition, subject identity, lighting, and visual style while adding plausible ambient motion and stable camera movement.

The default automatic prompt is intentionally generic and inspectable:

> Bring this still scene naturally to life with subtle coherent motion. Preserve the subjects, composition, identity, lighting, and visual style. Add only plausible ambient movement, gentle secondary motion, and stable cinematic camera behavior. Do not introduce new characters, objects, text, or scene changes.

## Existing machinery to reuse

Do not build another renderer or browser-owned queue.

```text
Scene Animator admin surface
  -> Scene Animator store/API orchestration
  -> /api/video/generate
  -> /api/art/enqueue
  -> durable ArtJob
  -> kr-relay
  -> existing LTX/WAN Comfy workflow
  -> ArtImage
  -> existing image offload/media URL behavior
```

`utils/videoPresets.ts` remains the preset authority. LTX and WAN remain the video engines. Existing ArtJob retry, mana gating, maturity flags, completion provenance, and ArtImage storage rules continue to apply.

## Source storage

Source stills are deliberately separate from generated-image storage.

Preferred production layout:

```text
/mnt/user/pc/kindrobots/animate/
  project-a/
    scene-001.webp
    scene-002.png
  project-b/
    shot-01.jpg
```

Environment contract:

- `ANIMATE_PATH` — filesystem root available to the self-hosted Kind Robots server.
- `ANIMATE_MEDIA_ORIGIN` — optional browser/public origin for source previews when the media server exposes the sibling tree.
- Development may fall back to an `animate/` directory under the repository only when the explicit source root is absent; it must never silently write seed files into `public/images`.

The API accepts only normalized relative folder/file names under the configured root. No `..`, absolute paths, symlink escape, or arbitrary server filesystem browsing.

## Durable progress without a second batch database

ArtJobs are the progress ledger. Each generated clip carries a small `sceneAnimator` provenance block containing:

- source folder
- source filename
- source content hash
- video engine and preset
- duration/FPS/size/output format
- maturity setting
- deterministic dedupe key

The dedupe key is derived from the source hash plus effective render settings. Folder status is reconstructed from these ArtJobs:

- **missing** — source exists, no matching job
- **queued/rendering** — matching PENDING/RUNNING job
- **done** — matching DONE job with result ArtImage
- **failed/cancelled** — matching terminal job may be explicitly retried

This makes Resume idempotent across browser refreshes and app restarts. Changing the source bytes or effective settings deliberately creates a new key and therefore a new generation.

## MVP admin surface

The first useful page should provide:

1. Source-folder picker rooted only at the animation source tree.
2. Image contact sheet with per-source status.
3. LTX/WAN engine and existing preset picker.
4. Clip duration control; preset fills the rest of the render settings.
5. Maturity toggle. Generated clips default private because this is an internal production tool.
6. Start/Resume action that queues only missing work.
7. Progress counts for total, missing, active, done, failed.
8. Result gallery with source still next to/playable generated clip and ArtJob ID.

No per-image prompt editor in the primary workflow. Advanced/manual prompting remains the existing `/play/video-generator` tool.

## Safety and operational boundaries

- Admin-only UI and server routes.
- No recursive access outside `ANIMATE_PATH`.
- No external publishing or automatic social/gallery promotion.
- No filesystem deletes or source mutation in the MVP.
- Reuse existing ArtJob and mana rules rather than bypassing them for admin convenience.
- A container bind mount or media-nginx route for the new sibling folder is infrastructure configuration and should be documented/tested separately from the reversible app code.

## Definition of done

A batch can be selected, queued, the browser can be closed, and on return Scene Animator accurately shows which stills are complete and queues only the remaining stills. Generated results play in the admin gallery and remain traceable to source file, render config, ArtJob, and ArtImage.
