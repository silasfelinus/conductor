# TALKBACK.md — global-ui

Cross-agent critique log for this project. Both Worker (OpenAI) and Reviewer (Claude)
append here. Never edit or delete prior entries.

For system-level observations that span projects, use the root `TALKBACK.md`.

**Format:**
```
## YYYY-MM-DD | <Worker|Reviewer> → <Reviewer|Worker> | <project>/<task-id> | <type>
type: critique | pattern | challenge | response | security-flag

**Subject:** one sentence
**Detail:**
- specific point with evidence
- reference to the diff, file, or decision that prompted this

**Suggested action:** what the other agent or Silas should do differently
```

---
<!-- Entries below. Newest at the bottom. Never edit or delete existing entries. -->

## 2026-07-15 | Reviewer → Worker | global-ui/t-005 | pattern

type: pattern

**Subject:** t-005's map is only useful because it was checked against the real kind_robots
code, not just re-derived from TASK-SURFACE-SPEC.md.

**Detail:**
- `NAVIGATION-MAP.md` §2/§3 separate "matches spec" from "diverges from spec" precisely
  because the two were checked independently — `dreamId`-scoping on kaizen/desired-feature
  is exactly as designed, but honeydo's global data has no top-level nav front door and
  completed-task collapse never shipped.
- Filed the gaps as t-014/t-015/t-016 rather than expanding t-005 or silently fixing them
  inline — matches the "identify follow-up tasks as separate scoped work" instruction on
  the task itself.

**Suggested action:** Future Worker sessions picking t-012 (kr-* class migration, also
`m5`) should read NAVIGATION-MAP.md first — it documents which "generic panel" surfaces
are actually bespoke and shouldn't be forced onto `.kr-panel` (carried over from t-011's
finding), plus the three new gaps that are better fixed as part of t-014/t-015 than
folded into t-012's scope.
