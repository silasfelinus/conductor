# lora-ingestion/t-003 — Resource-backed generation evidence

Date: 2026-08-10
Session: `20260810T093057Z-lora-t003-a50cb6`

## Question

Has the watched-folder → Resource → `Resource.localPath` → ArtJob → ComfyUI path been proven end-to-end strongly enough to close lora-ingestion?

## What is already proven

### Import and Resource registration

The import half was verified live on 2026-07-28: `ume_classic_impressionist` was detected as Flux, moved into the organized LoRA tree, and registered as a Kind Robots Resource (`created: 1`). The project roadmap records this as the completed half of t-003.

### Resource-localPath is now the application source of truth

Later Kind Robots work repaired the original path-loss class in several layers:

- PR #1090 resolves selected LoRAs through accessible active Resource rows before building Kontext, Krea2, Flux2, LTX, and WAN workflows. An explicit Resource selection replaces a stale caller-supplied name with the Resource's exact `localPath` and records both Resource identity and resolved path in ArtJob provenance.
- PR #1136 removed the Art Styler's legacy `FLUX/` prefix behavior and uses the matched Resource's real `localPath`.
- PR #1163 refreshes stored ArtJob LoRA selections from the current Resource on re-enqueue, updating workflow loader values and provenance together rather than replaying a stale serialized path.

PR #1163's regression fixtures preserve two concrete production-derived cases:

- ArtJob 2615 / Resource 4082 → `Flux/SFW/ume_classic_impressionist.safetensors`
- ArtJob 2621 / Resource 1300 → `Kontext/SFW/manuscript_illustration_kontext.safetensors`

That is strong evidence that Resource identity now survives through enqueue/retry code and resolves to a subfolder-qualified path.

## What is not yet proven

I could not find durable GitHub or Conductor evidence that either of those Resource-backed jobs later reached `DONE` and produced an ArtImage. `RENDER-BACKLOG.md` records ArtJob 2615 as pending on 2026-07-27 and later records the shared queue draining to zero, but its aggregate queue snapshots do not identify the terminal state of job 2615. A later empty queue therefore cannot safely be treated as proof that this specific job succeeded; it might also have failed or been cancelled.

The current AI Art Academy t-044 evidence also shows that Resource path correctness and ComfyUI acceptance are separate layers: recent Kontext jobs can still fail with `lora_name not-in-list` even after Kind Robots resolves the intended Resource path. That does not invalidate the Resource-authoritative fixes, but it means code-level path resolution alone is not an end-to-end render proof.

## Current conclusion

**The original application-side path bug appears fixed, but lora-ingestion's final end-to-end success criterion is not yet durably proven.** Closing the project from repository evidence alone would overstate what was verified.

The next verification should be exactly one current smoke render using an active Resource-backed LoRA on a supported Krea2/Flux2 path, then record:

1. Resource id and exact `localPath` selected at enqueue;
2. ArtJob id and terminal `DONE` state;
3. resulting ArtImage id/path;
4. enough payload/provenance to show the loader used that Resource path.

Do not repeat historical naming-convention guesses. If the smoke fails, preserve the exact ComfyUI loader rejection so the remaining failure can be assigned either to Resource/path resolution or to the backend model inventory.

## Limitation in this run

`KR_API_TOKEN` is not available in the current execution environment, so I did not queue a production ArtJob merely to manufacture evidence. The repository evidence above is read-only and leaves production unchanged.
