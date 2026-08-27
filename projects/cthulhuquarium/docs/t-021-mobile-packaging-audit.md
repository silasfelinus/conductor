# t-021: Mobile packaging groundwork — audit and submission checklist

Date: 2026-08-27
Scope: `/play/aquarium` (Cthulhuquarium) in the kind_robots repo (Nuxt 3 / Vue 3, shared
app-root PWA infra).

## Question

DESIGN-BRIEF.md's MVP scope names iOS/Android as Silas's tier 2 ("Agents can prepare a
Capacitor/PWA wrapper and document the steps; agents do not create accounts or submit
builds"). This task evaluates Capacitor vs PWA vs a native shell for Cthulhuquarium
specifically, fixes any build-side blocker to packaging that's actually found, and
writes the submission checklist Silas would execute.

## Don't re-derive what's already decided

kind_robots already ran this exact evaluation site-wide for Art Academy
(`ai-art-academy/t-061`, `docs/t-061-mobile-delivery-audit.md`) and shipped the result
(`ai-art-academy/t-066`, kind_robots PR #1588): **PWA first, Capacitor only if Silas
later asks for an actual store listing.** That decision and its infrastructure are
app-root scoped, not Academy-only — `nuxt.config.ts`'s `pwa:` block, `@vite-pwa/nuxt`,
the manifest, icon set, and service worker apply to every route including
`/play/aquarium`. There is no reason for Cthulhuquarium to re-litigate the
PWA-vs-Capacitor-vs-native question from zero; this doc confirms the existing answer
still holds for this specific game and audits what, if anything, is specific to it.

## What already works today (live-verified)

Checked `https://kindrobots.org/play/aquarium` directly (production, per AGENTS.md's
verification-path guidance — no PR-preview infra exists for this repo):

| Check | Result |
|---|---|
| `GET /play/aquarium` | `200`, real SSR markup |
| `<link rel="manifest" href="/manifest.webmanifest">` in `<head>` | present |
| `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">` | present (the `viewport-fit=cover` piece matters for iPhone notch/safe-area) |
| `<meta name="theme-color" content="#b4653a">` | present |
| `<link rel="apple-touch-icon" sizes="180x180" ...>` | present |
| `GET /manifest.webmanifest` | `200`, valid JSON — name, icons (192/512 + maskable), `display: standalone`, `start_url: /` |

This is the same installability chrome ai-art-academy/t-062 fixed the missing-mount bug
for (kind_robots PR #1621) — that fix is app-root scoped and already covers this route.
**No blocker found here; nothing to fix.** Cthulhuquarium is installable as a PWA today,
with zero additional per-project engineering, on both Android (Chrome install prompt)
and iOS (Safari "Add to Home Screen").

## Cthulhuquarium-specific review (beyond the generic site-wide PWA baseline)

Read `components/cthulhuquarium/cthulhuquarium-game.vue` (897 lines) and
`stores/cthulhuquariumTankStore.ts` looking for anything mobile-packaging-relevant that
the generic Academy audit wouldn't have covered, since this is a different component
tree:

- **Server-persisted, not offline.** State reaches the server through `performFetch`
  against `server/api/aquarium/*` (`feed`, `purchase`, `tick`, `clean`, `catalog`,
  `bestiary`) — same shape as Academy's API-driven content, not a fully offline game
  like `ruler-hooked` (whose card game *is* pure `localStorage` and got its own
  network-first document-caching rule for exactly that reason, ruler-hooked/t-015). That
  means Cthulhuquarium should **not** get the same offline-document caching treatment:
  the DESIGN-BRIEF's own MVP item 8 ("persist server-side across devices") requires the
  network, so an offline-cached shell would just show state that can silently drift from
  the server. Correct scope for this game's `workbox.runtimeCaching` is "none" — same
  as Academy, and the current site-wide config already agrees (no cthulhuquarium entry
  in `runtimeCaching`).
- **Canvas already phone-safe.** `cthulhuquarium/t-020` (done, kind_robots#2145)
  already fixed thumb-sized touch targets, `aspect-[16/9]` CSS scaling of the fixed
  640×360 logical canvas, and a `touchHitRadius()` helper so drift-mote taps stay
  accurate when the canvas is scaled down on a phone width. Re-verified the canvas is
  still CSS-scaled (`STAGE_WIDTH`/`STAGE_HEIGHT` constants, comment: "CSS scales it to
  the host width so the canvas survives phone widths without its own breakpoint
  logic") — nothing regressed since t-020, nothing new to fix for packaging.
- **No orientation lock, no fixed-desktop assumption.** The canvas is a fixed 16:9
  logical resolution CSS-scaled to its container in both dimensions; it renders
  (smaller, same aspect) in portrait, same as any other 16:9 media element. Not
  optimal — a native app would likely want a portrait-first layout for a phone-first
  game — but it is not a packaging **blocker**, and reworking the game's layout is out
  of this task's "research and prepare only" scope.
- **Minor, non-blocking finding: no `visibilitychange` pause.** `pollTick()` runs on a
  plain `setInterval(TANK_POLL_INTERVAL_MS)` (20s) and the render loop is a plain
  `requestAnimationFrame` loop — neither pauses when the tab/app is backgrounded.
  Browsers already throttle background-tab timers and `rAF` on their own, so this is
  not a functional bug, but it's exactly the kind of thing an App Store / Play Store
  reviewer or a battery-conscious user notices in a wrapped native app where background
  behavior is more visible than in a browser tab. Filed as a small, independently
  reversible follow-up (`t-023` below) rather than fixed inline here — it's a
  legitimate improvement, but out of scope for an audit-and-checklist task to also
  carry a gameplay-code change.

## Recommendation (unchanged from the site-wide precedent, confirmed for this game)

**PWA first — already shipped, already verified working for this specific route.**
Defer Capacitor unless Silas decides an actual Play Store / App Store *listing* is a
real requirement. When that happens, the manifest/icon work already done is directly
reusable; nothing here needs to be redone.

## Submission checklist (for Silas — nothing below is executed by an agent)

### A. Verify the PWA today (no accounts, no cost, agents can help verify but not click "install" on Silas's own device)
1. On an Android phone: open `https://kindrobots.org/play/aquarium` in Chrome, use the
   install prompt (or menu → "Install app"), confirm it opens standalone (no browser
   chrome), the canvas renders, touch feed/purchase controls work, and login/session
   survives the standalone context.
2. On an iPhone/iPad: open the same URL in Safari, Share → "Add to Home Screen", same
   standalone smoke test.
3. Confirm the "you're offline" case is graceful (a clear message, not a blank white
   screen) since gameplay actions require the network by design — if it isn't graceful,
   that's a small, separately-scoped follow-up, not a store blocker.

### B. If/when Silas wants an actual store listing — Capacitor path
1. `npm install @capacitor/core @capacitor/cli @capacitor/android @capacitor/ios`,
   `npx cap init` (app id, e.g. reverse-domain `org.kindrobots.app`; app name).
2. Because this app is SSR/API-driven rather than a static SPA bundle, point Capacitor
   at the live site (`server.url` in `capacitor.config.ts`) rather than bundling
   `webDir` from a static export — the same "hosted web app in a native shell" pattern
   the t-061 audit named for Academy. This means no separate mobile build has to track
   every web deploy; the wrapped app always shows current production.
3. `npx cap add android` (needs Android Studio + SDK — not available in this sandbox);
   `npx cap add ios` (needs a Mac + Xcode — also not available here). Both are real,
   human-operated build environments, not something to fake or skip.
4. Generate icon/splash assets from the existing 512×512 PWA icon via
   `@capacitor/assets` (or hand-authored per-platform sizes).
5. **Hard human gates below — an agent never performs these, regardless of how routine
   they look (per DESIGN-BRIEF.md's own guardrails and AGENTS.md's hard-gate rules):**
   - Google Play: Play Console developer account ($25 one-time), signed release
     AAB/APK (a keystore that must never be committed to any repo), content-rating
     questionnaire, privacy-policy URL, store listing copy/screenshots, staged
     rollout.
   - Apple App Store: Apple Developer Program enrollment ($99/yr), App Store Connect
     listing, TestFlight beta, App Review submission, privacy "nutrition label",
     any in-app-purchase/ads disclosure (Cthulhuquarium currently has neither, so
     this section should be short — reconfirm before submitting since the economy
     roadmap could change that).
6. Steam: explicitly out of scope for this task and this roadmap (DESIGN-BRIEF.md,
   Silas's "final final", separately human-gated whenever it comes up).

## What this task does NOT do

No developer accounts created, no certificates generated or handled, no payments made,
nothing submitted anywhere. No Capacitor config was added to the kind_robots repo —
following the same sequencing ai-art-academy/t-062 and t-063 already established
(PWA-verify first; Capacitor scaffolding only once Silas actually asks for store
distribution), so there's no half-finished native-shell config sitting unused in the
tree.

## Kaizen

Filed `cthulhuquarium/t-048` ("Pause the tank's 20s poll/render loop when the tab is
hidden") from the minor finding above — small, reversible, `visibilitychange`-gated,
worth doing before any eventual native wrap makes background CPU/battery use more
visible to reviewers and players, but independent of this task's own scope.
