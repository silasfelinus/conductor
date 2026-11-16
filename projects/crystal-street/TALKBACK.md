# Crystal Street TALKBACK

Append-only critique log for this project. Format: AGENTS.md "How to write a talkback entry".

## 2026-11-16 PT — Reviewer — t-024 scrapbook silhouettes (kind_robots#5240) — MERGED

- **Decision:** merged (squash de95ff2). Reversible, scoped UI slice implementing Silas's 2026-11-12 "Yes on crystal street silhouettes" decision for nightmares and friends; all 14 checks green on the head SHA.
- **Good:** `discoveryProgress` filters against the live catalog, so duplicate or obsolete save IDs can't inflate X/N. The new regression test is wired into the gameplay workflow, and the PR said plainly that no browser verification was possible.
- **Gap:** spoiler safety is only shown at the unit level. Nothing rendered checks that a locked slot never exposes a name or portrait path. Kaizen t-026 covers it.
- **Scope note:** the worker flagged this as one slice of the t-024 umbrella and asked for it to go back to ready, not done. That's the right discipline. Ending silhouettes are still outstanding.
