# Roadmap intent audit — 2026-09-01

Session: `openai-scheduled-20260901T161342Z-intent-audit-q7m4`

## Verified

- The current steering sources agree on the lead queue. `CONTROL.md` now names Mandarin Tutor → Cthulhuquarium → Kapowarr → Kind Economy → Interface Vision → AI Art Academy → Coloring Book → Humboldt Scoop CMS, matching the first eight entries in `projects/priority.yaml`. This closes the priority-sheet inconsistency recorded in the 2026-08-29 intent audit rather than carrying it forward.
- Mandarin Tutor still matches the latest explicit product intent. Its roadmap goal and notes prioritize a visual, trustworthy Mandarin study loop with decomposition/history, pronunciation/audio, generated art, broad practical vocabulary, custom/requested words, and a deliberately simple canonical-card curation model. The tutor-facing requested-word loop and curation work have landed; its remaining open work is human-gated steering rather than a hidden implementation queue.
- Cthulhuquarium still matches the current direction and repo split. The browser game remains in Kind Robots at `/play/aquarium`; `silasfelinus/cthulhuquarium` remains the portable data canon rather than a second game implementation. The roadmap still encodes the human decisions that fish do not die, progress does not degrade, the bestiary is the collection win state, and the `Monster` model is separate from conversational Characters.
- Kapowarr still reflects the latest aggregation-first direction: harden and broaden the acquisition fabric first, then discovery/curation and metadata resilience, with reader polish and multi-user work secondary. Its active milestones are ACQUIRE and SOURCES, consistent with that direction; the completed discovery/metadata milestones do not falsely imply the acquisition fabric is finished.
- Kind Economy remains intentionally blocked on real human/payment decisions rather than being silently advanced by automation. The roadmap preserves the for-profit-near-term / direct Against Malaria donation default, the per-interaction-accrual question, CPA confirmation, and the explicit prohibition on live/test Stripe actions without concrete approval.
- Interface Vision remains correctly active despite high task completion. Its goal is outcome-based beta readiness, phase 3 remains in progress, and recurring `t-104`/`t-105` are consistency/polish umbrellas rather than completion counters. The current STATUS snapshot shows `t-104` ready, so finite active work remains available after the higher-priority projects' currently gated queues.
- The current portfolio sensor reports zero Kind Robots ↔ Conductor scaffold drift and zero structural roadmap errors. No open PR exists in Conductor or Kind Robots at the start of this audit, so there was no reviewable implementation work that should have preempted the semantic review.

## Corrected

- No unambiguous roadmap or lifecycle correction was needed in this pass. The stale CONTROL priority band identified on 2026-08-29 is already repaired, and the current structural/parity sensors are clean.

## Still questionable

- No new subjective product-direction fork was uncovered that warrants manufacturing a `FOR SILAS:` gate. Existing human gates in Mandarin Tutor and Kind Economy already capture the decisions that genuinely require Silas or professional confirmation.
- Interface Vision's final beta-readiness acceptance remains a real human visual gate. Recurring polish work should continue to produce bounded, evidence-backed slices, but it should not be used to postpone that acceptance indefinitely once the finite visual criteria are actually satisfied.

## Next review

2026-09-04, or sooner after another explicit priority, lifecycle, or major product-direction change.
