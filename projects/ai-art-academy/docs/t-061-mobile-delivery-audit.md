# t-061: Academy mobile-delivery audit and recommended path

Date: 2026-08-07
Scope: kind_robots repo (`/home/user/kind_robots`), Nuxt 3 / Vue 3 app that hosts Art Academy.

## Question

No Academy iOS/Android implementation is documented in the roadmap. Before choosing an
architecture: what mobile-delivery infrastructure already exists in kind_robots (reuse
candidate), and what's the smallest durable path to a real iOS/Android presence for the
Academy/remix experience that doesn't fork business logic?

## What exists today (audit findings)

| Area | Status |
|---|---|
| PWA (`@vite-pwa/nuxt`, manifest, service worker, icons) | **Not found** |
| Capacitor (config, `android/`/`ios/` dirs, `@capacitor/*` deps) | **Not found** |
| Cordova / React Native / Expo / NativeScript | **Not found** |
| TWA / Bubblewrap | **Not found** |
| Separate mobile-app package in this repo (`/apps`, `/mobile`) | **Not found** — single-package repo, no `workspaces` |
| Add-to-Home-Screen / installability meta (viewport, theme-color, apple-touch-icon, manifest link) | **Not found** in `app.vue` / `nuxt.config.ts` `app.head` |
| Mobile-app strategy docs (repo-wide) | **Not found** anywhere under `docs/` |
| Mobile-app strategy docs (Academy-specific) | **Not found** — `academy.md`/`components/academy/*` describe the feature only; `backgroundMobile/Tablet/Desktop` fields are responsive backdrop images, not app infra |
| Responsive web (Tailwind breakpoints) | **Present**, wide use — 196 component files use `sm:`/`md:`/`lg:`/`xl:` |

One adjacent, relevant project: **"Conductor App"** (`content/conductor-app.md`,
`components/conductor/conductor-app-page.vue`) is an already-tracked, in-progress
**external Flutter client** for steering the Conductor tool specifically — "not on the
App Store or Play Store yet," built in a separate repo not present in this environment.
It is unrelated to Academy/remix delivery and shares no code path with it; it exists
purely as evidence Silas has weighed a native-client path before and chosen Flutter for
that one narrow use case (admin/ops tooling, not a content-browsing surface).

Bottom line: kind_robots today is a fully responsive website with **zero** installability
or native-wrapper infrastructure. Nothing to "extend" — any mobile path starts from zero.

## Options considered

1. **PWA (installable web app)** — add `@vite-pwa/nuxt`, a web manifest, service worker,
   and icon set to the existing Nuxt app. Zero new codebase; the existing Academy
   Vue components, Pinia stores, and API routes are reused as-is. Ships "Add to Home
   Screen" + offline-shell + app-like chrome on both iOS and Android from one app.vue
   change. Not App Store/Play Store listed (iOS PWA install is manual, via Safari's
   share sheet — no direct App Store presence).
2. **Capacitor wrapper around the existing Nuxt build** — wraps the same web app in a
   native shell, producing installable `.ipa`/`.apk` binaries and real store listings.
   Still reuses 100% of existing Vue/Nuxt code (Capacitor loads the built web bundle
   into a native WebView) — no business-logic fork. Adds real overhead: Xcode/Android
   Studio build pipeline, Apple Developer Program enrollment ($99/yr), Play Console
   registration, code-signing, and app-store review process — none of which exist in
   this repo or its CI today.
3. **Native rewrite (Flutter/React Native/Swift/Kotlin)** — a second, parallel
   implementation of the Academy UI. Explicitly ruled out by the task's own framing
   ("without forking business logic") — this is the one option that *does* fork it,
   duplicating every future Academy feature across two codebases indefinitely.
4. **Do nothing beyond current responsive web** — Academy is already phone/tablet
   reachable via the browser (per the interface-vision responsive-audit work in
   progress this same cycle). Zero new surface area, zero maintenance cost, but no
   installability, no home-screen icon, no app-store presence.

## Recommendation: PWA first, Capacitor only if store presence becomes a real requirement

Start with **option 1 (PWA)** as the durable baseline:

- Smallest actual change: add `@vite-pwa/nuxt`, a manifest (name, icons at 192/512,
  theme-color, `display: standalone`), and register a basic service worker (cache-first
  for static assets is enough — Academy content is API-driven, not offline-capable, so
  don't over-build a full offline mode in the first pass).
- No new build pipeline, no store accounts, no code-signing, no separate repo — ships
  through the existing Vercel deploy exactly like every other kind_robots change.
- Immediately usable on both iOS (Safari "Add to Home Screen") and Android (Chrome
  install prompt) — genuinely cross-platform from one implementation.
- 100% reuse of existing Academy components/stores/routes — literally the same app,
  just installable.

Escalate to **option 2 (Capacitor)** later, and only if Silas decides an actual App
Store / Play Store *listing* is a real product requirement (discoverability, push
notifications via native APIs, or a specific distribution ask) — at that point Capacitor
wraps the same PWA-ready build with comparatively little extra work, since the manifest/
icon work from the PWA pass is directly reusable. This sequencing avoids paying the
store-account/signing/review overhead until there's a concrete reason to.

**Not recommended:** option 3 (forks business logic, explicitly out of scope) or option 4
alone (leaves no path to an app-like or installable experience, which is what "choose a
path" is asking for).

## Suggested first task

Filed as `ai-art-academy/t-066` (see roadmap): add minimal PWA support to kind_robots
(`@vite-pwa/nuxt` + manifest + icon set + basic service worker), scoped to the whole app
(installability is a site-wide concern, not Academy-only — Academy is the driving use
case but the manifest/service-worker live at the app root). `stakes: reversible` —
fully additive, no existing behavior changes if the module is misconfigured or reverted.
