# Portfolio Intent Audit — 2026-10-10 (PT)

## Verified

- **Priority and lifecycle source of truth:** `CONTROL.md` and `projects/priority.yaml` agree on the explicitly ordered October 7 lead quartet: kind-pinball → zuzu-lair → kr-arcade → zuzu-showdown. The prior cthulhuquarium → kind-economy → butterfly-gallery → art-archive → mandarin-tutor band follows in the established relative order. The four newly promoted projects are all active. The order is a human direction, not an inference from task counts.
- **FX3 is an acceptance criterion, not a box-check:** kind-pinball still targets *one* AMI Village Rescue table with hidden sub-table and one leaderboard, and awaits Silas's hands-on FX3-quality verdict. Zuzu Pinball, added October 9 at normal priority, is a *separate* table and now specifies the shootable River Croc mouth, ball hold, Death Roll, and safe return. Neither is finished by virtue of a design document or demo.
- **Zuzu projects retain their separate scopes:** zuzu-lair is a branching animated QTE game; zuzu-showdown is an eight-fighter, lighter-toned 2D fighting game. Zuzu: Shifting Lands, also added October 9 at normal priority, follows the latest authored-card decision: no independent species × job randomizer, at least two choices with 2d6 outcomes per encounter, and readable face-up animations with custom backs. Its preview remains admin-only pending a separate release gate.
- **Older tentpoles remain intentional:** cthulhuquarium's public-access/art-acceptance decision remains explicitly human-gated; kind-economy's real-payment, publication and entity/filing gates are still hard gates. Butterfly Gallery owns curation, while Art Archive owns private/mature ingestion and provenance. Mandarin Tutor is active after the September 19 reopening and retains its expanded teaching flow; no task-count-only completion or gate clearance is justified.
- **Deterministic health at the alert:** `PORTFOLIO-OVERSIGHT.md` generated October 9 at 11:01 PM PT reported zero forward project drift, zero reverse orphans, zero structural roadmap errors, and 25 warnings. The 2026-10-09 `ROADMAP-AUDIT.md` snapshot lists advisory stale-claim and gating warnings, not new structural errors. This semantic review addresses the overdue three-day cadence rather than masking those warnings.
- **Production API migration:** Conductor's project-parity reader now calls `https://kindrobots.org/api/conductor/project-parity` (the October 9 oversight completed with zero drift); `fetch_todos.py`, `complete_todo.py`, and `sync_kind_robots_projection.py` default to `kindrobots.org`. Reviewed the oversight, project-sync, and projection workflows; none declares the retired Vercel origin. A regression check now scans operational scripts/workflows for the old hostname, and the projection refuses a `.vercel.app` API override before making a request.

## Corrected

- **Priority metadata drift:** all four projects explicitly named HIGH by Silas on October 7 still had `priority: normal` in `project-overrides.yaml`, even though the queue order was right. Set kind-pinball, zuzu-lair, kr-arcade and zuzu-showdown to `priority: high`. Added a regression assertion alongside the existing human-priority ordering test to keep the projected priority fields aligned with the human decision.
- **Legacy-origin safety:** the projection's optional `KR_API_BASE` override previously accepted a retired Vercel address even though the default had migrated. Refuse Vercel-hosted overrides before network I/O; assert the self-hosted outbound endpoints and absence of the old hostname from scheduled runnable files.

## Still questionable

- The 25 structural-audit warnings warrant their own scoped claim/gate cleanup; they are not evidence that the current human priority order or lifecycle should be rewritten en masse.
- Game play quality, live Cthulhuquarium access, and payment/publishing outcomes require their already-recorded acceptance gates. This review does not silently convert PR completion into product acceptance.
- This is a source-and-workflow audit, not a claim that every third-party historical reference has been migrated. The new CI guard specifically covers runnable Conductor scripts and workflows, including future additions.

No new FOR SILAS choice is required for this review.

## Next review

2026-10-13 PT, or earlier if the user changes priority, lifecycle, or product direction.
