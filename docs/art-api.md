# Kind Robots Art API — Request and Response Shape

Generated: 2026-06-30
Task: art-generator-connect/t-001

---

## Purpose

Document the kind_robots art generation endpoints for use by the Conductor art-generator-connect pipeline. Covers request fields, auth requirements, response shape, polling behavior, and failure modes so a Conductor wrapper script can call them without ambiguity.

---

## Overview of Endpoints

| Endpoint | Engine | Auth | Polling? |
|---|---|---|---|
| POST /api/art/generate | A1111 (Stable Diffusion) | User API key (Bearer) | No — synchronous |
| POST /api/comfy/flux/generate | ComfyUI Flux (dev/schnell) | User JWT (Bearer) | Yes — poll until done |
| POST /api/conductor/art-request | Art request queue (YAML) | Admin API key | No — fire-and-forget |
| GET /api/art/image/[id] | Read a saved ArtImage | Optional | No |
| GET /api/art/image | List ArtImages (filterable) | Optional | No |

---

## 1. POST /api/art/generate (A1111 Stable Diffusion)

### Auth

```
Authorization: Bearer <user.apiKey>
```

This uses the `apiKey` field on the User record — **not** the standard JWT from `/api/auth/login`. These are different tokens. The user's apiKey is a static long-lived key stored in the DB. If Conductor calls this endpoint, it must hold a valid user apiKey.

Internally: the route calls `prisma.user.findFirst({ where: { apiKey: token } })`. If no user matches, returns 401.

### Request Body

```json
{
  "promptString": "a glowing forest at dusk, watercolor style",   // required
  "negativePrompt": "blurry, low quality",                        // optional
  "steps": 20,          // optional, default 20
  "cfg": 3,             // optional, default 3
  "cfgHalf": false,     // optional; adds 0.5 to cfg if true
  "seed": -1,           // optional, default -1 (random)
  "width": 512,         // optional, default 512
  "height": 512,        // optional, default 512
  "sampler": "Euler a", // optional, default "Euler a"
  "checkpoint": null,   // optional — SD model checkpoint name
  "serverId": null,     // optional — specific server DB id
  "serverName": null,   // optional — server label
  "isPublic": true,     // optional, default true
  "isMature": false,    // optional, default false
  "userId": 10,         // optional — must match the auth user's ID
  "promptId": null,     // optional — FK to a saved Prompt record
  "artCollectionId": null,  // optional — FK to an ArtCollection
  "designer": "kindguest"   // optional — attribution string
}
```

### Response (201 on success)

```json
{
  "success": true,
  "message": "ArtImage generated successfully.",
  "data": {
    "id": 1234,
    "imagePath": "/images/generated/uuid.webp",
    "promptString": "a glowing forest at dusk, watercolor style",
    "artPrompt": "a glowing forest at dusk, watercolor style",
    "negativePrompt": "blurry, low quality",
    "steps": 20,
    "cfg": 3,
    "cfgHalf": false,
    "seed": 42,
    "width": 512,
    "height": 512,
    "sampler": "Euler a",
    "checkpoint": "v1-5-pruned-emaonly",
    "serverId": 1,
    "serverName": "Primary SD Server",
    "serverUrl": "http://internal:7860/sdapi/v1/txt2img",
    "userId": 10,
    "isPublic": true,
    "isMature": false,
    "createdAt": "2026-06-30T10:00:00Z"
  },
  "mana": {
    "balance": 980,
    "charged": 20
  }
}
```

### Failure Modes

| Code | Cause |
|---|---|
| 400 | Missing `promptString` |
| 401 | Missing or invalid Bearer token (apiKey not found) |
| 403 | `userId` in body doesn't match auth user |
| 400 | Server is not active or is not an A1111 server type |
| 500 | Upstream A1111 server returned no images |
| 500 | Failed to save generated image to DB |

### Important Notes

- The endpoint is **synchronous** — it calls the A1111 server inline and waits for the result. No polling needed.
- `imagePath` is a relative path (`/images/generated/...`), not a full URL. The Conductor wrapper must prepend the kind_robots base URL or the CDN hostname.
- Mana is deducted per call via `withArtMana` gate. If the user's mana balance is insufficient, the call fails with a 402/403 (mana gate error) before hitting the A1111 server.
- The caller must have a running A1111 server registered in the kind_robots DB. If no server is available, returns 400.

---

## 2. POST /api/comfy/flux/generate (ComfyUI Flux)

### Auth

```
Authorization: Bearer <JWT from /api/auth/login>
```

