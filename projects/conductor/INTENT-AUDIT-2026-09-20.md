# Portfolio intent audit — 2026-09-20

## Verified

- **Priority and lifecycle:** current `CONTROL.md` and `projects/priority.yaml` agree on the human-steered band `cthulhuquarium → kind-economy → butterfly-gallery → art-archive → mandarin-tutor → interface-vision → coloring-book → humboldt-scoop-cms → digital-storefront → kind-robots → rainbow-butterflies`. The stale `CONTROL_PRIORITY_DRIFT` in the older generated `ROADMAP-AUDIT.md` predates the 2026-09-19 Mandarin correction; current source files are aligned. `project-overrides.yaml` remains authoritative for lifecycle, so finite active work outranks continuous `interface-vision` even though the textual steering band keeps it in place for parity.
- **Cthulhuquarium:** the lead project still targets the actual owner outcome, a fully working browser aquarium, not task-count completion. Its remaining acceptance/gated work is consistent with that definition of done, so keeping it `active` is correct even with no ordinary ready task.
- **Kind Economy:** the second-place tentpole still reflects the later entity decision: near-term for-profit operation with direct Against Malaria giving, while live Stripe, payouts, government filings, and real-money actions remain explicitly gated. Its active lifecycle is still warranted by unfinished live-money/dispersal milestones.
- **Butterfly Gallery:** the 2026-09-18/19 human steering is represented accurately. It is a separate high-priority curation experience consuming Art Archive output; the illustrated `gallery-butterfly-start.png` direction supersedes procedural butterflies; animation jobs are allowed only at ArtJob priority 0 while the broader project remains high agent-work priority. The roadmap's foundation/sort/stage milestones are done and motion/polish remain open, matching current direction.
- **Art Archive:** its boundary still matches the paired Gallery direction: it owns legacy filesystem ingestion, privacy/maturity invariants, provenance reconciliation, curation, and regeneration infrastructure. It remains high-priority active work with regeneration/hardening still open. No Gallery animation or presentation responsibility has leaked into its goal.
- **Mandarin Tutor:** the 2026-09-19 reopening is represented consistently in all three coordination sources. It is active, sits behind the two newly high-priority art projects rather than being silently restored to its old lead slot, and the new m5 comprehension milestone preserves the accepted m1–m4 record while extending the product toward per-character teaching before drilling.
- **Source-of-truth / oversight:** current `PORTFOLIO-OVERSIGHT.md` reports zero Kind Robots↔Conductor parity drift and zero structural errors. The OpenAI scheduled-agent heartbeat is healthy. No Kind Robots-owned presentation fields were copied into Conductor during this review.

## Corrected

- No roadmap mutation was justified. The only apparent deterministic error in the older `ROADMAP-AUDIT.md`, `CONTROL_PRIORITY_DRIFT`, is already repaired in current `CONTROL.md`; changing either source again would reintroduce drift rather than fix it.
- No lifecycle, goal, milestone, gate, or open-task correction had enough evidence to change safely in this cycle.

## Still questionable

- **Kind Economy `t-017`:** the existing warning remains semantically important: completion of a creator-terms drafting task must not be mistaken for human approval or publication of creator policy. The evidence reviewed does not justify rewriting historical task completion or setting `approved_by_human`; any outward-facing use remains a separate human gate.
- **Cthulhuquarium exit representation:** the project can legitimately remain active while its remaining acceptance path is human-facing. If the indirect acceptance dependency persists through the next review, re-check whether the final exit task should carry that acceptance condition directly. Do not bypass the acceptance itself.

## Next review

2026-09-23, or sooner after a new explicit priority, lifecycle, or product-direction decision from Silas.
