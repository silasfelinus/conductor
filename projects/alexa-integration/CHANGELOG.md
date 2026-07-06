# alexa-integration changelog

## 2026-07-06
- Extended the voice bridge (t-013): theme control ("set theme to synthwave"), "surprise me" random animation, and art drafts relayed to a review panel on the Serendipity view. Command contract now spans animation | theme | art. Draft-only/client-side; verified via tests, vue-tsc/eslint/prettier, live curl, and headless browser.
- First working end-to-end voice-to-front-end call (t-012): "Serendipity, turn butterflies on" from an Alexa event drives the Kind Robots butterfly animation.
- serendipity-voice: added `control` domain, control adapter, in-memory relay bus, and CORS relay endpoints (`/api/alexa`, `/api/commands`, `/api/messages`).
- kind_robots: added the Serendipity Voice view at `/serendipity-voice` (serendipityVoiceStore + page) that polls the relay and drives animationStore.
- Design + verification notes in `docs/animation-control-bridge.md`. Physical Echo binding remains behind the t-010 human gate.

## 2026-06-28
- Added initial project scaffold.
- Added workspace image request queue entries.
