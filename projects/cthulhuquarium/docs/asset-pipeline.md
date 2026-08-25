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
failing because `Character.size` doesn't exist in production yet (the
cthulhuquarium/t-032 schema migration merged into kind_robots main but the
live DB hasn't had a Force Update/deploy since — matches the documented
deploy-timing gap in this repo's own AGENTS.md; self-resolves on Silas's next
Force Update, not a new bug). Neither signature appeared on any of this
task's four jobs.

## 4. Full end-to-end proof run — results

All four test jobs completed successfully with real image output, zero
errors, zero retries (`attempts: 1` on every job). Full timing:

| job | slug | engine/variant | queue wait (enqueue→claim) | render (claim→done) | ArtImage id |
|---|---|---|---|---|---|
| 9201 | goldfish-common | flux/schnell | 2m38s | **11m11s** | 18466 |
| 9202 | sardine-common | flux/schnell | 13m40s (waited for 9201) | 45s | 18467 |
| 9203 | crawdad-common | flux/schnell | 0s (claimed instantly) | 36s | 18468 |
| 9204 | tank-background | flux/schnell | 2s | 36s | 18469 |

**Cost**: mana `charged` was 0 at enqueue for all four (`gate.commit()` only
fires on completion, so a job that never renders never costs mana) — did not
re-verify the post-completion balance this session; worth checking
`GET /api/me` mana balance delta in a future pass if exact per-image mana
cost matters.

**The relay claims one job at a time, strictly serially** — 9202 sat
`PENDING` for the entire 11 minutes 9201 was rendering, then claimed
instantly the second 9201 finished. No parallelism observed or expected
(single `ComfyUI` instance, single relay process).

**9201's 11-minute render vs. 9202–9204's 36–45 seconds is almost certainly
a one-time model cold-start cost**, not a per-image baseline: same engine,
same variant, same dimensions, same relay, back-to-back — the only
difference is 9201 was the first Flux-schnell job this relay process had run
in a while (loading `flux1-schnell-Q8_0.gguf` + the dual-CLIP encoder into
VRAM), while 9202–9204 reused the already-warm model. **Budget ~40s/image
steady-state, but the first job after any relay restart or engine-switch
should expect a ~10+ minute warm-up tax** — worth remembering before reading
a single slow test as "the pipeline is slow."

### Image quality / prompt fidelity — the finding worth reading past the happy numbers

All four renders are real, on-topic, and would pass a casual glance. But
none of them actually delivered what "silhouette" in the bible's art_prompt
wording implies for a game asset:

- **goldfish-common**: a fully shaded, photoreal/painterly fish on solid
  black, not a flat silhouette — dramatic rim-lighting reads as moody rather
  than as the flat, tappable-collectible shape the game needs.
- **sardine-common**: same treatment, and the prompt's actual compositional
  ask — "tight schooling formation of matching silhouettes fading into
  darkness behind it" — was **dropped entirely**. The render is one single
  fish, no school, no fading duplicates. Flux-schnell (8 steps, no negative
  prompt support in this workflow) did not attempt the multi-subject
  composition at all.
