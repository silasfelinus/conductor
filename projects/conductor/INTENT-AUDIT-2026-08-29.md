# Roadmap intent audit — 2026-08-29

Session: `openai-scheduled-20260829T181312Z-oversight-k4m7`

## Verified

- The portfolio priority source is internally inconsistent today. `CONTROL.md` still names the older Interface Vision-led band, while `projects/priority.yaml` records a newer explicit human decision dated 2026-08-25: Mandarin Tutor first, Cthulhuquarium second, Kapowarr third, Kind Economy fourth. Commit `bcdc15e` / PR #2892 also added a contract test locking the new top pair, so the newer direction is well evidenced rather than inferred from task churn.
- Mandarin Tutor's roadmap still matches that priority decision. Its goal is a visual Mandarin learning system with trustworthy vocabulary, pronunciation, decomposition/history, art, durable audio, curation, and proficiency progression; the high-priority tutor-facing requested-word loop and catalog curation work have landed. Current remaining work is predominantly human-gated rather than evidence that the goal silently changed.
- Cthulhuquarium's roadmap still matches Silas's stated product direction: a playable darkly funny browser aquarium with persistent tanks, collectible monster-fish, idle economy, decoration, events, and browsable aquariums, with the portable canon living in the companion `cthulhuquarium` repository rather than duplicating game code there.
- Project scaffold parity is mechanically clean in the current portfolio oversight report: zero forward drift and zero reverse orphans.
- The open PR queue contains only conductor #3145. Its previously recorded Windows PowerShell correctness blockers remain unresolved on unchanged work, so repeating another review pass would not advance the repository.
- This completed intent audit landed on `main` through conductor #3175 after Worker PR CI, Security Audit, and Process task events all completed successfully on the exact head.

## Corrected / made actionable

- Opened #3174 for the stale CONTROL priority band, with the exact newer eight-project prefix and evidence needed to repair the highest-precedence steering sheet.
- Opened #3172 for the impossible Interface Vision recurring dependency chain. `t-104` and `t-105` are intentionally recurring and therefore never become `done`, yet `t-105` depends on `t-104` and final human gate `t-106` depends on `t-105`. The issue requires a finite completion/sentinel shape or equivalent explicit criteria rather than pretending a recurring task can satisfy a completion dependency.
- Opened #3173 for `kind-robots/t-071`'s missing human-approval provenance. The task's production outcome really completed because Silas personally ran the migration and health checks recovered, but automation policy forbids manufacturing `approved_by_human: true` retrospectively. The issue preserves the real outcome while routing the provenance fix to a Silas-present session.

## Still questionable

- Interface Vision is still correctly active despite high task completion. Its stated definition of done is outcome-based and includes a final human visual beta-readiness acceptance. The recurring consistency/polish umbrellas should not be used as numeric completion proxies; #3172 is the bookkeeping repair needed before that final gate can be represented cleanly.
- `kind-robots/t-071` should not be reverted to an unfinished production state merely to silence the auditor. The missing approval bit is provenance debt, not evidence that the incident remains broken.

## Next review

2026-09-01, or sooner after another explicit priority/lifecycle change.
