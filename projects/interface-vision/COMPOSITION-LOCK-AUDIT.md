# Composition-Lock Audit

Date: 2026-08-02
Task: interface-vision/t-023
Target repository snapshot: `silasfelinus/kind_robots@a3f9de1eaa79d7ca2e8e1643e15bd46d24cf52ee`

## Purpose

Identify files still present in `utils/scripts/layout-contract-baseline.json` whose current layout markup is also pinned by another verifier or workflow. These files need a companion contract update when t-017 removes their layout violation; changing the Vue markup alone will otherwise fail an unrelated migration or product contract.

## Confirmed layout-sensitive lock

| Baseline file | Baseline rules | Lock | Required companion change |
| --- | --- | --- | --- |
| `components/pages/serendipity-page.vue` | `one-header`, `one-scroll` | `utils/scripts/verifySerendipityRouteCutover.mjs` asserts the exact string `<h1 class="text-2xl font-black tracking-tight">Serendipity</h1>`. The workflow `.github/workflows/serendipity-route-contract.yml` runs that verifier. | Replace the exact-markup assertion with a semantic Serendipity identity assertion in the same PR that removes/demotes the duplicate page header. Keep the route, tab, dashboard and obsolete-route assertions intact. |

This is the only confirmed verifier that pins a layout token for a file still in the current allow-list.

## References that are not layout locks

These baseline files are read by other contracts, but the assertions concern behavior or wiring rather than the layout markup t-017 is expected to change.

| Baseline file | Reference | Why it is not currently a companion-layout change |
| --- | --- | --- |
| `pages/play/video-generator.vue` | `utils/scripts/verifyMaturityPrivacyContract.ts` | Pins maturity controls and payload fields, not headers, scroll ownership, viewport sizing, or root wrappers. Preserve those controls during the layout edit; the verifier should not need alteration. |
| `components/pages/conductor-page.vue` | `utils/scripts/verifyEntityArtManager.ts` and data-surface registration | References the component as an integration surface, but no current evidence found of an exact header or scroll-class assertion. Re-run the existing contract after changes; do not pre-emptively weaken it. |

## No direct verifier/workflow lock found

The current code index showed no direct `verify*` or workflow reference that pins layout markup for the remaining allow-list entries. This includes:

- `components/conductor/project-front-page.vue`
- `components/pages/registration-form.vue`
- the four `pages/admin/wonderlab-review*.vue` pages
- all remaining `one-scroll` entries other than Serendipity and Conductor Page
- `components/servers/chat-test.vue`
- `components/wonderlab/new-eyeball.vue`
- the current `one-mdc`, `ghost-prop`, and `zero-scroll` entries

“No direct lock found” is not permission to edit blindly. t-017 should still run the full PR check set because contracts can refer to component behavior without naming the file, and Vue composition can couple parent and child markup.

## t-017 checklist

1. Handle `serendipity-page.vue` with `verifySerendipityRouteCutover.mjs` in the same commit or PR.
2. Preserve the mature-content controls in `video-generator.vue`; its contract is behavioral and should remain green unchanged.
3. Run `npm run test:layout-contract`, the full TypeScript check, and all normal PR workflows after each scoped batch.
4. Shrink `layout-contract-baseline.json`; never replace a removed violation with a new exemption.
5. When a new failure reveals another exact-markup lock, update this audit and the owning contract rather than restoring obsolete layout markup.

## Evidence inspected

- `utils/scripts/layout-contract-baseline.json`
- `.github/workflows/serendipity-route-contract.yml`
- `utils/scripts/verifySerendipityRouteCutover.mjs`
- `utils/scripts/verifyMaturityPrivacyContract.ts`
- current GitHub code-index references for `serendipity-page.vue`, `registration-form.vue`, `video-generator.vue`, and `conductor-page.vue`
