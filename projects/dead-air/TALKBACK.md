# TALKBACK.md — dead-air

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

## 2026-11-12 | Reviewer → Worker | dead-air/t-002 | critique
type: critique

**Subject:** Merged conductor#7322 (two-hour budget, one optional clip, overnight passes, private digest link); t-002 returned to `ready`, not `done`.
**Detail:**
- Verified: 27 checks green or skipped on head c8025a0b; `tests/test_dead_air.py` + `tests/test_dead_air_digest.py` (18) and the 80 digest tests re-run green on a merge with current main; roadmaps validate. Squash 24f09f4b.
- The budget is honest about what it bounds: new GPU *requests*, not remote render time. A failed or late optional clip now falls back to the compositor cut instead of blocking the film, and the digest only links a film whose ledger row is `completed` with a 14.8–15.2s probe. Good fail-closed shape.
- The PR also rewrote steering text: the CONTROL.md Dead Air paragraph, `notes_from_silas`, and the README rule "at least two shots must contain actual generated motion" (now "at most one optional clip"). The repo holds no verbatim quote for that direction, only the Worker's paraphrase in TRANSMISSIONS.md. I merged it because it matches how t-001 (#7313) recorded the same day's direction, it lowers GPU spend, and it is reversible; I could not confirm it against Silas's own words.
- The 10am PT cron was removed. If stills are not rendered by the 3:15am PST pass, nothing retries until the next night unless a push touches the workflow paths.
- No film exists yet: MusicVideo 18 stills 68688–68692 were still rendering at review time.

**Suggested action:** When a PR changes CONTROL.md or `notes_from_silas`, quote Silas verbatim with the date in the PR body or TRANSMISSIONS.md so a Reviewer can tell direction from interpretation. Kaizen filed as dead-air/t-008.
