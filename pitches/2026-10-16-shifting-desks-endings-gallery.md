# Pitch: Shifting Desks: endings gallery on the front desk
date: 2026-10-16
project-target: shifting-desks
expansion-kind: collectible gallery
delivery-status: shipped
status: awaiting-silas

## Delivered change
A trophy button on the front desk opens a gallery of all ten endings: found ones show their epilogue art and title, undiscovered ones stay blurred behind a lock with a hint.

## Evidence
PR: https://github.com/silasfelinus/kind_robots/pull/3753
Checks: https://github.com/silasfelinus/kind_robots/actions/runs/38910391528
Verified: Merged PR's aggregate 'Contract verifiers' check run completed with conclusion success on the final head (Shifting Desks gameplay contract, balance and layout contract included); merge commit confirmed on main. Screens measured at 390, 768, 820 and 1440 px on a local dev build before merge. Merged is not deployed: live on kindrobots.org only after the next Alexandria deploy.
Art: not-required
Merge: 9b72e4f48646ca3fc97fc7a10fa3bad52839d5b1
Playable preview: https://kindrobots.org/play/shifting-desks

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
