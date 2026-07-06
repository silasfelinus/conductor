# Serendipity Voice → Kind Robots control bridge

First working end-to-end call from an Amazon Echo utterance to a live Kind Robots
front-end change. Built and verified 2026-07-06.

## What it does

A spoken command like **"Serendipity, turn butterflies on"** travels from the
Echo through the serendipity-voice runtime to the Kind Robots Serendipity Voice
view page, which turns the butterfly screen animation on. Both sides of the
conversation show up in a shared message feed.

## Shape

```text
Echo ──Alexa custom skill──▶ serendipity-voice runtime
                               parse → `control` domain → control adapter
                               │ emits a structured SerendipityCommand
                               ▼
                          relay bus (in-memory, in dev-web-server)
                          POST /api/alexa · GET /api/commands · GET/POST /api/messages
                               ▲ polled over CORS (localhost)
                     Kind Robots /serendipity-voice page
                     serendipityVoiceStore → animationStore.toggleScreenEffect('butterfly-animation')
                               ▼
                     app-wide <fx-region region="page"> renders the butterflies
```

## Where the code lives

**silasfelinus/serendipity-voice**
- `src/commands.ts` — the `SerendipityCommand` contract.
- `src/voice-router.ts` — new `control` domain + `parseControl` (animation vocabulary, on/off/toggle/clear).
- `src/adapters/control-adapter.ts` — builds the structured command + voice reply.
- `src/relay-bus.ts` — in-memory command + message bus with cursors.
- `src/voice-bridge.ts` — runs a request and publishes results to the bus.
- `src/dev-web-server.ts` — CORS + `/api/alexa`, `/api/commands`, `/api/messages`, `/api/bus`.
- Tests: `voice-router`, `handle-voice-request`, `skill-event`, `relay-bus`, `voice-bridge` (65 checks). `npm test` and `npm run typecheck` green.

**silasfelinus/kind_robots**
- `stores/serendipityVoiceStore.ts` — polls the relay, applies commands to `animationStore`, mirrors the message feed.
- `components/pages/serendipity-voice-page.vue` — the view (feed, connect, simulate box, live animation state).
- `content/serendipity-voice.md` — routes the page at `/serendipity-voice`.
- `npm run test` (vue-tsc), eslint, and prettier all green.

## Verification done

- serendipity-voice unit suite + typecheck green.
- Live `curl` proof: `POST /api/alexa` with the butterflies-on Alexa event returns
  the correct Alexa reply and enqueues the command; the front end polls it; the
  message feed shows both sides.
- Headless-browser proof (Playwright/Chromium) against the live relay: the Alexa
  event drove a front-end butterfly render (0 → 20 → 0 on off), no console errors.
- Kind Robots page verified by vue-tsc/eslint/prettier; the animationStore path
  it drives is the same one `screen-fx.vue` uses.

## Safety posture

- Commands only toggle reversible visual effects. No data writes, no publishing,
  no spend, no roadmap YAML edits.
- The relay is a local, in-memory dev seam (resets on restart), CORS scoped to
  local development.
- No Alexa skill was published and no live endpoint was exposed.

## Not done (human-gated — see t-010)

Binding a physical Echo needs an Amazon custom skill pointed at a publicly
reachable copy of `POST /api/alexa` (Lambda or tunnel). That exposure/publish
step stays behind the t-010 dry-run + approval gate. Everything up to that line
is built and proven locally.
