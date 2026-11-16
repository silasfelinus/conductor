# Pitch: Front door: sign-in page names where you were headed
date: 2026-11-16
project-target: interface-vision
expansion-kind: front-door
delivery-status: shipped
status: awaiting-silas

## Delivered change
Signed-out visitors bounced from a gated link to /login now see a real tab title and a note naming the page they were opening instead of a tab titled Robots.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5248
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/43855819500
Verified: verifyLoginDestination.test.ts passed locally and in contract shard 4; same-origin redirect parsing covered
Art: not-required
Merge: 88b21a1b3703bfd4a46ba1886f65cef6f6633bd7
Playable preview: https://kindrobots.org/login?redirect=/play/slime-city
Canonical roadmap: projects/interface-vision/roadmap.yaml task t-151

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
