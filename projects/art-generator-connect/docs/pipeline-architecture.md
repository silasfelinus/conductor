# Comfy / SD → kind_robots → conductor: pipeline architecture & routing policy

Date: 2026-07-05
Author: Reviewer session (Silas-directed)
Status: awaiting Silas's nod on the routing policy and queue design (soft gate — see roadmap t-010..t-012)

---

## 1. Where the pipeline stands today

Working and merged:

- **API contracts mapped** — `docs/art-api.md` documents `/api/art/generate`
  (A1111, sync, user apiKey), `/api/comfy/flux/generate` (ComfyUI Flux,
  internal polling, session JWT), and `/api/conductor/art-request`
  (queue-to-YAML, admin token). (t-001)
- **Request wrapper** — `scripts/request_art.py`, dry-run by default. (t-002)
- **URL/asset mapping** — `URL-MAPPING.md`: slug → filename conventions,
  `projects/images/` for project art, folder collections in kind_robots
  `public/images/{slug}/` with `gallery.json` manifests. (t-003)
- **Missing-art detector** — `scripts/queue_missing_project_art.py` writes
  `projects/art-generate.yaml` in dry-run. (t-004, t-006)
- **Intake/distribution** — `scripts/distribute_images.py` routes finished
  images from `projects/process/` into projects and kind_robots collections.
- **Server registry** — kind_robots `Server` model already carries
  `serverType` (A1111/COMFY), `baseUrl` (the tailscale URL), `endpointPath`,
  `healthPath`, and per-user preferred servers. `serverResolver.ts` normalizes
  endpoints and knows the health probes (`/system_stats`, `/sdapi/v1/progress`).
- **The tailscale handshake works** — kind_robots → home SD/Comfy has been a
  proven path since 2026-05-07 (devNotes).

So: every *piece* exists. What's missing is the connective tissue that lets it
run without Silas hand-cranking each step.

## 2. What's actually holding us back

Ranked; each maps to a roadmap task.

