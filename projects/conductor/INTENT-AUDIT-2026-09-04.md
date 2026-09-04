# Roadmap intent audit — 2026-09-04

Session: `openai-scheduled-20260904T211223Z-intent-audit-q7m4`

## Verified

- Current steering still agrees on the lead finite queue: Mandarin Tutor → Cthulhuquarium → Kapowarr → Kind Economy → Interface Vision → AI Art Academy → Coloring Book → Humboldt Scoop CMS. `CONTROL.md` and `projects/priority.yaml` match on that prefix, so there is no priority-order correction to manufacture.
- Mandarin Tutor still matches Silas's stated learning goal: visual vocabulary, pronunciation/audio, trustworthy component/history explanations, broad practical sets, requested/custom words, durable generated art, and eventual proficiency-test alignment. The current roadmap has no ordinary ready implementation task; remaining steering is human-gated rather than a hidden build queue.
- Cthulhuquarium still matches the latest product direction: the playable browser game belongs in Kind Robots while the companion `silasfelinus/cthulhuquarium` repository remains portable data canon. The roadmap still preserves the darkly funny idle-aquarium loop, persistent/browsable tanks, collectible monster fish, no-death/no-decay decisions, and shared bestiary direction.
- Kapowarr remains aligned with the explicit aggregation-first direction. ACQUIRE and SOURCES are still the incomplete milestones while discovery/curation, metadata resilience, and reader follow-ups are recorded as landed; that is consistent with prioritizing the acquisition fabric over deeper reader polish or multi-user work.
- Kind Economy remains intentionally gated around real money. Its roadmap still correctly prohibits live or test Stripe actions, payouts, government filings, account creation, or other financial actions without concrete human approval, while keeping the near-term for-profit/direct-AMF-donation direction explicit.
- Interface Vision remains correctly active despite a high done-task count. The project is an outcome-based beta-readiness effort, not a task-count project, so it should not be marked finished merely because its recurring consistency slices have consumed most of the queue.
- Kind Robots ↔ Conductor project parity is currently clean: the portfolio sensor reports zero forward drift and zero reverse orphan projects. The OpenAI scheduled heartbeat is also current.
- There were no open PRs in Conductor or Kind Robots at the start of this audit, so no reviewable implementation work was being skipped to perform the due semantic review.

## Corrected

- No lifecycle, priority, or product-direction bookkeeping needed a semantic correction in this pass.
- The portfolio sensor does contain one deterministic structural error, `kindrobots-unraid/t-014` (`GATED_DONE_WITHOUT_APPROVAL`). This is not evidence that the incident should be reopened: `docs/state-reconciliation.md` explicitly allows a production incident recovery task to close when its documented recovery criteria are objectively met, even when root cause remains unknown. The task itself records that `/` and `/api/health/database` recovered to HTTP 200 and deliberately preserves `approved_by_human: false` because no policy/irreversible action was approved. The audit rule is therefore stricter than the documented reconciliation contract for this recovery-only case. This needs an audit-rule repair, not falsifying human approval or reopening a recovered outage.

## Still questionable

- `kindrobots-unraid/t-014` exposes a narrow framework ambiguity: the roadmap auditor currently treats every `gate_human: true` + `status: done` + `approved_by_human: false` combination as an error, while the reconciliation contract explicitly permits objective incident-recovery closure. The right follow-up is to give the auditor an explicit, narrow recovery-resolution marker/exception rather than weakening human gates generally.
- `animation-manager/t-006` is reported as having remained in `review` for five days. That is stale coordination and should be handled by a review/branch medic before ordinary continuous work when the next cycle can inspect its implementation PR/branch evidence.
- No new subjective product-direction choice was found that warrants a new `FOR SILAS:` gate.

## Next review

2026-09-07, or sooner after another explicit priority, lifecycle, or major product-direction change.
