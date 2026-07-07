# alexa-integration changelog

## 2026-07-07
- Physical Echo went live end-to-end: a real Alexa custom skill ("serendipity please")
  reaches the serendipity-voice runtime over a Cloudflare quick tunnel. Runbook updated
  with the hard-won console gotchas: must be a **standard custom skill, not Alexa
  Conversations** (Conversations requires AMAZON.FallbackIntent and forbids
  AMAZON.SearchQuery → the opaque `invalid JsonArtifact` build error); two-word,
  serendipity-first invocation name; carrier-word utterances incl. the natural
  `will she {request}`; trycloudflare wildcard-cert endpoint option; where to find the
  Skill ID.
- Added per-person personalization (t-014, serendipity-voice PR #13): map each Alexa
  voice-profile personId → a Kind Robots user (SERENDIPITY_PERSON_MAP + default), so a
  shared Echo attributes art to the right person and greets them by name. Unmapped voices
  self-announce their personId on the view feed. KR-side owner-on-behalf-of is the
  remaining follow-up.
- serendipity-voice reliability: added a zero-dependency .env auto-loader (PR #12) so art
  vars actually reach the dev:web process (fixes draft-instead-of-queued). Normalized the
  home relay's local-copy path to forward slashes (conductor PR #259).

## 2026-07-06 (later)
- Added Alexa request-signature verification to serendipity-voice
  (src/alexa/verify-request.ts): cert-chain URL + cert SAN/validity + RSA body
  signature + timestamp replay window + applicationId. Off by default; enable
  SERENDIPITY_ALEXA_VERIFY_SIGNATURE=true before public exposure. Runbook updated.
- Standardized on the existing home relay (conductor ops/home-server/relay_agent.py,
  pm2 "kr-relay"); reverted a redundant TS relay that had been added to serendipity-voice.

## 2026-07-06
- Wired real art generation (t-011 done): voice art requests now submit to the Kind Robots art API (POST /api/art/queue by default, or /api/art/generate) using the service token; broadened the art parser for natural phrasing ("generate me an image of a fox"). Gated behind SERENDIPITY_ENABLE_ART + a token. Operator steps for the physical Echo in docs/physical-echo-runbook.md.
- Extended the voice bridge (t-013): theme control ("set theme to synthwave"), "surprise me" random animation, and art drafts relayed to a review panel on the Serendipity view. Command contract now spans animation | theme | art. Draft-only/client-side; verified via tests, vue-tsc/eslint/prettier, live curl, and headless browser.
- First working end-to-end voice-to-front-end call (t-012): "Serendipity, turn butterflies on" from an Alexa event drives the Kind Robots butterfly animation.
- serendipity-voice: added `control` domain, control adapter, in-memory relay bus, and CORS relay endpoints (`/api/alexa`, `/api/commands`, `/api/messages`).
- kind_robots: added the Serendipity Voice view at `/serendipity-voice` (serendipityVoiceStore + page) that polls the relay and drives animationStore.
- Design + verification notes in `docs/animation-control-bridge.md`. Physical Echo binding remains behind the t-010 human gate.

## 2026-06-28
- Added initial project scaffold.
- Added workspace image request queue entries.
