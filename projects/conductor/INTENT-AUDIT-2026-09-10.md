# Roadmap intent audit — 2026-09-10

Session: `openai-manual-20260910T0646Z-oversight-k7q2`

## Verified

- Current steering still agrees on the lead finite queue: Mandarin Tutor → Cthulhuquarium → Kapowarr → Kind Economy → Interface Vision → AI Art Academy → Coloring Book → Humboldt Scoop CMS. `CONTROL.md`, `project-overrides.yaml`, and `projects/priority.yaml` still agree on that direction; no newer explicit human steering found in the reviewed recent history reverses the order.
- Mandarin Tutor still matches the stated learning goal: visual vocabulary, pronunciation/audio, trustworthy decomposition/history, broad practical and specialist sets, requested/custom words, durable generated art, and proficiency-test alignment. All 20 implementation tasks are done; `t-021` is now the explicit closing visual-acceptance gate added on 2026-09-07, so keeping the project active is intentional rather than hidden implementation debt.
- Cthulhuquarium still matches the latest product direction: the playable browser game lives in Kind Robots, the companion repository is portable data canon, progress never decays, and the collectible bestiary/idle loop remains the center. Recent `t-019` and `t-041` close-outs advanced balance/endgame and hidden-event work without changing that direction; m3 remains the unfinished polish/ship milestone.
- Kapowarr still matches the aggregation-first direction. Recent source-expansion work closed m8, while m5 ACQUIRE remains the major incomplete milestone. That is consistent with prioritizing the acquisition fabric rather than reopening already-landed reader/metadata polish.
- Kind Economy remains correctly constrained by the explicit money gates. The append-only split/ledger design work has progressed, but first-dollar, entity, payment, payout, and remittance actions remain human-gated. No reviewed recent history justifies letting an autonomous agent cross those boundaries.
- Interface Vision remains correctly active as an outcome/consistency project despite the high done count. `t-104` is a recurring bounded consistency sweep and was claimed by the live Claude scheduled session `claude-scheduled-20260910T063151Z-t104s197` during this audit, so this session deliberately did not collide with it.
- Kind Robots ↔ Conductor project parity was clean in the latest persisted portfolio sensor: zero forward drift and zero reverse orphans. The sensor also reported zero roadmap errors; the two `kindrobots-unraid` findings are warning-level recovery bookkeeping, not evidence that recovered incidents should be reopened.
- The repeatedly paused OpenAI scheduled agent is not failing before GitHub access. Its 2026-09-10 05:11Z cycle successfully created a session-marked claim event for `interface-vision/t-104`, the event processor applied it, and the same cycle created a session-marked rearm event. The run then stopped after treating a truncated `assets/css/tailwind.css` Contents API response as a safe connector limitation. A later shell-capable Claude cycle completed the exact same scoped slice as Kind Robots PR #2577 and Conductor PR #4000.

## Corrected

- Found a real oversight-report persistence defect while following the audit trail. `.github/workflows/roadmap-audit.yml` generated fresh `ROADMAP-AUDIT.json` and `ROADMAP-AUDIT.md` on its daily schedule but only uploaded them as artifacts; its only commit step was hard-coded to the original `worker/roadmap-audit-2026-07-12` PR branch. As a result, checked-in `ROADMAP-AUDIT.md` remained frozen at 2026-08-30 even while `PORTFOLIO-OVERSIGHT.md` told agents to read it for current warning details.
- Conductor PR #4002 repairs that path: scheduled and main-ref manual Roadmap Audit runs now persist the generated snapshot with the same fetch/rebase/normal-push retry pattern used by Conductor Oversight. Checkout gains full history for that safe rebase. PR/manual runs on non-main refs cannot push the snapshot to main.

## Still questionable

- The ChatGPT `OpenAI Conductor Hourly Agent` continues to auto-pause after a short cycle. The repo evidence narrows the failure substantially: the 05:11Z scheduled cycle did real GitHub writes, safely re-armed its own claim, then stopped instead of following the connector runbook's instruction that truncation is not a blocker and rotating to another eligible task. The task was disabled minutes later. GitHub app permissions are already set to allow all actions, so ordinary GitHub write approval is not the explanation. This is now a ChatGPT scheduled-task execution/continuation problem, not a Conductor queue or GitHub-auth problem; repo code cannot keep a platform task enabled.
- `ROADMAP-AUDIT.md` will remain the old checked-in snapshot until the repaired scheduled/manual-main persistence path actually executes after PR #4002 lands. Until then, `PORTFOLIO-OVERSIGHT.json` is the fresher deterministic warning source.
- No new subjective product-direction choice was found that warrants another `FOR SILAS:` gate.

## Next review

2026-09-13, or sooner after another explicit priority, lifecycle, or major product-direction change.
