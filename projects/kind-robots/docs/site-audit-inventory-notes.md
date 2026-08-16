# Kind Robots site-audit inventory notes

Durable corrections to historical site-audit file inventories live here when the original audit is already closed and rewriting its long task note would add noise.

## 2026-08-07 — `store-butterfly.vue` relocation

`kind-robots/t-027`'s 2026-07-16 RegExp capture-group audit recorded `components/butterfly/store-butterfly.vue` among the live files it inspected. The current Kind Robots tree no longer contains that path; the component now lives at `components/abandonware/butterfly/store-butterfly.vue`.

This is an inventory correction only. It does not reopen t-027's capture-group findings or imply the abandonware component is reachable production UI.

## 2026-08-16 — `/video-generator` path/channel relocation

`kind-robots/t-046`'s 2026-07-26 wiring note (and the 2026-08-16 weekly site audit, `projects/global-ui/AUDIT-REPORT-2026-08-16.md`) recorded `pages/video-generator.vue` wired into the `lab` channel (`content/channels/lab/video-generator.md`, tabKey `video-generator`). The surface has since moved: the live file is `pages/play/video-generator.vue`, registered under the `play` channel (`content/channels/play/video-generator.md`, `utils/dataSurfaceManifest.ts` navEntry `{ channelKey: 'play', tabKey: 'video-generator' }`). `kind-robots/t-014` (2026-08-09) independently confirms the `/play/video-generator` route, but t-046's own note was never corrected to match.

This is an inventory correction only — the feature has been live and reachable throughout under its current path; it does not reopen t-046's wiring work.
