# Pitch: Dead Air: seven-day runway filled with The Empty Chair Rental
date: 2026-11-19
project-target: dead-air
expansion-kind: content
delivery-status: shipped
status: awaiting-silas

## Delivered change
Authored the missing 2026-11-25 private five-shot brief, an early-1960s department-store ad for rented holiday dinner guests, restoring the full seven-day film runway.

## Evidence
PR: https://github.com/silasfelinus/conductor/pull/7613
Checks: https://github.com/silasfelinus/conductor/actions/runs/44499604066
Verified: check_dead_air_runway.py --days 7 reports 7/7; dead_air_produce --dry-run passes; tests/test_dead_air.py passes; authored only, not rendered
Art: not-required
Merge: d22d072df89d95a24013e1bdb0496d4df5c11278
Canonical roadmap: projects/dead-air/roadmap.yaml task t-004

## Review after the work
Approve = keep, approve with changes = revise, pass = request a scoped, CI-verified rollback. Rejections never directly delete production data.
