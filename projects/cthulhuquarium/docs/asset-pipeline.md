# Cthulhuquarium asset pipeline — what actually works (t-005)

Date: 2026-08-25
Task: cthulhuquarium/t-005 — "Prove the Comfy asset pipeline end-to-end for game art"

---

## TL;DR

The two endpoints the task note named (`POST /api/comfy/flux/generate`,
`POST /api/art/generate`) are **not the current path** — one is architecturally
broken in production, the other doesn't have a matching server type. The
actual, current pipeline is:

```
POST /api/art/enqueue  (engine: "flux")   ArtJob created, status PENDING
        |
        v  (home relay agent polls, claims, renders, uploads)
GET  /api/art/queue/:id                    poll until DONE/FAILED
        |
        v
GET  /api/art/image/:artImageId            fetch the saved ArtImage
```

This is documented architecture (`projects/art-generator-connect/docs/pipeline-architecture.md`,
2026-07-05) and matches the source comments in kind_robots — this task just
confirms it's still the live shape and records what a caller outside the
home network actually experiences.

## 1. `/api/comfy/flux/generate` — dead end from outside the tailnet

`server/api/comfy/flux/generate.post.ts`'s own header comment says it plainly:

> Direct/relay-only synchronous Flux render. Dials the Comfy server inline,
> so it only works from a caller on the home tailnet (relay agent or on-box
> tool). The browser enqueues via /api/art/enqueue instead.

Confirmed live: a JWT-authed POST from this sandbox (no tailnet access)
returns instantly (~0.4s) with `400 {"message":"fetch failed"}` — the route's
inline `fetch()` to the Comfy box (`https://ferngrotto.foxhound-chicken.ts.net`)
never resolves/connects from outside the tailnet. `server/api/comfy/kontext/enqueue.post.ts`
independently documents the same failure mode: "the deployed backend is not
on the home tailnet (ENOTFOUND on ts.net names)." `docs/art-api.md` (dated
2026-06-30) still documents this as the recommended Flux path — it's stale
and should be corrected to point at the enqueue lane instead.

## 2. `/api/art/generate` — no A1111 server registered

This route is A1111-only. The one image server currently registered
(`GET /api/server`, id 96, title "Comfy") is `serverType: COMFY`, so the call
fails immediately: `400 {"message":"Server \"Comfy\" is COMFY. This route only
supports A1111 txt2img servers."}`. There is no A1111 server in the registry
to test this endpoint against at all right now.

## 3. The real path: `/api/art/enqueue` + home relay agent

### Auth

Standard session JWT, `Authorization: Bearer <token>` — the same
`KR_API_TOKEN` used everywhere else in this repo (`scripts/kr_token_set.sh`).
Works for enqueue and for polling.

### Request (what was actually sent)

```json
{
  "engine": "flux",
  "promptString": "<fish or background art_prompt from the bible>",
  "variant": "schnell",
  "width": 768,
  "height": 768,
  "isPublic": true,
  "designer": "cthulhuquarium-t-005-pipeline-proof",
  "projectSlug": "cthulhuquarium"
}
```

`engine: "flux"` builds a Flux-schnell GGUF workflow
(`buildFluxWorkflowFromRequest`) — 8 steps, `flux1-schnell-Q8_0.gguf` unet,
`t5-v1_1-xxl-encoder-Q5_K_S.gguf` + `clip_l.safetensors` dual-CLIP, no LoRA.
`variant: "dev"` is available for slower/higher-quality renders; not tested
here to keep the proof run fast.

### Response — enqueue (201, synchronous, instant)

```json
{
  "success": true,
  "message": "Art job queued. Poll /api/art/queue/:id until DONE.",
  "statusCode": 201,
  "data": { "jobId": 9201, "status": "PENDING", "deduplicated": false, "mana": { "balance": 711, "charged": 0 } }
}
```

Mana is **not** charged at enqueue time — `gate.commit()` only fires on the
relay's completion callback, so a job that never renders never costs mana.
Four jobs enqueued cleanly (three fish + one tank background), job ids
9201–9204, all `PENDING` with `claimedAt: null` immediately after creation —
the enqueue side of the pipeline works exactly as designed, no errors, no
retries needed.

### Poll: `GET /api/art/queue/:id`

Returns the full `ArtJob` row, including the exact ComfyUI workflow graph
that will be submitted (useful for debugging prompt/model wiring without
needing tailnet access at all — this alone is worth the doc: `GET
/api/art/queue/:id` shows you the rendered `KSampler`/`ImpactWildcardEncode`
node graph, so a mis-set model/steps/seed shows up here before spending a
render on it).

### `GET /api/art/queue/stats` — read this before assuming the pipeline is dead

The single most useful diagnostic endpoint for this whole pipeline. No wait
needed — instant JSON snapshot of queue health:

```json
{
  "queueDepth": {"PENDING": 12, "RUNNING": 1, "DONE": 5016, "FAILED": 158, "CANCELLED": 3182},
  "windowThroughput": {"PENDING": 6, "RUNNING": 1, "DONE": 164, "CANCELLED": 3},
  "staleRunningCount": 0,
  "recentFailed": [ /* last 25 FAILED jobs with engine, attempts, error, projectSlug */ ],
  "failuresBySignature": [ /* grouped/counted error signatures */ ],
  "imagesCreatedInWindow": 175
}
```

At the moment this task ran: **the relay agent is alive and actively
rendering** — 164 jobs completed in the trailing 24h, one job `RUNNING` right
when this was checked. The four test jobs sat `PENDING` for a few minutes
(not instantly claimed — `queueDepth.PENDING` was 12 system-wide at the same
moment, i.e. shared with every other project's queued work, not a
cthulhuquarium-specific slowdown) before job 9201 (goldfish) flipped to
`RUNNING` with `claimedBy: "Silas-PC"`. So: **do not read a few minutes of
`PENDING` on a freshly-enqueued job as the pipeline being down** — check
`/api/art/queue/stats` first; a healthy queue with normal depth explains it
far more often than an offline relay.

`recentFailed`/`failuresBySignature` also show this pipeline has real,
already-tracked failure modes unrelated to anything this task touched:
24 of the last 25 failures are `hostbuf_file_reader_read failed` on
`CLIPTextEncode` (facet-catalog project, dated 2026-08-21 — this is the
already-open hard gate `ai-art-academy/t-068`), plus one `dream-cycle` job
failing because `Character.size` doesn't exist in production yet (a schema
migration landed in conductor but hasn't reached the live DB — worth its own
ticket if not already tracked, out of scope here). Neither signature
appeared on any of this task's four jobs.

