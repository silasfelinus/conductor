# Roadmap audit follow-up — 2026-09-19

## Deterministic drift confirmed

`PORTFOLIO-OVERSIGHT.md` reports `CONTROL_PRIORITY_DRIFT`: `projects/priority.yaml` now includes `mandarin-tutor` immediately after `art-archive`, while CONTROL.md's human-facing priority band still jumps directly from `art-archive` to `interface-vision`.

The newer source is unambiguous. `projects/priority.yaml` records Silas's 2026-09-19 decision to reopen Mandarin Tutor and place it behind the two projects promoted HIGH on 2026-09-18, but ahead of the ordinary finite backlog. The correct repair is therefore to insert `mandarin-tutor` in CONTROL.md after `art-archive`, not to demote it in `projects/priority.yaml`.

## Connector limitation encountered

This connector exposes whole-file replacement for existing files but no line-level patch operation. CONTROL.md is long enough that paged reads are truncated by the transport display budget; replacing it from an incomplete response would risk deleting unrelated human steering. I therefore did not overwrite CONTROL.md merely to silence the sensor.

No lifecycle, roadmap task, or generated STATUS.md was changed. The deterministic correction remains: add `mandarin-tutor` to CONTROL.md's priority band after `art-archive` while preserving the rest of CONTROL.md byte-for-byte.