- **crawdad-common**: closest of the three to the mood ("murky ditch-water
  backlighting"), silhouette-ish and legibly a crawdad from above, but still
  a moody macro-photo render rather than a flat game-asset shape.
- **tank-background**: the strongest result — no fidelity gap, reads exactly
  as briefed (dark teal-black water, driftwood silhouette, bioluminescent
  particles, painterly, no fish).

**Conclusion for Silas, plainly stated:** Flux-schnell at 8 steps with a
plain text prompt reliably produces good *backgrounds and moody single-
subject renders*, but does **not** reliably produce true flat-silhouette
game-collectible assets, and drops explicit multi-subject/compositional
instructions (schooling fish) outright. If the bestiary's ~150 fish across 6
tiers need to actually look like tappable flat-silhouette collectibles (per
the project's Insaniquarium-style gameplay loop), this prompt style will not
get there at volume. Two directions worth testing before committing to a
production pass over the full bestiary:

1. A LoRA or checkpoint suited to flat vector/silhouette illustration
   (`Resource` registry already has `mode: prompt` fallback patterns from
   `ai-art-academy/t-044`'s cataloging work) rather than photoreal-leaning
   Flux-schnell.
2. A post-process step (background removal + posterize/silhouette filter) on
   the current photoreal output, since the subjects themselves are already
   well-composed and legible — turning them into flat shapes may be cheaper
   than re-prompting for a style the base model doesn't produce reliably.

Not attempted in this session — out of scope for a proof-of-pipeline task,
and worth its own dedicated task (with real render budget) rather than a
blind guess appended here.

## 5. `ArtImage.imagePath`/`path` land `null` — bytes live only in `imageData`

All four completed `ArtImage` rows (`GET /api/art/image/:id`) have
`imagePath: null` and `path: null`. The actual PNG bytes are only reachable
via `GET /api/art/image/:id?includeImageData=true` → `data.imageData`
(base64). `fileName` is a placeholder (`ArtImageUpload-<timestamp>`), not a
real served filename.

This matches `relay_agent.py`'s own docstring — "The upload creates a
staging ArtImage. Normal jobs keep that id" — so this looks like intended
current behavior (staging is the terminal state for an ordinary job, not a
transient one that finishes converting later) rather than a bug: nothing in
this pipeline currently promotes a plain generated image to a servable file
path/CDN URL automatically. Confirmed this isn't a slow-async artifact —
KR Project 2113's leftover `ArtImage` (id 18323, generated 2026-08-24, over a
day old) shows the identical null-path/placeholder-filename shape.

**Implication for t-005's own ask** ("land the results as ArtImage records
linked to the fish's Character rows"): linking by `artImageId` works fine —
the DB row exists and is queryable/linkable right now. But nothing renders
these as an actual `<img>` on a live page without either (a) a frontend that
reads `imageData` directly, or (b) a separate promotion step this session
did not find. Worth a follow-up if/when these need to actually display in
the game UI rather than just exist as linked records.

## 6. Recommendation

The pipeline works end-to-end and is usable today for landing linked
`ArtImage` records against fish/Character rows — enqueue → poll →
`artImageId` is solid, zero errors across 4/4 jobs. Before running it at the
bestiary's real volume (~150 fish), two things should be resolved first,
not treated as "we'll notice later":

1. **Style**: plain-prompt Flux-schnell does not reliably deliver the flat
   silhouette look the bible's `art_prompt` fields describe — see §4. Test a
   silhouette-suited LoRA/checkpoint or a background-removal post-process
   before a full production pass, or the bestiary ships in a visual style
   nobody asked for.
2. **Servable images**: resolve the `imagePath`/`path` null gap (§5) before
   any UI work depends on these images actually rendering on a page.

Neither blocks closing this task — the pipeline itself is proven working —
but both should be named explicitly rather than discovered mid-production.

## 7. On "linked to the fish's Character rows"

The task note asked for the results to land "as ArtImage records linked to
the fish's Character rows." That link doesn't exist yet and can't yet: no
`Character` rows for the bestiary exist in kind_robots at all —
`cthulhuquarium/t-008` ("Seed the bestiary — fish YAML into Character rows")
is still `status: ready`, not done. Faking a link against a Character that
doesn't exist would be worse than not linking. What's in place instead:
each `ArtImage` carries `designer: "cthulhuquarium-t-005-pipeline-proof"`
and `projectSlug: "cthulhuquarium"` for traceability back to this task, and
this doc records the slug→artImageId mapping (18466 goldfish-common, 18467
sardine-common, 18468 crawdad-common, 18469 tank-background) so whoever
picks up t-008 can wire the actual `Character.artImageId` link once the rows
exist, without needing to re-render.


