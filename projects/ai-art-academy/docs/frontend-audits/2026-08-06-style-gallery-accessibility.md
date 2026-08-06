# Academy Style Gallery disclosure audit

Date: 2026-08-06
Task: `ai-art-academy/t-010`
Lane: 1, front-end polish

## Surface inspected

`kind_robots/components/academy/academy-styles-browser.vue` on current `main`.

The style gallery already has unusually good keyboard basics: every lesson tile is a real button, Escape closes the expanded lesson, focus returns to the originating tile, progress filters expose `aria-pressed`, and search/results use explicit labels and a polite live summary.

## Verified defect

Every lesson tile always renders:

```vue
:aria-controls="`academy-style-detail-${style.slug}`"
```

The controlled detail element is rendered only while that lesson is expanded:

```vue
<div v-if="expandedStyle" :id="`academy-style-detail-${expandedStyle.slug}`">
```

For every collapsed tile, `aria-controls` therefore references an element that does not exist in the accessibility tree or DOM. This makes the disclosure relationship inaccurate for assistive technology and creates dozens of broken ID references on initial render.

## Recommended repair

Keep `aria-expanded` on every lesson tile, but bind `aria-controls` only for the currently expanded tile:

```vue
:aria-controls="
  expandedSlug === style.slug
    ? `academy-style-detail-${style.slug}`
    : undefined
"
```

This is a small reversible Kind Robots change. Add a focused verifier or component test that asserts collapsed cards omit `aria-controls` and the expanded card points to the live detail ID. Do not solve this by permanently mounting every detail panel; that would increase DOM weight and duplicate hidden lesson content.

## Scope boundary

No change was made directly to Kind Robots in this cycle because the connector runtime could inspect repository files and coordinate Conductor state but did not provide a local Vue test runner or browser-preview workflow suitable for safely validating a template edit. The verified defect and exact repair are now durable rather than being left as chat exhaust.

No production data, ArtJobs, publishing, secrets, billing, DNS, or account configuration were touched.
