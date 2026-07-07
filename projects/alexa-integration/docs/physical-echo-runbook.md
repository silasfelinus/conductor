# Physical Echo runbook — "Serendipity, generate me an image of a fox"

Everything in code is done and locally verified. This is the operator runbook
for the steps that require your accounts/hardware: giving Kind Robots a service
token, exposing the voice endpoint publicly, and registering the Alexa skill.

The go-live approval is the t-010 human gate — this doc is that review.

## The end-to-end path (default: conductor mode)

Requests go THROUGH kind_robots per the art-generator-connect routing policy,
using the documented producer that `scripts/request_art.py` wraps:

```
Echo → Alexa custom skill → (public) POST /api/alexa on the serendipity-voice runtime
     → parse "generate me an image of a fox" → art command
     → POST /api/conductor/art-request on Kind Robots (X-KR-API-Token, {src, prompt, label, variant})
     → Kind Robots appends the request to projects/art-prompts.yaml (conductor)
     → a worker/consumer claims it and generates → image lands in the gallery
```

The **producer half is done** (this is what serendipity-voice now sends). The
**consumer half** — turning a queued `art-prompts.yaml` request into a generated
image — is the piece still being finished (art-generator-connect t-010/t-012:
the ArtJob queue + a home relay agent; today `/api/conductor/art-request` only
appends to the YAML and nothing drains it). Silas is closing that loop; the voice
side already speaks the request into the canonical queue.

Alternative submit modes if you'd rather skip the YAML lane:
`SERENDIPITY_ART_SUBMIT_MODE=queue` → `POST /api/art/queue` (durable ArtJob DB
queue), or `=generate` → `POST /api/art/generate` (synchronous A1111).

## Step 1 — Kind Robots prerequisites (no code change)

On the Kind Robots server env:

- `JWT_SECRET` — already required for auth.
- The admin token conductor already uses (`KR_API_TOKEN` / `BETA_ADMIN_TOKEN`) —
  this is what `X-KR-API-Token` is checked against by `validateApiKey` +
  `userIsAdmin`. Optional `BETA_ADMIN_USER_ID` (defaults to 1) sets the owner.
- `CONDUCTOR_GITHUB_TOKEN` (or `GITHUB_TOKEN`) — `/api/conductor/art-request`
  needs it to commit the request into `projects/art-prompts.yaml`.
- For the `queue`/`generate` modes only: one **active `serverType='A1111'` Server
  row** reachable at its `baseUrl` + `/sdapi/v1/txt2img`, and optional
  `ART_SERVER_PROXY_TOKEN` if your box needs an auth header.

Sanity check the conductor request path from a machine that can reach KR:

```bash
curl -s -X POST https://<kind-robots-host>/api/conductor/art-request \
  -H 'content-type: application/json' -H "X-KR-API-Token: $KR_API_TOKEN" \
  --data '{"src":"/images/serendipity/a-fox.webp","prompt":"a fox","variant":"image"}'
# expect: {"success":true,"message":"Art request added to Conductor.", ...}
```

(For the DB-queue lane use `/api/art/queue` with
`{"engine":"A1111","payload":{"promptString":"a fox"}}`; for synchronous render
use `/api/art/generate` with `{"promptString":"a fox"}`.)

## Step 2 — Configure the voice runtime

`.env` for serendipity-voice (see `.env.example`):

```bash
SERENDIPITY_ENABLE_ART=true
SERENDIPITY_KR_SERVICE_TOKEN=<the KR admin token: KR_API_TOKEN / BETA_ADMIN_TOKEN>
SERENDIPITY_KIND_ROBOTS_BASE_URL=https://<kind-robots-host>
SERENDIPITY_ART_SUBMIT_MODE=queue   # queue is best for Alexa (fast return, relay renders)
```

The `.env` is **auto-loaded** by `dev:web` (and the handle/alexa/config CLIs), so
you don't have to export vars into the exact shell — just drop the file next to
the repo and `npm run config` will echo the loaded config back. Use the same
`SERENDIPITY_KIND_ROBOTS_BASE_URL` host your `kr-relay` polls, or a queued job
lands on one host and the relay claims from another and nothing renders.

Optional — **per-person attribution** (a shared Echo → each household member's KR
user). Add voice profiles in the Alexa app, then map each personId:

```bash
# discover a personId by speaking once: the view feed prints "Heard a new voice…"
SERENDIPITY_PERSON_MAP={"amzn1.ask.person.ABC":{"userId":5,"name":"Silas"}}
SERENDIPITY_DEFAULT_KR_USER_ID=1   # guests / profile-less devices
```

## Step 3 — Expose POST /api/alexa publicly (pick one)

Alexa must reach a public HTTPS endpoint (valid CA cert) or an AWS Lambda.

- **A. Cloudflare Tunnel / ngrok from your LAN (simplest if KR + SD are on your
  LAN).** Run `npm run dev:web` (or a small prod wrapper) next to Kind Robots,
  then `cloudflared tunnel --url http://localhost:4173`. Use the HTTPS URL it
  prints. Best fit because the runtime and the A1111 box are on the same network.
