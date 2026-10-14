# Pitch: Arcade cabinet and controls fit inside one screen
date: 2026-10-14
project-target: kr-arcade
expansion-kind: viewport fit
delivery-status: shipped
status: awaiting-silas

## Delivered change
Arcade cabinet gains a contained mode that sizes the screen to the measured pane so marquee, screen and Start controls are never clipped. The responsive audit now fails on clipped cabinets at three widths.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/3684
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/38530342805
Verified: Merged PR's aggregate 'Contract verifiers' check run completed with conclusion success; main commit confirmed. PR text states post-deploy 390/820/1440 screenshots are not yet confirmed, so visual acceptance is still open.
Art: not-required
Merge: 98fa6e1b1302a81d1d3db0c0c9561635342d1204

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
