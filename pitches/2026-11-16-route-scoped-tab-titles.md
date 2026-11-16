# Pitch: Tab titles: no more Robots or stale titles on dedicated pages
date: 2026-11-16
project-target: interface-vision
expansion-kind: bug-fix
delivery-status: shipped
status: awaiting-silas

## Delivered change
The app shell only uses the page store title when it describes the current route, so dedicated pages fall back to the site name rather than Robots or the previous page.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5248
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/43855819500
Verified: verifyFrontDoorPolish.test.ts and TypeScript passed in CI; live audit found /login, /build-bench and gated redirects titled Robots before the fix
Art: not-required
Merge: 88b21a1b3703bfd4a46ba1886f65cef6f6633bd7
Playable preview: https://kindrobots.org/build-bench
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-104

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
