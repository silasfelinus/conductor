# Pitch: Arcade: live cold-open probe for shared showcase links
date: 2026-11-16
project-target: kr-arcade
expansion-kind: reliability
delivery-status: shipped
status: awaiting-silas

## Delivered change
A new live probe opens every showcase cabinet from a shared link in a fresh phone and tablet browser and reports login walls, errors, missing canvas or overflow.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/5248
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/43855819500
Verified: node utils/scripts/checkArcadeColdOpenLive.mjs against production: 22/22 clean at 390x844 and 768x1024
Art: not-required
Merge: 88b21a1b3703bfd4a46ba1886f65cef6f6633bd7
Playable preview: https://kindrobots.org/play/arcade?game=pipe-pals
Canonical roadmap: projects/kr-arcade/roadmap.yaml task t-169

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
