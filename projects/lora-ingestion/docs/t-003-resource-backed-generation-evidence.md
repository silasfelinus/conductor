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

## Limitation in this run (2026-08-10)

`KR_API_TOKEN` is not available in the current execution environment, so I did not queue a production ArtJob merely to manufacture evidence. The repository evidence above is read-only and leaves production unchanged.

## 2026-09-05 update — smoke test run, both original jobs confirmed CANCELLED, and Flux2 engine hang found

`KR_API_TOKEN` was available in this session. Confirmed live via `GET /api/art/queue/{id}`:

- ArtJob 2615 (Resource 4082, `Flux/SFW/ume_classic_impressionist.safetensors`): **status `CANCELLED`**, not DONE.
- ArtJob 2621 (Resource 1300, `Kontext/SFW/manuscript_illustration_kontext.safetensors`): **status `CANCELLED`**, not DONE.

So the two jobs this doc's earlier evidence rested on definitively did **not** prove end-to-end success — they never finished at all. This closes the ambiguity the 2026-08-10 note left open.

Separately, also today, `silasfelinus/kind_robots#2416` merged (12:11 UTC) splitting Krea 2 LoRA compatibility from Flux.2's — it was previously possible for a FLUX/KONTEXT Resource to rank as Krea 2-compatible. Relevant to whether a *Krea2* smoke is even possible right now (see below).

### Searched for existing recent evidence before queuing anything new

Scanned the 700 most recent `DONE` ArtJobs (7 pages × 100, `GET /api/art/queue?status=DONE`) for any workflow payload containing both a `LoraLoader*` node and a Krea2/Flux2-family checkpoint (`UNETLoader`/`CheckpointLoader` `unet_name`/`ckpt_name` containing `krea`/`flux2`). **Zero matches.** No Resource-backed Krea2/Flux2 LoRA render has completed recently. Proof was still missing, so per this doc's own instruction, queued exactly one current smoke.

### Krea2 is currently untestable — zero compatible Resources exist

Fetched all 2344 rows from `GET /api/resources` and grouped by `generation`. **Not one Resource anywhere in the library has "Krea" in its `generation` field** (`utils/loraSelection.ts`'s `krea2LoraCompatibilityRank()` requires `generation` to match `/\bKREA[\s._-]*2\b/` or `=== 'KREA'`, gated on `supportedServer` being `COMFY`/`GENERIC`). This isn't a selection-logic bug — the underlying LoRA inventory simply contains no Krea2-tagged resource yet. **A literal Krea2 Resource-backed-LoRA smoke render cannot be run today, independent of agent effort**, until at least one Krea2-generation LoRA Resource is ingested.

### Flux2 smoke: queued, then found the relay hangs on the Flux.2 Klein checkpoint

`artLoraCompatibilityRank()` ranks any `supportedServer: FLUX` LoRA at 30 (highest) for the `flux2` engine — the library has 135 such (Flux.1-trained) LoRAs, all but a couple private. Queued one via the real user-facing endpoint, `POST /api/art/enqueue`:

```json
{"engine":"flux2","promptString":"3D Cartoon Vision FLUX style, a friendly small robot character standing in a colorful workshop, clean 3D render, studio lighting","loraResourceIds":[1055],"isPublic":false,"isMature":false,"designer":"conductor-lora-ingestion-t003-smoke","projectSlug":"lora-ingestion-t003"}
```

→ ArtJob **21616** created, `resources: {loraResourceIds:[1055], loraNames:["Flux/SFW/3D_Cartoon_Vision_flux_v1.safetensors"]}`. Confirmed the enqueued workflow correctly wired a `LoraLoaderModelOnly` node (`lora_name: Flux/SFW/3D_Cartoon_Vision_flux_v1.safetensors`, `strength_model: 1`) onto the `flux2_dev_fp8mixed.safetensors` UNETLoader graph — **Resource→localPath resolution and workflow wiring are correct** at the application layer, same conclusion the repository evidence already supported.

The job sat `PENDING` behind ~3100 queued jobs (this queue drains oldest/highest-priority-first, and the parallel dream-cycle/Krea repair batch runs at priority 50–200); bumped it to priority 250 via `POST /api/art/queue/21616/priority` to get evidence within the session instead of waiting days. Relay (`Silas-PC`) claimed it (`RUNNING`) at 18:46:46 UTC — and then **never completed it or claimed anything else**. `GET /api/art/queue/stats` flagged it under `staleRunning` past the 15-minute threshold; no other job reached `DONE` anywhere in the queue for the ~30 minutes it sat claimed (confirmed: last `DONE` timestamp stayed pinned at 18:46:45, one second before this job was claimed). The relay's single concurrent slot was fully wedged — this blocked the *entire* production render queue, not just this one job.

Cancelled it (`POST /api/art/queue/21616/cancel`) to restore throughput; confirmed `staleRunning` dropped to `[]` immediately after. No ComfyUI-side rejection message was ever recorded (`error: null` throughout) — this was a hang, not a clean loader rejection, so it can't yet be assigned to "Resource/path resolution" vs. "backend model inventory" the way this doc originally hoped a failure would be. Two live candidate explanations, neither confirmed:

1. First-ever use of `flux2_dev_fp8mixed.safetensors`/`mistral_3_small_flux2_bf16.safetensors` on this relay, stuck on a large first-time model load (Flux.2 Klein resources are rare in the catalog — only 3–5 rows total — suggesting this engine sees little live traffic).
2. The `LoraLoaderModelOnly` node choking silently on a Flux.1-architecture LoRA weight file against a Flux.2 checkpoint (these are different, incompatible model generations despite the app's `artLoraCompatibilityRank()` treating `FLUX`-tagged Resources as top-ranked Flux2 matches) — plausible, but a genuine hang rather than a rejection is not the usual signature of a shape mismatch, so this is a guess, not a finding.

### Current conclusion (supersedes 2026-08-10)

Resource-backed **path resolution** into a ComfyUI workflow is solidly proven at the application layer (three independent confirmations now: PR #1163 fixtures, this session's live enqueue, and the two original — if terminally CANCELLED — ArtJobs' payloads). The **execution** half remains unproven for both families, for two different reasons:

- **Krea2**: no compatible Resource exists to test with. Not an agent-actionable blocker — needs at least one Krea2-generation LoRA ingested first.
- **Flux2**: a real, reproduced relay hang on the one engine/LoRA-family pairing tested, serious enough to have stalled the whole render queue for ~30 minutes. This needs investigation on the relay side (ComfyUI/model-availability diagnosis on Silas-PC) before another Flux2 smoke is attempted — repeating the same queue-blocking hang without that diagnosis first would not be a responsible retry.

Recommend: do not close lora-ingestion on Resource-path evidence alone (as before), and do not retry a bare Flux2 smoke without first checking whether `flux2_dev_fp8mixed.safetensors` is actually present/loadable on the relay. Filed as `conductor/t-147` (see roadmap) for that relay-side diagnosis; t-003 itself is soft `needs-human` pending it.