1. **The home server isn't durable.** ComfyUI and A1111 are launched by hand
   from `.bat` files. A crash, Windows update, or reboot silently kills the
   entire pipeline until Silas notices. → **Fixed by `ops/home-server/`**
   (pm2 supervision + boot persistence + health watchdog). Roadmap t-009:
   Silas installs it (only he can — it's his box).

2. **No real job queue anywhere.** `/api/conductor/art-request` only appends
   to `art-prompts.yaml` — nothing consumes it. The two live-generation
   endpoints do the work *inside one held-open HTTP request* (Flux polls
   internally up to 3 min). That shape can't survive serverless timeouts,
   can't retry, can't survive the home server being briefly offline, and
   gives conductor nothing to poll. Silas's call (2026-07-05): kind_robots is
   the right owner — it has tokens, users, mana, and persistence.
   → **t-010: `ArtJob` queue in kind_robots** (design in §4).

3. **Machine-auth mismatch on the Comfy endpoints.** `/api/art/generate`
   accepts a long-lived user `apiKey`; `/api/comfy/flux/generate` requires a
   session JWT via `authAndGate`. Conductor automation holds static tokens,
   not browser sessions — so today the Worker literally cannot call Flux.
   → **t-011: accept user apiKey on comfy endpoints** (parity with
   `/api/art/generate`).

4. **No consumer closing the loop.** Even with a queue, nothing yet takes an
   approved `art-generate.yaml`, submits jobs, collects results, and drops
   the files into `projects/process/` where `distribute_images.py` already
   knows what to do. → **t-012: conductor consumer script** (human-gated
   first run).

## 3. Routing policy — through kind_robots vs. direct to the server

Silas's directive (2026-07-05): conductor must distinguish these two lanes.
kind_robots is the intermediary for anything stateful because it owns tokens,
users, mana, and (after t-010) the queue.

| Action | Route | Why |
|---|---|---|
| Generate an image (any engine, any agent) | **through kind_robots** | auth, mana accounting, ArtImage persistence, attribution, queue/retry |
| Queue an art request for human approval | **through kind_robots** (`/api/conductor/art-request`) | already the system of record (YAML in conductor via KR) |
| Look up/verify a generated asset | **through kind_robots** (`/api/art/image[/:id]`) | DB is the record; server disk is not |
| Pick which backend runs a job | **kind_robots decides** (`serverResolver` + Server registry) | callers say *what*, KR decides *where* |
| Health/liveness probe of Comfy or A1111 | **direct** (tailnet: `:8188/system_stats`, `:7860/sdapi/v1/progress`) | ops concern, no state involved; also used by the on-box watchdog via localhost |
| Process supervision (start/stop/restart) | **direct** (on the box: pm2) | KR should never own OS-level process control |
| Local experimentation on the tailnet (Silas at a keyboard) | **direct** | humans can do what they want; results just aren't in the DB |

**The rule in one line:** if the action produces or reads *state* (images,
jobs, tokens, mana), it goes through kind_robots; if it only observes or
manages the *machine*, it may go direct. Conductor Worker cycles never call
the home server directly for generation — a directly-generated image is an
orphan (no ArtImage row, no mana charge, no attribution, invisible to the UI).

## 4. Recommended shape: pull-based queue

```
conductor (scripts, cron, Worker cycles)
    │  POST /api/art/queue        (KR_API_TOKEN / user apiKey)
    ▼
kind_robots  ── ArtJob table (PENDING → RUNNING → DONE/FAILED)
    ▲  GET /api/art/queue/claim   (agent polls outward)
    │  POST /api/art/queue/:id/complete (result upload / imagePath)
    │
home relay agent  (small script ON the Windows box, pm2-managed
    │              alongside comfyui + sd-webui — see ops/home-server/)
    ▼  localhost:8188 / localhost:7860
ComfyUI / A1111
```

Why **pull** (relay agent polls kind_robots) instead of the current push:

- **No held-open requests** — KR's HTTP handlers become instant
  (enqueue / claim / complete), which is serverless-safe.
- **Offline-tolerant** — if the box is down, jobs wait in PENDING instead of
  erroring; pm2 brings the agent back and it drains the backlog.
- **No inbound exposure** — the home server only makes *outbound* HTTPS
  calls; tailscale stays the only door and even it isn't required for the
  data path.
- **kind_robots keeps the existing sync endpoints** for interactive UI use
  ("generate now while I watch"); the queue is the lane for batch/agent work.

The relay agent is deliberately dumb: claim job → call localhost engine →
post result → repeat. All policy (auth, mana, routing, retries, priorities)
lives in kind_robots.

ComfyUI note: Comfy has its own internal queue (`/prompt` returns a queue
position), which the relay can lean on for backpressure — but it is not a
substitute for ArtJob: it evaporates on restart, knows nothing about users or
mana, and can't be read usefully from Vercel. Same conclusion Silas reached:
build the durable queue in kind_robots.

### ArtJob sketch (additive migration only)

```
model ArtJob {
  id            Int      @id @default(autoincrement())
  createdAt     DateTime @default(now())
  updatedAt     DateTime @updatedAt
  status        ArtJobStatus @default(PENDING)   // PENDING RUNNING DONE FAILED CANCELLED
  engine        ServerType    // A1111 | COMFY
  payload       Json          // full request body (prompt, dims, workflow variant…)
  priority      Int      @default(0)
  attempts      Int      @default(0)
  claimedAt     DateTime?
  claimedBy     String?       // relay agent id
  userId        Int           // owner: auth + mana + attribution
  projectSlug   String?       // conductor slug for asset mapping
  artImageId    Int?          // set on completion
  error         String?  @db.Text
}
```

Claim endpoint must be atomic (single `updateMany` guarded on
`status: PENDING`) so a second relay agent someday doesn't double-run jobs.
A `RUNNING` job older than a timeout is re-claimable (crash recovery).

## 5. Phases → roadmap

| Task | What | Where | Status |
|---|---|---|---|
| t-009 | Install pm2 supervision kit (`ops/home-server/`) | Silas's box | needs-human (only Silas can) |
| t-010 | ArtJob queue: model + enqueue/claim/complete endpoints + relay agent | kind_robots PR (Silas-directed backend work, normal review) | ready |
| t-011 | Comfy endpoints accept user apiKey (machine-auth parity) | kind_robots PR | ready |
| t-012 | Conductor consumer: approved `art-generate.yaml` → queue → results → `projects/process/` | conductor | waiting on t-010; first live run human-gated |

With t-009 + t-010 + t-012 in place the loop closes: missing art detected →
queued → approved → generated on the home box → distributed into project
folders and kind_robots collections — with the existing dry-run and approval
gates keeping Silas in control of what actually renders.
