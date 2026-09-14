# Roadmap intent audit — 2026-09-14

Session: `openai-manual-20260914T0615Z-oversight-fix`

## Verified

- Current human steering and deterministic priority agree on the lead queue: Cthulhuquarium → Kind Economy → Interface Vision → Coloring Book → Humboldt Scoop CMS → Digital Storefront → Kind Robots → Rainbow Butterflies. `CONTROL.md` and the head of `projects/priority.yaml` match exactly for that band.
- The major 2026-09-11 direction changes are reflected rather than being treated as stale task-count churn: Mandarin Tutor and Kapowarr were accepted and moved to `finished`; AI Art Academy was explicitly closed as an outdated test project; Mermaids of Venice was paused; Cthulhuquarium inherited the lead and Kind Economy inherited second place without inventing a new ordering decision.
- Later lifecycle steering is also represented: DaVinci is retired into Storybook's `life` shape, and Mural Design is paused while its current direction is retired. Neither remains in the selectable priority queue.
- The latest persisted portfolio sensor reports zero roadmap errors, zero Kind Robots → Conductor forward drift, zero reverse project orphans, and a healthy OpenAI scheduled-agent heartbeat. The seven roadmap findings are warning-level rather than direction drift.
- Coloring Book remains active and correctly placed. Its current render-box `hostbuf_file_reader_read failed` recurrence is an operational/hardware incident tracked outside the semantic product-direction decision; it does not justify changing Coloring Book's priority or lifecycle.

## Corrected

- No roadmap direction correction was required by this semantic pass. The September 11–12 human steering has already been propagated into `CONTROL.md`, `project-overrides.yaml`, and `projects/priority.yaml`.
- The oversight delivery path is being corrected in the same maintenance PR: a semantic review becoming due remains an internal agent-routing signal immediately, while email becomes an escalation after a one-day grace. The active OpenAI Conductor automation was also updated to read `PORTFOLIO-OVERSIGHT.md` and select `roadmap-intent-auditor` ahead of ordinary Worker work when this signal is due.

## Still questionable

- `cthulhuquarium/t-065` is `needs-human` without an obvious hard-gate marker. The structural auditor is correctly asking whether it should instead be `ready`, carry `soft_gate: true`, or document the concrete human gate.
- Six completed human-gated tasks lack `approved_by_human: true`: `davinci/t-022`, `kind-economy/t-017`, and `kindrobots-unraid/t-014`, `t-015`, `t-017`, `t-018`. These are bookkeeping/provenance warnings, not current product-direction drift; review their close-out evidence rather than reopening them automatically.
- No new subjective product-direction choice was found that warrants a fresh `FOR SILAS:` gate.

## Next review

2026-09-17, or sooner after another explicit priority, lifecycle, or major product-direction change.
