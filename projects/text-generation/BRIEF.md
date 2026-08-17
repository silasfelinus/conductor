# Text Generation — Design Brief

Task: text-generation/t-001 · Date: 2026-08-17 · Status: direction for m2/m3, not a
permanent contract — course-correct per task as implementation proceeds.

Source: `notes_from_silas` in `roadmap.yaml` — cloud text providers (OpenAI,
Anthropic/Claude) already exist; private/self-hosted text generation should be a
first-class supported path for chat and general text generation, not an ad-hoc
special case. This brief inventories what already exists in `kind_robots` (based
directly on reading the current code, not assumptions) and defines the target
contract, migration plan, security boundaries, and implementation sequence for
m2 (t-002–t-004) and m3 (t-005–t-006).

## Current-state capability map

Three separate, hand-written streaming chat endpoints exist today, each ~250–320
lines, each duplicating the same scaffolding (auth, mana gate, header setup,
byte-relay pump, trailing `event: mana` frame, per-route cost estimator):

| Route | Server resolution | Default model | Default maxTokens | Content-Type | Auth header style |
|---|---|---|---|---|---|
| `server/api/chats/openai/stream.post.ts` | **optional** — only if `serverId`/`serverName` given, else hardcoded `api.openai.com` + env key | `gpt-4o-mini` | 2048 | `text/event-stream` | `Authorization: Bearer` |
| `server/api/chats/anthropic/stream.post.ts` | same optional pattern, else `api.anthropic.com` + env key | `claude-sonnet-4-6` | 4096 | `text/event-stream` | `x-api-key` + `anthropic-version` |
| `server/api/chats/ollama/stream.post.ts` | **unconditional** — always calls `resolveServer`, throws if none resolves | `llama3.2` | 1024 | `application/x-ndjson` | built generically from `Server.authType` (`NONE`/`BEARER`/`HEADER`/`API_KEY`) |

**What already works, in full, today:**
- **Stored server profiles** (`Server` Prisma model: `serverType`, `baseUrl`,
  `endpointPath`, `healthPath`, `apiKey`, `authType`, `isPublic`/`isOfficial`/
  `isDefault`/`isActive`/`isEditable`, `accessMode`) with full CRUD
  (`server/api/server/index.{get,post}.ts`, `[id].{get,patch,delete}.ts`,
  `key/[id].patch.ts`, `batch.post.ts`) and ownership/visibility enforcement
  (`canReadServer`/`canMutateServer`/`canDeleteServer` in `serverApi.ts`), with
  API keys redacted (`safeServer`) to everyone except the owner/admin.
- **Canonical server resolution** (`server/utils/serverResolver.ts`
  `resolveServer({userId, serverId, serverName, capability})`): explicit id →
  explicit name → `User.preferredTextServerId` (or `preferredArtServerId`) →
  first `isDefault` matching capability+visibility → first matching
  active/visible server → throw. This is already generic across text and art.
- **A real, working native Ollama route** with generic per-server auth-header
  building — a private/self-hosted LAN or Tailscale Ollama box is already a
  fully working request path today, not a stub.