- **B. AWS Lambda (the "official" Alexa path, no cert to manage).** Wrap
  `runAlexaEvent` in a Lambda handler and set it as the skill endpoint. The
  Lambda must be able to reach `SERENDIPITY_KIND_ROBOTS_BASE_URL` (so KR must be
  public, or the Lambda joins your network). Ask me and I'll add the handler +
  a deploy config.
- **C. Small always-on host (Fly/Render/VPS/Pi).** Deploy the node server, put
  it behind HTTPS, point the skill at `https://host/api/alexa`.

Note: `/api/alexa` supports Amazon request-signature verification (built in
serendipity-voice `src/alexa/verify-request.ts`). It is **off by default** so
local/simulation testing works. Turn it ON before the endpoint is public:

```bash
SERENDIPITY_ALEXA_VERIFY_SIGNATURE=true
SERENDIPITY_ALEXA_SKILL_ID=amzn1.ask.skill.<your-skill-id>   # optional but recommended
```

It checks the cert chain URL, the certificate validity + SAN, the RSA body
signature, the request timestamp (±150s replay window), and the applicationId.

## Step 4 — Create the Alexa custom skill

In developer.amazon.com → Alexa → Create Skill (Custom, provision your own).

> **CRITICAL — pick a standard custom skill, NOT Alexa Conversations.** On the
> templates screen choose **"Start from Scratch"**. An Alexa Conversations skill
> **requires `AMAZON.FallbackIntent`** and **does not support `AMAZON.SearchQuery`**
> — the free-form slot this whole design depends on. A `SearchQuery` slot in a
> Conversations skill fails the build with the opaque error `invalid JsonArtifact`,
> and adding FallbackIntent doesn't fix it (SearchQuery still can't exist there).
> Alexa Conversations also sends a different request shape our `/api/alexa`
> handler doesn't parse. If you already made a Conversations skill, recreate it
> from "Start from Scratch" — there's no in-place toggle.

1. **Invocation name:** two words, `serendipity`-**first** so it reads naturally
   after "ask" — e.g. `serendipity please` ("Alexa, ask serendipity please …").
   Amazon rejects single-word names (`serendipity` alone won't save) and names
   that *contain* launch words like ask/open/tell/to. A name like `hey serendipity`
   technically saves but forces the ungrammatical "ask **hey** serendipity"; put
   the filler word after serendipity instead. The name is independent of our
   parser (it only reads the request text), so any valid two-word name works.
2. **Intent:** `SerendipityRequestIntent` with one slot `request` of type
   `AMAZON.SearchQuery`, sample utterances:
   - `will she {request}`   ← natural + gives Serendipity personality
   - `can she {request}`
   - `to {request}`
   - `to please {request}`
   - `please {request}`
   Every utterance needs at least one carrier word before the slot: Amazon
   rejects a bare `{request}` (an `AMAZON.SearchQuery` slot may not be the whole
   utterance). "to" is optional in the spoken phrase — `ask <name> <utterance>`
   works directly — so `will she {request}` lets you say "ask serendipity please
   **will she** generate a fox" and the slot captures "generate a fox". A single
   bare function word like `to` occasionally trips the SearchQuery validator;
   multi-word carriers are safer.

   A full known-good interaction model (invocationName `serendipity please`, only
   Amazon's four required built-ins + this intent, no FallbackIntent) is the most
   reliable thing to paste into the console's **JSON Editor** if the visual
   builder fights you.
3. **Endpoint:** HTTPS → your Step-3 URL `.../api/alexa` (or the Lambda ARN).
   For HTTPS pick the cert option matching your host. A `trycloudflare.com` quick
   tunnel is a sub-domain under a CA wildcard cert, so choose "My development
   endpoint is a sub-domain of a domain that has a wildcard certificate from a
   certificate authority". Most other PaaS hosts: "has a certificate from a
   trusted authority".
4. Save + Build Model. Test in the console's Test tab first ("ask serendipity
   please will she generate me an image of a fox").

**Finding the Skill ID** (for `SERENDIPITY_ALEXA_SKILL_ID`): the skills list →
⋮ → "Copy Skill ID", or the Build page's "Your Skill ID". Easiest: it's in every
request our `/api/alexa` receives (`applicationId`) and in the reply — so just
say the utterance and read it off the `dev:web` log.

## Step 5 — Say it to the Echo

> "Alexa, ask serendipity please will she generate me an image of a fox."

Expected: Alexa replies "On it. I queued a fox. It will appear in your gallery
shortly." (or "On it, <name>." when the speaker's voice profile is mapped) and
the image shows up in Kind Robots once the home relay renders it.

## Security posture

- The service token is a powerful credential (free generation as the service
  user). Keep it in env only; never commit it. Rotate if leaked.
- Prefer `queue` mode: the endpoint returns fast (under Alexa's ~8s timeout) and
  generation happens on your relay, off the request path.
- Turn on Alexa request-signature verification (`SERENDIPITY_ALEXA_VERIFY_SIGNATURE=true`) before any public exposure — it is built and off by default.
- Voice still cannot approve, merge, publish, spend, delete, or edit roadmap
  YAML — only enqueue a reversible art job.