This uses the standard session JWT, not the user's static apiKey. The ComfyUI gate (`authAndGate`) validates the JWT from the cookie or Authorization header.

### Request Body

```json
{
  "prompt": "a glowing forest at dusk, watercolor style",   // required
  "variant": "dev",       // optional: "dev" (slow, high quality) | "schnell" (fast, lower quality). Default: "dev"
  "negativePrompt": "",   // optional
  "width": 1024,          // optional, default 1024
  "height": 512,          // optional, default 512
  "steps": 20,            // optional
  "cfg": 1.0,             // optional
  "guidance": 3.5,        // optional — Flux-specific guidance scale
  "seed": -1,             // optional, default random
  "sampler": "euler",     // optional, default "euler"
  "scheduler": "normal",  // optional, default "normal"
  "denoise": 1.0,         // optional, default 1.0
  "serverId": null,       // optional — target ComfyUI server DB id
  "serverName": null,     // optional
  "timeoutMs": 180000     // optional — max wait time in ms (default 3 min)
}
```

### Response

This endpoint is **asynchronous and polling-based**. It submits a workflow to ComfyUI, then polls `/history/<prompt_id>` until the job completes.

On success (200):
```json
{
  "success": true,
  "promptId": "uuid-of-comfy-job",
  "images": ["/images/comfy/output_00001_.png"],
  "status": "complete"
}
```

On timeout:
```json
{
  "success": false,
  "message": "Generation timed out after 180000ms",
  "promptId": "uuid-of-comfy-job"
}
```

### Polling Behavior (Handled Internally)

The endpoint handles its own polling internally:
- Poll interval: 1,500ms
- Max wait: `timeoutMs` (default 180,000ms = 3 minutes)
- The HTTP request stays open until the ComfyUI job completes or times out

**From the Conductor wrapper's perspective:** A single POST call — no external polling needed. But set the HTTP client timeout to at least `timeoutMs + 10,000ms` to avoid premature client-side timeout.

### Failure Modes

| Code | Cause |
|---|---|
| 401 | Invalid JWT |
| 400 | No active ComfyUI server available |
| 500 | ComfyUI workflow returned node errors |
| 500 | Timed out waiting for ComfyUI to complete |

---

## 3. POST /api/conductor/art-request (Queue Only)

### Auth

```
X-KR-API-Token: <KR_API_TOKEN>
```
or
```
Authorization: Bearer <KR_API_TOKEN>
```

Uses `validateApiKey` — the static admin API token.

### Request Body

```json
{
  "src": "projects/images/myproject-icon.webp",   // required: target image path
  "pageUrl": "/myproject",                         // optional: where the image is used
  "alt": "MyProject icon",                         // optional
  "label": "MyProject",                            // optional
  "variant": "icon",                               // optional: "icon" | "card" | "hero"
  "prompt": "A glowing robot holding a paintbrush, clean app icon style"  // optional
}
```

### Response (200)

```json
{
  "success": true,
  "message": "Art request queued.",
  "entry": {
    "src": "projects/images/myproject-icon.webp",
    "label": "MyProject",
    "variant": "icon",
    "prompt": "..."
  }
}
```

**Note:** This endpoint writes to `conductor/projects/art-prompts.yaml` via GitHub commit. It does NOT trigger generation — it adds to the queue for the next human-approved generation cycle.

---

## 4. GET /api/art/image/[id] and GET /api/art/image

Read-only endpoints. No auth required for public images.

| Endpoint | Description |
|---|---|
| GET /api/art/image/[id] | Single ArtImage record with all fields |
| GET /api/art/image | List ArtImages, filterable by userId, dreamId, etc. |

---

## Summary for Conductor Wrapper (scripts/request_art.py)

| Use case | Endpoint | Auth |
|---|---|---|
| Queue an art request for human approval | POST /api/conductor/art-request | Admin API key |
| Generate immediately (SD A1111) | POST /api/art/generate | User apiKey (Bearer) |
| Generate immediately (Flux) | POST /api/comfy/flux/generate | User JWT (Bearer) |
| Read a generated image record | GET /api/art/image/[id] | None (public) |

**For Conductor's automated art pipeline:**
- Phase 1 (MVP): Queue-only via POST /api/conductor/art-request — no live generation, just adds to the YAML queue
- Phase 2 (after approval): Live generation via POST /api/art/generate or /api/comfy/flux/generate with a stored user apiKey

This document feeds into art-generator-connect/t-002 (Conductor art request script design).