- **Health infrastructure**: `ServerHealthCheck` model, `server/api/server/
  heartbeat.post.ts` (machine/relay-only ingestion — built for the
  can't-be-reached-from-deployed-backend home-relay pattern), `uptime.get.ts`
  (admin dashboard, currently scoped to `A1111`/`COMFY` by default).
- **Mana accounting** (`server/utils/manaGate.ts`) consistently gates all three
  routes pre-flight (402 on insufficient balance) and commits post-stream, with
  a correct free-generation exemption set (owned server, non-official public
  server, admin, server-key, `FAMILY` role, explicit `useOwnResource`).
- **Client-side plumbing** (`stores/chatStore.ts`): `getTextStreamEndpoint`
  already dispatches by `serverType`; `resolveTextServer` mirrors the backend's
  resolution precedence; `buildStreamPayload` builds the right shape per
  provider (including splitting Anthropic's system/messages); a permissive
  `extractStreamToken` already parses all three providers' differing native
  stream shapes plus the synthetic `mana`/`error` trailer frames.

**What is missing or incomplete:**
- **`capabilityWhere('text')` excludes `OLLAMA`** in `serverResolver.ts` — an
  Ollama server can only ever be reached via explicit `serverId`/`serverName`/
  `preferredTextServerId`, never as a type-based default/fallback. This is the
  concrete "capability routing is incomplete" gap the roadmap note calls out.
- **No shared provider service.** All three routes duplicate message
  normalization, header building, streaming relay, and (critically) cost
  estimation. Three near-identical, silently-drifted local cost estimators
  exist (`estimateOpenAiTextCostUsd`/`estimateAnthropicTextCostUsd`/
  `estimateOllamaTextCostUsd`) even though a correct shared one already exists
  and is unused here (`server/utils/manaCost.ts`'s `estimateTextCostUsd`, which
  also correctly multiplies by `n` — the OpenAI route's local estimator does
  not, undercharging multi-completion requests). A separate legacy path,
  `server/api/botcafe/stream.ts`, *does* use the shared estimator — the drift
  is specifically in the three `chats/*/stream.post.ts` routes.
- **No canonical one-shot (non-chat) generation surface.** All three routes are
  chat-shaped (`chatId`, mana `refId: chat:${chatId}`) — there's no endpoint a
  non-chat feature (e.g. a title generator, a brainstorm helper) can call
  without faking a chat context. (`botcafe/*` is exactly this kind of ad-hoc
  special-casing the roadmap note wants to end.)
- **No cancellation anywhere**, front or back. Confirmed zero `AbortController`/
  `signal` usage in any of the three backend routes or in `chatStore.ts`. A
  client navigating away or clicking "stop" cannot currently end an in-flight
  generation or its mana charge early.
- **No SSRF/network boundary work done yet for private servers.** Any stored
  `Server` row with a `baseUrl` is dialed as-is; there is no explicit block on
  cloud-metadata (`169.254.169.254`), link-local, or otherwise unsafe
  destinations, no redirect policy, and no connect/read timeout or response-size
  cap visible in any of the three routes. This is fine today only because
  server creation is itself gated to an authenticated owner/admin picking a
  `baseUrl` (not derived from arbitrary request input) — but it is not yet a
  *defended* boundary, just an *incidental* one. This is exactly m3/t-005's scope.
- **`Server.serverType` has no `OPENAI_COMPATIBLE`/generic-chat-API variant** —
  today `CUSTOM` is the closest fit for a self-hosted OpenAI-compatible server
  (e.g. vLLM, LM Studio, llama.cpp server), but nothing in the three routes
  actually branches on `CUSTOM` for text; only `ANTHROPIC` and `OLLAMA` get
  dedicated routing in `chatStore.getTextStreamEndpoint`, so a `CUSTOM` text
  server currently falls through to the OpenAI route's request shape, which
  happens to work for most OpenAI-compatible servers but is untested/implicit.
- **No UI for choosing a text provider/server** beyond whatever `serverId` a
  calling component hardcodes; `preferredTextServerId` exists on `User` but no
  settings surface to set it was found in this pass.

## Target generation contract (m2)

Design principle from the roadmap note and this audit: **consolidate mechanics,
keep behavior compatible, make private servers a real first-class capability
rather than a bolt-on.**

- **One-shot vs. chat vs. streaming** are the same underlying call with
  different framing, not three different code paths:
  - *Input*: `prompt` OR `messages[]` (existing `normalizeMessages` shape, kept),
    optional `system`, `model`, `temperature`, `maxTokens`, `n`.
  - *Context*: optional `chatId` for chat-shaped calls (keeps `Chat` persistence
    and mana `refId` scoping as-is); its absence means one-shot — no forced chat
    context, so `botcafe/*`-style ad-hoc callers have a real home.
  - *Mode*: `stream: boolean` (default true, matching current behavior) — a
    non-streaming caller gets one JSON response instead of an SSE/ndjson feed,
    reusing the same provider dispatch and mana accounting.
- **Provider/profile capability**: `serverId`/`serverName` selects a stored
  `Server` profile exactly as today; absent both, resolution falls through
  `preferredTextServerId` → default → first-matching, per the existing
  `resolveServer` precedence (fix the `OLLAMA` capability-set gap so this
  actually reaches Ollama servers, not just OpenAI/Anthropic/Custom).
  `userApiKey` (OpenAI/Anthropic only) and the system-env fallback keys remain
  supported for the zero-configuration case.
- **Model selection**: unchanged per-provider default (`gpt-4o-mini`,
  `claude-sonnet-4-6`, `llama3.2`), explicit `model` always wins, no allow-list
  added — providers/servers already constrain what's actually callable.
- **Server ownership/visibility**: unchanged — `resolveServer`'s existing
  visibility `where` (public OR owned) stays the single source of truth; no
  route should re-derive its own visibility check.
- **Error semantics**: keep the existing two-phase shape — pre-stream failures
  (`createError` with real HTTP status) vs. mid-stream failures (`event:
  error` frame, since headers are already committed). Normalize the *message*
  shape across providers (currently each route writes a differently-worded
  message) without changing the two-phase mechanism itself.
- **Cancellation semantics (new)**: wire an `AbortController` from the h3
  request lifecycle (`event.node.req` close/`event.context`) through to the
  upstream `fetch`, so a client disconnect stops the upstream call and skips
  `commit()` (or commits a partial/reduced charge — decide in t-004, but
  *some* signal must exist; charging full price for an aborted generation is a
  concrete bug this brief is flagging, not something to silently keep). Expose
  a client-callable way to cancel (e.g. closing the `EventSource`/`fetch`
  reader) matching whatever h3 actually supports for abort detection.
- **Mana accounting**: keep `manaGate`/`applyMana`/`GENERATION_TEXT` exactly as
  today (pre-flight check, post-stream commit) but route *all* text-generation
  callers — one-shot and chat alike, cloud and private alike — through the one
  shared `estimateTextCostUsd` (already correct, already handles `n`) instead
  of the three drifted local estimators. Free-generation exemptions
  (`isFreeGeneration`) stay unchanged.

## Migration / compatibility plan

The three existing endpoints (`chats/openai/stream`, `chats/anthropic/stream`,
`chats/ollama/stream`) stay as the literal request URLs the client currently
calls — **no `chatStore.ts` breakage on day one.** Consolidation happens
*underneath* them:

1. **t-002** extracts the shared provider-service layer (message normalization,
   endpoint/header resolution per `serverType`, the byte-relay pump, the
   `event: mana`/`event: error` trailer convention, and — critically — a single
   cost-estimation call site using `estimateTextCostUsd`). The three existing
   `stream.post.ts` files become thin adapters calling into this service,
   preserving their current request/response shape and content-type
   (`text/event-stream` vs `application/x-ndjson`) exactly, verified by
   existing/expanded tests before touching call sites.
2. **t-003** fixes `capabilityWhere('text')` to include `OLLAMA`, adds whatever
   `Server` UX/CRUD is needed to make a private text server a first-class
   selectable thing (not just reachable by lucky id), and adds an authenticated
   health/test action reusing `recordServerHealthCheck`.
3. **t-004** adds the new unified one-shot/streaming surface (new route, e.g.
   `server/api/text/generate.post.ts` — exact path decided at implementation
   time) built on the t-002 service, for non-chat callers. Existing three chat
   routes are **not deleted** in this milestone; they keep working, now backed
   by the shared service. `botcafe/*`'s ad-hoc OpenAI-only paths become
   candidates to migrate onto the new surface once it exists and is proven
   (tracked as a follow-up, not silently done as scope creep inside t-004).
4. **t-005** (human-gated) hardens the private-server network boundary
   (SSRF/timeout/redirect/cancellation-on-disconnect) across whichever routes
   now dial arbitrary stored `baseUrl`s — this is a security-boundary change on
   already-shipped private-server reachability, so it stays gated even though
   the code itself is reversible, per the existing task's `gate_human: true`.
5. **t-006** wires provider/server selection into the actual product surfaces
   (`conductor-project-chat.vue`, `bot-chat.vue`, `character-chat.vue`,
   `character-flip-card.vue`, `reward-encounter.vue` — the five confirmed
   `chatStore.streamResponse` callers) and documents a real self-hosted setup
   path (Ollama + one OpenAI-compatible server), without ever exposing a raw
   `apiKey` to the browser (`safeServer`'s redaction stays the only path
   client code reads server credentials through).

**Explicitly out of scope for this project:**
- Rewriting `chatStore.ts`'s multi-provider stream-token parser — it already
  works across all three current shapes; only extend it if the unified surface
  (t-004) introduces a genuinely new wire shape.
- Deleting or replacing `server/api/botcafe/*` — noted as a migration
  candidate, not committed work, until t-004 exists to migrate onto.
- Image/art generation (`server/api/comfy/*`, `chats/openai/images/*`,
  `artStore.ts`) — `resolveServer`'s `'art'`/`'comfy'` capabilities and the
  `A1111`/`COMFY` server types are unaffected by this project.
- Building new provider integrations beyond OpenAI/Anthropic/Ollama/
  OpenAI-compatible-custom (e.g. no Bedrock/Vertex/Azure-specific work) unless
  a later task adds it explicitly.
- `server/api/server/uptime.get.ts`'s admin dashboard scope — currently
  `A1111`/`COMFY`-only by default; extending it to text servers is a nice-to-have
  the roadmap doesn't currently ask for.

## Security boundaries

- **Credential custody unchanged**: provider API keys stay server-side only
  (`server.apiKey` read directly by route/service code, never returned raw to
  clients — `safeServer` redaction is the only client-facing path). The
  precedence `userApiKey (request) → server.apiKey (stored) → runtime env key`
  stays as-is; the unified surface must not introduce a fourth, less-audited
  precedence rule.
- **Private-server SSRF boundary (t-005)**: a stored `Server.baseUrl` is
  created only by an authenticated owner/admin through the existing
  CRUD+ownership checks — private-network access must stay reachable **only**
  through such a stored, authorized profile, never through a client-supplied
  ad-hoc URL on a generation request. t-005 adds the actual defenses (block
  cloud-metadata/link-local targets, constrain protocols, cap redirects,
  connect/read timeouts, response-size limits) on top of that existing
  authorization boundary — the authorization already exists; the network-layer
  defense-in-depth does not yet.
- **Mana as the de facto rate limit**: no separate rate-limiting was found on
  any of the three routes beyond the mana balance check — this is accepted
  existing behavior, not a new gap introduced by this project, but worth
  naming as a real constraint (a free/admin/server-key caller has no volume
  cap on private-server calls beyond whatever the private server itself
  enforces).
- **Cancellation-on-disconnect** (see contract above) is also a security-minor
  point, not just a UX one: an unbounded, uncancellable upstream stream held
  open by a client that already left is unnecessary resource/cost exposure.

## Success criteria

- A private/self-hosted text server (Ollama today; an OpenAI-compatible
  `CUSTOM` server as the second proof point) is reachable through the exact
  same resolution path as a cloud provider — no special-cased "if Ollama"
  branches left in application code outside the provider-service layer itself.
- The three existing chat routes' current behavior (request/response shape,
  content-type, mana charging, error framing) is unchanged from a caller's
  perspective after t-002, verified by tests, not just by inspection.
- Exactly one cost-estimation code path is used for text generation
  (`estimateTextCostUsd`), not four (three local + one unused shared one).
- A non-chat feature can generate text (one-shot or streaming) without
  fabricating a `Chat` row to do it.
- A generation request can be cancelled client-side and the server stops
  billing/streaming promptly instead of running to provider completion
  regardless of client presence.
- Private-server destinations are defended against SSRF-class abuse
  (metadata/link-local/redirect) with tests proving the block, while an
  approved private profile still completes a real generation end-to-end.
- `preferredTextServerId` is settable from a real UI, not just a raw database
  field, and the chosen provider is visible/understandable in the surfaces
  that use it (not a hidden request parameter).

## Concrete implementation sequence

1. **t-001 (this brief)** — done.
2. **t-002** — shared server-side provider layer; adapt the three existing
   routes onto it with no observable behavior change; consolidate cost
   estimation onto `estimateTextCostUsd`.
3. **t-003** — fix `OLLAMA` capability routing; first-class trusted
   private-server profile UX/CRUD path; authenticated health/test action.
4. **t-004** — unified one-shot + streaming generation endpoint on top of
   t-002/t-003; integration tests proving cloud + private-server parity in
   both modes.
5. **t-005 (human-gated)** — SSRF/timeout/redirect/cancellation hardening
   across every route that dials a stored `baseUrl`; security-focused test
   suite; stays at `needs-human` before merge per its existing `gate_human`.
6. **t-006** — product-surface wiring (the five confirmed chat consumers) +
   self-hosted setup docs (Ollama + one OpenAI-compatible server), never
   exposing raw secrets to the browser.

Milestones map directly: m1 = this brief (t-001); m2 = t-002–t-004 (unified
generation + real private-server integration); m3 = t-005–t-006 (security
hardening, UX, docs).
