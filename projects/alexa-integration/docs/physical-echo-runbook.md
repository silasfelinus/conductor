# Physical Echo runbook — "Serendipity, generate me an image of a fox"

Everything in code is done and locally verified. This is the operator runbook
for the steps that require your accounts/hardware: giving Kind Robots a service
token, exposing the voice endpoint publicly, and registering the Alexa skill.

The go-live approval is the t-010 human gate — this doc is that review.

## The end-to-end path

```
Echo → Alexa custom skill → (public) POST /api/alexa on the serendipity-voice runtime
     → parse "generate me an image of a fox" → art command
     → POST /api/art/queue on Kind Robots  (x-admin-token, {engine:'A1111', payload:{promptString:'a fox'}})
     → Kind Robots enqueues an ArtJob → a home relay claims it → A1111 renders → saved to your gallery
```

## Step 1 — Kind Robots prerequisites (no code change)

On the Kind Robots server env:

- `JWT_SECRET` — already required for auth.
- `BETA_ADMIN_TOKEN=<a long random secret>` — the service token. Optional
  `BETA_ADMIN_USER_ID` (defaults to 1) sets which user owns voice-made art.
- One **active `serverType='A1111'` Server row** reachable at its `baseUrl` +
  `/sdapi/v1/txt2img` (your Stable Diffusion box). Without it KR returns
  "No available server was found."
- Optional `ART_SERVER_PROXY_TOKEN` if your A1111 box needs an auth header.

Sanity check from a machine that can reach KR:

```bash
curl -s -X POST https://<kind-robots-host>/api/art/queue \
  -H 'content-type: application/json' -H "x-admin-token: $BETA_ADMIN_TOKEN" \
  --data '{"engine":"A1111","payload":{"promptString":"a fox"}}'
# expect: {"success":true,"data":{... job ...}}
```

(For synchronous testing use `/api/art/generate` with `{"promptString":"a fox"}`;
it returns the saved ArtImage with base64 in `data.imageData`.)

## Step 2 — Configure the voice runtime

`.env` for serendipity-voice (see `.env.example`):

```bash
SERENDIPITY_ENABLE_ART=true
SERENDIPITY_KR_SERVICE_TOKEN=<same value as BETA_ADMIN_TOKEN>
SERENDIPITY_KIND_ROBOTS_BASE_URL=https://<kind-robots-host>
SERENDIPITY_ART_SUBMIT_MODE=queue     # Alexa-safe; use 'generate' only if fast/local
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

Note: the current `/api/alexa` does not yet verify Alexa's request signature —
fine behind a private tunnel, but before a public/production endpoint add
signature validation (I can add this; it's a small, well-defined addition).

## Step 4 — Create the Alexa custom skill

In developer.amazon.com → Alexa → Create Skill (Custom, provision your own):

1. **Invocation name:** `serendipity`.
2. **Intent:** `SerendipityRequestIntent` with one slot `request` of type
   `AMAZON.SearchQuery`, sample utterances:
   - `{request}`
   - `to {request}`
   - `generate {request}`
   (AMAZON.SearchQuery captures the free-form tail, e.g. "generate me an image of
   a fox".)
3. **Endpoint:** HTTPS → your Step-3 URL `.../api/alexa` (or the Lambda ARN).
   For HTTPS pick the cert option matching your host (Cloudflare/most PaaS: "has
   a certificate from a trusted authority").
4. Save + Build Model. Test in the console's Test tab first ("ask serendipity to
   generate me an image of a fox").

## Step 5 — Say it to the Echo

> "Alexa, ask Serendipity to generate me an image of a fox."

Expected: Alexa replies "On it. I queued a fox. It will appear in your gallery
shortly." and the image shows up in Kind Robots once the home relay renders it.

## Security posture

- The service token is a powerful credential (free generation as the service
  user). Keep it in env only; never commit it. Rotate if leaked.
- Prefer `queue` mode: the endpoint returns fast (under Alexa's ~8s timeout) and
  generation happens on your relay, off the request path.
- Add Alexa request-signature verification before any public exposure.
- Voice still cannot approve, merge, publish, spend, delete, or edit roadmap
  YAML — only enqueue a reversible art job.
